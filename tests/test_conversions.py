from eido.conversion import *


class TestConversionInfrastructure:
    def test_plugins_are_read(self):
        avail_filters = get_available_pep_filters()
        assert isinstance(avail_filters, list)

    def test_plugins_contents(self):
        avail_plugins = pep_conversion_plugins()
        avail_filters = get_available_pep_filters()
        assert all(
            [plugin_name in avail_filters for plugin_name in avail_plugins.keys()]
        )

    def test_plugins_are_callable(self):
        avail_plugins = pep_conversion_plugins()
        assert all(
            [callable(plugin_fun) for plugin_name, plugin_fun in avail_plugins.items()]
        )

    def test_basic_filter(self, save_result_mock, project_object):
        conv_result = run_filter(
            project_object,
            "basic",
            verbose=False,
            plugin_kwargs={"paths": {"project": "out/basic_prj.txt"}},
        )

        assert save_result_mock.called
        assert conv_result["project"] == str(project_object)

    def test_csv_filter(
        self, save_result_mock, taxprofiler_project, taxprofiler_csv_multiline_output
    ):

        conv_result = run_filter(
            taxprofiler_project,
            "csv",
            verbose=False,
            plugin_kwargs={"paths": {"samples": "out/basic_prj.txt"}},
        )

        assert save_result_mock.called
        assert conv_result["samples"] == taxprofiler_csv_multiline_output
