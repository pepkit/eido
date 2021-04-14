import sys
from logging import getLogger

from pkg_resources import iter_entry_points
from yaml import safe_dump

_LOGGER = getLogger(__name__)

# TODO: document
# TODO: add to jupyter notebooks


def plugins():
    """
    Plugins registered by entry points in the current Python env

    :return dict[dict[function(peppy.Project)]]: dict which keys
        are names of all possible hooks and values are dicts mapping
        registered functions names to their values
    """
    return {ep.name: ep.load() for ep in iter_entry_points("pep.filters")}


def convert_project(prj, target_format):
    """
    Convert a peppy.Project to a selected format

    :param peppy.Project: a Project object to convert
    :param str target_format: the format to convert the Project object to
    """
    run_filter(prj, target_format)
    sys.exit(0)


def my_basic_plugin(p):
    print(p)


def yaml_samples(p):
    import re

    for s in p.samples:
        sys.stdout.write("- ")
        out = re.sub("\n", "\n  ", safe_dump(s.to_dict(), default_flow_style=False))
        sys.stdout.write(out + "\n")


def complete_yaml(p):
    print(p.to_yaml())


def csv(p):
    sys.stdout.write(p._sample_df.to_csv())
    sys.stdout.write(p._subsample_df[0].to_csv())


def run_filter(prj, filter_name):
    myplugins = plugins()

    for name, func in myplugins.items():
        if name == filter_name:
            _LOGGER.info(f"running plugin {name}")
            func(prj)


def get_available_formats():
    """
    Get a list of available target formats

    :return List[str]: a list of available formats
    """
    return list(plugins().keys())
