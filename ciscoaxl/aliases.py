"""Translate the SDK's user-friendly argument names into AXL schema element names.

Every request made through ``axl.client`` passes through :class:`AliasingService`, which
looks up the zeep request type of the operation and renames any key the schema does not
accept but an alias resolves to. Keys the schema already accepts are never touched, so AXL
names always work alongside the friendly ones.
"""

import functools
import inspect
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# Friendly field name -> AXL element name. Dotted targets nest (gateway -> destination.gatewayName).
FIELD_ALIASES = {
    "partition": "routePartitionName",
    "route_partition": "routePartitionName",
    "device_pool": "devicePoolName",
    "location": "locationName",
    "css": "callingSearchSpaceName",
    "calling_search_space": "callingSearchSpaceName",
    "aar_css": "automatedAlternateRoutingCssName",
    "subscribe_css": "subscribeCallingSearchSpaceName",
    "security_profile": "securityProfileName",
    "sip_profile": "sipProfileName",
    "media_resource_group_list": "mediaResourceListName",
    "mediaResourceGroupListName": "mediaResourceListName",
    "cm_group": "callManagerGroupName",
    "cm_group_name": "callManagerGroupName",
    "callManagerGroup": "callManagerGroupName",
    "route_list_enabled": "routeListEnabled",
    "run_on_all_nodes": "runOnEveryNode",
    "distribution_algorithm": "distributionAlgorithm",
    "alerting_name": "alertingName",
    "ascii_alerting_name": "asciiAlertingName",
    "vm_profile_name": "voiceMailProfileName",
    "shared_line_css": "shareLineAppearanceCssName",
    "aar_destination_mask": "aarDestinationMask",
    "enable_em": "enableExtensionMobility",
    "use_trusted_relay_point": "useTrustedRelayPoint",
    "owner_user_name": "ownerUserName",
    "withImmersiveKbits": "withinImmersiveKbits",
    "calledPartyTransformationmask": "calledPartyTransformationMask",
    "callingPartyTransformationmask": "callingPartyTransformationMask",
    "status": "dndStatus",
    "device": "deviceName",
    "device_name": "deviceName",
    "user_id": "userid",
    "first_name": "firstName",
    "last_name": "lastName",
    "date_time_group": "dateTimeSettingName",
    "region": "regionName",
    "srst": "srstName",
    "network_locale": "networkLocale",
    "new_name": "newName",
    "new_pattern": "newPattern",
    "new_partition": "newRoutePartitionName",
    "phone_template": "phoneTemplateName",
    "softkey_template": "softkeyTemplateName",
    "common_device_config": "commonDeviceConfigName",
    "protocol_side": "protocolSide",
    "dev_class": "class",
    "sig_digits": "sigDigits",
    "hunt_list": "huntListName",
    "aar_neighborhood": "aarNeighborhoodName",
    "aar_neighbourhood": "aarNeighborhoodName",
    "media_resource_list": "mediaResourceListName",
    "prefix_dn": "prefixDn",
    "pstn_access": "pstnAccess",
    "redirect_in_num_ie": "redirectInboundNumberIe",
    "redirect_out_num_ie": "redirectOutboundNumberIe",
    "cld_party_ie_num_type": "calledPartyIeNumberType",
    "clng_party_ie_num_type": "callingPartyIeNumberType",
    "clng_party_nat_pre": "callingPartyNationalPrefix",
    "clng_party_inat_prefix": "callingPartyInternationalPrefix",
    "clng_party_unknown_prefix": "callingPartyUnknownPrefix",
    "clng_party_sub_prefix": "callingPartySubscriberPrefix",
    "clng_party_nat_strip_digits": "callingPartyNationalStripDigits",
    "clng_party_inat_strip_digits": "callingPartyInternationalStripDigits",
    "clng_party_unknown_strip_digits": "callingPartyUnknownStripDigits",
    "clng_party_sub_strip_digits": "callingPartySubscriberStripDigits",
    "clng_party_nat_trans_css": "callingPartyNationalTransformationCssName",
    "clng_party_inat_trans_css": "callingPartyInternationalTransformationCssName",
    "clng_party_unknown_trans_css": "callingPartyUnknownTransformationCssName",
    "clng_party_sub_trans_css": "callingPartySubscriberTransformationCssName",
    "gateway": "destination.gatewayName",
    "route_list": "destination.routeListName",
}

# Object nouns that identify the object itself (delete_device_pool(device_pool="x") -> name="x").
NAME_NOUNS = {
    "device",
    "device_pool",
    "calling_search_space",
    "css",
    "partition",
    "region",
    "location",
    "route_group",
    "route_list",
    "cti_route_point",
    "phone",
    "profile",
    "transcoder",
    "mtp",
    "srst",
    "conference_bridge",
    "media_resource_group",
    "media_resource_group_list",
    "h323_gateway",
    "sip_trunk",
    "hunt_list",
    "line_group",
    "call_pickup_group",
    "call_manager_group",
}

# Keys that identify a pattern-based object (directory number, hunt pilot, transformations).
PATTERN_NOUNS = {"name", "directory_number", "dn"}


