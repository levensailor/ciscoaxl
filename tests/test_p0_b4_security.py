"""Offline tests for P0 Batch B4 — p0_security.py

Verifies that every method in P0Security:
  * calls the correct AXL operation
  * passes the right element names and values
  * handles name/uuid routing via _identify
  * returns the unwrapped result

Run with: pytest tests/test_p0_b4_security.py
"""
from pathlib import Path

import pytest
from zeep import Client, Settings
from zeep.exceptions import Fault

from ciscoaxl import axl
from ciscoaxl.aliases import AliasingService

SCHEMA_DIR = Path(__file__).resolve().parent.parent / "ciscoaxl" / "schema"
BINDING = "{http://www.cisco.com/AXLAPIService/}AXLAPIBinding"
_clients = {}


# ---------------------------------------------------------------------------
# Shared test infrastructure (mirrors test_offline_requests.py)
# ---------------------------------------------------------------------------

class AutoDict(dict):
    """Canned response: any missing key returns another AutoDict."""

    def __missing__(self, key):
        value = AutoDict()
        self[key] = value
        return value


class Recorder:
    """Stands in for the zeep service: serialises each call, returns canned response."""

    def __init__(self, zeep_client, service):
        self._zeep = zeep_client
        self._real = service
        self._binding = service._binding
        self.calls = []
        self.responses = {}

    def __getattr__(self, op_name):
        def call(*args, **kwargs):
            message = self._zeep.create_message(self._real, op_name, *args, **kwargs)
            body = message.find("{http://schemas.xmlsoap.org/soap/envelope/}Body")[0]
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
    return make_ucm("15.0")


# ---------------------------------------------------------------------------
# PhoneSecurityProfile
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# SipProfile  (get_sip_profile stays in axl.py — only new ops here)
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# SipTrunkSecurityProfile
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# DateTimeGroup
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# LdapDirectory
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# LdapSyncStatus
# ---------------------------------------------------------------------------

class TestLdapSyncStatus:
    def test_get_ldap_sync_status(self, ucm):
        ucm.recorder.responses["getLdapSyncStatus"] = {"return": "sync completed"}
        result = ucm.get_ldap_sync_status(name="CorpAD")
        op, body = sent(ucm)
        assert op == "getLdapSyncStatus"
        assert text(body, "name") == "CorpAD"
        assert result == "sync completed"


# ---------------------------------------------------------------------------
# CCMVersion
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# RegistrationDynamic
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Phone lifecycle
# ---------------------------------------------------------------------------

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
