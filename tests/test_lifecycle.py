"""Offline request tests for ciscoaxl/lifecycle.py.

Run with: pytest tests/test_lifecycle.py
"""
import pytest

from test_offline_requests import make_ucm, sent, text, has


@pytest.fixture
def ucm():
    return make_ucm("15.0")


class TestCtiRoutePointLifecycle:
    def test_apply_cti_route_point_by_name(self, ucm):
        ucm.apply_cti_route_point(name="AA_CTI")
        op, body = sent(ucm)
        assert op == "applyCtiRoutePoint"
        assert text(body, "name") == "AA_CTI"

    def test_reset_cti_route_point_by_name(self, ucm):
        ucm.reset_cti_route_point(name="AA_CTI")
        op, body = sent(ucm)
        assert op == "resetCtiRoutePoint"
        assert text(body, "name") == "AA_CTI"

    def test_restart_cti_route_point_by_uuid(self, ucm):
        ucm.restart_cti_route_point(uuid="{11111111-0000-0000-0000-000000000001}")
        op, body = sent(ucm)
        assert op == "restartCtiRoutePoint"
        assert text(body, "uuid") == "{11111111-0000-0000-0000-000000000001}"
        assert not has(body, "name")

    def test_apply_cti_route_point_requires_one_identifier(self, ucm):
        with pytest.raises(ValueError):
            ucm.apply_cti_route_point()
        with pytest.raises(ValueError):
            ucm.apply_cti_route_point(name="x", uuid="{a}")


class TestLineLifecycle:
    def test_apply_line_by_pattern(self, ucm):
        ucm.apply_line(pattern="1000", partition="Internal_PT")
        op, body = sent(ucm)
        assert op == "applyLine"
        assert text(body, "pattern") == "1000"
        assert text(body, "routePartitionName") == "Internal_PT"

    def test_apply_line_by_uuid(self, ucm):
        ucm.apply_line(uuid="{11111111-0000-0000-0000-000000000002}")
        op, body = sent(ucm)
        assert op == "applyLine"
        assert text(body, "uuid") == "{11111111-0000-0000-0000-000000000002}"
        assert not has(body, "pattern")

    def test_reset_line_by_pattern(self, ucm):
        ucm.reset_line(pattern="2000")
        op, body = sent(ucm)
        assert op == "resetLine"
        assert text(body, "pattern") == "2000"

    def test_restart_line_by_uuid(self, ucm):
        ucm.restart_line(uuid="{11111111-0000-0000-0000-000000000003}")
        op, body = sent(ucm)
        assert op == "restartLine"
        assert text(body, "uuid") == "{11111111-0000-0000-0000-000000000003}"

    def test_apply_line_requires_one_identifier(self, ucm):
        with pytest.raises(ValueError):
            ucm.apply_line()
        with pytest.raises(ValueError):
            ucm.apply_line(pattern="1000", uuid="{a}")


class TestHuntListLifecycle:
    def test_apply_hunt_list(self, ucm):
        ucm.apply_hunt_list(name="HL1")
        op, body = sent(ucm)
        assert op == "applyHuntList"
        assert text(body, "name") == "HL1"

    def test_reset_hunt_list(self, ucm):
        ucm.reset_hunt_list(name="HL1")
        op, body = sent(ucm)
        assert op == "resetHuntList"
        assert text(body, "name") == "HL1"

    def test_reset_hunt_list_by_uuid(self, ucm):
        ucm.reset_hunt_list(uuid="{11111111-0000-0000-0000-000000000004}")
        op, body = sent(ucm)
        assert op == "resetHuntList"
        assert text(body, "uuid") == "{11111111-0000-0000-0000-000000000004}"


class TestRouteListLifecycle:
    def test_apply_route_list(self, ucm):
        ucm.apply_route_list(name="RL1")
        op, body = sent(ucm)
        assert op == "applyRouteList"
        assert text(body, "name") == "RL1"

    def test_reset_route_list(self, ucm):
        ucm.reset_route_list(name="RL1")
        op, body = sent(ucm)
        assert op == "resetRouteList"
        assert text(body, "name") == "RL1"


class TestRoutePartitionLifecycle:
    def test_apply_route_partition(self, ucm):
        ucm.apply_route_partition(name="Internal_PT")
        op, body = sent(ucm)
        assert op == "applyRoutePartition"
        assert text(body, "name") == "Internal_PT"

    def test_restart_route_partition(self, ucm):
        ucm.restart_route_partition(name="Internal_PT")
        op, body = sent(ucm)
        assert op == "restartRoutePartition"
        assert text(body, "name") == "Internal_PT"

    def test_restart_route_partition_by_uuid(self, ucm):
        ucm.restart_route_partition(uuid="{11111111-0000-0000-0000-000000000005}")
        op, body = sent(ucm)
        assert op == "restartRoutePartition"
        assert text(body, "uuid") == "{11111111-0000-0000-0000-000000000005}"


