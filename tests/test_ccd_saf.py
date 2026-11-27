"""Offline request tests for ciscoaxl/ccd_saf.py.

Run with: pytest tests/test_ccd_saf.py
"""
import pytest

from test_offline_requests import make_ucm, sent, text, has


@pytest.fixture
def ucm():
    return make_ucm("15.0")


class TestCcdAdvertisingService:
    def test_add_ccd_advertising_service(self, ucm):
        ucm.add_ccd_advertising_service(
            name="TestAdvSvc",
            hostDnGroup="TestDNGroup",
        )
        op, body = sent(ucm)
        assert op == "addCcdAdvertisingService"
        assert text(body, "ccdAdvertisingService/name") == "TestAdvSvc"
        assert text(body, "ccdAdvertisingService/hostDnGroup") == "TestDNGroup"

    def test_get_ccd_advertising_service_by_name(self, ucm):
        ucm.recorder.responses["getCcdAdvertisingService"] = {
            "return": {"ccdAdvertisingService": {"name": "TestAdvSvc"}}
        }
        result = ucm.get_ccd_advertising_service(name="TestAdvSvc")
        op, body = sent(ucm)
        assert op == "getCcdAdvertisingService"
        assert text(body, "name") == "TestAdvSvc"
        assert result == {"name": "TestAdvSvc"}

    def test_get_ccd_advertising_service_by_uuid(self, ucm):
        ucm.recorder.responses["getCcdAdvertisingService"] = {
            "return": {"ccdAdvertisingService": {"name": "TestAdvSvc"}}
        }
        ucm.get_ccd_advertising_service(uuid="{AAAA-1111}")
        op, body = sent(ucm)
        assert op == "getCcdAdvertisingService"
        assert text(body, "uuid") == "{AAAA-1111}"
        assert not has(body, "name")

    def test_get_ccd_advertising_services(self, ucm):
        ucm.recorder.responses["listCcdAdvertisingService"] = {
            "return": {"ccdAdvertisingService": [{"name": "TestAdvSvc"}]}
        }
        result = ucm.get_ccd_advertising_services()
        op, body = sent(ucm)
        assert op == "listCcdAdvertisingService"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_ccd_advertising_services_empty(self, ucm):
        ucm.recorder.responses["listCcdAdvertisingService"] = {"return": None}
        result = ucm.get_ccd_advertising_services()
        assert result == []

    def test_update_ccd_advertising_service(self, ucm):
        ucm.update_ccd_advertising_service(name="TestAdvSvc", description="Updated")
        op, body = sent(ucm)
        assert op == "updateCcdAdvertisingService"
        assert text(body, "name") == "TestAdvSvc"

    def test_remove_ccd_advertising_service_by_name(self, ucm):
        ucm.remove_ccd_advertising_service(name="TestAdvSvc")
        op, body = sent(ucm)
        assert op == "removeCcdAdvertisingService"
        assert text(body, "name") == "TestAdvSvc"

    def test_remove_ccd_advertising_service_by_uuid(self, ucm):
        ucm.remove_ccd_advertising_service(uuid="{AAAA-1111}")
        op, body = sent(ucm)
        assert op == "removeCcdAdvertisingService"
        assert text(body, "uuid") == "{AAAA-1111}"
        assert not has(body, "name")


class TestCcdFeatureConfig:
    def test_get_ccd_feature_config(self, ucm):
        ucm.recorder.responses["getCcdFeatureConfig"] = {
            "return": {
                "ccdFeatureConfig": {
                    "ccdParamName": "EnableCCD",
                    "ccdParamValue": "true",
                }
            }
        }
        result = ucm.get_ccd_feature_config("EnableCCD")
        op, body = sent(ucm)
        assert op == "getCcdFeatureConfig"
        assert text(body, "paramName") == "EnableCCD"
        assert result["ccdParamName"] == "EnableCCD"

    def test_update_ccd_feature_config_dict(self, ucm):
        ucm.update_ccd_feature_config(
            {"ccdParamName": "EnableCCD", "ccdParamValue": "false"}
        )
        op, body = sent(ucm)
        assert op == "updateCcdFeatureConfig"
        assert text(body, "ccdParam/ccdParamName") == "EnableCCD"
        assert text(body, "ccdParam/ccdParamValue") == "false"

    def test_update_ccd_feature_config_list(self, ucm):
        ucm.update_ccd_feature_config(
            [{"ccdParamName": "EnableCCD", "ccdParamValue": "false"}]
        )
        op, body = sent(ucm)
        assert op == "updateCcdFeatureConfig"


