"""Offline tests for P3 Batch B5 — p3_niche_a.py

Verifies that every method in P3NicheA:
  * calls the correct AXL operation
  * passes the right element names and values
  * handles identifier routing (uuid / name)
  * returns the unwrapped result or [] on empty

Run with: pytest tests/test_p3_b5_niche_a.py
"""
from pathlib import Path

import pytest
from zeep import Client, Settings

from ciscoaxl import axl
from ciscoaxl.aliases import AliasingService

SCHEMA_DIR = Path(__file__).resolve().parent.parent / "ciscoaxl" / "schema"
BINDING = "{http://www.cisco.com/AXLAPIService/}AXLAPIBinding"
_clients = {}


# ---------------------------------------------------------------------------
# Shared test infrastructure (mirrors other offline test files)
# ---------------------------------------------------------------------------

class AutoDict(dict):
    """Canned response: any missing key returns another AutoDict."""

    def __missing__(self, key):
        value = AutoDict()
        self[key] = value
        return value


class Recorder:
    """Stands in for the zeep service: records each call, returns canned response."""

    def __init__(self, zeep_client, service):
        self._zeep = zeep_client
        self._real = service
        self._binding = service._binding
        self.calls = []
        self.responses = {}

    def __getattr__(self, op_name):
        def call(*args, **kwargs):
            envelope, _http_headers = self._real._binding._create(
                op_name, args, kwargs, client=self._zeep
            )
            body = envelope.find("{http://schemas.xmlsoap.org/soap/envelope/}Body")[0]
            self.calls.append((op_name, body))
            response = self.responses.get(op_name, AutoDict())
            if isinstance(response, Exception):
                raise response
            return response

        return call


def make_ucm(version="15.0"):
    if version not in _clients:
        wsdl = (SCHEMA_DIR / version / "AXLAPI.wsdl").as_uri()
        settings = Settings(
            strict=False, xml_huge_tree=True, xsd_ignore_sequence_order=True
        )
        _clients[version] = Client(wsdl, settings=settings)
    zeep_client = _clients[version]
    service = zeep_client.create_service(BINDING, "https://cucm.invalid:8443/axl/")
    recorder = Recorder(zeep_client, service)

    ucm = axl.__new__(axl)
    ucm._zeep = zeep_client
    ucm.cucm = "cucm.invalid"
    ucm.cucm_version = version
    ucm.client = AliasingService(zeep_client, recorder)
    ucm.recorder = recorder
    return ucm


def sent(ucm, index=-1):
    return ucm.recorder.calls[index]


def text(body, path):
    xpath = "./" + "/".join(
        "*" if p == "*" else f"*[local-name()='{p}']" for p in path.split("/")
    )
    found = body.xpath(xpath)
    return found[0].text if found else None


def has(body, path):
    xpath = "./" + "/".join(
        "*" if p == "*" else f"*[local-name()='{p}']" for p in path.split("/")
    )
    return bool(body.xpath(xpath))


@pytest.fixture
def ucm():
    return make_ucm()


# ---------------------------------------------------------------------------
# GeoLocation
# ---------------------------------------------------------------------------

class TestGeoLocation:
    def test_add_geo_location(self, ucm):
        ucm.add_geo_location(name="GeoLoc1")
        op, body = sent(ucm)
        assert op == "addGeoLocation"
        assert text(body, "geoLocation/name") == "GeoLoc1"

    def test_get_geo_location_by_name(self, ucm):
        ucm.recorder.responses["getGeoLocation"] = {
            "return": {"geoLocation": {"name": "GeoLoc1"}}
        }
        result = ucm.get_geo_location(name="GeoLoc1")
        op, body = sent(ucm)
        assert op == "getGeoLocation"
        assert text(body, "name") == "GeoLoc1"
        assert result["name"] == "GeoLoc1"

    def test_get_geo_locations_list(self, ucm):
        ucm.recorder.responses["listGeoLocation"] = {
            "return": {"geoLocation": [{"name": "GeoLoc1"}]}
        }
        result = ucm.get_geo_locations()
        op, body = sent(ucm)
        assert op == "listGeoLocation"
        assert result[0]["name"] == "GeoLoc1"

    def test_get_geo_locations_empty(self, ucm):
        ucm.recorder.responses["listGeoLocation"] = {"return": None}
        assert ucm.get_geo_locations() == []

    def test_update_geo_location(self, ucm):
        ucm.update_geo_location(name="GeoLoc1", description="Updated")
        op, body = sent(ucm)
        assert op == "updateGeoLocation"
        assert text(body, "name") == "GeoLoc1"

    def test_delete_geo_location_by_name(self, ucm):
        ucm.delete_geo_location(name="GeoLoc1")
        op, body = sent(ucm)
        assert op == "removeGeoLocation"
        assert text(body, "name") == "GeoLoc1"


