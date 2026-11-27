"""Offline tests for P2 Batch B4 — p2_system.py

Verifies that every method in P2System:
  * calls the correct AXL operation
  * passes the right element names and values
  * handles identifier routing (uuid / name / ipAddress …)
  * returns the unwrapped result or [] on empty

Run with: pytest tests/test_p2_b4_system.py
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
            # Use _binding._create directly to avoid zeep's create_message(service, ...)
            # signature conflict when kwargs contains 'service' as an AXL element name.
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
# ApplicationToSoftkeyTemplate
# ---------------------------------------------------------------------------

class TestApplicationToSoftkeyTemplate:
    def test_add_application_to_softkey_template(self, ucm):
        ucm.add_application_to_softkey_template(
            softKeyTemplateName="Standard User",
            standardSoftKeyTemplateName="Standard User",
        )
        op, body = sent(ucm)
        assert op == "addApplicationToSoftkeyTemplate"
        assert text(body, "applicationToSoftkeyTemplate/softKeyTemplateName") == "Standard User"

    def test_remove_application_to_softkey_template_by_names(self, ucm):
        ucm.remove_application_to_softkey_template(
            softKeyTemplateName="Standard User",
            applicationName="Cisco IP Communicator",
        )
        op, body = sent(ucm)
        assert op == "removeApplicationToSoftkeyTemplate"
        assert text(body, "softKeyTemplateName") == "Standard User"
        assert text(body, "applicationName") == "Cisco IP Communicator"


# ---------------------------------------------------------------------------
# DeviceProfileOptions
# ---------------------------------------------------------------------------

class TestDeviceProfileOptions:
    def test_get_device_profile_options(self, ucm):
        ucm.recorder.responses["getDeviceProfileOptions"] = {
            "return": {"deviceProfile": {"product": "Cisco 7962"}}
        }
        result = ucm.get_device_profile_options(uuid="{BBBB-2222}")
        op, body = sent(ucm)
        assert op == "getDeviceProfileOptions"
        assert text(body, "uuid") == "{BBBB-2222}"
        assert result == {"product": "Cisco 7962"}


# ---------------------------------------------------------------------------
# LineOptions
# ---------------------------------------------------------------------------

class TestLineOptions:
    def test_get_line_options(self, ucm):
        ucm.recorder.responses["getLineOptions"] = {
            "return": {"line": {"routePartitionName": "Corp_PT"}}
        }
        result = ucm.get_line_options(uuid="{CCCC-3333}")
        op, body = sent(ucm)
        assert op == "getLineOptions"
        assert text(body, "uuid") == "{CCCC-3333}"
        assert result == {"routePartitionName": "Corp_PT"}


# ---------------------------------------------------------------------------
# NumDevices
# ---------------------------------------------------------------------------

class TestNumDevices:
    def test_get_num_devices_phone(self, ucm):
        ucm.recorder.responses["getNumDevices"] = {"return": 42}
        result = ucm.get_num_devices(device_class="Phone")
        op, body = sent(ucm)
        assert op == "getNumDevices"
        assert text(body, "class") == "Phone"
        assert result == 42

    def test_get_num_devices_gateway(self, ucm):
        ucm.recorder.responses["getNumDevices"] = {"return": 10}
        result = ucm.get_num_devices(device_class="Gateway")
        op, body = sent(ucm)
        assert op == "getNumDevices"
        assert text(body, "class") == "Gateway"
        assert result == 10


# ---------------------------------------------------------------------------
# PhoneOptions
# ---------------------------------------------------------------------------

class TestPhoneOptions:
    def test_get_phone_options(self, ucm):
        ucm.recorder.responses["getPhoneOptions"] = {
            "return": {"phone": {"product": "Cisco 7962"}}
        }
        result = ucm.get_phone_options(uuid="{DDDD-4444}")
        op, body = sent(ucm)
        assert op == "getPhoneOptions"
        assert text(body, "uuid") == "{DDDD-4444}"
        assert result == {"product": "Cisco 7962"}


# ---------------------------------------------------------------------------
# AppServerInfo
# ---------------------------------------------------------------------------

class TestAppServerInfo:
    def test_add_app_server_info(self, ucm):
        ucm.add_app_server_info(
            appServerName="AppSrv1",
            appServerContent="SomeContent",
        )
        op, body = sent(ucm)
        assert op == "addAppServerInfo"
        assert text(body, "appServerInfo/appServerName") == "AppSrv1"

    def test_get_app_server_info(self, ucm):
        ucm.recorder.responses["getAppServerInfo"] = {
            "return": {"appServerInfo": {"appServerName": "AppSrv1"}}
        }
        result = ucm.get_app_server_info(uuid="{EEEE-5555}")
        op, body = sent(ucm)
        assert op == "getAppServerInfo"
        assert text(body, "uuid") == "{EEEE-5555}"
        assert result == {"appServerName": "AppSrv1"}

    def test_update_app_server_info(self, ucm):
        ucm.update_app_server_info(uuid="{EEEE-5555}", appServerContent="Updated")
        op, body = sent(ucm)
        assert op == "updateAppServerInfo"
        assert text(body, "uuid") == "{EEEE-5555}"

    def test_remove_app_server_info(self, ucm):
        ucm.remove_app_server_info(uuid="{EEEE-5555}")
        op, body = sent(ucm)
        assert op == "removeAppServerInfo"
        assert text(body, "uuid") == "{EEEE-5555}"


# ---------------------------------------------------------------------------
# ApplicationServer
# ---------------------------------------------------------------------------

class TestApplicationServer:
    def test_add_application_server(self, ucm):
        ucm.add_application_server(
            appServerType="EMService",
            name="AppServer1",
            ipAddress="10.0.0.1",
        )
        op, body = sent(ucm)
        assert op == "addApplicationServer"
        assert text(body, "applicationServer/name") == "AppServer1"

    def test_get_application_server(self, ucm):
        ucm.recorder.responses["getApplicationServer"] = {
            "return": {"applicationServer": {"name": "AppServer1"}}
        }
        result = ucm.get_application_server(uuid="{FFFF-6666}")
        op, body = sent(ucm)
        assert op == "getApplicationServer"
        assert text(body, "uuid") == "{FFFF-6666}"
        assert result == {"name": "AppServer1"}

    def test_get_application_servers(self, ucm):
        ucm.recorder.responses["listApplicationServer"] = {
            "return": {"applicationServer": [{"name": "AppServer1"}]}
        }
        result = ucm.get_application_servers()
        op, body = sent(ucm)
        assert op == "listApplicationServer"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_application_servers_empty(self, ucm):
        ucm.recorder.responses["listApplicationServer"] = {"return": None}
        result = ucm.get_application_servers()
        assert result == []

    def test_update_application_server(self, ucm):
        ucm.update_application_server(uuid="{FFFF-6666}", newName="AppServer1_new")
        op, body = sent(ucm)
        assert op == "updateApplicationServer"
        assert text(body, "uuid") == "{FFFF-6666}"

    def test_remove_application_server(self, ucm):
        ucm.remove_application_server(uuid="{FFFF-6666}")
        op, body = sent(ucm)
        assert op == "removeApplicationServer"
        assert text(body, "uuid") == "{FFFF-6666}"


# ---------------------------------------------------------------------------
# Change (listChange)
# ---------------------------------------------------------------------------

class TestChange:
    def test_list_changes_no_start_id(self, ucm):
        """First call: omit startChangeId (minOccurs=0 in AXL schema)."""
        ucm.recorder.responses["listChange"] = {
            "queueInfo": {"nextStartChangeId": 100, "queueId": "queue-abc"},
            "changes": {"change": []},
        }
        result = ucm.list_changes()
        op, body = sent(ucm)
        assert op == "listChange"
        # No startChangeId element should appear for first call
        assert not has(body, "startChangeId")
        assert result is not None

    def test_list_changes_with_start_id(self, ucm):
        """Subsequent call: pass startChangeId as zeep-compatible dict."""
        ucm.recorder.responses["listChange"] = {
            "queueInfo": {"nextStartChangeId": 200, "queueId": "queue-abc"},
            "changes": {"change": []},
        }
        result = ucm.list_changes(
            startChangeId={"_value_1": 100, "queueId": "queue-abc"}
        )
        op, body = sent(ucm)
        assert op == "listChange"
        assert has(body, "startChangeId")
        assert result is not None


# ---------------------------------------------------------------------------
# EnterpriseParametersReset
# ---------------------------------------------------------------------------

class TestEnterpriseParametersReset:
    def test_do_enterprise_parameters_reset(self, ucm):
        ucm.do_enterprise_parameters_reset()
        op, body = sent(ucm)
        assert op == "doEnterpriseParametersReset"


# ---------------------------------------------------------------------------
# PhoneNtp
# ---------------------------------------------------------------------------

class TestPhoneNtp:
    def test_add_phone_ntp_ipv4(self, ucm):
        # AXL XPhoneNtp requires both ipAddress and ipv6Address fields;
        # provide the unused one as an empty string.
        ucm.add_phone_ntp(
            ipAddress="10.0.0.100",
            ipv6Address="",
            description="Corp NTP",
            mode="Directed Broadcast",
        )
        op, body = sent(ucm)
        assert op == "addPhoneNtp"
        assert text(body, "phoneNtp/ipAddress") == "10.0.0.100"

    def test_add_phone_ntp_ipv6(self, ucm):
        ucm.add_phone_ntp(
            ipAddress="",
            ipv6Address="2001:db8::1",
            mode="Directed Broadcast",
        )
        op, body = sent(ucm)
        assert op == "addPhoneNtp"
        assert text(body, "phoneNtp/ipv6Address") == "2001:db8::1"

    def test_get_phone_ntp_by_uuid(self, ucm):
        ucm.recorder.responses["getPhoneNtp"] = {
            "return": {"phoneNtp": {"ipAddress": "10.0.0.100"}}
        }
        result = ucm.get_phone_ntp(uuid="{AAAA-9999}")
        op, body = sent(ucm)
        assert op == "getPhoneNtp"
        assert text(body, "uuid") == "{AAAA-9999}"
        assert result == {"ipAddress": "10.0.0.100"}

    def test_get_phone_ntp_by_ipaddress(self, ucm):
        """AXL choice: when not using uuid, pass both ipAddress+ipv6Address."""
        ucm.recorder.responses["getPhoneNtp"] = {
            "return": {"phoneNtp": {"ipAddress": "10.0.0.100"}}
        }
        ucm.get_phone_ntp(ipAddress="10.0.0.100", ipv6Address="")
        op, body = sent(ucm)
        assert op == "getPhoneNtp"
        assert text(body, "ipAddress") == "10.0.0.100"

    def test_get_phone_ntp_requires_identifier(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_phone_ntp()

    def test_get_phone_ntps(self, ucm):
        ucm.recorder.responses["listPhoneNtp"] = {
            "return": {"phoneNtp": [{"ipAddress": "10.0.0.100"}]}
        }
        result = ucm.get_phone_ntps()
        op, body = sent(ucm)
        assert op == "listPhoneNtp"
        assert len(result) == 1

    def test_get_phone_ntps_empty(self, ucm):
        ucm.recorder.responses["listPhoneNtp"] = {"return": None}
        result = ucm.get_phone_ntps()
        assert result == []

    def test_update_phone_ntp_by_uuid(self, ucm):
        ucm.update_phone_ntp(uuid="{AAAA-9999}", newIpAddress="10.0.0.101")
        op, body = sent(ucm)
        assert op == "updatePhoneNtp"
        assert text(body, "uuid") == "{AAAA-9999}"

    def test_update_phone_ntp_by_ipaddress(self, ucm):
        """AXL choice: when not using uuid, pass both ipAddress+ipv6Address."""
        ucm.update_phone_ntp(
            ipAddress="10.0.0.100", ipv6Address="", newIpAddress="10.0.0.101"
        )
        op, body = sent(ucm)
        assert op == "updatePhoneNtp"
        assert text(body, "ipAddress") == "10.0.0.100"
        assert text(body, "newIpAddress") == "10.0.0.101"

    def test_remove_phone_ntp_by_uuid(self, ucm):
        ucm.remove_phone_ntp(uuid="{AAAA-9999}")
        op, body = sent(ucm)
        assert op == "removePhoneNtp"
        assert text(body, "uuid") == "{AAAA-9999}"

    def test_remove_phone_ntp_by_ipaddress(self, ucm):
        """AXL choice: when not using uuid, pass both ipAddress+ipv6Address."""
        ucm.remove_phone_ntp(ipAddress="10.0.0.100", ipv6Address="")
        op, body = sent(ucm)
        assert op == "removePhoneNtp"
        assert text(body, "ipAddress") == "10.0.0.100"

    def test_remove_phone_ntp_requires_identifier(self, ucm):
        with pytest.raises(ValueError):
            ucm.remove_phone_ntp()


# ---------------------------------------------------------------------------
# SQLQueryInactive
# ---------------------------------------------------------------------------

class TestSQLQueryInactive:
    def test_sql_query_inactive_no_rows(self, ucm):
        ucm.recorder.responses["executeSQLQueryInactive"] = {"return": None}
        result = ucm.sql_query_inactive("SELECT 1 FROM device")
        op, body = sent(ucm)
        assert op == "executeSQLQueryInactive"
        assert text(body, "sql") == "SELECT 1 FROM device"
        assert result["num_rows"] == 0
        assert result["query"] == "SELECT 1 FROM device"
        assert "rows" not in result

    def test_sql_query_inactive_with_rows(self, ucm):
        # Build a fake row list that acts like lxml elements
        class FakeCol:
            def __init__(self, tag, text_val):
                self.tag = tag
                self.text = text_val

        class FakeRow(list):
            pass

        row = FakeRow([FakeCol("name", "SEP001122334455")])

        ucm.recorder.responses["executeSQLQueryInactive"] = {
            "return": {"row": [row]}
        }
        result = ucm.sql_query_inactive("SELECT name FROM device")
        assert result["num_rows"] == 1
        assert result["rows"][0]["name"] == "SEP001122334455"


# ---------------------------------------------------------------------------
# ServiceParametersReset
# ---------------------------------------------------------------------------

class TestServiceParametersReset:
    def test_do_service_parameters_reset(self, ucm):
        ucm.do_service_parameters_reset(
            processNodeName="pub.corp.com",
            service="Cisco CallManager",
        )
        op, body = sent(ucm)
        assert op == "doServiceParametersReset"
        assert text(body, "processNodeName") == "pub.corp.com"
        assert text(body, "service") == "Cisco CallManager"


# ---------------------------------------------------------------------------
# SyslogConfiguration
# ---------------------------------------------------------------------------

class TestSyslogConfiguration:
    def test_get_syslog_configuration(self, ucm):
        ucm.recorder.responses["getSyslogConfiguration"] = {
            "return": {"syslogConfiguration": {"serverName": "pub.corp.com"}}
        }
        result = ucm.get_syslog_configuration(
            serverName="pub.corp.com",
            serviceGroup="CM Services",
            service="Cisco CallManager",
        )
        op, body = sent(ucm)
        assert op == "getSyslogConfiguration"
        assert text(body, "serverName") == "pub.corp.com"
        assert text(body, "serviceGroup") == "CM Services"
        assert text(body, "service") == "Cisco CallManager"
        assert result == {"serverName": "pub.corp.com"}

    def test_update_syslog_configuration(self, ucm):
        # alarmConfigs requires 1-4 AlarmConfig elements (XSyslogConfig).
        # All XSyslogConfig fields within the sequence are required when present.
        alarm = {
            "AlarmLevelEvent": "Warning",
            "RemoteServerName1": "syslog.corp.com",
            "RemoteServerName2": "",
            "RemoteServerName3": "",
            "RemoteServerName4": "",
            "RemoteServerName5": "",
            "monitor": "Local1",
            "Enable": True,
        }
        ucm.update_syslog_configuration(
            serverName="pub.corp.com",
            serviceGroup="CM Services",
            service="Cisco CallManager",
            alarmConfigs={"AlarmConfig": [alarm]},
        )
        op, body = sent(ucm)
        assert op == "updateSyslogConfiguration"
        assert text(body, "serverName") == "pub.corp.com"


# ---------------------------------------------------------------------------
# AuthenticateUser
# ---------------------------------------------------------------------------

class TestAuthenticateUser:
    def test_do_authenticate_user_password(self, ucm):
        ucm.recorder.responses["doAuthenticateUser"] = {
            "return": {"userAuthenticated": "true", "code": 0}
        }
        result = ucm.do_authenticate_user(userid="jsmith", password="secret123")
        op, body = sent(ucm)
        assert op == "doAuthenticateUser"
        assert text(body, "userid") == "jsmith"
        assert text(body, "password") == "secret123"
        assert result["userAuthenticated"] == "true"

    def test_do_authenticate_user_pin(self, ucm):
        ucm.recorder.responses["doAuthenticateUser"] = {
            "return": {"userAuthenticated": "true"}
        }
        ucm.do_authenticate_user(userid="jsmith", pin="1234")
        op, body = sent(ucm)
        assert op == "doAuthenticateUser"
        assert text(body, "pin") == "1234"

    def test_do_authenticate_user_no_credentials(self, ucm):
        # Should succeed without password/pin (AXL allows it)
        ucm.do_authenticate_user(userid="jsmith")
        op, body = sent(ucm)
        assert op == "doAuthenticateUser"
        assert text(body, "userid") == "jsmith"


# ---------------------------------------------------------------------------
# CustomUserField
# ---------------------------------------------------------------------------

class TestCustomUserField:
    def test_add_custom_user_field(self, ucm):
        ucm.add_custom_user_field(field="customField1")
        op, body = sent(ucm)
        assert op == "addCustomUserField"
        assert text(body, "customUserField/field") == "customField1"

    def test_get_custom_user_field_by_field(self, ucm):
        ucm.recorder.responses["getCustomUserField"] = {
            "return": {"customUserField": {"field": "customField1"}}
        }
        result = ucm.get_custom_user_field(field="customField1")
        op, body = sent(ucm)
        assert op == "getCustomUserField"
        assert text(body, "field") == "customField1"
        assert result == {"field": "customField1"}

    def test_get_custom_user_field_by_uuid(self, ucm):
        ucm.recorder.responses["getCustomUserField"] = {
            "return": {"customUserField": {"field": "customField1"}}
        }
        ucm.get_custom_user_field(uuid="{AAAA-1111}")
        op, body = sent(ucm)
        assert op == "getCustomUserField"
        assert text(body, "uuid") == "{AAAA-1111}"

    def test_get_custom_user_field_requires_identifier(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_custom_user_field()

    def test_get_custom_user_fields(self, ucm):
        ucm.recorder.responses["listCustomUserField"] = {
            "return": {"customUserField": [{"field": "customField1"}]}
        }
        result = ucm.get_custom_user_fields()
        op, body = sent(ucm)
        assert op == "listCustomUserField"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_custom_user_fields_empty(self, ucm):
        ucm.recorder.responses["listCustomUserField"] = {"return": None}
        result = ucm.get_custom_user_fields()
        assert result == []

    def test_update_custom_user_field(self, ucm):
        ucm.update_custom_user_field(field="customField1", newField="customField1Renamed")
        op, body = sent(ucm)
        assert op == "updateCustomUserField"
        assert text(body, "field") == "customField1"
        assert text(body, "newField") == "customField1Renamed"

    def test_remove_custom_user_field_by_field(self, ucm):
        ucm.remove_custom_user_field(field="customField1")
        op, body = sent(ucm)
        assert op == "removeCustomUserField"
        assert text(body, "field") == "customField1"

    def test_remove_custom_user_field_by_uuid(self, ucm):
        ucm.remove_custom_user_field(uuid="{AAAA-1111}")
        op, body = sent(ucm)
        assert op == "removeCustomUserField"
        assert text(body, "uuid") == "{AAAA-1111}"

    def test_remove_custom_user_field_requires_identifier(self, ucm):
        with pytest.raises(ValueError):
            ucm.remove_custom_user_field()


# ---------------------------------------------------------------------------
# SelfProvisioning
# ---------------------------------------------------------------------------

class TestSelfProvisioning:
    def test_update_self_provisioning(self, ucm):
        ucm.update_self_provisioning(
            requireAuthentication="true",
            authenticationCode="8675",
        )
        op, body = sent(ucm)
        assert op == "updateSelfProvisioning"
        assert text(body, "requireAuthentication") == "true"
        assert text(body, "authenticationCode") == "8675"
