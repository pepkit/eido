# Changelog

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) and [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format. 

## [0.1.2] - 2020-08-05
### Added
- license in the package source distribution

## [0.1.1] - 2020-05-27
### Changed
- documentation updates
- CLI behavior when no subcommand provided; [#20](https://github.com/pepkit/eido/issues/20)

## [0.1.0] - 2020-05-26
### Added
- automatic support for subsamples for sample the following property types:
    - `string`
    - `boolean`
    - `numeric`
- `eido inspect` CLI command
- schema importing functionality (via top level `imports` key)
- exported functions:
    - `validate_inputs`
    - `inspect_project`
    - `read_schema`

### Changed
- previous CLI `eido` functionality moved to `eido validate`
 
## [0.0.6] - 2020-02-07
### Changed
- CLI can accommodate URLs.

## [0.0.5] - 2020-02-04
### Added 
- [documentation website](http://eido.databio.org/en/latest/)
- include version in the CLI help

## [0.0.4] - 2020-01-31
### Added
- `validate_sample` function for sample level validation
- sample validation CLI support (via `-n`/`--sample-name` argument)
- `validate_config` to facilitate samples exclusion in validation
- config validation CLI support (via `-c`/`--just-config` argument)  

## [0.0.3] - 2020-01-30
### Added
- Option to exclude the validation case from error messages in both Python API and CLI app with `exclude_case` and `-e`/`--exclude-case`, respectively.
- include requirements in the source distribution

## [0.0.2] - 2020-01-12

### Added
- Initial project release
