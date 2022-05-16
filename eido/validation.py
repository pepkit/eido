import os
from copy import deepcopy as dpcpy
from logging import getLogger
from warnings import catch_warnings as cw

import jsonschema
from pandas.core.common import flatten
from ubiquerg import size

from .const import (
    ALL_INPUTS_KEY,
    FILES_KEY,
    INPUT_FILE_SIZE_KEY,
    MISSING_KEY,
    PROP_KEY,
    REQUIRED_FILES_KEY,
    REQUIRED_INPUTS_KEY,
)
from .schema import preprocess_schema, read_schema

_LOGGER = getLogger(__name__)


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
        _validate_object(project_dict, preprocess_schema(schema_dict), exclude_case)
        _LOGGER.debug("Project validation successful")


def _validate_sample_object(sample, schemas, exclude_case=False):
    """
    Internal function that allows to validate a peppy.Sample object without
    requiring a reference to peppy.Project.

    :param peppy.Sample sample: a sample object to validate
    :param list[dict] schemas: list of schemas to validate against or a path to one
    :param bool exclude_case: whether to exclude validated objects
        from the error. Useful when used ith large projects
    """
    for schema_dict in schemas:
        schema_dict = preprocess_schema(schema_dict)
        sample_schema_dict = schema_dict[PROP_KEY]["_samples"]["items"]
        _validate_object(sample, sample_schema_dict, exclude_case)
        _LOGGER.debug(
            f"{getattr(sample, 'sample_name', '')} sample validation successful"
        )


def validate_sample(project, sample_name, schema, exclude_case=False):
    """
    Validate the selected sample object against a schema

    :param peppy.Project project: a project object to validate
    :param str | int sample_name: name or index of the sample to validate
    :param str | dict schema: schema dict to validate against or a path to one
    :param bool exclude_case: whether to exclude validated objects
        from the error. Useful when used ith large projects
    """
    sample = (
        project.samples[sample_name]
        if isinstance(sample_name, int)
        else project.get_sample(sample_name)
    )
    _validate_sample_object(
        sample=sample, schemas=read_schema(schema=schema), exclude_case=exclude_case
    )


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
        schema_cpy = preprocess_schema(dpcpy(schema_dict))
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


def validate_inputs(sample, schema, exclude_case=False):
    """
    Determine which of this Sample's required attributes/files are missing
    and calculate sizes of the inputs.

    The names of the attributes that are required and/or deemed as inputs
    are sourced from the schema, more specifically from required_input_attrs
    and input_attrs sections in samples section. Note, this function does
    perform actual Sample object validation with jsonschema.

    :param peppy.Sample sample: sample to investigate
    :param list[dict] | str schema: schema dict to validate against or a path to one
    :return dict: dictionary with validation data, i.e missing,
        required_inputs, all_inputs, input_file_size
    :param bool exclude_case: whether to exclude validated objects
        from the error. Useful when used ith large projects
    :raise ValidationError: if any required sample attribute is missing
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

    if isinstance(schema, str):
        schema = read_schema(schema)

    # validate attrs existence first
    _validate_sample_object(schemas=schema, sample=sample, exclude_case=exclude_case)

    all_inputs = set()
    required_inputs = set()
    schema = schema[-1]  # use only first schema, in case there are imports
    sample_schema_dict = schema["properties"]["_samples"]["items"]
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
        ) / (1024**3)
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
