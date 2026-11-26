# AXL SDK Audit: Code and Docs vs. AXL 15.0 Schema

**Date:** 2026-11-26
**Scope:** `ciscoaxl/axl.py` (157 public methods, 174 AXL calls), `README.md`, `docs/`, build config
**Ground truth:** `ciscoaxl/schema/15.0/AXLSoap.xsd` (spot-checked against 12.5, 10.0, 9.1, 8.5)

Fix these before adding new endpoints. Most new endpoints would copy the same patterns.

## How this was produced

| Step | What it did |
|---|---|
| Static schema diff | Parsed every method with Python's `ast` module and compared the arguments, dictionary keys and `tagfilter` keys sent to each `self.client.<op>()` call against the zeep-parsed request type. Ran against 12.5 and 15.0 (identical results). |
| Expert committee | Five reviewers worked in parallel: four each took a line range of `axl.py`, and one took the README and docs site. Every finding had to cite an xsd type and line number. |
| Offline zeep verification | Disputed High findings were reproduced with `client.create_message()` using the SDK's own zeep `Settings`. Nothing was sent to CUCM. |

Two committee claims were corrected during verification:
- `add_location`'s `betweenLocations` list serializes correctly, so that claim was dropped.
- `add_phone`'s `vendorConfig` is silently dropped rather than crashing, so it was downgraded to Medium.

## Summary

| Severity | Count | Meaning |
|---|---|---|
| High | 27 | The call fails, sends invalid data, or is destructive as written or as documented |
| Medium | 45 | Wrong or misleading names, or wrong required/optional guidance, that users will hit |
| Low | 40+ | Documentation-only problems (copy-paste text, stale params, empty `:return:`) |

### Root causes (fixing these clears most of the list)

1. **Two vocabularies.** The `add_*` methods take snake_case Python arguments. The `get_*`/`update_*`/`delete_*` methods pass `**args` straight to zeep, so only AXL camelCase element names work. Docstrings and the README mix the two, so users following them get `TypeError: unexpected keyword argument`.
2. **Required fields are guesswork.** Docstrings call fields "required" when the schema has a `uuid` alternative, and leave out fields the schema requires (`blockEnable`, `distributionAlgorithm`, `loginDuration`, `class`, and others). zeep does **not** fill schema defaults; a missing required element raises `ValidationError` before the request is sent.
3. **Name/uuid choices are handled inconsistently.** Some methods accept name only, `do_ldap_sync` accepts uuid only, `do_device_reset` invents a `uuid` element, and pattern+partition lookups reject the `<None>` partition.
4. **Empty strings instead of omission.** Defaults of `""` produce empty elements (`<newName/>`, `<lines/>`, `<pattern/>`) that the schema rejects as non-nillable or as unmet required choices.
5. **No error or return contract.** Most methods return the `zeep.Fault` object instead of raising it. List getters raise `TypeError` on empty results. Getters variously return the full envelope, `["return"]`, or the unwrapped object. Some methods return plain strings on bad input.
6. **Version claims aren't implemented.** Branches in `add_location` and `add_phone` don't match the bundled schemas, so the README's 8.5–15.0 support claim is untrue for those methods.

---

## High severity

> **Status (v0.165):** all High items are resolved. `tests/test_offline_requests.py` covers them by building each request against the bundled schemas.

Items marked **(zeep-verified)** were reproduced offline with `create_message()`.

