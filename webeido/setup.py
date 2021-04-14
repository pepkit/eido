#! /usr/bin/env python

from setuptools import setup
import sys

PACKAGE = "webeido"

# Additional keyword arguments for setup().
extra = {}

# Ordinary dependencies
DEPENDENCIES = []
with open("requirements/requirements-all.txt", 'r') as reqs_file:
    for line in reqs_file:
        print(line)
        if not line.strip():
            continue
        DEPENDENCIES.append(line)

# 2to3
if sys.version_info >= (3, ):
    extra["use_2to3"] = True
extra["install_requires"] = DEPENDENCIES


with open("{}/_version.py".format(PACKAGE), 'r') as versionfile:
    version = versionfile.readline().split()[-1].strip("\"'\n")

with open('README.md') as f:
    long_description = f.read()

setup(
    name=PACKAGE,
    packages=[PACKAGE],
    version=version,
    description="Web-based PEP validator using eido",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering :: Bio-Informatics"
    ],
    keywords="bioinformatics, sequencing, ngs, metadata, reproducibility",
    url="https://eido.databio.org/",
    author=u"Nathan Sheffield",
    license="BSD2",
    entry_points={
        "console_scripts": [
            "{p} = {p}.__main__:main".format(p=PACKAGE),
        ],
    },
    include_package_data=True,
    **extra
)
