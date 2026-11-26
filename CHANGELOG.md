# CHANGELOG

## v0.165 - 11-26-2026
### Breaking changes
- AXL errors now raise `zeep.exceptions.Fault` instead of being returned as a value. Wrap calls in `try/except Fault` where you previously checked `isinstance(result, Fault)`. `run_sql_query` still never raises and keeps the error on `ucm.last_exception`.
- Single-object getters return the object itself instead of the SOAP envelope: `get_location`, `get_translation`, `get_route_pattern`, `get_media_resource_group_list`, `get_call_manager_group`, `get_sip_profile`, `get_sip_security_profile`, `list_route_plan_specific`.
- List getters return `[]` when nothing matches instead of raising `TypeError`.
- `add_called_party_xform` and `add_calling_party_xform` require `pattern`.
- `add_route_pattern` raises `ValueError` unless exactly one of `gateway` or `route_list` is given.

### Added
- feat: bundle AXL schema 14.0 and 15.0 (WSDL/XSD) so `cucm_version="14.0"` and `"15.0"` work against CUCM 14 and 15 clusters
- feat: translate friendly argument names (`partition`, `device_pool`, `css`, `location`, `device`...) to AXL element names for every method, while still accepting the AXL names; Python booleans are sent as AXL `true`/`false`
- feat: `update_user_em` merges with the user's existing device profiles and user groups instead of replacing them
- feat: `add_phone` supports SIP profiles, `common_phone_config`, and sends `enableActivationID`/`allowMraMode` only on schemas that have them
- feat: offline request-building tests (`tests/test_offline_requests.py`) validate generated requests against the bundled schemas without a CUCM

### Fixed
- Resolve the 27 High findings in `docs/audit/axl-schema-audit.md`: `update_call_manager_group` called the wrong operation; `add_sip_trunk`, `add_h323_gateway`, `add_hunt_pilot`, `add_line_group`, `add_hunt_list` omitted required elements; uuid-based resets, `add_location` on pre-10.0 schemas, empty `newName` updates, `phoneProfiles`, Extension Mobility services, and mis-cased transformation masks produced invalid requests
- README examples now match the method signatures; `docs/sql.md` documents the real SQL methods; Read the Docs installs from `docs/requirements.txt`

## v0.163 - 11-22-2022
### Fixed
- PR#60 - update readme for pattern vs directory number
- PR#35 - make AXL ports a variable
- PR#32 - Fix issue with uuid for `update user`
- PR#30 - tagfilter resolving and filtering
- PR#27 - improve handling of strict mode ssl

**!!! NOTE**
- This version also addresses some CI issues with the latest version and begins to build out a new mkdocs style documentation