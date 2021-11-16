<img src="img/eido.svg" alt="eido" width="200"/>
![Run pytests](https://github.com/pepkit/eido/workflows/Run%20pytests/badge.svg)
[![codecov](https://codecov.io/gh/pepkit/eido/branch/master/graph/badge.svg)](https://codecov.io/gh/pepkit/eido)
[![PEP compatible](http://pepkit.github.io/img/PEP-compatible-green.svg)](http://pepkit.github.io)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Introduction

Eido is used to 1) validate or 2) convert format of sample metadata. Sample metadata is stored according to the standard [PEP specification](https://pep.databio.org). For validation, eido is based on [JSON Schema](https://json-schema.org) and extends it with new features, like required input files. You can [write your own schema](writing-a-schema.md) for your pipeline and use eido to validate sample metadata. For conversion, [eido filters](filters.md) convert sample metadata input into any output format, including [custom filters](writing-a-filter.md).

## Why do we need eido?

Data-intensive bioinformatics projects often include metadata describing a set of samples. When it comes to handling such sample metadata, there are two common challenges that eido solves:

1. **Validation**. Tool authors may be interested in specifying and describing what the tool requires in terms of sample attributes. The tool author provides a schema, and then eido validates the sample metadata. Eido uses [JSON Schema](https://json-schema.org/), which allows you to annotate and validate JSON documents. JSON schema alone is great for validating JSON documents, but bioinformatics sample metadata is more complicated, so eido provides additional capability and features tailored to bioinformatics projects listed below.

2. **Format conversion**. Pipelines or other use cases may require the sample metadata in a particular format. Eido provides built-in and custom *filters*, which allow you to take a metadata in standard PEP format and easily convert it to any desired output format. This helps you keep a single sample metadata source that can be used for multiple downstream analyses.

## Eido validation features

An eido schema is written using the JSON Schema vocabulary, plus a few additional features:

1. **required input files**. Eido adds `required_files`, which allows a schema author to specify which attributes must point to files that exist.
2. **optional input files**. `files` specifies which attributes point to files that may or may not exist.
3. **project and sample validation**. Eido validates project attributes separately from sample attributes.
4. **schema imports**. Eido adds an `imports` section for schemas that should be validated prior to this schema
5. **automatic multi-value support**. Eido validates successfully for singular or plural sample attributes for strings, booleans, and numbers. This accommodates the PEP subsample_table feature.

## How to use eido

- [Use eido to validate data from the command line](cli.md)
- [Use eido to validate data from Python](demo.md)
- [Write your own schema](writing-a-schema.md)

---

## Why is called 'eido'?

*Eidos* is a Greek term meaning *form*, *essence*, or *type* (see Plato's [Theory of Forms](https://en.wikipedia.org/wiki/Theory_of_forms)). Schemas are analogous to *forms*, and eido tests claims that an instance is of a particular form. Eido also helps *change* forms using filters.
