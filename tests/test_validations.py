import urllib

import pytest
from jsonschema.exceptions import ValidationError
from peppy import Project
from peppy.utils import load_yaml

from eido import *
from eido.exceptions import EidoValidationError


def _check_remote_file_accessible(url):
    try:
        code = urllib.request.urlopen(url).getcode()
    except:
        pytest.skip(f"Remote file not found: {url}")
    else:
        if code != 200:
            pytest.skip(f"Return code: {code}. Remote file not found: {url}")


class TestProjectValidation:
    def test_validate_works(self, project_object, schema_file_path):
        validate_project(project=project_object, schema=schema_file_path)

    def test_validate_detects_invalid(self, project_object, schema_invalid_file_path):
        with pytest.raises(EidoValidationError):
            validate_project(project=project_object, schema=schema_invalid_file_path)

    def test_validate_detects_invalid_imports(
        self, project_object, schema_imports_file_path
    ):
        with pytest.raises(EidoValidationError):
            validate_project(project=project_object, schema=schema_imports_file_path)

    def test_validate_converts_samples_to_private_attr(
        self, project_object, schema_samples_file_path
    ):
        """
        In peppy.Project the list of peppy.Sample objects is
        accessible via _samples attr.
        To make the schema creation more accessible for eido users
        samples->_samples key conversion has been implemented
        """
        validate_project(project=project_object, schema=schema_samples_file_path)

    def test_validate_works_with_dict_schema(self, project_object, schema_file_path):
        validate_project(project=project_object, schema=load_yaml(schema_file_path))

    @pytest.mark.parametrize("schema_arg", [1, None, [1, 2, 3]])
    def test_validate_raises_error_for_incorrect_schema_type(
        self, project_object, schema_arg
    ):
        with pytest.raises(TypeError):
            validate_project(project=project_object, schema=schema_arg)


class TestSampleValidation:
    @pytest.mark.parametrize("sample_name", [0, 1, "GSM1558746"])
    def test_validate_works(
        self, project_object, sample_name, schema_samples_file_path
    ):
        validate_sample(
            project=project_object,
            sample_name=sample_name,
            schema=schema_samples_file_path,
        )

    @pytest.mark.parametrize("sample_name", [22, "bogus_sample_name"])
    def test_validate_raises_error_for_incorrect_sample_name(
        self, project_object, sample_name, schema_samples_file_path
    ):
        with pytest.raises((ValueError, IndexError)):
            validate_sample(
                project=project_object,
                sample_name=sample_name,
                schema=schema_samples_file_path,
            )

    @pytest.mark.parametrize("sample_name", [0, 1, "GSM1558746"])
    def test_validate_detects_invalid(
        self, project_object, sample_name, schema_sample_invalid_file_path
    ):
        with pytest.raises(EidoValidationError):
            validate_sample(
                project=project_object,
                sample_name=sample_name,
                schema=schema_sample_invalid_file_path,
            )


class TestConfigValidation:
    def test_validate_succeeds_on_invalid_sample(
        self, project_object, schema_sample_invalid_file_path
    ):
        validate_config(project=project_object, schema=schema_sample_invalid_file_path)


class TestRemoteValidation:
    @pytest.mark.parametrize("schema_url", ["http://schema.databio.org/pep/2.0.0.yaml"])
    def test_validate_works_with_remote_schemas(self, project_object, schema_url):
        _check_remote_file_accessible(schema_url)
        validate_project(project=project_object, schema=schema_url)
        validate_config(project=project_object, schema=schema_url)
        validate_sample(project=project_object, schema=schema_url, sample_name=0)


class TestImportsValidation:
    def test_validate(self, project_object, schema_file_path):
        validate_project(project=project_object, schema=schema_file_path)


class TestProjectWithoutConfigValidation:
    @pytest.mark.parametrize(
        "remote_pep_cfg",
        [
            "https://raw.githubusercontent.com/pepkit/example_peps/master/example_basic/sample_table.csv"
        ],
    )
    def test_validate_works(self, schema_file_path, remote_pep_cfg):
        _check_remote_file_accessible(remote_pep_cfg)
        validate_project(
            project=Project(
                remote_pep_cfg
            ),  # create Project object from a remote sample table
            schema=schema_file_path,
        )

    @pytest.mark.parametrize(
        "remote_pep_cfg",
        [
            "https://raw.githubusercontent.com/pepkit/example_peps/master/example_basic/sample_table.csv"
        ],
    )
    def test_validate_detects_invalid(self, schema_invalid_file_path, remote_pep_cfg):
        _check_remote_file_accessible(remote_pep_cfg)
        with pytest.raises(EidoValidationError):
            validate_project(
                project=Project(remote_pep_cfg), schema=schema_invalid_file_path
            )
