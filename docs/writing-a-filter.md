# How to write a custom eido filter

One of `eido`'s tasks is to provide a CLI to convert a PEP into alternative formats. These include some built-in formats, `like csv` (which spits out a processed `csv` file, with project/sample modified), `yaml`, and a few others. It also provides a plugin system so that you can write your own Python functions to provide custom output formats.

## Custom filters

To write a custom filter, start by writing a Python package. You will need to write a function that takes a `peppy.Project` object as input, and prints out the custom file format.

### 1. Write functions to call

The package contain one or more functions. The filter function **must take a peppy.Project object as sole parameter**. Example:

```python
import peppy
  
def my_custom_filter(p):
    import re
    for s in p.samples:
        sys.stdout.write("- ")
        out = re.sub('\n', '\n  ', yaml.safe_dump(s.to_dict(), default_flow_style=False))
        sys.stdout.write(out + "\n")
```

Then, we need to link that function in to the `eido` filter plugin system.

### 2. Add entry_points to setup.py

The [setup.py](setup.py) file uses `entry_points` to specify a mapping of eido hooks to functions to call.

```python
    entry_points={
        "pep.filters": ["basic=pepconvert:my_basic_plugin",
                        "yaml=pepconvert:complete_yaml",
                        "csv=pepconvert:csv",
                        "yaml-samples=pepconvert:yaml_samples"]
        }
```

The format is: `'pep.filters': 'FILTER_NAME=PLUGIN_PACKAGE_NAME:FUNCTION_NAME'`.

- "FILTER_NAME" can be any unique identifier for your plugin
- "PLUGIN_PACKAGE_NAME" must be the name of python package the holds your plugin.
- "FUNCTION_NAME" must match the name of the function in your package