| # | Method (axl.py line) | Problem | Schema evidence (15.0 xsd) | Fix |
|---|---|---|---|---|
| H1 | `update_call_manager_group` (3060) | Calls `listCallManagerGroup` instead of `updateCallManagerGroup`, so it never updates anything. | `UpdateCallManagerGroupReq` L5406 | Call `updateCallManagerGroup(**args)` |
| H2 | `add_sip_trunk` (2992) | `addSipTrunk(**args)` raises `TypeError` for every documented argument because the request has one wrapper element, `sipTrunk`. **(zeep-verified)** | `AddSipTrunkReq` L20699 | `addSipTrunk({**args})` |
| H3 | `add_h323_gateway` (957) | Same wrapper bug (`h323Gateway`). The docstring lists flat snake_case arguments that don't exist. **(zeep-verified)** | `AddH323GatewayReq` L17152 | Wrap the arguments and document the `XH323Gateway` required fields |
| H4 | `do_device_reset` (244) | The UUID path sends a `uuid` element that doesn't exist; `deviceName` takes a name or UUID. Both-or-neither silently returns `None`. **(zeep-verified)** | `DoDeviceResetReq` L50419 | `deviceName=uuid`; raise `ValueError` |
| H5 | `add_location` (292) | Version branches are wrong. "10.0" sends `kbits`/`videoKbits`, which the 10.0 schema lacks. "8.5" sends `within*` fields, which the 8.5 schema lacks. "8.6", "9.0" and "9.5" have no bundled schema. | 8.5 `XLocation` L2218; 10.0 `XLocation` ~L2876 | Use `kbits` only for 8.5 and `within*` for 9.1 and later |
| H6 | `update_region` (419) | Always sends `<newName></newName>` (non-nillable `String50`), so every non-rename call sends invalid data. **(zeep-verified)** | `UpdateRegionReq` L2245 | Default to `None` and omit it when unset |
| H7 | `update_srst` (547) | Same empty `newName`. A rename is the only thing this method can do. | `UpdateSrstReq` L9186 | Omit `newName` when unset, or use `**args` |
| H8 | `add_hunt_pilot` (3120) | Docs say "minimal: pattern + routePartitionName". The schema also requires `blockEnable`, `useCallingPartyPhoneMask` and `huntListName`. `routePartitionName` is optional. **(zeep-verified)** | `XHuntPilot` L12191 | Fix the docstring, or set defaults |
| H9 | `add_line_group` (3287) | Docs say only `name` is required. `distributionAlgorithm`, `rnaReversionTimeOut` and the three `huntAlgorithm*` fields are also required. **(zeep-verified)** | `XLineGroup` L4961 | Python defaults equal to the schema defaults |
| H10 | `add_hunt_list` (3205) / `update_hunt_list` (3220) | Docs say `callManagerGroup`; the element is `callManagerGroupName`. | `XHuntList` L4654 | Rename |
| H11 | `add_user` (2332) | `phoneProfiles` is a bare list. A non-empty list fails (`Missing element profileName`) and the default `[]` sends an empty `<phoneProfiles/>`. **(zeep-verified)** | `XUser/phoneProfiles` L7526 | `{"profileName": [...]}`, omitted when empty |
| H12 | `update_user_em` (2374) | Overwrites **all** of the user's group and role memberships with the hard-coded "Standard CCM End Users", and replaces their device profiles. | `UpdateUserReq/associatedGroups` L7783 | Merge with existing values; make the group a parameter |
| H13 | `add_phone` (1977) | `enableActivationID` and `allowMraMode` arguments are ignored; Python `True` is always sent, and it serializes as `True`, which the case-sensitive `axlapi:boolean` pattern rejects. These elements don't exist before 12.5, so every `add_phone` fails on 8.5–12.0 and `current`. **(zeep-verified render)** | `XPhone` L16413/L16419; boolean pattern L49972 | Pass the arguments through, lowercase `"true"`/`"false"`, and send only on 12.5 and later |
| H14 | `add_phone` (1977) | When `em_service_url` is set, a list gets appended inside `service` (nested list). With `em_url_button_enable` this raises an uncaught `AttributeError` or `IndexError`. | `XPhone/services/service` L16185 | Append the dict itself |
| H15 | `add_route_pattern` (1407) | The `patternUrgency` argument is never added to the request. | `XRoutePattern` L12453 | Add it to `req` |
| H16 | `add_called_party_xform` (2755) / `add_calling_party_xform` (2858) | `pattern` defaults to `""`, but it is required and non-nillable. Docstrings list arguments the signature doesn't accept (`routePartitionName`, `dialPlanName`, …). | `XCalledPartyTransformationPattern` L21075; `XCallingPartyTransformationPattern` L11887 | Make `pattern` a required positional argument; align the docs |
| H17 | `do_device_login` (219) | Required `loginDuration` is undocumented. The README example also uses the invalid key `device`. | `DoDeviceLoginReq` L50364 | Document all four required fields |
| H18 | `do_device_logout` (232) | Docs list `device`/`userId`; the only element is `deviceName`. **(zeep-verified)** | `DoDeviceLogoutReq` L50400 | `deviceName` |
| H19 | `update_mtp` (898) | Docs list `mtpType` (not updatable) and `device_pool`. **(zeep-verified)** | `UpdateMtpReq` L13945 | `devicePoolName`; drop `mtpType` |
| H20 | `update_location` (367) | Docs say `withImmersiveKbits`; the element is `withinImmersiveKbits`. **(zeep-verified)** | `UpdateLocationReq` L3208 | Rename |
| H21 | All passthrough `update_*` docstrings (phone, line, CTI RP, device profile, route list/group/pattern, conf bridge, transcoder, device pool, media resource list) | Document snake_case `add_*` names (`device_pool`, `css`, `partition`, `alerting_name`, `cm_group_name`, `distribution_algorithm`…) and non-updatable fields (`product`, `class`, `protocol`). Every one raises `TypeError`. | `Update*Req` types | Rewrite with AXL element names |
| H22 | Get/delete docstrings for DN, hunt pilot, route pattern, transformations, hunt list | Document `name`/`partition`. The actual keys are `pattern` + `routePartitionName`, or `uuid`. Hunt lists have no partition. | `GetLineReq` L14640, `GetHuntPilotReq` L12369, `RemoveRoutePatternReq` L12646 | Rename and document the choice |
| H23 | List getters without an empty guard: `get_locations`, `get_regions`, `get_srsts`, `get_device_pools`, `get_conference_bridges`, `get_transcoders`, `get_mtps`, `get_directory_numbers`, `get_cti_route_points`, `get_device_profiles`, `get_translations`, `list_route_plan`, `get_called_party_xforms`, `get_calling_party_xforms`, `get_call_manager_groups`, `list_process_nodes` | When there are zero results `return` is `None`, so `["return"]["x"]` raises an uncaught `TypeError`. | e.g. `ListLocationRes` L3274 (`minOccurs=0`) | `(res["return"] or {}).get(...) or []` |
| H24 | README examples (lines 113–611) | Most examples fail: `user_id=`, `device_pool=`, `calling_search_space=`, `region=`, `location=`, `route_group=`, `route_list=`, `cti_route_point=`, `routePartitionName=` (where the argument is `partition`), `device=`, and a positional `delete_device_profile('x')`. Line 269 has a `SyntaxError` (missing comma). | Signatures in `axl.py` | Rewrite against the current signatures |
| H25 | README `get_translation` / `get_location` examples | These access `.description`/`.name`, but the method returns the SOAP envelope. | `axl.py` L288, L2488 | Unwrap `["return"][obj]` in code |
| H26 | `docs/sql.md` | Documents `sql_execute`, which doesn't exist. | `axl.py` L128–165 | Document `sql_query`, `sql_update`, `run_sql_query` |
| H27 | `.readthedocs.yaml:20` | Installs from `requirements.txt`, which doesn't exist, so the docs build fails. | — | Add `docs/requirements.txt` |