# ---------------------------------------------------------------------------
# GeoLocationFilter
# ---------------------------------------------------------------------------

class TestGeoLocationFilter:
    def test_add_geo_location_filter(self, ucm):
        ucm.add_geo_location_filter(name="GeoFilter1")
        op, body = sent(ucm)
        assert op == "addGeoLocationFilter"
        assert text(body, "geoLocationFilter/name") == "GeoFilter1"

    def test_get_geo_location_filter_by_name(self, ucm):
        ucm.recorder.responses["getGeoLocationFilter"] = {
            "return": {"geoLocationFilter": {"name": "GeoFilter1"}}
        }
        result = ucm.get_geo_location_filter(name="GeoFilter1")
        op, body = sent(ucm)
        assert op == "getGeoLocationFilter"
        assert result["name"] == "GeoFilter1"

    def test_get_geo_location_filters_list(self, ucm):
        ucm.recorder.responses["listGeoLocationFilter"] = {
            "return": {"geoLocationFilter": [{"name": "GeoFilter1"}]}
        }
        result = ucm.get_geo_location_filters()
        assert result[0]["name"] == "GeoFilter1"

    def test_update_geo_location_filter(self, ucm):
        ucm.update_geo_location_filter(name="GeoFilter1", useCountry="true")
        op, body = sent(ucm)
        assert op == "updateGeoLocationFilter"

    def test_delete_geo_location_filter_by_name(self, ucm):
        ucm.delete_geo_location_filter(name="GeoFilter1")
        op, body = sent(ucm)
        assert op == "removeGeoLocationFilter"
        assert text(body, "name") == "GeoFilter1"


# ---------------------------------------------------------------------------
# GeoLocationPolicy
# ---------------------------------------------------------------------------

class TestGeoLocationPolicy:
    def test_add_geo_location_policy(self, ucm):
        ucm.add_geo_location_policy(name="GeoPolicy1")
        op, body = sent(ucm)
        assert op == "addGeoLocationPolicy"
        assert text(body, "geoLocationPolicy/name") == "GeoPolicy1"

    def test_get_geo_location_policy_by_name(self, ucm):
        ucm.recorder.responses["getGeoLocationPolicy"] = {
            "return": {"geoLocationPolicy": {"name": "GeoPolicy1"}}
        }
        result = ucm.get_geo_location_policy(name="GeoPolicy1")
        op, body = sent(ucm)
        assert op == "getGeoLocationPolicy"
        assert result["name"] == "GeoPolicy1"

    def test_get_geo_location_policies_list(self, ucm):
        ucm.recorder.responses["listGeoLocationPolicy"] = {
            "return": {"geoLocationPolicy": [{"name": "GeoPolicy1"}]}
        }
        result = ucm.get_geo_location_policies()
        assert result[0]["name"] == "GeoPolicy1"

    def test_update_geo_location_policy(self, ucm):
        ucm.update_geo_location_policy(uuid="{AAA-111}")
        op, body = sent(ucm)
        assert op == "updateGeoLocationPolicy"

    def test_delete_geo_location_policy_by_uuid(self, ucm):
        ucm.delete_geo_location_policy(uuid="{AAA-111}")
        op, body = sent(ucm)
        assert op == "removeGeoLocationPolicy"
        assert text(body, "uuid") == "{AAA-111}"


# ---------------------------------------------------------------------------
# BillingServer
# ---------------------------------------------------------------------------

