"""Offline request tests for ciscoaxl/ime.py.

Run with: pytest tests/test_ime.py
"""
import pytest

from test_offline_requests import make_ucm, sent, text, has


@pytest.fixture
def ucm():
    return make_ucm("15.0")


class TestImeServer:
    def test_add_ime_server(self, ucm):
        ucm.add_ime_server(
            name="IMEServer01",
            ipAddress="10.0.0.1",
            applicationUser="imeappuser",
        )
        op, body = sent(ucm)
        assert op == "addImeServer"
        assert text(body, "imeServer/name") == "IMEServer01"
        assert text(body, "imeServer/ipAddress") == "10.0.0.1"

    def test_get_ime_server_by_name(self, ucm):
        ucm.recorder.responses["getImeServer"] = {
            "return": {"imeServer": {"name": "IMEServer01"}}
        }
        result = ucm.get_ime_server(name="IMEServer01")
        op, body = sent(ucm)
        assert op == "getImeServer"
        assert text(body, "name") == "IMEServer01"
        assert result == {"name": "IMEServer01"}

    def test_get_ime_server_by_uuid(self, ucm):
        ucm.recorder.responses["getImeServer"] = {
            "return": {"imeServer": {"name": "IMEServer01"}}
        }
        ucm.get_ime_server(uuid="{AAAA-1111}")
        op, body = sent(ucm)
        assert op == "getImeServer"
        assert text(body, "uuid") == "{AAAA-1111}"
        assert not has(body, "name")

    def test_get_ime_servers(self, ucm):
        ucm.recorder.responses["listImeServer"] = {
            "return": {"imeServer": [{"name": "IMEServer01"}]}
        }
        result = ucm.get_ime_servers()
        op, body = sent(ucm)
        assert op == "listImeServer"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_ime_servers_empty(self, ucm):
        ucm.recorder.responses["listImeServer"] = {"return": None}
        result = ucm.get_ime_servers()
        assert result == []

    def test_update_ime_server(self, ucm):
        ucm.update_ime_server(name="IMEServer01", description="Updated")
        op, body = sent(ucm)
        assert op == "updateImeServer"
        assert text(body, "name") == "IMEServer01"

    def test_delete_ime_server_by_name(self, ucm):
        ucm.delete_ime_server(name="IMEServer01")
        op, body = sent(ucm)
        assert op == "removeImeServer"
        assert text(body, "name") == "IMEServer01"

    def test_delete_ime_server_by_uuid(self, ucm):
        ucm.delete_ime_server(uuid="{AAAA-1111}")
        op, body = sent(ucm)
        assert op == "removeImeServer"
        assert text(body, "uuid") == "{AAAA-1111}"


class TestImeRouteFilterGroup:
    def test_add_ime_route_filter_group(self, ucm):
        ucm.add_ime_route_filter_group(name="IMEFilterGroup01")
        op, body = sent(ucm)
        assert op == "addImeRouteFilterGroup"
        assert text(body, "imeRouteFilterGroup/name") == "IMEFilterGroup01"

    def test_get_ime_route_filter_group_by_name(self, ucm):
        ucm.recorder.responses["getImeRouteFilterGroup"] = {
            "return": {"imeRouteFilterGroup": {"name": "IMEFilterGroup01"}}
        }
        result = ucm.get_ime_route_filter_group(name="IMEFilterGroup01")
        op, body = sent(ucm)
        assert op == "getImeRouteFilterGroup"
        assert result == {"name": "IMEFilterGroup01"}

    def test_get_ime_route_filter_groups(self, ucm):
        ucm.recorder.responses["listImeRouteFilterGroup"] = {
            "return": {"imeRouteFilterGroup": [{"name": "IMEFilterGroup01"}]}
        }
        result = ucm.get_ime_route_filter_groups()
        op, body = sent(ucm)
        assert op == "listImeRouteFilterGroup"
        assert isinstance(result, list)

    def test_get_ime_route_filter_groups_empty(self, ucm):
        ucm.recorder.responses["listImeRouteFilterGroup"] = {"return": None}
        result = ucm.get_ime_route_filter_groups()
        assert result == []

    def test_update_ime_route_filter_group(self, ucm):
        ucm.update_ime_route_filter_group(name="IMEFilterGroup01", description="Updated")
        op, body = sent(ucm)
        assert op == "updateImeRouteFilterGroup"

    def test_delete_ime_route_filter_group(self, ucm):
        ucm.delete_ime_route_filter_group(name="IMEFilterGroup01")
        op, body = sent(ucm)
        assert op == "removeImeRouteFilterGroup"
        assert text(body, "name") == "IMEFilterGroup01"


