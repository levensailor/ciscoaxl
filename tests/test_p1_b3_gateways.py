"""Offline tests for P1 Batch B3 — p1_gateways.py

Verifies that every method in P1Gateways:
  * calls the correct AXL operation
  * passes the right element names and values
  * handles domainName/uuid routing via _identify_gateway (Gateway)
  * handles name/uuid routing via _identify (endpoint types)
  * returns the unwrapped result
  * returns [] on empty list responses

Run with: pytest tests/test_p1_b3_gateways.py
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
    """Lightweight recorder that captures (op_name, kwargs) WITHOUT SOAP serialization.

    Use this when the AXL operation wraps a complex nested object whose required
    inner fields would cause zeep validation errors during create_message, but all
    you need to verify is that the correct operation and top-level wrapper kwarg are
    used (e.g. add* operations for gateway endpoints).
    """

    def __init__(self, zeep_client, service):
        self._zeep = zeep_client
        self._real = service
        self._binding = service._binding
        self.calls = []     # list of (op_name, kwargs) tuples
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
    """Return a UCM stub backed by SimpleRecorder (no SOAP serialization)."""
    if version not in _clients:
        wsdl = (SCHEMA_DIR / version / "AXLAPI.wsdl").as_uri()
        settings = Settings(
            strict=False, xml_huge_tree=True, xsd_ignore_sequence_order=True
        )
        _clients[version] = Client(wsdl, settings=settings)
    zeep_client = _clients[version]
    service = zeep_client.create_service(BINDING, "https://cucm.invalid:8443/axl/")
    recorder = SimpleRecorder(zeep_client, service)

    ucm = axl.__new__(axl)
    ucm._zeep = zeep_client
    ucm.cucm = "cucm.invalid"
    ucm.cucm_version = version
    ucm.client = AliasingService(zeep_client, recorder)
    ucm.recorder = recorder
    return ucm


def simple_sent(ucm, index=-1):
    """Return (op_name, kwargs) from a SimpleRecorder call."""
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
# Gateway
# ---------------------------------------------------------------------------

class TestGateway:
    def test_add_gateway(self, ucm):
        ucm.add_gateway(
            domainName="mgcp-gw.corp.com",
            product="Cisco VG200",
            protocol="MGCP",
            callManagerGroupName="Default",
        )
        op, body = sent(ucm)
        assert op == "addGateway"
        assert text(body, "gateway/domainName") == "mgcp-gw.corp.com"
        assert text(body, "gateway/protocol") == "MGCP"

    def test_get_gateway_by_domain_name(self, ucm):
        ucm.recorder.responses["getGateway"] = {
            "return": {"gateway": {"domainName": "mgcp-gw.corp.com"}}
        }
        result = ucm.get_gateway(domainName="mgcp-gw.corp.com")
        op, body = sent(ucm)
        assert op == "getGateway"
        assert text(body, "domainName") == "mgcp-gw.corp.com"
        assert not has(body, "uuid")
        assert result == {"domainName": "mgcp-gw.corp.com"}

    def test_get_gateway_by_uuid(self, ucm):
        ucm.recorder.responses["getGateway"] = {
            "return": {"gateway": {"uuid": "{1234}"}}
        }
        ucm.get_gateway(uuid="{1234}")
        op, body = sent(ucm)
        assert op == "getGateway"
        assert text(body, "uuid") == "{1234}"
        assert not has(body, "domainName")

    def test_get_gateway_requires_exactly_one_identifier(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_gateway()
        with pytest.raises(ValueError):
            ucm.get_gateway(domainName="x", uuid="y")

    def test_get_gateways(self, ucm):
        ucm.recorder.responses["listGateway"] = {
            "return": {"gateway": [{"domainName": "mgcp-gw.corp.com"}]}
        }
        result = ucm.get_gateways()
        op, body = sent(ucm)
        assert op == "listGateway"
        assert len(result) == 1

    def test_get_gateways_empty(self, ucm):
        ucm.recorder.responses["listGateway"] = {"return": None}
        result = ucm.get_gateways()
        assert result == []

    def test_update_gateway(self, ucm):
        ucm.update_gateway(domainName="mgcp-gw.corp.com", description="Updated")
        op, body = sent(ucm)
        assert op == "updateGateway"
        assert text(body, "domainName") == "mgcp-gw.corp.com"

    def test_remove_gateway_by_domain_name(self, ucm):
        ucm.remove_gateway(domainName="mgcp-gw.corp.com")
        op, body = sent(ucm)
        assert op == "removeGateway"
        assert text(body, "domainName") == "mgcp-gw.corp.com"
        assert not has(body, "uuid")

    def test_remove_gateway_by_uuid(self, ucm):
        ucm.remove_gateway(uuid="{AAAA-1111}")
        op, body = sent(ucm)
        assert op == "removeGateway"
        assert text(body, "uuid") == "{AAAA-1111}"
        assert not has(body, "domainName")

    def test_apply_gateway(self, ucm):
        ucm.apply_gateway(domainName="mgcp-gw.corp.com")
        op, body = sent(ucm)
        assert op == "applyGateway"
        assert text(body, "domainName") == "mgcp-gw.corp.com"

    def test_reset_gateway(self, ucm):
        ucm.reset_gateway(domainName="mgcp-gw.corp.com")
        op, body = sent(ucm)
        assert op == "resetGateway"
        assert text(body, "domainName") == "mgcp-gw.corp.com"

    def test_restart_gateway(self, ucm):
        ucm.restart_gateway(domainName="mgcp-gw.corp.com")
        op, body = sent(ucm)
        assert op == "restartGateway"
        assert text(body, "domainName") == "mgcp-gw.corp.com"

    def test_restart_gateway_by_uuid(self, ucm):
        ucm.restart_gateway(uuid="{BBBB-2222}")
        op, body = sent(ucm)
        assert op == "restartGateway"
        assert text(body, "uuid") == "{BBBB-2222}"
        assert not has(body, "domainName")


# ---------------------------------------------------------------------------
# GatewayEndpointAnalogAccess
# ---------------------------------------------------------------------------

class TestGatewayEndpointAnalogAccess:
    def test_add_gateway_endpoint_analog_access(self):
        # XGatewayEndpointAnalogAccess endpoint has many inner required fields (name, product,
        # class, protocol, devicePoolName, locationName …). Use SimpleRecorder to verify the
        # correct operation and wrapper kwarg without full SOAP serialization.
        ucm = make_ucm_simple()
        ucm.add_gateway_endpoint_analog_access(
            domainName="mgcp-gw.corp.com",
            unit=0,
            subunit=0,
            endpoint={"name": "AALN/S0/SU0/0@mgcp-gw.corp.com"},
        )
        op, kwargs = simple_sent(ucm)
        assert op == "addGatewayEndpointAnalogAccess"
        assert "gatewayEndpointAnalogAccess" in kwargs

    def test_get_gateway_endpoint_analog_access_by_name(self, ucm):
        ucm.recorder.responses["getGatewayEndpointAnalogAccess"] = {
            "return": {"gatewayEndpointAnalogAccess": {"name": "AALN/S0/SU0/0@mgcp-gw"}}
        }
        result = ucm.get_gateway_endpoint_analog_access(name="AALN/S0/SU0/0@mgcp-gw")
        op, body = sent(ucm)
        assert op == "getGatewayEndpointAnalogAccess"
        assert text(body, "name") == "AALN/S0/SU0/0@mgcp-gw"
        assert result == {"name": "AALN/S0/SU0/0@mgcp-gw"}

    def test_get_gateway_endpoint_analog_access_by_uuid(self, ucm):
        ucm.recorder.responses["getGatewayEndpointAnalogAccess"] = {
            "return": {"gatewayEndpointAnalogAccess": {"uuid": "{1111}"}}
        }
        ucm.get_gateway_endpoint_analog_access(uuid="{1111}")
        op, body = sent(ucm)
        assert text(body, "uuid") == "{1111}"
        assert not has(body, "name")

    def test_update_gateway_endpoint_analog_access(self, ucm):
        # XGatewayEndpointAnalog has: index, name, description, product, model, class, ...
        ucm.update_gateway_endpoint_analog_access(
            name="AALN/S0/SU0/0@mgcp-gw",
        )
        op, body = sent(ucm)
        assert op == "updateGatewayEndpointAnalogAccess"
        assert text(body, "name") == "AALN/S0/SU0/0@mgcp-gw"

    def test_remove_gateway_endpoint_analog_access(self, ucm):
        ucm.remove_gateway_endpoint_analog_access(name="AALN/S0/SU0/0@mgcp-gw")
        op, body = sent(ucm)
        assert op == "removeGatewayEndpointAnalogAccess"
        assert text(body, "name") == "AALN/S0/SU0/0@mgcp-gw"

    def test_remove_gateway_endpoint_analog_access_by_uuid(self, ucm):
        ucm.remove_gateway_endpoint_analog_access(uuid="{2222}")
        op, body = sent(ucm)
        assert text(body, "uuid") == "{2222}"
        assert not has(body, "name")

    def test_get_requires_name_or_uuid(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_gateway_endpoint_analog_access()
        with pytest.raises(ValueError):
            ucm.get_gateway_endpoint_analog_access(name="x", uuid="y")


# ---------------------------------------------------------------------------
# GatewayEndpointDigitalAccessPri
# ---------------------------------------------------------------------------

class TestGatewayEndpointDigitalAccessPri:
    def test_add_gateway_endpoint_digital_access_pri(self):
        ucm = make_ucm_simple()
        ucm.add_gateway_endpoint_digital_access_pri(
            domainName="mgcp-gw.corp.com",
            unit=0,
            subunit=0,
            endpoint={"name": "T1-PRI/S0/SU0/0@mgcp-gw.corp.com"},
        )
        op, kwargs = simple_sent(ucm)
        assert op == "addGatewayEndpointDigitalAccessPri"
        assert "gatewayEndpointDigitalAccessPri" in kwargs

    def test_get_gateway_endpoint_digital_access_pri(self, ucm):
        ucm.recorder.responses["getGatewayEndpointDigitalAccessPri"] = {
            "return": {"gatewayEndpointDigitalAccessPri": {"name": "T1-PRI@mgcp-gw"}}
        }
        result = ucm.get_gateway_endpoint_digital_access_pri(name="T1-PRI@mgcp-gw")
        op, body = sent(ucm)
        assert op == "getGatewayEndpointDigitalAccessPri"
        assert text(body, "name") == "T1-PRI@mgcp-gw"
        assert result == {"name": "T1-PRI@mgcp-gw"}

    def test_update_gateway_endpoint_digital_access_pri(self, ucm):
        ucm.update_gateway_endpoint_digital_access_pri(name="T1-PRI@mgcp-gw")
        op, body = sent(ucm)
        assert op == "updateGatewayEndpointDigitalAccessPri"
        assert text(body, "name") == "T1-PRI@mgcp-gw"

    def test_remove_gateway_endpoint_digital_access_pri(self, ucm):
        ucm.remove_gateway_endpoint_digital_access_pri(name="T1-PRI@mgcp-gw")
        op, body = sent(ucm)
        assert op == "removeGatewayEndpointDigitalAccessPri"
        assert text(body, "name") == "T1-PRI@mgcp-gw"

    def test_remove_by_uuid(self, ucm):
        ucm.remove_gateway_endpoint_digital_access_pri(uuid="{3333}")
        op, body = sent(ucm)
        assert text(body, "uuid") == "{3333}"
        assert not has(body, "name")


# ---------------------------------------------------------------------------
# GatewayEndpointDigitalAccessT1
# ---------------------------------------------------------------------------

class TestGatewayEndpointDigitalAccessT1:
    def test_add_gateway_endpoint_digital_access_t1(self):
        ucm = make_ucm_simple()
        ucm.add_gateway_endpoint_digital_access_t1(
            domainName="mgcp-gw.corp.com",
            unit=0,
            subunit=0,
            endpoint={"name": "T1/S0/SU0/0@mgcp-gw.corp.com"},
        )
        op, kwargs = simple_sent(ucm)
        assert op == "addGatewayEndpointDigitalAccessT1"
        assert "gatewayEndpointDigitalAccessT1" in kwargs

    def test_get_gateway_endpoint_digital_access_t1(self, ucm):
        ucm.recorder.responses["getGatewayEndpointDigitalAccessT1"] = {
            "return": {"gatewayEndpointDigitalAccessT1": {"name": "T1@mgcp-gw"}}
        }
        result = ucm.get_gateway_endpoint_digital_access_t1(name="T1@mgcp-gw")
        op, body = sent(ucm)
        assert op == "getGatewayEndpointDigitalAccessT1"
        assert text(body, "name") == "T1@mgcp-gw"
        assert result == {"name": "T1@mgcp-gw"}

    def test_update_gateway_endpoint_digital_access_t1(self, ucm):
        ucm.update_gateway_endpoint_digital_access_t1(name="T1@mgcp-gw")
        op, body = sent(ucm)
        assert op == "updateGatewayEndpointDigitalAccessT1"
        assert text(body, "name") == "T1@mgcp-gw"

    def test_remove_gateway_endpoint_digital_access_t1(self, ucm):
        ucm.remove_gateway_endpoint_digital_access_t1(name="T1@mgcp-gw")
        op, body = sent(ucm)
        assert op == "removeGatewayEndpointDigitalAccessT1"
        assert text(body, "name") == "T1@mgcp-gw"

    def test_remove_by_uuid(self, ucm):
        ucm.remove_gateway_endpoint_digital_access_t1(uuid="{4444}")
        op, body = sent(ucm)
        assert text(body, "uuid") == "{4444}"
        assert not has(body, "name")


# ---------------------------------------------------------------------------
# GatewaySccpEndpoints
# ---------------------------------------------------------------------------

class TestGatewaySccpEndpoints:
    def test_add_gateway_sccp_endpoints(self):
        ucm = make_ucm_simple()
        ucm.add_gateway_sccp_endpoints(
            domainName="SEPAABBCCDD1122",
            unit=0,
            subunit=0,
            endpoint={"name": "SCCP/S0/SU0/0@SEPAABBCCDD1122"},
        )
        op, kwargs = simple_sent(ucm)
        assert op == "addGatewaySccpEndpoints"
        assert "gatewaySccpEndpoints" in kwargs

    def test_get_gateway_sccp_endpoints(self, ucm):
        ucm.recorder.responses["getGatewaySccpEndpoints"] = {
            "return": {"gatewaySccpEndpoints": {"name": "SCCP/S0/SU0/0@SEPAA"}}
        }
        result = ucm.get_gateway_sccp_endpoints(name="SCCP/S0/SU0/0@SEPAA")
        op, body = sent(ucm)
        assert op == "getGatewaySccpEndpoints"
        assert text(body, "name") == "SCCP/S0/SU0/0@SEPAA"
        assert result == {"name": "SCCP/S0/SU0/0@SEPAA"}

    def test_get_gateway_sccp_endpoints_by_uuid(self, ucm):
        ucm.recorder.responses["getGatewaySccpEndpoints"] = {
            "return": {"gatewaySccpEndpoints": {"uuid": "{5555}"}}
        }
        ucm.get_gateway_sccp_endpoints(uuid="{5555}")
        op, body = sent(ucm)
        assert text(body, "uuid") == "{5555}"
        assert not has(body, "name")

    def test_update_gateway_sccp_endpoints(self, ucm):
        ucm.update_gateway_sccp_endpoints(name="SCCP/S0/SU0/0@SEPAA")
        op, body = sent(ucm)
        assert op == "updateGatewaySccpEndpoints"
        assert text(body, "name") == "SCCP/S0/SU0/0@SEPAA"

    def test_remove_gateway_sccp_endpoints(self, ucm):
        ucm.remove_gateway_sccp_endpoints(name="SCCP/S0/SU0/0@SEPAA")
        op, body = sent(ucm)
        assert op == "removeGatewaySccpEndpoints"
        assert text(body, "name") == "SCCP/S0/SU0/0@SEPAA"

    def test_remove_by_uuid(self, ucm):
        ucm.remove_gateway_sccp_endpoints(uuid="{6666}")
        op, body = sent(ucm)
        assert text(body, "uuid") == "{6666}"
        assert not has(body, "name")

    def test_get_requires_name_or_uuid(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_gateway_sccp_endpoints()
        with pytest.raises(ValueError):
            ucm.get_gateway_sccp_endpoints(name="x", uuid="y")


# ---------------------------------------------------------------------------
# GatewaySubunits
# ---------------------------------------------------------------------------

class TestGatewaySubunits:
    def test_add_gateway_subunits(self, ucm):
        ucm.add_gateway_subunits(
            domainName="mgcp-gw.corp.com",
            unit=0,
            subunits={"subunit": [{"index": 0, "product": "Cisco VG200 FXS"}]},
        )
        op, body = sent(ucm)
        assert op == "addGatewaySubunits"
        assert has(body, "gatewaySubunits")

    def test_remove_gateway_subunits(self, ucm):
        ucm.remove_gateway_subunits(
            domainName="mgcp-gw.corp.com",
            unit=0,
            subunits={"subunit": [{"index": 0}]},
        )
        op, body = sent(ucm)
        assert op == "removeGatewaySubunits"
        assert text(body, "domainName") == "mgcp-gw.corp.com"

    def test_remove_gateway_subunits_by_uuid(self, ucm):
        ucm.remove_gateway_subunits(
            gatewayUuid="{CCCC-7777}",
            unit=0,
            subunits={"subunit": [{"index": 0}]},
        )
        op, body = sent(ucm)
        assert op == "removeGatewaySubunits"
        assert text(body, "gatewayUuid") == "{CCCC-7777}"


# ---------------------------------------------------------------------------
# UnitsToGateway
# ---------------------------------------------------------------------------

class TestUnitsToGateway:
    def test_add_units_to_gateway(self, ucm):
        ucm.add_units_to_gateway(
            domainName="mgcp-gw.corp.com",
            units={"unit": [{"index": 0, "product": "Cisco VG200"}]},
        )
        op, body = sent(ucm)
        assert op == "addUnitsToGateway"
        assert has(body, "unitsToGateway")

    def test_remove_units_to_gateway(self, ucm):
        ucm.remove_units_to_gateway(
            domainName="mgcp-gw.corp.com",
            units={"unit": [{"index": 0}]},
        )
        op, body = sent(ucm)
        assert op == "removeUnitsToGateway"
        assert text(body, "domainName") == "mgcp-gw.corp.com"

    def test_remove_units_to_gateway_by_uuid(self, ucm):
        ucm.remove_units_to_gateway(
            gatewayUuid="{DDDD-8888}",
            units={"unit": [{"index": 0}]},
        )
        op, body = sent(ucm)
        assert op == "removeUnitsToGateway"
        assert text(body, "gatewayUuid") == "{DDDD-8888}"


# ---------------------------------------------------------------------------
# SIPNormalizationScript
# ---------------------------------------------------------------------------

class TestSIPNormalizationScript:
    def test_add_sip_normalization_script(self, ucm):
        # XSIPNormalizationScript requires: name, content, scriptExecutionErrorRecoveryAction,
        # systemResourceErrorRecoveryAction, maxMemoryThreshold, maxLuaInstructionsThreshold,
        # isStandard (all minOccurs=1)
        ucm.add_sip_normalization_script(
            name="MyNormScript",
            content="-- Lua script",
            scriptExecutionErrorRecoveryAction="Message Rollback Only",
            systemResourceErrorRecoveryAction="Disable Script",
            maxMemoryThreshold="50",
            maxLuaInstructionsThreshold="1000",
            isStandard="false",
        )
        op, body = sent(ucm)
        assert op == "addSIPNormalizationScript"
        assert text(body, "sIPNormalizationScript/name") == "MyNormScript"

    def test_get_sip_normalization_script_by_name(self, ucm):
        ucm.recorder.responses["getSIPNormalizationScript"] = {
            "return": {"sIPNormalizationScript": {"name": "MyNormScript"}}
        }
        result = ucm.get_sip_normalization_script(name="MyNormScript")
        op, body = sent(ucm)
        assert op == "getSIPNormalizationScript"
        assert text(body, "name") == "MyNormScript"
        assert result == {"name": "MyNormScript"}

    def test_get_sip_normalization_script_by_uuid(self, ucm):
        ucm.recorder.responses["getSIPNormalizationScript"] = {
            "return": {"sIPNormalizationScript": {"uuid": "{9999}"}}
        }
        ucm.get_sip_normalization_script(uuid="{9999}")
        op, body = sent(ucm)
        assert op == "getSIPNormalizationScript"
        assert text(body, "uuid") == "{9999}"
        assert not has(body, "name")

    def test_get_sip_normalization_scripts(self, ucm):
        ucm.recorder.responses["listSIPNormalizationScript"] = {
            "return": {"sIPNormalizationScript": [{"name": "MyNormScript"}]}
        }
        result = ucm.get_sip_normalization_scripts()
        op, body = sent(ucm)
        assert op == "listSIPNormalizationScript"
        assert len(result) == 1

    def test_get_sip_normalization_scripts_empty(self, ucm):
        ucm.recorder.responses["listSIPNormalizationScript"] = {"return": None}
        result = ucm.get_sip_normalization_scripts()
        assert result == []

    def test_update_sip_normalization_script(self, ucm):
        ucm.update_sip_normalization_script(
            name="MyNormScript", newName="MyNormScriptV2"
        )
        op, body = sent(ucm)
        assert op == "updateSIPNormalizationScript"
        assert text(body, "name") == "MyNormScript"
        assert text(body, "newName") == "MyNormScriptV2"

    def test_remove_sip_normalization_script(self, ucm):
        ucm.remove_sip_normalization_script(name="MyNormScript")
        op, body = sent(ucm)
        assert op == "removeSIPNormalizationScript"
        assert text(body, "name") == "MyNormScript"

    def test_remove_sip_normalization_script_by_uuid(self, ucm):
        ucm.remove_sip_normalization_script(uuid="{EEEE-9999}")
        op, body = sent(ucm)
        assert text(body, "uuid") == "{EEEE-9999}"
        assert not has(body, "name")

    def test_get_requires_name_or_uuid(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_sip_normalization_script()
        with pytest.raises(ValueError):
            ucm.get_sip_normalization_script(name="x", uuid="y")