class TestH323GatewayLifecycle:
    def test_apply_h323_gateway(self, ucm):
        ucm.apply_h323_gateway(name="10.1.1.1")
        op, body = sent(ucm)
        assert op == "applyH323Gateway"
        assert text(body, "name") == "10.1.1.1"

    def test_reset_h323_gateway(self, ucm):
        ucm.reset_h323_gateway(name="10.1.1.1")
        op, body = sent(ucm)
        assert op == "resetH323Gateway"
        assert text(body, "name") == "10.1.1.1"

    def test_restart_h323_gateway_by_uuid(self, ucm):
        ucm.restart_h323_gateway(uuid="{11111111-0000-0000-0000-000000000006}")
        op, body = sent(ucm)
        assert op == "restartH323Gateway"
        assert text(body, "uuid") == "{11111111-0000-0000-0000-000000000006}"


class TestSipTrunkLifecycle:
    def test_restart_sip_trunk_by_name(self, ucm):
        ucm.restart_sip_trunk(name="ITSP")
        op, body = sent(ucm)
        assert op == "restartSipTrunk"
        assert text(body, "name") == "ITSP"

    def test_restart_sip_trunk_by_uuid(self, ucm):
        ucm.restart_sip_trunk(uuid="{11111111-0000-0000-0000-000000000007}")
        op, body = sent(ucm)
        assert op == "restartSipTrunk"
        assert text(body, "uuid") == "{11111111-0000-0000-0000-000000000007}"

    def test_restart_sip_trunk_requires_one_identifier(self, ucm):
        with pytest.raises(ValueError):
            ucm.restart_sip_trunk()


class TestSrstLifecycle:
    def test_apply_srst(self, ucm):
        ucm.apply_srst(name="SRST1")
        op, body = sent(ucm)
        assert op == "applySrst"
        assert text(body, "name") == "SRST1"

    def test_reset_srst(self, ucm):
        ucm.reset_srst(name="SRST1")
        op, body = sent(ucm)
        assert op == "resetSrst"
        assert text(body, "name") == "SRST1"

    def test_restart_srst(self, ucm):
        ucm.restart_srst(name="SRST1")
        op, body = sent(ucm)
        assert op == "restartSrst"
        assert text(body, "name") == "SRST1"


class TestConferenceBridgeLifecycle:
    def test_apply_conference_bridge(self, ucm):
        ucm.apply_conference_bridge(name="CFB1")
        op, body = sent(ucm)
        assert op == "applyConferenceBridge"
        assert text(body, "name") == "CFB1"

    def test_reset_conference_bridge(self, ucm):
        ucm.reset_conference_bridge(name="CFB1")
        op, body = sent(ucm)
        assert op == "resetConferenceBridge"
        assert text(body, "name") == "CFB1"

    def test_restart_conference_bridge_by_uuid(self, ucm):
        ucm.restart_conference_bridge(uuid="{11111111-0000-0000-0000-000000000008}")
        op, body = sent(ucm)
        assert op == "restartConferenceBridge"
        assert text(body, "uuid") == "{11111111-0000-0000-0000-000000000008}"


class TestMtpLifecycle:
    def test_apply_mtp(self, ucm):
        ucm.apply_mtp(name="MTP1")
        op, body = sent(ucm)
        assert op == "applyMtp"
        assert text(body, "name") == "MTP1"

    def test_reset_mtp(self, ucm):
        ucm.reset_mtp(name="MTP1")
        op, body = sent(ucm)
        assert op == "resetMtp"
        assert text(body, "name") == "MTP1"

    def test_restart_mtp(self, ucm):
        ucm.restart_mtp(name="MTP1")
        op, body = sent(ucm)
        assert op == "restartMtp"
        assert text(body, "name") == "MTP1"


class TestRegionLifecycle:
    def test_apply_region(self, ucm):
        ucm.apply_region(name="Hollywood_REG")
        op, body = sent(ucm)
        assert op == "applyRegion"
        assert text(body, "name") == "Hollywood_REG"

    def test_restart_region(self, ucm):
        ucm.restart_region(name="Hollywood_REG")
        op, body = sent(ucm)
        assert op == "restartRegion"
        assert text(body, "name") == "Hollywood_REG"


class TestTranscoderLifecycle:
    def test_apply_transcoder(self, ucm):
        ucm.apply_transcoder(name="XCODE1")
        op, body = sent(ucm)
        assert op == "applyTranscoder"
        assert text(body, "name") == "XCODE1"

    def test_reset_transcoder(self, ucm):
        ucm.reset_transcoder(name="XCODE1")
        op, body = sent(ucm)
        assert op == "resetTranscoder"
        assert text(body, "name") == "XCODE1"


