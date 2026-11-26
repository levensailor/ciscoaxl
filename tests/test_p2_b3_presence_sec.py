"""Offline tests for P2 Batch B3 — p2_presence_sec.py

Verifies every method in P2PresenceSec:
  * calls the correct AXL operation
  * passes the right element names and values
  * returns the unwrapped result
  * handles empty list responses gracefully

Run with: pytest tests/test_p2_b3_presence_sec.py
"""
import pytest

# Re-use the shared offline test infrastructure
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from test_offline_requests import make_ucm, sent, text, has


# ---------------------------------------------------------------------------
# Shared fixture
# ---------------------------------------------------------------------------
@pytest.fixture
def ucm():
    return make_ucm("15.0")


# ---------------------------------------------------------------------------
# AssignedPresenceServers — list only
# ---------------------------------------------------------------------------
class TestAssignedPresenceServers:
    def test_get_assigned_presence_servers_returns_list(self, ucm):
        ucm.recorder.responses["listAssignedPresenceServers"] = {
            "return": {"assignedPresenceServers": [{"name": "imp-pub"}, {"name": "imp-sub"}]}
        }
        result = ucm.get_assigned_presence_servers()
        op, body = sent(ucm)
        assert op == "listAssignedPresenceServers"
        assert len(result) == 2
        assert result[0]["name"] == "imp-pub"

    def test_get_assigned_presence_servers_empty(self, ucm):
        ucm.recorder.responses["listAssignedPresenceServers"] = {"return": None}
        assert ucm.get_assigned_presence_servers() == []


# ---------------------------------------------------------------------------
# UnassignedPresenceServers — list only
# ---------------------------------------------------------------------------
class TestUnassignedPresenceServers:
    def test_get_unassigned_presence_servers_returns_list(self, ucm):
        ucm.recorder.responses["listUnassignedPresenceServers"] = {
            "return": {"unassignedPresenceServers": [{"name": "imp-new"}]}
        }
        result = ucm.get_unassigned_presence_servers()
        op, body = sent(ucm)
        assert op == "listUnassignedPresenceServers"
        assert len(result) == 1

    def test_get_unassigned_presence_servers_empty(self, ucm):
        ucm.recorder.responses["listUnassignedPresenceServers"] = {"return": None}
        assert ucm.get_unassigned_presence_servers() == []


# ---------------------------------------------------------------------------
# AssignedPresenceUsers — list only
# ---------------------------------------------------------------------------
class TestAssignedPresenceUsers:
    def test_get_assigned_presence_users_returns_list(self, ucm):
        ucm.recorder.responses["listAssignedPresenceUsers"] = {
            "return": {
                "assignedPresenceUsers": [
                    {"userid": "jsmith", "server": "imp-pub"},
                    {"userid": "jdoe", "server": "imp-pub"},
                ]
            }
        }
        result = ucm.get_assigned_presence_users()
        op, body = sent(ucm)
        assert op == "listAssignedPresenceUsers"
        assert len(result) == 2

    def test_get_assigned_presence_users_empty(self, ucm):
        ucm.recorder.responses["listAssignedPresenceUsers"] = {"return": None}
        assert ucm.get_assigned_presence_users() == []


# ---------------------------------------------------------------------------
# UnassignedPresenceUsers — list only
# ---------------------------------------------------------------------------
class TestUnassignedPresenceUsers:
    def test_get_unassigned_presence_users_returns_list(self, ucm):
        ucm.recorder.responses["listUnassignedPresenceUsers"] = {
            "return": {"unassignedPresenceUsers": [{"userid": "jsmith"}]}
        }
        result = ucm.get_unassigned_presence_users()
        op, body = sent(ucm)
        assert op == "listUnassignedPresenceUsers"
        assert len(result) == 1

    def test_get_unassigned_presence_users_empty(self, ucm):
        ucm.recorder.responses["listUnassignedPresenceUsers"] = {"return": None}
        assert ucm.get_unassigned_presence_users() == []


