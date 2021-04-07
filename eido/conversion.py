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


def convert_project(prj, format):
    run_filter(prj, format)
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


def list_formats():
    myplugins = plugins()
    if len(myplugins) > 0:
        _LOGGER.info("Available filters:")
        for name, func in myplugins.items():
            _LOGGER.info(f" - {name}")
    else:
        _LOGGER.info("No available filters")
