#! /usr/bin/env python

import os
from setuptools import setup
import sys

# Additional keyword arguments for setup().
extra = {}

# Ordinary dependencies
DEPENDENCIES = []
with open("requirements/requirements-all.txt", "r") as reqs_file:
    for line in reqs_file:
        if not line.strip():
            continue
        #DEPENDENCIES.append(line.split("=")[0].rstrip("<>"))
        DEPENDENCIES.append(line)

# 2to3
if sys.version_info >= (3, ):
    extra["use_2to3"] = True
extra["install_requires"] = DEPENDENCIES


# Additional files to include with package
def get_static(name, condition=None):
    static = [os.path.join(name, f) for f in os.listdir(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), name))]
    if condition is None:
        return static
    else:
        return [i for i in filter(lambda x: eval(condition), static)]

# scripts to be added to the $PATH
# scripts = get_static("scripts", condition="'.' in x")
# scripts removed (TO remove this)
scripts = None

with open("eido/_version.py", 'r') as versionfile:
    version = versionfile.readline().split()[-1].strip("\"'\n")

# Handle the pypi README formatting.
try:
    import pypandoc
    long_description = pypandoc.convert_file('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setup(
    name="eido",
    packages=["eido"],
    version=version,
    description="A project metadata validator",
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Topic :: Scientific/Engineering :: Bio-Informatics"
    ],
    keywords="project, metadata, bioinformatics, sequencing, ngs, workflow",
    url='https://github.com/pepkit/eido/',
    author=u"Michal Stolarczyk, Nathan Sheffield",
    license="BSD2",
    entry_points={
        "console_scripts": [
            'eido = eido.__main__:main'
        ],
    },
    scripts=scripts,
    include_package_data=True,
    test_suite="tests",
    tests_require=(["mock", "pytest"]),
    setup_requires=(["pytest-runner"] if {"test", "pytest", "ptr"} & set(sys.argv) else []),
    **extra
)
