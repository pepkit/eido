#!/bin/bash
lucidoc eido -P rst --blacklist basic_pep_filter,yaml_pep_filter,csv_pep_filter,yaml_samples_pep_filter > docs/api_docs.md