---

## Medium severity

### Naming mismatches (docstring or argument vs. schema element)

| Method (line) | Documented / used | Schema element |
|---|---|---|
| `do_change_dnd_status` (207) | `status` | `dndStatus` (required); `userID` or `uuid` |
| `update_device_pool` (640) | `mediaResourceGroupListName`, `media_resource_group_list` | `mediaResourceListName` |
| `update_conference_bridge` (740) | `device_pool`, `location`, `security_profile` | `devicePoolName`, `locationName`, `securityProfileName` |
| `update_transcoder` (821) | `product`, `device_pool` | not updatable; `devicePoolName` |
| `update_route_group` (1085) | `distribution_algorithm` | `distributionAlgorithm` |
| `update_route_list` (1190) | `cm_group_name`, `route_list_enabled`, `run_on_all_nodes` | `callManagerGroupName`, `routeListEnabled`, `runOnEveryNode` |
| `update_route_pattern` (1468) / `delete_route_pattern` (1455) | `partition`, `gateway`, `route_list` | `routePartitionName`, `destination{gatewayName\|routeListName}` |
| `get_partition` / `delete_partition` (1220/1251) | `partition` | `name` / `uuid` |
| `delete_calling_search_space` (1333) | `calling_search_space` | `name` / `uuid` |
| `get_media_resource_group` (1499) | `media_resource_group` | `name` / `uuid` |
| `update_media_resource_group_list` (1608) | `description`, `multicast` | not in `UpdateMediaResourceListReq` |
| `delete_cti_route_point` / `delete_phone` / `delete_device_profile` | `cti_route_point` / `phone` / `profile` | `name` / `uuid` |
| `get_phone` (1966) | "device profile", `phone` | `name` / `uuid` |
| `get_user` (2321) | `user_id` | `userid` / `uuid` |
| `add_user` (2332) | `user_id`, `first_name`, `last_name` | arguments are `userid`, `firstName`, `lastName` |
| `add_cti_route_point` (1836) | argument `protocol_slide` | typo for `protocolSide` |
| `update_calling_party_xform` (2909) | `calledParty*` fields (copy-paste) | `callingPartyPrefixDigits`, `callingPartyNumberingPlan`, `callingPartyNumberType` |
| `update_called_party_xform` (2806) | `calledPartyTransformationmask` | `calledPartyTransformationMask` |
| `add_call_pickup_group` / `update_call_pickup_group` | `usage` | read-only; exists only in list/get responses |
| `get_hunt_list` (3193) | `partition` | hunt lists have only `name` / `uuid` |

