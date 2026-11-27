"""Offline request tests for ciscoaxl/system.py.

Run with: pytest tests/test_system.py
"""
import pytest

from test_offline_requests import make_ucm, sent, text, has


@pytest.fixture
def ucm():
    return make_ucm("15.0")


class TestDefaultDeviceProfile:
    def test_add_default_device_profile(self, ucm):
        ucm.add_default_device_profile(
            name="TestDDP",
            product="Cisco 7962",
            **{"class": "Phone"},
            protocol="SCCP",
            protocolSide="User",
            phoneButtonTemplate="Standard 7962 SCCP",
            softkeyTemplate="Standard User",
            privacy="Default",
            mlppIndication="Default",
            preemption="Default",
        )
        op, body = sent(ucm)
        assert op == "addDefaultDeviceProfile"
        assert text(body, "defaultDeviceProfile/name") == "TestDDP"

    def test_get_default_device_profile(self, ucm):
        ucm.recorder.responses["getDefaultDeviceProfile"] = {
            "return": {"defaultDeviceProfile": {"name": "TestDDP"}}
        }
        result = ucm.get_default_device_profile(name="TestDDP")
        op, body = sent(ucm)
        assert op == "getDefaultDeviceProfile"
        assert text(body, "name") == "TestDDP"
        assert result == {"name": "TestDDP"}

    def test_get_default_device_profiles(self, ucm):
        ucm.recorder.responses["listDefaultDeviceProfile"] = {
            "return": {"defaultDeviceProfile": [{"name": "TestDDP"}]}
        }
        result = ucm.get_default_device_profiles()
        op, body = sent(ucm)
        assert op == "listDefaultDeviceProfile"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_default_device_profiles_empty(self, ucm):
        ucm.recorder.responses["listDefaultDeviceProfile"] = {"return": None}
        result = ucm.get_default_device_profiles()
        assert result == []

    def test_update_default_device_profile(self, ucm):
        ucm.update_default_device_profile(name="TestDDP", description="Updated")
        op, body = sent(ucm)
        assert op == "updateDefaultDeviceProfile"
        assert text(body, "name") == "TestDDP"

    def test_remove_default_device_profile(self, ucm):
        ucm.remove_default_device_profile(name="TestDDP")
        op, body = sent(ucm)
        assert op == "removeDefaultDeviceProfile"
        assert text(body, "name") == "TestDDP"

    def test_remove_default_device_profile_by_uuid(self, ucm):
        ucm.remove_default_device_profile(uuid="{AAAA-1111}")
        op, body = sent(ucm)
        assert op == "removeDefaultDeviceProfile"
        assert text(body, "uuid") == "{AAAA-1111}"
        assert not has(body, "name")


