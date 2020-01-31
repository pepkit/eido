import pytest
from eido import *
from eido.eido import _load_yaml
from jsonschema.exceptions import ValidationError


class TestProjectValidation:
    def test_validate_works(self, project_object, schema_file_path):
        validate_project(project=project_object, schema=schema_file_path)

    def test_validate_detects_invalid(self, project_object, schema_invalid_file_path):
        with pytest.raises(ValidationError):
            validate_project(project=project_object, schema=schema_invalid_file_path)

    def test_validate_converts_samples_to_private_attr(self, project_object, schema_samples_file_path):
        """
        In peppy.Project the list of peppy.Sample objects is accessible via _samples attr.
        To make the schema creation more accessible for eido users samples->_samples key conversion has been implemented
        """
        validate_project(project=project_object, schema=schema_samples_file_path)

    def test_validate_works_with_dict_schema(self, project_object, schema_file_path):
        validate_project(project=project_object, schema=_load_yaml(schema_file_path))

    @pytest.mark.parametrize("schema_arg", [1, None, [1, 2, 3]])
    def test_validate_raises_error_for_incorrect_schema_type(self, project_object, schema_arg):
        with pytest.raises(TypeError):
            validate_project(project=project_object, schema=schema_arg)


class TestSampleValidation:
    @pytest.mark.parametrize("sample_name", [0, 1, "GSM1558746"])
    def test_validate_works(self, project_object, sample_name, schema_samples_file_path):
        validate_sample(project=project_object, sample_name=sample_name, schema=schema_samples_file_path)

    @pytest.mark.parametrize("sample_name", [22, "bogus_sample_name"])
    def test_validate_raises_error_for_incorrect_sample_name(self, project_object, sample_name, schema_samples_file_path):
        with pytest.raises((ValueError, IndexError)):
            validate_sample(project=project_object, sample_name=sample_name, schema=schema_samples_file_path)

    @pytest.mark.parametrize("sample_name", [0, 1, "GSM1558746"])
    def test_validate_detects_invalid(self, project_object, sample_name, schema_sample_invalid_file_path):
        with pytest.raises(ValidationError):
            validate_sample(project=project_object, sample_name=sample_name, schema=schema_sample_invalid_file_path)


class TestConfigValidation:
    def test_validate_succeeds_on_invalid_sample(self, project_object, schema_sample_invalid_file_path):
        validate_config(project=project_object, schema=schema_sample_invalid_file_path)