class TestImeRouteFilterElement:
    def test_add_ime_route_filter_element(self, ucm):
        ucm.add_ime_route_filter_element(
            name="IMEFilterElem01",
            imeRouteFilterGroupName="IMEFilterGroup01",
        )
        op, body = sent(ucm)
        assert op == "addImeRouteFilterElement"
        assert text(body, "imeRouteFilterElement/name") == "IMEFilterElem01"

    def test_get_ime_route_filter_element_by_name(self, ucm):
        ucm.recorder.responses["getImeRouteFilterElement"] = {
            "return": {"imeRouteFilterElement": {"name": "IMEFilterElem01"}}
        }
        result = ucm.get_ime_route_filter_element(name="IMEFilterElem01")
        op, body = sent(ucm)
        assert op == "getImeRouteFilterElement"
        assert result == {"name": "IMEFilterElem01"}

    def test_get_ime_route_filter_elements(self, ucm):
        ucm.recorder.responses["listImeRouteFilterElement"] = {
            "return": {"imeRouteFilterElement": [{"name": "IMEFilterElem01"}]}
        }
        result = ucm.get_ime_route_filter_elements()
        op, body = sent(ucm)
        assert op == "listImeRouteFilterElement"
        assert isinstance(result, list)

    def test_get_ime_route_filter_elements_empty(self, ucm):
        ucm.recorder.responses["listImeRouteFilterElement"] = {"return": None}
        result = ucm.get_ime_route_filter_elements()
        assert result == []

    def test_update_ime_route_filter_element(self, ucm):
        ucm.update_ime_route_filter_element(name="IMEFilterElem01", description="Updated")
        op, body = sent(ucm)
        assert op == "updateImeRouteFilterElement"

    def test_delete_ime_route_filter_element(self, ucm):
        ucm.delete_ime_route_filter_element(name="IMEFilterElem01")
        op, body = sent(ucm)
        assert op == "removeImeRouteFilterElement"
        assert text(body, "name") == "IMEFilterElem01"


class TestImeClient:
    def test_add_ime_client(self, ucm):
        ucm.add_ime_client(
            name="IMEClient01",
            domain="example.com",
            sipTrunkName="SIPTrunk01",
            primaryImeServerName="IMEServer01",
        )
        op, body = sent(ucm)
        assert op == "addImeClient"
        assert text(body, "imeClient/name") == "IMEClient01"
        assert text(body, "imeClient/domain") == "example.com"

    def test_get_ime_client_by_name(self, ucm):
        ucm.recorder.responses["getImeClient"] = {
            "return": {"imeClient": {"name": "IMEClient01"}}
        }
        result = ucm.get_ime_client(name="IMEClient01")
        op, body = sent(ucm)
        assert op == "getImeClient"
        assert text(body, "name") == "IMEClient01"
        assert result == {"name": "IMEClient01"}

    def test_get_ime_client_by_uuid(self, ucm):
        ucm.recorder.responses["getImeClient"] = {
            "return": {"imeClient": {"name": "IMEClient01"}}
        }
        ucm.get_ime_client(uuid="{BBBB-2222}")
        op, body = sent(ucm)
        assert op == "getImeClient"
        assert text(body, "uuid") == "{BBBB-2222}"
        assert not has(body, "name")

    def test_get_ime_clients(self, ucm):
        ucm.recorder.responses["listImeClient"] = {
            "return": {"imeClient": [{"name": "IMEClient01"}]}
        }
        result = ucm.get_ime_clients()
        op, body = sent(ucm)
        assert op == "listImeClient"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_ime_clients_empty(self, ucm):
        ucm.recorder.responses["listImeClient"] = {"return": None}
        result = ucm.get_ime_clients()
        assert result == []

    def test_update_ime_client(self, ucm):
        ucm.update_ime_client(name="IMEClient01", description="Updated")
        op, body = sent(ucm)
        assert op == "updateImeClient"
        assert text(body, "name") == "IMEClient01"

    def test_delete_ime_client(self, ucm):
        ucm.delete_ime_client(name="IMEClient01")
        op, body = sent(ucm)
        assert op == "removeImeClient"
        assert text(body, "name") == "IMEClient01"


