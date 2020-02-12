# eido

[![Build Status](https://travis-ci.org/pepkit/eido.svg?branch=master)](https://travis-ci.org/pepkit/eido)
[![Coverage Status](https://coveralls.io/repos/github/pepkit/eido/badge.svg?branch=master)](https://coveralls.io/github/pepkit/eido?branch=master)
[![PEP compatible](http://pepkit.github.io/img/PEP-compatible-green.svg)](http://pepkit.github.io)

Eido is a validation tool for [PEPs](http://pepkit.github.io) based on [`jsonschema`](https://github.com/Julian/jsonschema). The PEP standard defines a structure for organizing metadata using a simple yaml + tsv format. Projects that follow the PEP standard can be read by a variety of PEP-compatible tools, which may require specific sample or project attributes. These requirements can be specified by a tool author using a schema, and then eido is used to validate PEPs against these schemas.

---
*Eidos* is a Greek term meaning "form" "essence", "type" or "species". See Plato's theory of Forms and Aristotle's theory of universals. The schemas are analogous to a "form" of an object, and the role of the `eido` software is to confirm or refute a claim that an instance fits that particular  object type.