class TestCcdHostedDN:
    def test_add_ccd_hosted_dn(self, ucm):
        ucm.add_ccd_hosted_dn(
            hostedPattern="1XXX",
            CcdHostedDnGroup="TestDNGroup",
        )
        op, body = sent(ucm)
        assert op == "addCcdHostedDN"
        assert text(body, "ccdHostedDN/hostedPattern") == "1XXX"

    def test_get_ccd_hosted_dn_by_pattern(self, ucm):
        ucm.recorder.responses["getCcdHostedDN"] = {
            "return": {"ccdHostedDN": {"hostedPattern": "1XXX"}}
        }
        result = ucm.get_ccd_hosted_dn(hostedPattern="1XXX")
        op, body = sent(ucm)
        assert op == "getCcdHostedDN"
        assert text(body, "hostedPattern") == "1XXX"
        assert result == {"hostedPattern": "1XXX"}

    def test_get_ccd_hosted_dn_by_uuid(self, ucm):
        ucm.recorder.responses["getCcdHostedDN"] = {
            "return": {"ccdHostedDN": {"hostedPattern": "1XXX"}}
        }
        ucm.get_ccd_hosted_dn(uuid="{BBBB-2222}")
        op, body = sent(ucm)
        assert op == "getCcdHostedDN"
        assert text(body, "uuid") == "{BBBB-2222}"
        assert not has(body, "hostedPattern")

    def test_get_ccd_hosted_dn_raises_on_both(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_ccd_hosted_dn(hostedPattern="1XXX", uuid="{BBBB-2222}")

    def test_get_ccd_hosted_dn_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.get_ccd_hosted_dn()

    def test_get_ccd_hosted_dns(self, ucm):
        ucm.recorder.responses["listCcdHostedDN"] = {
            "return": {"ccdHostedDN": [{"hostedPattern": "1XXX"}]}
        }
        result = ucm.get_ccd_hosted_dns()
        op, body = sent(ucm)
        assert op == "listCcdHostedDN"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_ccd_hosted_dns_empty(self, ucm):
        ucm.recorder.responses["listCcdHostedDN"] = {"return": None}
        result = ucm.get_ccd_hosted_dns()
        assert result == []

    def test_update_ccd_hosted_dn(self, ucm):
        ucm.update_ccd_hosted_dn(hostedPattern="1XXX", description="Updated")
        op, body = sent(ucm)
        assert op == "updateCcdHostedDN"
        assert text(body, "hostedPattern") == "1XXX"

    def test_remove_ccd_hosted_dn_by_pattern(self, ucm):
        ucm.remove_ccd_hosted_dn(hostedPattern="1XXX")
        op, body = sent(ucm)
        assert op == "removeCcdHostedDN"
        assert text(body, "hostedPattern") == "1XXX"

    def test_remove_ccd_hosted_dn_by_uuid(self, ucm):
        ucm.remove_ccd_hosted_dn(uuid="{BBBB-2222}")
        op, body = sent(ucm)
        assert op == "removeCcdHostedDN"
        assert text(body, "uuid") == "{BBBB-2222}"
        assert not has(body, "hostedPattern")

    def test_remove_ccd_hosted_dn_raises_on_neither(self, ucm):
        with pytest.raises(ValueError):
            ucm.remove_ccd_hosted_dn()


class TestCcdHostedDNGroup:
    def test_add_ccd_hosted_dn_group(self, ucm):
        ucm.add_ccd_hosted_dn_group(name="TestDNGroup")
        op, body = sent(ucm)
        assert op == "addCcdHostedDNGroup"
        assert text(body, "ccdHostedDNGroup/name") == "TestDNGroup"

    def test_get_ccd_hosted_dn_group_by_name(self, ucm):
        ucm.recorder.responses["getCcdHostedDNGroup"] = {
            "return": {"ccdHostedDNGroup": {"name": "TestDNGroup"}}
        }
        result = ucm.get_ccd_hosted_dn_group(name="TestDNGroup")
        op, body = sent(ucm)
        assert op == "getCcdHostedDNGroup"
        assert text(body, "name") == "TestDNGroup"
        assert result == {"name": "TestDNGroup"}

    def test_get_ccd_hosted_dn_group_by_uuid(self, ucm):
        ucm.recorder.responses["getCcdHostedDNGroup"] = {
            "return": {"ccdHostedDNGroup": {"name": "TestDNGroup"}}
        }
        ucm.get_ccd_hosted_dn_group(uuid="{CCCC-3333}")
        op, body = sent(ucm)
        assert op == "getCcdHostedDNGroup"
        assert text(body, "uuid") == "{CCCC-3333}"
        assert not has(body, "name")

    def test_get_ccd_hosted_dn_groups(self, ucm):
        ucm.recorder.responses["listCcdHostedDNGroup"] = {
            "return": {"ccdHostedDNGroup": [{"name": "TestDNGroup"}]}
        }
        result = ucm.get_ccd_hosted_dn_groups()
        op, body = sent(ucm)
        assert op == "listCcdHostedDNGroup"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_ccd_hosted_dn_groups_empty(self, ucm):
        ucm.recorder.responses["listCcdHostedDNGroup"] = {"return": None}
        result = ucm.get_ccd_hosted_dn_groups()
        assert result == []

    def test_update_ccd_hosted_dn_group(self, ucm):
        ucm.update_ccd_hosted_dn_group(name="TestDNGroup", description="Updated")
        op, body = sent(ucm)
        assert op == "updateCcdHostedDNGroup"
        assert text(body, "name") == "TestDNGroup"

    def test_remove_ccd_hosted_dn_group_by_name(self, ucm):
        ucm.remove_ccd_hosted_dn_group(name="TestDNGroup")
        op, body = sent(ucm)
        assert op == "removeCcdHostedDNGroup"
        assert text(body, "name") == "TestDNGroup"

    def test_remove_ccd_hosted_dn_group_by_uuid(self, ucm):
        ucm.remove_ccd_hosted_dn_group(uuid="{CCCC-3333}")
        op, body = sent(ucm)
        assert op == "removeCcdHostedDNGroup"
        assert text(body, "uuid") == "{CCCC-3333}"
        assert not has(body, "name")


class TestCcdRequestingService:
    def test_add_ccd_requesting_service(self, ucm):
        ucm.add_ccd_requesting_service(name="TestReqSvc")
        op, body = sent(ucm)
        assert op == "addCcdRequestingService"
        assert text(body, "ccdRequestingService/name") == "TestReqSvc"

    def test_get_ccd_requesting_service_by_name(self, ucm):
        ucm.recorder.responses["getCcdRequestingService"] = {
            "return": {"ccdRequestingService": {"name": "TestReqSvc"}}
        }
        result = ucm.get_ccd_requesting_service(name="TestReqSvc")
        op, body = sent(ucm)
        assert op == "getCcdRequestingService"
        assert text(body, "name") == "TestReqSvc"
        assert result == {"name": "TestReqSvc"}

    def test_get_ccd_requesting_service_by_uuid(self, ucm):
        ucm.recorder.responses["getCcdRequestingService"] = {
            "return": {"ccdRequestingService": {"name": "TestReqSvc"}}
        }
        ucm.get_ccd_requesting_service(uuid="{DDDD-4444}")
        op, body = sent(ucm)
        assert op == "getCcdRequestingService"
        assert text(body, "uuid") == "{DDDD-4444}"
        assert not has(body, "name")

    def test_update_ccd_requesting_service(self, ucm):
        ucm.update_ccd_requesting_service(name="TestReqSvc", description="Updated")
        op, body = sent(ucm)
        assert op == "updateCcdRequestingService"
        assert text(body, "name") == "TestReqSvc"

    def test_remove_ccd_requesting_service_by_name(self, ucm):
        ucm.remove_ccd_requesting_service(name="TestReqSvc")
        op, body = sent(ucm)
        assert op == "removeCcdRequestingService"
        assert text(body, "name") == "TestReqSvc"

    def test_remove_ccd_requesting_service_by_uuid(self, ucm):
        ucm.remove_ccd_requesting_service(uuid="{DDDD-4444}")
        op, body = sent(ucm)
        assert op == "removeCcdRequestingService"
        assert text(body, "uuid") == "{DDDD-4444}"
        assert not has(body, "name")


class TestSafCcdPurgeBlockLearnedRoutes:
    def test_add_saf_ccd_purge_block_learned_routes(self, ucm):
        ucm.add_saf_ccd_purge_block_learned_routes(learnedPattern="5XXX")
        op, body = sent(ucm)
        assert op == "addSafCcdPurgeBlockLearnedRoutes"
        assert text(body, "safCcdPurgeBlockLearnedRoutes/learnedPattern") == "5XXX"

    def test_get_saf_ccd_purge_block_learned_routes_by_uuid(self, ucm):
        ucm.recorder.responses["getSafCcdPurgeBlockLearnedRoutes"] = {
            "return": {
                "safCcdPurgeBlockLearnedRoutes": {"learnedPattern": "5XXX"}
            }
        }
        result = ucm.get_saf_ccd_purge_block_learned_routes(uuid="{EEEE-5555}")
        op, body = sent(ucm)
        assert op == "getSafCcdPurgeBlockLearnedRoutes"
        assert text(body, "uuid") == "{EEEE-5555}"
        assert result == {"learnedPattern": "5XXX"}

    def test_get_saf_ccd_purge_block_learned_routes_by_pattern(self, ucm):
        ucm.recorder.responses["getSafCcdPurgeBlockLearnedRoutes"] = {
            "return": {
                "safCcdPurgeBlockLearnedRoutes": {"learnedPattern": "5XXX"}
            }
        }
        ucm.get_saf_ccd_purge_block_learned_routes(learnedPattern="5XXX")
        op, body = sent(ucm)
        assert op == "getSafCcdPurgeBlockLearnedRoutes"
        assert text(body, "learnedPattern") == "5XXX"

    def test_get_saf_ccd_purge_block_learned_routes_list(self, ucm):
        ucm.recorder.responses["listSafCcdPurgeBlockLearnedRoutes"] = {
            "return": {
                "safCcdPurgeBlockLearnedRoutes": [{"learnedPattern": "5XXX"}]
            }
        }
        result = ucm.get_saf_ccd_purge_block_learned_routes_list()
        op, body = sent(ucm)
        assert op == "listSafCcdPurgeBlockLearnedRoutes"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_saf_ccd_purge_block_learned_routes_list_empty(self, ucm):
        ucm.recorder.responses["listSafCcdPurgeBlockLearnedRoutes"] = {
            "return": None
        }
        result = ucm.get_saf_ccd_purge_block_learned_routes_list()
        assert result == []

    def test_update_saf_ccd_purge_block_learned_routes(self, ucm):
        ucm.update_saf_ccd_purge_block_learned_routes(
            uuid="{EEEE-5555}", newLearnedPattern="6XXX"
        )
        op, body = sent(ucm)
        assert op == "updateSafCcdPurgeBlockLearnedRoutes"
        assert text(body, "uuid") == "{EEEE-5555}"

    def test_remove_saf_ccd_purge_block_learned_routes_by_uuid(self, ucm):
        ucm.remove_saf_ccd_purge_block_learned_routes(uuid="{EEEE-5555}")
        op, body = sent(ucm)
        assert op == "removeSafCcdPurgeBlockLearnedRoutes"
        assert text(body, "uuid") == "{EEEE-5555}"

    def test_remove_saf_ccd_purge_block_learned_routes_by_pattern(self, ucm):
        ucm.remove_saf_ccd_purge_block_learned_routes(learnedPattern="5XXX")
        op, body = sent(ucm)
        assert op == "removeSafCcdPurgeBlockLearnedRoutes"
        assert text(body, "learnedPattern") == "5XXX"


class TestSafForwarder:
    def test_add_saf_forwarder(self, ucm):
        ucm.add_saf_forwarder(
            name="TestForwarder",
            clientLabel="TestLabel",
            safSecurityProfile="TestProfile",
            ipAddress="10.0.0.1",
        )
        op, body = sent(ucm)
        assert op == "addSafForwarder"
        assert text(body, "safForwarder/name") == "TestForwarder"
        assert text(body, "safForwarder/ipAddress") == "10.0.0.1"

    def test_get_saf_forwarder_by_name(self, ucm):
        ucm.recorder.responses["getSafForwarder"] = {
            "return": {"safForwarder": {"name": "TestForwarder"}}
        }
        result = ucm.get_saf_forwarder(name="TestForwarder")
        op, body = sent(ucm)
        assert op == "getSafForwarder"
        assert text(body, "name") == "TestForwarder"
        assert result == {"name": "TestForwarder"}

    def test_get_saf_forwarder_by_uuid(self, ucm):
        ucm.recorder.responses["getSafForwarder"] = {
            "return": {"safForwarder": {"name": "TestForwarder"}}
        }
        ucm.get_saf_forwarder(uuid="{FFFF-6666}")
        op, body = sent(ucm)
        assert op == "getSafForwarder"
        assert text(body, "uuid") == "{FFFF-6666}"
        assert not has(body, "name")

    def test_get_saf_forwarders(self, ucm):
        ucm.recorder.responses["listSafForwarder"] = {
            "return": {"safForwarder": [{"name": "TestForwarder"}]}
        }
        result = ucm.get_saf_forwarders()
        op, body = sent(ucm)
        assert op == "listSafForwarder"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_saf_forwarders_empty(self, ucm):
        ucm.recorder.responses["listSafForwarder"] = {"return": None}
        result = ucm.get_saf_forwarders()
        assert result == []

    def test_update_saf_forwarder(self, ucm):
        ucm.update_saf_forwarder(name="TestForwarder", description="Updated")
        op, body = sent(ucm)
        assert op == "updateSafForwarder"
        assert text(body, "name") == "TestForwarder"

    def test_remove_saf_forwarder_by_name(self, ucm):
        ucm.remove_saf_forwarder(name="TestForwarder")
        op, body = sent(ucm)
        assert op == "removeSafForwarder"
        assert text(body, "name") == "TestForwarder"

    def test_remove_saf_forwarder_by_uuid(self, ucm):
        ucm.remove_saf_forwarder(uuid="{FFFF-6666}")
        op, body = sent(ucm)
        assert op == "removeSafForwarder"
        assert text(body, "uuid") == "{FFFF-6666}"
        assert not has(body, "name")


class TestSafSecurityProfile:
    def test_add_saf_security_profile(self, ucm):
        ucm.add_saf_security_profile(
            name="TestProfile",
            userid="safuser",
            password="s3cr3t",
        )
        op, body = sent(ucm)
        assert op == "addSafSecurityProfile"
        assert text(body, "safSecurityProfile/name") == "TestProfile"
        assert text(body, "safSecurityProfile/userid") == "safuser"

    def test_get_saf_security_profile_by_name(self, ucm):
        ucm.recorder.responses["getSafSecurityProfile"] = {
            "return": {"safSecurityProfile": {"name": "TestProfile"}}
        }
        result = ucm.get_saf_security_profile(name="TestProfile")
        op, body = sent(ucm)
        assert op == "getSafSecurityProfile"
        assert text(body, "name") == "TestProfile"
        assert result == {"name": "TestProfile"}

    def test_get_saf_security_profile_by_uuid(self, ucm):
        ucm.recorder.responses["getSafSecurityProfile"] = {
            "return": {"safSecurityProfile": {"name": "TestProfile"}}
        }
        ucm.get_saf_security_profile(uuid="{GGGG-7777}")
        op, body = sent(ucm)
        assert op == "getSafSecurityProfile"
        assert text(body, "uuid") == "{GGGG-7777}"
        assert not has(body, "name")

    def test_get_saf_security_profiles(self, ucm):
        ucm.recorder.responses["listSafSecurityProfile"] = {
            "return": {"safSecurityProfile": [{"name": "TestProfile"}]}
        }
        result = ucm.get_saf_security_profiles()
        op, body = sent(ucm)
        assert op == "listSafSecurityProfile"
        assert isinstance(result, list)
        assert len(result) == 1

    def test_get_saf_security_profiles_empty(self, ucm):
        ucm.recorder.responses["listSafSecurityProfile"] = {"return": None}
        result = ucm.get_saf_security_profiles()
        assert result == []

    def test_update_saf_security_profile(self, ucm):
        ucm.update_saf_security_profile(name="TestProfile", description="Updated")
        op, body = sent(ucm)
        assert op == "updateSafSecurityProfile"
        assert text(body, "name") == "TestProfile"

    def test_remove_saf_security_profile_by_name(self, ucm):
        ucm.remove_saf_security_profile(name="TestProfile")
        op, body = sent(ucm)
        assert op == "removeSafSecurityProfile"
        assert text(body, "name") == "TestProfile"

    def test_remove_saf_security_profile_by_uuid(self, ucm):
        ucm.remove_saf_security_profile(uuid="{GGGG-7777}")
        op, body = sent(ucm)
        assert op == "removeSafSecurityProfile"
        assert text(body, "uuid") == "{GGGG-7777}"
        assert not has(body, "name")
