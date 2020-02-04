jupyter:True
# Python API usage

There are 3 `eido` functions in the public package interface:

- `validate_project` to validate the entire PEP
- `validate_sample` to validate only a selected sample
- `validate_config` to validate only the config part of the PEP

## Entire PEP validation


```python
from eido import *
from peppy import Project
```

Within Python the `validate_project` function can be used to perform the entire PEP validation. It requires `peppy.Project` object and either a path to the YAML schema file or a read schema (`dict`) as inputs.


```python
p = Project("../tests/data/peps/test_cfg.yaml")
validate_project(project=p, schema="../tests/data/schemas/test_schema.yaml")

from eido.eido import _load_yaml
s = _load_yaml("../tests/data/schemas/test_schema.yaml")
validate_project(project=p, schema=s)
```

If a validation is successful, no message is printed. An unsuccessful one is signalized with a corresponding `jsonschema.exceptions.ValidationError`


```python
validate_project(project=p, schema="../tests/data/schemas/test_schema_invalid.yaml")
```


    ---------------------------------------------------------------------------

    ValidationError                           Traceback (most recent call last)

    <ipython-input-9-29fa9395c52f> in <module>
    ----> 1 validate_project(project=p, schema="../tests/data/schemas/test_schema_invalid.yaml")
    

    /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/eido/eido.py in validate_project(project, schema, exclude_case)
        130     schema_dict = _read_schema(schema=schema)
        131     project_dict = project.to_dict()
    --> 132     _validate_object(project_dict, _preprocess_schema(schema_dict), exclude_case)
        133     _LOGGER.debug("Project validation successful")
        134 


    /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/eido/eido.py in _validate_object(object, schema, exclude_case)
        115     except jsonschema.exceptions.ValidationError as e:
        116         if not exclude_case:
    --> 117             raise e
        118         raise jsonschema.exceptions.ValidationError(e.message)
        119 


    /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/eido/eido.py in _validate_object(object, schema, exclude_case)
        112     """
        113     try:
    --> 114         jsonschema.validate(object, schema)
        115     except jsonschema.exceptions.ValidationError as e:
        116         if not exclude_case:


    ~/Library/Python/3.6/lib/python/site-packages/jsonschema/validators.py in validate(instance, schema, cls, *args, **kwargs)
        897     error = exceptions.best_match(validator.iter_errors(instance))
        898     if error is not None:
    --> 899         raise error
        900 
        901 


    ValidationError: 'invalid' is a required property
    
    Failed validating 'required' in schema:
        {'description': 'test PEP schema',
         'properties': {'_samples': {'items': {'properties': {'genome': {'type': 'string'},
                                                              'protocol': {'type': 'string'},
                                                              'sample_name': {'type': 'string'}},
                                               'type': 'object'},
                                     'type': 'array'},
                        'dcc': {'properties': {'compute_packages': {'type': 'object'}},
                                'type': 'object'},
                        'invalid': {'type': 'string'}},
         'required': ['dcc', '_samples', 'invalid']}
    
    On instance:
        {'_main_index_cols': 'sample_name',
         '_sample_table':   sample_name protocol genome
        0  GSM1558746      GRO   hg38
        1  GSM1480327      PRO   hg38,
         '_samples': [{'derived_cols_done': [],
                       'genome': 'hg38',
                       'merged': False,
                       'merged_cols': PathExAttMap: {},
                       'name': 'GSM1558746',
                       'paths': Paths object.,
                       'protocol': 'GRO',
                       'required_paths': None,
                       'results_subdir': '/Users/mstolarczyk/Uczelnia/UVA/code/eido/tests/data/peps/test/results_pipeline',
                       'sample_name': 'GSM1558746',
                       'sheet_attributes': ['sample_name',
                                            'protocol',
                                            'genome'],
                       'yaml_file': None},
                      {'derived_cols_done': [],
                       'genome': 'hg38',
                       'merged': False,
                       'merged_cols': PathExAttMap: {},
                       'name': 'GSM1480327',
                       'paths': Paths object.,
                       'protocol': 'PRO',
                       'required_paths': None,
                       'results_subdir': '/Users/mstolarczyk/Uczelnia/UVA/code/eido/tests/data/peps/test/results_pipeline',
                       'sample_name': 'GSM1480327',
                       'sheet_attributes': ['sample_name',
                                            'protocol',
                                            'genome'],
                       'yaml_file': None}],
         '_sections': {'name', 'metadata', 'implied_attributes'},
         '_subproject': None,
         '_subs_index_cols': ('sample_name', 'subsample_name'),
         '_subsample_table': None,
         'config_file': '/Users/mstolarczyk/Uczelnia/UVA/code/eido/tests/data/peps/test_cfg.yaml',
         'constant_attributes': {},
         'data_sources': None,
         'dcc': {'_file_path': '/Users/mstolarczyk/Uczelnia/UVA/code/pepenv/uva_rivanna.yaml',
                 '_ro': True,
                 '_wait_time': 10,
                 'compute': {'partition': 'standard',
                             'submission_command': 'sbatch',
                             'submission_template': '/Users/mstolarczyk/Uczelnia/UVA/code/pepenv/templates/slurm_template.sub'},
                 'compute_packages': {'default': {'partition': 'standard',
                                                  'submission_command': 'sbatch',
                                                  'submission_template': 'templates/slurm_template.sub'},
                                      'largemem': {'partition': 'largemem',
                                                   'submission_command': 'sbatch',
                                                   'submission_template': 'templates/slurm_template.sub'},
                                      'local': {'submission_command': 'sh',
                                                'submission_template': 'templates/localhost_template.sub'},
                                      'parallel': {'partition': 'parallel',
                                                   'submission_command': 'sbatch',
                                                   'submission_template': 'templates/slurm_template.sub'},
                                      'sigterm': {'partition': 'standard',
                                                  'submission_command': 'sbatch',
                                                  'submission_template': 'templates/slurm_sig_template.sub'},
                                      'singularity_local': {'singularity_args': '-B '
                                                                                '/ext:/ext',
                                                            'submission_command': 'sh',
                                                            'submission_template': 'templates/localhost_singularity_template.sub'},
                                      'singularity_slurm': {'singularity_args': '-B '
                                                                                '/sfs/lustre:/sfs/lustre,/nm/t1:/nm/t1',
                                                            'submission_command': 'sbatch',
                                                            'submission_template': 'templates/slurm_singularity_template.sub'}},
                 'config_file': '/Users/mstolarczyk/Uczelnia/UVA/code/pepenv/uva_rivanna.yaml'},
         'derived_attributes': ['data_source'],
         'file_checks': False,
         'implied_attributes': {'organism': {'Homo sapiens': {'genome': 'hg38'}}},
         'metadata': {'output_dir': '/Users/mstolarczyk/Uczelnia/UVA/code/eido/tests/data/peps/test',
                      'pipeline_interfaces': [],
                      'sample_table': '/Users/mstolarczyk/Uczelnia/UVA/code/eido/tests/data/peps/test_sample_table.csv'},
         'name': 'test',
         'permissive': True}


## Config validation

Similarily, the config part of the PEP can be validated; the function inputs remain the same


```python
validate_config(project=p, schema="../tests/data/schemas/test_schema.yaml")
```

## Sample validation

To validate a specific `peppy.Sample` object within a PEP, one needs to also specify the `sample_name` argument which can be the `peppy.Sample.name` attribute (`str`) or the ID of the sample (`int`)


```python
validate_sample(project=p, schema="../tests/data/schemas/test_schema.yaml", sample_name=0)
```

## Output details

As depicted above the error raised by the `jsonschema` package is very detailed. That's because the entire validated PEP is printed out for the user reference. Since it can get overwhelming in case of the multi sample PEPs each of the `eido` functions presented above privide a way to limit the output to just the general information indicating the unmet schema requirements


```python
validate_project(project=p, schema="../tests/data/schemas/test_schema_invalid.yaml", exclude_case=True)
```


    ---------------------------------------------------------------------------

    ValidationError                           Traceback (most recent call last)

    <ipython-input-12-af7d16ab2ae8> in <module>
    ----> 1 validate_project(project=p, schema="../tests/data/schemas/test_schema_invalid.yaml", exclude_case=True)
    

    /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/eido/eido.py in validate_project(project, schema, exclude_case)
        130     schema_dict = _read_schema(schema=schema)
        131     project_dict = project.to_dict()
    --> 132     _validate_object(project_dict, _preprocess_schema(schema_dict), exclude_case)
        133     _LOGGER.debug("Project validation successful")
        134 


    /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/eido/eido.py in _validate_object(object, schema, exclude_case)
        116         if not exclude_case:
        117             raise e
    --> 118         raise jsonschema.exceptions.ValidationError(e.message)
        119 
        120 


    ValidationError: 'invalid' is a required property



```python

```