class TestBillingServer:
    def test_add_billing_server(self, ucm):
        # BillingServer requires: hostName, userId, password, directory, billingServerProtocol
        ucm.add_billing_server(
            hostName="billing.example.com",
            userId="admin",
            password="secret",
            directory="/var/billing",
            billingServerProtocol="SFTP",
        )
        op, body = sent(ucm)
        assert op == "addBillingServer"
        assert text(body, "billingServer/hostName") == "billing.example.com"
        assert text(body, "billingServer/userId") == "admin"

    def test_get_billing_server(self, ucm):
        ucm.recorder.responses["getBillingServer"] = {
            "return": {"billingServer": {"hostName": "billing.example.com"}}
        }
        result = ucm.get_billing_server(uuid="{BBB-222}")
        op, body = sent(ucm)
        assert op == "getBillingServer"
        assert text(body, "uuid") == "{BBB-222}"
        assert result["hostName"] == "billing.example.com"

    def test_get_billing_servers_list(self, ucm):
        ucm.recorder.responses["listBillingServer"] = {
            "return": {"billingServer": [{"hostName": "billing.example.com"}]}
        }
        result = ucm.get_billing_servers()
        assert result[0]["hostName"] == "billing.example.com"

    def test_update_billing_server(self, ucm):
        # UpdateBillingServerReq valid fields: uuid, userId, password, resendOnFailure, billingServerProtocol
        ucm.update_billing_server(uuid="{BBB-222}", userId="newadmin")
        op, body = sent(ucm)
        assert op == "updateBillingServer"
        assert text(body, "uuid") == "{BBB-222}"

    def test_delete_billing_server(self, ucm):
        ucm.delete_billing_server(uuid="{BBB-222}")
        op, body = sent(ucm)
        assert op == "removeBillingServer"
        assert text(body, "uuid") == "{BBB-222}"


# ---------------------------------------------------------------------------
# BlockedLearnedPatterns
# ---------------------------------------------------------------------------

class TestBlockedLearnedPatterns:
    # BlockedLearnedPatterns has no 'name' field; identity is 'pattern' or 'uuid'
    def test_add_blocked_learned_patterns(self, ucm):
        ucm.add_blocked_learned_patterns(pattern="12345")
        op, body = sent(ucm)
        assert op == "addBlockedLearnedPatterns"
        assert text(body, "blockedLearnedPatterns/pattern") == "12345"

    def test_get_blocked_learned_patterns(self, ucm):
        ucm.recorder.responses["getBlockedLearnedPatterns"] = {
            "return": {"blockedLearnedPatterns": {"pattern": "12345"}}
        }
        result = ucm.get_blocked_learned_patterns(pattern="12345")
        op, body = sent(ucm)
        assert op == "getBlockedLearnedPatterns"
        assert result["pattern"] == "12345"

    def test_get_blocked_learned_patterns_list(self, ucm):
        ucm.recorder.responses["listBlockedLearnedPatterns"] = {
            "return": {"blockedLearnedPatterns": [{"pattern": "12345"}]}
        }
        result = ucm.get_blocked_learned_patterns_list()
        assert result[0]["pattern"] == "12345"

    def test_update_blocked_learned_patterns(self, ucm):
        ucm.update_blocked_learned_patterns(pattern="12345", description="test")
        op, body = sent(ucm)
        assert op == "updateBlockedLearnedPatterns"
        assert text(body, "pattern") == "12345"

    def test_delete_blocked_learned_patterns(self, ucm):
        ucm.delete_blocked_learned_patterns(pattern="12345")
        op, body = sent(ucm)
        assert op == "removeBlockedLearnedPatterns"
        assert text(body, "pattern") == "12345"


# ---------------------------------------------------------------------------
# CCAProfiles
# ---------------------------------------------------------------------------

