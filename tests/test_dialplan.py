"""Offline request tests for ciscoaxl/dialplan.py.

Run with: pytest tests/test_dialplan.py
"""
import pytest

from test_offline_requests import make_ucm, sent, text, has


@pytest.fixture
def ucm():
    return make_ucm("15.0")


class TestAarGroup:
    def test_add_aar_group_builds_message(self, ucm):
        ucm.add_aar_group(name="TestAAR")
        op, body = sent(ucm)
        assert op == "addAarGroup"
        assert text(body, "aarGroup/name") == "TestAAR"

    def test_get_aar_groups_empty_list(self, ucm):
        ucm.recorder.responses["listAarGroup"] = {"return": None}
        assert ucm.get_aar_groups() == []

    def test_get_aar_group_unwraps(self, ucm):
        ucm.recorder.responses["getAarGroup"] = {
            "return": {"aarGroup": {"name": "TestAAR"}}
        }
        result = ucm.get_aar_group(name="TestAAR")
        assert result["name"] == "TestAAR"

    def test_delete_aar_group(self, ucm):
        ucm.delete_aar_group(name="TestAAR")
        op, body = sent(ucm)
        assert op == "removeAarGroup"
        assert text(body, "name") == "TestAAR"

    def test_delete_aar_group_by_uuid(self, ucm):
        ucm.delete_aar_group(uuid="{AAAAAAAA-0000-0000-0000-000000000001}")
        op, body = sent(ucm)
        assert op == "removeAarGroup"
        assert text(body, "uuid") == "{AAAAAAAA-0000-0000-0000-000000000001}"
        assert not has(body, "name")

    def test_update_aar_group(self, ucm):
        ucm.update_aar_group(name="TestAAR", newName="UpdatedAAR")
        op, body = sent(ucm)
        assert op == "updateAarGroup"
        assert text(body, "name") == "TestAAR"


class TestAarGroupMatrix:
    def test_update_aar_group_matrix_by_from_to(self, ucm):
        ucm.update_aar_group_matrix(
            aarGroupFromName="Group1",
            aarGroupToName="Group2",
            prefixDigit="9",
        )
        op, body = sent(ucm)
        assert op == "updateAarGroupMatrix"
        assert text(body, "aarGroupFromName") == "Group1"
        assert text(body, "aarGroupToName") == "Group2"
        assert text(body, "prefixDigit") == "9"

    def test_update_aar_group_matrix_by_uuid(self, ucm):
        ucm.update_aar_group_matrix(
            uuid="{BBBBBBBB-0000-0000-0000-000000000001}",
            prefixDigit="8",
        )
        op, body = sent(ucm)
        assert op == "updateAarGroupMatrix"
        assert text(body, "uuid") == "{BBBBBBBB-0000-0000-0000-000000000001}"


class TestApplicationDialRules:
    def test_add_application_dial_rules_builds_message(self, ucm):
        ucm.add_application_dial_rules(name="TestADR")
        op, body = sent(ucm)
        assert op == "addApplicationDialRules"
        assert text(body, "applicationDialRules/name") == "TestADR"

    def test_get_application_dial_rules_list_empty(self, ucm):
        ucm.recorder.responses["listApplicationDialRules"] = {"return": None}
        assert ucm.get_application_dial_rules_list() == []

    def test_get_application_dial_rules_unwraps(self, ucm):
        ucm.recorder.responses["getApplicationDialRules"] = {
            "return": {"applicationDialRules": {"name": "TestADR"}}
        }
        result = ucm.get_application_dial_rules(name="TestADR")
        assert result["name"] == "TestADR"

    def test_delete_application_dial_rules(self, ucm):
        ucm.delete_application_dial_rules(name="TestADR")
        op, body = sent(ucm)
        assert op == "removeApplicationDialRules"
        assert text(body, "name") == "TestADR"


