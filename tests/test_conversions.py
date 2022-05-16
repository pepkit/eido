from eido.conversion import *
import peppy


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

    def test_basic_filter(self, project_object):
        conv_result = run_filter(
            project_object,
            "basic",
            verbose=False,
            plugin_kwargs={"paths": {"project": "out/basic_prj.txt"}},
        )
        # the basic filter just converts to a string
        assert conv_result["project"] == str(project_object)
