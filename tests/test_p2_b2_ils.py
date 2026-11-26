"""Offline tests for P2 Batch B2 — p2_ils.py

Verifies that every method in P2Ils:
  * calls the correct AXL operation
  * passes the right element names and values
  * handles identifier routing (name/pattern/clusterId vs uuid)
  * returns the unwrapped result or [] on empty

Run with: pytest tests/test_p2_b2_ils.py
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
# AdvertisedPatterns
# ---------------------------------------------------------------------------

class TestAdvertisedPatterns:
    def test_add_advertised_pattern(self, ucm):
        ucm.add_advertised_pattern(
            pattern="5XXX",
            pstnFailStrip=0,
        )
        op, body = sent(ucm)
        assert op == "addAdvertisedPatterns"
        assert text(body, "advertisedPatterns/pattern") == "5XXX"

    def test_get_advertised_pattern_by_pattern(self, ucm):
        ucm.recorder.responses["getAdvertisedPatterns"] = {
            "return": {"advertisedPatterns": {"pattern": "5XXX"}}
        }
        result = ucm.get_advertised_pattern(pattern="5XXX")
        op, body = sent(ucm)
        assert op == "getAdvertisedPatterns"
        assert text(body, "pattern") == "5XXX"
        assert result == {"pattern": "5XXX"}

    def test_get_advertised_pattern_by_uuid(self, ucm):
        ucm.recorder.responses["getAdvertisedPatterns"] = {
            "return": {"advertisedPatterns": {"pattern": "5XXX"}}
        }
        ucm.get_advertised_pattern(uuid="{AAAA-1111}")
        op, body = sent(ucm)
        assert op == "getAdvertisedPatterns"
        assert text(body, "uuid") == "{AAAA-1111}"
        assert not has(body, "pattern")

    def test_get_advertised_pattern_raises_on_both(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_advertised_pattern(pattern="5XXX", uuid="{AAAA-1111}")

    def test_get_advertised_pattern_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_advertised_pattern()

    def test_get_advertised_patterns(self, ucm):
        ucm.recorder.responses["listAdvertisedPatterns"] = {
            "return": {"advertisedPatterns": [{"pattern": "5XXX"}]}
        }
        result = ucm.get_advertised_patterns()
        op, body = sent(ucm)
        assert op == "listAdvertisedPatterns"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_advertised_patterns_empty(self, ucm):
        ucm.recorder.responses["listAdvertisedPatterns"] = {"return": None}
        result = ucm.get_advertised_patterns()
        assert result == []

    def test_update_advertised_pattern(self, ucm):
        ucm.update_advertised_pattern(pattern="5XXX", description="Updated")
        op, body = sent(ucm)
        assert op == "updateAdvertisedPatterns"
        assert text(body, "pattern") == "5XXX"

    def test_remove_advertised_pattern_by_pattern(self, ucm):
        ucm.remove_advertised_pattern(pattern="5XXX")
        op, body = sent(ucm)
        assert op == "removeAdvertisedPatterns"
        assert text(body, "pattern") == "5XXX"

    def test_remove_advertised_pattern_by_uuid(self, ucm):
        ucm.remove_advertised_pattern(uuid="{AAAA-1111}")
        op, body = sent(ucm)
        assert op == "removeAdvertisedPatterns"
        assert text(body, "uuid") == "{AAAA-1111}"
        assert not has(body, "pattern")


# ---------------------------------------------------------------------------
# IlsConfig
# ---------------------------------------------------------------------------

class TestIlsConfig:
    def test_get_ils_config(self, ucm):
        ucm.recorder.responses["getIlsConfig"] = {
            "return": {"ilsConfig": {"role": "Hub Cluster"}}
        }
        result = ucm.get_ils_config()
        op, body = sent(ucm)
        assert op == "getIlsConfig"
        assert result == {"role": "Hub Cluster"}

    def test_get_ils_config_with_cluster_id(self, ucm):
        ucm.recorder.responses["getIlsConfig"] = {
            "return": {"ilsConfig": {"role": "Spoke Cluster"}}
        }
        ucm.get_ils_config(clusterId="cluster1")
        op, body = sent(ucm)
        assert op == "getIlsConfig"
        assert text(body, "clusterId") == "cluster1"

    def test_update_ils_config(self, ucm):
        # All fields in UpdateIlsConfigReq are schema-required
        ucm.update_ils_config(
            role="Hub Cluster",
            registrationServer="10.0.0.1",
            activateIls=True,
            synchronizeClustersEvery="30",
            activatedServers="",
            deactivatedServers="",
            useTls=False,
            enableUsePassword=False,
            usePassword="",
        )
        op, body = sent(ucm)
        assert op == "updateIlsConfig"
        assert text(body, "role") == "Hub Cluster"
        assert text(body, "registrationServer") == "10.0.0.1"


# ---------------------------------------------------------------------------
# ImportedDirectoryUriCatalogs
# ---------------------------------------------------------------------------

class TestImportedDirectoryUriCatalogs:
    def test_add_imported_directory_uri_catalog(self, ucm):
        ucm.add_imported_directory_uri_catalog(
            name="TestCatalog",
            routeString="cluster1.example.com",
        )
        op, body = sent(ucm)
        assert op == "addImportedDirectoryUriCatalogs"
        assert text(body, "importedDirectoryUriCatalogs/name") == "TestCatalog"
        assert text(body, "importedDirectoryUriCatalogs/routeString") == "cluster1.example.com"

    def test_get_imported_directory_uri_catalog(self, ucm):
        ucm.recorder.responses["getImportedDirectoryUriCatalogs"] = {
            "return": {"importedDirectoryUriCatalogs": {"name": "TestCatalog"}}
        }
        result = ucm.get_imported_directory_uri_catalog(name="TestCatalog")
        op, body = sent(ucm)
        assert op == "getImportedDirectoryUriCatalogs"
        assert text(body, "name") == "TestCatalog"
        assert result == {"name": "TestCatalog"}

    def test_get_imported_directory_uri_catalog_by_uuid(self, ucm):
        ucm.recorder.responses["getImportedDirectoryUriCatalogs"] = {
            "return": {"importedDirectoryUriCatalogs": {"name": "TestCatalog"}}
        }
        ucm.get_imported_directory_uri_catalog(uuid="{BBBB-2222}")
        op, body = sent(ucm)
        assert op == "getImportedDirectoryUriCatalogs"
        assert text(body, "uuid") == "{BBBB-2222}"
        assert not has(body, "name")

    def test_get_imported_directory_uri_catalogs(self, ucm):
        ucm.recorder.responses["listImportedDirectoryUriCatalogs"] = {
            "return": {"importedDirectoryUriCatalogs": [{"name": "TestCatalog"}]}
        }
        result = ucm.get_imported_directory_uri_catalogs()
        op, body = sent(ucm)
        assert op == "listImportedDirectoryUriCatalogs"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_imported_directory_uri_catalogs_empty(self, ucm):
        ucm.recorder.responses["listImportedDirectoryUriCatalogs"] = {"return": None}
        result = ucm.get_imported_directory_uri_catalogs()
        assert result == []

    def test_update_imported_directory_uri_catalog(self, ucm):
        ucm.update_imported_directory_uri_catalog(name="TestCatalog", description="Updated")
        op, body = sent(ucm)
        assert op == "updateImportedDirectoryUriCatalogs"
        assert text(body, "name") == "TestCatalog"

    def test_remove_imported_directory_uri_catalog(self, ucm):
        ucm.remove_imported_directory_uri_catalog(name="TestCatalog")
        op, body = sent(ucm)
        assert op == "removeImportedDirectoryUriCatalogs"
        assert text(body, "name") == "TestCatalog"

    def test_remove_imported_directory_uri_catalog_by_uuid(self, ucm):
        ucm.remove_imported_directory_uri_catalog(uuid="{BBBB-2222}")
        op, body = sent(ucm)
        assert op == "removeImportedDirectoryUriCatalogs"
        assert text(body, "uuid") == "{BBBB-2222}"
        assert not has(body, "name")


# ---------------------------------------------------------------------------
# RemoteCluster
# ---------------------------------------------------------------------------

class TestRemoteCluster:
    def test_add_remote_cluster(self, ucm):
        ucm.add_remote_cluster(
            clusterId="cluster-remote-01",
            fullyQualifiedName="remote.example.com",
        )
        op, body = sent(ucm)
        assert op == "addRemoteCluster"
        assert text(body, "remoteCluster/clusterId") == "cluster-remote-01"
        assert text(body, "remoteCluster/fullyQualifiedName") == "remote.example.com"

    def test_get_remote_cluster_by_cluster_id(self, ucm):
        ucm.recorder.responses["getRemoteCluster"] = {
            "return": {"remoteCluster": {"clusterId": "cluster-remote-01"}}
        }
        result = ucm.get_remote_cluster(clusterId="cluster-remote-01")
        op, body = sent(ucm)
        assert op == "getRemoteCluster"
        assert text(body, "clusterId") == "cluster-remote-01"
        assert result == {"clusterId": "cluster-remote-01"}

    def test_get_remote_cluster_by_uuid(self, ucm):
        ucm.recorder.responses["getRemoteCluster"] = {
            "return": {"remoteCluster": {"clusterId": "cluster-remote-01"}}
        }
        ucm.get_remote_cluster(uuid="{CCCC-3333}")
        op, body = sent(ucm)
        assert op == "getRemoteCluster"
        assert text(body, "uuid") == "{CCCC-3333}"
        assert not has(body, "clusterId")

    def test_get_remote_cluster_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_remote_cluster()

    def test_get_remote_clusters(self, ucm):
        ucm.recorder.responses["listRemoteCluster"] = {
            "return": {"remoteCluster": [{"clusterId": "cluster-remote-01"}]}
        }
        result = ucm.get_remote_clusters()
        op, body = sent(ucm)
        assert op == "listRemoteCluster"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_remote_clusters_empty(self, ucm):
        ucm.recorder.responses["listRemoteCluster"] = {"return": None}
        result = ucm.get_remote_clusters()
        assert result == []

    def test_update_remote_cluster(self, ucm):
        ucm.update_remote_cluster(clusterId="cluster-remote-01")
        op, body = sent(ucm)
        assert op == "updateRemoteCluster"
        assert text(body, "clusterId") == "cluster-remote-01"

    def test_remove_remote_cluster_by_cluster_id(self, ucm):
        ucm.remove_remote_cluster(clusterId="cluster-remote-01")
        op, body = sent(ucm)
        assert op == "removeRemoteCluster"
        assert text(body, "clusterId") == "cluster-remote-01"

    def test_remove_remote_cluster_by_uuid(self, ucm):
        ucm.remove_remote_cluster(uuid="{CCCC-3333}")
        op, body = sent(ucm)
        assert op == "removeRemoteCluster"
        assert text(body, "uuid") == "{CCCC-3333}"

    def test_remove_remote_cluster_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.remove_remote_cluster()


# ---------------------------------------------------------------------------
# doUpdateRemoteCluster
# ---------------------------------------------------------------------------

class TestDoUpdateRemoteCluster:
    def test_do_update_remote_cluster(self, ucm):
        ucm.do_update_remote_cluster(server="10.0.0.1", clusterId="cluster-remote-01")
        op, body = sent(ucm)
        assert op == "doUpdateRemoteCluster"
        assert text(body, "server") == "10.0.0.1"
        assert text(body, "clusterId") == "cluster-remote-01"


# ---------------------------------------------------------------------------
# Smart Licensing — do* actions
# ---------------------------------------------------------------------------

class TestSmartLicensing:
    def test_do_smart_entitlement_request(self, ucm):
        ucm.do_smart_entitlement_request()
        op, _body = sent(ucm)
        assert op == "doSmartEntitlementRequest"

    def test_do_smart_license_de_register(self, ucm):
        ucm.do_smart_license_de_register()
        op, _body = sent(ucm)
        assert op == "doSmartLicenseDeRegister"

    def test_do_smart_license_re_register(self, ucm):
        ucm.do_smart_license_re_register(token="AbCdEfGhIj1234567890")
        op, body = sent(ucm)
        assert op == "doSmartLicenseReRegister"
        assert text(body, "token") == "AbCdEfGhIj1234567890"

    def test_do_smart_license_register(self, ucm):
        ucm.do_smart_license_register(token="AbCdEfGhIj1234567890", force=True)
        op, body = sent(ucm)
        assert op == "doSmartLicenseRegister"
        assert text(body, "token") == "AbCdEfGhIj1234567890"
        assert text(body, "force") in ("true", "1", True, "True")

    def test_do_smart_license_renew_authorization(self, ucm):
        ucm.do_smart_license_renew_authorization()
        op, _body = sent(ucm)
        assert op == "doSmartLicenseRenewAuthorization"

    def test_do_smart_license_renew_registration(self, ucm):
        ucm.do_smart_license_renew_registration()
        op, _body = sent(ucm)
        assert op == "doSmartLicenseRenewRegistration"


# ---------------------------------------------------------------------------
# License usage
# ---------------------------------------------------------------------------

class TestLicenseUsage:
    def test_do_update_license_usage(self, ucm):
        ucm.do_update_license_usage()
        op, _body = sent(ucm)
        assert op == "doUpdateLicenseUsage"
