__author__ = "Johannes Köster"
__contributors__ = ["Per Unneberg"]
__copyright__ = "Copyright 2015, Johannes Köster"
__email__ = "koester@jimmy.harvard.edu"
__license__ = "MIT"

import os
import json
import re
import inspect
import textwrap
import platform
from itertools import chain
import collections
import multiprocessing
import string
import shlex
import sys
from urllib.parse import urljoin

from snakemake.io import regex, Namedlist, Wildcards, _load_configfile
from snakemake.logging import logger
from snakemake.exceptions import WorkflowError
import snakemake


def validate(data, schema, set_default=True):
    """Validate data with JSON schema at given path.

    Args:
        data (object): data to validate. Can be a config dict or a pandas data frame.
        schema (str): Path to JSON schema used for validation. The schema can also be
            in YAML format. If validating a pandas data frame, the schema has to
            describe a row record (i.e., a dict with column names as keys pointing
            to row values). See http://json-schema.org. The path is interpreted
            relative to the Snakefile when this function is called.
        set_default (bool): set default values defined in schema. See
            http://python-jsonschema.readthedocs.io/en/latest/faq/ for more
            information
    """
    try:
        import jsonschema
        from jsonschema import validators, RefResolver
    except ImportError:
        raise WorkflowError("The Python 3 package jsonschema must be installed "
                            "in order to use the validate directive.")

    if not os.path.isabs(schema):
        frame = inspect.currentframe().f_back
        # if workflow object is not available this has not been started from a workflow
        if "workflow" in frame.f_globals:
            workflow = frame.f_globals["workflow"]
            schema = os.path.join(workflow.current_basedir, schema)

    schemafile = schema
    schema = _load_configfile(schema, filetype="Schema")
    resolver = RefResolver(
        urljoin('file:', schemafile), schema,
        handlers={'file': lambda uri: _load_configfile(re.sub("^file://", "", uri))})

    # Taken from http://python-jsonschema.readthedocs.io/en/latest/faq/
    def extend_with_default(validator_class):
        validate_properties = validator_class.VALIDATORS["properties"]

        def set_defaults(validator, properties, instance, schema):
            for property, subschema in properties.items():
                if "default" in subschema:
                    instance.setdefault(property, subschema["default"])

            for error in validate_properties(
                    validator, properties, instance, schema,
            ):
                yield error

        return validators.extend(
            validator_class, {"properties": set_defaults},
        )

    Validator = validators.validator_for(schema)
    if Validator.META_SCHEMA['$schema'] != schema['$schema']:
        logger.warning("No validator found for JSON Schema version identifier '{}'".format(schema['$schema']))
        logger.warning("Defaulting to validator for JSON Schema version '{}'".format(Validator.META_SCHEMA['$schema']))
        logger.warning("Note that schema file may not be validated correctly.")
    DefaultValidator = extend_with_default(Validator)

    if not isinstance(data, dict):
        try:
            import pandas as pd
            recordlist = []
            if isinstance(data, pd.DataFrame):
                for i, record in enumerate(data.to_dict("records")):
                    record = {k: v for k, v in record.items() if not pd.isnull(v)}
                    try:
                        if set_default:
                            DefaultValidator(schema, resolver=resolver).validate(record)
                            recordlist.append(record)
                        else:
                            jsonschema.validate(record, schema, resolver=resolver)
                    except jsonschema.exceptions.ValidationError as e:
                        raise WorkflowError(
                            "Error validating row {} of data frame.".format(i),
                            e)
                if set_default:
                    newdata = pd.DataFrame(recordlist, data.index)
                    newcol = ~newdata.columns.isin(data.columns)
                    n = len(data.columns)
                    for col in newdata.loc[:, newcol].columns:
                        data.insert(n, col, newdata.loc[:, col])
                        n = n + 1
                return
        except ImportError:
            pass
        raise WorkflowError("Unsupported data type for validation.")
    else:
        try:
            if set_default:
                DefaultValidator(schema, resolver=resolver).validate(data)
            else:
                jsonschema.validate(data, schema, resolver=resolver)
        except jsonschema.exceptions.ValidationError as e:
            raise WorkflowError("Error validating config file.", e)






from jsonschema import validate
import yaml

with open("schema.json") as f:
    schema = yaml.load(f, Loader=yaml.SafeLoader)


