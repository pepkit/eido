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