class TestCCAProfiles:
    # CCAProfiles has no 'name' field; identity is 'ccaId' or 'uuid'
    def test_add_cca_profiles(self, ucm):
        ucm.add_cca_profiles(
            ccaId="cca-001",
            primarySoftSwitchId="switch-01",
            objectClass="device",
        )
        op, body = sent(ucm)
        assert op == "addCCAProfiles"
        assert text(body, "cCAProfiles/ccaId") == "cca-001"

    def test_get_cca_profiles(self, ucm):
        ucm.recorder.responses["getCCAProfiles"] = {
            "return": {"cCAProfiles": {"ccaId": "cca-001"}}
        }
        result = ucm.get_cca_profiles(ccaId="cca-001")
        op, body = sent(ucm)
        assert op == "getCCAProfiles"
        assert result["ccaId"] == "cca-001"

    def test_get_cca_profiles_list(self, ucm):
        ucm.recorder.responses["listCCAProfiles"] = {
            "return": {"cCAProfiles": [{"ccaId": "cca-001"}]}
        }
        result = ucm.get_cca_profiles_list()
        assert result[0]["ccaId"] == "cca-001"

    def test_update_cca_profiles(self, ucm):
        ucm.update_cca_profiles(ccaId="cca-001", sipAliasSuffix="@example.com")
        op, body = sent(ucm)
        assert op == "updateCCAProfiles"
        assert text(body, "ccaId") == "cca-001"

    def test_delete_cca_profiles(self, ucm):
        ucm.delete_cca_profiles(ccaId="cca-001")
        op, body = sent(ucm)
        assert op == "removeCCAProfiles"
        assert text(body, "ccaId") == "cca-001"


# ---------------------------------------------------------------------------
# CiscoCloudOnboarding
# ---------------------------------------------------------------------------

class TestCiscoCloudOnboarding:
    # listCiscoCloudOnboarding searchCriteria has no filterable fields
    def test_get_cisco_cloud_onboarding_list(self, ucm):
        ucm.recorder.responses["listCiscoCloudOnboarding"] = {
            "return": {"ciscoCloudOnboarding": [{"orgId": "org-001"}]}
        }
        result = ucm.get_cisco_cloud_onboarding_list()
        op, body = sent(ucm)
        assert op == "listCiscoCloudOnboarding"
        assert result[0]["orgId"] == "org-001"

    def test_get_cisco_cloud_onboarding_list_empty(self, ucm):
        ucm.recorder.responses["listCiscoCloudOnboarding"] = {"return": None}
        assert ucm.get_cisco_cloud_onboarding_list() == []

    def test_update_cisco_cloud_onboarding(self, ucm):
        # Valid update fields: enablePushNotifications, enableHttpProxy, etc.
        ucm.update_cisco_cloud_onboarding(enablePushNotifications="true")
        op, body = sent(ucm)
        assert op == "updateCiscoCloudOnboarding"


# ---------------------------------------------------------------------------
# CumaServerSecurityProfile
# ---------------------------------------------------------------------------

class TestCumaServerSecurityProfile:
    def test_add_cuma_server_security_profile(self, ucm):
        # Required fields: name + serverIpHostName
        ucm.add_cuma_server_security_profile(
            name="CumaProf1", serverIpHostName="cuma.example.com"
        )
        op, body = sent(ucm)
        assert op == "addCumaServerSecurityProfile"
        assert text(body, "cumaServerSecurityProfile/name") == "CumaProf1"
        assert text(body, "cumaServerSecurityProfile/serverIpHostName") == "cuma.example.com"

    def test_get_cuma_server_security_profile(self, ucm):
        ucm.recorder.responses["getCumaServerSecurityProfile"] = {
            "return": {"cumaServerSecurityProfile": {"name": "CumaProf1"}}
        }
        result = ucm.get_cuma_server_security_profile(name="CumaProf1")
        op, body = sent(ucm)
        assert op == "getCumaServerSecurityProfile"
        assert result["name"] == "CumaProf1"

    def test_get_cuma_server_security_profiles_list(self, ucm):
        ucm.recorder.responses["listCumaServerSecurityProfile"] = {
            "return": {"cumaServerSecurityProfile": [{"name": "CumaProf1"}]}
        }
        result = ucm.get_cuma_server_security_profiles()
        assert result[0]["name"] == "CumaProf1"

    def test_update_cuma_server_security_profile(self, ucm):
        ucm.update_cuma_server_security_profile(name="CumaProf1")
        op, body = sent(ucm)
        assert op == "updateCumaServerSecurityProfile"

    def test_delete_cuma_server_security_profile(self, ucm):
        ucm.delete_cuma_server_security_profile(name="CumaProf1")
        op, body = sent(ucm)
        assert op == "removeCumaServerSecurityProfile"
        assert text(body, "name") == "CumaProf1"


