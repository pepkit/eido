import logging
import os
import sys
import jsonschema
import logging
import oyaml as yaml
from copy import deepcopy as dpcpy

from logmuse import init_logger
from ubiquerg import VersionInHelpParser
from peppy import Project, Sample

from yacman import load_yaml as _load_yaml

from . import __version__
from .const import *
from .exceptions import *

_LOGGER = logging.getLogger(__name__)

_LEVEL_BY_VERBOSITY = [logging.ERROR, logging.CRITICAL, logging.WARN,
                       logging.INFO, logging.DEBUG]


def build_argparser():
    banner = "%(prog)s - Interact with PEPs"
    additional_description = "\nhttp://eido.databio.org/"

    parser = VersionInHelpParser(
            prog=PKG_NAME,
            description=banner,
            epilog=additional_description,
            version=__version__)

    subparsers = parser.add_subparsers(dest="command")
    parser.add_argument(
            "--verbosity", dest="verbosity",
            type=int, choices=range(len(_LEVEL_BY_VERBOSITY)),
            help="Choose level of verbosity (default: %(default)s)")
    parser.add_argument(
            "--logging-level", dest="logging_level",
            help="logging level")
    parser.add_argument(
            "--dbg", dest="dbg", action="store_true",
            help="Turn on debug mode (default: %(default)s)")
    sps = {}
    for cmd, desc in SUBPARSER_MSGS.items():
        sps[cmd] = subparsers.add_parser(cmd, description=desc, help=desc)
        sps[cmd].add_argument('pep', metavar="PEP",
                              help="Path to a PEP configuration "
                                   "file in yaml format.")

    sps[VALIDATE_CMD].add_argument("-s", "--schema", required=True,
            help="Path to a PEP schema file in yaml format.")

    sps[VALIDATE_CMD].add_argument(
            "-e", "--exclude-case", default=False, action="store_true",
            help="Whether to exclude the validation case from an error. "
                 "Only the human readable message explaining the error will "
                 "be raised. Useful when validating large PEPs.")

    sps[INSPECT_CMD].add_argument(
        "-n", "--sample-name", required=False, nargs="+",
        help="Name of the samples to inspect.")

    group = sps[VALIDATE_CMD].add_mutually_exclusive_group()

    group.add_argument(
        "-n", "--sample-name", required=False,
        help="Name or index of the sample to validate. "
             "Only this sample will be validated.")

    group.add_argument(
        "-c", "--just-config", required=False, action="store_true",
        default=False, help="Whether samples should be excluded from the "
                            "validation.")
    return parser


def _preprocess_schema(schema_dict):
    """
    Preprocess schema before validation for user's convenience

    Preprocessing includes:
    - renaming 'samples' to '_samples' since in the peppy.Project object
        _samples attribute holds the list of peppy.Samples objects.
    - adding array of strings entry for every string specified to accommodate
        subsamples in peppy.Project

    :param dict schema_dict: schema dictionary to preprocess
    :return dict: preprocessed schema
    """
    _LOGGER.debug("schema ori: {}".format(schema_dict))
    if "samples" in schema_dict[PROP_KEY]:
        schema_dict[PROP_KEY]["_samples"] = \
            schema_dict[PROP_KEY]["samples"]
        del schema_dict[PROP_KEY]["samples"]
        schema_dict["required"][schema_dict["required"].index("samples")] = \
            "_samples"
    if "items" in schema_dict[PROP_KEY]["_samples"] \
            and PROP_KEY in schema_dict[PROP_KEY]["_samples"]["items"]:
        s_props = schema_dict[PROP_KEY]["_samples"]["items"][PROP_KEY]
        for prop, val in s_props.items():
            if "type" in val and val["type"] in ["string", "number", "boolean"]:
                s_props[prop] = {}
                s_props[prop]["anyOf"] = [val, {"type": "array", "items": val}]
    return schema_dict


def read_schema(schema):
    """
    Safely read schema from YAML-formatted file.

    If the schema imports any other schemas, they will be read recursively.

    :param str | Mapping schema: path to the schema file
        or schema in a dict form
    :return list[dict]: read schemas
    :raise TypeError: if the schema arg is neither a Mapping nor a file path or
        if the 'imports' sections in any of the schemas is not a list
    """
    schema_list = []
    if isinstance(schema, str):
        s = _load_yaml(schema)
        if "imports" in s:
            if isinstance(s["imports"], list):
                for sch in s["imports"]:
                    schema_list.extend(read_schema(sch))
            else:
                raise TypeError("'imports' section has to be a list")
        schema_list.append(s)
        return schema_list
    elif isinstance(schema, dict):
        schema_list.append(schema)
        return schema_list
    raise TypeError("schema has to be either a dict, path to an existing "
                    "file or URL to a remote one")