class TestDirectedCallPark:
    def test_add_directed_call_park_builds_message(self, ucm):
        ucm.add_directed_call_park(pattern="7000", retrievalPrefix="*")
        op, body = sent(ucm)
        assert op == "addDirectedCallPark"
        assert text(body, "directedCallPark/pattern") == "7000"

    def test_get_directed_call_parks_empty_list(self, ucm):
        ucm.recorder.responses["listDirectedCallPark"] = {"return": None}
        assert ucm.get_directed_call_parks() == []

    def test_get_directed_call_parks_uses_pattern_search(self, ucm):
        """List search must use 'pattern', not 'name'."""
        ucm.recorder.responses["listDirectedCallPark"] = {"return": None}
        ucm.get_directed_call_parks()
        op, body = sent(ucm)
        assert op == "listDirectedCallPark"
        assert text(body, "searchCriteria/pattern") == "%"
        assert not has(body, "searchCriteria/name")

    def test_get_directed_call_park_unwraps(self, ucm):
        ucm.recorder.responses["getDirectedCallPark"] = {
            "return": {"directedCallPark": {"pattern": "7000"}}
        }
        result = ucm.get_directed_call_park(pattern="7000")
        assert result["pattern"] == "7000"

    def test_delete_directed_call_park_by_pattern(self, ucm):
        ucm.delete_directed_call_park(pattern="7000")
        op, body = sent(ucm)
        assert op == "removeDirectedCallPark"
        assert text(body, "pattern") == "7000"

    def test_delete_directed_call_park_by_uuid(self, ucm):
        ucm.delete_directed_call_park(uuid="{CCCCCCCC-0000-0000-0000-000000000001}")
        op, body = sent(ucm)
        assert op == "removeDirectedCallPark"
        assert text(body, "uuid") == "{CCCCCCCC-0000-0000-0000-000000000001}"

    def test_apply_directed_call_park(self, ucm):
        ucm.apply_directed_call_park(pattern="7000")
        op, body = sent(ucm)
        assert op == "applyDirectedCallPark"
        assert text(body, "pattern") == "7000"

    def test_reset_directed_call_park(self, ucm):
        ucm.reset_directed_call_park(pattern="7000")
        op, body = sent(ucm)
        assert op == "resetDirectedCallPark"
        assert text(body, "pattern") == "7000"


class TestDirectoryLookupDialRules:
    def test_add_directory_lookup_dial_rules_builds_message(self, ucm):
        ucm.add_directory_lookup_dial_rules(name="TestDLDR")
        op, body = sent(ucm)
        assert op == "addDirectoryLookupDialRules"
        assert text(body, "directoryLookupDialRules/name") == "TestDLDR"

    def test_get_directory_lookup_dial_rules_list_empty(self, ucm):
        ucm.recorder.responses["listDirectoryLookupDialRules"] = {"return": None}
        assert ucm.get_directory_lookup_dial_rules_list() == []

    def test_get_directory_lookup_dial_rules_unwraps(self, ucm):
        ucm.recorder.responses["getDirectoryLookupDialRules"] = {
            "return": {"directoryLookupDialRules": {"name": "TestDLDR"}}
        }
        result = ucm.get_directory_lookup_dial_rules(name="TestDLDR")
        assert result["name"] == "TestDLDR"

    def test_delete_directory_lookup_dial_rules(self, ucm):
        ucm.delete_directory_lookup_dial_rules(name="TestDLDR")
        op, body = sent(ucm)
        assert op == "removeDirectoryLookupDialRules"
        assert text(body, "name") == "TestDLDR"


class TestLocalRouteGroup:
    def test_add_local_route_group_builds_message(self, ucm):
        ucm.add_local_route_group(name="TestLRG")
        op, body = sent(ucm)
        assert op == "addLocalRouteGroup"
        assert text(body, "localRouteGroup/name") == "TestLRG"

    def test_get_local_route_groups_empty_list(self, ucm):
        ucm.recorder.responses["listLocalRouteGroup"] = {"return": None}
        assert ucm.get_local_route_groups() == []

    def test_get_local_route_group_unwraps(self, ucm):
        ucm.recorder.responses["getLocalRouteGroup"] = {
            "return": {"localRouteGroup": {"name": "TestLRG"}}
        }
        result = ucm.get_local_route_group(name="TestLRG")
        assert result["name"] == "TestLRG"

    def test_delete_local_route_group(self, ucm):
        ucm.delete_local_route_group(name="TestLRG")
        op, body = sent(ucm)
        assert op == "removeLocalRouteGroup"
        assert text(body, "name") == "TestLRG"

    def test_update_local_route_group(self, ucm):
        # UpdateLocalRouteGroupReq wraps everything in a 'localRouteGroup' sub-element.
        # The schema (unusual) lists uuid AND name as required; real CUCM accepts either.
        ucm.update_local_route_group(
            localRouteGroup={
                "uuid": "{EEEEEEEE-0000-0000-0000-000000000001}",
                "name": "TestLRG",
                "newName": "UpdatedLRG",
            }
        )
        op, body = sent(ucm)
        assert op == "updateLocalRouteGroup"
        assert text(body, "localRouteGroup/newName") == "UpdatedLRG"