def _children(xsd_type):
    """Return {element_or_attribute_name: xsd_type} accepted directly by a complex type."""
    names = {}
    for name, element in getattr(xsd_type, "elements", []) or []:
        names[name] = getattr(element, "type", None)
    for name, attribute in getattr(xsd_type, "attributes", []) or []:
        if name:
            names[name] = None
    return names


def _resolve(key, allowed):
    """Return the AXL path (list of names) for key, or None to leave it untouched."""
    if key in allowed:
        return None
    target = FIELD_ALIASES.get(key)
    if target and target.split(".")[0] in allowed:
        return target.split(".")
    if key in NAME_NOUNS and "name" in allowed:
        return ["name"]
    if key in PATTERN_NOUNS and "pattern" in allowed and "name" not in allowed:
        return ["pattern"]
    return None


def _is_axl_boolean(xsd_type):
    """AXL booleans are pattern-restricted strings that only accept lowercase true/false/t/f/1/0."""
    qname = getattr(xsd_type, "qname", None)
    return (
        qname is not None
        and qname.localname == "boolean"
        and "cisco.com/AXL" in (qname.namespace or "")
    )


def translate(value, xsd_type):
    """Recursively rename friendly keys in value to the element names of xsd_type."""
    if isinstance(value, list):
        return [translate(v, xsd_type) for v in value]
    if isinstance(value, bool) and _is_axl_boolean(xsd_type):
        return "true" if value else "false"
    if not isinstance(value, dict) or xsd_type is None:
        return value
    allowed = _children(xsd_type)
    if not allowed:
        return value

    out = {}
    renamed = {}
    for key, item in value.items():
        path = _resolve(key, allowed)
        if path is None:
            out[key] = translate(item, allowed.get(key))
            continue
        renamed[key] = ".".join(path)
        if len(path) == 1:
            if path[0] in value:
                raise ValueError(f"Both '{key}' and its AXL name '{path[0]}' were given")
            out[path[0]] = translate(item, allowed.get(path[0]))
        else:
            parent = out.setdefault(path[0], {})
            if not isinstance(parent, dict):
                raise ValueError(f"'{key}' conflicts with '{path[0]}'")
            parent[path[1]] = item
    if renamed:
        logger.debug("Translated argument names %s", renamed)
    return out


def fill_required(value, xsd_type):
    """Add required elements missing from value: the schema default, or nil when nillable."""
    filled = dict(value)
    for name, element in getattr(xsd_type, "elements", []) or []:
        if name in filled or element.is_optional:
            continue
        if element.default is not None:
            filled[name] = element.default
        elif element.nillable:
            filled[name] = None
    return filled


def _canonical(key):
    return FIELD_ALIASES.get(key, key)


def _match_parameter(key, params):
    """Return the method parameter that a keyword the method does not declare stands for."""
    canonical = _canonical(key)
    for param in params:
        if _canonical(param) == canonical:
            return param
    if key in NAME_NOUNS and "name" in params:
        return "name"
    if key in PATTERN_NOUNS and "pattern" in params and "name" not in params:
        return "pattern"
    return None


def accept_aliases(method):
    """Let a method with an explicit signature take friendly nouns and AXL names as keywords."""
    signature = inspect.signature(method)
    params = [
        p.name
        for p in signature.parameters.values()
        if p.kind in (p.POSITIONAL_OR_KEYWORD, p.KEYWORD_ONLY) and p.name != "self"
    ]
    if not params:
        return method

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        for key in [k for k in kwargs if k not in params]:
            target = _match_parameter(key, params)
            if target is None:
                continue
            if target in kwargs:
                raise ValueError(f"Both '{key}' and '{target}' were given")
            kwargs[target] = kwargs.pop(key)
        return method(self, *args, **kwargs)

    return wrapper


def apply_aliases(cls):
    """Class decorator: wrap every public method of cls with accept_aliases."""
    for name, member in list(vars(cls).items()):
        if not name.startswith("_") and inspect.isfunction(member):
            setattr(cls, name, accept_aliases(member))
    return cls


class AliasingService:
    """Proxy for a zeep ServiceProxy that translates friendly names and normalizes list results."""

    def __init__(self, zeep_client, service):
        self._zeep = zeep_client
        self._service = service
        self._operations = service._binding._operations

    def __getattr__(self, op_name):
        operation = getattr(self._service, op_name)
        meta = self._operations.get(op_name)
        if meta is None:
            return operation
        request_type = meta.input.body.type
        elements = list(getattr(request_type, "elements", []) or [])

        def call(*args, **kwargs):
            args = list(args)
            for index, arg in enumerate(args):
                if isinstance(arg, dict) and index < len(elements):
                    args[index] = translate(arg, elements[index][1].type)
            kwargs = translate(kwargs, request_type)
            result = operation(*args, **kwargs)
            if op_name.startswith("list"):
                result = self._empty_list_result(meta, result)
            return result

        call.__name__ = op_name
        return call

    @staticmethod
    def _empty_list_result(meta, result):
        """AXL omits <return> children when nothing matches; give callers an empty list instead."""
        try:
            if result is None or result["return"] is not None:
                return result
            return_type = dict(meta.output.body.type.elements)["return"].type
            item = next(iter(_children(return_type)), None)
            if item is not None:
                result["return"] = {item: []}
        except (KeyError, TypeError, StopIteration):
            pass
        return result