class TestImeEnrolledPattern:
    def test_add_ime_enrolled_pattern(self, ucm):
        ucm.add_ime_enrolled_pattern(pattern="+15551234")
        op, body = sent(ucm)
        assert op == "addImeEnrolledPattern"
        assert text(body, "imeEnrolledPattern/pattern") == "+15551234"

    def test_get_ime_enrolled_pattern_by_pattern(self, ucm):
        ucm.recorder.responses["getImeEnrolledPattern"] = {
            "return": {"imeEnrolledPattern": {"pattern": "+15551234"}}
        }
        result = ucm.get_ime_enrolled_pattern(pattern="+15551234")
        op, body = sent(ucm)
        assert op == "getImeEnrolledPattern"
        assert text(body, "pattern") == "+15551234"
        assert result == {"pattern": "+15551234"}

    def test_get_ime_enrolled_pattern_by_uuid(self, ucm):
        ucm.recorder.responses["getImeEnrolledPattern"] = {
            "return": {"imeEnrolledPattern": {"pattern": "+15551234"}}
        }
        ucm.get_ime_enrolled_pattern(uuid="{CCCC-3333}")
        op, body = sent(ucm)
        assert op == "getImeEnrolledPattern"
        assert text(body, "uuid") == "{CCCC-3333}"
        assert not has(body, "pattern")

    def test_get_ime_enrolled_pattern_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_ime_enrolled_pattern()

    def test_get_ime_enrolled_patterns(self, ucm):
        ucm.recorder.responses["listImeEnrolledPattern"] = {
            "return": {"imeEnrolledPattern": [{"pattern": "+15551234"}]}
        }
        result = ucm.get_ime_enrolled_patterns()
        op, body = sent(ucm)
        assert op == "listImeEnrolledPattern"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_ime_enrolled_patterns_empty(self, ucm):
        ucm.recorder.responses["listImeEnrolledPattern"] = {"return": None}
        result = ucm.get_ime_enrolled_patterns()
        assert result == []

    def test_update_ime_enrolled_pattern(self, ucm):
        ucm.update_ime_enrolled_pattern(pattern="+15551234", description="Updated")
        op, body = sent(ucm)
        assert op == "updateImeEnrolledPattern"

    def test_delete_ime_enrolled_pattern_by_pattern(self, ucm):
        ucm.delete_ime_enrolled_pattern(pattern="+15551234")
        op, body = sent(ucm)
        assert op == "removeImeEnrolledPattern"
        assert text(body, "pattern") == "+15551234"

    def test_delete_ime_enrolled_pattern_by_uuid(self, ucm):
        ucm.delete_ime_enrolled_pattern(uuid="{CCCC-3333}")
        op, body = sent(ucm)
        assert op == "removeImeEnrolledPattern"
        assert text(body, "uuid") == "{CCCC-3333}"

    def test_delete_ime_enrolled_pattern_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.delete_ime_enrolled_pattern()


