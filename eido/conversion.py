import inspect
import sys
import os
from logging import getLogger

from pkg_resources import iter_entry_points

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
    return run_filter(prj, target_format, plugin_kwargs or dict())


def run_filter(prj, filter_name, verbose=True, plugin_kwargs=None):
    """
    Run a selected filter on a peppy.Project object

    :param peppy.Project prj: a Project to run filter on
    :param str filter_name: name of the filter to run
    :param dict plugin_kwargs: kwargs to pass to the plugin function
    :raise EidoFilterError: if the requested filter is not defined
    """
    # convert to empty dictionary if no plugin_kwargs are passed
    plugin_kwargs = plugin_kwargs or dict()

    # get necessary objects
    installed_plugins = pep_conversion_plugins()
    installed_plugin_names = list(installed_plugins.keys())
    paths = plugin_kwargs.get('paths')
    env = plugin_kwargs.get('env')

    # set environment
    if env is not None:
        for var in env:
            os.environ[var] = env[var]

    # check for valid filter
    if filter_name not in installed_plugin_names:
        raise EidoFilterError(
            f"Requested filter ({filter_name}) not found. "
            f"Available: {', '.join(installed_plugin_names)}"
        )
    _LOGGER.info(f"Running plugin {filter_name}")
    func = installed_plugins[filter_name]

    # run filter
    conv_results = func(prj, **plugin_kwargs)

    # if paths supplied, write to disk
    if paths is not None:
        # make out dirs if they don't already exist
        for path in paths:
            if not os.path.exists(path):
                os.makedirs(path)

        # extract potential results
        cfg_result = conv_results.get('cfg')
        samples_result = conv_results.get('samples')

        # write config conversion result
        if cfg_result is not None:
            with open(paths['cfg'], 'w') as f:
                f.write(cfg_result)
        
        # write samples conversion result
        if samples_result is not None:
            with open(paths['samples'], 'w') as f:
                f.write(samples_result)

    if verbose:
        # loop through and print to
        # standard out
        for res in conv_results:
            sys.stdout.write(conv_results[res])
    else:
        # if no path is provided and the verbose flag is not set,
        # then most likely eido is being uesd programmatically and
        # nothing needs to be done.
        pass

    return conv_results


def get_available_pep_filters():
    """
    Get a list of available target formats

    :return List[str]: a list of available formats
    """
    return list(pep_conversion_plugins().keys())