# ---------------------------------------------------------------------------
# Customer
# ---------------------------------------------------------------------------

class TestCustomer:
    def test_add_customer(self, ucm):
        ucm.add_customer(name="Acme Corp")
        op, body = sent(ucm)
        assert op == "addCustomer"
        assert text(body, "customer/name") == "Acme Corp"

    def test_get_customer_by_name(self, ucm):
        ucm.recorder.responses["getCustomer"] = {
            "return": {"customer": {"name": "Acme Corp"}}
        }
        result = ucm.get_customer(name="Acme Corp")
        op, body = sent(ucm)
        assert op == "getCustomer"
        assert result["name"] == "Acme Corp"

    def test_get_customers_list(self, ucm):
        ucm.recorder.responses["listCustomer"] = {
            "return": {"customer": [{"name": "Acme Corp"}]}
        }
        result = ucm.get_customers()
        assert result[0]["name"] == "Acme Corp"

    def test_update_customer(self, ucm):
        ucm.update_customer(name="Acme Corp")
        op, body = sent(ucm)
        assert op == "updateCustomer"

    def test_delete_customer(self, ucm):
        ucm.delete_customer(name="Acme Corp")
        op, body = sent(ucm)
        assert op == "removeCustomer"
        assert text(body, "name") == "Acme Corp"


# ---------------------------------------------------------------------------
# Ddi (read-only)
# ---------------------------------------------------------------------------

class TestDdi:
    def test_get_ddi(self, ucm):
        ucm.recorder.responses["getDdi"] = {
            "return": {"ddi": {"name": "ddi1"}}
        }
        result = ucm.get_ddi(uuid="{DDI-001}")
        op, body = sent(ucm)
        assert op == "getDdi"
        assert text(body, "uuid") == "{DDI-001}"
        assert result["name"] == "ddi1"

    def test_get_ddis_list(self, ucm):
        ucm.recorder.responses["listDdi"] = {
            "return": {"ddi": [{"name": "ddi1"}]}
        }
        result = ucm.get_ddis()
        op, body = sent(ucm)
        assert op == "listDdi"
        assert result[0]["name"] == "ddi1"

    def test_get_ddis_empty(self, ucm):
        ucm.recorder.responses["listDdi"] = {"return": None}
        assert ucm.get_ddis() == []


# ---------------------------------------------------------------------------
# DialPlan (read-only)
# ---------------------------------------------------------------------------

class TestDialPlan:
    def test_get_dial_plan_by_name(self, ucm):
        ucm.recorder.responses["getDialPlan"] = {
            "return": {"dialPlan": {"name": "NANP"}}
        }
        result = ucm.get_dial_plan(name="NANP")
        op, body = sent(ucm)
        assert op == "getDialPlan"
        assert result["name"] == "NANP"

    def test_get_dial_plans_list(self, ucm):
        ucm.recorder.responses["listDialPlan"] = {
            "return": {"dialPlan": [{"name": "NANP"}]}
        }
        result = ucm.get_dial_plans()
        op, body = sent(ucm)
        assert op == "listDialPlan"
        assert result[0]["name"] == "NANP"

    def test_get_dial_plans_empty(self, ucm):
        ucm.recorder.responses["listDialPlan"] = {"return": None}
        assert ucm.get_dial_plans() == []


# ---------------------------------------------------------------------------
# DialPlanTag (read-only)
# ---------------------------------------------------------------------------