class TestImeEnrolledPatternGroup:
    def test_add_ime_enrolled_pattern_group(self, ucm):
        ucm.add_ime_enrolled_pattern_group(name="IMEPatternGroup01")
        op, body = sent(ucm)
        assert op == "addImeEnrolledPatternGroup"
        assert text(body, "imeEnrolledPatternGroup/name") == "IMEPatternGroup01"

    def test_get_ime_enrolled_pattern_group_by_name(self, ucm):
        ucm.recorder.responses["getImeEnrolledPatternGroup"] = {
            "return": {"imeEnrolledPatternGroup": {"name": "IMEPatternGroup01"}}
        }
        result = ucm.get_ime_enrolled_pattern_group(name="IMEPatternGroup01")
        op, body = sent(ucm)
        assert op == "getImeEnrolledPatternGroup"
        assert result == {"name": "IMEPatternGroup01"}

    def test_get_ime_enrolled_pattern_groups(self, ucm):
        ucm.recorder.responses["listImeEnrolledPatternGroup"] = {
            "return": {"imeEnrolledPatternGroup": [{"name": "IMEPatternGroup01"}]}
        }
        result = ucm.get_ime_enrolled_pattern_groups()
        op, body = sent(ucm)
        assert op == "listImeEnrolledPatternGroup"
        assert isinstance(result, list)

    def test_get_ime_enrolled_pattern_groups_empty(self, ucm):
        ucm.recorder.responses["listImeEnrolledPatternGroup"] = {"return": None}
        result = ucm.get_ime_enrolled_pattern_groups()
        assert result == []

    def test_update_ime_enrolled_pattern_group(self, ucm):
        ucm.update_ime_enrolled_pattern_group(name="IMEPatternGroup01", description="Updated")
        op, body = sent(ucm)
        assert op == "updateImeEnrolledPatternGroup"

    def test_delete_ime_enrolled_pattern_group(self, ucm):
        ucm.delete_ime_enrolled_pattern_group(name="IMEPatternGroup01")
        op, body = sent(ucm)
        assert op == "removeImeEnrolledPatternGroup"
        assert text(body, "name") == "IMEPatternGroup01"


class TestImeExclusionNumber:
    def test_add_ime_exclusion_number(self, ucm):
        ucm.add_ime_exclusion_number(
            pattern="+15559999",
            imeExclusionNumberGroupName="IMEExclGroup01",
        )
        op, body = sent(ucm)
        assert op == "addImeExclusionNumber"
        assert text(body, "imeExclusionNumber/pattern") == "+15559999"

    def test_get_ime_exclusion_number_by_pattern(self, ucm):
        ucm.recorder.responses["getImeExclusionNumber"] = {
            "return": {"imeExclusionNumber": {"pattern": "+15559999"}}
        }
        result = ucm.get_ime_exclusion_number(pattern="+15559999")
        op, body = sent(ucm)
        assert op == "getImeExclusionNumber"
        assert text(body, "pattern") == "+15559999"
        assert result == {"pattern": "+15559999"}

    def test_get_ime_exclusion_number_by_uuid(self, ucm):
        ucm.recorder.responses["getImeExclusionNumber"] = {
            "return": {"imeExclusionNumber": {"pattern": "+15559999"}}
        }
        ucm.get_ime_exclusion_number(uuid="{DDDD-4444}")
        op, body = sent(ucm)
        assert op == "getImeExclusionNumber"
        assert text(body, "uuid") == "{DDDD-4444}"
        assert not has(body, "pattern")

    def test_get_ime_exclusion_number_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_ime_exclusion_number()

    def test_get_ime_exclusion_numbers(self, ucm):
        ucm.recorder.responses["listImeExclusionNumber"] = {
            "return": {"imeExclusionNumber": [{"pattern": "+15559999"}]}
        }
        result = ucm.get_ime_exclusion_numbers()
        op, body = sent(ucm)
        assert op == "listImeExclusionNumber"
        assert isinstance(result, list)

    def test_get_ime_exclusion_numbers_empty(self, ucm):
        ucm.recorder.responses["listImeExclusionNumber"] = {"return": None}
        result = ucm.get_ime_exclusion_numbers()
        assert result == []

    def test_update_ime_exclusion_number(self, ucm):
        ucm.update_ime_exclusion_number(pattern="+15559999", description="Updated")
        op, body = sent(ucm)
        assert op == "updateImeExclusionNumber"

    def test_delete_ime_exclusion_number_by_pattern(self, ucm):
        ucm.delete_ime_exclusion_number(pattern="+15559999")
        op, body = sent(ucm)
        assert op == "removeImeExclusionNumber"
        assert text(body, "pattern") == "+15559999"

    def test_delete_ime_exclusion_number_by_uuid(self, ucm):
        ucm.delete_ime_exclusion_number(uuid="{DDDD-4444}")
        op, body = sent(ucm)
        assert op == "removeImeExclusionNumber"
        assert text(body, "uuid") == "{DDDD-4444}"

    def test_delete_ime_exclusion_number_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.delete_ime_exclusion_number()


