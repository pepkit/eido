from argparse import ArgumentParser
from eido import build_argparser


class TestUtils:
    def test_argparser_building(self):
        assert isinstance(build_argparser(), ArgumentParser)