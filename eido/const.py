"""
Constant variables for eido package.
"""

LOGGING_LEVEL: str = "INFO"
PKG_NAME: str = "eido"
INSPECT_CMD: str = "inspect"
VALIDATE_CMD: str = "validate"
CONVERT_CMD: str = "convert"
FILTERS_CMD: str = "filters"
SUBPARSER_MSGS: dict[str, str] = {
    VALIDATE_CMD: "Validate a PEP or its components",
    INSPECT_CMD: "Inspect a PEP",
    CONVERT_CMD: "Convert PEP format using filters",
}
PROP_KEY: str = "properties"

# eido is archived; it is now shipped as the peppy.eido module within peppy
DEPRECATION_MESSAGE: str = (
    "eido is deprecated and this repository is now a public archive. "
    "It is now part of the peppy package as the 'peppy.eido' module "
    "(https://github.com/pepkit/peppy). Please migrate to 'import peppy.eido'."
)

SAMPLES_KEY: str = "samples"

TANGIBLE_KEY: str = "tangible"
SIZING_KEY: str = "sizing"

# sample schema input validation key names, these values are required by looper
# to refer to the dict values
MISSING_KEY: str = "missing"
REQUIRED_INPUTS_KEY: str = "required_inputs"
ALL_INPUTS_KEY: str = "all_inputs"
INPUT_FILE_SIZE_KEY: str = "input_file_size"

# groups of constants
GENERAL: list[str] = [
    "LOGGING_LEVEL",
    "PKG_NAME",
    "DEPRECATION_MESSAGE",
    "INSPECT_CMD",
    "VALIDATE_CMD",
    "CONVERT_CMD",
    "FILTERS_CMD",
    "SUBPARSER_MSGS",
]

SCHEMA_SECTIONS: list[str] = ["PROP_KEY", "TANGIBLE_KEY", "SIZING_KEY"]

SCHEMA_VALIDAION_KEYS: list[str] = [
    "MISSING_KEY",
    "REQUIRED_INPUTS_KEY",
    "ALL_INPUTS_KEY",
    "INPUT_FILE_SIZE_KEY",
]

__all__ = GENERAL + SCHEMA_SECTIONS + SCHEMA_VALIDAION_KEYS
