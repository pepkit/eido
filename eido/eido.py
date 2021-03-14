import logging
import os
from copy import deepcopy as dpcpy
from warnings import catch_warnings as cw

import jsonschema
from pandas.core.common import flatten
from ubiquerg import size
from yacman import load_yaml as _load_yaml

from .const import *
from .exceptions import *

_LOGGER = logging.getLogger(__name__)


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
    _LOGGER.debug(f"schema ori: {schema_dict}")
    if "config" in schema_dict[PROP_KEY]:
        schema_dict[PROP_KEY]["_config"] = schema_dict[PROP_KEY]["config"]
        del schema_dict[PROP_KEY]["config"]
    if "samples" in schema_dict[PROP_KEY]:
        schema_dict[PROP_KEY]["_samples"] = schema_dict[PROP_KEY]["samples"]
        del schema_dict[PROP_KEY]["samples"]
        schema_dict["required"][schema_dict["required"].index("samples")] = "_samples"
    if (
        "items" in schema_dict[PROP_KEY]["_samples"]
        and PROP_KEY in schema_dict[PROP_KEY]["_samples"]["items"]
    ):
        s_props = schema_dict[PROP_KEY]["_samples"]["items"][PROP_KEY]
        for prop, val in s_props.items():
            if "type" in val and val["type"] in ["string", "number", "boolean"]:
                s_props[prop] = {}
                s_props[prop]["anyOf"] = [val, {"type": "array", "items": val}]
    _LOGGER.debug(f"schema processed: {schema_dict}")
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

    def _recursively_read_schemas(x, lst):
        if "imports" in x:
            if isinstance(x["imports"], list):
                for sch in x["imports"]:
                    lst.extend(read_schema(sch))
            else:
                raise TypeError("In schema the 'imports' section has " "to be a list")
        lst.append(x)
        return lst

    schema_list = []
    if isinstance(schema, str):
        return _recursively_read_schemas(_load_yaml(schema), schema_list)
    elif isinstance(schema, dict):
        return _recursively_read_schemas(schema, schema_list)
    raise TypeError(
        "schema has to be either a dict, path to an existing "
        "file or URL to a remote one"
    )


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
            raise
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
        _validate_object(project_dict, _preprocess_schema(schema_dict), exclude_case)
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
        sample_dict = (
            project.samples[sample_name]
            if isinstance(sample_name, int)
            else project.get_sample(sample_name)
        )
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
        schema_cpy = _preprocess_schema(dpcpy(schema_dict))
        try:
            del schema_cpy[PROP_KEY]["_samples"]
        except KeyError:
            pass
        if "required" in schema_cpy:
            try:
                schema_cpy["required"].remove("_samples")
            except ValueError:
                pass
        project_dict = project.to_dict()
        _validate_object(project_dict, schema_cpy, exclude_case)
        _LOGGER.debug("Config validation successful")


def validate_inputs(sample, schema):
    """
    Determine which of this Sample's required attributes/files are missing
    and calculate sizes of the inputs.

    The names of the attributes that are required and/or deemed as inputs
    are sourced from the schema, more specifically from required_input_attrs
    and input_attrs sections in samples section. Note, this function does
    perform actual Sample object validation with jsonschema.

    :param peppy.Sample sample: sample to investigate
    :param dict schema: schema dict to validate against
    :return dict: dictionary with validation data, i.e missing,
        required_inputs, all_inputs, input_file_size
    """

    def _get_attr_values(obj, attrlist):
        """
        Get value corresponding to each given attribute.

        :param Mapping obj: an object to get the attributes from
        :param str | Iterable[str] attrlist: names of attributes to
            retrieve values for
        :return dict: value corresponding to
            each named attribute; null if this Sample's value for the
            attribute given by the argument to the "attrlist" parameter is
            empty/null, or if this Sample lacks the indicated attribute
        """
        # If attribute is None, then value is also None.
        if not attrlist:
            return None
        if not isinstance(attrlist, list):
            attrlist = [attrlist]
        # Strings contained here are appended later so shouldn't be null.
        return list(flatten([getattr(obj, attr, "") for attr in attrlist]))

    all_inputs = set()
    required_inputs = set()
    schema = schema[-1]  # use only first schema, in case there are imports
    sample_schema_dict = schema["properties"]["samples"]["items"]
    if FILES_KEY in sample_schema_dict:
        all_inputs.update(_get_attr_values(sample, sample_schema_dict[FILES_KEY]))
    if REQUIRED_FILES_KEY in sample_schema_dict:
        required_inputs = set(
            _get_attr_values(sample, sample_schema_dict[REQUIRED_FILES_KEY])
        )
        all_inputs.update(required_inputs)
    with cw(record=True) as w:
        input_file_size = sum(
            [size(f, size_str=False) or 0.0 for f in all_inputs if f != ""]
        ) / (1024 ** 3)
        if w:
            _LOGGER.warning(
                f"{len(w)} input files missing, job input size was "
                f"not calculated accurately"
            )

    return {
        MISSING_KEY: [i for i in required_inputs if not os.path.exists(i)],
        REQUIRED_INPUTS_KEY: required_inputs,
        ALL_INPUTS_KEY: all_inputs,
        INPUT_FILE_SIZE_KEY: input_file_size,
    }


def inspect_project(p, sample_names=None, max_attr=10):
    """
    Print inspection info: Project or,
    if sample_names argument is provided, matched samples

    :param peppy.Project p: project to inspect
    :param Iterable[str] sample_names: list of samples to inspect
    :param int max_attr: max number of sample attributes to display
    """
    if sample_names:
        samples = p.get_samples(sample_names)
        if not samples:
            print("No samples matched by names: {}".format(sample_names))
            return
        for s in samples:
            print(s.__str__(max_attr=max_attr))
            print("\n")
        return
    print(p)
    return
