import inspect
import sys
from logging import getLogger

from pkg_resources import iter_entry_points
from yaml import safe_dump

from .exceptions import *

_LOGGER = getLogger(__name__)


def pep_conversion_plugins():
    """
    Plugins registered by entry points in the current Python env

    :return dict[dict[function(peppy.Project)]]: dict which keys
        are names of all possible hooks and values are dicts mapping
        registered functions names to their values
    :raise EidoFilterError: if any of the filters has an invalid signature.
    """
    plugins = {}
    for ep in iter_entry_points("pep.filters"):
        plugin_fun = ep.load()
        if len(list(inspect.signature(plugin_fun).parameters)) != 2:
            raise EidoFilterError(
                f"Invalid filter plugin signature: {ep.name}. "
                f"Filter functions must take 2 arguments: peppy.Project and **kwargs"
            )
        plugins[ep.name] = plugin_fun
    return plugins


def convert_project(prj, target_format, plugin_kwargs=None):
    """
    Convert a `peppy.Project` object to a selected format

    :param peppy.Project prj: a Project object to convert
    :param dict plugin_kwargs: kwargs to pass to the plugin function
    :param str target_format: the format to convert the Project object to
    """
    run_filter(prj, target_format, plugin_kwargs or dict())
    sys.exit(0)


def run_filter(prj, filter_name, plugin_kwargs=None):
    """
    Run a selected filter on a peppy.Project object

    :param peppy.Project prj: a Project to run filter on
    :param str filter_name: name of the filter to run
    :param dict plugin_kwargs: kwargs to pass to the plugin function
    :raise EidoFilterError: if the requested filter is not defined
    """
    installed_plugins = pep_conversion_plugins()
    installed_plugin_names = list(installed_plugins.keys())
    if filter_name not in installed_plugin_names:
        raise EidoFilterError(
            f"Requested filter ({filter_name}) not found. "
            f"Available: {', '.join(installed_plugin_names)}"
        )
    _LOGGER.info(f"Running plugin {filter_name}")
    func = installed_plugins[filter_name]
    plugin_kwargs = plugin_kwargs or dict()
    func(prj, **plugin_kwargs)


def get_available_pep_filters():
    """
    Get a list of available target formats

    :return List[str]: a list of available formats
    """
    return list(pep_conversion_plugins().keys())


# built-in PEP filters defined below


def basic_pep_filter(p, **kwargs):
    """
    Basic PEP filter, that does not convert the Project object

    :param peppy.Project p: a Project to run filter on
    """
    print(p)


def yaml_samples_pep_filter(p, **kwargs):
    """
    YAML samples PEP filter, that returns only Sample object representations

    :param peppy.Project p: a Project to run filter on
    """
    import re

    for s in p.samples:
        sys.stdout.write("- ")
        out = re.sub("\n", "\n  ", safe_dump(s.to_dict(), default_flow_style=False))
        sys.stdout.write(out + "\n")


def yaml_pep_filter(p, **kwargs):
    """
    YAML PEP filter, that returns Project object representation

    :param peppy.Project p: a Project to run filter on
    """
    print(p.to_yaml())


def csv_pep_filter(p, **kwargs):
    """
    CSV PEP filter, that returns Sample object representations

    :param peppy.Project p: a Project to run filter on
    """
    sys.stdout.write(p.sample_table.to_csv())
    if p.subsample_table is not None:
        sys.stdout.write(p.subsample_table.to_csv())
