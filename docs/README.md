<img src="img/eido.svg" alt="eido" width="200"/>
[![Build Status](https://travis-ci.org/pepkit/eido.svg?branch=master)](https://travis-ci.org/pepkit/eido)
[![Coverage Status](https://coveralls.io/repos/github/pepkit/eido/badge.svg?branch=master)](https://coveralls.io/github/pepkit/eido?branch=master)
[![PEP compatible](http://pepkit.github.io/img/PEP-compatible-green.svg)](http://pepkit.github.io)

## Introduction

Eido is a validation tool for [PEPs](http://pepkit.github.io) based on [JSON Schema](https://github.com/Julian/jsonschema). The PEP specification defines a formal structure for organizing project and sample metadata, and eido provides a way to validate if data complies with that specification. Eido extends the JSON Schema vocabulary with PEP-specific features, like required input files.

## Why do we need eido?

A PEP consists of metadata describing a set of items called *samples*. The metadata is divided into two-components: 1) sample-specific attributes; and 2) project attributes, which apply to all samples. A PEP follows a [formal specification](http://pep.databio.org) for formatting and organizing this data. Projects that follow the PEP specification can be read by a variety of PEP-compatible tools, which may require specific sample or project attributes. Eido is used to validate these specific required attributes.

[JSON Schema](https://json-schema.org/) is a vocabulary that allows you to annotate and validate JSON documents. It's great for validating JSON documents, but alone it cannot validate a PEP, which has powerful portability features that go beyond a simple JSON document, so we require additional capability to validate it. Eido extends JSON Schema to add this capability, along with other features for validating sample metadata listed below.

## PEP-specific validation features

An eido schema is written using the JSON Schema vocabulary, plus a few additional features:

1. **required input files**. Eido adds `requied_files`, which allows a schema author to specify which attributes must point to files that exist.
2. **optional input files**. `files` specifies which attributes point to files that may or may not exist.
3. **project and sample validation**. Eido validates project attributes separately from sample attributes.
4. **schema imports**. Eido adds an `imports` section for schemas that should be validated prior to this schema
5. **automatic multi-value support**. Eido validates successfully for singular or plural sample attributes for strings, booleans, and numbers. This accommodates the PEP subsample_table feature.

## How to use eido

- [Use eido to validate data from the command line](cli.md)
- [Use eido to validate data from Python](demo.md)
- [Write your own schema](writing-a-schema.md)

---

## What does 'eido' mean?

*Eidos* is a Greek term meaning *form*, *essence*, or *type* (see Plato's [Theory of Forms](https://en.wikipedia.org/wiki/Theory_of_forms)). Schemas are analogous to *forms*, and eido tests claims that an instance is of a particular form.


