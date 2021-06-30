**The PEP filters are an experimental feature and may change in feature versions of `eido`**

# Eido filters

Eido provides a CLI to convert a PEP into different output formats. These include some built-in formats, like csv (which takes your spits out a processed csv file, with project/sample modified), yaml, and a few others. It also provides a plugin system so that you can write your own Python functions to provide custom output formats.

## View available filters

Run this command to see what filters are available:

```console
eido filters
```

You'll see some output like this. There are a few built-in filters available:


```console
Available filters:
 - basic
 - csv
 - yaml
 - yaml-samples
```

You can also [write a custom filters](writing-a-filter.md), which will write your PEP into whatever format you need.

## Convert a PEP into an alternative format with a filter

To convert a PEP into an output format, do this:

```console
eido convert config.yaml -f basic
running plugin pep
Project 'pepconvert' (/home/nsheff/code/pepconvert/config.yaml)
5 samples: WT_REP1, WT_REP2, RAP1_UNINDUCED_REP1, RAP1_UNINDUCED_REP2, RAP1_IAA_30M_REP1
Sections: pep_version, sample_table, subsample_table
...
```

This *basic* format just lists the config file, the number of samples and their names, and identifies the sections in the project config file. Another format is `-f yaml`,

```console
eido convert config.yaml -f yaml
```

This will output your samples in yaml format.

### Parametrizing PEP conversions

The filter functions are parameterizable, so depending on the desired filter function design and required arguments you might need to provide them like this:

```console
eido convert config.yaml -f yaml -a argument1=value1 argument2=value2
```

To learn more about the parameters filters require, you can issue a `eido filter -c <filter_name> command, which will display the plugin documentation. For example:

```console
eido filters -f yaml-samples

    YAML samples PEP filter, that returns only Sample object representations.

    This filter can save the YAML to file, if kwargs include `path`.

    :param peppy.Project p: a Project to run filter on
```

Based on what the filter author of `yaml-samples` filter specified, `path` argument can be passed to `eido convert`.
