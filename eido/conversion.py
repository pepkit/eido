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
    :raise EidoFilterError: if the requested filter is not defined
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
    Basic PEP filter, that does not convert the Project object.

    This filter can save the PEP representation to file, if kwargs include `path`.

    :param peppy.Project p: a Project to run filter on
    """
    path = kwargs.get("path")
    if path is not None:
        with open(path, "w") as text_file:
            text_file.write(p.__str__)
    else:
        print(p)


def yaml_samples_pep_filter(p, **kwargs):
    """
    YAML samples PEP filter, that returns only Sample object representations.

    This filter can save the YAML to file, if kwargs include `path`.

    :param peppy.Project p: a Project to run filter on
    """
    path = kwargs.get("path")
    if path is not None:
        from yaml import dump

        samples_yaml = []
        for s in p.samples:
            samples_yaml.append(s.to_dict())
        with open(path, "w") as outfile:
            dump(samples_yaml, outfile, default_flow_style=False)
    else:
        import re

        for s in p.samples:
            sys.stdout.write("- ")
            out = re.sub("\n", "\n  ", safe_dump(s.to_dict(), default_flow_style=False))
            sys.stdout.write(out + "\n")


def yaml_pep_filter(p, **kwargs):
    """
    YAML PEP filter, that returns Project object representation.

    This filter can save the YAML to file, if kwargs include `path`.

    :param peppy.Project p: a Project to run filter on
    """
    from yaml import dump

    path = kwargs.get("path")
    if path is not None:
        data = p.config.to_dict()
        with open(path, "w") as outfile:
            dump(data, outfile, default_flow_style=False)
    else:
        data = p.config.to_yaml()
        print(data)


def csv_pep_filter(p, **kwargs):
    """
    CSV PEP filter, that returns Sample object representations

    This filter can save the CSVs to files, if kwargs include
    `sample_table_path` and/or `subsample_table_path`.

    :param peppy.Project p: a Project to run filter on
    """
    sample_table_path = kwargs.get("sample_table_path")
    subsample_table_path = kwargs.get("subsample_table_path")
    sample_table_repr = p.sample_table.to_csv(path_or_buf=sample_table_path)
    if sample_table_repr is not None:
        sys.stdout.write(sample_table_repr)
    if p.subsample_table is not None:
        subsample_table_repr = p.subsample_table.to_csv(
            path_or_buf=subsample_table_path
        )
        if subsample_table_repr is not None:
            sys.stdout.write(subsample_table_repr)