class TestCallManagerGroupLifecycle:
    def test_apply_call_manager_group(self, ucm):
        ucm.apply_call_manager_group(name="Default")
        op, body = sent(ucm)
        assert op == "applyCallManagerGroup"
        assert text(body, "name") == "Default"

    def test_reset_call_manager_group(self, ucm):
        ucm.reset_call_manager_group(name="Default")
        op, body = sent(ucm)
        assert op == "resetCallManagerGroup"
        assert text(body, "name") == "Default"


class TestDevicePoolLifecycle:
    def test_apply_device_pool(self, ucm):
        ucm.apply_device_pool(name="Branch_DP")
        op, body = sent(ucm)
        assert op == "applyDevicePool"
        assert text(body, "name") == "Branch_DP"

    def test_reset_device_pool(self, ucm):
        ucm.reset_device_pool(name="Branch_DP")
        op, body = sent(ucm)
        assert op == "resetDevicePool"
        assert text(body, "name") == "Branch_DP"

    def test_restart_device_pool_by_uuid(self, ucm):
        ucm.restart_device_pool(uuid="{11111111-0000-0000-0000-000000000009}")
        op, body = sent(ucm)
        assert op == "restartDevicePool"
        assert text(body, "uuid") == "{11111111-0000-0000-0000-000000000009}"

    def test_apply_device_pool_requires_one_identifier(self, ucm):
        with pytest.raises(ValueError):
            ucm.apply_device_pool()


class TestPhoneActivationCode:
    def test_add_phone_activation_code_builds_message(self, ucm):
        ucm.add_phone_activation_code(phoneName="SEP001122334455")
        op, body = sent(ucm)
        assert op == "addPhoneActivationCode"
        assert text(body, "phoneActivationCode/phoneName") == "SEP001122334455"

    def test_get_phone_activation_codes_empty_list(self, ucm):
        ucm.recorder.responses["listPhoneActivationCode"] = {"return": None}
        result = ucm.get_phone_activation_codes()
        assert result == []

    def test_get_phone_activation_codes_by_phone_name(self, ucm):
        ucm.recorder.responses["listPhoneActivationCode"] = {
            "return": {"phoneActivationCode": [{"phoneName": "SEP001122334455"}]}
        }
        result = ucm.get_phone_activation_codes(phone_name="SEP001122334455")
        assert result == [{"phoneName": "SEP001122334455"}]
        _, body = sent(ucm)
        assert text(body, "searchCriteria/phoneName") == "SEP001122334455"

    def test_get_phone_activation_codes_default_search_is_wildcard(self, ucm):
        ucm.recorder.responses["listPhoneActivationCode"] = {"return": None}
        ucm.get_phone_activation_codes()
        _, body = sent(ucm)
        assert text(body, "searchCriteria/phoneName") == "%"

    def test_delete_phone_activation_code_by_activation_code(self, ucm):
        ucm.delete_phone_activation_code(activation_code="12345678")
        op, body = sent(ucm)
        assert op == "removePhoneActivationCode"
        assert text(body, "activationCode") == "12345678"

    def test_delete_phone_activation_code_by_uuid(self, ucm):
        ucm.delete_phone_activation_code(uuid="{11111111-0000-0000-0000-000000000010}")
        op, body = sent(ucm)
        assert op == "removePhoneActivationCode"
        assert text(body, "uuid") == "{11111111-0000-0000-0000-000000000010}"

    def test_delete_phone_activation_code_requires_one_identifier(self, ucm):
        with pytest.raises(ValueError):
            ucm.delete_phone_activation_code()
        with pytest.raises(ValueError):
            ucm.delete_phone_activation_code(activation_code="x", uuid="{a}")


class TestUnassignedDevice:
    def test_get_unassigned_devices_empty_list(self, ucm):
        ucm.recorder.responses["listUnassignedDevice"] = {"return": None}
        result = ucm.get_unassigned_devices()
        assert result == []

    def test_get_unassigned_devices_returns_list(self, ucm):
        ucm.recorder.responses["listUnassignedDevice"] = {
            "return": {"unassignedDevice": [{"name": "SEP001122334455"}]}
        }
        result = ucm.get_unassigned_devices()
        assert result == [{"name": "SEP001122334455"}]

    def test_get_unassigned_devices_by_name_filter(self, ucm):
        ucm.recorder.responses["listUnassignedDevice"] = {"return": None}
        ucm.get_unassigned_devices(name="SEP%")
        _, body = sent(ucm)
        assert text(body, "searchCriteria/name") == "SEP%"

    def test_get_unassigned_devices_default_search_is_wildcard(self, ucm):
        ucm.recorder.responses["listUnassignedDevice"] = {"return": None}
        ucm.get_unassigned_devices()
        _, body = sent(ucm)
        assert text(body, "searchCriteria/name") == "%"