### Required vs. optional errors

| Method (line) | Problem | Schema evidence |
|---|---|---|
| `add_device_pool` (594) | Never sends required (nillable) `aarNeighborhoodName`. Sends an empty non-nillable `localRouteGroup.value`. Hard-codes "Standard Local Route Group". | `XDevicePool` L2796, L2848 |
| `add_transcoder` (794) | Never sends required (nillable) `loadInformation` | `XTranscoder` L3403 |
| `add_phone` (1977) | Required `primaryPhoneName` missing. Sends an empty `<lines/>` (required choice). Default `Cisco 7941`/SCCP doesn't match `Standard 8861 SIP` template. `securityProfileName` argument ignored. | `XPhone` L16155, L16124, L16140, L16113 |
| `add_phone` (1977) | `vendorConfig` serializes as an empty `<vendorConfig/>`, so `ehook_enable` has no effect **(zeep-verified)** | `XVendorConfig` = `xsd:any` L50232 |
| `add_cti_route_point` / `add_device_profile` | Sends an empty `<lines/>` when there are no lines | `XCtiRoutePoint` L11486; `XDeviceProfile` L17447 |
| `add_directory_number` (1665) | `callForwardAll` omits required (nillable) `secondaryCallingSearchSpaceName` | `XCallForwardAll` L48420 |
| `add_user` (2332) | `firstName` is a required positional argument but optional in the schema | `XUser` L7450 |
| `add_route_pattern` (1407) | `releaseClause` defaults to "Call Rejected" (schema default "No Error"). Docs say gateway and route list can both be used, but the destination is an exclusive choice. Returns a string instead of raising. | `XRoutePattern` L12466, L12473 |
| `add_partition` (1232) | Always sends `timeScheduleIdName="All the time"`, which fails if no schedule with that name exists | `XRoutePartition` L1335 |
| `add_call_manager_group` (3023) | `members` documented as a plain array; needs `{"member":[{callManagerName, priority}]}`, minimum 1 | `XCallManagerGroup` L5370 |
| Update xform / hunt pilot / hunt list / line group / pickup docs | Call `pattern`/`name` "required" when `uuid` is an alternative; omit the `new*` rename elements | `Update*Req` choices |
| `get_translation` / `delete_translation` / `update_translation` | Require a non-empty `routePartitionName`, so `<None>`-partition patterns can't be targeted. Return strings on bad input. | `GetTransPatternReq` L11793 (nillable) |
| `add_translation` (2532) | `routeNextHopByCgpn` accepted but never sent | `XTransPattern` L11698 |
| Member-based adds (MRGL, route group, phone/CTI/UDP lines) | Order/index comes from `list.index()`, so duplicate entries collide | `XPhoneLine/index` L48546 |

### Inconsistent return values

These return the full envelope instead of the object: `get_location`, `get_route_pattern` (uuid path), `get_media_resource_group_list`, `get_translation`, `get_call_manager_group`, `list_route_plan_specific`. `get_sip_profile` and `get_sip_security_profile` return the `return` wrapper.

### Docs site and metadata