class TestDialPlanTag:
    # DialPlanTag identity is uuid alone, or (name + dialPlanName) together
    def test_get_dial_plan_tag_by_uuid(self, ucm):
        ucm.recorder.responses["getDialPlanTag"] = {
            "return": {"dialPlanTag": {"name": "NANP_TAG"}}
        }
        result = ucm.get_dial_plan_tag(uuid="{DPT-001}")
        op, body = sent(ucm)
        assert op == "getDialPlanTag"
        assert text(body, "uuid") == "{DPT-001}"
        assert result["name"] == "NANP_TAG"

    def test_get_dial_plan_tags_list(self, ucm):
        ucm.recorder.responses["listDialPlanTag"] = {
            "return": {"dialPlanTag": [{"name": "NANP_TAG"}]}
        }
        result = ucm.get_dial_plan_tags()
        op, body = sent(ucm)
        assert op == "listDialPlanTag"
        assert result[0]["name"] == "NANP_TAG"

    def test_get_dial_plan_tags_empty(self, ucm):
        ucm.recorder.responses["listDialPlanTag"] = {"return": None}
        assert ucm.get_dial_plan_tags() == []


# ---------------------------------------------------------------------------
# DirNumberAliasLookupandSync
# ---------------------------------------------------------------------------

class TestDirNumberAliasLookupandSync:
    # add requires: ldapConfigName, ldapManagerDisgName, ldapPassword, ldapUserSearch, servers
    # get/update/remove uses 'name' or 'uuid'
    def test_add_dir_number_alias_lookup_and_sync(self, ucm):
        ucm.add_dir_number_alias_lookup_and_sync(
            ldapConfigName="ldap-cfg-1",
            ldapManagerDisgName="cn=manager,dc=example,dc=com",
            ldapPassword="pass",
            ldapUserSearch="dc=example,dc=com",
            servers={"server": [{"hostName": "ldap.example.com", "ldapPort": 389}]},
        )
        op, body = sent(ucm)
        assert op == "addDirNumberAliasLookupandSync"
        assert text(body, "dirNumberAliasLookupandSync/ldapConfigName") == "ldap-cfg-1"

    def test_get_dir_number_alias_lookup_and_sync(self, ucm):
        ucm.recorder.responses["getDirNumberAliasLookupandSync"] = {
            "return": {"dirNumberAliasLookupandSync": {"ldapConfigName": "ldap-cfg-1"}}
        }
        result = ucm.get_dir_number_alias_lookup_and_sync(name="ldap-cfg-1")
        op, body = sent(ucm)
        assert op == "getDirNumberAliasLookupandSync"
        assert result["ldapConfigName"] == "ldap-cfg-1"

    def test_get_dir_number_alias_lookup_and_sync_list(self, ucm):
        ucm.recorder.responses["listDirNumberAliasLookupandSync"] = {
            "return": {"dirNumberAliasLookupandSync": [{"ldapConfigName": "ldap-cfg-1"}]}
        }
        result = ucm.get_dir_number_alias_lookup_and_sync_list()
        assert result[0]["ldapConfigName"] == "ldap-cfg-1"

    def test_update_dir_number_alias_lookup_and_sync(self, ucm):
        ucm.update_dir_number_alias_lookup_and_sync(name="ldap-cfg-1", sipAliasSuffix="@example.com")
        op, body = sent(ucm)
        assert op == "updateDirNumberAliasLookupandSync"
        assert text(body, "name") == "ldap-cfg-1"

    def test_delete_dir_number_alias_lookup_and_sync(self, ucm):
        ucm.delete_dir_number_alias_lookup_and_sync(name="ldap-cfg-1")
        op, body = sent(ucm)
        assert op == "removeDirNumberAliasLookupandSync"
        assert text(body, "name") == "ldap-cfg-1"


# ---------------------------------------------------------------------------
# EmccFeatureConfig (singleton)
# ---------------------------------------------------------------------------

class TestEmccFeatureConfig:
    def test_get_emcc_feature_config(self, ucm):
        ucm.recorder.responses["getEmccFeatureConfig"] = {
            "return": {"emccFeatureConfig": {"value": "true"}}
        }
        result = ucm.get_emcc_feature_config()
        op, body = sent(ucm)
        assert op == "getEmccFeatureConfig"
        assert result["value"] == "true"

    def test_update_emcc_feature_config(self, ucm):
        # UpdateEmccFeatureConfigReq: (uuid | parameterName), value
        ucm.update_emcc_feature_config(parameterName="InterClusterEmccEnabled", value="false")
        op, body = sent(ucm)
        assert op == "updateEmccFeatureConfig"
        assert text(body, "parameterName") == "InterClusterEmccEnabled"


