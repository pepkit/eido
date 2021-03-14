"""
Constant variables for eido package
"""

LOGGING_LEVEL = "INFO"
PKG_NAME = "eido"
INSPECT_CMD = "inspect"
VALIDATE_CMD = "validate"
SUBPARSER_MSGS = {
    VALIDATE_CMD: "Validate the PEP or its components.",
    INSPECT_CMD: "Inspect a PEP.",
}
PROP_KEY = "properties"
REQUIRED_FILES_KEY = "required_files"
FILES_KEY = "files"

# sample schema input validation key names, these values are required by looper
# to refer to the dict values
MISSING_KEY = "missing"
REQUIRED_INPUTS_KEY = "required_inputs"
ALL_INPUTS_KEY = "all_inputs"
INPUT_FILE_SIZE_KEY = "input_file_size"

# groups of constants
GENERAL = ["LOGGING_LEVEL", "PKG_NAME", "INSPECT_CMD", "VALIDATE_CMD", "SUBPARSER_MSGS"]
SCHEMA_SECTIONS = ["PROP_KEY", "REQUIRED_FILES_KEY", "FILES_KEY"]
SCHEMA_VALIDAION_KEYS = [
    "MISSING_KEY",
    "REQUIRED_INPUTS_KEY",
    "ALL_INPUTS_KEY",
    "INPUT_FILE_SIZE_KEY",
]

__all__ = GENERAL + SCHEMA_SECTIONS + SCHEMA_VALIDAION_KEYS