| Location | Problem |
|---|---|
| `README.md:2` | Badge points at the `PresidioCode` owner; the remote is `levensailor/ciscoaxl` |
| `README.md:88` | Claims every multi-item getter takes `tagfilter`. `get_translations`, the xform list getters, `get_call_manager_groups` and `list_process_nodes` don't. |
| `README.md:584` | `run_sql_query` example iterates over the result dictionary's keys and uses an `sh` code fence |
| `axl.py:45` | Constructor example: `from axl import AXL`, missing `cucm_version`; `cucm_port` and `strict_ssl` undocumented |
| `docs/linegroup.md`, `rd.md`, `ucservice.md`, `vm.md` | Copies of the users page |
| `docs/about.md`, `api.md`, `intro.md`, `examples.md` | mkdocs boilerplate |
| `mkdocs.yml` | Missing `templates` directory; legacy `selection`/`rendering` keys; `mkdocstrings` lacks the `[python]` extra |
| `schema/current` | Identical to 12.0 and undocumented |

---

## Low severity (documentation only)

- **Stale `:param mini:`** on about 25 list getters; `tagfilter` is never documented. Mutable `dict` defaults are used for `tagfilter`.
- **Copy-paste summaries:**
  - `get_location` says "device pool".
  - `get_transcoder` says "conference bridge".
  - `delete_region` says "location".
  - `get_mtp`/`delete_mtp` say "transcoder".
  - `update_partition` says "calling search space".
  - `get_hunt_lists`/`get_line_groups` say "hunt pilot".
  - `get_media_resource_group(s)` say "route pattern".
  - `update_phone`/`update_cti_route_point` say "Add".
  - `delete_hunt_pilot` says "transformation".
- **Missing docstrings:** `run_sql_query`, `get_phones`, `get_sip_trunks`, `delete_sip_trunk`, `get_sip_security_profile`, `get_sip_profile`, `list_process_nodes`.
- **Docstring params not in the signature:** `add_location` (`cucm_version`), `update_region` (`uuid`), `get_call_manager_groups` (`name`).
- **Empty `:return:` or empty `:param` lines:** most `add_*` methods, plus a duplicate `:return:` in `update_line_group` and the xform updates.
- **Undocumented enum values:**
  - `useCallingPartyPhoneMask` "Default".
  - `distributionAlgorithm` "Longest Idle Time" and "Broadcast".
  - `XHuntAlgorithm`.
  - MTP product values.
- **Undocumented structures:** `members`, `addMembers`/`removeMembers`, SIP trunk `destinations` (`sortOrder` required, max 16), pickup-group members.
- **Undocumented limits:** `description` length limits (`String50`).
- **Typos and stale comments:** "mangaer", "Mulicast", "does anyone use this?".
- **Version drift:** 0.1 in `axl.py`, 0.14 in `docs/source/conf.py`, 0.164 in `pyproject.toml`. The changelog's last release is v0.163. A stray Sphinx tree sits beside mkdocs.

## Undocumented public surface

- **No docs page or README example:** `get_call_manager_groups`, `list_route_plan_specific`, `sql_query`.
- **README example only:** `run_sql_query`, `list_route_plan`.
- **No docs at all:** the helper modules `wsdl.py` (`print_element_layout`, `print_required_element_layout`, `print_return_tags_layout`, `validate_arguments`, `get_tree`, `get_return_tags`) and `helpers.check_tagfilter`. `axl.py` doesn't use them, despite the CHANGELOG's PR#30 entry.

## Recommended order of work

1. **Fix the confirmed breakages:** H1–H7, H11–H15, and H23 (the empty-result guard).
2. **Adopt one convention.** Pick one, ideally schema camelCase names via `**args` with a wrapper dict for `add*`. Then regenerate the docstrings from the schema. `wsdl.py`'s `print_required_element_layout` already does most of the work.
3. **Define the return and error contract:** raise faults, unwrap `["return"][obj]`, and return `[]` for empty lists. Then update the README.
4. **Gate version-specific fields** with the bundled schema (for example, check the zeep type for the element instead of comparing version strings).
5. **Repair the docs build** (`docs/requirements.txt`, mkdocs config) and replace the copied pages.

Then add new endpoints following that convention. Re-run the static schema diff as a check: zero unknown keys and zero missing required fields.
