# CHANGELOG

## Unreleased - 11-27-2026
### Changed
- refactor: organize wrapper mixins by entity instead of rollout priority — `ciscoaxl/p0_*.py`…`p3_*.py` are now `templates`, `users`, `presence`, `security`, `lifecycle`, `dialplan`, `gateways`, `media`, `system`, `ils`, `ime`, `ccd_saf`, `network`, and `niche` (classes `TemplatesMixin`, `MediaMixin`, …), and their tests are `tests/test_<entity>.py`. `ucm.<method>()` calls are unchanged; only direct imports of the old `ciscoaxl.pX_*` modules need updating.

### Docs
- docs: coverage table lists Remote Destinations, UC Services, and Voicemail Profiles

## v0.171 - 11-26-2026
### Fixed
- fix: correct SOAP unwrap keys on seven AXL getters — OS version (`os`), Smart License (`LicenseDetails`; status stays on `return`), device profile options (`deviceProfile`), translation pattern options (`transPattern`), SIP profile options (`sipProfile`), phone type display instance (`displayInstance`, requires `productName` and `protocol`), and transport settings (`TransportSettings`)

## v0.170 - 11-26-2026
### Added
- feat: wrap P3 AXL objects for niche, legacy, IME/CCD/SAF, and network features — IME, CCD/SAF, LBM/SNMP/DHCP/WLAN, Catalyst 6000/VG224/H.323/gatekeeper, geo-location/billing/cloud onboarding/dial-plan tags, HTTP/infrastructure/MLPP/resource-priority/SDP/VoH/transport settings
- Offline tests for every P3 batch (`tests/test_p3_b*.py`)

## v0.169 - 11-26-2026
### Added
- feat: wrap P2 AXL objects — media/dial-plan extras (announcements, CMC/FAC, ELIN, H.323 trunks), ILS/remote cluster and Smart Licensing actions, IM&P presence/MRA/VPN/CAPF, and system helpers (change notification, options getters, inactive SQL, authenticate user, self-provisioning)
- Offline tests for every P2 batch (`tests/test_p2_b*.py`)

## v0.168 - 11-26-2026
### Added
- feat: wrap P1 AXL objects — lifecycle apply/reset/restart for existing resources, dial-plan helpers (AAR, dial rules, directed park, local route group, route filter, SIP dial/route patterns), MGCP/SCCP gateways and endpoints, media/mobility (Meet-Me, MOH, recording, device mobility, presence groups), and system/LDAP/credential/voicemail-port wrappers
- Offline tests for every P1 batch (`tests/test_p1_b*.py`)

## v0.167 - 11-26-2026
### Added
- feat: wrap P0 AXL objects for day-to-day admin work — device templates (`CommonDeviceConfig`, `CommonPhoneConfig`, `PhoneButtonTemplate`, `SoftKeyTemplate`, `UniversalDeviceTemplate`, `UniversalLineTemplate`), users/mobility (`AppUser`, `UserGroup`, `UserPhoneAssociation`, `UserProfileProvision`, `RemoteDestination`, `RemoteDestinationProfile`), presence/voicemail/dial plan (`ServiceProfile`, `UcService`, `VoiceMailPilot`, `VoiceMailProfile`, `TimePeriod`, `TimeSchedule`, `CallPark`), and security/system/LDAP/phone lifecycle (`PhoneSecurityProfile`, `SipProfile` CRUD, `SipTrunkSecurityProfile`, `DateTimeGroup`, `LdapDirectory`, `LdapSyncStatus`, `CCMVersion`, `RegistrationDynamic`, phone apply/reset/restart/lock/wipe)
- Offline tests for every P0 batch (`tests/test_p0_b*.py`)

## v0.166 - 11-26-2026
### Breaking changes
- `run_sql_query` raises `zeep.exceptions.Fault` on AXL errors (it no longer swallows faults onto `ucm.last_exception`).
- `add_phone` parameters `ownerUserName`, `securityProfileName`, `enableActivationID`, and `allowMraMode` are snake_case (`owner_user_name`, `security_profile_name`, `enable_activation_id`, `allow_mra_mode`); the AXL camelCase names still work via aliases.

### Fixed
- Empty-list contract: hunt pilot/list, line group, and call pickup group list getters return `[]` instead of `None`; route-plan, call-manager-group, and called-party-xform list helpers guard a missing `return`.
- Docs build: Material theme, `mkdocstrings[python]`, replaced copied stub pages, removed orphaned Sphinx tree.
- Deleted unused `axl_generator.py`.

### Added
- Offline tests for empty-list results, `run_sql_query` Fault propagation, and `_schema_fields` version gating.
- CONTRIBUTING.md with feature-branch and PR workflow.

## v0.165 - 11-26-2026
### Breaking changes
- AXL errors now raise `zeep.exceptions.Fault` instead of being returned as a value. Wrap calls in `try/except Fault` where you previously checked `isinstance(result, Fault)`.
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