def _validate_object(object, schema, exclude_case=False):
    """
    Generic function to validate object against a schema

    :param Mapping object: an object to validate
    :param str | dict schema: schema dict to validate against or a path to one
    :param bool exclude_case: whether to exclude validated objects
        from the error. Useful when used ith large projects
    """
    try:
        jsonschema.validate(object, schema)
    except jsonschema.exceptions.ValidationError as e:
        if not exclude_case:
            raise e
        raise jsonschema.exceptions.ValidationError(e.message)


def validate_project(project, schema, exclude_case=False):
    """
    Validate a project object against a schema

    :param peppy.Sample project: a project object to validate
    :param str | dict schema: schema dict to validate against or a path to one
    :param bool exclude_case: whether to exclude validated objects
    from the error. Useful when used ith large projects
    """
    schema_dicts = read_schema(schema=schema)
    for schema_dict in schema_dicts:
        project_dict = project.to_dict()
        _validate_object(project_dict, _preprocess_schema(schema_dict),
                         exclude_case)
        _LOGGER.debug("Project validation successful")


def validate_sample(project, sample_name, schema, exclude_case=False):
    """
    Validate the selected sample object against a schema

    :param peppy.Project project: a project object to validate
    :param str | int sample_name: name or index of the sample to validate
    :param str | dict schema: schema dict to validate against or a path to one
    :param bool exclude_case: whether to exclude validated objects
        from the error. Useful when used ith large projects
    """
    schema_dicts = read_schema(schema=schema)
    for schema_dict in schema_dicts:
        schema_dict = _preprocess_schema(schema_dict)
        sample_dict = project.samples[sample_name] \
            if isinstance(sample_name, int) else project.get_sample(sample_name)
        sample_schema_dict = schema_dict[PROP_KEY]["_samples"]["items"]
        _validate_object(sample_dict, sample_schema_dict, exclude_case)
        _LOGGER.debug("'{}' sample validation successful".format(sample_name))


def validate_config(project, schema, exclude_case=False):
    """
    Validate the config part of the Project object against a schema

    :param peppy.Project project: a project object to validate
    :param str | dict schema: schema dict to validate against or a path to one
    :param bool exclude_case: whether to exclude validated objects
        from the error. Useful when used ith large projects
    """
    schema_dicts = read_schema(schema=schema)
    for schema_dict in schema_dicts:
        schema_cpy = dpcpy(schema_dict)
        try:
            del schema_cpy[PROP_KEY]["samples"]
        except KeyError:
            pass
        if "required" in schema_cpy:
            try:
                schema_cpy["required"].remove("samples")
            except ValueError:
                pass
        project_dict = project.to_dict()
        _validate_object(project_dict, schema_cpy, exclude_case)
        _LOGGER.debug("Config validation successful")


def main():
    """ Primary workflow """
    parser = build_argparser()
    args, remaining_args = parser.parse_known_args()
    # Set the logging level.
    if args.dbg:
        # Debug mode takes precedence and will listen for all messages.
        level = args.logging_level or logging.DEBUG
    elif args.verbosity is not None:
        # Verbosity-framed specification trumps logging_level.
        level = _LEVEL_BY_VERBOSITY[args.verbosity]
    else:
        # Normally, we're not in debug mode, and there's not verbosity.
        level = LOGGING_LEVEL

    logger_kwargs = {"level": level, "devmode": args.dbg}
    init_logger(name="peppy", **logger_kwargs)
    global _LOGGER
    _LOGGER = init_logger(name=PKG_NAME, **logger_kwargs)
    _LOGGER.debug("Creating a Project object from: {}".format(args.pep))
    p = Project(args.pep)
    if args.command == VALIDATE_CMD:
        if args.sample_name:
            try:
                args.sample_name = int(args.sample_name)
            except ValueError:
                pass
            _LOGGER.debug("Comparing Sample ('{}') in the Project ('{}') "
                          "against a schema: {}.".
                          format(args.sample_name, args.pep, args.schema))
            validate_sample(p, args.sample_name, args.schema, args.exclude_case)
        elif args.just_config:
            _LOGGER.debug("Comparing config ('{}') against a schema: {}.".
                          format(args.pep, args.schema))
            validate_config(p, args.schema, args.exclude_case)
        else:
            _LOGGER.debug("Comparing Project ('{}') against a schema: {}.".
                          format(args.pep, args.schema))
            validate_project(p, args.schema, args.exclude_case)
        _LOGGER.info("Validation successful")
    if args.command == INSPECT_CMD:
        # TODO: add more detailed Project info
        if args.sample_name:
            samples = p.get_samples(args.sample_name)
            for s in samples:
                print(s)
                print("\n")
            sys.exit(0)
        print(p)
