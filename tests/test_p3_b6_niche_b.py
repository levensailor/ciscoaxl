"""Offline tests for P3 Batch B6 — p3_niche_b.py

Verifies that every method in P3NicheB:
  * calls the correct AXL operation
  * passes the right element names and values
  * handles identifier routing (name vs uuid)
  * returns the unwrapped result or [] on empty

Run with: pytest tests/test_p3_b6_niche_b.py
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
# Shared test infrastructure
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
# HttpProfile
# ---------------------------------------------------------------------------

class TestHttpProfile:
    def test_add_http_profile(self, ucm):
        ucm.add_http_profile(
            name="TestHttpProfile",
            userName="admin",
            password="secret",
            webServiceRootUri="https://example.com/api",
        )
        op, body = sent(ucm)
        assert op == "addHttpProfile"
        assert text(body, "httpProfile/name") == "TestHttpProfile"

    def test_get_http_profile_by_name(self, ucm):
        ucm.recorder.responses["getHttpProfile"] = {
            "return": {"httpProfile": {"name": "TestHttpProfile"}}
        }
        result = ucm.get_http_profile(name="TestHttpProfile")
        op, body = sent(ucm)
        assert op == "getHttpProfile"
        assert text(body, "name") == "TestHttpProfile"
        assert result == {"name": "TestHttpProfile"}

    def test_get_http_profile_by_uuid(self, ucm):
        ucm.recorder.responses["getHttpProfile"] = {
            "return": {"httpProfile": {"name": "TestHttpProfile"}}
        }
        ucm.get_http_profile(uuid="{AAAA-1111}")
        op, body = sent(ucm)
        assert op == "getHttpProfile"
        assert text(body, "uuid") == "{AAAA-1111}"
        assert not has(body, "name")

    def test_get_http_profile_raises_on_both(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_http_profile(name="x", uuid="{AAAA-1111}")

    def test_get_http_profile_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_http_profile()

    def test_update_http_profile(self, ucm):
        ucm.update_http_profile(name="TestHttpProfile", webServiceRootUri="/api")
        op, body = sent(ucm)
        assert op == "updateHttpProfile"
        assert text(body, "name") == "TestHttpProfile"

    def test_remove_http_profile_by_name(self, ucm):
        ucm.remove_http_profile(name="TestHttpProfile")
        op, body = sent(ucm)
        assert op == "removeHttpProfile"
        assert text(body, "name") == "TestHttpProfile"

    def test_remove_http_profile_by_uuid(self, ucm):
        ucm.remove_http_profile(uuid="{AAAA-1111}")
        op, body = sent(ucm)
        assert op == "removeHttpProfile"
        assert text(body, "uuid") == "{AAAA-1111}"

    def test_remove_http_profile_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.remove_http_profile()


# ---------------------------------------------------------------------------
# InfrastructureDevice
# ---------------------------------------------------------------------------

class TestInfrastructureDevice:
    def test_add_infrastructure_device(self, ucm):
        ucm.add_infrastructure_device(name="switch-01")
        op, body = sent(ucm)
        assert op == "addInfrastructureDevice"
        assert text(body, "infrastructureDevice/name") == "switch-01"

    def test_get_infrastructure_device_by_uuid(self, ucm):
        ucm.recorder.responses["getInfrastructureDevice"] = {
            "return": {"infrastructureDevice": {"name": "switch-01"}}
        }
        result = ucm.get_infrastructure_device(uuid="{BBBB-2222}")
        op, body = sent(ucm)
        assert op == "getInfrastructureDevice"
        assert text(body, "uuid") == "{BBBB-2222}"
        assert result == {"name": "switch-01"}

    def test_get_infrastructure_device_raises_on_missing_uuid(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_infrastructure_device()

    def test_get_infrastructure_devices(self, ucm):
        ucm.recorder.responses["listInfrastructureDevice"] = {
            "return": {"infrastructureDevice": [{"name": "switch-01"}]}
        }
        result = ucm.get_infrastructure_devices()
        op, body = sent(ucm)
        assert op == "listInfrastructureDevice"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_infrastructure_devices_empty(self, ucm):
        ucm.recorder.responses["listInfrastructureDevice"] = {"return": None}
        result = ucm.get_infrastructure_devices()
        assert result == []

    def test_update_infrastructure_device(self, ucm):
        ucm.update_infrastructure_device(uuid="{BBBB-2222}")
        op, body = sent(ucm)
        assert op == "updateInfrastructureDevice"
        assert text(body, "uuid") == "{BBBB-2222}"

    def test_update_infrastructure_device_raises_on_missing_uuid(self, ucm):
        with pytest.raises(ValueError):
            ucm.update_infrastructure_device()

    def test_remove_infrastructure_device_by_uuid(self, ucm):
        ucm.remove_infrastructure_device(uuid="{BBBB-2222}")
        op, body = sent(ucm)
        assert op == "removeInfrastructureDevice"
        assert text(body, "uuid") == "{BBBB-2222}"

    def test_remove_infrastructure_device_raises_on_missing_uuid(self, ucm):
        with pytest.raises(ValueError):
            ucm.remove_infrastructure_device()


# ---------------------------------------------------------------------------
# InterClusterDirectoryUri
# ---------------------------------------------------------------------------

class TestInterClusterDirectoryUri:
    def test_update_inter_cluster_directory_uri(self, ucm):
        ucm.update_inter_cluster_directory_uri(
            exchangeDirectoryUri=True,
            routeString="cluster1.example.com",
        )
        op, body = sent(ucm)
        assert op == "updateInterClusterDirectoryUri"
        assert text(body, "routeString") == "cluster1.example.com"


# ---------------------------------------------------------------------------
# InterClusterServiceProfile
# ---------------------------------------------------------------------------

class TestInterClusterServiceProfile:
    def test_get_inter_cluster_service_profile_by_service(self, ucm):
        ucm.recorder.responses["getInterClusterServiceProfile"] = {
            "return": {"interClusterServiceProfile": {"interClusterService": "svc1"}}
        }
        result = ucm.get_inter_cluster_service_profile(interClusterService="svc1")
        op, body = sent(ucm)
        assert op == "getInterClusterServiceProfile"
        assert text(body, "interClusterService") == "svc1"
        assert result == {"interClusterService": "svc1"}

    def test_get_inter_cluster_service_profile_by_uuid(self, ucm):
        ucm.recorder.responses["getInterClusterServiceProfile"] = {
            "return": {"interClusterServiceProfile": {"interClusterService": "svc1"}}
        }
        ucm.get_inter_cluster_service_profile(uuid="{CCCC-3333}")
        op, body = sent(ucm)
        assert op == "getInterClusterServiceProfile"
        assert text(body, "uuid") == "{CCCC-3333}"

    def test_get_inter_cluster_service_profile_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_inter_cluster_service_profile()

    def test_update_inter_cluster_service_profile(self, ucm):
        ucm.update_inter_cluster_service_profile(
            interClusterService="svc1", isActivated=True
        )
        op, body = sent(ucm)
        assert op == "updateInterClusterServiceProfile"
        assert text(body, "interClusterService") == "svc1"


# ---------------------------------------------------------------------------
# IvrUserLocale
# ---------------------------------------------------------------------------

class TestIvrUserLocale:
    def test_add_ivr_user_locale(self, ucm):
        ucm.add_ivr_user_locale(userLocale="English_United_States", orderIndex=1)
        op, body = sent(ucm)
        assert op == "addIvrUserLocale"

    def test_get_ivr_user_locale_by_locale(self, ucm):
        ucm.recorder.responses["getIvrUserLocale"] = {
            "return": {"ivrUserLocale": {"userLocale": "English_United_States"}}
        }
        result = ucm.get_ivr_user_locale(userLocale="English_United_States")
        op, body = sent(ucm)
        assert op == "getIvrUserLocale"
        assert text(body, "userLocale") == "English_United_States"
        assert result == {"userLocale": "English_United_States"}

    def test_get_ivr_user_locale_by_uuid(self, ucm):
        ucm.recorder.responses["getIvrUserLocale"] = {
            "return": {"ivrUserLocale": {"userLocale": "English_United_States"}}
        }
        ucm.get_ivr_user_locale(uuid="{DDDD-4444}")
        op, body = sent(ucm)
        assert op == "getIvrUserLocale"
        assert text(body, "uuid") == "{DDDD-4444}"

    def test_get_ivr_user_locale_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_ivr_user_locale()

    def test_get_ivr_user_locales(self, ucm):
        ucm.recorder.responses["listIvrUserLocale"] = {
            "return": {"ivrUserLocale": [{"userLocale": "English_United_States"}]}
        }
        result = ucm.get_ivr_user_locales()
        op, body = sent(ucm)
        assert op == "listIvrUserLocale"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_ivr_user_locales_empty(self, ucm):
        ucm.recorder.responses["listIvrUserLocale"] = {"return": None}
        result = ucm.get_ivr_user_locales()
        assert result == []

    def test_update_ivr_user_locale(self, ucm):
        ucm.update_ivr_user_locale(userLocale="English_United_States")
        op, body = sent(ucm)
        assert op == "updateIvrUserLocale"
        assert text(body, "userLocale") == "English_United_States"

    def test_remove_ivr_user_locale_by_locale(self, ucm):
        ucm.remove_ivr_user_locale(userLocale="English_United_States")
        op, body = sent(ucm)
        assert op == "removeIvrUserLocale"
        assert text(body, "userLocale") == "English_United_States"

    def test_remove_ivr_user_locale_by_uuid(self, ucm):
        ucm.remove_ivr_user_locale(uuid="{DDDD-4444}")
        op, body = sent(ucm)
        assert op == "removeIvrUserLocale"
        assert text(body, "uuid") == "{DDDD-4444}"

    def test_remove_ivr_user_locale_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.remove_ivr_user_locale()


# ---------------------------------------------------------------------------
# MlppDomain
# ---------------------------------------------------------------------------

class TestMlppDomain:
    def test_add_mlpp_domain(self, ucm):
        ucm.add_mlpp_domain(domainName="TestDomain", domainId="ABCDEF")
        op, body = sent(ucm)
        assert op == "addMlppDomain"
        assert text(body, "mlppDomain/domainName") == "TestDomain"

    def test_get_mlpp_domain_by_domain_name(self, ucm):
        ucm.recorder.responses["getMlppDomain"] = {
            "return": {"mlppDomain": {"domainName": "TestDomain"}}
        }
        result = ucm.get_mlpp_domain(domainName="TestDomain")
        op, body = sent(ucm)
        assert op == "getMlppDomain"
        assert text(body, "domainName") == "TestDomain"
        assert result == {"domainName": "TestDomain"}

    def test_get_mlpp_domain_by_uuid(self, ucm):
        ucm.recorder.responses["getMlppDomain"] = {
            "return": {"mlppDomain": {"domainName": "TestDomain"}}
        }
        ucm.get_mlpp_domain(uuid="{EEEE-5555}")
        op, body = sent(ucm)
        assert op == "getMlppDomain"
        assert text(body, "uuid") == "{EEEE-5555}"

    def test_get_mlpp_domain_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_mlpp_domain()

    def test_get_mlpp_domains(self, ucm):
        ucm.recorder.responses["listMlppDomain"] = {
            "return": {"mlppDomain": [{"domainName": "TestDomain"}]}
        }
        result = ucm.get_mlpp_domains()
        op, body = sent(ucm)
        assert op == "listMlppDomain"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_mlpp_domains_empty(self, ucm):
        ucm.recorder.responses["listMlppDomain"] = {"return": None}
        result = ucm.get_mlpp_domains()
        assert result == []

    def test_update_mlpp_domain(self, ucm):
        ucm.update_mlpp_domain(domainName="TestDomain", newDomainName="NewTestDomain")
        op, body = sent(ucm)
        assert op == "updateMlppDomain"
        assert text(body, "domainName") == "TestDomain"

    def test_remove_mlpp_domain_by_domain_name(self, ucm):
        ucm.remove_mlpp_domain(domainName="TestDomain")
        op, body = sent(ucm)
        assert op == "removeMlppDomain"
        assert text(body, "domainName") == "TestDomain"

    def test_remove_mlpp_domain_by_uuid(self, ucm):
        ucm.remove_mlpp_domain(uuid="{EEEE-5555}")
        op, body = sent(ucm)
        assert op == "removeMlppDomain"
        assert text(body, "uuid") == "{EEEE-5555}"

    def test_remove_mlpp_domain_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.remove_mlpp_domain()


# ---------------------------------------------------------------------------
# MobileSmartClientProfile
# ---------------------------------------------------------------------------

class TestMobileSmartClientProfile:
    def test_get_mobile_smart_client_profile_by_name(self, ucm):
        ucm.recorder.responses["getMobileSmartClientProfile"] = {
            "return": {"mobileSmartClientProfile": {"name": "DefaultMobileProfile"}}
        }
        result = ucm.get_mobile_smart_client_profile(name="DefaultMobileProfile")
        op, body = sent(ucm)
        assert op == "getMobileSmartClientProfile"
        assert text(body, "name") == "DefaultMobileProfile"
        assert result == {"name": "DefaultMobileProfile"}

    def test_get_mobile_smart_client_profile_by_uuid(self, ucm):
        ucm.recorder.responses["getMobileSmartClientProfile"] = {
            "return": {"mobileSmartClientProfile": {"name": "DefaultMobileProfile"}}
        }
        ucm.get_mobile_smart_client_profile(uuid="{FFFF-6666}")
        op, body = sent(ucm)
        assert op == "getMobileSmartClientProfile"
        assert text(body, "uuid") == "{FFFF-6666}"

    def test_get_mobile_smart_client_profile_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_mobile_smart_client_profile()

    def test_get_mobile_smart_client_profiles(self, ucm):
        ucm.recorder.responses["listMobileSmartClientProfile"] = {
            "return": {"mobileSmartClientProfile": [{"name": "DefaultMobileProfile"}]}
        }
        result = ucm.get_mobile_smart_client_profiles(
            tagfilter={"name": "", "mobileSmartClient": ""}
        )
        op, body = sent(ucm)
        assert op == "listMobileSmartClientProfile"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_mobile_smart_client_profiles_empty(self, ucm):
        ucm.recorder.responses["listMobileSmartClientProfile"] = {"return": None}
        result = ucm.get_mobile_smart_client_profiles(
            tagfilter={"name": "", "mobileSmartClient": ""}
        )
        assert result == []


# ---------------------------------------------------------------------------
# NetworkAccessProfile
# ---------------------------------------------------------------------------

class TestNetworkAccessProfile:
    def test_add_network_access_profile(self, ucm):
        ucm.add_network_access_profile(
            name="TestNAP",
            description="Test Profile",
            proxySettings="Manual",
            proxyHostname="proxy.example.com",
        )
        op, body = sent(ucm)
        assert op == "addNetworkAccessProfile"
        assert text(body, "networkAccessProfile/name") == "TestNAP"

    def test_get_network_access_profile_by_name(self, ucm):
        ucm.recorder.responses["getNetworkAccessProfile"] = {
            "return": {"networkAccessProfile": {"name": "TestNAP"}}
        }
        result = ucm.get_network_access_profile(name="TestNAP")
        op, body = sent(ucm)
        assert op == "getNetworkAccessProfile"
        assert text(body, "name") == "TestNAP"
        assert result == {"name": "TestNAP"}

    def test_get_network_access_profile_by_uuid(self, ucm):
        ucm.recorder.responses["getNetworkAccessProfile"] = {
            "return": {"networkAccessProfile": {"name": "TestNAP"}}
        }
        ucm.get_network_access_profile(uuid="{GGGG-7777}")
        op, body = sent(ucm)
        assert op == "getNetworkAccessProfile"
        assert text(body, "uuid") == "{GGGG-7777}"

    def test_get_network_access_profile_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_network_access_profile()

    def test_get_network_access_profiles(self, ucm):
        ucm.recorder.responses["listNetworkAccessProfile"] = {
            "return": {"networkAccessProfile": [{"name": "TestNAP"}]}
        }
        result = ucm.get_network_access_profiles()
        op, body = sent(ucm)
        assert op == "listNetworkAccessProfile"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_network_access_profiles_empty(self, ucm):
        ucm.recorder.responses["listNetworkAccessProfile"] = {"return": None}
        result = ucm.get_network_access_profiles()
        assert result == []

    def test_update_network_access_profile(self, ucm):
        ucm.update_network_access_profile(name="TestNAP", description="Updated")
        op, body = sent(ucm)
        assert op == "updateNetworkAccessProfile"
        assert text(body, "name") == "TestNAP"

    def test_remove_network_access_profile_by_name(self, ucm):
        ucm.remove_network_access_profile(name="TestNAP")
        op, body = sent(ucm)
        assert op == "removeNetworkAccessProfile"
        assert text(body, "name") == "TestNAP"

    def test_remove_network_access_profile_by_uuid(self, ucm):
        ucm.remove_network_access_profile(uuid="{GGGG-7777}")
        op, body = sent(ucm)
        assert op == "removeNetworkAccessProfile"
        assert text(body, "uuid") == "{GGGG-7777}"

    def test_remove_network_access_profile_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.remove_network_access_profile()


# ---------------------------------------------------------------------------
# PageLayoutPreferences
# ---------------------------------------------------------------------------

class TestPageLayoutPreferences:
    def test_get_page_layout_preferences(self, ucm):
        ucm.recorder.responses["getPageLayoutPreferences"] = {
            "return": {"pageLayoutPreferences": {"pageName": "Phones"}}
        }
        result = ucm.get_page_layout_preferences(pageName="Phones")
        op, body = sent(ucm)
        assert op == "getPageLayoutPreferences"
        assert text(body, "pageName") == "Phones"
        assert result == {"pageName": "Phones"}

    def test_update_page_layout_preferences(self, ucm):
        ucm.update_page_layout_preferences(
            pageName="Phones",
            pageSections={
                "pageSection": [{"name": "Device Information", "state": "show", "order": "0"}]
            },
        )
        op, body = sent(ucm)
        assert op == "updatePageLayoutPreferences"
        assert text(body, "pageName") == "Phones"


# ---------------------------------------------------------------------------
# PhoneTypeDisplayInstance
# ---------------------------------------------------------------------------

class TestPhoneTypeDisplayInstance:
    def test_get_phone_type_display_instance(self, ucm):
        ucm.recorder.responses["getPhoneTypeDisplayInstance"] = {
            "return": {"phoneTypeDisplayInstance": {"productName": "Cisco 7960"}}
        }
        result = ucm.get_phone_type_display_instance(
            productName="Cisco 7960",
            protocol="SCCP",
            trunkType="None",
        )
        op, body = sent(ucm)
        assert op == "getPhoneTypeDisplayInstance"
        assert text(body, "productName") == "Cisco 7960"
        assert text(body, "protocol") == "SCCP"
        assert result == {"productName": "Cisco 7960"}

    def test_get_phone_type_display_instance_raises_on_missing_product_name(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_phone_type_display_instance()


# ---------------------------------------------------------------------------
# ResourcePriorityNamespace
# ---------------------------------------------------------------------------

class TestResourcePriorityNamespace:
    def test_add_resource_priority_namespace(self, ucm):
        ucm.add_resource_priority_namespace(
            namespace="dsn.mil", description="DSN namespace"
        )
        op, body = sent(ucm)
        assert op == "addResourcePriorityNamespace"
        assert text(body, "resourcePriorityNamespace/namespace") == "dsn.mil"

    def test_get_resource_priority_namespace_by_namespace(self, ucm):
        ucm.recorder.responses["getResourcePriorityNamespace"] = {
            "return": {"resourcePriorityNamespace": {"namespace": "dsn.mil"}}
        }
        result = ucm.get_resource_priority_namespace(namespace="dsn.mil")
        op, body = sent(ucm)
        assert op == "getResourcePriorityNamespace"
        assert text(body, "namespace") == "dsn.mil"
        assert result == {"namespace": "dsn.mil"}

    def test_get_resource_priority_namespace_by_uuid(self, ucm):
        ucm.recorder.responses["getResourcePriorityNamespace"] = {
            "return": {"resourcePriorityNamespace": {"namespace": "dsn.mil"}}
        }
        ucm.get_resource_priority_namespace(uuid="{IIII-9999}")
        op, body = sent(ucm)
        assert op == "getResourcePriorityNamespace"
        assert text(body, "uuid") == "{IIII-9999}"

    def test_get_resource_priority_namespace_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_resource_priority_namespace()

    def test_get_resource_priority_namespaces(self, ucm):
        ucm.recorder.responses["listResourcePriorityNamespace"] = {
            "return": {"resourcePriorityNamespace": [{"namespace": "dsn.mil"}]}
        }
        result = ucm.get_resource_priority_namespaces()
        op, body = sent(ucm)
        assert op == "listResourcePriorityNamespace"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_resource_priority_namespaces_empty(self, ucm):
        ucm.recorder.responses["listResourcePriorityNamespace"] = {"return": None}
        result = ucm.get_resource_priority_namespaces()
        assert result == []

    def test_update_resource_priority_namespace(self, ucm):
        ucm.update_resource_priority_namespace(namespace="dsn.mil", description="Updated")
        op, body = sent(ucm)
        assert op == "updateResourcePriorityNamespace"
        assert text(body, "namespace") == "dsn.mil"

    def test_remove_resource_priority_namespace_by_namespace(self, ucm):
        ucm.remove_resource_priority_namespace(namespace="dsn.mil")
        op, body = sent(ucm)
        assert op == "removeResourcePriorityNamespace"
        assert text(body, "namespace") == "dsn.mil"

    def test_remove_resource_priority_namespace_by_uuid(self, ucm):
        ucm.remove_resource_priority_namespace(uuid="{IIII-9999}")
        op, body = sent(ucm)
        assert op == "removeResourcePriorityNamespace"
        assert text(body, "uuid") == "{IIII-9999}"

    def test_remove_resource_priority_namespace_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.remove_resource_priority_namespace()

    def test_reset_resource_priority_namespace(self, ucm):
        ucm.reset_resource_priority_namespace(namespace="dsn.mil")
        op, body = sent(ucm)
        assert op == "resetResourcePriorityNamespace"
        assert text(body, "namespace") == "dsn.mil"

    def test_restart_resource_priority_namespace(self, ucm):
        ucm.restart_resource_priority_namespace(namespace="dsn.mil")
        op, body = sent(ucm)
        assert op == "restartResourcePriorityNamespace"
        assert text(body, "namespace") == "dsn.mil"

    def test_apply_resource_priority_namespace(self, ucm):
        ucm.apply_resource_priority_namespace(namespace="dsn.mil")
        op, body = sent(ucm)
        assert op == "applyResourcePriorityNamespace"
        assert text(body, "namespace") == "dsn.mil"


# ---------------------------------------------------------------------------
# ResourcePriorityNamespaceList
# ---------------------------------------------------------------------------

class TestResourcePriorityNamespaceList:
    def test_add_resource_priority_namespace_list(self, ucm):
        ucm.add_resource_priority_namespace_list(
            name="TestNSList", description="Test list"
        )
        op, body = sent(ucm)
        assert op == "addResourcePriorityNamespaceList"
        assert text(body, "resourcePriorityNamespaceList/name") == "TestNSList"

    def test_get_resource_priority_namespace_list_by_name(self, ucm):
        ucm.recorder.responses["getResourcePriorityNamespaceList"] = {
            "return": {"resourcePriorityNamespaceList": {"name": "TestNSList"}}
        }
        result = ucm.get_resource_priority_namespace_list(name="TestNSList")
        op, body = sent(ucm)
        assert op == "getResourcePriorityNamespaceList"
        assert text(body, "name") == "TestNSList"
        assert result == {"name": "TestNSList"}

    def test_get_resource_priority_namespace_list_by_uuid(self, ucm):
        ucm.recorder.responses["getResourcePriorityNamespaceList"] = {
            "return": {"resourcePriorityNamespaceList": {"name": "TestNSList"}}
        }
        ucm.get_resource_priority_namespace_list(uuid="{JJJJ-0000}")
        op, body = sent(ucm)
        assert op == "getResourcePriorityNamespaceList"
        assert text(body, "uuid") == "{JJJJ-0000}"

    def test_get_resource_priority_namespace_list_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_resource_priority_namespace_list()

    def test_get_resource_priority_namespace_lists(self, ucm):
        ucm.recorder.responses["listResourcePriorityNamespaceList"] = {
            "return": {"resourcePriorityNamespaceList": [{"name": "TestNSList"}]}
        }
        result = ucm.get_resource_priority_namespace_lists()
        op, body = sent(ucm)
        assert op == "listResourcePriorityNamespaceList"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_resource_priority_namespace_lists_empty(self, ucm):
        ucm.recorder.responses["listResourcePriorityNamespaceList"] = {"return": None}
        result = ucm.get_resource_priority_namespace_lists()
        assert result == []

    def test_update_resource_priority_namespace_list(self, ucm):
        ucm.update_resource_priority_namespace_list(name="TestNSList", description="Updated")
        op, body = sent(ucm)
        assert op == "updateResourcePriorityNamespaceList"
        assert text(body, "name") == "TestNSList"

    def test_remove_resource_priority_namespace_list_by_name(self, ucm):
        ucm.remove_resource_priority_namespace_list(name="TestNSList")
        op, body = sent(ucm)
        assert op == "removeResourcePriorityNamespaceList"
        assert text(body, "name") == "TestNSList"

    def test_remove_resource_priority_namespace_list_by_uuid(self, ucm):
        ucm.remove_resource_priority_namespace_list(uuid="{JJJJ-0000}")
        op, body = sent(ucm)
        assert op == "removeResourcePriorityNamespaceList"
        assert text(body, "uuid") == "{JJJJ-0000}"

    def test_remove_resource_priority_namespace_list_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.remove_resource_priority_namespace_list()

    def test_reset_resource_priority_namespace_list(self, ucm):
        ucm.reset_resource_priority_namespace_list(name="TestNSList")
        op, body = sent(ucm)
        assert op == "resetResourcePriorityNamespaceList"
        assert text(body, "name") == "TestNSList"

    def test_restart_resource_priority_namespace_list(self, ucm):
        ucm.restart_resource_priority_namespace_list(name="TestNSList")
        op, body = sent(ucm)
        assert op == "restartResourcePriorityNamespaceList"
        assert text(body, "name") == "TestNSList"

    def test_apply_resource_priority_namespace_list(self, ucm):
        ucm.apply_resource_priority_namespace_list(name="TestNSList")
        op, body = sent(ucm)
        assert op == "applyResourcePriorityNamespaceList"
        assert text(body, "name") == "TestNSList"


# ---------------------------------------------------------------------------
# RoutePartitionsForLearnedPatterns
# ---------------------------------------------------------------------------

class TestRoutePartitionsForLearnedPatterns:
    def test_update_route_partitions_for_learned_patterns(self, ucm):
        ucm.update_route_partitions_for_learned_patterns(
            partitionForEnterpriseANo="PT_ENT_ALT",
            partitionForE164ANo="PT_E164_ALT",
            partitionForEnterprisePatterns="PT_ENT",
            partitionForE164Pattern="PT_E164",
            markLearnedEntAltNumbers=True,
            markLearnedE164AltNumbers=True,
            markFixedLengthEntPatterns=True,
            markVariableLengthEntPatterns=True,
            markFixedLengthE164Patterns=True,
            markVariableLengthE164Patterns=True,
        )
        op, body = sent(ucm)
        assert op == "updateRoutePartitionsForLearnedPatterns"
        assert text(body, "partitionForEnterpriseANo") == "PT_ENT_ALT"
        assert text(body, "partitionForE164ANo") == "PT_E164_ALT"


# ---------------------------------------------------------------------------
# SdpTransparencyProfile
# ---------------------------------------------------------------------------

class TestSdpTransparencyProfile:
    def test_add_sdp_transparency_profile(self, ucm):
        ucm.add_sdp_transparency_profile(
            name="TestSDP",
            description="SDP Profile",
            attributeSet=[
                {
                    "attributeNameString": "sendrecv",
                    "sdpAttributeHandling": "forward",
                }
            ],
        )
        op, body = sent(ucm)
        assert op == "addSdpTransparencyProfile"
        assert text(body, "sdpTransparencyProfile/name") == "TestSDP"

    def test_get_sdp_transparency_profile_by_name(self, ucm):
        ucm.recorder.responses["getSdpTransparencyProfile"] = {
            "return": {"sdpTransparencyProfile": {"name": "TestSDP"}}
        }
        result = ucm.get_sdp_transparency_profile(name="TestSDP")
        op, body = sent(ucm)
        assert op == "getSdpTransparencyProfile"
        assert text(body, "name") == "TestSDP"
        assert result == {"name": "TestSDP"}

    def test_get_sdp_transparency_profile_by_uuid(self, ucm):
        ucm.recorder.responses["getSdpTransparencyProfile"] = {
            "return": {"sdpTransparencyProfile": {"name": "TestSDP"}}
        }
        ucm.get_sdp_transparency_profile(uuid="{KKKK-1111}")
        op, body = sent(ucm)
        assert op == "getSdpTransparencyProfile"
        assert text(body, "uuid") == "{KKKK-1111}"

    def test_get_sdp_transparency_profile_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_sdp_transparency_profile()

    def test_get_sdp_transparency_profiles(self, ucm):
        ucm.recorder.responses["listSdpTransparencyProfile"] = {
            "return": {"sdpTransparencyProfile": [{"name": "TestSDP"}]}
        }
        result = ucm.get_sdp_transparency_profiles()
        op, body = sent(ucm)
        assert op == "listSdpTransparencyProfile"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_sdp_transparency_profiles_empty(self, ucm):
        ucm.recorder.responses["listSdpTransparencyProfile"] = {"return": None}
        result = ucm.get_sdp_transparency_profiles()
        assert result == []

    def test_update_sdp_transparency_profile(self, ucm):
        ucm.update_sdp_transparency_profile(name="TestSDP", description="Updated")
        op, body = sent(ucm)
        assert op == "updateSdpTransparencyProfile"
        assert text(body, "name") == "TestSDP"

    def test_remove_sdp_transparency_profile_by_name(self, ucm):
        ucm.remove_sdp_transparency_profile(name="TestSDP")
        op, body = sent(ucm)
        assert op == "removeSdpTransparencyProfile"
        assert text(body, "name") == "TestSDP"

    def test_remove_sdp_transparency_profile_by_uuid(self, ucm):
        ucm.remove_sdp_transparency_profile(uuid="{KKKK-1111}")
        op, body = sent(ucm)
        assert op == "removeSdpTransparencyProfile"
        assert text(body, "uuid") == "{KKKK-1111}"

    def test_remove_sdp_transparency_profile_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.remove_sdp_transparency_profile()


# ---------------------------------------------------------------------------
# TransportSettings / UpdateTransportSettings
# ---------------------------------------------------------------------------

class TestTransportSettings:
    def test_get_transport_settings(self, ucm):
        ucm.recorder.responses["getTransportSettings"] = {
            "return": {"TransportSettings": {"transportmode": "HTTPS"}}
        }
        result = ucm.get_transport_settings()
        op, _ = sent(ucm)
        assert op == "getTransportSettings"
        assert result["transportmode"] == "HTTPS"

    def test_do_update_transport_settings(self, ucm):
        ucm.do_update_transport_settings(
            transportMode="HTTPS",
            url="https://cucm.example.com",
            httpHost="proxy.example.com",
            httpPort="8080",
            enableProxyAuthentication="false",
            proxyUserName="",
            proxyPassword="",
        )
        op, body = sent(ucm)
        assert op == "doUpdateTransportSettings"
        assert text(body, "transportMode") == "HTTPS"


# ---------------------------------------------------------------------------
# VohServer
# ---------------------------------------------------------------------------

class TestVohServer:
    def test_add_voh_server(self, ucm):
        ucm.add_voh_server(
            name="TestVoH",
            description="Test VoH Server",
            sipTrunkName="SIP-TRUNK",
            defaultVideoStreamId="stream1",
        )
        op, body = sent(ucm)
        assert op == "addVohServer"
        assert text(body, "vohServer/name") == "TestVoH"

    def test_get_voh_server_by_name(self, ucm):
        ucm.recorder.responses["getVohServer"] = {
            "return": {"vohServer": {"name": "TestVoH"}}
        }
        result = ucm.get_voh_server(name="TestVoH")
        op, body = sent(ucm)
        assert op == "getVohServer"
        assert text(body, "name") == "TestVoH"
        assert result == {"name": "TestVoH"}

    def test_get_voh_server_by_uuid(self, ucm):
        ucm.recorder.responses["getVohServer"] = {
            "return": {"vohServer": {"name": "TestVoH"}}
        }
        ucm.get_voh_server(uuid="{LLLL-2222}")
        op, body = sent(ucm)
        assert op == "getVohServer"
        assert text(body, "uuid") == "{LLLL-2222}"

    def test_get_voh_server_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_voh_server()

    def test_get_voh_servers(self, ucm):
        ucm.recorder.responses["listVohServer"] = {
            "return": {"vohServer": [{"name": "TestVoH"}]}
        }
        result = ucm.get_voh_servers()
        op, body = sent(ucm)
        assert op == "listVohServer"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_voh_servers_empty(self, ucm):
        ucm.recorder.responses["listVohServer"] = {"return": None}
        result = ucm.get_voh_servers()
        assert result == []

    def test_update_voh_server(self, ucm):
        ucm.update_voh_server(name="TestVoH", description="Updated")
        op, body = sent(ucm)
        assert op == "updateVohServer"
        assert text(body, "name") == "TestVoH"

    def test_remove_voh_server_by_name(self, ucm):
        ucm.remove_voh_server(name="TestVoH")
        op, body = sent(ucm)
        assert op == "removeVohServer"
        assert text(body, "name") == "TestVoH"

    def test_remove_voh_server_by_uuid(self, ucm):
        ucm.remove_voh_server(uuid="{LLLL-2222}")
        op, body = sent(ucm)
        assert op == "removeVohServer"
        assert text(body, "uuid") == "{LLLL-2222}"

    def test_remove_voh_server_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.remove_voh_server()
