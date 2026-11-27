"""Offline request tests for ciscoaxl/security.py.

Run with: pytest tests/test_security.py
"""
import pytest

from test_offline_requests import make_ucm, sent, text, has


@pytest.fixture
def ucm():
    return make_ucm("15.0")


class TestPhoneSecurityProfile:
    def test_add_phone_security_profile(self, ucm):
        ucm.add_phone_security_profile(name="Cisco 8861 - Standard SIP Non-Secure Profile")
        op, body = sent(ucm)
        assert op == "addPhoneSecurityProfile"
        assert text(body, "phoneSecurityProfile/name") == "Cisco 8861 - Standard SIP Non-Secure Profile"

    def test_get_phone_security_profile_by_name(self, ucm):
        ucm.recorder.responses["getPhoneSecurityProfile"] = {
            "return": {"phoneSecurityProfile": {"name": "TestProfile"}}
        }
        result = ucm.get_phone_security_profile(name="TestProfile")
        op, body = sent(ucm)
        assert op == "getPhoneSecurityProfile"
        assert text(body, "name") == "TestProfile"
        assert result == {"name": "TestProfile"}

    def test_get_phone_security_profile_by_uuid(self, ucm):
        ucm.recorder.responses["getPhoneSecurityProfile"] = {
            "return": {"phoneSecurityProfile": {"uuid": "{1234}"}}
        }
        ucm.get_phone_security_profile(uuid="{1234}")
        op, body = sent(ucm)
        assert text(body, "uuid") == "{1234}"
        assert not has(body, "name")

    def test_get_phone_security_profiles_calls_list(self, ucm):
        ucm.recorder.responses["listPhoneSecurityProfile"] = {
            "return": {"phoneSecurityProfile": [{"name": "Profile1"}]}
        }
        result = ucm.get_phone_security_profiles()
        op, body = sent(ucm)
        assert op == "listPhoneSecurityProfile"
        assert result == [{"name": "Profile1"}]

    def test_get_phone_security_profiles_empty(self, ucm):
        ucm.recorder.responses["listPhoneSecurityProfile"] = {"return": None}
        result = ucm.get_phone_security_profiles()
        assert result == []

    def test_update_phone_security_profile(self, ucm):
        ucm.update_phone_security_profile(name="Profile1", newName="Profile2")
        op, body = sent(ucm)
        assert op == "updatePhoneSecurityProfile"
        assert text(body, "name") == "Profile1"
        assert text(body, "newName") == "Profile2"

    def test_delete_phone_security_profile(self, ucm):
        ucm.delete_phone_security_profile(name="Profile1")
        op, body = sent(ucm)
        assert op == "removePhoneSecurityProfile"
        assert text(body, "name") == "Profile1"

    def test_apply_phone_security_profile(self, ucm):
        ucm.apply_phone_security_profile(name="Profile1")
        op, body = sent(ucm)
        assert op == "applyPhoneSecurityProfile"
        assert text(body, "name") == "Profile1"

    def test_reset_phone_security_profile(self, ucm):
        ucm.reset_phone_security_profile(name="Profile1")
        op, body = sent(ucm)
        assert op == "resetPhoneSecurityProfile"
        assert text(body, "name") == "Profile1"

    def test_name_and_uuid_both_raises(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_phone_security_profile(name="x", uuid="y")


class TestSipProfile:
    def test_add_sip_profile(self, ucm):
        ucm.add_sip_profile(name="Standard SIP Profile")
        op, body = sent(ucm)
        assert op == "addSipProfile"
        assert text(body, "sipProfile/name") == "Standard SIP Profile"

    def test_get_sip_profiles_calls_list(self, ucm):
        ucm.recorder.responses["listSipProfile"] = {
            "return": {"sipProfile": [{"name": "Standard SIP Profile"}]}
        }
        result = ucm.get_sip_profiles()
        op, body = sent(ucm)
        assert op == "listSipProfile"
        assert len(result) == 1

    def test_get_sip_profiles_empty(self, ucm):
        ucm.recorder.responses["listSipProfile"] = {"return": None}
        result = ucm.get_sip_profiles()
        assert result == []

    def test_update_sip_profile(self, ucm):
        ucm.update_sip_profile(name="Standard SIP Profile", newName="Custom SIP Profile")
        op, body = sent(ucm)
        assert op == "updateSipProfile"

    def test_delete_sip_profile(self, ucm):
        ucm.delete_sip_profile(name="Standard SIP Profile")
        op, body = sent(ucm)
        assert op == "removeSipProfile"
        assert text(body, "name") == "Standard SIP Profile"

    def test_apply_sip_profile(self, ucm):
        ucm.apply_sip_profile(name="Standard SIP Profile")
        op, body = sent(ucm)
        assert op == "applySipProfile"
        assert text(body, "name") == "Standard SIP Profile"

    def test_restart_sip_profile(self, ucm):
        ucm.restart_sip_profile(name="Standard SIP Profile")
        op, body = sent(ucm)
        assert op == "restartSipProfile"
        assert text(body, "name") == "Standard SIP Profile"

    def test_get_sip_profile_still_works(self, ucm):
        """get_sip_profile from axl.py must still resolve without error."""
        ucm.recorder.responses["getSipProfile"] = {
            "return": {"sipProfile": {"name": "Standard SIP Profile"}}
        }
        result = ucm.get_sip_profile(name="Standard SIP Profile")
        assert result == {"name": "Standard SIP Profile"}


class TestSipTrunkSecurityProfile:
    def test_add_sip_trunk_security_profile(self, ucm):
        ucm.add_sip_trunk_security_profile(name="Non Secure SIP Trunk Profile")
        op, body = sent(ucm)
        assert op == "addSipTrunkSecurityProfile"
        assert text(body, "sipTrunkSecurityProfile/name") == "Non Secure SIP Trunk Profile"

    def test_get_sip_trunk_security_profiles(self, ucm):
        ucm.recorder.responses["listSipTrunkSecurityProfile"] = {
            "return": {
                "sipTrunkSecurityProfile": [{"name": "Non Secure SIP Trunk Profile"}]
            }
        }
        result = ucm.get_sip_trunk_security_profiles()
        op, body = sent(ucm)
        assert op == "listSipTrunkSecurityProfile"
        assert len(result) == 1

    def test_get_sip_trunk_security_profiles_empty(self, ucm):
        ucm.recorder.responses["listSipTrunkSecurityProfile"] = {"return": None}
        result = ucm.get_sip_trunk_security_profiles()
        assert result == []

    def test_update_sip_trunk_security_profile(self, ucm):
        ucm.update_sip_trunk_security_profile(name="Profile1", newName="Profile2")
        op, body = sent(ucm)
        assert op == "updateSipTrunkSecurityProfile"

    def test_delete_sip_trunk_security_profile(self, ucm):
        ucm.delete_sip_trunk_security_profile(name="Non Secure SIP Trunk Profile")
        op, body = sent(ucm)
        assert op == "removeSipTrunkSecurityProfile"
        assert text(body, "name") == "Non Secure SIP Trunk Profile"

    def test_apply_sip_trunk_security_profile(self, ucm):
        ucm.apply_sip_trunk_security_profile(name="Non Secure SIP Trunk Profile")
        op, body = sent(ucm)
        assert op == "applySipTrunkSecurityProfile"

    def test_reset_sip_trunk_security_profile(self, ucm):
        ucm.reset_sip_trunk_security_profile(name="Non Secure SIP Trunk Profile")
        op, body = sent(ucm)
        assert op == "resetSipTrunkSecurityProfile"

    def test_get_sip_security_profile_still_works(self, ucm):
        """get_sip_security_profile from axl.py must still resolve."""
        ucm.recorder.responses["getSipTrunkSecurityProfile"] = {
            "return": {"sipTrunkSecurityProfile": {"name": "Non Secure SIP Trunk Profile"}}
        }
        result = ucm.get_sip_security_profile(name="Non Secure SIP Trunk Profile")
        assert result == {"name": "Non Secure SIP Trunk Profile"}


class TestDateTimeGroup:
    def test_add_date_time_group(self, ucm):
        ucm.add_date_time_group(name="CMLocal", timeZone="(GMT-05:00) America/New_York")
        op, body = sent(ucm)
        assert op == "addDateTimeGroup"
        assert text(body, "dateTimeGroup/name") == "CMLocal"

    def test_get_date_time_group(self, ucm):
        ucm.recorder.responses["getDateTimeGroup"] = {
            "return": {"dateTimeGroup": {"name": "CMLocal"}}
        }
        result = ucm.get_date_time_group(name="CMLocal")
        op, body = sent(ucm)
        assert op == "getDateTimeGroup"
        assert text(body, "name") == "CMLocal"
        assert result == {"name": "CMLocal"}

    def test_get_date_time_groups(self, ucm):
        ucm.recorder.responses["listDateTimeGroup"] = {
            "return": {"dateTimeGroup": [{"name": "CMLocal"}]}
        }
        result = ucm.get_date_time_groups()
        op, body = sent(ucm)
        assert op == "listDateTimeGroup"
        assert len(result) == 1

    def test_get_date_time_groups_empty(self, ucm):
        ucm.recorder.responses["listDateTimeGroup"] = {"return": None}
        result = ucm.get_date_time_groups()
        assert result == []

    def test_update_date_time_group(self, ucm):
        ucm.update_date_time_group(name="CMLocal", newName="CMLocal_EST")
        op, body = sent(ucm)
        assert op == "updateDateTimeGroup"
        assert text(body, "name") == "CMLocal"

    def test_delete_date_time_group(self, ucm):
        ucm.delete_date_time_group(name="CMLocal")
        op, body = sent(ucm)
        assert op == "removeDateTimeGroup"
        assert text(body, "name") == "CMLocal"

    def test_apply_date_time_group(self, ucm):
        ucm.apply_date_time_group(name="CMLocal")
        op, body = sent(ucm)
        assert op == "applyDateTimeGroup"

    def test_reset_date_time_group(self, ucm):
        ucm.reset_date_time_group(name="CMLocal")
        op, body = sent(ucm)
        assert op == "resetDateTimeGroup"

    def test_name_uuid_mutual_exclusion(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_date_time_group(name="CMLocal", uuid="{1234}")


class TestLdapDirectory:
    def test_add_ldap_directory(self, ucm):
        ucm.add_ldap_directory(
            name="CorpAD",
            ldapDn="cn=admin,dc=corp,dc=com",
            ldapPassword="secret",
            userSearchBase="dc=corp,dc=com",
            nextExecTime="00:00",
            servers={"server": [{"hostName": "ldap.corp.com", "ldapPortNumber": "389"}]},
        )
        op, body = sent(ucm)
        assert op == "addLdapDirectory"
        assert text(body, "ldapDirectory/name") == "CorpAD"

    def test_get_ldap_directory(self, ucm):
        ucm.recorder.responses["getLdapDirectory"] = {
            "return": {"ldapDirectory": {"name": "CorpAD"}}
        }
        result = ucm.get_ldap_directory(name="CorpAD")
        op, body = sent(ucm)
        assert op == "getLdapDirectory"
        assert text(body, "name") == "CorpAD"
        assert result == {"name": "CorpAD"}

    def test_update_ldap_directory(self, ucm):
        ucm.update_ldap_directory(name="CorpAD", ldapDn="cn=svc,dc=corp,dc=com")
        op, body = sent(ucm)
        assert op == "updateLdapDirectory"
        assert text(body, "name") == "CorpAD"

    def test_delete_ldap_directory(self, ucm):
        ucm.delete_ldap_directory(name="CorpAD")
        op, body = sent(ucm)
        assert op == "removeLdapDirectory"
        assert text(body, "name") == "CorpAD"

    def test_delete_ldap_directory_by_uuid(self, ucm):
        ucm.delete_ldap_directory(uuid="{AAAA-1111}")
        op, body = sent(ucm)
        assert text(body, "uuid") == "{AAAA-1111}"
        assert not has(body, "name")

    def test_get_ldap_dir_still_works(self, ucm):
        """Existing get_ldap_dir (listLdapDirectory) must still resolve."""
        ucm.recorder.responses["listLdapDirectory"] = {
            "return": {"ldapDirectory": [{"name": "CorpAD"}]}
        }
        result = ucm.get_ldap_dir()
        assert isinstance(result, list)


class TestLdapSyncStatus:
    def test_get_ldap_sync_status(self, ucm):
        ucm.recorder.responses["getLdapSyncStatus"] = {"return": "sync completed"}
        result = ucm.get_ldap_sync_status(name="CorpAD")
        op, body = sent(ucm)
        assert op == "getLdapSyncStatus"
        assert text(body, "name") == "CorpAD"
        assert result == "sync completed"


class TestCCMVersion:
    def test_get_ccm_version_no_node(self, ucm):
        ucm.recorder.responses["getCCMVersion"] = {
            "return": {"componentVersion": {"version": "15.0.1.10000-10"}}
        }
        result = ucm.get_ccm_version()
        op, body = sent(ucm)
        assert op == "getCCMVersion"
        assert result == {"componentVersion": {"version": "15.0.1.10000-10"}}

    def test_get_ccm_version_with_node(self, ucm):
        ucm.recorder.responses["getCCMVersion"] = {"return": {}}
        ucm.get_ccm_version(process_node_name="cucm-pub.corp.com")
        op, body = sent(ucm)
        assert op == "getCCMVersion"
        assert text(body, "processNodeName") == "cucm-pub.corp.com"


class TestRegistrationDynamic:
    def test_get_registration_dynamic_by_device(self, ucm):
        ucm.recorder.responses["getRegistrationDynamic"] = {
            "return": {"registrationDynamic": {"device": "SEP001122334455"}}
        }
        result = ucm.get_registration_dynamic(device="SEP001122334455")
        op, body = sent(ucm)
        assert op == "getRegistrationDynamic"
        assert text(body, "device") == "SEP001122334455"
        assert result == {"device": "SEP001122334455"}

    def test_get_registration_dynamic_requires_one_identifier(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_registration_dynamic()
        with pytest.raises(ValueError):
            ucm.get_registration_dynamic(device="SEP001122334455", uuid="{1234}")

    def test_get_registrations_dynamic(self, ucm):
        ucm.recorder.responses["listRegistrationDynamic"] = {
            "return": {"registrationDynamic": [{"device": "SEP001122334455"}]}
        }
        result = ucm.get_registrations_dynamic()
        op, body = sent(ucm)
        assert op == "listRegistrationDynamic"
        assert len(result) == 1

    def test_get_registrations_dynamic_empty(self, ucm):
        ucm.recorder.responses["listRegistrationDynamic"] = {"return": None}
        result = ucm.get_registrations_dynamic()
        assert result == []


class TestPhoneLifecycle:
    @pytest.mark.parametrize("method,expected_op", [
        ("apply_phone", "applyPhone"),
        ("reset_phone", "resetPhone"),
        ("restart_phone", "restartPhone"),
        ("lock_phone", "lockPhone"),
        ("wipe_phone", "wipePhone"),
    ])
    def test_phone_lifecycle_by_name(self, ucm, method, expected_op):
        getattr(ucm, method)(name="SEP001122334455")
        op, body = sent(ucm)
        assert op == expected_op
        assert text(body, "name") == "SEP001122334455"
        assert not has(body, "uuid")

    @pytest.mark.parametrize("method,expected_op", [
        ("apply_phone", "applyPhone"),
        ("reset_phone", "resetPhone"),
        ("restart_phone", "restartPhone"),
        ("lock_phone", "lockPhone"),
        ("wipe_phone", "wipePhone"),
    ])
    def test_phone_lifecycle_by_uuid(self, ucm, method, expected_op):
        getattr(ucm, method)(uuid="{AAAA-1111-2222-3333-444444444444}")
        op, body = sent(ucm)
        assert op == expected_op
        assert text(body, "uuid") == "{AAAA-1111-2222-3333-444444444444}"
        assert not has(body, "name")

    def test_phone_lifecycle_requires_name_or_uuid(self, ucm):
        for method in ("apply_phone", "reset_phone", "restart_phone", "lock_phone", "wipe_phone"):
            with pytest.raises(ValueError):
                getattr(ucm, method)()
            with pytest.raises(ValueError):
                getattr(ucm, method)(name="x", uuid="y")

    def test_existing_phone_methods_unaffected(self, ucm):
        """get/add/update/delete phone still work alongside lifecycle methods."""
        ucm.recorder.responses["getPhone"] = {
            "return": {"phone": {"name": "SEP001122334455"}}
        }
        result = ucm.get_phone(name="SEP001122334455")
        assert result == {"name": "SEP001122334455"}


class TestApplicationUserCapfProfile:
    def test_add_application_user_capf_profile(self, ucm):
        ucm.add_application_user_capf_profile(
            applicationUser="AppUser1",
            instanceId="1",
            certificateOperation="Install / Upgrade",
            authenticationMode="By Null String",
        )
        op, body = sent(ucm)
        assert op == "addApplicationUserCapfProfile"
        assert text(body, "applicationUserCapfProfile/applicationUser") == "AppUser1"

    def test_get_application_user_capf_profile(self, ucm):
        ucm.recorder.responses["getApplicationUserCapfProfile"] = {
            "return": {
                "applicationUserCapfProfile": {
                    "applicationUser": "AppUser1",
                    "instanceId": "1",
                }
            }
        }
        result = ucm.get_application_user_capf_profile(instanceId="1")
        op, body = sent(ucm)
        assert op == "getApplicationUserCapfProfile"
        assert text(body, "instanceId") == "1"
        assert result["applicationUser"] == "AppUser1"

    def test_get_application_user_capf_profiles(self, ucm):
        ucm.recorder.responses["listApplicationUserCapfProfile"] = {
            "return": {
                "applicationUserCapfProfile": [
                    {"applicationUser": "AppUser1", "instanceId": "1"}
                ]
            }
        }
        result = ucm.get_application_user_capf_profiles()
        op, _ = sent(ucm)
        assert op == "listApplicationUserCapfProfile"
        assert len(result) == 1

    def test_get_application_user_capf_profiles_empty(self, ucm):
        ucm.recorder.responses["listApplicationUserCapfProfile"] = {"return": None}
        assert ucm.get_application_user_capf_profiles() == []

    def test_update_application_user_capf_profile(self, ucm):
        ucm.update_application_user_capf_profile(
            instanceId="1", authenticationString="NewPass1"
        )
        op, body = sent(ucm)
        assert op == "updateApplicationUserCapfProfile"
        assert text(body, "instanceId") == "1"

    def test_delete_application_user_capf_profile(self, ucm):
        ucm.delete_application_user_capf_profile(instanceId="1")
        op, body = sent(ucm)
        assert op == "removeApplicationUserCapfProfile"
        assert text(body, "instanceId") == "1"


class TestEndUserCapfProfile:
    def test_add_end_user_capf_profile(self, ucm):
        ucm.add_end_user_capf_profile(
            endUserId="jsmith",
            instanceId="1",
            certificationOperation="Install / Upgrade",
            authenticationMode="By Null String",
        )
        op, body = sent(ucm)
        assert op == "addEndUserCapfProfile"
        assert text(body, "endUserCapfProfile/endUserId") == "jsmith"

    def test_get_end_user_capf_profile(self, ucm):
        ucm.recorder.responses["getEndUserCapfProfile"] = {
            "return": {
                "endUserCapfProfile": {"endUserId": "jsmith", "instanceId": "1"}
            }
        }
        result = ucm.get_end_user_capf_profile(instanceId="1")
        op, body = sent(ucm)
        assert op == "getEndUserCapfProfile"
        assert text(body, "instanceId") == "1"
        assert result["endUserId"] == "jsmith"

    def test_get_end_user_capf_profiles(self, ucm):
        ucm.recorder.responses["listEndUserCapfProfile"] = {
            "return": {
                "endUserCapfProfile": [{"endUserId": "jsmith", "instanceId": "1"}]
            }
        }
        result = ucm.get_end_user_capf_profiles()
        op, _ = sent(ucm)
        assert op == "listEndUserCapfProfile"
        assert len(result) == 1

    def test_get_end_user_capf_profiles_empty(self, ucm):
        ucm.recorder.responses["listEndUserCapfProfile"] = {"return": None}
        assert ucm.get_end_user_capf_profiles() == []

    def test_update_end_user_capf_profile(self, ucm):
        ucm.update_end_user_capf_profile(instanceId="1", authenticationString="NewPass1")
        op, body = sent(ucm)
        assert op == "updateEndUserCapfProfile"
        assert text(body, "instanceId") == "1"

    def test_delete_end_user_capf_profile(self, ucm):
        ucm.delete_end_user_capf_profile(instanceId="1")
        op, body = sent(ucm)
        assert op == "removeEndUserCapfProfile"
        assert text(body, "instanceId") == "1"


class TestSecureConfig:
    def test_get_secure_config(self, ucm):
        ucm.recorder.responses["getSecureConfig"] = {
            "return": {"secureConfig": {"name": "Cisco Callmanager", "value": "true"}}
        }
        result = ucm.get_secure_config(name="Cisco Callmanager")
        op, body = sent(ucm)
        assert op == "getSecureConfig"
        assert text(body, "name") == "Cisco Callmanager"
        assert result == {"name": "Cisco Callmanager", "value": "true"}

    def test_get_secure_config_by_uuid(self, ucm):
        ucm.recorder.responses["getSecureConfig"] = {
            "return": {"secureConfig": {"uuid": "{CCCC-3333}"}}
        }
        ucm.get_secure_config(uuid="{CCCC-3333}")
        op, body = sent(ucm)
        assert op == "getSecureConfig"
        assert text(body, "uuid") == "{CCCC-3333}"

    def test_update_secure_config(self, ucm):
        ucm.update_secure_config(name="Cisco Callmanager", value="false")
        op, body = sent(ucm)
        assert op == "updateSecureConfig"
        assert text(body, "name") == "Cisco Callmanager"


class TestSipRealm:
    def test_add_sip_realm(self, ucm):
        ucm.add_sip_realm(
            realm="sip.corp.com",
            userid="sipuser",
            digestCredentials="secret",
        )
        op, body = sent(ucm)
        assert op == "addSipRealm"
        assert text(body, "sipRealm/realm") == "sip.corp.com"

    def test_get_sip_realm(self, ucm):
        ucm.recorder.responses["getSipRealm"] = {
            "return": {"sipRealm": {"realm": "sip.corp.com", "userid": "sipuser"}}
        }
        result = ucm.get_sip_realm(realm="sip.corp.com")
        op, body = sent(ucm)
        assert op == "getSipRealm"
        assert text(body, "realm") == "sip.corp.com"
        assert result["realm"] == "sip.corp.com"

    def test_get_sip_realms(self, ucm):
        ucm.recorder.responses["listSipRealm"] = {
            "return": {"sipRealm": [{"realm": "sip.corp.com"}]}
        }
        result = ucm.get_sip_realms()
        op, _ = sent(ucm)
        assert op == "listSipRealm"
        assert result[0]["realm"] == "sip.corp.com"

    def test_get_sip_realms_empty(self, ucm):
        ucm.recorder.responses["listSipRealm"] = {"return": None}
        assert ucm.get_sip_realms() == []

    def test_update_sip_realm(self, ucm):
        ucm.update_sip_realm(realm="sip.corp.com", userid="sipuser", digestCredentials="newpass")
        op, body = sent(ucm)
        assert op == "updateSipRealm"

    def test_delete_sip_realm(self, ucm):
        ucm.delete_sip_realm(realm="sip.corp.com")
        op, body = sent(ucm)
        assert op == "removeSipRealm"
        assert text(body, "realm") == "sip.corp.com"


class TestTvsCertificate:
    def test_get_tvs_certificate_by_uuid(self, ucm):
        ucm.recorder.responses["getTvsCertificate"] = {
            "return": {
                "tvsCertificate": {
                    "uuid": "{DDDD-4444}",
                    "subjectName": "CN=cucm-pub",
                    "issuerName": "CN=CUCM-CA",
                    "serialNumber": "1A2B3C",
                }
            }
        }
        result = ucm.get_tvs_certificate(uuid="{DDDD-4444}")
        op, body = sent(ucm)
        assert op == "getTvsCertificate"
        assert text(body, "uuid") == "{DDDD-4444}"
        assert result["subjectName"] == "CN=cucm-pub"

    def test_get_tvs_certificates(self, ucm):
        ucm.recorder.responses["listTvsCertificate"] = {
            "return": {"tvsCertificate": [{"subjectName": "CN=cucm-pub"}]}
        }
        result = ucm.get_tvs_certificates()
        op, _ = sent(ucm)
        assert op == "listTvsCertificate"
        assert len(result) == 1

    def test_get_tvs_certificates_empty(self, ucm):
        ucm.recorder.responses["listTvsCertificate"] = {"return": None}
        assert ucm.get_tvs_certificates() == []

    def test_update_tvs_certificate(self, ucm):
        ucm.update_tvs_certificate(uuid="{DDDD-4444}", timeToLive=365)
        op, body = sent(ucm)
        assert op == "updateTvsCertificate"
        assert text(body, "uuid") == "{DDDD-4444}"


class TestVpnGateway:
    def test_add_vpn_gateway(self, ucm):
        ucm.add_vpn_gateway(
            name="VPN-GW1",
            url="https://vpn.corp.com",
            certificates={
                "certificate": [{"issuerName": "CN=CUCM-CA", "serialNumber": "1A2B3C"}]
            },
        )
        op, body = sent(ucm)
        assert op == "addVpnGateway"
        assert text(body, "vpnGateway/name") == "VPN-GW1"

    def test_get_vpn_gateway(self, ucm):
        ucm.recorder.responses["getVpnGateway"] = {
            "return": {"vpnGateway": {"name": "VPN-GW1", "url": "https://vpn.corp.com"}}
        }
        result = ucm.get_vpn_gateway(name="VPN-GW1")
        op, body = sent(ucm)
        assert op == "getVpnGateway"
        assert text(body, "name") == "VPN-GW1"
        assert result["name"] == "VPN-GW1"

    def test_get_vpn_gateways(self, ucm):
        ucm.recorder.responses["listVpnGateway"] = {
            "return": {"vpnGateway": [{"name": "VPN-GW1"}]}
        }
        result = ucm.get_vpn_gateways()
        op, _ = sent(ucm)
        assert op == "listVpnGateway"
        assert result[0]["name"] == "VPN-GW1"

    def test_get_vpn_gateways_empty(self, ucm):
        ucm.recorder.responses["listVpnGateway"] = {"return": None}
        assert ucm.get_vpn_gateways() == []

    def test_update_vpn_gateway(self, ucm):
        ucm.update_vpn_gateway(name="VPN-GW1", description="Updated")
        op, body = sent(ucm)
        assert op == "updateVpnGateway"
        assert text(body, "name") == "VPN-GW1"

    def test_delete_vpn_gateway(self, ucm):
        ucm.delete_vpn_gateway(name="VPN-GW1")
        op, body = sent(ucm)
        assert op == "removeVpnGateway"
        assert text(body, "name") == "VPN-GW1"

    def test_delete_vpn_gateway_by_uuid(self, ucm):
        ucm.delete_vpn_gateway(uuid="{EEEE-5555}")
        op, body = sent(ucm)
        assert op == "removeVpnGateway"
        assert text(body, "uuid") == "{EEEE-5555}"
        assert not has(body, "name")


class TestVpnGroup:
    def test_add_vpn_group(self, ucm):
        ucm.add_vpn_group(name="VPN-GRP1")
        op, body = sent(ucm)
        assert op == "addVpnGroup"
        assert text(body, "vpnGroup/name") == "VPN-GRP1"

    def test_get_vpn_group(self, ucm):
        ucm.recorder.responses["getVpnGroup"] = {
            "return": {"vpnGroup": {"name": "VPN-GRP1"}}
        }
        result = ucm.get_vpn_group(name="VPN-GRP1")
        op, body = sent(ucm)
        assert op == "getVpnGroup"
        assert text(body, "name") == "VPN-GRP1"
        assert result == {"name": "VPN-GRP1"}

    def test_get_vpn_groups(self, ucm):
        ucm.recorder.responses["listVpnGroup"] = {
            "return": {"vpnGroup": [{"name": "VPN-GRP1"}, {"name": "VPN-GRP2"}]}
        }
        result = ucm.get_vpn_groups()
        op, _ = sent(ucm)
        assert op == "listVpnGroup"
        assert len(result) == 2

    def test_get_vpn_groups_empty(self, ucm):
        ucm.recorder.responses["listVpnGroup"] = {"return": None}
        assert ucm.get_vpn_groups() == []

    def test_update_vpn_group(self, ucm):
        ucm.update_vpn_group(name="VPN-GRP1", description="Updated")
        op, body = sent(ucm)
        assert op == "updateVpnGroup"
        assert text(body, "name") == "VPN-GRP1"

    def test_delete_vpn_group(self, ucm):
        ucm.delete_vpn_group(name="VPN-GRP1")
        op, body = sent(ucm)
        assert op == "removeVpnGroup"
        assert text(body, "name") == "VPN-GRP1"

    def test_delete_vpn_group_by_uuid(self, ucm):
        ucm.delete_vpn_group(uuid="{FFFF-6666}")
        op, body = sent(ucm)
        assert op == "removeVpnGroup"
        assert text(body, "uuid") == "{FFFF-6666}"
        assert not has(body, "name")


class TestVpnProfile:
    def test_add_vpn_profile(self, ucm):
        ucm.add_vpn_profile(name="VPN-PROF1")
        op, body = sent(ucm)
        assert op == "addVpnProfile"
        assert text(body, "vpnProfile/name") == "VPN-PROF1"

    def test_get_vpn_profile(self, ucm):
        ucm.recorder.responses["getVpnProfile"] = {
            "return": {"vpnProfile": {"name": "VPN-PROF1"}}
        }
        result = ucm.get_vpn_profile(name="VPN-PROF1")
        op, body = sent(ucm)
        assert op == "getVpnProfile"
        assert text(body, "name") == "VPN-PROF1"
        assert result == {"name": "VPN-PROF1"}

    def test_get_vpn_profiles(self, ucm):
        ucm.recorder.responses["listVpnProfile"] = {
            "return": {
                "vpnProfile": [
                    {"name": "VPN-PROF1"},
                    {"name": "VPN-PROF2"},
                    {"name": "VPN-PROF3"},
                ]
            }
        }
        result = ucm.get_vpn_profiles()
        op, _ = sent(ucm)
        assert op == "listVpnProfile"
        assert len(result) == 3

    def test_get_vpn_profiles_empty(self, ucm):
        ucm.recorder.responses["listVpnProfile"] = {"return": None}
        assert ucm.get_vpn_profiles() == []

    def test_update_vpn_profile(self, ucm):
        ucm.update_vpn_profile(name="VPN-PROF1", description="Updated")
        op, body = sent(ucm)
        assert op == "updateVpnProfile"
        assert text(body, "name") == "VPN-PROF1"

    def test_delete_vpn_profile(self, ucm):
        ucm.delete_vpn_profile(name="VPN-PROF1")
        op, body = sent(ucm)
        assert op == "removeVpnProfile"
        assert text(body, "name") == "VPN-PROF1"

    def test_delete_vpn_profile_by_uuid(self, ucm):
        ucm.delete_vpn_profile(uuid="{GGGG-7777}")
        op, body = sent(ucm)
        assert op == "removeVpnProfile"
        assert text(body, "uuid") == "{GGGG-7777}"
        assert not has(body, "name")