class TestDeviceDefaults:
    def test_get_device_defaults(self, ucm):
        ucm.recorder.responses["getDeviceDefaults"] = {
            "return": {"deviceDefaults": {"Model": "Cisco 7962", "Protocol": "SCCP"}}
        }
        result = ucm.get_device_defaults(Model="Cisco 7962", Protocol="SCCP")
        op, body = sent(ucm)
        assert op == "getDeviceDefaults"
        assert text(body, "Model") == "Cisco 7962"
        assert text(body, "Protocol") == "SCCP"
        assert result == {"Model": "Cisco 7962", "Protocol": "SCCP"}

    def test_get_device_defaults_by_uuid(self, ucm):
        ucm.recorder.responses["getDeviceDefaults"] = {
            "return": {"deviceDefaults": {"Model": "Cisco 7962"}}
        }
        ucm.get_device_defaults(uuid="{AAAA-1111}")
        op, body = sent(ucm)
        assert op == "getDeviceDefaults"
        assert text(body, "uuid") == "{AAAA-1111}"

    def test_get_device_defaults_requires_identifier(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_device_defaults()
        with pytest.raises(ValueError):
            ucm.get_device_defaults(Model="Cisco 7962")  # missing Protocol

    def test_get_device_defaults_list(self, ucm):
        ucm.recorder.responses["listDeviceDefaults"] = {
            "return": {"deviceDefaults": [{"Model": "Cisco 7962", "Protocol": "SCCP"}]}
        }
        result = ucm.get_device_defaults_list()
        op, body = sent(ucm)
        assert op == "listDeviceDefaults"
        assert len(result) == 1

    def test_get_device_defaults_list_empty(self, ucm):
        ucm.recorder.responses["listDeviceDefaults"] = {"return": None}
        result = ucm.get_device_defaults_list()
        assert result == []

    def test_update_device_defaults(self, ucm):
        ucm.update_device_defaults(Model="Cisco 7962", Protocol="SCCP", LoadInformation="Loads/sccp.load")
        op, body = sent(ucm)
        assert op == "updateDeviceDefaults"
        assert text(body, "Model") == "Cisco 7962"


class TestEnterprisePhoneConfig:
    def test_get_enterprise_phone_config(self, ucm):
        ucm.recorder.responses["getEnterprisePhoneConfig"] = {
            "return": {"enterprisePhoneConfig": {"name": "Enterprise"}}
        }
        result = ucm.get_enterprise_phone_config()
        op, body = sent(ucm)
        assert op == "getEnterprisePhoneConfig"
        assert result == {"name": "Enterprise"}

    def test_update_enterprise_phone_config(self, ucm):
        ucm.update_enterprise_phone_config()
        op, body = sent(ucm)
        assert op == "updateEnterprisePhoneConfig"


class TestFeatureControlPolicy:
    def test_add_feature_control_policy(self, ucm):
        ucm.add_feature_control_policy(name="TestFCP")
        op, body = sent(ucm)
        assert op == "addFeatureControlPolicy"
        assert text(body, "featureControlPolicy/name") == "TestFCP"

    def test_get_feature_control_policy(self, ucm):
        ucm.recorder.responses["getFeatureControlPolicy"] = {
            "return": {"featureControlPolicy": {"name": "TestFCP"}}
        }
        result = ucm.get_feature_control_policy(name="TestFCP")
        op, body = sent(ucm)
        assert op == "getFeatureControlPolicy"
        assert text(body, "name") == "TestFCP"
        assert result == {"name": "TestFCP"}

    def test_get_feature_control_policies(self, ucm):
        ucm.recorder.responses["listFeatureControlPolicy"] = {
            "return": {"featureControlPolicy": [{"name": "TestFCP"}]}
        }
        result = ucm.get_feature_control_policies()
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_feature_control_policies_empty(self, ucm):
        ucm.recorder.responses["listFeatureControlPolicy"] = {"return": None}
        result = ucm.get_feature_control_policies()
        assert result == []

    def test_update_feature_control_policy(self, ucm):
        ucm.update_feature_control_policy(name="TestFCP", description="Updated")
        op, body = sent(ucm)
        assert op == "updateFeatureControlPolicy"

    def test_remove_feature_control_policy(self, ucm):
        ucm.remove_feature_control_policy(name="TestFCP")
        op, body = sent(ucm)
        assert op == "removeFeatureControlPolicy"
        assert text(body, "name") == "TestFCP"

    def test_remove_feature_control_policy_by_uuid(self, ucm):
        ucm.remove_feature_control_policy(uuid="{AAAA-1111}")
        op, body = sent(ucm)
        assert op == "removeFeatureControlPolicy"
        assert text(body, "uuid") == "{AAAA-1111}"


class TestFeatureGroupTemplate:
    def test_add_feature_group_template(self, ucm):
        ucm.add_feature_group_template(name="TestFGT", BLFPresenceGp="Standard Presence Group")
        op, body = sent(ucm)
        assert op == "addFeatureGroupTemplate"
        assert text(body, "featureGroupTemplate/name") == "TestFGT"

    def test_get_feature_group_template(self, ucm):
        ucm.recorder.responses["getFeatureGroupTemplate"] = {
            "return": {"featureGroupTemplate": {"name": "TestFGT"}}
        }
        result = ucm.get_feature_group_template(name="TestFGT")
        op, body = sent(ucm)
        assert op == "getFeatureGroupTemplate"
        assert result == {"name": "TestFGT"}

    def test_get_feature_group_templates(self, ucm):
        ucm.recorder.responses["listFeatureGroupTemplate"] = {
            "return": {"featureGroupTemplate": [{"name": "TestFGT"}]}
        }
        result = ucm.get_feature_group_templates()
        assert len(result) == 1

    def test_get_feature_group_templates_empty(self, ucm):
        ucm.recorder.responses["listFeatureGroupTemplate"] = {"return": None}
        result = ucm.get_feature_group_templates()
        assert result == []

    def test_update_feature_group_template(self, ucm):
        ucm.update_feature_group_template(name="TestFGT", description="Updated")
        op, body = sent(ucm)
        assert op == "updateFeatureGroupTemplate"

    def test_remove_feature_group_template(self, ucm):
        ucm.remove_feature_group_template(name="TestFGT")
        op, body = sent(ucm)
        assert op == "removeFeatureGroupTemplate"
        assert text(body, "name") == "TestFGT"


class TestIpPhoneServices:
    def test_add_ip_phone_service(self, ucm):
        ucm.add_ip_phone_service(
            serviceName="TestSvc",
            asciiServiceName="TestSvc",
            serviceUrl="http://test/",
            serviceCategory="XML Service",
            serviceType="Standard IP Phone Service",
        )
        op, body = sent(ucm)
        assert op == "addIpPhoneServices"
        assert text(body, "ipPhoneServices/serviceName") == "TestSvc"

    def test_get_ip_phone_service(self, ucm):
        ucm.recorder.responses["getIpPhoneServices"] = {
            "return": {"ipPhoneServices": {"serviceName": "TestSvc"}}
        }
        result = ucm.get_ip_phone_service(serviceName="TestSvc")
        op, body = sent(ucm)
        assert op == "getIpPhoneServices"
        assert text(body, "serviceName") == "TestSvc"
        assert result == {"serviceName": "TestSvc"}

    def test_get_ip_phone_service_by_uuid(self, ucm):
        ucm.recorder.responses["getIpPhoneServices"] = {
            "return": {"ipPhoneServices": {"serviceName": "TestSvc"}}
        }
        ucm.get_ip_phone_service(uuid="{AAAA-1111}")
        op, body = sent(ucm)
        assert op == "getIpPhoneServices"
        assert text(body, "uuid") == "{AAAA-1111}"

    def test_get_ip_phone_service_requires_one(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_ip_phone_service()
        with pytest.raises(ValueError):
            ucm.get_ip_phone_service(serviceName="x", uuid="y")

    def test_get_ip_phone_services(self, ucm):
        ucm.recorder.responses["listIpPhoneServices"] = {
            "return": {"ipPhoneServices": [{"serviceName": "TestSvc"}]}
        }
        result = ucm.get_ip_phone_services()
        assert len(result) == 1

    def test_get_ip_phone_services_empty(self, ucm):
        ucm.recorder.responses["listIpPhoneServices"] = {"return": None}
        result = ucm.get_ip_phone_services()
        assert result == []

    def test_update_ip_phone_service(self, ucm):
        ucm.update_ip_phone_service(serviceName="TestSvc", serviceDescription="Updated")
        op, body = sent(ucm)
        assert op == "updateIpPhoneServices"

    def test_remove_ip_phone_service(self, ucm):
        ucm.remove_ip_phone_service(serviceName="TestSvc")
        op, body = sent(ucm)
        assert op == "removeIpPhoneServices"
        assert text(body, "serviceName") == "TestSvc"

    def test_remove_ip_phone_service_by_uuid(self, ucm):
        ucm.remove_ip_phone_service(uuid="{AAAA-1111}")
        op, body = sent(ucm)
        assert op == "removeIpPhoneServices"
        assert text(body, "uuid") == "{AAAA-1111}"

    def test_remove_ip_phone_service_requires_one(self, ucm):
        with pytest.raises(ValueError):
            ucm.remove_ip_phone_service()
        with pytest.raises(ValueError):
            ucm.remove_ip_phone_service(serviceName="x", uuid="y")


class TestSoftKeySet:
    def test_get_soft_key_set(self, ucm):
        ucm.recorder.responses["getSoftKeySet"] = {
            "return": {"softKeySet": {"name": "Default"}}
        }
        result = ucm.get_soft_key_set(name="Default")
        op, body = sent(ucm)
        assert op == "getSoftKeySet"
        assert text(body, "name") == "Default"
        assert result == {"name": "Default"}

    def test_update_soft_key_set(self, ucm):
        ucm.update_soft_key_set(name="Default")
        op, body = sent(ucm)
        assert op == "updateSoftKeySet"
        assert text(body, "name") == "Default"


class TestLdapAuthentication:
    def test_get_ldap_authentication(self, ucm):
        ucm.recorder.responses["getLdapAuthentication"] = {
            "return": {"ldapAuthentication": {"distinguishedName": "cn=admin,dc=corp,dc=com"}}
        }
        result = ucm.get_ldap_authentication()
        op, body = sent(ucm)
        assert op == "getLdapAuthentication"
        assert result == {"distinguishedName": "cn=admin,dc=corp,dc=com"}

    def test_update_ldap_authentication(self, ucm):
        ucm.update_ldap_authentication(distinguishedName="cn=admin,dc=corp,dc=com")
        op, body = sent(ucm)
        assert op == "updateLdapAuthentication"
        assert text(body, "distinguishedName") == "cn=admin,dc=corp,dc=com"


class TestLdapFilter:
    def test_add_ldap_filter(self, ucm):
        ucm.add_ldap_filter(name="SIPFilter", filter="(objectClass=user)")
        op, body = sent(ucm)
        assert op == "addLdapFilter"
        assert text(body, "ldapFilter/name") == "SIPFilter"

    def test_get_ldap_filter(self, ucm):
        ucm.recorder.responses["getLdapFilter"] = {
            "return": {"ldapFilter": {"name": "SIPFilter"}}
        }
        result = ucm.get_ldap_filter(name="SIPFilter")
        op, body = sent(ucm)
        assert op == "getLdapFilter"
        assert text(body, "name") == "SIPFilter"
        assert result == {"name": "SIPFilter"}

    def test_get_ldap_filters(self, ucm):
        ucm.recorder.responses["listLdapFilter"] = {
            "return": {"ldapFilter": [{"name": "SIPFilter"}]}
        }
        result = ucm.get_ldap_filters()
        assert len(result) == 1

    def test_get_ldap_filters_empty(self, ucm):
        ucm.recorder.responses["listLdapFilter"] = {"return": None}
        result = ucm.get_ldap_filters()
        assert result == []

    def test_update_ldap_filter(self, ucm):
        ucm.update_ldap_filter(name="SIPFilter", filter="(objectClass=person)")
        op, body = sent(ucm)
        assert op == "updateLdapFilter"
        assert text(body, "name") == "SIPFilter"

    def test_remove_ldap_filter(self, ucm):
        ucm.remove_ldap_filter(name="SIPFilter")
        op, body = sent(ucm)
        assert op == "removeLdapFilter"
        assert text(body, "name") == "SIPFilter"

    def test_remove_ldap_filter_by_uuid(self, ucm):
        ucm.remove_ldap_filter(uuid="{AAAA-1111}")
        op, body = sent(ucm)
        assert op == "removeLdapFilter"
        assert text(body, "uuid") == "{AAAA-1111}"


class TestLdapSearch:
    def test_get_ldap_search(self, ucm):
        ucm.recorder.responses["getLdapSearch"] = {
            "return": {"ldapSearch": {"distinguishedName": "cn=svc,dc=corp,dc=com"}}
        }
        result = ucm.get_ldap_search(uuid="{AAAA-1111}")
        op, body = sent(ucm)
        assert op == "getLdapSearch"
        assert text(body, "uuid") == "{AAAA-1111}"
        assert result == {"distinguishedName": "cn=svc,dc=corp,dc=com"}

    def test_get_ldap_search_requires_uuid(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_ldap_search()

    def test_get_ldap_searches(self, ucm):
        ucm.recorder.responses["listLdapSearch"] = {
            "return": {"ldapSearch": [{"distinguishedName": "cn=svc,dc=corp,dc=com"}]}
        }
        result = ucm.get_ldap_searches()
        op, body = sent(ucm)
        assert op == "listLdapSearch"
        assert len(result) == 1

    def test_get_ldap_searches_empty(self, ucm):
        ucm.recorder.responses["listLdapSearch"] = {"return": None}
        result = ucm.get_ldap_searches()
        assert result == []

    def test_update_ldap_search(self, ucm):
        ucm.update_ldap_search(uuid="{AAAA-1111}", userSearchBase1="ou=users,dc=corp,dc=com")
        op, body = sent(ucm)
        assert op == "updateLdapSearch"
        assert text(body, "uuid") == "{AAAA-1111}"


class TestLdapSyncCustomField:
    def test_add_ldap_sync_custom_field(self, ucm):
        ucm.add_ldap_sync_custom_field(
            ldapConfigurationName="CorpAD",
            customUserField="ipPhone",
            ldapUserField="telephoneNumber",
        )
        op, body = sent(ucm)
        assert op == "addLdapSyncCustomField"
        assert text(body, "ldapSyncCustomField/ldapConfigurationName") == "CorpAD"

    def test_get_ldap_sync_custom_field(self, ucm):
        ucm.recorder.responses["getLdapSyncCustomField"] = {
            "return": {"ldapSyncCustomField": {"ldapConfigurationName": "CorpAD"}}
        }
        result = ucm.get_ldap_sync_custom_field(
            ldapConfigurationName="CorpAD", customUserField="ipPhone"
        )
        op, body = sent(ucm)
        assert op == "getLdapSyncCustomField"
        assert text(body, "ldapConfigurationName") == "CorpAD"
        assert text(body, "customUserField") == "ipPhone"
        assert result == {"ldapConfigurationName": "CorpAD"}

    def test_get_ldap_sync_custom_field_by_uuid(self, ucm):
        ucm.recorder.responses["getLdapSyncCustomField"] = {
            "return": {"ldapSyncCustomField": {"ldapConfigurationName": "CorpAD"}}
        }
        ucm.get_ldap_sync_custom_field(uuid="{AAAA-1111}")
        op, body = sent(ucm)
        assert op == "getLdapSyncCustomField"
        assert text(body, "uuid") == "{AAAA-1111}"

    def test_get_ldap_sync_custom_field_requires_identifier(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_ldap_sync_custom_field()
        with pytest.raises(ValueError):
            ucm.get_ldap_sync_custom_field(ldapConfigurationName="CorpAD")  # missing customUserField

    def test_get_ldap_sync_custom_fields(self, ucm):
        ucm.recorder.responses["listLdapSyncCustomField"] = {
            "return": {"ldapSyncCustomField": [{"ldapConfigurationName": "CorpAD"}]}
        }
        result = ucm.get_ldap_sync_custom_fields()
        op, body = sent(ucm)
        assert op == "listLdapSyncCustomField"
        assert len(result) == 1

    def test_get_ldap_sync_custom_fields_empty(self, ucm):
        ucm.recorder.responses["listLdapSyncCustomField"] = {"return": None}
        result = ucm.get_ldap_sync_custom_fields()
        assert result == []

    def test_update_ldap_sync_custom_field(self, ucm):
        ucm.update_ldap_sync_custom_field(
            ldapConfigurationName="CorpAD",
            customUserField="ipPhone",
            ldapUserField="mobile",
        )
        op, body = sent(ucm)
        assert op == "updateLdapSyncCustomField"
        assert text(body, "ldapConfigurationName") == "CorpAD"

    def test_remove_ldap_sync_custom_field(self, ucm):
        ucm.remove_ldap_sync_custom_field(
            ldapConfigurationName="CorpAD", customUserField="ipPhone"
        )
        op, body = sent(ucm)
        assert op == "removeLdapSyncCustomField"
        assert text(body, "ldapConfigurationName") == "CorpAD"

    def test_remove_ldap_sync_custom_field_by_uuid(self, ucm):
        ucm.remove_ldap_sync_custom_field(uuid="{AAAA-1111}")
        op, body = sent(ucm)
        assert op == "removeLdapSyncCustomField"
        assert text(body, "uuid") == "{AAAA-1111}"

    def test_remove_ldap_sync_custom_field_requires_identifier(self, ucm):
        with pytest.raises(ValueError):
            ucm.remove_ldap_sync_custom_field()
        with pytest.raises(ValueError):
            ucm.remove_ldap_sync_custom_field(ldapConfigurationName="CorpAD")  # missing customUserField


class TestLdapSystem:
    def test_get_ldap_system(self, ucm):
        ucm.recorder.responses["getLdapSystem"] = {
            "return": {"ldapSystem": {"syncEnabled": True}}
        }
        result = ucm.get_ldap_system()
        op, body = sent(ucm)
        assert op == "getLdapSystem"
        assert result == {"syncEnabled": True}

    def test_update_ldap_system(self, ucm):
        ucm.update_ldap_system(syncEnabled=True, ldapServer="Microsoft Active Directory")
        op, body = sent(ucm)
        assert op == "updateLdapSystem"


class TestCallManager:
    def test_get_call_manager(self, ucm):
        ucm.recorder.responses["getCallManager"] = {
            "return": {"callManager": {"name": "pub.corp.com"}}
        }
        result = ucm.get_call_manager(name="pub.corp.com")
        op, body = sent(ucm)
        assert op == "getCallManager"
        assert text(body, "name") == "pub.corp.com"
        assert result == {"name": "pub.corp.com"}

    def test_get_call_managers(self, ucm):
        ucm.recorder.responses["listCallManager"] = {
            "return": {"callManager": [{"name": "pub.corp.com"}]}
        }
        result = ucm.get_call_managers()
        assert len(result) == 1

    def test_get_call_managers_empty(self, ucm):
        ucm.recorder.responses["listCallManager"] = {"return": None}
        result = ucm.get_call_managers()
        assert result == []

    def test_update_call_manager(self, ucm):
        ucm.update_call_manager(name="pub.corp.com", description="Publisher")
        op, body = sent(ucm)
        assert op == "updateCallManager"
        assert text(body, "name") == "pub.corp.com"

    @pytest.mark.parametrize("method,expected_op", [
        ("apply_call_manager", "applyCallManager"),
        ("reset_call_manager", "resetCallManager"),
        ("restart_call_manager", "restartCallManager"),
    ])
    def test_call_manager_lifecycle_by_name(self, ucm, method, expected_op):
        getattr(ucm, method)(name="pub.corp.com")
        op, body = sent(ucm)
        assert op == expected_op
        assert text(body, "name") == "pub.corp.com"

    @pytest.mark.parametrize("method,expected_op", [
        ("apply_call_manager", "applyCallManager"),
        ("reset_call_manager", "resetCallManager"),
        ("restart_call_manager", "restartCallManager"),
    ])
    def test_call_manager_lifecycle_by_uuid(self, ucm, method, expected_op):
        getattr(ucm, method)(uuid="{AAAA-1111}")
        op, body = sent(ucm)
        assert op == expected_op
        assert text(body, "uuid") == "{AAAA-1111}"

    def test_call_manager_lifecycle_requires_identifier(self, ucm):
        for method in ("apply_call_manager", "reset_call_manager", "restart_call_manager"):
            with pytest.raises(ValueError):
                getattr(ucm, method)()
            with pytest.raises(ValueError):
                getattr(ucm, method)(name="x", uuid="y")


class TestConfigEnterpriseParameters:
    def test_apply_config_enterprise_parameters(self, ucm):
        ucm.apply_config_enterprise_parameters()
        op, body = sent(ucm)
        assert op == "applyConfigEnterpriseParameters"


class TestEnterpriseParameters:
    def test_reset_enterprise_parameters(self, ucm):
        ucm.reset_enterprise_parameters()
        op, body = sent(ucm)
        assert op == "resetEnterpriseParameters"

    def test_restart_enterprise_parameters(self, ucm):
        ucm.restart_enterprise_parameters()
        op, body = sent(ucm)
        assert op == "restartEnterpriseParameters"


class TestOSVersion:
    def test_get_os_version(self, ucm):
        ucm.recorder.responses["getOSVersion"] = {
            "return": {"os": {"osName": "VOS", "osVersion": "14.0.1.12900-20"}}
        }
        result = ucm.get_os_version()
        op, body = sent(ucm)
        assert op == "getOSVersion"
        assert result == {"osName": "VOS", "osVersion": "14.0.1.12900-20"}


class TestProcessNode:
    def test_add_process_node(self, ucm):
        ucm.add_process_node(name="sub.corp.com", description="Subscriber")
        op, body = sent(ucm)
        assert op == "addProcessNode"
        assert text(body, "processNode/name") == "sub.corp.com"

    def test_get_process_node(self, ucm):
        ucm.recorder.responses["getProcessNode"] = {
            "return": {"processNode": {"name": "sub.corp.com"}}
        }
        result = ucm.get_process_node(name="sub.corp.com")
        op, body = sent(ucm)
        assert op == "getProcessNode"
        assert text(body, "name") == "sub.corp.com"
        assert result == {"name": "sub.corp.com"}

    def test_get_process_node_by_uuid(self, ucm):
        ucm.recorder.responses["getProcessNode"] = {
            "return": {"processNode": {"name": "sub.corp.com"}}
        }
        ucm.get_process_node(uuid="{AAAA-1111}")
        op, body = sent(ucm)
        assert op == "getProcessNode"
        assert text(body, "uuid") == "{AAAA-1111}"

    def test_update_process_node(self, ucm):
        ucm.update_process_node(name="sub.corp.com", description="Updated")
        op, body = sent(ucm)
        assert op == "updateProcessNode"
        assert text(body, "name") == "sub.corp.com"

    def test_remove_process_node(self, ucm):
        ucm.remove_process_node(name="sub.corp.com")
        op, body = sent(ucm)
        assert op == "removeProcessNode"
        assert text(body, "name") == "sub.corp.com"

    def test_remove_process_node_by_uuid(self, ucm):
        ucm.remove_process_node(uuid="{AAAA-1111}")
        op, body = sent(ucm)
        assert op == "removeProcessNode"
        assert text(body, "uuid") == "{AAAA-1111}"


class TestProcessNodeService:
    def test_get_process_node_service(self, ucm):
        ucm.recorder.responses["getProcessNodeService"] = {
            "return": {
                "processNodeService": {
                    "processNodeName": "pub.corp.com",
                    "service": "Cisco CallManager",
                }
            }
        }
        result = ucm.get_process_node_service(
            processNodeName="pub.corp.com",
            service_name="Cisco CallManager",
        )
        op, body = sent(ucm)
        assert op == "getProcessNodeService"
        assert text(body, "processNodeName") == "pub.corp.com"
        assert text(body, "service") == "Cisco CallManager"
        assert result["processNodeName"] == "pub.corp.com"

    def test_get_process_node_services(self, ucm):
        ucm.recorder.responses["listProcessNodeService"] = {
            "return": {
                "processNodeService": [
                    {"processNodeName": "pub.corp.com", "service": "Cisco CallManager"}
                ]
            }
        }
        result = ucm.get_process_node_services()
        op, body = sent(ucm)
        assert op == "listProcessNodeService"
        assert len(result) == 1

    def test_get_process_node_services_empty(self, ucm):
        ucm.recorder.responses["listProcessNodeService"] = {"return": None}
        result = ucm.get_process_node_services()
        assert result == []

    def test_update_process_node_service(self, ucm):
        ucm.update_process_node_service(
            processNodeName="pub.corp.com",
            service_name="Cisco CallManager",
            traceLevel="Error",
        )
        op, body = sent(ucm)
        assert op == "updateProcessNodeService"
        assert text(body, "processNodeName") == "pub.corp.com"
        assert text(body, "service") == "Cisco CallManager"


class TestServiceParameter:
    def test_get_service_parameter(self, ucm):
        ucm.recorder.responses["getServiceParameter"] = {
            "return": {
                "serviceParameter": {
                    "processNodeName": "pub.corp.com",
                    "service": "Cisco CallManager",
                    "name": "T302Timer",
                    "value": "15000",
                }
            }
        }
        result = ucm.get_service_parameter(
            processNodeName="pub.corp.com",
            service_name="Cisco CallManager",
            name="T302Timer",
        )
        op, body = sent(ucm)
        assert op == "getServiceParameter"
        assert text(body, "processNodeName") == "pub.corp.com"
        assert text(body, "service") == "Cisco CallManager"
        assert text(body, "name") == "T302Timer"
        assert result["value"] == "15000"

    def test_get_service_parameters(self, ucm):
        ucm.recorder.responses["listServiceParameter"] = {
            "return": {
                "serviceParameter": [
                    {"processNodeName": "pub.corp.com", "service": "Cisco CallManager"}
                ]
            }
        }
        result = ucm.get_service_parameters()
        op, body = sent(ucm)
        assert op == "listServiceParameter"
        assert len(result) == 1

    def test_get_service_parameters_empty(self, ucm):
        ucm.recorder.responses["listServiceParameter"] = {"return": None}
        result = ucm.get_service_parameters()
        assert result == []

    def test_update_service_parameter(self, ucm):
        ucm.update_service_parameter(
            processNodeName="pub.corp.com",
            service_name="Cisco CallManager",
            name="T302Timer",
            value="20000",
        )
        op, body = sent(ucm)
        assert op == "updateServiceParameter"
        assert text(body, "processNodeName") == "pub.corp.com"
        assert text(body, "service") == "Cisco CallManager"
        assert text(body, "value") == "20000"


class TestCredentialPolicy:
    def test_add_credential_policy(self, ucm):
        ucm.add_credential_policy(name="Corp Policy")
        op, body = sent(ucm)
        assert op == "addCredentialPolicy"
        assert text(body, "credentialPolicy/name") == "Corp Policy"

    def test_get_credential_policy(self, ucm):
        ucm.recorder.responses["getCredentialPolicy"] = {
            "return": {"credentialPolicy": {"name": "Corp Policy"}}
        }
        result = ucm.get_credential_policy(name="Corp Policy")
        op, body = sent(ucm)
        assert op == "getCredentialPolicy"
        assert text(body, "name") == "Corp Policy"
        assert result == {"name": "Corp Policy"}

    def test_get_credential_policies(self, ucm):
        ucm.recorder.responses["listCredentialPolicy"] = {
            "return": {"credentialPolicy": [{"name": "Corp Policy"}]}
        }
        result = ucm.get_credential_policies()
        op, body = sent(ucm)
        assert op == "listCredentialPolicy"
        assert len(result) == 1

    def test_get_credential_policies_empty(self, ucm):
        ucm.recorder.responses["listCredentialPolicy"] = {"return": None}
        result = ucm.get_credential_policies()
        assert result == []

    def test_update_credential_policy(self, ucm):
        ucm.update_credential_policy(name="Corp Policy", failedLogon=5)
        op, body = sent(ucm)
        assert op == "updateCredentialPolicy"

    def test_remove_credential_policy(self, ucm):
        ucm.remove_credential_policy(name="Corp Policy")
        op, body = sent(ucm)
        assert op == "removeCredentialPolicy"
        assert text(body, "name") == "Corp Policy"

    def test_remove_credential_policy_by_uuid(self, ucm):
        ucm.remove_credential_policy(uuid="{AAAA-1111}")
        op, body = sent(ucm)
        assert op == "removeCredentialPolicy"
        assert text(body, "uuid") == "{AAAA-1111}"


class TestCredentialPolicyDefault:
    def test_get_credential_policy_default(self, ucm):
        ucm.recorder.responses["getCredentialPolicyDefault"] = {
            "return": {"credentialPolicyDefault": {"credentialUser": {"name": "Corp Policy"}}}
        }
        result = ucm.get_credential_policy_default()
        op, body = sent(ucm)
        assert op == "getCredentialPolicyDefault"
        assert result == {"credentialUser": {"name": "Corp Policy"}}

    def test_update_credential_policy_default(self, ucm):
        ucm.update_credential_policy_default(
            credentialUser="End User",
            credentialType="PIN",
            credPolicyName="Corp Policy",
        )
        op, body = sent(ucm)
        assert op == "updateCredentialPolicyDefault"
        assert text(body, "credentialUser") == "End User"


class TestLicensedUser:
    def test_get_licensed_user(self, ucm):
        ucm.recorder.responses["getLicensedUser"] = {
            "return": {"licensedUser": {"name": "jsmith"}}
        }
        result = ucm.get_licensed_user(name="jsmith")
        op, body = sent(ucm)
        assert op == "getLicensedUser"
        assert text(body, "name") == "jsmith"
        assert result == {"name": "jsmith"}

    def test_get_licensed_user_by_uuid(self, ucm):
        ucm.recorder.responses["getLicensedUser"] = {
            "return": {"licensedUser": {"name": "jsmith"}}
        }
        ucm.get_licensed_user(uuid="{AAAA-1111}")
        op, body = sent(ucm)
        assert op == "getLicensedUser"
        assert text(body, "uuid") == "{AAAA-1111}"

    def test_get_licensed_user_requires_one(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_licensed_user()
        with pytest.raises(ValueError):
            ucm.get_licensed_user(name="jsmith", uuid="{AAAA-1111}")

    def test_get_licensed_users(self, ucm):
        ucm.recorder.responses["listLicensedUser"] = {
            "return": {"licensedUser": [{"userId": "jsmith"}]}
        }
        result = ucm.get_licensed_users()
        op, body = sent(ucm)
        assert op == "listLicensedUser"
        assert len(result) == 1

    def test_get_licensed_users_empty(self, ucm):
        ucm.recorder.responses["listLicensedUser"] = {"return": None}
        result = ucm.get_licensed_users()
        assert result == []


class TestSmartLicenseStatus:
    def test_get_smart_license_status(self, ucm):
        ucm.recorder.responses["getSmartLicenseStatus"] = {
            "return": "Registered",
            "LicenseDetails": {
                "SmartLicensing": "true",
                "Registration": {"Status": "REGISTERED"},
            },
        }
        result = ucm.get_smart_license_status()
        op, body = sent(ucm)
        assert op == "getSmartLicenseStatus"
        assert result["SmartLicensing"] == "true"
        assert result["Registration"]["Status"] == "REGISTERED"


class TestMessageWaiting:
    def test_add_message_waiting(self, ucm):
        ucm.add_message_waiting(pattern="8500", messageWaitingIndicator="Set")
        op, body = sent(ucm)
        assert op == "addMessageWaiting"
        assert text(body, "messageWaiting/pattern") == "8500"

    def test_get_message_waiting(self, ucm):
        ucm.recorder.responses["getMessageWaiting"] = {
            "return": {"messageWaiting": {"pattern": "8500"}}
        }
        result = ucm.get_message_waiting(pattern="8500")
        op, body = sent(ucm)
        assert op == "getMessageWaiting"
        assert text(body, "pattern") == "8500"
        assert result == {"pattern": "8500"}

    def test_get_message_waiting_by_uuid(self, ucm):
        ucm.recorder.responses["getMessageWaiting"] = {
            "return": {"messageWaiting": {"pattern": "8500"}}
        }
        ucm.get_message_waiting(uuid="{AAAA-1111}")
        op, body = sent(ucm)
        assert op == "getMessageWaiting"
        assert text(body, "uuid") == "{AAAA-1111}"

    def test_get_message_waiting_requires_one(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_message_waiting()
        with pytest.raises(ValueError):
            ucm.get_message_waiting(pattern="8500", uuid="{AAAA-1111}")

    def test_get_message_waitings(self, ucm):
        ucm.recorder.responses["listMessageWaiting"] = {
            "return": {"messageWaiting": [{"pattern": "8500"}]}
        }
        result = ucm.get_message_waitings()
        assert len(result) == 1

    def test_get_message_waitings_empty(self, ucm):
        ucm.recorder.responses["listMessageWaiting"] = {"return": None}
        result = ucm.get_message_waitings()
        assert result == []

    def test_update_message_waiting(self, ucm):
        ucm.update_message_waiting(pattern="8500", description="MWI On")
        op, body = sent(ucm)
        assert op == "updateMessageWaiting"
        assert text(body, "pattern") == "8500"

    def test_remove_message_waiting(self, ucm):
        ucm.remove_message_waiting(pattern="8500")
        op, body = sent(ucm)
        assert op == "removeMessageWaiting"
        assert text(body, "pattern") == "8500"

    def test_remove_message_waiting_by_uuid(self, ucm):
        ucm.remove_message_waiting(uuid="{AAAA-1111}")
        op, body = sent(ucm)
        assert op == "removeMessageWaiting"
        assert text(body, "uuid") == "{AAAA-1111}"

    def test_remove_message_waiting_requires_one(self, ucm):
        with pytest.raises(ValueError):
            ucm.remove_message_waiting()
        with pytest.raises(ValueError):
            ucm.remove_message_waiting(pattern="8500", uuid="{AAAA-1111}")


class TestVoiceMailPort:
    def test_add_voice_mail_port(self, ucm):
        ucm.add_voice_mail_port(
            name="VMPORT001",
            product="Cisco VGC Port",
            **{"class": "VoiceMailPort"},
            protocol="SCCP",
            protocolSide="User",
            devicePoolName="Default",
            locationName="Hub_None",
            useTrustedRelayPoint="Default",
            securityProfileName="Cisco VGC Port - Standard SCCP Non-Secure Profile",
            dnPattern="8500",
        )
        op, body = sent(ucm)
        assert op == "addVoiceMailPort"
        assert text(body, "voiceMailPort/name") == "VMPORT001"

    def test_get_voice_mail_port(self, ucm):
        ucm.recorder.responses["getVoiceMailPort"] = {
            "return": {"voiceMailPort": {"name": "VMPORT001"}}
        }
        result = ucm.get_voice_mail_port(name="VMPORT001")
        op, body = sent(ucm)
        assert op == "getVoiceMailPort"
        assert text(body, "name") == "VMPORT001"
        assert result == {"name": "VMPORT001"}

    def test_get_voice_mail_ports(self, ucm):
        ucm.recorder.responses["listVoiceMailPort"] = {
            "return": {"voiceMailPort": [{"name": "VMPORT001"}]}
        }
        result = ucm.get_voice_mail_ports()
        assert len(result) == 1

    def test_get_voice_mail_ports_empty(self, ucm):
        ucm.recorder.responses["listVoiceMailPort"] = {"return": None}
        result = ucm.get_voice_mail_ports()
        assert result == []

    def test_update_voice_mail_port(self, ucm):
        ucm.update_voice_mail_port(name="VMPORT001", description="Updated")
        op, body = sent(ucm)
        assert op == "updateVoiceMailPort"
        assert text(body, "name") == "VMPORT001"

    def test_remove_voice_mail_port(self, ucm):
        ucm.remove_voice_mail_port(name="VMPORT001")
        op, body = sent(ucm)
        assert op == "removeVoiceMailPort"
        assert text(body, "name") == "VMPORT001"

    def test_remove_voice_mail_port_by_uuid(self, ucm):
        ucm.remove_voice_mail_port(uuid="{AAAA-1111}")
        op, body = sent(ucm)
        assert op == "removeVoiceMailPort"
        assert text(body, "uuid") == "{AAAA-1111}"

    @pytest.mark.parametrize("method,expected_op", [
        ("apply_voice_mail_port", "applyVoiceMailPort"),
        ("reset_voice_mail_port", "resetVoiceMailPort"),
        ("restart_voice_mail_port", "restartVoiceMailPort"),
    ])
    def test_voice_mail_port_lifecycle_by_name(self, ucm, method, expected_op):
        getattr(ucm, method)(name="VMPORT001")
        op, body = sent(ucm)
        assert op == expected_op
        assert text(body, "name") == "VMPORT001"

    @pytest.mark.parametrize("method,expected_op", [
        ("apply_voice_mail_port", "applyVoiceMailPort"),
        ("reset_voice_mail_port", "resetVoiceMailPort"),
        ("restart_voice_mail_port", "restartVoiceMailPort"),
    ])
    def test_voice_mail_port_lifecycle_by_uuid(self, ucm, method, expected_op):
        getattr(ucm, method)(uuid="{AAAA-1111}")
        op, body = sent(ucm)
        assert op == expected_op
        assert text(body, "uuid") == "{AAAA-1111}"

    def test_voice_mail_port_lifecycle_requires_identifier(self, ucm):
        for method in ("apply_voice_mail_port", "reset_voice_mail_port", "restart_voice_mail_port"):
            with pytest.raises(ValueError):
                getattr(ucm, method)()
            with pytest.raises(ValueError):
                getattr(ucm, method)(name="x", uuid="y")


class TestApplicationToSoftkeyTemplate:
    def test_add_application_to_softkey_template(self, ucm):
        ucm.add_application_to_softkey_template(
            softKeyTemplateName="Standard User",
            standardSoftKeyTemplateName="Standard User",
        )
        op, body = sent(ucm)
        assert op == "addApplicationToSoftkeyTemplate"
        assert text(body, "applicationToSoftkeyTemplate/softKeyTemplateName") == "Standard User"

    def test_remove_application_to_softkey_template_by_names(self, ucm):
        ucm.remove_application_to_softkey_template(
            softKeyTemplateName="Standard User",
            applicationName="Cisco IP Communicator",
        )
        op, body = sent(ucm)
        assert op == "removeApplicationToSoftkeyTemplate"
        assert text(body, "softKeyTemplateName") == "Standard User"
        assert text(body, "applicationName") == "Cisco IP Communicator"


class TestDeviceProfileOptions:
    def test_get_device_profile_options(self, ucm):
        ucm.recorder.responses["getDeviceProfileOptions"] = {
            "return": {"deviceProfile": {"product": "Cisco 7962"}}
        }
        result = ucm.get_device_profile_options(uuid="{BBBB-2222}")
        op, body = sent(ucm)
        assert op == "getDeviceProfileOptions"
        assert text(body, "uuid") == "{BBBB-2222}"
        assert result == {"product": "Cisco 7962"}


class TestLineOptions:
    def test_get_line_options(self, ucm):
        ucm.recorder.responses["getLineOptions"] = {
            "return": {"line": {"routePartitionName": "Corp_PT"}}
        }
        result = ucm.get_line_options(uuid="{CCCC-3333}")
        op, body = sent(ucm)
        assert op == "getLineOptions"
        assert text(body, "uuid") == "{CCCC-3333}"
        assert result == {"routePartitionName": "Corp_PT"}


class TestNumDevices:
    def test_get_num_devices_phone(self, ucm):
        ucm.recorder.responses["getNumDevices"] = {"return": 42}
        result = ucm.get_num_devices(device_class="Phone")
        op, body = sent(ucm)
        assert op == "getNumDevices"
        assert text(body, "class") == "Phone"
        assert result == 42

    def test_get_num_devices_gateway(self, ucm):
        ucm.recorder.responses["getNumDevices"] = {"return": 10}
        result = ucm.get_num_devices(device_class="Gateway")
        op, body = sent(ucm)
        assert op == "getNumDevices"
        assert text(body, "class") == "Gateway"
        assert result == 10


class TestPhoneOptions:
    def test_get_phone_options(self, ucm):
        ucm.recorder.responses["getPhoneOptions"] = {
            "return": {"phone": {"product": "Cisco 7962"}}
        }
        result = ucm.get_phone_options(uuid="{DDDD-4444}")
        op, body = sent(ucm)
        assert op == "getPhoneOptions"
        assert text(body, "uuid") == "{DDDD-4444}"
        assert result == {"product": "Cisco 7962"}


class TestAppServerInfo:
    def test_add_app_server_info(self, ucm):
        ucm.add_app_server_info(
            appServerName="AppSrv1",
            appServerContent="SomeContent",
        )
        op, body = sent(ucm)
        assert op == "addAppServerInfo"
        assert text(body, "appServerInfo/appServerName") == "AppSrv1"

    def test_get_app_server_info(self, ucm):
        ucm.recorder.responses["getAppServerInfo"] = {
            "return": {"appServerInfo": {"appServerName": "AppSrv1"}}
        }
        result = ucm.get_app_server_info(uuid="{EEEE-5555}")
        op, body = sent(ucm)
        assert op == "getAppServerInfo"
        assert text(body, "uuid") == "{EEEE-5555}"
        assert result == {"appServerName": "AppSrv1"}

    def test_update_app_server_info(self, ucm):
        ucm.update_app_server_info(uuid="{EEEE-5555}", appServerContent="Updated")
        op, body = sent(ucm)
        assert op == "updateAppServerInfo"
        assert text(body, "uuid") == "{EEEE-5555}"

    def test_remove_app_server_info(self, ucm):
        ucm.remove_app_server_info(uuid="{EEEE-5555}")
        op, body = sent(ucm)
        assert op == "removeAppServerInfo"
        assert text(body, "uuid") == "{EEEE-5555}"


class TestApplicationServer:
    def test_add_application_server(self, ucm):
        ucm.add_application_server(
            appServerType="EMService",
            name="AppServer1",
            ipAddress="10.0.0.1",
        )
        op, body = sent(ucm)
        assert op == "addApplicationServer"
        assert text(body, "applicationServer/name") == "AppServer1"

    def test_get_application_server(self, ucm):
        ucm.recorder.responses["getApplicationServer"] = {
            "return": {"applicationServer": {"name": "AppServer1"}}
        }
        result = ucm.get_application_server(uuid="{FFFF-6666}")
        op, body = sent(ucm)
        assert op == "getApplicationServer"
        assert text(body, "uuid") == "{FFFF-6666}"
        assert result == {"name": "AppServer1"}

    def test_get_application_servers(self, ucm):
        ucm.recorder.responses["listApplicationServer"] = {
            "return": {"applicationServer": [{"name": "AppServer1"}]}
        }
        result = ucm.get_application_servers()
        op, body = sent(ucm)
        assert op == "listApplicationServer"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_application_servers_empty(self, ucm):
        ucm.recorder.responses["listApplicationServer"] = {"return": None}
        result = ucm.get_application_servers()
        assert result == []

    def test_update_application_server(self, ucm):
        ucm.update_application_server(uuid="{FFFF-6666}", newName="AppServer1_new")
        op, body = sent(ucm)
        assert op == "updateApplicationServer"
        assert text(body, "uuid") == "{FFFF-6666}"

    def test_remove_application_server(self, ucm):
        ucm.remove_application_server(uuid="{FFFF-6666}")
        op, body = sent(ucm)
        assert op == "removeApplicationServer"
        assert text(body, "uuid") == "{FFFF-6666}"


class TestChange:
    def test_list_changes_no_start_id(self, ucm):
        """First call: omit startChangeId (minOccurs=0 in AXL schema)."""
        ucm.recorder.responses["listChange"] = {
            "queueInfo": {"nextStartChangeId": 100, "queueId": "queue-abc"},
            "changes": {"change": []},
        }
        result = ucm.list_changes()
        op, body = sent(ucm)
        assert op == "listChange"
        # No startChangeId element should appear for first call
        assert not has(body, "startChangeId")
        assert result is not None

    def test_list_changes_with_start_id(self, ucm):
        """Subsequent call: pass startChangeId as zeep-compatible dict."""
        ucm.recorder.responses["listChange"] = {
            "queueInfo": {"nextStartChangeId": 200, "queueId": "queue-abc"},
            "changes": {"change": []},
        }
        result = ucm.list_changes(
            startChangeId={"_value_1": 100, "queueId": "queue-abc"}
        )
        op, body = sent(ucm)
        assert op == "listChange"
        assert has(body, "startChangeId")
        assert result is not None


class TestEnterpriseParametersReset:
    def test_do_enterprise_parameters_reset(self, ucm):
        ucm.do_enterprise_parameters_reset()
        op, body = sent(ucm)
        assert op == "doEnterpriseParametersReset"


class TestPhoneNtp:
    def test_add_phone_ntp_ipv4(self, ucm):
        # AXL XPhoneNtp requires both ipAddress and ipv6Address fields;
        # provide the unused one as an empty string.
        ucm.add_phone_ntp(
            ipAddress="10.0.0.100",
            ipv6Address="",
            description="Corp NTP",
            mode="Directed Broadcast",
        )
        op, body = sent(ucm)
        assert op == "addPhoneNtp"
        assert text(body, "phoneNtp/ipAddress") == "10.0.0.100"

    def test_add_phone_ntp_ipv6(self, ucm):
        ucm.add_phone_ntp(
            ipAddress="",
            ipv6Address="2001:db8::1",
            mode="Directed Broadcast",
        )
        op, body = sent(ucm)
        assert op == "addPhoneNtp"
        assert text(body, "phoneNtp/ipv6Address") == "2001:db8::1"

    def test_get_phone_ntp_by_uuid(self, ucm):
        ucm.recorder.responses["getPhoneNtp"] = {
            "return": {"phoneNtp": {"ipAddress": "10.0.0.100"}}
        }
        result = ucm.get_phone_ntp(uuid="{AAAA-9999}")
        op, body = sent(ucm)
        assert op == "getPhoneNtp"
        assert text(body, "uuid") == "{AAAA-9999}"
        assert result == {"ipAddress": "10.0.0.100"}

    def test_get_phone_ntp_by_ipaddress(self, ucm):
        """AXL choice: when not using uuid, pass both ipAddress+ipv6Address."""
        ucm.recorder.responses["getPhoneNtp"] = {
            "return": {"phoneNtp": {"ipAddress": "10.0.0.100"}}
        }
        ucm.get_phone_ntp(ipAddress="10.0.0.100", ipv6Address="")
        op, body = sent(ucm)
        assert op == "getPhoneNtp"
        assert text(body, "ipAddress") == "10.0.0.100"

    def test_get_phone_ntp_requires_identifier(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_phone_ntp()

    def test_get_phone_ntps(self, ucm):
        ucm.recorder.responses["listPhoneNtp"] = {
            "return": {"phoneNtp": [{"ipAddress": "10.0.0.100"}]}
        }
        result = ucm.get_phone_ntps()
        op, body = sent(ucm)
        assert op == "listPhoneNtp"
        assert len(result) == 1

    def test_get_phone_ntps_empty(self, ucm):
        ucm.recorder.responses["listPhoneNtp"] = {"return": None}
        result = ucm.get_phone_ntps()
        assert result == []

    def test_update_phone_ntp_by_uuid(self, ucm):
        ucm.update_phone_ntp(uuid="{AAAA-9999}", newIpAddress="10.0.0.101")
        op, body = sent(ucm)
        assert op == "updatePhoneNtp"
        assert text(body, "uuid") == "{AAAA-9999}"

    def test_update_phone_ntp_by_ipaddress(self, ucm):
        """AXL choice: when not using uuid, pass both ipAddress+ipv6Address."""
        ucm.update_phone_ntp(
            ipAddress="10.0.0.100", ipv6Address="", newIpAddress="10.0.0.101"
        )
        op, body = sent(ucm)
        assert op == "updatePhoneNtp"
        assert text(body, "ipAddress") == "10.0.0.100"
        assert text(body, "newIpAddress") == "10.0.0.101"

    def test_remove_phone_ntp_by_uuid(self, ucm):
        ucm.remove_phone_ntp(uuid="{AAAA-9999}")
        op, body = sent(ucm)
        assert op == "removePhoneNtp"
        assert text(body, "uuid") == "{AAAA-9999}"

    def test_remove_phone_ntp_by_ipaddress(self, ucm):
        """AXL choice: when not using uuid, pass both ipAddress+ipv6Address."""
        ucm.remove_phone_ntp(ipAddress="10.0.0.100", ipv6Address="")
        op, body = sent(ucm)
        assert op == "removePhoneNtp"
        assert text(body, "ipAddress") == "10.0.0.100"

    def test_remove_phone_ntp_requires_identifier(self, ucm):
        with pytest.raises(ValueError):
            ucm.remove_phone_ntp()


class TestSQLQueryInactive:
    def test_sql_query_inactive_no_rows(self, ucm):
        ucm.recorder.responses["executeSQLQueryInactive"] = {"return": None}
        result = ucm.sql_query_inactive("SELECT 1 FROM device")
        op, body = sent(ucm)
        assert op == "executeSQLQueryInactive"
        assert text(body, "sql") == "SELECT 1 FROM device"
        assert result["num_rows"] == 0
        assert result["query"] == "SELECT 1 FROM device"
        assert "rows" not in result

    def test_sql_query_inactive_with_rows(self, ucm):
        # Build a fake row list that acts like lxml elements
        class FakeCol:
            def __init__(self, tag, text_val):
                self.tag = tag
                self.text = text_val

        class FakeRow(list):
            pass

        row = FakeRow([FakeCol("name", "SEP001122334455")])

        ucm.recorder.responses["executeSQLQueryInactive"] = {
            "return": {"row": [row]}
        }
        result = ucm.sql_query_inactive("SELECT name FROM device")
        assert result["num_rows"] == 1
        assert result["rows"][0]["name"] == "SEP001122334455"


class TestServiceParametersReset:
    def test_do_service_parameters_reset(self, ucm):
        ucm.do_service_parameters_reset(
            processNodeName="pub.corp.com",
            service="Cisco CallManager",
        )
        op, body = sent(ucm)
        assert op == "doServiceParametersReset"
        assert text(body, "processNodeName") == "pub.corp.com"
        assert text(body, "service") == "Cisco CallManager"


class TestSyslogConfiguration:
    def test_get_syslog_configuration(self, ucm):
        ucm.recorder.responses["getSyslogConfiguration"] = {
            "return": {"syslogConfiguration": {"serverName": "pub.corp.com"}}
        }
        result = ucm.get_syslog_configuration(
            serverName="pub.corp.com",
            serviceGroup="CM Services",
            service="Cisco CallManager",
        )
        op, body = sent(ucm)
        assert op == "getSyslogConfiguration"
        assert text(body, "serverName") == "pub.corp.com"
        assert text(body, "serviceGroup") == "CM Services"
        assert text(body, "service") == "Cisco CallManager"
        assert result == {"serverName": "pub.corp.com"}

    def test_update_syslog_configuration(self, ucm):
        # alarmConfigs requires 1-4 AlarmConfig elements (XSyslogConfig).
        # All XSyslogConfig fields within the sequence are required when present.
        alarm = {
            "AlarmLevelEvent": "Warning",
            "RemoteServerName1": "syslog.corp.com",
            "RemoteServerName2": "",
            "RemoteServerName3": "",
            "RemoteServerName4": "",
            "RemoteServerName5": "",
            "monitor": "Local1",
            "Enable": True,
        }
        ucm.update_syslog_configuration(
            serverName="pub.corp.com",
            serviceGroup="CM Services",
            service="Cisco CallManager",
            alarmConfigs={"AlarmConfig": [alarm]},
        )
        op, body = sent(ucm)
        assert op == "updateSyslogConfiguration"
        assert text(body, "serverName") == "pub.corp.com"


class TestAuthenticateUser:
    def test_do_authenticate_user_password(self, ucm):
        ucm.recorder.responses["doAuthenticateUser"] = {
            "return": {"userAuthenticated": "true", "code": 0}
        }
        result = ucm.do_authenticate_user(userid="jsmith", password="secret123")
        op, body = sent(ucm)
        assert op == "doAuthenticateUser"
        assert text(body, "userid") == "jsmith"
        assert text(body, "password") == "secret123"
        assert result["userAuthenticated"] == "true"

    def test_do_authenticate_user_pin(self, ucm):
        ucm.recorder.responses["doAuthenticateUser"] = {
            "return": {"userAuthenticated": "true"}
        }
        ucm.do_authenticate_user(userid="jsmith", pin="1234")
        op, body = sent(ucm)
        assert op == "doAuthenticateUser"
        assert text(body, "pin") == "1234"

    def test_do_authenticate_user_no_credentials(self, ucm):
        # Should succeed without password/pin (AXL allows it)
        ucm.do_authenticate_user(userid="jsmith")
        op, body = sent(ucm)
        assert op == "doAuthenticateUser"
        assert text(body, "userid") == "jsmith"


class TestCustomUserField:
    def test_add_custom_user_field(self, ucm):
        ucm.add_custom_user_field(field="customField1")
        op, body = sent(ucm)
        assert op == "addCustomUserField"
        assert text(body, "customUserField/field") == "customField1"

    def test_get_custom_user_field_by_field(self, ucm):
        ucm.recorder.responses["getCustomUserField"] = {
            "return": {"customUserField": {"field": "customField1"}}
        }
        result = ucm.get_custom_user_field(field="customField1")
        op, body = sent(ucm)
        assert op == "getCustomUserField"
        assert text(body, "field") == "customField1"
        assert result == {"field": "customField1"}

    def test_get_custom_user_field_by_uuid(self, ucm):
        ucm.recorder.responses["getCustomUserField"] = {
            "return": {"customUserField": {"field": "customField1"}}
        }
        ucm.get_custom_user_field(uuid="{AAAA-1111}")
        op, body = sent(ucm)
        assert op == "getCustomUserField"
        assert text(body, "uuid") == "{AAAA-1111}"

    def test_get_custom_user_field_requires_identifier(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_custom_user_field()

    def test_get_custom_user_fields(self, ucm):
        ucm.recorder.responses["listCustomUserField"] = {
            "return": {"customUserField": [{"field": "customField1"}]}
        }
        result = ucm.get_custom_user_fields()
        op, body = sent(ucm)
        assert op == "listCustomUserField"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_custom_user_fields_empty(self, ucm):
        ucm.recorder.responses["listCustomUserField"] = {"return": None}
        result = ucm.get_custom_user_fields()
        assert result == []

    def test_update_custom_user_field(self, ucm):
        ucm.update_custom_user_field(field="customField1", newField="customField1Renamed")
        op, body = sent(ucm)
        assert op == "updateCustomUserField"
        assert text(body, "field") == "customField1"
        assert text(body, "newField") == "customField1Renamed"

    def test_remove_custom_user_field_by_field(self, ucm):
        ucm.remove_custom_user_field(field="customField1")
        op, body = sent(ucm)
        assert op == "removeCustomUserField"
        assert text(body, "field") == "customField1"

    def test_remove_custom_user_field_by_uuid(self, ucm):
        ucm.remove_custom_user_field(uuid="{AAAA-1111}")
        op, body = sent(ucm)
        assert op == "removeCustomUserField"
        assert text(body, "uuid") == "{AAAA-1111}"

    def test_remove_custom_user_field_requires_identifier(self, ucm):
        with pytest.raises(ValueError):
            ucm.remove_custom_user_field()


class TestSelfProvisioning:
    def test_update_self_provisioning(self, ucm):
        ucm.update_self_provisioning(
            requireAuthentication="true",
            authenticationCode="8675",
        )
        op, body = sent(ucm)
        assert op == "updateSelfProvisioning"
        assert text(body, "requireAuthentication") == "true"
        assert text(body, "authenticationCode") == "8675"
