from logging import CRITICAL, DEBUG, ERROR, INFO, WARN

from ubiquerg import VersionInHelpParser

from . import __version__
from .const import *

LEVEL_BY_VERBOSITY = [
    ERROR,
    CRITICAL,
    WARN,
    INFO,
    DEBUG,
]


def build_argparser():
    banner = "%(prog)s - Interact with PEPs"
    additional_description = "\nhttp://eido.databio.org/"

    parser = VersionInHelpParser(
        prog=PKG_NAME,
        description=banner,
        epilog=additional_description,
        version=__version__,
    )

    subparsers = parser.add_subparsers(dest="command")
    parser.add_argument(
        "--verbosity",
        dest="verbosity",
        type=int,
        choices=range(len(LEVEL_BY_VERBOSITY)),
        help="Choose level of verbosity (default: %(default)s)",
    )
    parser.add_argument("--logging-level", dest="logging_level", help="logging level")
    parser.add_argument(
        "--dbg",
        dest="dbg",
        action="store_true",
        help="Turn on debug mode (default: %(default)s)",
    )
    sps = {}
    for cmd, desc in SUBPARSER_MSGS.items():
        sps[cmd] = subparsers.add_parser(cmd, description=desc, help=desc)
        sps[cmd].add_argument(
            "pep",
            metavar="PEP",
            help="Path to a PEP configuration " "file in yaml format.",
        )

    sps[VALIDATE_CMD].add_argument(
        "-s",
        "--schema",
        required=True,
        help="Path to a PEP schema file in yaml format.",
        metavar="S",
    )

    sps[VALIDATE_CMD].add_argument(
        "-e",
        "--exclude-case",
        default=False,
        action="store_true",
        help="Whether to exclude the validation case from an error. "
        "Only the human readable message explaining the error will "
        "be raised. Useful when validating large PEPs.",
    )

    sps[INSPECT_CMD].add_argument(
        "-n",
        "--sample-name",
        required=False,
        nargs="+",
        help="Name of the samples to inspect.",
        metavar="SN",
    )

    sps[INSPECT_CMD].add_argument(
        "-l",
        "--attr-limit",
        required=False,
        type=int,
        default=10,
        help="Number of sample attributes to display.",
    )

    group = sps[VALIDATE_CMD].add_mutually_exclusive_group()

    group.add_argument(
        "-n",
        "--sample-name",
        required=False,
        help="Name or index of the sample to validate. "
        "Only this sample will be validated.",
        metavar="S",
    )

    group.add_argument(
        "-c",
        "--just-config",
        required=False,
        action="store_true",
        default=False,
        help="Whether samples should be excluded from the " "validation.",
    )
    return parser
