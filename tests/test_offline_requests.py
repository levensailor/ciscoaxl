"""Offline tests: build every request with zeep against the bundled schemas, no CUCM needed.

Run with: pytest tests/test_offline_requests.py
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


class AutoDict(dict):
    """Canned response: any missing key returns another AutoDict."""

    def __missing__(self, key):
        value = AutoDict()
        self[key] = value
        return value


class Recorder:
    """Stands in for the zeep service: serializes each call and returns a canned response."""

    def __init__(self, zeep_client, service):
        self._zeep = zeep_client
        self._real = service
        self._binding = service._binding
        self.calls = []
        self.responses = {}

    def __getattr__(self, op_name):
        def call(*args, **kwargs):
            # Bypass create_message: some AXL requests have an element named "service".
            message, _headers = self._real._binding._create(op_name, args, kwargs, client=self._zeep)
            body = message.find("{http://schemas.xmlsoap.org/soap/envelope/}Body")[0]
            self.calls.append((op_name, body))
            response = self.responses.get(op_name, AutoDict())
            if isinstance(response, Exception):
                raise response
            return response

        return call


class SimpleRecorder(Recorder):
    """Records (operation, kwargs) without SOAP serialization.

    Use when a request embeds a complex nested object whose inner required fields
    would fail create_message, and the test only checks the operation and wrapper kwarg.
    """

    def __getattr__(self, op_name):
        def call(*args, **kwargs):
            self.calls.append((op_name, kwargs))
            response = self.responses.get(op_name, AutoDict())
            if isinstance(response, Exception):
                raise response
            return response

        return call


def make_ucm(version="15.0", recorder_class=Recorder):
    if version not in _clients:
        wsdl = (SCHEMA_DIR / version / "AXLAPI.wsdl").as_uri()
        settings = Settings(strict=False, xml_huge_tree=True, xsd_ignore_sequence_order=True)
        _clients[version] = Client(wsdl, settings=settings)
    zeep_client = _clients[version]
    service = zeep_client.create_service(BINDING, "https://cucm.invalid:8443/axl/")
    recorder = recorder_class(zeep_client, service)

    ucm = axl.__new__(axl)
    ucm._zeep = zeep_client
    ucm.cucm = "cucm.invalid"
    ucm.cucm_version = version
    ucm.client = AliasingService(zeep_client, recorder)
    ucm.recorder = recorder
    return ucm


def make_ucm_simple(version="15.0"):
    """Return a UCM stub backed by SimpleRecorder (no SOAP serialization)."""
    return make_ucm(version, recorder_class=SimpleRecorder)


def sent(ucm, index=-1):
    """Return (operation, xml element) of a recorded call."""
    return ucm.recorder.calls[index]


def simple_sent(ucm, index=-1):
    """Return (operation, kwargs) of a SimpleRecorder call."""
    return ucm.recorder.calls[index]


def text(body, path):
    """Text of the first element matching a local-name path like 'phone/name'."""
    xpath = "./" + "/".join("*" if p == "*" else f"*[local-name()='{p}']" for p in path.split("/"))
    found = body.xpath(xpath)
    return found[0].text if found else None


def has(body, path):
    xpath = "./" + "/".join("*" if p == "*" else f"*[local-name()='{p}']" for p in path.split("/"))
    return bool(body.xpath(xpath))


@pytest.fixture
def ucm():
    return make_ucm("15.0")


class TestErrorContract:
    def test_fault_is_raised(self, ucm):
        ucm.recorder.responses["getPhone"] = Fault("Item not valid")
        with pytest.raises(Fault):
            ucm.get_phone(name="SEP000000000000")

    def test_empty_list_returns_empty_list(self, ucm):
        ucm.recorder.responses["listLocation"] = {"return": None}
        assert ucm.get_locations() == []

    def test_empty_hunt_pilots_returns_empty_list(self, ucm):
        ucm.recorder.responses["listHuntPilot"] = {"return": None}
        assert ucm.get_hunt_pilots() == []

    def test_empty_hunt_lists_returns_empty_list(self, ucm):
        ucm.recorder.responses["listHuntList"] = {"return": None}
        assert ucm.get_hunt_lists() == []

    def test_empty_line_groups_returns_empty_list(self, ucm):
        ucm.recorder.responses["listLineGroup"] = {"return": None}
        assert ucm.get_line_groups() == []

    def test_empty_call_pickup_groups_returns_empty_list(self, ucm):
        ucm.recorder.responses["listCallPickupGroup"] = {"return": None}
        assert ucm.get_call_pickup_groups() == []

    def test_empty_route_plan_returns_empty_list(self, ucm):
        ucm.recorder.responses["listRoutePlan"] = {"return": None}
        assert ucm.list_route_plan_specific() == []

    def test_empty_call_manager_groups_returns_empty_list(self, ucm):
        ucm.recorder.responses["listCallManagerGroup"] = {"return": None}
        assert ucm.get_call_manager_groups() == []

    def test_empty_called_party_xforms_returns_empty_list(self, ucm):
        ucm.recorder.responses["listCalledPartyTransformationPattern"] = {"return": None}
        assert ucm.get_called_party_xforms() == []

    def test_run_sql_query_raises_fault(self, ucm):
        ucm.recorder.responses["executeSQLQuery"] = Fault("SQL error")
        with pytest.raises(Fault):
            ucm.run_sql_query("select * from device")

    def test_name_or_uuid_required(self, ucm):
        with pytest.raises(ValueError):
            ucm.do_device_reset()
        with pytest.raises(ValueError):
            ucm.reset_sip_trunk(name="a", uuid="b")


class TestFriendlyNames:
    def test_partition_becomes_route_partition_name(self, ucm):
        ucm.get_directory_number(pattern="1000", partition="Internal_PT")
        op, body = sent(ucm)
        assert op == "getLine"
        assert text(body, "routePartitionName") == "Internal_PT"

    def test_name_becomes_pattern_for_pattern_objects(self, ucm):
        ucm.get_hunt_pilot(name="5000", partition="Internal_PT")
        _, body = sent(ucm)
        assert text(body, "pattern") == "5000"

    def test_mixin_methods_accept_friendly_names(self, ucm):
        ucm.get_meet_me(pattern="8000", partition="Internal_PT")
        ucm.delete_recording_profile(profile="Rec1")
        ucm.get_handoff_configuration(pattern="9900", partition="PT")
        assert text(sent(ucm, 0)[1], "routePartitionName") == "Internal_PT"
        assert sent(ucm, 1)[0] == "removeRecordingProfile"
        assert text(sent(ucm, 1)[1], "name") == "Rec1"
        assert text(sent(ucm, 2)[1], "routePartitionName") == "PT"

    def test_object_noun_becomes_name(self, ucm):
        ucm.delete_device_pool(device_pool="Branch_DP")
        ucm.get_partition(partition="Internal_PT")
        ucm.delete_calling_search_space(calling_search_space="Device_CSS")
        assert [text(body, "name") for _, body in ucm.recorder.calls] == [
            "Branch_DP",
            "Internal_PT",
            "Device_CSS",
        ]

    def test_field_aliases_on_update(self, ucm):
        ucm.update_conference_bridge(
            name="CFB", device_pool="Default", location="Hub_None", security_profile="x"
        )
        _, body = sent(ucm)
        assert text(body, "devicePoolName") == "Default"
        assert text(body, "locationName") == "Hub_None"
        assert text(body, "securityProfileName") == "x"

    def test_axl_names_still_work(self, ucm):
        ucm.update_device_pool(name="DP", mediaResourceListName="MRGL")
        _, body = sent(ucm)
        assert text(body, "mediaResourceListName") == "MRGL"

    def test_alias_and_axl_name_together_is_an_error(self, ucm):
        with pytest.raises(ValueError):
            ucm.update_device_pool(name="DP", device_pool="x", devicePoolName="y")

    def test_explicit_signatures_accept_nouns_and_axl_names(self, ucm):
        ucm.add_device_pool(device_pool="Hollywood_DP")
        ucm.add_partition(partition="VIP_PT")
        ucm.add_region(region="Hollywood_REG")
        ucm.add_location(location="Hollywood_LOC")
        ucm.add_route_group(route_group="RG1", members=["ITSP"])
        ucm.add_route_list(route_list="RL1", members=["RG1"])
        ucm.add_cti_route_point(cti_route_point="AA_CTI")
        ucm.do_device_reset(device="SEP001122334455")
        names = [text(body, "*/name") or text(body, "deviceName") for _, body in ucm.recorder.calls]
        assert names == [
            "Hollywood_DP",
            "VIP_PT",
            "Hollywood_REG",
            "Hollywood_LOC",
            "RG1",
            "RL1",
            "AA_CTI",
            "SEP001122334455",
        ]

    def test_explicit_signatures_accept_axl_field_names(self, ucm):
        ucm.add_directory_number(pattern="1102", routePartitionName="ABQ_PT")
        ucm.add_translation(pattern="1000", routePartitionName="PT", callingSearchSpaceName="CSS")
        assert text(sent(ucm, 0)[1], "line/routePartitionName") == "ABQ_PT"
        assert text(sent(ucm, 1)[1], "transPattern/callingSearchSpaceName") == "CSS"

    def test_explicit_signature_conflict_is_an_error(self, ucm):
        with pytest.raises(ValueError):
            ucm.add_directory_number(pattern="1102", partition="A", routePartitionName="B")

    def test_user_id_alias(self, ucm):
        ucm.delete_user(user_id="jsmith")
        ucm.get_user(user_id="jsmith")
        assert [text(body, "userid") for _, body in ucm.recorder.calls] == ["jsmith", "jsmith"]

    def test_python_booleans_become_axl_booleans(self, ucm):
        ucm.add_route_pattern(pattern="9.@", route_list="RL", blockEnable=False, patternUrgency=True)
        _, body = sent(ucm)
        assert text(body, "routePattern/blockEnable") == "false"
        assert text(body, "routePattern/patternUrgency") == "true"


class TestHighSeverityFixes:
    def test_update_call_manager_group_calls_update(self, ucm):
        ucm.update_call_manager_group(name="Default", members=["cucm-pub", "cucm-sub"])
        op, body = sent(ucm)
        assert op == "updateCallManagerGroup"
        assert len(body.xpath("./*[local-name()='members']/*")) == 2

    def test_add_sip_trunk_wraps_and_fills_required(self, ucm):
        ucm.add_sip_trunk(
            name="ITSP",
            device_pool="Default",
            destinations={"destination": [{"addressIpv4": "10.0.0.1", "port": 5060, "sortOrder": 1}]},
        )
        op, body = sent(ucm)
        assert op == "addSipTrunk"
        assert text(body, "sipTrunk/class") == "Trunk"
        assert text(body, "sipTrunk/devicePoolName") == "Default"
        assert text(body, "sipTrunk/callingAndCalledPartyInfoFormat")

    def test_add_h323_gateway_friendly_names(self, ucm):
        ucm.add_h323_gateway(h323_gateway="10.1.1.1", device_pool="Default", clng_party_nat_pre="9")
        _, body = sent(ucm)
        assert text(body, "h323Gateway/name") == "10.1.1.1"
        assert text(body, "h323Gateway/callingPartyNationalPrefix") == "9"
        assert text(body, "h323Gateway/signalingPort") == "1720"

    def test_do_device_reset_by_uuid(self, ucm):
        ucm.do_device_reset(uuid="{11111111-2222-3333-4444-555555555555}")
        _, body = sent(ucm)
        assert text(body, "deviceName") == "{11111111-2222-3333-4444-555555555555}"
        assert not has(body, "uuid")

    @pytest.mark.parametrize("version,field", [("8.5", "kbits"), ("10.0", "withinAudioBandwidth"), ("15.0", "withinAudioBandwidth")])
    def test_add_location_matches_schema(self, version, field):
        ucm = make_ucm(version)
        ucm.add_location(name="Branch")
        _, body = sent(ucm)
        assert has(body, f"location/{field}")

    def test_update_region_omits_empty_new_name(self, ucm):
        ucm.recorder.responses["listRegion"] = {"return": {"region": [{"name": "Default"}, {"name": "Branch"}]}}
        ucm.update_region(name="Branch")
        op, body = sent(ucm)
        assert op == "updateRegion"
        assert not has(body, "newName")

    def test_update_srst_omits_empty_new_name(self, ucm):
        ucm.update_srst(name="SRST1", ipAddress="10.0.0.1")
        _, body = sent(ucm)
        assert not has(body, "newName")
        assert text(body, "ipAddress") == "10.0.0.1"

    def test_add_hunt_pilot_fills_required(self, ucm):
        ucm.add_hunt_pilot(pattern="5000", hunt_list="HL1")
        _, body = sent(ucm)
        assert text(body, "huntPilot/huntListName") == "HL1"
        assert text(body, "huntPilot/blockEnable") == "false"

    def test_add_line_group_fills_schema_defaults(self, ucm):
        ucm.add_line_group(name="LG1")
        _, body = sent(ucm)
        assert text(body, "lineGroup/distributionAlgorithm") == "Longest Idle Time"

    def test_add_hunt_list_call_manager_group_alias(self, ucm):
        ucm.add_hunt_list(name="HL1", callManagerGroup="Default")
        _, body = sent(ucm)
        assert text(body, "huntList/callManagerGroupName") == "Default"

    def test_add_user_phone_profiles(self, ucm):
        ucm.add_user(user_id="jsmith", last_name="Smith", phoneProfiles=["UDP_jsmith"])
        _, body = sent(ucm)
        assert text(body, "user/phoneProfiles/profileName") == "UDP_jsmith"
        assert not has(body, "user/firstName")

    def test_update_user_em_merges_groups_and_profiles(self, ucm):
        ucm.recorder.responses["getDeviceProfile"] = {
            "return": {"deviceProfile": {"uuid": "{AAAAAAAA-0000-0000-0000-000000000001}"}}
        }
        ucm.recorder.responses["getUser"] = {
            "return": {
                "user": {
                    "phoneProfiles": {"profileName": [{"uuid": "{AAAAAAAA-0000-0000-0000-000000000002}"}]},
                    "associatedGroups": {"userGroup": [{"name": "Standard CCM Admin Users"}]},
                }
            }
        }
        ucm.update_user_em("jsmith", "UDP_jsmith", "UDP_jsmith", "CSS", "1000")
        op, body = sent(ucm)
        assert op == "updateUser"
        groups = [e.text for e in body.xpath(".//*[local-name()='userGroup']/*[local-name()='name']")]
        assert groups == ["Standard CCM Admin Users", "Standard CCM End Users"]
        assert len(body.xpath(".//*[local-name()='profileName']")) == 2

    def test_add_phone_flags_gated_by_schema(self):
        modern = make_ucm("15.0")
        modern.add_phone(name="SEP001122334455")
        _, body = sent(modern)
        assert text(body, "phone/enableActivationID") == "false"
        assert text(body, "phone/securityProfileName") == "Cisco 8861 - Standard SIP Non-Secure Profile"
        assert not has(body, "phone/lines")

        legacy = make_ucm("12.0")
        legacy.add_phone(name="SEP001122334455")
        _, body = sent(legacy)
        assert not has(body, "phone/enableActivationID")

    def test_add_phone_services_lines_and_vendor_config(self, ucm):
        ucm.add_phone(
            name="SEP001122334455",
            lines=[("1000", "Internal_PT", "Jim", "Jim", "Jim - 1000", "5551000")],
            em_service_url=True,
            em_url_button_enable=True,
            ehook_enable=1,
        )
        _, body = sent(ucm)
        assert text(body, "phone/lines/line/dirn/pattern") == "1000"
        assert text(body, "phone/services/service/urlButtonIndex") == "1"
        assert text(body, "phone/vendorConfig/ehookEnable") == "1"

    def test_add_called_party_xform_requires_pattern(self, ucm):
        with pytest.raises(TypeError):
            ucm.add_called_party_xform()
        ucm.add_called_party_xform("9.@")
        _, body = sent(ucm)
        assert text(body, "calledPartyTransformationPattern/pattern") == "9.@"

    def test_device_login_and_logout_aliases(self, ucm):
        ucm.do_device_login(device="SEP001122334455", loginDuration=0, profileName="UDP", userId="jsmith")
        ucm.do_device_logout(device="SEP001122334455")
        assert [text(body, "deviceName") for _, body in ucm.recorder.calls] == ["SEP001122334455"] * 2

    def test_update_mtp_and_location_aliases(self, ucm):
        ucm.update_mtp(name="MTP1", device_pool="Default")
        ucm.update_location(name="Branch", withImmersiveKbits=100)
        assert text(sent(ucm, 0)[1], "devicePoolName") == "Default"
        assert text(sent(ucm, 1)[1], "withinImmersiveKbits") == "100"

    def test_update_phone_lines_and_aliases(self, ucm):
        ucm.update_phone(name="SEP001122334455", css="Device_CSS", lines=[("1000", "Internal_PT")])
        _, body = sent(ucm)
        assert text(body, "callingSearchSpaceName") == "Device_CSS"
        assert text(body, "lines/line/dirn/routePartitionName") == "Internal_PT"

    def test_update_route_pattern_destination_alias(self, ucm):
        ucm.update_route_pattern(pattern="9.@", partition="PSTN_PT", route_list="RL1")
        _, body = sent(ucm)
        assert text(body, "destination/routeListName") == "RL1"
        assert text(body, "routePartitionName") == "PSTN_PT"

    def test_getters_unwrap(self, ucm):
        ucm.recorder.responses["getLocation"] = {"return": {"location": {"name": "Hub_None"}}}
        ucm.recorder.responses["getTransPattern"] = {"return": {"transPattern": {"pattern": "1000"}}}
        assert ucm.get_location(name="Hub_None") == {"name": "Hub_None"}
        assert ucm.get_translation(pattern="1000", partition="PT") == {"pattern": "1000"}

    def test_translation_in_none_partition(self, ucm):
        ucm.delete_translation(pattern="1000")
        _, body = sent(ucm)
        assert text(body, "pattern") == "1000"
        assert has(body, "routePartitionName")


class TestSchemaVersions:
    @pytest.mark.parametrize("version", ["11.0", "12.5", "14.0", "15.0"])
    def test_common_adds_build(self, version):
        ucm = make_ucm(version)
        ucm.add_partition(name="Internal_PT")
        ucm.add_calling_search_space(name="Device_CSS", members=["Internal_PT"])
        ucm.add_directory_number(pattern="1000", partition="Internal_PT")
        ucm.add_route_group(name="RG1", members=["ITSP"])
        ucm.add_route_list(name="RL1", members=["RG1"])
        ucm.add_device_pool(name="Branch_DP", route_group="RG1")
        ucm.add_transcoder(name="XCODE1")
        assert len(ucm.recorder.calls) == 7


class TestSchemaFields:
    def test_add_phone_enable_activation_id_in_15(self):
        ucm = make_ucm("15.0")
        assert "enableActivationID" in ucm._schema_fields("addPhone", "phone")

    def test_add_phone_enable_activation_id_not_in_12(self):
        ucm = make_ucm("12.0")
        assert "enableActivationID" not in ucm._schema_fields("addPhone", "phone")
