
import argparse
from attmap import PathExAttMap

from . import  __version__

class _VersionInHelpParser(argparse.ArgumentParser):
    def format_help(self):
        """ Add version information to help text. """
        return "version: {}\n".format(__version__) + \
               super(_VersionInHelpParser, self).format_help()




def parse_args():
    banner = "%(prog)s - validate project metadata against a schema"
    additional_description = "\nhttps://github.com/pepkit/eido"

    parser = _VersionInHelpParser(
            description=banner,
            epilog=additional_description)

    parser.add_argument(
            "-V", "--version",
            action="version",
            version="%(prog)s {v}".format(v=__version__))

    parser.add_argument(
            "-p", "--pep", required=True,
            help="PEP configuration file (yaml format).")

    parser.add_argument(
            "-s", "--schema", required=True,
            help="PEP schema file (yaml format)")


    args = parser.parse_args()
    return args

 

def main():
    """ Primary workflow """

    args = parse_args()

    print("Compare PEP {} against schema {}.").format(args.pep, args.schema)



if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(1)
