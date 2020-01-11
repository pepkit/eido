import pytest
import subprocess
from eido import *


class TestProjectValidation:
    def test_validate_works(self, project_object, schema_file_path):
        validate_project(project=project_object, schema=schema_file_path)


class TestCLI:
    def test_cli_help(self):
        out = subprocess.check_call(['eido', '-h'])
        assert out == 0

    def test_cli_works(self, project_file_path, schema_file_path):
        out = subprocess.check_call(['eido', '-p', project_file_path, '-s', schema_file_path])
        assert out == 0