class TestRouteFilter:
    def test_add_route_filter_builds_message(self, ucm):
        # RouteFilter requires name, dialPlanName, and members (all minOccurs=1)
        ucm.add_route_filter(
            name="TestRF",
            dialPlanName="DefaultDialPlan",
            members={},
        )
        op, body = sent(ucm)
        assert op == "addRouteFilter"
        assert text(body, "routeFilter/name") == "TestRF"
        assert text(body, "routeFilter/dialPlanName") == "DefaultDialPlan"

    def test_get_route_filters_empty_list(self, ucm):
        ucm.recorder.responses["listRouteFilter"] = {"return": None}
        assert ucm.get_route_filters() == []

    def test_get_route_filter_unwraps(self, ucm):
        ucm.recorder.responses["getRouteFilter"] = {
            "return": {"routeFilter": {"name": "TestRF"}}
        }
        result = ucm.get_route_filter(name="TestRF")
        assert result["name"] == "TestRF"

    def test_delete_route_filter(self, ucm):
        ucm.delete_route_filter(name="TestRF")
        op, body = sent(ucm)
        assert op == "removeRouteFilter"
        assert text(body, "name") == "TestRF"

    def test_update_route_filter(self, ucm):
        ucm.update_route_filter(name="TestRF", newName="UpdatedRF")
        op, body = sent(ucm)
        assert op == "updateRouteFilter"
        assert text(body, "name") == "TestRF"


class TestSipDialRules:
    def test_add_sip_dial_rules_builds_message(self, ucm):
        ucm.add_sip_dial_rules(name="TestSDR")
        op, body = sent(ucm)
        assert op == "addSipDialRules"
        assert text(body, "sipDialRules/name") == "TestSDR"

    def test_get_sip_dial_rules_list_empty(self, ucm):
        ucm.recorder.responses["listSipDialRules"] = {"return": None}
        assert ucm.get_sip_dial_rules_list() == []

    def test_get_sip_dial_rules_unwraps(self, ucm):
        ucm.recorder.responses["getSipDialRules"] = {
            "return": {"sipDialRules": {"name": "TestSDR"}}
        }
        result = ucm.get_sip_dial_rules(name="TestSDR")
        assert result["name"] == "TestSDR"

    def test_delete_sip_dial_rules(self, ucm):
        ucm.delete_sip_dial_rules(name="TestSDR")
        op, body = sent(ucm)
        assert op == "removeSipDialRules"
        assert text(body, "name") == "TestSDR"


class TestSipRoutePattern:
    def test_add_sip_route_pattern_builds_message(self, ucm):
        # SipRoutePattern requires pattern, usage, routePartitionName, sipTrunkName
        ucm.add_sip_route_pattern(
            pattern="*.sip.example.com",
            usage="Domain Routing",
            routePartitionName="PSTN_PT",
            sipTrunkName="ITSP_SIPTrunk",
        )
        op, body = sent(ucm)
        assert op == "addSipRoutePattern"
        assert text(body, "sipRoutePattern/pattern") == "*.sip.example.com"
        assert text(body, "sipRoutePattern/sipTrunkName") == "ITSP_SIPTrunk"

    def test_get_sip_route_patterns_empty_list(self, ucm):
        ucm.recorder.responses["listSipRoutePattern"] = {"return": None}
        assert ucm.get_sip_route_patterns() == []

    def test_get_sip_route_patterns_uses_pattern_search(self, ucm):
        """List search must use 'pattern', not 'name'."""
        ucm.recorder.responses["listSipRoutePattern"] = {"return": None}
        ucm.get_sip_route_patterns()
        op, body = sent(ucm)
        assert op == "listSipRoutePattern"
        assert text(body, "searchCriteria/pattern") == "%"
        assert not has(body, "searchCriteria/name")

    def test_get_sip_route_pattern_unwraps(self, ucm):
        ucm.recorder.responses["getSipRoutePattern"] = {
            "return": {
                "sipRoutePattern": {
                    "pattern": "*.sip.example.com",
                    "routePartitionName": "PSTN_PT",
                }
            }
        }
        result = ucm.get_sip_route_pattern(
            pattern="*.sip.example.com", routePartitionName="PSTN_PT"
        )
        assert result["pattern"] == "*.sip.example.com"

    def test_delete_sip_route_pattern_by_pattern_and_partition(self, ucm):
        ucm.delete_sip_route_pattern(
            pattern="*.sip.example.com", routePartitionName="PSTN_PT"
        )
        op, body = sent(ucm)
        assert op == "removeSipRoutePattern"
        assert text(body, "pattern") == "*.sip.example.com"
        assert text(body, "routePartitionName") == "PSTN_PT"

    def test_delete_sip_route_pattern_by_uuid(self, ucm):
        ucm.delete_sip_route_pattern(uuid="{DDDDDDDD-0000-0000-0000-000000000001}")
        op, body = sent(ucm)
        assert op == "removeSipRoutePattern"
        assert text(body, "uuid") == "{DDDDDDDD-0000-0000-0000-000000000001}"

    def test_update_sip_route_pattern(self, ucm):
        ucm.update_sip_route_pattern(
            pattern="*.sip.example.com",
            routePartitionName="PSTN_PT",
            newPattern="*.sip.new.com",
        )
        op, body = sent(ucm)
        assert op == "updateSipRoutePattern"
        assert text(body, "pattern") == "*.sip.example.com"
