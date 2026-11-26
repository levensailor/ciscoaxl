"""Offline tests for P3 Batch B3 — p3_network.py

Verifies that every method in P3Network:
  * calls the correct AXL operation
  * passes the right element names and values
  * handles identifier routing (uuid / name / processNodeName / communityName …)
  * returns the unwrapped result or [] on empty

Run with: pytest tests/test_p3_b3_network.py
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
# LbmGroup
# ---------------------------------------------------------------------------

class TestLbmGroup:
    def test_add_lbm_group(self, ucm):
        ucm.add_lbm_group(
            name="LBM-Group-1",
            ProcessnodeActive="pub.corp.com",
        )
        op, body = sent(ucm)
        assert op == "addLbmGroup"
        assert text(body, "lbmGroup/name") == "LBM-Group-1"
        assert text(body, "lbmGroup/ProcessnodeActive") == "pub.corp.com"

    def test_get_lbm_group_by_name(self, ucm):
        ucm.recorder.responses["getLbmGroup"] = {
            "return": {"lbmGroup": {"name": "LBM-Group-1"}}
        }
        result = ucm.get_lbm_group(name="LBM-Group-1")
        op, body = sent(ucm)
        assert op == "getLbmGroup"
        assert text(body, "name") == "LBM-Group-1"
        assert result == {"name": "LBM-Group-1"}

    def test_get_lbm_group_by_uuid(self, ucm):
        ucm.recorder.responses["getLbmGroup"] = {
            "return": {"lbmGroup": {"name": "LBM-Group-1"}}
        }
        ucm.get_lbm_group(uuid="{AAAA-1111}")
        op, body = sent(ucm)
        assert op == "getLbmGroup"
        assert text(body, "uuid") == "{AAAA-1111}"

    def test_get_lbm_group_requires_identifier(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_lbm_group()

    def test_get_lbm_groups(self, ucm):
        ucm.recorder.responses["listLbmGroup"] = {
            "return": {"lbmGroup": [{"name": "LBM-Group-1"}]}
        }
        result = ucm.get_lbm_groups()
        op, body = sent(ucm)
        assert op == "listLbmGroup"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_lbm_groups_empty(self, ucm):
        ucm.recorder.responses["listLbmGroup"] = {"return": None}
        result = ucm.get_lbm_groups()
        assert result == []

    def test_update_lbm_group(self, ucm):
        ucm.update_lbm_group(name="LBM-Group-1", newName="LBM-Group-1-Renamed")
        op, body = sent(ucm)
        assert op == "updateLbmGroup"
        assert text(body, "name") == "LBM-Group-1"
        assert text(body, "newName") == "LBM-Group-1-Renamed"

    def test_remove_lbm_group_by_name(self, ucm):
        ucm.remove_lbm_group(name="LBM-Group-1")
        op, body = sent(ucm)
        assert op == "removeLbmGroup"
        assert text(body, "name") == "LBM-Group-1"

    def test_remove_lbm_group_by_uuid(self, ucm):
        ucm.remove_lbm_group(uuid="{AAAA-1111}")
        op, body = sent(ucm)
        assert op == "removeLbmGroup"
        assert text(body, "uuid") == "{AAAA-1111}"

    def test_remove_lbm_group_requires_identifier(self, ucm):
        with pytest.raises(ValueError):
            ucm.remove_lbm_group()


# ---------------------------------------------------------------------------
# LbmHubGroup
# ---------------------------------------------------------------------------

class TestLbmHubGroup:
    def test_add_lbm_hub_group(self, ucm):
        ucm.add_lbm_hub_group(
            name="LBM-Hub-1",
            member1="pub.corp.com",
        )
        op, body = sent(ucm)
        assert op == "addLbmHubGroup"
        assert text(body, "lbmHubGroup/name") == "LBM-Hub-1"
        assert text(body, "lbmHubGroup/member1") == "pub.corp.com"

    def test_get_lbm_hub_group_by_name(self, ucm):
        ucm.recorder.responses["getLbmHubGroup"] = {
            "return": {"lbmHubGroup": {"name": "LBM-Hub-1"}}
        }
        result = ucm.get_lbm_hub_group(name="LBM-Hub-1")
        op, body = sent(ucm)
        assert op == "getLbmHubGroup"
        assert text(body, "name") == "LBM-Hub-1"
        assert result == {"name": "LBM-Hub-1"}

    def test_get_lbm_hub_group_by_uuid(self, ucm):
        ucm.recorder.responses["getLbmHubGroup"] = {
            "return": {"lbmHubGroup": {"name": "LBM-Hub-1"}}
        }
        ucm.get_lbm_hub_group(uuid="{BBBB-2222}")
        op, body = sent(ucm)
        assert op == "getLbmHubGroup"
        assert text(body, "uuid") == "{BBBB-2222}"

    def test_get_lbm_hub_group_requires_identifier(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_lbm_hub_group()

    def test_get_lbm_hub_groups(self, ucm):
        ucm.recorder.responses["listLbmHubGroup"] = {
            "return": {"lbmHubGroup": [{"name": "LBM-Hub-1"}]}
        }
        result = ucm.get_lbm_hub_groups()
        op, body = sent(ucm)
        assert op == "listLbmHubGroup"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_lbm_hub_groups_empty(self, ucm):
        ucm.recorder.responses["listLbmHubGroup"] = {"return": None}
        result = ucm.get_lbm_hub_groups()
        assert result == []

    def test_update_lbm_hub_group(self, ucm):
        ucm.update_lbm_hub_group(name="LBM-Hub-1", newName="LBM-Hub-1-Renamed")
        op, body = sent(ucm)
        assert op == "updateLbmHubGroup"
        assert text(body, "name") == "LBM-Hub-1"

    def test_remove_lbm_hub_group_by_name(self, ucm):
        ucm.remove_lbm_hub_group(name="LBM-Hub-1")
        op, body = sent(ucm)
        assert op == "removeLbmHubGroup"
        assert text(body, "name") == "LBM-Hub-1"

    def test_remove_lbm_hub_group_by_uuid(self, ucm):
        ucm.remove_lbm_hub_group(uuid="{BBBB-2222}")
        op, body = sent(ucm)
        assert op == "removeLbmHubGroup"
        assert text(body, "uuid") == "{BBBB-2222}"

    def test_remove_lbm_hub_group_requires_identifier(self, ucm):
        with pytest.raises(ValueError):
            ucm.remove_lbm_hub_group()


# ---------------------------------------------------------------------------
# SNMPCommunityString
# ---------------------------------------------------------------------------

class TestSNMPCommunityString:
    def test_add_snmp_community_string(self, ucm):
        # AXL RArrayOfHosts uses 'item' elements (xsd:string[]) not 'host'
        ucm.add_snmp_community_string(
            communityName="public",
            accessPrivilege="ReadOnly",
            ArrayOfHosts={"item": []},
        )
        op, body = sent(ucm)
        assert op == "addSNMPCommunityString"
        assert text(body, "CommunityString/communityName") == "public"
        assert text(body, "CommunityString/accessPrivilege") == "ReadOnly"

    def test_get_snmp_community_string(self, ucm):
        ucm.recorder.responses["getSNMPCommunityString"] = {
            "return": {"SNMPCommunityString": {"communityName": "public"}}
        }
        result = ucm.get_snmp_community_string(communityName="public")
        op, body = sent(ucm)
        assert op == "getSNMPCommunityString"
        assert text(body, "communityName") == "public"
        assert result == {"communityName": "public"}

    def test_update_snmp_community_string(self, ucm):
        # AXL UpdateSNMPCommunityStringReq requires newValues.ArrayOfHosts
        # communityName is the positional identifier; newValues fields go in kwargs
        ucm.update_snmp_community_string(
            "public",
            accessPrivilege="ReadWrite",
            ArrayOfHosts={"item": []},
        )
        op, body = sent(ucm)
        assert op == "updateSNMPCommunityString"
        assert text(body, "communityName") == "public"

    def test_remove_snmp_community_string(self, ucm):
        ucm.remove_snmp_community_string(communityName="public")
        op, body = sent(ucm)
        assert op == "removeSNMPCommunityString"
        assert text(body, "CommunityString") == "public"


# ---------------------------------------------------------------------------
# SNMPMIB2List
# ---------------------------------------------------------------------------

class TestSNMPMIB2List:
    def test_get_snmp_mib2_list(self, ucm):
        ucm.recorder.responses["getSNMPMIB2List"] = {
            "return": {"SNMPMIB2List": {"sysContact": "admin@corp.com"}}
        }
        result = ucm.get_snmp_mib2_list(sysContact="admin@corp.com")
        op, body = sent(ucm)
        assert op == "getSNMPMIB2List"
        assert text(body, "sysContact") == "admin@corp.com"
        assert result == {"sysContact": "admin@corp.com"}

    def test_update_snmp_mib2_list(self, ucm):
        ucm.update_snmp_mib2_list(
            sysLocation="Data Center",
            sysContact="admin@corp.com",
        )
        op, body = sent(ucm)
        assert op == "updateSNMPMIB2List"
        assert text(body, "sysLocation") == "Data Center"
        assert text(body, "sysContact") == "admin@corp.com"


# ---------------------------------------------------------------------------
# SNMPUser
# ---------------------------------------------------------------------------

class TestSNMPUser:
    def test_add_snmp_user(self, ucm):
        # AXL RArrayOfHosts uses 'item' elements (xsd:string[]) not 'host'
        ucm.add_snmp_user(
            userName="snmpadmin",
            authRequired="true",
            authPassword="authpassword",
            authProtocol="MD5",
            privacyRequired="true",
            privacyPassword="privpassword",
            privacyProtocol="DES",
            accessPrivilege="ReadOnly",
            ArrayOfHosts={"item": []},
        )
        op, body = sent(ucm)
        assert op == "addSNMPUser"
        assert text(body, "user/userName") == "snmpadmin"
        assert text(body, "user/authProtocol") == "MD5"

    def test_get_snmp_user(self, ucm):
        ucm.recorder.responses["getSNMPUser"] = {
            "return": {"SNMPUser": {"userName": "snmpadmin"}}
        }
        result = ucm.get_snmp_user(userName="snmpadmin")
        op, body = sent(ucm)
        assert op == "getSNMPUser"
        assert text(body, "userName") == "snmpadmin"
        assert result == {"userName": "snmpadmin"}

    def test_update_snmp_user(self, ucm):
        # AXL RArrayOfHosts uses 'item' elements (xsd:string[]) not 'host'
        ucm.update_snmp_user(
            userName="snmpadmin",
            authPassword="newpassword",
            authRequired="true",
            authProtocol="MD5",
            privacyRequired="false",
            privacyPassword="",
            privacyProtocol="DES",
            accessPrivilege="ReadOnly",
            ArrayOfHosts={"item": []},
        )
        op, body = sent(ucm)
        assert op == "updateSNMPUser"
        assert text(body, "user/userName") == "snmpadmin"

    def test_remove_snmp_user(self, ucm):
        ucm.remove_snmp_user(userName="snmpadmin")
        op, body = sent(ucm)
        assert op == "removeSNMPUser"
        assert text(body, "User") == "snmpadmin"


# ---------------------------------------------------------------------------
# DhcpServer
# ---------------------------------------------------------------------------

class TestDhcpServer:
    def test_add_dhcp_server(self, ucm):
        ucm.add_dhcp_server(
            processNodeName="pub.corp.com",
            arpCacheTimeout=0,
            ipAddressLeaseTime=86400,
            renewalTime=43200,
        )
        op, body = sent(ucm)
        assert op == "addDhcpServer"
        assert text(body, "dhcpServer/processNodeName") == "pub.corp.com"

    def test_get_dhcp_server_by_uuid(self, ucm):
        ucm.recorder.responses["getDhcpServer"] = {
            "return": {"dhcpServer": {"processNodeName": "pub.corp.com"}}
        }
        result = ucm.get_dhcp_server(uuid="{CCCC-3333}")
        op, body = sent(ucm)
        assert op == "getDhcpServer"
        assert text(body, "uuid") == "{CCCC-3333}"
        assert result == {"processNodeName": "pub.corp.com"}

    def test_get_dhcp_server_by_process_node(self, ucm):
        ucm.recorder.responses["getDhcpServer"] = {
            "return": {"dhcpServer": {"processNodeName": "pub.corp.com"}}
        }
        ucm.get_dhcp_server(processNodeName="pub.corp.com")
        op, body = sent(ucm)
        assert op == "getDhcpServer"
        assert text(body, "processNodeName") == "pub.corp.com"

    def test_get_dhcp_server_requires_identifier(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_dhcp_server()

    def test_get_dhcp_servers(self, ucm):
        ucm.recorder.responses["listDhcpServer"] = {
            "return": {"dhcpServer": [{"processNodeName": "pub.corp.com"}]}
        }
        result = ucm.get_dhcp_servers()
        op, body = sent(ucm)
        assert op == "listDhcpServer"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_dhcp_servers_empty(self, ucm):
        ucm.recorder.responses["listDhcpServer"] = {"return": None}
        result = ucm.get_dhcp_servers()
        assert result == []

    def test_update_dhcp_server(self, ucm):
        ucm.update_dhcp_server(uuid="{CCCC-3333}", ipAddressLeaseTime=172800)
        op, body = sent(ucm)
        assert op == "updateDhcpServer"
        assert text(body, "uuid") == "{CCCC-3333}"

    def test_remove_dhcp_server_by_uuid(self, ucm):
        ucm.remove_dhcp_server(uuid="{CCCC-3333}")
        op, body = sent(ucm)
        assert op == "removeDhcpServer"
        assert text(body, "uuid") == "{CCCC-3333}"

    def test_remove_dhcp_server_by_process_node(self, ucm):
        ucm.remove_dhcp_server(processNodeName="pub.corp.com")
        op, body = sent(ucm)
        assert op == "removeDhcpServer"
        assert text(body, "processNodeName") == "pub.corp.com"

    def test_remove_dhcp_server_requires_identifier(self, ucm):
        with pytest.raises(ValueError):
            ucm.remove_dhcp_server()


# ---------------------------------------------------------------------------
# DhcpSubnet
# ---------------------------------------------------------------------------

class TestDhcpSubnet:
    def test_add_dhcp_subnet(self, ucm):
        ucm.add_dhcp_subnet(
            dhcpServerName="pub.corp.com",
            subnetIpAddress="10.0.0.0",
            primaryStartIpAddress="10.0.0.100",
            primaryEndIpAddress="10.0.0.200",
            subnetMask="255.255.255.0",
        )
        op, body = sent(ucm)
        assert op == "addDhcpSubnet"
        assert text(body, "dhcpSubnet/dhcpServerName") == "pub.corp.com"
        assert text(body, "dhcpSubnet/subnetIpAddress") == "10.0.0.0"

    def test_get_dhcp_subnet_by_uuid(self, ucm):
        ucm.recorder.responses["getDhcpSubnet"] = {
            "return": {"dhcpSubnet": {"subnetIpAddress": "10.0.0.0"}}
        }
        result = ucm.get_dhcp_subnet(uuid="{DDDD-4444}")
        op, body = sent(ucm)
        assert op == "getDhcpSubnet"
        assert text(body, "uuid") == "{DDDD-4444}"
        assert result == {"subnetIpAddress": "10.0.0.0"}

    def test_get_dhcp_subnet_by_server_and_ip(self, ucm):
        ucm.recorder.responses["getDhcpSubnet"] = {
            "return": {"dhcpSubnet": {"subnetIpAddress": "10.0.0.0"}}
        }
        ucm.get_dhcp_subnet(
            dhcpServerName="pub.corp.com", subnetIpAddress="10.0.0.0"
        )
        op, body = sent(ucm)
        assert op == "getDhcpSubnet"
        assert text(body, "dhcpServerName") == "pub.corp.com"
        assert text(body, "subnetIpAddress") == "10.0.0.0"

    def test_get_dhcp_subnet_requires_identifier(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_dhcp_subnet()

    def test_get_dhcp_subnets(self, ucm):
        ucm.recorder.responses["listDhcpSubnet"] = {
            "return": {"dhcpSubnet": [{"subnetIpAddress": "10.0.0.0"}]}
        }
        # AXL LDhcpSubnet search criteria uses subnetIpAddress, not dhcpServerName
        result = ucm.get_dhcp_subnets(search_subnetIpAddress="%")
        op, body = sent(ucm)
        assert op == "listDhcpSubnet"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_dhcp_subnets_empty(self, ucm):
        ucm.recorder.responses["listDhcpSubnet"] = {"return": None}
        result = ucm.get_dhcp_subnets(search_subnetIpAddress="%")
        assert result == []

    def test_update_dhcp_subnet(self, ucm):
        ucm.update_dhcp_subnet(uuid="{DDDD-4444}", primaryDnsIpAddress="8.8.8.8")
        op, body = sent(ucm)
        assert op == "updateDhcpSubnet"
        assert text(body, "uuid") == "{DDDD-4444}"

    def test_remove_dhcp_subnet_by_uuid(self, ucm):
        ucm.remove_dhcp_subnet(uuid="{DDDD-4444}")
        op, body = sent(ucm)
        assert op == "removeDhcpSubnet"
        assert text(body, "uuid") == "{DDDD-4444}"

    def test_remove_dhcp_subnet_by_server_and_ip(self, ucm):
        ucm.remove_dhcp_subnet(
            dhcpServerName="pub.corp.com", subnetIpAddress="10.0.0.0"
        )
        op, body = sent(ucm)
        assert op == "removeDhcpSubnet"
        assert text(body, "dhcpServerName") == "pub.corp.com"

    def test_remove_dhcp_subnet_requires_identifier(self, ucm):
        with pytest.raises(ValueError):
            ucm.remove_dhcp_subnet()


# ---------------------------------------------------------------------------
# WLANProfile
# ---------------------------------------------------------------------------

class TestWLANProfile:
    def test_add_wlan_profile(self, ucm):
        ucm.add_wlan_profile(
            name="Corp-WLAN",
            ssid="CorpWiFi",
            frequencyBand="Auto",
            userModifiable="Disallowed",
            authMethod="EAP-FAST",
        )
        op, body = sent(ucm)
        assert op == "addWLANProfile"
        assert text(body, "wLANProfile/name") == "Corp-WLAN"
        assert text(body, "wLANProfile/ssid") == "CorpWiFi"

    def test_get_wlan_profile_by_name(self, ucm):
        ucm.recorder.responses["getWLANProfile"] = {
            "return": {"wLANProfile": {"name": "Corp-WLAN"}}
        }
        result = ucm.get_wlan_profile(name="Corp-WLAN")
        op, body = sent(ucm)
        assert op == "getWLANProfile"
        assert text(body, "name") == "Corp-WLAN"
        assert result == {"name": "Corp-WLAN"}

    def test_get_wlan_profile_by_uuid(self, ucm):
        ucm.recorder.responses["getWLANProfile"] = {
            "return": {"wLANProfile": {"name": "Corp-WLAN"}}
        }
        ucm.get_wlan_profile(uuid="{EEEE-5555}")
        op, body = sent(ucm)
        assert op == "getWLANProfile"
        assert text(body, "uuid") == "{EEEE-5555}"

    def test_get_wlan_profile_requires_identifier(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_wlan_profile()

    def test_get_wlan_profiles(self, ucm):
        ucm.recorder.responses["listWLANProfile"] = {
            "return": {"wLANProfile": [{"name": "Corp-WLAN"}]}
        }
        result = ucm.get_wlan_profiles()
        op, body = sent(ucm)
        assert op == "listWLANProfile"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_wlan_profiles_empty(self, ucm):
        ucm.recorder.responses["listWLANProfile"] = {"return": None}
        result = ucm.get_wlan_profiles()
        assert result == []

    def test_update_wlan_profile(self, ucm):
        ucm.update_wlan_profile(name="Corp-WLAN", ssid="CorpWiFi-New")
        op, body = sent(ucm)
        assert op == "updateWLANProfile"
        assert text(body, "name") == "Corp-WLAN"
        assert text(body, "ssid") == "CorpWiFi-New"

    def test_remove_wlan_profile_by_name(self, ucm):
        ucm.remove_wlan_profile(name="Corp-WLAN")
        op, body = sent(ucm)
        assert op == "removeWLANProfile"
        assert text(body, "name") == "Corp-WLAN"

    def test_remove_wlan_profile_by_uuid(self, ucm):
        ucm.remove_wlan_profile(uuid="{EEEE-5555}")
        op, body = sent(ucm)
        assert op == "removeWLANProfile"
        assert text(body, "uuid") == "{EEEE-5555}"

    def test_remove_wlan_profile_requires_identifier(self, ucm):
        with pytest.raises(ValueError):
            ucm.remove_wlan_profile()


# ---------------------------------------------------------------------------
# WifiHotspot
# ---------------------------------------------------------------------------

class TestWifiHotspot:
    def test_add_wifi_hotspot(self, ucm):
        ucm.add_wifi_hotspot(
            name="Hotspot-1",
            ssidPrefix="Corp-HS",
            frequencyBand="Auto",
            authenticationMethod="None",
        )
        op, body = sent(ucm)
        assert op == "addWifiHotspot"
        assert text(body, "wifiHotspot/name") == "Hotspot-1"
        assert text(body, "wifiHotspot/ssidPrefix") == "Corp-HS"

    def test_get_wifi_hotspot_by_name(self, ucm):
        ucm.recorder.responses["getWifiHotspot"] = {
            "return": {"wifiHotspot": {"name": "Hotspot-1"}}
        }
        result = ucm.get_wifi_hotspot(name="Hotspot-1")
        op, body = sent(ucm)
        assert op == "getWifiHotspot"
        assert text(body, "name") == "Hotspot-1"
        assert result == {"name": "Hotspot-1"}

    def test_get_wifi_hotspot_by_uuid(self, ucm):
        ucm.recorder.responses["getWifiHotspot"] = {
            "return": {"wifiHotspot": {"name": "Hotspot-1"}}
        }
        ucm.get_wifi_hotspot(uuid="{FFFF-6666}")
        op, body = sent(ucm)
        assert op == "getWifiHotspot"
        assert text(body, "uuid") == "{FFFF-6666}"

    def test_get_wifi_hotspot_requires_identifier(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_wifi_hotspot()

    def test_get_wifi_hotspots(self, ucm):
        ucm.recorder.responses["listWifiHotspot"] = {
            "return": {"wifiHotspot": [{"name": "Hotspot-1"}]}
        }
        result = ucm.get_wifi_hotspots()
        op, body = sent(ucm)
        assert op == "listWifiHotspot"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_wifi_hotspots_empty(self, ucm):
        ucm.recorder.responses["listWifiHotspot"] = {"return": None}
        result = ucm.get_wifi_hotspots()
        assert result == []

    def test_update_wifi_hotspot(self, ucm):
        ucm.update_wifi_hotspot(name="Hotspot-1", ssidPrefix="Corp-HS-New")
        op, body = sent(ucm)
        assert op == "updateWifiHotspot"
        assert text(body, "name") == "Hotspot-1"

    def test_remove_wifi_hotspot_by_name(self, ucm):
        ucm.remove_wifi_hotspot(name="Hotspot-1")
        op, body = sent(ucm)
        assert op == "removeWifiHotspot"
        assert text(body, "name") == "Hotspot-1"

    def test_remove_wifi_hotspot_by_uuid(self, ucm):
        ucm.remove_wifi_hotspot(uuid="{FFFF-6666}")
        op, body = sent(ucm)
        assert op == "removeWifiHotspot"
        assert text(body, "uuid") == "{FFFF-6666}"

    def test_remove_wifi_hotspot_requires_identifier(self, ucm):
        with pytest.raises(ValueError):
            ucm.remove_wifi_hotspot()


# ---------------------------------------------------------------------------
# WirelessAccessPointControllers
# ---------------------------------------------------------------------------

class TestWirelessAccessPointControllers:
    def test_add_wireless_access_point_controllers(self, ucm):
        ucm.add_wireless_access_point_controllers(
            name="WAP-Controller-1",
            snmpUserIdOrCommunityString="public",
            resyncInterval=32,
        )
        op, body = sent(ucm)
        assert op == "addWirelessAccessPointControllers"
        assert text(body, "wirelessAccessPointControllers/name") == "WAP-Controller-1"
        assert (
            text(body, "wirelessAccessPointControllers/snmpUserIdOrCommunityString")
            == "public"
        )

    def test_get_wireless_access_point_controllers_by_name(self, ucm):
        ucm.recorder.responses["getWirelessAccessPointControllers"] = {
            "return": {
                "wirelessAccessPointControllers": {"name": "WAP-Controller-1"}
            }
        }
        result = ucm.get_wireless_access_point_controllers(name="WAP-Controller-1")
        op, body = sent(ucm)
        assert op == "getWirelessAccessPointControllers"
        assert text(body, "name") == "WAP-Controller-1"
        assert result == {"name": "WAP-Controller-1"}

    def test_get_wireless_access_point_controllers_by_uuid(self, ucm):
        ucm.recorder.responses["getWirelessAccessPointControllers"] = {
            "return": {
                "wirelessAccessPointControllers": {"name": "WAP-Controller-1"}
            }
        }
        ucm.get_wireless_access_point_controllers(uuid="{GGGG-7777}")
        op, body = sent(ucm)
        assert op == "getWirelessAccessPointControllers"
        assert text(body, "uuid") == "{GGGG-7777}"

    def test_get_wireless_access_point_controllers_requires_identifier(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_wireless_access_point_controllers()

    def test_get_wireless_access_point_controllers_list(self, ucm):
        ucm.recorder.responses["listWirelessAccessPointControllers"] = {
            "return": {
                "wirelessAccessPointControllers": [{"name": "WAP-Controller-1"}]
            }
        }
        result = ucm.get_wireless_access_point_controllers_list()
        op, body = sent(ucm)
        assert op == "listWirelessAccessPointControllers"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_wireless_access_point_controllers_list_empty(self, ucm):
        ucm.recorder.responses["listWirelessAccessPointControllers"] = {
            "return": None
        }
        result = ucm.get_wireless_access_point_controllers_list()
        assert result == []

    def test_update_wireless_access_point_controllers(self, ucm):
        ucm.update_wireless_access_point_controllers(
            name="WAP-Controller-1",
            snmpUserIdOrCommunityString="private",
        )
        op, body = sent(ucm)
        assert op == "updateWirelessAccessPointControllers"
        assert text(body, "name") == "WAP-Controller-1"

    def test_remove_wireless_access_point_controllers_by_name(self, ucm):
        ucm.remove_wireless_access_point_controllers(name="WAP-Controller-1")
        op, body = sent(ucm)
        assert op == "removeWirelessAccessPointControllers"
        assert text(body, "name") == "WAP-Controller-1"

    def test_remove_wireless_access_point_controllers_by_uuid(self, ucm):
        ucm.remove_wireless_access_point_controllers(uuid="{GGGG-7777}")
        op, body = sent(ucm)
        assert op == "removeWirelessAccessPointControllers"
        assert text(body, "uuid") == "{GGGG-7777}"

    def test_remove_wireless_access_point_controllers_requires_identifier(self, ucm):
        with pytest.raises(ValueError):
            ucm.remove_wireless_access_point_controllers()


# ---------------------------------------------------------------------------
# WlanProfileGroup
# ---------------------------------------------------------------------------

class TestWlanProfileGroup:
    def test_add_wlan_profile_group(self, ucm):
        ucm.add_wlan_profile_group(
            name="WLAN-Group-1",
            description="Corp WLAN group",
        )
        op, body = sent(ucm)
        assert op == "addWlanProfileGroup"
        assert text(body, "wlanProfileGroup/name") == "WLAN-Group-1"
        assert text(body, "wlanProfileGroup/description") == "Corp WLAN group"

    def test_get_wlan_profile_group_by_name(self, ucm):
        ucm.recorder.responses["getWlanProfileGroup"] = {
            "return": {"wlanProfileGroup": {"name": "WLAN-Group-1"}}
        }
        result = ucm.get_wlan_profile_group(name="WLAN-Group-1")
        op, body = sent(ucm)
        assert op == "getWlanProfileGroup"
        assert text(body, "name") == "WLAN-Group-1"
        assert result == {"name": "WLAN-Group-1"}

    def test_get_wlan_profile_group_by_uuid(self, ucm):
        ucm.recorder.responses["getWlanProfileGroup"] = {
            "return": {"wlanProfileGroup": {"name": "WLAN-Group-1"}}
        }
        ucm.get_wlan_profile_group(uuid="{HHHH-8888}")
        op, body = sent(ucm)
        assert op == "getWlanProfileGroup"
        assert text(body, "uuid") == "{HHHH-8888}"

    def test_get_wlan_profile_group_requires_identifier(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_wlan_profile_group()

    def test_get_wlan_profile_groups(self, ucm):
        ucm.recorder.responses["listWlanProfileGroup"] = {
            "return": {"wlanProfileGroup": [{"name": "WLAN-Group-1"}]}
        }
        result = ucm.get_wlan_profile_groups()
        op, body = sent(ucm)
        assert op == "listWlanProfileGroup"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_wlan_profile_groups_empty(self, ucm):
        ucm.recorder.responses["listWlanProfileGroup"] = {"return": None}
        result = ucm.get_wlan_profile_groups()
        assert result == []

    def test_update_wlan_profile_group(self, ucm):
        ucm.update_wlan_profile_group(
            name="WLAN-Group-1", newName="WLAN-Group-1-Renamed"
        )
        op, body = sent(ucm)
        assert op == "updateWlanProfileGroup"
        assert text(body, "name") == "WLAN-Group-1"
        assert text(body, "newName") == "WLAN-Group-1-Renamed"

    def test_remove_wlan_profile_group_by_name(self, ucm):
        ucm.remove_wlan_profile_group(name="WLAN-Group-1")
        op, body = sent(ucm)
        assert op == "removeWlanProfileGroup"
        assert text(body, "name") == "WLAN-Group-1"

    def test_remove_wlan_profile_group_by_uuid(self, ucm):
        ucm.remove_wlan_profile_group(uuid="{HHHH-8888}")
        op, body = sent(ucm)
        assert op == "removeWlanProfileGroup"
        assert text(body, "uuid") == "{HHHH-8888}"

    def test_remove_wlan_profile_group_requires_identifier(self, ucm):
        with pytest.raises(ValueError):
            ucm.remove_wlan_profile_group()
