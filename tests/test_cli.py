import subprocess
import pytest
from eido.const import *


class TestCLI:
    def test_cli_help(self):
        out = subprocess.check_call(['eido', '-h'])
        assert out == 0

    def test_validate_works(self, project_file_path, schema_file_path):
        out = subprocess.check_call(['eido', VALIDATE_CMD, project_file_path, '-s', schema_file_path])
        assert out == 0

    def test_validate_exclusiveness(self, project_file_path, schema_file_path):
        with pytest.raises(subprocess.CalledProcessError):
            subprocess.check_call(['eido', VALIDATE_CMD, project_file_path, '-s', schema_file_path, '-s', 'name', '-c'])

    def test_inspect_works(self, project_file_path):
        out = subprocess.check_call(['eido', INSPECT_CMD, project_file_path])
        assert out == 0
        out = subprocess.check_call(['eido', INSPECT_CMD, project_file_path, '-n', "0"])
        assert out == 0