# ---------------------------------------------------------------------------
# FallbackFeatureConfig (singleton)
# ---------------------------------------------------------------------------

class TestFallbackFeatureConfig:
    def test_get_fallback_feature_config(self, ucm):
        ucm.recorder.responses["getFallbackFeatureConfig"] = {
            "return": {"fallbackFeatureConfig": {"enableFallbackForImeCalls": "false"}}
        }
        result = ucm.get_fallback_feature_config()
        op, body = sent(ucm)
        assert op == "getFallbackFeatureConfig"
        assert result["enableFallbackForImeCalls"] == "false"

    def test_update_fallback_feature_config(self, ucm):
        # Valid fields: enableFallbackForImeCalls, qosSensistivityLevel, ...
        ucm.update_fallback_feature_config(enableFallbackForImeCalls="true")
        op, body = sent(ucm)
        assert op == "updateFallbackFeatureConfig"
        assert text(body, "enableFallbackForImeCalls") == "true"


# ---------------------------------------------------------------------------
# FallbackProfile
# ---------------------------------------------------------------------------

class TestFallbackProfile:
    def test_add_fallback_profile(self, ucm):
        ucm.add_fallback_profile(name="FallbackProf1")
        op, body = sent(ucm)
        assert op == "addFallbackProfile"
        assert text(body, "fallbackProfile/name") == "FallbackProf1"

    def test_get_fallback_profile_by_name(self, ucm):
        ucm.recorder.responses["getFallbackProfile"] = {
            "return": {"fallbackProfile": {"name": "FallbackProf1"}}
        }
        result = ucm.get_fallback_profile(name="FallbackProf1")
        op, body = sent(ucm)
        assert op == "getFallbackProfile"
        assert result["name"] == "FallbackProf1"

    def test_get_fallback_profiles_list(self, ucm):
        ucm.recorder.responses["listFallbackProfile"] = {
            "return": {"fallbackProfile": [{"name": "FallbackProf1"}]}
        }
        result = ucm.get_fallback_profiles()
        assert result[0]["name"] == "FallbackProf1"

    def test_update_fallback_profile(self, ucm):
        ucm.update_fallback_profile(name="FallbackProf1")
        op, body = sent(ucm)
        assert op == "updateFallbackProfile"

    def test_delete_fallback_profile(self, ucm):
        ucm.delete_fallback_profile(name="FallbackProf1")
        op, body = sent(ucm)
        assert op == "removeFallbackProfile"
        assert text(body, "name") == "FallbackProf1"


# ---------------------------------------------------------------------------
# HandoffConfiguration (no list in schema)
# ---------------------------------------------------------------------------

class TestHandoffConfiguration:
    # HandoffConfiguration identity is uuid or (pattern + optional routePartitionName)
    def test_add_handoff_configuration(self, ucm):
        ucm.add_handoff_configuration(pattern="9900")
        op, body = sent(ucm)
        assert op == "addHandoffConfiguration"
        assert text(body, "handoffConfiguration/pattern") == "9900"

    def test_get_handoff_configuration(self, ucm):
        ucm.recorder.responses["getHandoffConfiguration"] = {
            "return": {"handoffConfiguration": {"pattern": "9900"}}
        }
        result = ucm.get_handoff_configuration(uuid="{HO-001}")
        op, body = sent(ucm)
        assert op == "getHandoffConfiguration"
        assert text(body, "uuid") == "{HO-001}"
        assert result["pattern"] == "9900"

    def test_update_handoff_configuration(self, ucm):
        ucm.update_handoff_configuration(uuid="{HO-001}")
        op, body = sent(ucm)
        assert op == "updateHandoffConfiguration"
        assert text(body, "uuid") == "{HO-001}"

    def test_delete_handoff_configuration(self, ucm):
        ucm.delete_handoff_configuration(uuid="{HO-001}")
        op, body = sent(ucm)
        assert op == "removeHandoffConfiguration"
        assert text(body, "uuid") == "{HO-001}"
