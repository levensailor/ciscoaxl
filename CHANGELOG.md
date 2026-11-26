# CHANGELOG

## Unreleased - 11-26-2026
### Added
- feat: bundle AXL schema 14.0 and 15.0 (WSDL/XSD) so `cucm_version="14.0"` and `"15.0"` work against CUCM 14 and 15 clusters

## v0.163 - 11-22-2022
### Fixed
- PR#60 - update readme for pattern vs directory number
- PR#35 - make AXL ports a variable
- PR#32 - Fix issue with uuid for `update user`
- PR#30 - tagfilter resolving and filtering
- PR#27 - improve handling of strict mode ssl

**!!! NOTE**
- This version also addresses some CI issues with the latest version and begins to build out a new mkdocs style documentation