class TestImeExclusionNumberGroup:
    def test_add_ime_exclusion_number_group(self, ucm):
        ucm.add_ime_exclusion_number_group(name="IMEExclGroup01")
        op, body = sent(ucm)
        assert op == "addImeExclusionNumberGroup"
        assert text(body, "imeExclusionNumberGroup/name") == "IMEExclGroup01"

    def test_get_ime_exclusion_number_group_by_name(self, ucm):
        ucm.recorder.responses["getImeExclusionNumberGroup"] = {
            "return": {"imeExclusionNumberGroup": {"name": "IMEExclGroup01"}}
        }
        result = ucm.get_ime_exclusion_number_group(name="IMEExclGroup01")
        op, body = sent(ucm)
        assert op == "getImeExclusionNumberGroup"
        assert result == {"name": "IMEExclGroup01"}

    def test_get_ime_exclusion_number_groups(self, ucm):
        ucm.recorder.responses["listImeExclusionNumberGroup"] = {
            "return": {"imeExclusionNumberGroup": [{"name": "IMEExclGroup01"}]}
        }
        result = ucm.get_ime_exclusion_number_groups()
        op, body = sent(ucm)
        assert op == "listImeExclusionNumberGroup"
        assert isinstance(result, list)

    def test_get_ime_exclusion_number_groups_empty(self, ucm):
        ucm.recorder.responses["listImeExclusionNumberGroup"] = {"return": None}
        result = ucm.get_ime_exclusion_number_groups()
        assert result == []

    def test_update_ime_exclusion_number_group(self, ucm):
        ucm.update_ime_exclusion_number_group(name="IMEExclGroup01", description="Updated")
        op, body = sent(ucm)
        assert op == "updateImeExclusionNumberGroup"

    def test_delete_ime_exclusion_number_group(self, ucm):
        ucm.delete_ime_exclusion_number_group(name="IMEExclGroup01")
        op, body = sent(ucm)
        assert op == "removeImeExclusionNumberGroup"
        assert text(body, "name") == "IMEExclGroup01"


class TestImeFirewall:
    def test_add_ime_firewall(self, ucm):
        ucm.add_ime_firewall(name="IMEFirewall01", ipAddress="192.168.1.1")
        op, body = sent(ucm)
        assert op == "addImeFirewall"
        assert text(body, "imeFirewall/name") == "IMEFirewall01"
        assert text(body, "imeFirewall/ipAddress") == "192.168.1.1"

    def test_get_ime_firewall_by_name(self, ucm):
        ucm.recorder.responses["getImeFirewall"] = {
            "return": {"imeFirewall": {"name": "IMEFirewall01"}}
        }
        result = ucm.get_ime_firewall(name="IMEFirewall01")
        op, body = sent(ucm)
        assert op == "getImeFirewall"
        assert result == {"name": "IMEFirewall01"}

    def test_get_ime_firewalls(self, ucm):
        ucm.recorder.responses["listImeFirewall"] = {
            "return": {"imeFirewall": [{"name": "IMEFirewall01"}]}
        }
        result = ucm.get_ime_firewalls()
        op, body = sent(ucm)
        assert op == "listImeFirewall"
        assert isinstance(result, list)

    def test_get_ime_firewalls_empty(self, ucm):
        ucm.recorder.responses["listImeFirewall"] = {"return": None}
        result = ucm.get_ime_firewalls()
        assert result == []

    def test_update_ime_firewall(self, ucm):
        ucm.update_ime_firewall(name="IMEFirewall01", description="Updated")
        op, body = sent(ucm)
        assert op == "updateImeFirewall"

    def test_delete_ime_firewall(self, ucm):
        ucm.delete_ime_firewall(name="IMEFirewall01")
        op, body = sent(ucm)
        assert op == "removeImeFirewall"
        assert text(body, "name") == "IMEFirewall01"


