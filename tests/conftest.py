import pytest
import os
from peppy import Project


@pytest.fixture
def data_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


@pytest.fixture
def schemas_path(data_path):
    return os.path.join(data_path, "schemas")


@pytest.fixture
def peps_path(data_path):
    return os.path.join(data_path, "peps")


@pytest.fixture
def project_file_path(peps_path):
    return os.path.join(peps_path, "test_cfg.yaml")


@pytest.fixture
def project_object(project_file_path):
    return Project(project_file_path)


@pytest.fixture
def schema_file_path(schemas_path):
    return os.path.join(schemas_path, "test_schema.yaml")


@pytest.fixture
def schema_samples_file_path(schemas_path):
    return os.path.join(schemas_path, "test_schema_samples.yaml")


@pytest.fixture
def schema_invalid_file_path(schemas_path):
    return os.path.join(schemas_path, "test_schema_invalid.yaml")

@pytest.fixture
def schema_sample_invalid_file_path(schemas_path):
    return os.path.join(schemas_path, "test_schema_sample_invalid.yaml")