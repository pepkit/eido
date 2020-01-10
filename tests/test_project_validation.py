import pytest
from eido import *


class TestProjectValidation:
    def test_validate_works(self, project_object, schema_file_path):
        validate_project(project=project_object, schema=schema_file_path)
