import subprocess
import pytest

class TestCLI:
    def test_cli_help(self):
        out = subprocess.check_call(['eido', '-h'])
        assert out == 0

    def test_cli_works(self, project_file_path, schema_file_path):
        out = subprocess.check_call(['eido', '-p', project_file_path, '-s', schema_file_path])
        assert out == 0

    def test_cli_exclusiveness(self, project_file_path, schema_file_path):
        with pytest.raises(subprocess.CalledProcessError):
            subprocess.check_call(['eido', '-p', project_file_path, '-s', schema_file_path, '-s', 'name', '-c'])