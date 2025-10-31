# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1](https://github.com/openshift-hyperfleet/rh-hooks-ai/compare/v1.0.0...v1.0.1) (2025-10-31)


### Bug Fixes

* Fix version check not checking installed version of hook. ([ee5cb16](https://github.com/openshift-hyperfleet/rh-hooks-ai/commit/ee5cb16769d53e3b2a0a04969401794dd911f40b))

## 1.0.0 (2025-10-31)


### Features

* Add optional update check & use release-please ([8450b39](https://github.com/openshift-hyperfleet/rh-hooks-ai/commit/8450b39cb8f118cb9a3702cb722d1b8fb86c8f9b))


### Bug Fixes

* **ci:** configure release-please with PAT ([cbd2e0a](https://github.com/openshift-hyperfleet/rh-hooks-ai/commit/cbd2e0a2ece37388de48c85cad89827e5cd45c0b))
* Use `script` type ([465d528](https://github.com/openshift-hyperfleet/rh-hooks-ai/commit/465d528e6181e2148f393856dcb7bebc3bf4608c))

## [Unreleased]

### Added
- Initial release of rh-ai-hooks
- Three core hooks: check-rh-precommit, validate-agents-md, ai-attribution-reminder
- Version checking hook (check-version) - optional
- Bootstrap script for one-command setup
- Templates for AGENTS.md and git commit messages
- Comprehensive documentation
- Automated releases with release-please
- Conventional commits enforcement
