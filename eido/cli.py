import logging
import sys

from logmuse import init_logger
from peppy import Project

from .argparser import LEVEL_BY_VERBOSITY, build_argparser
from .const import *
from .conversion import convert_project, get_available_pep_filters
from .inspection import inspect_project
from .validation import validate_config, validate_project, validate_sample


def _parse_filter_args_str(input):
    """
    Parse user input specification.

    :param Iterable[Iterable[str]] input: user command line input,
        formatted as follows: [[arg=txt, arg1=txt]]
    :return dict: mapping of keys, which are input names and values
    """
    lst = []
    for i in input or []:
        lst.extend(i)
    return (
        {x.split("=")[0]: x.split("=")[1] for x in lst if "=" in x}
        if lst is not None
        else lst
    )


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

    if args.command == FILTERS_CMD:
        filters = get_available_pep_filters()
        if len(filters) < 1:
            _LOGGER.info("No available filters")
            sys.exit(0)
        _LOGGER.info("Available filters:")
        for filter_name in filters:
            _LOGGER.info(f" - {filter_name}")
        sys.exit(0)

    _LOGGER.debug(f"Creating a Project object from: {args.pep}")
    p = Project(args.pep)
    if args.command == VALIDATE_CMD:
        if args.sample_name:
            try:
                args.sample_name = int(args.sample_name)
            except ValueError:
                pass
            _LOGGER.debug(
                f"Comparing Sample ('{args.pep}') in Project ('{args.pep}') "
                f"against a schema: {args.schema}"
            )
            validate_sample(p, args.sample_name, args.schema, args.exclude_case)
        elif args.just_config:
            _LOGGER.debug(
                f"Comparing Project ('{args.pep}') against a schema: {args.schema}"
            )
            validate_config(p, args.schema, args.exclude_case)
        else:
            _LOGGER.debug(
                f"Comparing Project ('{args.pep}') against a schema: {args.schema}"
            )
            validate_project(p, args.schema, args.exclude_case)
        _LOGGER.info("Validation successful")
    if args.command == INSPECT_CMD:
        inspect_project(p, args.sample_name, args.attr_limit)
        sys.exit(0)

    if args.command == CONVERT_CMD:
        p = Project(args.pep)
        plugin_kwargs = _parse_filter_args_str(args.args)
        convert_project(p, args.format, plugin_kwargs)
        _LOGGER.info("Conversion successful")
        sys.exit(0)
