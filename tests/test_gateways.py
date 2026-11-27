"""Offline request tests for ciscoaxl/gateways.py.

Run with: pytest tests/test_gateways.py
"""
import pytest

from test_offline_requests import make_ucm, make_ucm_simple, sent, simple_sent, text, has


@pytest.fixture
def ucm():
    return make_ucm("15.0")


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
