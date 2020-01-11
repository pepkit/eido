import logging
import os
import jsonschema
import oyaml as yaml

import logmuse
from ubiquerg import VersionInHelpParser
from peppy import Project

from . import __version__
from .const import *

_LOGGER = logging.getLogger(__name__)


def build_argparser():
    banner = "%(prog)s - validate project metadata against a schema"
    additional_description = "\nhttps://github.com/pepkit/eido"

    parser = VersionInHelpParser(
            prog=PKG_NAME,
            description=banner,
            epilog=additional_description)

    parser.add_argument(
            "-V", "--version",
            action="version",
            version="%(prog)s {v}".format(v=__version__))

    parser.add_argument(
            "-p", "--pep", required=True,
            help="PEP configuration file in yaml format.")

    parser.add_argument(
            "-s", "--schema", required=True,
            help="PEP schema file in yaml format.")

    return parser


def _preprocess_schema(schema_dict):
    """
    Preprocess schema before validation for user's convenience

    Preprocessing includes: renaming 'samples' to '_samples'
    since in the peppy.Project object _samples attribute holds the list of peppy.Samples objects.
    :param dict schema_dict: schema dictionary to preprocess
    :return dict: preprocessed schema
    """
    _LOGGER.debug("schema ori: {}".format(schema_dict))
    if "samples" in schema_dict["properties"]:
        schema_dict["properties"]["_samples"] = schema_dict["properties"]["samples"]
        del schema_dict["properties"]["samples"]
        schema_dict["required"][schema_dict["required"].index("samples")] = "_samples"
    _LOGGER.debug("schema edited: {}".format(schema_dict))
    return schema_dict


def _load_yaml(filepath):
    """
    Read a YAML file

    :param str filepath: path to the file to read
    :return dict: read data
    """
    with open(filepath, 'r') as f:
        data = yaml.safe_load(f)
    return data


def validate_project(project, schema):
    """
    Validate a project object against a schema

    :param peppy.Project project: a project object to validate
    :param str | dict schema: schema dict to validate against or a path to one
    :return:
    """
    if isinstance(schema, str) and os.path.isfile(schema):
        schema_dict = _load_yaml(schema)
    elif isinstance(schema, dict):
        schema_dict = schema
    else:
        raise TypeError("schema has to be either a dict or a path to an existing file")
    project_dict = project.to_dict()
    jsonschema.validate(project_dict, _preprocess_schema(schema_dict))


def main():
    """ Primary workflow """
    parser = logmuse.add_logging_options(build_argparser())
    args, remaining_args = parser.parse_known_args()
    logger_kwargs = {"level": args.verbosity, "devmode": args.logdev}
    logmuse.init_logger(name="peppy", **logger_kwargs)
    logmuse.init_logger(name=PKG_NAME, **logger_kwargs)
    global _LOGGER
    _LOGGER = logmuse.logger_via_cli(args)
    _LOGGER.debug("Creating a Project object from: {}".format(args.pep))
    p = Project(args.pep)
    _LOGGER.debug("Comparing the Project ('{}') against a schema: {}.".format(args.pep, args.schema))
    validate_project(p, args.schema)
    _LOGGER.info("Validation successful")