# ---------------------------------------------------------------------------
# PresenceUser — assign / unassign only
# ---------------------------------------------------------------------------
class TestPresenceUser:
    def test_assign_presence_user(self, ucm):
        ucm.assign_presence_user(userid="jsmith", server="imp-pub")
        op, body = sent(ucm)
        assert op == "assignPresenceUser"
        assert text(body, "userid") == "jsmith"
        assert text(body, "server") == "imp-pub"

    def test_unassign_presence_user(self, ucm):
        ucm.unassign_presence_user(userid="jsmith")
        op, body = sent(ucm)
        assert op == "unassignPresenceUser"
        assert text(body, "userid") == "jsmith"


# ---------------------------------------------------------------------------
# PresenceRedundancyGroup
# ---------------------------------------------------------------------------
class TestPresenceRedundancyGroup:
    def test_add_presence_redundancy_group(self, ucm):
        ucm.add_presence_redundancy_group(name="PRG1", server1="imp-pub", server2="imp-sub")
        op, body = sent(ucm)
        assert op == "addPresenceRedundancyGroup"
        assert text(body, "presenceRedundancyGroup/name") == "PRG1"

    def test_get_presence_redundancy_group(self, ucm):
        ucm.recorder.responses["getPresenceRedundancyGroup"] = {
            "return": {"presenceRedundancyGroup": {"name": "PRG1"}}
        }
        result = ucm.get_presence_redundancy_group(name="PRG1")
        op, body = sent(ucm)
        assert op == "getPresenceRedundancyGroup"
        assert text(body, "name") == "PRG1"
        assert result == {"name": "PRG1"}

    def test_get_presence_redundancy_groups(self, ucm):
        ucm.recorder.responses["listPresenceRedundancyGroup"] = {
            "return": {"presenceRedundancyGroup": [{"name": "PRG1"}]}
        }
        result = ucm.get_presence_redundancy_groups()
        op, _ = sent(ucm)
        assert op == "listPresenceRedundancyGroup"
        assert result[0]["name"] == "PRG1"

    def test_get_presence_redundancy_groups_empty(self, ucm):
        ucm.recorder.responses["listPresenceRedundancyGroup"] = {"return": None}
        assert ucm.get_presence_redundancy_groups() == []

    def test_update_presence_redundancy_group(self, ucm):
        ucm.update_presence_redundancy_group(name="PRG1", description="Updated")
        op, body = sent(ucm)
        assert op == "updatePresenceRedundancyGroup"
        assert text(body, "name") == "PRG1"

    def test_delete_presence_redundancy_group(self, ucm):
        ucm.delete_presence_redundancy_group(name="PRG1")
        op, body = sent(ucm)
        assert op == "removePresenceRedundancyGroup"
        assert text(body, "name") == "PRG1"

    def test_delete_presence_redundancy_group_by_uuid(self, ucm):
        ucm.delete_presence_redundancy_group(uuid="{AAAA-1111}")
        op, body = sent(ucm)
        assert op == "removePresenceRedundancyGroup"
        assert text(body, "uuid") == "{AAAA-1111}"
        assert not has(body, "name")


