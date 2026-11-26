"""Offline tests for P3 Batch B4 — p3_legacy_gw.py

Verifies that every method in P3LegacyGw:
  * calls the correct AXL operation
  * passes the right element names and values
  * handles name/uuid routing via _identify (Catalyst/Gatekeeper/H323Phone/BRI)
  * handles domainName/uuid routing via _identify_domain (Vg224)
  * returns the unwrapped result
  * returns [] on empty list responses

Run with: pytest tests/test_p3_b4_legacy_gw.py
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
# Shared test infrastructure (mirrors other offline test modules)
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


class SimpleRecorder:
    """Lightweight recorder (no SOAP serialization) for complex nested objects."""

    def __init__(self, zeep_client, service):
        self._zeep = zeep_client
        self._real = service
        self._binding = service._binding
        self.calls = []
        self.responses = {}

    def __getattr__(self, op_name):
        def call(*args, **kwargs):
            self.calls.append((op_name, kwargs))
            response = self.responses.get(op_name, AutoDict())
            if isinstance(response, Exception):
                raise response
            return response

        return call


def make_ucm_simple(version="15.0"):
    if version not in _clients:
        wsdl = (SCHEMA_DIR / version / "AXLAPI.wsdl").as_uri()
        settings = Settings(
            strict=False, xml_huge_tree=True, xsd_ignore_sequence_order=True
        )
        _clients[version] = Client(wsdl, settings=settings)
    zeep_client = _clients[version]
    service = zeep_client.create_service(BINDING, "https://cucm.invalid:8443/axl/")
    recorder = SimpleRecorder(zeep_client, service)
    u = axl.__new__(axl)
    u._zeep = zeep_client
    u.cucm = "cucm.invalid"
    u.cucm_version = version
    u.client = AliasingService(zeep_client, recorder)
    u.recorder = recorder
    return u


def simple_sent(ucm, index=-1):
    return ucm.recorder.calls[index]


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
    u = axl.__new__(axl)
    u._zeep = zeep_client
    u.cucm = "cucm.invalid"
    u.cucm_version = version
    u.client = AliasingService(zeep_client, recorder)
    u.recorder = recorder
    return u


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
# CiscoCatalyst600024PortFXSGateway
# ---------------------------------------------------------------------------

class TestCiscoCatalyst600024PortFXSGateway:
    def test_add(self):
        u = make_ucm_simple()
        u.add_cisco_catalyst600024_port_fxs_gateway(name="CAT-FXS-01")
        op, kwargs = simple_sent(u)
        assert op == "addCiscoCatalyst600024PortFXSGateway"
        assert "ciscoCatalyst600024PortFXSGateway" in kwargs

    def test_get_by_name(self, ucm):
        ucm.recorder.responses["getCiscoCatalyst600024PortFXSGateway"] = {
            "return": {"ciscoCatalyst600024PortFXSGateway": {"name": "CAT-FXS-01"}}
        }
        result = ucm.get_cisco_catalyst600024_port_fxs_gateway(name="CAT-FXS-01")
        op, body = sent(ucm)
        assert op == "getCiscoCatalyst600024PortFXSGateway"
        assert text(body, "name") == "CAT-FXS-01"
        assert result == {"name": "CAT-FXS-01"}

    def test_get_by_uuid(self, ucm):
        ucm.recorder.responses["getCiscoCatalyst600024PortFXSGateway"] = {
            "return": {"ciscoCatalyst600024PortFXSGateway": {"uuid": "{1111}"}}
        }
        ucm.get_cisco_catalyst600024_port_fxs_gateway(uuid="{1111}")
        op, body = sent(ucm)
        assert text(body, "uuid") == "{1111}"
        assert not has(body, "name")

    def test_get_requires_exactly_one_id(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_cisco_catalyst600024_port_fxs_gateway()
        with pytest.raises(ValueError):
            ucm.get_cisco_catalyst600024_port_fxs_gateway(name="x", uuid="y")

    def test_list(self, ucm):
        ucm.recorder.responses["listCiscoCatalyst600024PortFXSGateway"] = {
            "return": {"ciscoCatalyst600024PortFXSGateway": [{"name": "CAT-FXS-01"}]}
        }
        result = ucm.get_cisco_catalyst600024_port_fxs_gateways()
        op, body = sent(ucm)
        assert op == "listCiscoCatalyst600024PortFXSGateway"
        assert len(result) == 1

    def test_list_empty(self, ucm):
        ucm.recorder.responses["listCiscoCatalyst600024PortFXSGateway"] = {"return": None}
        assert ucm.get_cisco_catalyst600024_port_fxs_gateways() == []

    def test_update(self, ucm):
        ucm.update_cisco_catalyst600024_port_fxs_gateway(name="CAT-FXS-01", description="x")
        op, body = sent(ucm)
        assert op == "updateCiscoCatalyst600024PortFXSGateway"
        assert text(body, "name") == "CAT-FXS-01"

    def test_remove(self, ucm):
        ucm.remove_cisco_catalyst600024_port_fxs_gateway(name="CAT-FXS-01")
        op, body = sent(ucm)
        assert op == "removeCiscoCatalyst600024PortFXSGateway"
        assert text(body, "name") == "CAT-FXS-01"

    def test_remove_by_uuid(self, ucm):
        ucm.remove_cisco_catalyst600024_port_fxs_gateway(uuid="{2222}")
        op, body = sent(ucm)
        assert text(body, "uuid") == "{2222}"
        assert not has(body, "name")

    def test_apply(self, ucm):
        ucm.apply_cisco_catalyst600024_port_fxs_gateway(name="CAT-FXS-01")
        op, body = sent(ucm)
        assert op == "applyCiscoCatalyst600024PortFXSGateway"
        assert text(body, "name") == "CAT-FXS-01"

    def test_reset(self, ucm):
        ucm.reset_cisco_catalyst600024_port_fxs_gateway(name="CAT-FXS-01")
        op, body = sent(ucm)
        assert op == "resetCiscoCatalyst600024PortFXSGateway"
        assert text(body, "name") == "CAT-FXS-01"

    def test_restart(self, ucm):
        ucm.restart_cisco_catalyst600024_port_fxs_gateway(name="CAT-FXS-01")
        op, body = sent(ucm)
        assert op == "restartCiscoCatalyst600024PortFXSGateway"
        assert text(body, "name") == "CAT-FXS-01"


# ---------------------------------------------------------------------------
# CiscoCatalyst6000E1VoIPGateway
# ---------------------------------------------------------------------------

class TestCiscoCatalyst6000E1VoIPGateway:
    def test_add(self):
        u = make_ucm_simple()
        u.add_cisco_catalyst6000_e1_voip_gateway(name="CAT-E1-01")
        op, kwargs = simple_sent(u)
        assert op == "addCiscoCatalyst6000E1VoIPGateway"
        assert "ciscoCatalyst6000E1VoIPGateway" in kwargs

    def test_get_by_name(self, ucm):
        ucm.recorder.responses["getCiscoCatalyst6000E1VoIPGateway"] = {
            "return": {"ciscoCatalyst6000E1VoIPGateway": {"name": "CAT-E1-01"}}
        }
        result = ucm.get_cisco_catalyst6000_e1_voip_gateway(name="CAT-E1-01")
        op, body = sent(ucm)
        assert op == "getCiscoCatalyst6000E1VoIPGateway"
        assert text(body, "name") == "CAT-E1-01"
        assert result == {"name": "CAT-E1-01"}

    def test_get_by_uuid(self, ucm):
        ucm.recorder.responses["getCiscoCatalyst6000E1VoIPGateway"] = {
            "return": {"ciscoCatalyst6000E1VoIPGateway": {"uuid": "{A111}"}}
        }
        ucm.get_cisco_catalyst6000_e1_voip_gateway(uuid="{A111}")
        op, body = sent(ucm)
        assert text(body, "uuid") == "{A111}"
        assert not has(body, "name")

    def test_list(self, ucm):
        ucm.recorder.responses["listCiscoCatalyst6000E1VoIPGateway"] = {
            "return": {"ciscoCatalyst6000E1VoIPGateway": [{"name": "CAT-E1-01"}]}
        }
        result = ucm.get_cisco_catalyst6000_e1_voip_gateways()
        op, body = sent(ucm)
        assert op == "listCiscoCatalyst6000E1VoIPGateway"
        assert len(result) == 1

    def test_list_empty(self, ucm):
        ucm.recorder.responses["listCiscoCatalyst6000E1VoIPGateway"] = {"return": None}
        assert ucm.get_cisco_catalyst6000_e1_voip_gateways() == []

    def test_update(self, ucm):
        ucm.update_cisco_catalyst6000_e1_voip_gateway(name="CAT-E1-01")
        op, body = sent(ucm)
        assert op == "updateCiscoCatalyst6000E1VoIPGateway"

    def test_remove(self, ucm):
        ucm.remove_cisco_catalyst6000_e1_voip_gateway(name="CAT-E1-01")
        op, body = sent(ucm)
        assert op == "removeCiscoCatalyst6000E1VoIPGateway"
        assert text(body, "name") == "CAT-E1-01"

    def test_apply(self, ucm):
        ucm.apply_cisco_catalyst6000_e1_voip_gateway(name="CAT-E1-01")
        op, body = sent(ucm)
        assert op == "applyCiscoCatalyst6000E1VoIPGateway"
        assert text(body, "name") == "CAT-E1-01"

    def test_reset(self, ucm):
        ucm.reset_cisco_catalyst6000_e1_voip_gateway(name="CAT-E1-01")
        op, body = sent(ucm)
        assert op == "resetCiscoCatalyst6000E1VoIPGateway"

    def test_restart(self, ucm):
        ucm.restart_cisco_catalyst6000_e1_voip_gateway(name="CAT-E1-01")
        op, body = sent(ucm)
        assert op == "restartCiscoCatalyst6000E1VoIPGateway"


# ---------------------------------------------------------------------------
# CiscoCatalyst6000T1VoIPGatewayPri
# ---------------------------------------------------------------------------

class TestCiscoCatalyst6000T1VoIPGatewayPri:
    def test_add(self):
        u = make_ucm_simple()
        u.add_cisco_catalyst6000_t1_voip_gateway_pri(name="CAT-T1PRI-01")
        op, kwargs = simple_sent(u)
        assert op == "addCiscoCatalyst6000T1VoIPGatewayPri"
        assert "ciscoCatalyst6000T1VoIPGatewayPri" in kwargs

    def test_get_by_name(self, ucm):
        ucm.recorder.responses["getCiscoCatalyst6000T1VoIPGatewayPri"] = {
            "return": {"ciscoCatalyst6000T1VoIPGatewayPri": {"name": "CAT-T1PRI-01"}}
        }
        result = ucm.get_cisco_catalyst6000_t1_voip_gateway_pri(name="CAT-T1PRI-01")
        op, body = sent(ucm)
        assert op == "getCiscoCatalyst6000T1VoIPGatewayPri"
        assert text(body, "name") == "CAT-T1PRI-01"
        assert result == {"name": "CAT-T1PRI-01"}

    def test_get_by_uuid(self, ucm):
        ucm.recorder.responses["getCiscoCatalyst6000T1VoIPGatewayPri"] = {
            "return": {"ciscoCatalyst6000T1VoIPGatewayPri": {"uuid": "{B222}"}}
        }
        ucm.get_cisco_catalyst6000_t1_voip_gateway_pri(uuid="{B222}")
        op, body = sent(ucm)
        assert text(body, "uuid") == "{B222}"
        assert not has(body, "name")

    def test_list(self, ucm):
        ucm.recorder.responses["listCiscoCatalyst6000T1VoIPGatewayPri"] = {
            "return": {"ciscoCatalyst6000T1VoIPGatewayPri": [{"name": "CAT-T1PRI-01"}]}
        }
        result = ucm.get_cisco_catalyst6000_t1_voip_gateway_pris()
        op, body = sent(ucm)
        assert op == "listCiscoCatalyst6000T1VoIPGatewayPri"
        assert len(result) == 1

    def test_list_empty(self, ucm):
        ucm.recorder.responses["listCiscoCatalyst6000T1VoIPGatewayPri"] = {"return": None}
        assert ucm.get_cisco_catalyst6000_t1_voip_gateway_pris() == []

    def test_update(self, ucm):
        ucm.update_cisco_catalyst6000_t1_voip_gateway_pri(name="CAT-T1PRI-01")
        op, body = sent(ucm)
        assert op == "updateCiscoCatalyst6000T1VoIPGatewayPri"

    def test_remove(self, ucm):
        ucm.remove_cisco_catalyst6000_t1_voip_gateway_pri(name="CAT-T1PRI-01")
        op, body = sent(ucm)
        assert op == "removeCiscoCatalyst6000T1VoIPGatewayPri"
        assert text(body, "name") == "CAT-T1PRI-01"

    def test_apply(self, ucm):
        ucm.apply_cisco_catalyst6000_t1_voip_gateway_pri(name="CAT-T1PRI-01")
        op, body = sent(ucm)
        assert op == "applyCiscoCatalyst6000T1VoIPGatewayPri"

    def test_reset(self, ucm):
        ucm.reset_cisco_catalyst6000_t1_voip_gateway_pri(name="CAT-T1PRI-01")
        op, body = sent(ucm)
        assert op == "resetCiscoCatalyst6000T1VoIPGatewayPri"

    def test_restart(self, ucm):
        ucm.restart_cisco_catalyst6000_t1_voip_gateway_pri(name="CAT-T1PRI-01")
        op, body = sent(ucm)
        assert op == "restartCiscoCatalyst6000T1VoIPGatewayPri"


# ---------------------------------------------------------------------------
# CiscoCatalyst6000T1VoIPGatewayT1
# ---------------------------------------------------------------------------

class TestCiscoCatalyst6000T1VoIPGatewayT1:
    def test_add(self):
        u = make_ucm_simple()
        u.add_cisco_catalyst6000_t1_voip_gateway_t1(name="CAT-T1-01")
        op, kwargs = simple_sent(u)
        assert op == "addCiscoCatalyst6000T1VoIPGatewayT1"
        assert "ciscoCatalyst6000T1VoIPGatewayT1" in kwargs

    def test_get_by_name(self, ucm):
        ucm.recorder.responses["getCiscoCatalyst6000T1VoIPGatewayT1"] = {
            "return": {"ciscoCatalyst6000T1VoIPGatewayT1": {"name": "CAT-T1-01"}}
        }
        result = ucm.get_cisco_catalyst6000_t1_voip_gateway_t1(name="CAT-T1-01")
        op, body = sent(ucm)
        assert op == "getCiscoCatalyst6000T1VoIPGatewayT1"
        assert text(body, "name") == "CAT-T1-01"
        assert result == {"name": "CAT-T1-01"}

    def test_get_by_uuid(self, ucm):
        ucm.recorder.responses["getCiscoCatalyst6000T1VoIPGatewayT1"] = {
            "return": {"ciscoCatalyst6000T1VoIPGatewayT1": {"uuid": "{C333}"}}
        }
        ucm.get_cisco_catalyst6000_t1_voip_gateway_t1(uuid="{C333}")
        op, body = sent(ucm)
        assert text(body, "uuid") == "{C333}"
        assert not has(body, "name")

    def test_list(self, ucm):
        ucm.recorder.responses["listCiscoCatalyst6000T1VoIPGatewayT1"] = {
            "return": {"ciscoCatalyst6000T1VoIPGatewayT1": [{"name": "CAT-T1-01"}]}
        }
        result = ucm.get_cisco_catalyst6000_t1_voip_gateway_t1s()
        op, body = sent(ucm)
        assert op == "listCiscoCatalyst6000T1VoIPGatewayT1"
        assert len(result) == 1

    def test_list_empty(self, ucm):
        ucm.recorder.responses["listCiscoCatalyst6000T1VoIPGatewayT1"] = {"return": None}
        assert ucm.get_cisco_catalyst6000_t1_voip_gateway_t1s() == []

    def test_update(self, ucm):
        ucm.update_cisco_catalyst6000_t1_voip_gateway_t1(name="CAT-T1-01")
        op, body = sent(ucm)
        assert op == "updateCiscoCatalyst6000T1VoIPGatewayT1"

    def test_remove(self, ucm):
        ucm.remove_cisco_catalyst6000_t1_voip_gateway_t1(name="CAT-T1-01")
        op, body = sent(ucm)
        assert op == "removeCiscoCatalyst6000T1VoIPGatewayT1"
        assert text(body, "name") == "CAT-T1-01"

    def test_apply(self, ucm):
        ucm.apply_cisco_catalyst6000_t1_voip_gateway_t1(name="CAT-T1-01")
        op, body = sent(ucm)
        assert op == "applyCiscoCatalyst6000T1VoIPGatewayT1"

    def test_reset(self, ucm):
        ucm.reset_cisco_catalyst6000_t1_voip_gateway_t1(name="CAT-T1-01")
        op, body = sent(ucm)
        assert op == "resetCiscoCatalyst6000T1VoIPGatewayT1"

    def test_restart(self, ucm):
        ucm.restart_cisco_catalyst6000_t1_voip_gateway_t1(name="CAT-T1-01")
        op, body = sent(ucm)
        assert op == "restartCiscoCatalyst6000T1VoIPGatewayT1"


# ---------------------------------------------------------------------------
# Gatekeeper
# ---------------------------------------------------------------------------

class TestGatekeeper:
    def test_add(self, ucm):
        ucm.add_gatekeeper(
            name="GK-01",
            description="Test GK",
            rrqTimeToLive="1800",
        )
        op, body = sent(ucm)
        assert op == "addGatekeeper"
        assert text(body, "gatekeeper/name") == "GK-01"

    def test_get_by_name(self, ucm):
        ucm.recorder.responses["getGatekeeper"] = {
            "return": {"gatekeeper": {"name": "GK-01"}}
        }
        result = ucm.get_gatekeeper(name="GK-01")
        op, body = sent(ucm)
        assert op == "getGatekeeper"
        assert text(body, "name") == "GK-01"
        assert result == {"name": "GK-01"}

    def test_get_by_uuid(self, ucm):
        ucm.recorder.responses["getGatekeeper"] = {
            "return": {"gatekeeper": {"uuid": "{GK11}"}}
        }
        ucm.get_gatekeeper(uuid="{GK11}")
        op, body = sent(ucm)
        assert text(body, "uuid") == "{GK11}"
        assert not has(body, "name")

    def test_get_requires_exactly_one_id(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_gatekeeper()
        with pytest.raises(ValueError):
            ucm.get_gatekeeper(name="x", uuid="y")

    def test_list(self, ucm):
        ucm.recorder.responses["listGatekeeper"] = {
            "return": {"gatekeeper": [{"name": "GK-01"}]}
        }
        result = ucm.get_gatekeepers()
        op, body = sent(ucm)
        assert op == "listGatekeeper"
        assert len(result) == 1

    def test_list_empty(self, ucm):
        ucm.recorder.responses["listGatekeeper"] = {"return": None}
        assert ucm.get_gatekeepers() == []

    def test_update(self, ucm):
        ucm.update_gatekeeper(name="GK-01", description="Updated")
        op, body = sent(ucm)
        assert op == "updateGatekeeper"
        assert text(body, "name") == "GK-01"

    def test_remove(self, ucm):
        ucm.remove_gatekeeper(name="GK-01")
        op, body = sent(ucm)
        assert op == "removeGatekeeper"
        assert text(body, "name") == "GK-01"

    def test_remove_by_uuid(self, ucm):
        ucm.remove_gatekeeper(uuid="{GK22}")
        op, body = sent(ucm)
        assert text(body, "uuid") == "{GK22}"
        assert not has(body, "name")

    def test_apply(self, ucm):
        ucm.apply_gatekeeper(name="GK-01")
        op, body = sent(ucm)
        assert op == "applyGatekeeper"
        assert text(body, "name") == "GK-01"

    def test_reset(self, ucm):
        ucm.reset_gatekeeper(name="GK-01")
        op, body = sent(ucm)
        assert op == "resetGatekeeper"
        assert text(body, "name") == "GK-01"

    def test_restart(self, ucm):
        ucm.restart_gatekeeper(name="GK-01")
        op, body = sent(ucm)
        assert op == "restartGatekeeper"
        assert text(body, "name") == "GK-01"

    def test_restart_by_uuid(self, ucm):
        ucm.restart_gatekeeper(uuid="{GK33}")
        op, body = sent(ucm)
        assert text(body, "uuid") == "{GK33}"
        assert not has(body, "name")


# ---------------------------------------------------------------------------
# GatewayEndpointDigitalAccessBri
# ---------------------------------------------------------------------------

class TestGatewayEndpointDigitalAccessBri:
    def test_add(self):
        u = make_ucm_simple()
        u.add_gateway_endpoint_digital_access_bri(
            domainName="mgcp-gw.corp.com",
            unit=0,
            subunit=0,
            endpoint={"name": "BRI/S0/SU0/0@mgcp-gw.corp.com"},
        )
        op, kwargs = simple_sent(u)
        assert op == "addGatewayEndpointDigitalAccessBri"
        assert "gatewayEndpointDigitalAccessBri" in kwargs

    def test_get_by_name(self, ucm):
        ucm.recorder.responses["getGatewayEndpointDigitalAccessBri"] = {
            "return": {"gatewayEndpointDigitalAccessBri": {"name": "BRI/S0/SU0/0@gw"}}
        }
        result = ucm.get_gateway_endpoint_digital_access_bri(name="BRI/S0/SU0/0@gw")
        op, body = sent(ucm)
        assert op == "getGatewayEndpointDigitalAccessBri"
        assert text(body, "name") == "BRI/S0/SU0/0@gw"
        assert result == {"name": "BRI/S0/SU0/0@gw"}

    def test_get_by_uuid(self, ucm):
        ucm.recorder.responses["getGatewayEndpointDigitalAccessBri"] = {
            "return": {"gatewayEndpointDigitalAccessBri": {"uuid": "{BRI1}"}}
        }
        ucm.get_gateway_endpoint_digital_access_bri(uuid="{BRI1}")
        op, body = sent(ucm)
        assert text(body, "uuid") == "{BRI1}"
        assert not has(body, "name")

    def test_get_requires_exactly_one_id(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_gateway_endpoint_digital_access_bri()
        with pytest.raises(ValueError):
            ucm.get_gateway_endpoint_digital_access_bri(name="x", uuid="y")

    def test_update(self, ucm):
        ucm.update_gateway_endpoint_digital_access_bri(name="BRI/S0/SU0/0@gw")
        op, body = sent(ucm)
        assert op == "updateGatewayEndpointDigitalAccessBri"
        assert text(body, "name") == "BRI/S0/SU0/0@gw"

    def test_remove(self, ucm):
        ucm.remove_gateway_endpoint_digital_access_bri(name="BRI/S0/SU0/0@gw")
        op, body = sent(ucm)
        assert op == "removeGatewayEndpointDigitalAccessBri"
        assert text(body, "name") == "BRI/S0/SU0/0@gw"

    def test_remove_by_uuid(self, ucm):
        ucm.remove_gateway_endpoint_digital_access_bri(uuid="{BRI2}")
        op, body = sent(ucm)
        assert text(body, "uuid") == "{BRI2}"
        assert not has(body, "name")


# ---------------------------------------------------------------------------
# H323Phone
# ---------------------------------------------------------------------------

class TestH323Phone:
    def test_add(self):
        u = make_ucm_simple()
        u.add_h323_phone(name="H323-PHONE-01")
        op, kwargs = simple_sent(u)
        assert op == "addH323Phone"
        assert "h323Phone" in kwargs

    def test_get_by_name(self, ucm):
        ucm.recorder.responses["getH323Phone"] = {
            "return": {"h323Phone": {"name": "H323-PHONE-01"}}
        }
        result = ucm.get_h323_phone(name="H323-PHONE-01")
        op, body = sent(ucm)
        assert op == "getH323Phone"
        assert text(body, "name") == "H323-PHONE-01"
        assert result == {"name": "H323-PHONE-01"}

    def test_get_by_uuid(self, ucm):
        ucm.recorder.responses["getH323Phone"] = {
            "return": {"h323Phone": {"uuid": "{H323-1}"}}
        }
        ucm.get_h323_phone(uuid="{H323-1}")
        op, body = sent(ucm)
        assert text(body, "uuid") == "{H323-1}"
        assert not has(body, "name")

    def test_get_requires_exactly_one_id(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_h323_phone()
        with pytest.raises(ValueError):
            ucm.get_h323_phone(name="x", uuid="y")

    def test_list(self, ucm):
        ucm.recorder.responses["listH323Phone"] = {
            "return": {"h323Phone": [{"name": "H323-PHONE-01"}]}
        }
        result = ucm.get_h323_phones()
        op, body = sent(ucm)
        assert op == "listH323Phone"
        assert len(result) == 1

    def test_list_empty(self, ucm):
        ucm.recorder.responses["listH323Phone"] = {"return": None}
        assert ucm.get_h323_phones() == []

    def test_update(self, ucm):
        ucm.update_h323_phone(name="H323-PHONE-01", description="Updated")
        op, body = sent(ucm)
        assert op == "updateH323Phone"
        assert text(body, "name") == "H323-PHONE-01"

    def test_remove(self, ucm):
        ucm.remove_h323_phone(name="H323-PHONE-01")
        op, body = sent(ucm)
        assert op == "removeH323Phone"
        assert text(body, "name") == "H323-PHONE-01"

    def test_remove_by_uuid(self, ucm):
        ucm.remove_h323_phone(uuid="{H323-2}")
        op, body = sent(ucm)
        assert text(body, "uuid") == "{H323-2}"
        assert not has(body, "name")

    def test_apply(self, ucm):
        ucm.apply_h323_phone(name="H323-PHONE-01")
        op, body = sent(ucm)
        assert op == "applyH323Phone"
        assert text(body, "name") == "H323-PHONE-01"

    def test_reset(self, ucm):
        ucm.reset_h323_phone(name="H323-PHONE-01")
        op, body = sent(ucm)
        assert op == "resetH323Phone"
        assert text(body, "name") == "H323-PHONE-01"

    def test_restart(self, ucm):
        ucm.restart_h323_phone(name="H323-PHONE-01")
        op, body = sent(ucm)
        assert op == "restartH323Phone"
        assert text(body, "name") == "H323-PHONE-01"

    def test_restart_by_uuid(self, ucm):
        ucm.restart_h323_phone(uuid="{H323-3}")
        op, body = sent(ucm)
        assert text(body, "uuid") == "{H323-3}"
        assert not has(body, "name")


# ---------------------------------------------------------------------------
# Vg224
# ---------------------------------------------------------------------------

class TestVg224:
    def test_add(self):
        u = make_ucm_simple()
        u.add_vg224(
            domainName="vg224-gw.corp.com",
            product="Cisco VG224",
            protocol="MGCP",
        )
        op, kwargs = simple_sent(u)
        assert op == "addVg224"
        assert "vg224" in kwargs

    def test_get_by_domain_name(self, ucm):
        ucm.recorder.responses["getVg224"] = {
            "return": {"vg224": {"domainName": "vg224-gw.corp.com"}}
        }
        result = ucm.get_vg224(domainName="vg224-gw.corp.com")
        op, body = sent(ucm)
        assert op == "getVg224"
        assert text(body, "domainName") == "vg224-gw.corp.com"
        assert not has(body, "uuid")
        assert result == {"domainName": "vg224-gw.corp.com"}

    def test_get_by_uuid(self, ucm):
        ucm.recorder.responses["getVg224"] = {
            "return": {"vg224": {"uuid": "{VG-1}"}}
        }
        ucm.get_vg224(uuid="{VG-1}")
        op, body = sent(ucm)
        assert text(body, "uuid") == "{VG-1}"
        assert not has(body, "domainName")

    def test_get_requires_exactly_one_id(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_vg224()
        with pytest.raises(ValueError):
            ucm.get_vg224(domainName="x", uuid="y")

    def test_update(self, ucm):
        ucm.update_vg224(domainName="vg224-gw.corp.com", description="Updated")
        op, body = sent(ucm)
        assert op == "updateVg224"
        assert text(body, "domainName") == "vg224-gw.corp.com"

    def test_remove_by_domain_name(self, ucm):
        ucm.remove_vg224(domainName="vg224-gw.corp.com")
        op, body = sent(ucm)
        assert op == "removeVg224"
        assert text(body, "domainName") == "vg224-gw.corp.com"
        assert not has(body, "uuid")

    def test_remove_by_uuid(self, ucm):
        ucm.remove_vg224(uuid="{VG-2}")
        op, body = sent(ucm)
        assert text(body, "uuid") == "{VG-2}"
        assert not has(body, "domainName")

    def test_reset(self, ucm):
        ucm.reset_vg224(domainName="vg224-gw.corp.com")
        op, body = sent(ucm)
        assert op == "resetVg224"
        assert text(body, "domainName") == "vg224-gw.corp.com"

    def test_restart(self, ucm):
        ucm.restart_vg224(domainName="vg224-gw.corp.com")
        op, body = sent(ucm)
        assert op == "restartVg224"
        assert text(body, "domainName") == "vg224-gw.corp.com"

    def test_restart_by_uuid(self, ucm):
        ucm.restart_vg224(uuid="{VG-3}")
        op, body = sent(ucm)
        assert text(body, "uuid") == "{VG-3}"
        assert not has(body, "domainName")
