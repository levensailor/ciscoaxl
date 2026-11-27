"""Offline request tests for ciscoaxl/niche.py.

Run with: pytest tests/test_niche.py
"""
import pytest

from test_offline_requests import make_ucm, sent, text, has


@pytest.fixture
def ucm():
    return make_ucm("15.0")


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


class TestHttpProfile:
    def test_add_http_profile(self, ucm):
        ucm.add_http_profile(
            name="TestHttpProfile",
            userName="admin",
            password="secret",
            webServiceRootUri="https://example.com/api",
        )
        op, body = sent(ucm)
        assert op == "addHttpProfile"
        assert text(body, "httpProfile/name") == "TestHttpProfile"

    def test_get_http_profile_by_name(self, ucm):
        ucm.recorder.responses["getHttpProfile"] = {
            "return": {"httpProfile": {"name": "TestHttpProfile"}}
        }
        result = ucm.get_http_profile(name="TestHttpProfile")
        op, body = sent(ucm)
        assert op == "getHttpProfile"
        assert text(body, "name") == "TestHttpProfile"
        assert result == {"name": "TestHttpProfile"}

    def test_get_http_profile_by_uuid(self, ucm):
        ucm.recorder.responses["getHttpProfile"] = {
            "return": {"httpProfile": {"name": "TestHttpProfile"}}
        }
        ucm.get_http_profile(uuid="{AAAA-1111}")
        op, body = sent(ucm)
        assert op == "getHttpProfile"
        assert text(body, "uuid") == "{AAAA-1111}"
        assert not has(body, "name")

    def test_get_http_profile_raises_on_both(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_http_profile(name="x", uuid="{AAAA-1111}")

    def test_get_http_profile_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_http_profile()

    def test_update_http_profile(self, ucm):
        ucm.update_http_profile(name="TestHttpProfile", webServiceRootUri="/api")
        op, body = sent(ucm)
        assert op == "updateHttpProfile"
        assert text(body, "name") == "TestHttpProfile"

    def test_remove_http_profile_by_name(self, ucm):
        ucm.remove_http_profile(name="TestHttpProfile")
        op, body = sent(ucm)
        assert op == "removeHttpProfile"
        assert text(body, "name") == "TestHttpProfile"

    def test_remove_http_profile_by_uuid(self, ucm):
        ucm.remove_http_profile(uuid="{AAAA-1111}")
        op, body = sent(ucm)
        assert op == "removeHttpProfile"
        assert text(body, "uuid") == "{AAAA-1111}"

    def test_remove_http_profile_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.remove_http_profile()


class TestInfrastructureDevice:
    def test_add_infrastructure_device(self, ucm):
        ucm.add_infrastructure_device(name="switch-01")
        op, body = sent(ucm)
        assert op == "addInfrastructureDevice"
        assert text(body, "infrastructureDevice/name") == "switch-01"

    def test_get_infrastructure_device_by_uuid(self, ucm):
        ucm.recorder.responses["getInfrastructureDevice"] = {
            "return": {"infrastructureDevice": {"name": "switch-01"}}
        }
        result = ucm.get_infrastructure_device(uuid="{BBBB-2222}")
        op, body = sent(ucm)
        assert op == "getInfrastructureDevice"
        assert text(body, "uuid") == "{BBBB-2222}"
        assert result == {"name": "switch-01"}

    def test_get_infrastructure_device_raises_on_missing_uuid(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_infrastructure_device()

    def test_get_infrastructure_devices(self, ucm):
        ucm.recorder.responses["listInfrastructureDevice"] = {
            "return": {"infrastructureDevice": [{"name": "switch-01"}]}
        }
        result = ucm.get_infrastructure_devices()
        op, body = sent(ucm)
        assert op == "listInfrastructureDevice"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_infrastructure_devices_empty(self, ucm):
        ucm.recorder.responses["listInfrastructureDevice"] = {"return": None}
        result = ucm.get_infrastructure_devices()
        assert result == []

    def test_update_infrastructure_device(self, ucm):
        ucm.update_infrastructure_device(uuid="{BBBB-2222}")
        op, body = sent(ucm)
        assert op == "updateInfrastructureDevice"
        assert text(body, "uuid") == "{BBBB-2222}"

    def test_update_infrastructure_device_raises_on_missing_uuid(self, ucm):
        with pytest.raises(ValueError):
            ucm.update_infrastructure_device()

    def test_remove_infrastructure_device_by_uuid(self, ucm):
        ucm.remove_infrastructure_device(uuid="{BBBB-2222}")
        op, body = sent(ucm)
        assert op == "removeInfrastructureDevice"
        assert text(body, "uuid") == "{BBBB-2222}"

    def test_remove_infrastructure_device_raises_on_missing_uuid(self, ucm):
        with pytest.raises(ValueError):
            ucm.remove_infrastructure_device()


class TestInterClusterDirectoryUri:
    def test_update_inter_cluster_directory_uri(self, ucm):
        ucm.update_inter_cluster_directory_uri(
            exchangeDirectoryUri=True,
            routeString="cluster1.example.com",
        )
        op, body = sent(ucm)
        assert op == "updateInterClusterDirectoryUri"
        assert text(body, "routeString") == "cluster1.example.com"


class TestInterClusterServiceProfile:
    def test_get_inter_cluster_service_profile_by_service(self, ucm):
        ucm.recorder.responses["getInterClusterServiceProfile"] = {
            "return": {"interClusterServiceProfile": {"interClusterService": "svc1"}}
        }
        result = ucm.get_inter_cluster_service_profile(interClusterService="svc1")
        op, body = sent(ucm)
        assert op == "getInterClusterServiceProfile"
        assert text(body, "interClusterService") == "svc1"
        assert result == {"interClusterService": "svc1"}

    def test_get_inter_cluster_service_profile_by_uuid(self, ucm):
        ucm.recorder.responses["getInterClusterServiceProfile"] = {
            "return": {"interClusterServiceProfile": {"interClusterService": "svc1"}}
        }
        ucm.get_inter_cluster_service_profile(uuid="{CCCC-3333}")
        op, body = sent(ucm)
        assert op == "getInterClusterServiceProfile"
        assert text(body, "uuid") == "{CCCC-3333}"

    def test_get_inter_cluster_service_profile_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_inter_cluster_service_profile()

    def test_update_inter_cluster_service_profile(self, ucm):
        ucm.update_inter_cluster_service_profile(
            interClusterService="svc1", isActivated=True
        )
        op, body = sent(ucm)
        assert op == "updateInterClusterServiceProfile"
        assert text(body, "interClusterService") == "svc1"


class TestIvrUserLocale:
    def test_add_ivr_user_locale(self, ucm):
        ucm.add_ivr_user_locale(userLocale="English_United_States", orderIndex=1)
        op, body = sent(ucm)
        assert op == "addIvrUserLocale"

    def test_get_ivr_user_locale_by_locale(self, ucm):
        ucm.recorder.responses["getIvrUserLocale"] = {
            "return": {"ivrUserLocale": {"userLocale": "English_United_States"}}
        }
        result = ucm.get_ivr_user_locale(userLocale="English_United_States")
        op, body = sent(ucm)
        assert op == "getIvrUserLocale"
        assert text(body, "userLocale") == "English_United_States"
        assert result == {"userLocale": "English_United_States"}

    def test_get_ivr_user_locale_by_uuid(self, ucm):
        ucm.recorder.responses["getIvrUserLocale"] = {
            "return": {"ivrUserLocale": {"userLocale": "English_United_States"}}
        }
        ucm.get_ivr_user_locale(uuid="{DDDD-4444}")
        op, body = sent(ucm)
        assert op == "getIvrUserLocale"
        assert text(body, "uuid") == "{DDDD-4444}"

    def test_get_ivr_user_locale_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_ivr_user_locale()

    def test_get_ivr_user_locales(self, ucm):
        ucm.recorder.responses["listIvrUserLocale"] = {
            "return": {"ivrUserLocale": [{"userLocale": "English_United_States"}]}
        }
        result = ucm.get_ivr_user_locales()
        op, body = sent(ucm)
        assert op == "listIvrUserLocale"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_ivr_user_locales_empty(self, ucm):
        ucm.recorder.responses["listIvrUserLocale"] = {"return": None}
        result = ucm.get_ivr_user_locales()
        assert result == []

    def test_update_ivr_user_locale(self, ucm):
        ucm.update_ivr_user_locale(userLocale="English_United_States")
        op, body = sent(ucm)
        assert op == "updateIvrUserLocale"
        assert text(body, "userLocale") == "English_United_States"

    def test_remove_ivr_user_locale_by_locale(self, ucm):
        ucm.remove_ivr_user_locale(userLocale="English_United_States")
        op, body = sent(ucm)
        assert op == "removeIvrUserLocale"
        assert text(body, "userLocale") == "English_United_States"

    def test_remove_ivr_user_locale_by_uuid(self, ucm):
        ucm.remove_ivr_user_locale(uuid="{DDDD-4444}")
        op, body = sent(ucm)
        assert op == "removeIvrUserLocale"
        assert text(body, "uuid") == "{DDDD-4444}"

    def test_remove_ivr_user_locale_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.remove_ivr_user_locale()


class TestMlppDomain:
    def test_add_mlpp_domain(self, ucm):
        ucm.add_mlpp_domain(domainName="TestDomain", domainId="ABCDEF")
        op, body = sent(ucm)
        assert op == "addMlppDomain"
        assert text(body, "mlppDomain/domainName") == "TestDomain"

    def test_get_mlpp_domain_by_domain_name(self, ucm):
        ucm.recorder.responses["getMlppDomain"] = {
            "return": {"mlppDomain": {"domainName": "TestDomain"}}
        }
        result = ucm.get_mlpp_domain(domainName="TestDomain")
        op, body = sent(ucm)
        assert op == "getMlppDomain"
        assert text(body, "domainName") == "TestDomain"
        assert result == {"domainName": "TestDomain"}

    def test_get_mlpp_domain_by_uuid(self, ucm):
        ucm.recorder.responses["getMlppDomain"] = {
            "return": {"mlppDomain": {"domainName": "TestDomain"}}
        }
        ucm.get_mlpp_domain(uuid="{EEEE-5555}")
        op, body = sent(ucm)
        assert op == "getMlppDomain"
        assert text(body, "uuid") == "{EEEE-5555}"

    def test_get_mlpp_domain_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_mlpp_domain()

    def test_get_mlpp_domains(self, ucm):
        ucm.recorder.responses["listMlppDomain"] = {
            "return": {"mlppDomain": [{"domainName": "TestDomain"}]}
        }
        result = ucm.get_mlpp_domains()
        op, body = sent(ucm)
        assert op == "listMlppDomain"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_mlpp_domains_empty(self, ucm):
        ucm.recorder.responses["listMlppDomain"] = {"return": None}
        result = ucm.get_mlpp_domains()
        assert result == []

    def test_update_mlpp_domain(self, ucm):
        ucm.update_mlpp_domain(domainName="TestDomain", newDomainName="NewTestDomain")
        op, body = sent(ucm)
        assert op == "updateMlppDomain"
        assert text(body, "domainName") == "TestDomain"

    def test_remove_mlpp_domain_by_domain_name(self, ucm):
        ucm.remove_mlpp_domain(domainName="TestDomain")
        op, body = sent(ucm)
        assert op == "removeMlppDomain"
        assert text(body, "domainName") == "TestDomain"

    def test_remove_mlpp_domain_by_uuid(self, ucm):
        ucm.remove_mlpp_domain(uuid="{EEEE-5555}")
        op, body = sent(ucm)
        assert op == "removeMlppDomain"
        assert text(body, "uuid") == "{EEEE-5555}"

    def test_remove_mlpp_domain_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.remove_mlpp_domain()


class TestMobileSmartClientProfile:
    def test_get_mobile_smart_client_profile_by_name(self, ucm):
        ucm.recorder.responses["getMobileSmartClientProfile"] = {
            "return": {"mobileSmartClientProfile": {"name": "DefaultMobileProfile"}}
        }
        result = ucm.get_mobile_smart_client_profile(name="DefaultMobileProfile")
        op, body = sent(ucm)
        assert op == "getMobileSmartClientProfile"
        assert text(body, "name") == "DefaultMobileProfile"
        assert result == {"name": "DefaultMobileProfile"}

    def test_get_mobile_smart_client_profile_by_uuid(self, ucm):
        ucm.recorder.responses["getMobileSmartClientProfile"] = {
            "return": {"mobileSmartClientProfile": {"name": "DefaultMobileProfile"}}
        }
        ucm.get_mobile_smart_client_profile(uuid="{FFFF-6666}")
        op, body = sent(ucm)
        assert op == "getMobileSmartClientProfile"
        assert text(body, "uuid") == "{FFFF-6666}"

    def test_get_mobile_smart_client_profile_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_mobile_smart_client_profile()

    def test_get_mobile_smart_client_profiles(self, ucm):
        ucm.recorder.responses["listMobileSmartClientProfile"] = {
            "return": {"mobileSmartClientProfile": [{"name": "DefaultMobileProfile"}]}
        }
        result = ucm.get_mobile_smart_client_profiles(
            tagfilter={"name": "", "mobileSmartClient": ""}
        )
        op, body = sent(ucm)
        assert op == "listMobileSmartClientProfile"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_mobile_smart_client_profiles_empty(self, ucm):
        ucm.recorder.responses["listMobileSmartClientProfile"] = {"return": None}
        result = ucm.get_mobile_smart_client_profiles(
            tagfilter={"name": "", "mobileSmartClient": ""}
        )
        assert result == []


class TestNetworkAccessProfile:
    def test_add_network_access_profile(self, ucm):
        ucm.add_network_access_profile(
            name="TestNAP",
            description="Test Profile",
            proxySettings="Manual",
            proxyHostname="proxy.example.com",
        )
        op, body = sent(ucm)
        assert op == "addNetworkAccessProfile"
        assert text(body, "networkAccessProfile/name") == "TestNAP"

    def test_get_network_access_profile_by_name(self, ucm):
        ucm.recorder.responses["getNetworkAccessProfile"] = {
            "return": {"networkAccessProfile": {"name": "TestNAP"}}
        }
        result = ucm.get_network_access_profile(name="TestNAP")
        op, body = sent(ucm)
        assert op == "getNetworkAccessProfile"
        assert text(body, "name") == "TestNAP"
        assert result == {"name": "TestNAP"}

    def test_get_network_access_profile_by_uuid(self, ucm):
        ucm.recorder.responses["getNetworkAccessProfile"] = {
            "return": {"networkAccessProfile": {"name": "TestNAP"}}
        }
        ucm.get_network_access_profile(uuid="{GGGG-7777}")
        op, body = sent(ucm)
        assert op == "getNetworkAccessProfile"
        assert text(body, "uuid") == "{GGGG-7777}"

    def test_get_network_access_profile_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_network_access_profile()

    def test_get_network_access_profiles(self, ucm):
        ucm.recorder.responses["listNetworkAccessProfile"] = {
            "return": {"networkAccessProfile": [{"name": "TestNAP"}]}
        }
        result = ucm.get_network_access_profiles()
        op, body = sent(ucm)
        assert op == "listNetworkAccessProfile"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_network_access_profiles_empty(self, ucm):
        ucm.recorder.responses["listNetworkAccessProfile"] = {"return": None}
        result = ucm.get_network_access_profiles()
        assert result == []

    def test_update_network_access_profile(self, ucm):
        ucm.update_network_access_profile(name="TestNAP", description="Updated")
        op, body = sent(ucm)
        assert op == "updateNetworkAccessProfile"
        assert text(body, "name") == "TestNAP"

    def test_remove_network_access_profile_by_name(self, ucm):
        ucm.remove_network_access_profile(name="TestNAP")
        op, body = sent(ucm)
        assert op == "removeNetworkAccessProfile"
        assert text(body, "name") == "TestNAP"

    def test_remove_network_access_profile_by_uuid(self, ucm):
        ucm.remove_network_access_profile(uuid="{GGGG-7777}")
        op, body = sent(ucm)
        assert op == "removeNetworkAccessProfile"
        assert text(body, "uuid") == "{GGGG-7777}"

    def test_remove_network_access_profile_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.remove_network_access_profile()


class TestPageLayoutPreferences:
    def test_get_page_layout_preferences(self, ucm):
        ucm.recorder.responses["getPageLayoutPreferences"] = {
            "return": {"pageLayoutPreferences": {"pageName": "Phones"}}
        }
        result = ucm.get_page_layout_preferences(pageName="Phones")
        op, body = sent(ucm)
        assert op == "getPageLayoutPreferences"
        assert text(body, "pageName") == "Phones"
        assert result == {"pageName": "Phones"}

    def test_update_page_layout_preferences(self, ucm):
        ucm.update_page_layout_preferences(
            pageName="Phones",
            pageSections={
                "pageSection": [{"name": "Device Information", "state": "show", "order": "0"}]
            },
        )
        op, body = sent(ucm)
        assert op == "updatePageLayoutPreferences"
        assert text(body, "pageName") == "Phones"


class TestPhoneTypeDisplayInstance:
    def test_get_phone_type_display_instance(self, ucm):
        ucm.recorder.responses["getPhoneTypeDisplayInstance"] = {
            "displayInstance": "Cisco 7960"
        }
        result = ucm.get_phone_type_display_instance(
            productName="Cisco 7960",
            protocol="SCCP",
            trunkType="None",
        )
        op, body = sent(ucm)
        assert op == "getPhoneTypeDisplayInstance"
        assert text(body, "productName") == "Cisco 7960"
        assert text(body, "protocol") == "SCCP"
        assert result == "Cisco 7960"

    def test_get_phone_type_display_instance_raises_on_missing_product_name(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_phone_type_display_instance()

    def test_get_phone_type_display_instance_raises_on_missing_protocol(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_phone_type_display_instance(productName="Cisco 7960")


class TestResourcePriorityNamespace:
    def test_add_resource_priority_namespace(self, ucm):
        ucm.add_resource_priority_namespace(
            namespace="dsn.mil", description="DSN namespace"
        )
        op, body = sent(ucm)
        assert op == "addResourcePriorityNamespace"
        assert text(body, "resourcePriorityNamespace/namespace") == "dsn.mil"

    def test_get_resource_priority_namespace_by_namespace(self, ucm):
        ucm.recorder.responses["getResourcePriorityNamespace"] = {
            "return": {"resourcePriorityNamespace": {"namespace": "dsn.mil"}}
        }
        result = ucm.get_resource_priority_namespace(namespace="dsn.mil")
        op, body = sent(ucm)
        assert op == "getResourcePriorityNamespace"
        assert text(body, "namespace") == "dsn.mil"
        assert result == {"namespace": "dsn.mil"}

    def test_get_resource_priority_namespace_by_uuid(self, ucm):
        ucm.recorder.responses["getResourcePriorityNamespace"] = {
            "return": {"resourcePriorityNamespace": {"namespace": "dsn.mil"}}
        }
        ucm.get_resource_priority_namespace(uuid="{IIII-9999}")
        op, body = sent(ucm)
        assert op == "getResourcePriorityNamespace"
        assert text(body, "uuid") == "{IIII-9999}"

    def test_get_resource_priority_namespace_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_resource_priority_namespace()

    def test_get_resource_priority_namespaces(self, ucm):
        ucm.recorder.responses["listResourcePriorityNamespace"] = {
            "return": {"resourcePriorityNamespace": [{"namespace": "dsn.mil"}]}
        }
        result = ucm.get_resource_priority_namespaces()
        op, body = sent(ucm)
        assert op == "listResourcePriorityNamespace"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_resource_priority_namespaces_empty(self, ucm):
        ucm.recorder.responses["listResourcePriorityNamespace"] = {"return": None}
        result = ucm.get_resource_priority_namespaces()
        assert result == []

    def test_update_resource_priority_namespace(self, ucm):
        ucm.update_resource_priority_namespace(namespace="dsn.mil", description="Updated")
        op, body = sent(ucm)
        assert op == "updateResourcePriorityNamespace"
        assert text(body, "namespace") == "dsn.mil"

    def test_remove_resource_priority_namespace_by_namespace(self, ucm):
        ucm.remove_resource_priority_namespace(namespace="dsn.mil")
        op, body = sent(ucm)
        assert op == "removeResourcePriorityNamespace"
        assert text(body, "namespace") == "dsn.mil"

    def test_remove_resource_priority_namespace_by_uuid(self, ucm):
        ucm.remove_resource_priority_namespace(uuid="{IIII-9999}")
        op, body = sent(ucm)
        assert op == "removeResourcePriorityNamespace"
        assert text(body, "uuid") == "{IIII-9999}"

    def test_remove_resource_priority_namespace_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.remove_resource_priority_namespace()

    def test_reset_resource_priority_namespace(self, ucm):
        ucm.reset_resource_priority_namespace(namespace="dsn.mil")
        op, body = sent(ucm)
        assert op == "resetResourcePriorityNamespace"
        assert text(body, "namespace") == "dsn.mil"

    def test_restart_resource_priority_namespace(self, ucm):
        ucm.restart_resource_priority_namespace(namespace="dsn.mil")
        op, body = sent(ucm)
        assert op == "restartResourcePriorityNamespace"
        assert text(body, "namespace") == "dsn.mil"

    def test_apply_resource_priority_namespace(self, ucm):
        ucm.apply_resource_priority_namespace(namespace="dsn.mil")
        op, body = sent(ucm)
        assert op == "applyResourcePriorityNamespace"
        assert text(body, "namespace") == "dsn.mil"


class TestResourcePriorityNamespaceList:
    def test_add_resource_priority_namespace_list(self, ucm):
        ucm.add_resource_priority_namespace_list(
            name="TestNSList", description="Test list"
        )
        op, body = sent(ucm)
        assert op == "addResourcePriorityNamespaceList"
        assert text(body, "resourcePriorityNamespaceList/name") == "TestNSList"

    def test_get_resource_priority_namespace_list_by_name(self, ucm):
        ucm.recorder.responses["getResourcePriorityNamespaceList"] = {
            "return": {"resourcePriorityNamespaceList": {"name": "TestNSList"}}
        }
        result = ucm.get_resource_priority_namespace_list(name="TestNSList")
        op, body = sent(ucm)
        assert op == "getResourcePriorityNamespaceList"
        assert text(body, "name") == "TestNSList"
        assert result == {"name": "TestNSList"}

    def test_get_resource_priority_namespace_list_by_uuid(self, ucm):
        ucm.recorder.responses["getResourcePriorityNamespaceList"] = {
            "return": {"resourcePriorityNamespaceList": {"name": "TestNSList"}}
        }
        ucm.get_resource_priority_namespace_list(uuid="{JJJJ-0000}")
        op, body = sent(ucm)
        assert op == "getResourcePriorityNamespaceList"
        assert text(body, "uuid") == "{JJJJ-0000}"

    def test_get_resource_priority_namespace_list_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_resource_priority_namespace_list()

    def test_get_resource_priority_namespace_lists(self, ucm):
        ucm.recorder.responses["listResourcePriorityNamespaceList"] = {
            "return": {"resourcePriorityNamespaceList": [{"name": "TestNSList"}]}
        }
        result = ucm.get_resource_priority_namespace_lists()
        op, body = sent(ucm)
        assert op == "listResourcePriorityNamespaceList"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_resource_priority_namespace_lists_empty(self, ucm):
        ucm.recorder.responses["listResourcePriorityNamespaceList"] = {"return": None}
        result = ucm.get_resource_priority_namespace_lists()
        assert result == []

    def test_update_resource_priority_namespace_list(self, ucm):
        ucm.update_resource_priority_namespace_list(name="TestNSList", description="Updated")
        op, body = sent(ucm)
        assert op == "updateResourcePriorityNamespaceList"
        assert text(body, "name") == "TestNSList"

    def test_remove_resource_priority_namespace_list_by_name(self, ucm):
        ucm.remove_resource_priority_namespace_list(name="TestNSList")
        op, body = sent(ucm)
        assert op == "removeResourcePriorityNamespaceList"
        assert text(body, "name") == "TestNSList"

    def test_remove_resource_priority_namespace_list_by_uuid(self, ucm):
        ucm.remove_resource_priority_namespace_list(uuid="{JJJJ-0000}")
        op, body = sent(ucm)
        assert op == "removeResourcePriorityNamespaceList"
        assert text(body, "uuid") == "{JJJJ-0000}"

    def test_remove_resource_priority_namespace_list_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.remove_resource_priority_namespace_list()

    def test_reset_resource_priority_namespace_list(self, ucm):
        ucm.reset_resource_priority_namespace_list(name="TestNSList")
        op, body = sent(ucm)
        assert op == "resetResourcePriorityNamespaceList"
        assert text(body, "name") == "TestNSList"

    def test_restart_resource_priority_namespace_list(self, ucm):
        ucm.restart_resource_priority_namespace_list(name="TestNSList")
        op, body = sent(ucm)
        assert op == "restartResourcePriorityNamespaceList"
        assert text(body, "name") == "TestNSList"

    def test_apply_resource_priority_namespace_list(self, ucm):
        ucm.apply_resource_priority_namespace_list(name="TestNSList")
        op, body = sent(ucm)
        assert op == "applyResourcePriorityNamespaceList"
        assert text(body, "name") == "TestNSList"


class TestRoutePartitionsForLearnedPatterns:
    def test_update_route_partitions_for_learned_patterns(self, ucm):
        ucm.update_route_partitions_for_learned_patterns(
            partitionForEnterpriseANo="PT_ENT_ALT",
            partitionForE164ANo="PT_E164_ALT",
            partitionForEnterprisePatterns="PT_ENT",
            partitionForE164Pattern="PT_E164",
            markLearnedEntAltNumbers=True,
            markLearnedE164AltNumbers=True,
            markFixedLengthEntPatterns=True,
            markVariableLengthEntPatterns=True,
            markFixedLengthE164Patterns=True,
            markVariableLengthE164Patterns=True,
        )
        op, body = sent(ucm)
        assert op == "updateRoutePartitionsForLearnedPatterns"
        assert text(body, "partitionForEnterpriseANo") == "PT_ENT_ALT"
        assert text(body, "partitionForE164ANo") == "PT_E164_ALT"


class TestSdpTransparencyProfile:
    def test_add_sdp_transparency_profile(self, ucm):
        ucm.add_sdp_transparency_profile(
            name="TestSDP",
            description="SDP Profile",
            attributeSet=[
                {
                    "attributeNameString": "sendrecv",
                    "sdpAttributeHandling": "forward",
                }
            ],
        )
        op, body = sent(ucm)
        assert op == "addSdpTransparencyProfile"
        assert text(body, "sdpTransparencyProfile/name") == "TestSDP"

    def test_get_sdp_transparency_profile_by_name(self, ucm):
        ucm.recorder.responses["getSdpTransparencyProfile"] = {
            "return": {"sdpTransparencyProfile": {"name": "TestSDP"}}
        }
        result = ucm.get_sdp_transparency_profile(name="TestSDP")
        op, body = sent(ucm)
        assert op == "getSdpTransparencyProfile"
        assert text(body, "name") == "TestSDP"
        assert result == {"name": "TestSDP"}

    def test_get_sdp_transparency_profile_by_uuid(self, ucm):
        ucm.recorder.responses["getSdpTransparencyProfile"] = {
            "return": {"sdpTransparencyProfile": {"name": "TestSDP"}}
        }
        ucm.get_sdp_transparency_profile(uuid="{KKKK-1111}")
        op, body = sent(ucm)
        assert op == "getSdpTransparencyProfile"
        assert text(body, "uuid") == "{KKKK-1111}"

    def test_get_sdp_transparency_profile_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_sdp_transparency_profile()

    def test_get_sdp_transparency_profiles(self, ucm):
        ucm.recorder.responses["listSdpTransparencyProfile"] = {
            "return": {"sdpTransparencyProfile": [{"name": "TestSDP"}]}
        }
        result = ucm.get_sdp_transparency_profiles()
        op, body = sent(ucm)
        assert op == "listSdpTransparencyProfile"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_sdp_transparency_profiles_empty(self, ucm):
        ucm.recorder.responses["listSdpTransparencyProfile"] = {"return": None}
        result = ucm.get_sdp_transparency_profiles()
        assert result == []

    def test_update_sdp_transparency_profile(self, ucm):
        ucm.update_sdp_transparency_profile(name="TestSDP", description="Updated")
        op, body = sent(ucm)
        assert op == "updateSdpTransparencyProfile"
        assert text(body, "name") == "TestSDP"

    def test_remove_sdp_transparency_profile_by_name(self, ucm):
        ucm.remove_sdp_transparency_profile(name="TestSDP")
        op, body = sent(ucm)
        assert op == "removeSdpTransparencyProfile"
        assert text(body, "name") == "TestSDP"

    def test_remove_sdp_transparency_profile_by_uuid(self, ucm):
        ucm.remove_sdp_transparency_profile(uuid="{KKKK-1111}")
        op, body = sent(ucm)
        assert op == "removeSdpTransparencyProfile"
        assert text(body, "uuid") == "{KKKK-1111}"

    def test_remove_sdp_transparency_profile_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.remove_sdp_transparency_profile()


class TestTransportSettings:
    def test_get_transport_settings(self, ucm):
        ucm.recorder.responses["getTransportSettings"] = {
            "return": "true",
            "TransportSettings": {"transportmode": "HTTPS"},
        }
        result = ucm.get_transport_settings()
        op, _ = sent(ucm)
        assert op == "getTransportSettings"
        assert result["transportmode"] == "HTTPS"

    def test_do_update_transport_settings(self, ucm):
        ucm.do_update_transport_settings(
            transportMode="HTTPS",
            url="https://cucm.example.com",
            httpHost="proxy.example.com",
            httpPort="8080",
            enableProxyAuthentication="false",
            proxyUserName="",
            proxyPassword="",
        )
        op, body = sent(ucm)
        assert op == "doUpdateTransportSettings"
        assert text(body, "transportMode") == "HTTPS"


class TestVohServer:
    def test_add_voh_server(self, ucm):
        ucm.add_voh_server(
            name="TestVoH",
            description="Test VoH Server",
            sipTrunkName="SIP-TRUNK",
            defaultVideoStreamId="stream1",
        )
        op, body = sent(ucm)
        assert op == "addVohServer"
        assert text(body, "vohServer/name") == "TestVoH"

    def test_get_voh_server_by_name(self, ucm):
        ucm.recorder.responses["getVohServer"] = {
            "return": {"vohServer": {"name": "TestVoH"}}
        }
        result = ucm.get_voh_server(name="TestVoH")
        op, body = sent(ucm)
        assert op == "getVohServer"
        assert text(body, "name") == "TestVoH"
        assert result == {"name": "TestVoH"}

    def test_get_voh_server_by_uuid(self, ucm):
        ucm.recorder.responses["getVohServer"] = {
            "return": {"vohServer": {"name": "TestVoH"}}
        }
        ucm.get_voh_server(uuid="{LLLL-2222}")
        op, body = sent(ucm)
        assert op == "getVohServer"
        assert text(body, "uuid") == "{LLLL-2222}"

    def test_get_voh_server_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_voh_server()

    def test_get_voh_servers(self, ucm):
        ucm.recorder.responses["listVohServer"] = {
            "return": {"vohServer": [{"name": "TestVoH"}]}
        }
        result = ucm.get_voh_servers()
        op, body = sent(ucm)
        assert op == "listVohServer"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_voh_servers_empty(self, ucm):
        ucm.recorder.responses["listVohServer"] = {"return": None}
        result = ucm.get_voh_servers()
        assert result == []

    def test_update_voh_server(self, ucm):
        ucm.update_voh_server(name="TestVoH", description="Updated")
        op, body = sent(ucm)
        assert op == "updateVohServer"
        assert text(body, "name") == "TestVoH"

    def test_remove_voh_server_by_name(self, ucm):
        ucm.remove_voh_server(name="TestVoH")
        op, body = sent(ucm)
        assert op == "removeVohServer"
        assert text(body, "name") == "TestVoH"

    def test_remove_voh_server_by_uuid(self, ucm):
        ucm.remove_voh_server(uuid="{LLLL-2222}")
        op, body = sent(ucm)
        assert op == "removeVohServer"
        assert text(body, "uuid") == "{LLLL-2222}"

    def test_remove_voh_server_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.remove_voh_server()