class TestImeE164Transformation:
    def test_add_ime_e164_transformation(self, ucm):
        ucm.add_ime_e164_transformation(name="IMEE164Transform01")
        op, body = sent(ucm)
        assert op == "addImeE164Transformation"
        assert text(body, "imeE164Transformation/name") == "IMEE164Transform01"

    def test_get_ime_e164_transformation_by_name(self, ucm):
        ucm.recorder.responses["getImeE164Transformation"] = {
            "return": {"imeE164Transformation": {"name": "IMEE164Transform01"}}
        }
        result = ucm.get_ime_e164_transformation(name="IMEE164Transform01")
        op, body = sent(ucm)
        assert op == "getImeE164Transformation"
        assert result == {"name": "IMEE164Transform01"}

    def test_get_ime_e164_transformations(self, ucm):
        ucm.recorder.responses["listImeE164Transformation"] = {
            "return": {"imeE164Transformation": [{"name": "IMEE164Transform01"}]}
        }
        result = ucm.get_ime_e164_transformations()
        op, body = sent(ucm)
        assert op == "listImeE164Transformation"
        assert isinstance(result, list)

    def test_get_ime_e164_transformations_empty(self, ucm):
        ucm.recorder.responses["listImeE164Transformation"] = {"return": None}
        result = ucm.get_ime_e164_transformations()
        assert result == []

    def test_update_ime_e164_transformation(self, ucm):
        ucm.update_ime_e164_transformation(name="IMEE164Transform01", description="Updated")
        op, body = sent(ucm)
        assert op == "updateImeE164Transformation"

    def test_delete_ime_e164_transformation(self, ucm):
        ucm.delete_ime_e164_transformation(name="IMEE164Transform01")
        op, body = sent(ucm)
        assert op == "removeImeE164Transformation"
        assert text(body, "name") == "IMEE164Transform01"


class TestImeFeatureConfig:
    def test_get_ime_feature_config(self, ucm):
        ucm.recorder.responses["getImeFeatureConfig"] = {
            "return": {"imeFeatureConfig": {"useImeForOutboundCalls": True}}
        }
        result = ucm.get_ime_feature_config()
        op, body = sent(ucm)
        assert op == "getImeFeatureConfig"
        assert result == {"useImeForOutboundCalls": True}

    def test_update_ime_feature_config(self, ucm):
        ucm.update_ime_feature_config(useImeForOutboundCalls=True, trunkConnectionTimer=120)
        op, body = sent(ucm)
        assert op == "updateImeFeatureConfig"
        assert text(body, "useImeForOutboundCalls") in ("true", "1", "True", True)
        assert text(body, "trunkConnectionTimer") == "120"


class TestImeLearnedRoutes:
    def test_get_ime_learned_routes_by_e164did(self, ucm):
        ucm.recorder.responses["getImeLearnedRoutes"] = {
            "return": {"imeLearnedRoutes": {"e164Did": "+14085551234"}}
        }
        result = ucm.get_ime_learned_routes(e164Did="+14085551234")
        op, body = sent(ucm)
        assert op == "getImeLearnedRoutes"
        assert text(body, "e164Did") == "+14085551234"
        assert result == {"e164Did": "+14085551234"}

    def test_get_ime_learned_routes_by_uuid(self, ucm):
        ucm.recorder.responses["getImeLearnedRoutes"] = {
            "return": {"imeLearnedRoutes": {"e164Did": "+14085551234"}}
        }
        ucm.get_ime_learned_routes(uuid="{EEEE-5555}")
        op, body = sent(ucm)
        assert op == "getImeLearnedRoutes"
        assert text(body, "uuid") == "{EEEE-5555}"
        assert not has(body, "e164Did")

    def test_get_ime_learned_routes_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_ime_learned_routes()

    def test_update_ime_learned_routes(self, ucm):
        ucm.update_ime_learned_routes(e164Did="+14085551234", adminEnabled=True)
        op, body = sent(ucm)
        assert op == "updateImeLearnedRoutes"
        assert text(body, "e164Did") == "+14085551234"

    def test_delete_ime_learned_routes_by_e164did(self, ucm):
        ucm.delete_ime_learned_routes(e164Did="+14085551234")
        op, body = sent(ucm)
        assert op == "removeImeLearnedRoutes"
        assert text(body, "e164Did") == "+14085551234"

    def test_delete_ime_learned_routes_by_uuid(self, ucm):
        ucm.delete_ime_learned_routes(uuid="{EEEE-5555}")
        op, body = sent(ucm)
        assert op == "removeImeLearnedRoutes"
        assert text(body, "uuid") == "{EEEE-5555}"

    def test_delete_ime_learned_routes_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.delete_ime_learned_routes()