# ---------------------------------------------------------------------------
# ExpresswayCConfiguration
# ---------------------------------------------------------------------------
class TestExpresswayCConfiguration:
    def test_add_expressway_c_configuration(self, ucm):
        ucm.add_expressway_c_configuration(HostNameOrIP="exp-c.corp.com")
        op, body = sent(ucm)
        assert op == "addExpresswayCConfiguration"
        assert text(body, "expresswayCConfiguration/HostNameOrIP") == "exp-c.corp.com"

    def test_get_expressway_c_configuration(self, ucm):
        ucm.recorder.responses["getExpresswayCConfiguration"] = {
            "return": {"expresswayCConfiguration": {"HostNameOrIP": "exp-c.corp.com"}}
        }
        result = ucm.get_expressway_c_configuration(HostNameOrIP="exp-c.corp.com")
        op, body = sent(ucm)
        assert op == "getExpresswayCConfiguration"
        assert result == {"HostNameOrIP": "exp-c.corp.com"}

    def test_get_expressway_c_configurations(self, ucm):
        ucm.recorder.responses["listExpresswayCConfiguration"] = {
            "return": {"expresswayCConfiguration": [{"HostNameOrIP": "exp-c.corp.com"}]}
        }
        result = ucm.get_expressway_c_configurations()
        op, _ = sent(ucm)
        assert op == "listExpresswayCConfiguration"
        assert len(result) == 1

    def test_get_expressway_c_configurations_empty(self, ucm):
        ucm.recorder.responses["listExpresswayCConfiguration"] = {"return": None}
        assert ucm.get_expressway_c_configurations() == []

    def test_update_expressway_c_configuration(self, ucm):
        ucm.update_expressway_c_configuration(HostNameOrIP="exp-c.corp.com", description="Updated")
        op, body = sent(ucm)
        assert op == "updateExpresswayCConfiguration"

    def test_delete_expressway_c_configuration(self, ucm):
        ucm.delete_expressway_c_configuration(HostNameOrIP="exp-c.corp.com")
        op, body = sent(ucm)
        assert op == "removeExpresswayCConfiguration"


# ---------------------------------------------------------------------------
# MraServiceDomain
# ---------------------------------------------------------------------------
class TestMraServiceDomain:
    def test_add_mra_service_domain(self, ucm):
        ucm.add_mra_service_domain(name="corp.com", serviceDomains="corp.com")
        op, body = sent(ucm)
        assert op == "addMraServiceDomain"
        assert text(body, "mraServiceDomain/name") == "corp.com"

    def test_get_mra_service_domain(self, ucm):
        ucm.recorder.responses["getMraServiceDomain"] = {
            "return": {"mraServiceDomain": {"name": "corp.com"}}
        }
        result = ucm.get_mra_service_domain(name="corp.com")
        op, body = sent(ucm)
        assert op == "getMraServiceDomain"
        assert text(body, "name") == "corp.com"
        assert result == {"name": "corp.com"}

    def test_get_mra_service_domains(self, ucm):
        ucm.recorder.responses["listMraServiceDomain"] = {
            "return": {"mraServiceDomain": [{"name": "corp.com"}]}
        }
        result = ucm.get_mra_service_domains()
        op, _ = sent(ucm)
        assert op == "listMraServiceDomain"
        assert result[0]["name"] == "corp.com"

    def test_get_mra_service_domains_empty(self, ucm):
        ucm.recorder.responses["listMraServiceDomain"] = {"return": None}
        assert ucm.get_mra_service_domains() == []

    def test_update_mra_service_domain(self, ucm):
        ucm.update_mra_service_domain(name="corp.com", isDefault=True)
        op, body = sent(ucm)
        assert op == "updateMraServiceDomain"
        assert text(body, "name") == "corp.com"

    def test_delete_mra_service_domain(self, ucm):
        ucm.delete_mra_service_domain(name="corp.com")
        op, body = sent(ucm)
        assert op == "removeMraServiceDomain"
        assert text(body, "name") == "corp.com"

    def test_delete_mra_service_domain_by_uuid(self, ucm):
        ucm.delete_mra_service_domain(uuid="{BBBB-2222}")
        op, body = sent(ucm)
        assert op == "removeMraServiceDomain"
        assert text(body, "uuid") == "{BBBB-2222}"


# ---------------------------------------------------------------------------
# ApplicationUserCapfProfile
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# EndUserCapfProfile
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# SecureConfig — get / update only
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# SipRealm
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# TvsCertificate — get / update / list (no add / delete)
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# VpnGateway
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# VpnGroup
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# VpnProfile
# ---------------------------------------------------------------------------
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
