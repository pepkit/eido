
from ubiquerg import VersionInHelpParser
import logging
import logmuse

from . import __version__
from .const import *

_LOGGER = logging.getLogger(__name__)


def build_argparser():
    banner = "%(prog)s - validate project metadata against a schema"
    additional_description = "\nhttps://github.com/pepkit/eido"

    parser = VersionInHelpParser(
            prog=pkg_name,
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

 
def main():
    """ Primary workflow """
    parser = logmuse.add_logging_options(build_argparser())
    args, remaining_args = parser.parse_known_args()
    logger_kwargs = {"level": args.verbosity, "devmode": args.logdev}
    logmuse.init_logger(name=pkg_name, **logger_kwargs)
    global _LOGGER
    _LOGGER = logmuse.logger_via_cli(args)
    _LOGGER.info("Comparing PEP ('{}') against schema: {}.".format(args.pep, args.schema))
