import logging
import sys

from logmuse import init_logger
from peppy import Project

from .argparser import LEVEL_BY_VERBOSITY, build_argparser
from .const import *
from .eido import inspect_project, validate_config, validate_project, validate_sample


def main():
    """ Primary workflow """
    parser = build_argparser()
    args, remaining_args = parser.parse_known_args()

    if args.command is None:
        parser.print_help(sys.stderr)
        sys.exit(1)

    # Set the logging level.
    if args.dbg:
        # Debug mode takes precedence and will listen for all messages.
        level = args.logging_level or logging.DEBUG
    elif args.verbosity is not None:
        # Verbosity-framed specification trumps logging_level.
        level = LEVEL_BY_VERBOSITY[args.verbosity]
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
            _LOGGER.debug(
                "Comparing Sample ('{}') in the Project ('{}') "
                "against a schema: {}.".format(args.sample_name, args.pep, args.schema)
            )
            validate_sample(p, args.sample_name, args.schema, args.exclude_case)
        elif args.just_config:
            _LOGGER.debug(
                "Comparing config ('{}') against a schema: {}.".format(
                    args.pep, args.schema
                )
            )
            validate_config(p, args.schema, args.exclude_case)
        else:
            _LOGGER.debug(
                "Comparing Project ('{}') against a schema: {}.".format(
                    args.pep, args.schema
                )
            )
            validate_project(p, args.schema, args.exclude_case)
        _LOGGER.info("Validation successful")
    if args.command == INSPECT_CMD:
        inspect_project(p, args.sample_name, args.attr_limit)
        sys.exit(0)
