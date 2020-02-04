jupyter:True
# `eido` command line usage

To use the command line application one just needs two required paths as arguments to the `eido` command: 
- a path to a project configuration file (`-p`/`--pep` option)
- a path to a YAML formatted schema (`-s`/`--schema` option)

Optionally, to validate just the config parto of the PEP or a specific sample, `n`/`--sample-name` or `-c`/`--just-config` arguments should be used, respectively. Please refer to the help for more details:

```
~ eido -h
```
```
usage: eido [-h] [-V] -p PEP -s SCHEMA [-e] [-n SAMPLE_NAME | -c] [--silent]
            [--verbosity V] [--logdev]

eido - validate project metadata against a schema

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  -p PEP, --pep PEP     PEP configuration file in yaml format.
  -s SCHEMA, --schema SCHEMA
                        PEP schema file in yaml format.
  -e, --exclude-case    Whether to exclude the validation case from an error.
                        Only the human readable message explaining the error
                        will be raised. Useful when validating large PEPs.
  -n SAMPLE_NAME, --sample-name SAMPLE_NAME
                        Name or index of the sample to validate. Only this
                        sample will be validated.
  -c, --just-config     Whether samples should be excluded from the
                        validation.
  --silent              Silence logging. Overrides verbosity.
  --verbosity V         Set logging level (1-5 or logging module level name)
  --logdev              Expand content of logging message format.

https://github.com/pepkit/eido
```

Successful validation of the project is confirmed with an appropriate message:
```
~ eido -p config.yaml -s tests/data/schemas/test_schema.yaml
Reading sample table: '/Users/mstolarczyk/Uczelnia/UVA/code/eido/tests/data/peps/test_sample_table.csv'
Validation successful
```

Alternatively, a `jsonschema.exceptions.ValidationError` is raised with a discrepancy description.
