# AGENTS.md

## Learned User Preferences

- Public methods keep the friendly argument names (`partition`, `device_pool`, `css`, and the rest of the alias map). `partition` is intentional because it is easier than `routePartitionName`. The client converts those names to the AXL element on the request and still accepts the AXL name when the caller passes it. Ask before changing a friendly public name that a schema review flags.
- AXL wrappers live in one module per entity (`ciscoaxl/media.py`, `ciscoaxl/dialplan.py`, and the other entity modules). Rollout priority (`p0` through `p3`) is a backlog label and stays out of the package layout.

## Learned Workspace Facts

- Bundled schemas are `ciscoaxl/schema/<version>/{AXLAPI.wsdl,AXLSoap.xsd,AXLEnums.xsd}` for 8.5, 9.1, 10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 14.0, and 15.0. `axl(..., cucm_version=...)` loads `schema/{cucm_version}/AXLAPI.wsdl`. 15.0 is the newest AXL API version in the repo; CUCM 15 service updates still use it. `schema/current` is the 12.0 namespace and was left as that copy when 14.0 and 15.0 were added.
- 14.0 and 15.0 came from the MIT-licensed sieteunoseis/cisco-axl repo. Cisco publishes those files only in the AXL Toolkit on a CUCM server. 12.5, 14.0, and 15.0 share 1,068 operations; 14.0 adds headset and phone-onboarding fields and enums.
- `axl` inherits the entity mixins Templates, Users, Presence, Security, Lifecycle, DialPlan, Gateways, Media, System, Ils, Ime, CcdSaf, Network, and Niche. Callers use `ucm.<method>()`.
- Friendly-name translation lives in `ciscoaxl/aliases.py`. `@apply_aliases` wraps methods on `axl` and its mixin bases. Keys the schema already accepts are left unchanged. List operations return `[]` when AXL omits the return body. AXL errors raise `zeep.exceptions.Fault`.
- Each AXL method docstring ends with a `Schema:` line taken from the 15.0 XSD, including choice identities such as `uuid` or `pattern` plus an optional partition.
- `wsdl.py`, `helpers.py`, `config.py`, `exceptions.py`, and `axl_generator.py` were removed because nothing in the SDK imported them.
- Offline tests in `tests/test_offline_requests.py` and `tests/test_<entity>.py` build SOAP against the bundled schemas with no live CUCM. New wrappers follow that pattern.
