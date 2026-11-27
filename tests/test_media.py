"""Offline request tests for ciscoaxl/media.py.

Run with: pytest tests/test_media.py
"""
import pytest

from test_offline_requests import make_ucm, sent, text


@pytest.fixture
def ucm():
    return make_ucm("15.0")


class TestMeetMe:
    def test_get_meet_mes_returns_list(self, ucm):
        ucm.recorder.responses["listMeetMe"] = {
            "return": {"meetMe": [{"pattern": "8000"}, {"pattern": "8001"}]}
        }
        result = ucm.get_meet_mes()
        assert len(result) == 2
        assert result[0]["pattern"] == "8000"

    def test_get_meet_mes_empty(self, ucm):
        ucm.recorder.responses["listMeetMe"] = {"return": None}
        assert ucm.get_meet_mes() == []

    def test_get_meet_me_unwraps(self, ucm):
        ucm.recorder.responses["getMeetMe"] = {
            "return": {"meetMe": {"pattern": "8000"}}
        }
        assert ucm.get_meet_me(pattern="8000") == {"pattern": "8000"}

    def test_add_meet_me_builds_wrapper(self, ucm):
        ucm.add_meet_me(pattern="8000")
        op, body = sent(ucm)
        assert op == "addMeetMe"
        assert text(body, "meetMe/pattern") == "8000"

    def test_update_meet_me(self, ucm):
        ucm.update_meet_me(pattern="8000", description="Conference room")
        op, _ = sent(ucm)
        assert op == "updateMeetMe"

    def test_delete_meet_me_by_name(self, ucm):
        ucm.delete_meet_me(name="8000")
        op, body = sent(ucm)
        assert op == "removeMeetMe"


class TestMohAudioSource:
    def test_get_moh_audio_sources_returns_list(self, ucm):
        ucm.recorder.responses["listMohAudioSource"] = {
            "return": {"mohAudioSource": [{"name": "SampleAudio1"}, {"name": "SampleAudio2"}]}
        }
        result = ucm.get_moh_audio_sources()
        assert len(result) == 2

    def test_get_moh_audio_sources_empty(self, ucm):
        ucm.recorder.responses["listMohAudioSource"] = {"return": None}
        assert ucm.get_moh_audio_sources() == []

    def test_get_moh_audio_source_unwraps(self, ucm):
        ucm.recorder.responses["getMohAudioSource"] = {
            "return": {"mohAudioSource": {"name": "SampleAudio1", "sourceId": 1}}
        }
        result = ucm.get_moh_audio_source(sourceId=1)
        assert result["sourceId"] == 1

    def test_update_moh_audio_source(self, ucm):
        ucm.update_moh_audio_source(sourceId=1, multicast=False)
        op, _ = sent(ucm)
        assert op == "updateMohAudioSource"

    def test_delete_moh_audio_source_by_source_id(self, ucm):
        ucm.delete_moh_audio_source(source_id=1)
        op, body = sent(ucm)
        assert op == "removeMohAudioSource"
        assert text(body, "sourceId") == "1"

    def test_delete_moh_audio_source_by_uuid(self, ucm):
        ucm.delete_moh_audio_source(uuid="{11111111-0000-0000-0000-000000000001}")
        op, body = sent(ucm)
        assert op == "removeMohAudioSource"
        assert text(body, "uuid") == "{11111111-0000-0000-0000-000000000001}"

    def test_delete_moh_audio_source_no_args_raises(self, ucm):
        with pytest.raises(ValueError):
            ucm.delete_moh_audio_source()


class TestMohServer:
    def test_get_moh_servers_returns_list(self, ucm):
        ucm.recorder.responses["listMohServer"] = {
            "return": {"mohServer": [{"name": "MOH_Server_1"}]}
        }
        result = ucm.get_moh_servers()
        assert result[0]["name"] == "MOH_Server_1"

    def test_get_moh_servers_empty(self, ucm):
        ucm.recorder.responses["listMohServer"] = {"return": None}
        assert ucm.get_moh_servers() == []

    def test_get_moh_server_unwraps(self, ucm):
        ucm.recorder.responses["getMohServer"] = {
            "return": {"mohServer": {"name": "MOH_Server_1"}}
        }
        assert ucm.get_moh_server(name="MOH_Server_1") == {"name": "MOH_Server_1"}

    def test_update_moh_server(self, ucm):
        ucm.update_moh_server(name="MOH_Server_1", description="Updated")
        op, _ = sent(ucm)
        assert op == "updateMohServer"


class TestRecordingProfile:
    def test_get_recording_profiles_returns_list(self, ucm):
        ucm.recorder.responses["listRecordingProfile"] = {
            "return": {"recordingProfile": [{"name": "RP1"}, {"name": "RP2"}]}
        }
        result = ucm.get_recording_profiles()
        assert len(result) == 2

    def test_get_recording_profiles_empty(self, ucm):
        ucm.recorder.responses["listRecordingProfile"] = {"return": None}
        assert ucm.get_recording_profiles() == []

    def test_get_recording_profile_unwraps(self, ucm):
        ucm.recorder.responses["getRecordingProfile"] = {
            "return": {"recordingProfile": {"name": "RP1"}}
        }
        assert ucm.get_recording_profile(name="RP1") == {"name": "RP1"}

    def test_add_recording_profile_builds_wrapper(self, ucm):
        # recorderDestination is required in XRecordingProfile
        ucm.add_recording_profile(name="RP1", recorderDestination="sip:recorder@cucm:5060")
        op, body = sent(ucm)
        assert op == "addRecordingProfile"
        assert text(body, "recordingProfile/name") == "RP1"
        assert text(body, "recordingProfile/recorderDestination") == "sip:recorder@cucm:5060"

    def test_update_recording_profile(self, ucm):
        # UpdateRecordingProfileReq fields: newName, recordingCssName, recorderDestination
        ucm.update_recording_profile(name="RP1", recorderDestination="sip:new@cucm:5060")
        op, _ = sent(ucm)
        assert op == "updateRecordingProfile"

    def test_delete_recording_profile(self, ucm):
        ucm.delete_recording_profile(name="RP1")
        op, body = sent(ucm)
        assert op == "removeRecordingProfile"
        assert text(body, "name") == "RP1"


class TestRegionMatrix:
    def test_update_region_matrix(self, ucm):
        ucm.update_region_matrix(regionAName="RegionA", regionBName="RegionB", bandwidth="64")
        op, body = sent(ucm)
        assert op == "updateRegionMatrix"
        assert text(body, "regionAName") == "RegionA"
        assert text(body, "regionBName") == "RegionB"


class TestDeviceMobility:
    def test_get_device_mobilities_returns_list(self, ucm):
        ucm.recorder.responses["listDeviceMobility"] = {
            "return": {"deviceMobility": [{"name": "DM1"}]}
        }
        result = ucm.get_device_mobilities()
        assert result[0]["name"] == "DM1"

    def test_get_device_mobilities_empty(self, ucm):
        ucm.recorder.responses["listDeviceMobility"] = {"return": None}
        assert ucm.get_device_mobilities() == []

    def test_get_device_mobility_unwraps(self, ucm):
        ucm.recorder.responses["getDeviceMobility"] = {
            "return": {"deviceMobility": {"name": "DM1"}}
        }
        assert ucm.get_device_mobility(name="DM1") == {"name": "DM1"}

    def test_add_device_mobility_builds_wrapper(self, ucm):
        # subNetDetails and members.member are required in XDeviceMobility
        ucm.add_device_mobility(
            name="DM1",
            subNetDetails={"ipv4SubNetDetails": {"ipv4Subnet": "10.0.0.0", "ipv4SubNetMaskSz": 24}},
            members={"member": [{"devicePoolName": "Default"}]},
        )
        op, body = sent(ucm)
        assert op == "addDeviceMobility"
        assert text(body, "deviceMobility/name") == "DM1"

    def test_update_device_mobility(self, ucm):
        # UpdateDeviceMobilityReq fields: newName, subNetDetails, members, deviceMobilityGroupName, etc.
        ucm.update_device_mobility(name="DM1", newName="DM1-Updated")
        op, _ = sent(ucm)
        assert op == "updateDeviceMobility"

    def test_delete_device_mobility(self, ucm):
        ucm.delete_device_mobility(name="DM1")
        op, body = sent(ucm)
        assert op == "removeDeviceMobility"
        assert text(body, "name") == "DM1"


class TestDeviceMobilityGroup:
    def test_get_device_mobility_groups_returns_list(self, ucm):
        ucm.recorder.responses["listDeviceMobilityGroup"] = {
            "return": {"deviceMobilityGroup": [{"name": "DMG1"}]}
        }
        result = ucm.get_device_mobility_groups()
        assert result[0]["name"] == "DMG1"

    def test_get_device_mobility_groups_empty(self, ucm):
        ucm.recorder.responses["listDeviceMobilityGroup"] = {"return": None}
        assert ucm.get_device_mobility_groups() == []

    def test_get_device_mobility_group_unwraps(self, ucm):
        ucm.recorder.responses["getDeviceMobilityGroup"] = {
            "return": {"deviceMobilityGroup": {"name": "DMG1"}}
        }
        assert ucm.get_device_mobility_group(name="DMG1") == {"name": "DMG1"}

    def test_add_device_mobility_group_builds_wrapper(self, ucm):
        ucm.add_device_mobility_group(name="DMG1")
        op, body = sent(ucm)
        assert op == "addDeviceMobilityGroup"
        assert text(body, "deviceMobilityGroup/name") == "DMG1"

    def test_update_device_mobility_group(self, ucm):
        ucm.update_device_mobility_group(name="DMG1", description="Updated")
        op, _ = sent(ucm)
        assert op == "updateDeviceMobilityGroup"

    def test_delete_device_mobility_group(self, ucm):
        ucm.delete_device_mobility_group(name="DMG1")
        op, body = sent(ucm)
        assert op == "removeDeviceMobilityGroup"
        assert text(body, "name") == "DMG1"


class TestMobileVoiceAccess:
    def test_get_mobile_voice_access_unwraps(self, ucm):
        ucm.recorder.responses["getMobileVoiceAccess"] = {
            "return": {"mobileVoiceAccess": {"pattern": "8500"}}
        }
        assert ucm.get_mobile_voice_access(pattern="8500") == {"pattern": "8500"}

    def test_add_mobile_voice_access_builds_wrapper(self, ucm):
        ucm.add_mobile_voice_access(pattern="8500")
        op, body = sent(ucm)
        assert op == "addMobileVoiceAccess"
        assert text(body, "mobileVoiceAccess/pattern") == "8500"

    def test_update_mobile_voice_access(self, ucm):
        # UpdateMobileVoiceAccessReq valid fields: newPattern, routePartitionName, locales
        ucm.update_mobile_voice_access(pattern="8500", newPattern="8501")
        op, _ = sent(ucm)
        assert op == "updateMobileVoiceAccess"

    def test_delete_mobile_voice_access_by_pattern(self, ucm):
        ucm.delete_mobile_voice_access(pattern="8500")
        op, body = sent(ucm)
        assert op == "removeMobileVoiceAccess"
        assert text(body, "pattern") == "8500"

    def test_delete_mobile_voice_access_by_uuid(self, ucm):
        ucm.delete_mobile_voice_access(uuid="{22222222-0000-0000-0000-000000000001}")
        op, body = sent(ucm)
        assert op == "removeMobileVoiceAccess"
        assert text(body, "uuid") == "{22222222-0000-0000-0000-000000000001}"

    def test_delete_mobile_voice_access_no_args_raises(self, ucm):
        with pytest.raises(ValueError):
            ucm.delete_mobile_voice_access()


class TestMobility:
    def test_get_mobility_unwraps(self, ucm):
        ucm.recorder.responses["getMobility"] = {
            "return": {"mobility": {"handoffNumber": "9000"}}
        }
        result = ucm.get_mobility(handoffNumber="9000")
        assert result["handoffNumber"] == "9000"

    def test_add_mobility_builds_wrapper(self, ucm):
        # XMobility requires both handoffNumber and DTMFNumber
        ucm.add_mobility(handoffNumber="9000", DTMFNumber="9001")
        op, body = sent(ucm)
        assert op == "addMobility"
        assert text(body, "mobility/handoffNumber") == "9000"
        assert text(body, "mobility/DTMFNumber") == "9001"

    def test_update_mobility(self, ucm):
        ucm.update_mobility(handoffNumber="9000")
        op, _ = sent(ucm)
        assert op == "updateMobility"


class TestMobilityProfile:
    def test_get_mobility_profiles_returns_list(self, ucm):
        ucm.recorder.responses["listMobilityProfile"] = {
            "return": {"mobilityProfile": [{"name": "MP1"}, {"name": "MP2"}]}
        }
        result = ucm.get_mobility_profiles()
        assert len(result) == 2

    def test_get_mobility_profiles_empty(self, ucm):
        ucm.recorder.responses["listMobilityProfile"] = {"return": None}
        assert ucm.get_mobility_profiles() == []

    def test_get_mobility_profile_unwraps(self, ucm):
        ucm.recorder.responses["getMobilityProfile"] = {
            "return": {"mobilityProfile": {"name": "MP1"}}
        }
        assert ucm.get_mobility_profile(name="MP1") == {"name": "MP1"}

    def test_add_mobility_profile_builds_wrapper(self, ucm):
        ucm.add_mobility_profile(name="MP1")
        op, body = sent(ucm)
        assert op == "addMobilityProfile"
        assert text(body, "mobilityProfile/name") == "MP1"

    def test_update_mobility_profile(self, ucm):
        ucm.update_mobility_profile(name="MP1", description="Updated")
        op, _ = sent(ucm)
        assert op == "updateMobilityProfile"

    def test_delete_mobility_profile(self, ucm):
        ucm.delete_mobility_profile(name="MP1")
        op, body = sent(ucm)
        assert op == "removeMobilityProfile"
        assert text(body, "name") == "MP1"


class TestPhysicalLocation:
    def test_get_physical_locations_returns_list(self, ucm):
        ucm.recorder.responses["listPhysicalLocation"] = {
            "return": {"physicalLocation": [{"name": "HQ"}, {"name": "Branch1"}]}
        }
        result = ucm.get_physical_locations()
        assert len(result) == 2

    def test_get_physical_locations_empty(self, ucm):
        ucm.recorder.responses["listPhysicalLocation"] = {"return": None}
        assert ucm.get_physical_locations() == []

    def test_get_physical_location_unwraps(self, ucm):
        ucm.recorder.responses["getPhysicalLocation"] = {
            "return": {"physicalLocation": {"name": "HQ"}}
        }
        assert ucm.get_physical_location(name="HQ") == {"name": "HQ"}

    def test_add_physical_location_builds_wrapper(self, ucm):
        ucm.add_physical_location(name="HQ")
        op, body = sent(ucm)
        assert op == "addPhysicalLocation"
        assert text(body, "physicalLocation/name") == "HQ"

    def test_update_physical_location(self, ucm):
        ucm.update_physical_location(name="HQ", description="Headquarters")
        op, _ = sent(ucm)
        assert op == "updatePhysicalLocation"

    def test_delete_physical_location(self, ucm):
        ucm.delete_physical_location(name="HQ")
        op, body = sent(ucm)
        assert op == "removePhysicalLocation"
        assert text(body, "name") == "HQ"


class TestPresenceGroup:
    def test_get_presence_groups_returns_list(self, ucm):
        ucm.recorder.responses["listPresenceGroup"] = {
            "return": {"presenceGroup": [{"name": "PG1"}, {"name": "PG2"}]}
        }
        result = ucm.get_presence_groups()
        assert len(result) == 2

    def test_get_presence_groups_empty(self, ucm):
        ucm.recorder.responses["listPresenceGroup"] = {"return": None}
        assert ucm.get_presence_groups() == []

    def test_get_presence_group_unwraps(self, ucm):
        ucm.recorder.responses["getPresenceGroup"] = {
            "return": {"presenceGroup": {"name": "PG1"}}
        }
        assert ucm.get_presence_group(name="PG1") == {"name": "PG1"}

    def test_add_presence_group_builds_wrapper(self, ucm):
        ucm.add_presence_group(name="PG1")
        op, body = sent(ucm)
        assert op == "addPresenceGroup"
        assert text(body, "presenceGroup/name") == "PG1"

    def test_update_presence_group(self, ucm):
        ucm.update_presence_group(name="PG1", description="Updated")
        op, _ = sent(ucm)
        assert op == "updatePresenceGroup"

    def test_delete_presence_group(self, ucm):
        ucm.delete_presence_group(name="PG1")
        op, body = sent(ucm)
        assert op == "removePresenceGroup"
        assert text(body, "name") == "PG1"


class TestCalledPartyTracing:
    def test_add_builds_wrapper(self, ucm):
        ucm.add_called_party_tracing(directorynumber="1234")
        op, body = sent(ucm)
        assert op == "addCalledPartyTracing"
        assert text(body, "calledPartyTracing/directorynumber") == "1234"

    def test_list_returns_list(self, ucm):
        ucm.recorder.responses["listCalledPartyTracing"] = {
            "return": {"calledPartyTracing": [{"directorynumber": "1234"}]}
        }
        result = ucm.get_called_party_tracings()
        assert len(result) == 1
        assert result[0]["directorynumber"] == "1234"

    def test_list_empty(self, ucm):
        ucm.recorder.responses["listCalledPartyTracing"] = {"return": None}
        assert ucm.get_called_party_tracings() == []

    def test_delete_by_directorynumber(self, ucm):
        ucm.delete_called_party_tracing(directorynumber="1234")
        op, body = sent(ucm)
        assert op == "removeCalledPartyTracing"
        assert text(body, "directorynumber") == "1234"

    def test_delete_by_uuid(self, ucm):
        ucm.delete_called_party_tracing(uuid="{AAAAAAAA-0000-0000-0000-000000000001}")
        op, body = sent(ucm)
        assert op == "removeCalledPartyTracing"
        assert text(body, "uuid") == "{AAAAAAAA-0000-0000-0000-000000000001}"

    def test_delete_no_args_raises(self, ucm):
        with pytest.raises(ValueError):
            ucm.delete_called_party_tracing()


class TestCmcInfo:
    def test_add_builds_wrapper(self, ucm):
        ucm.add_cmc_info(code="1234", description="Test CMC")
        op, body = sent(ucm)
        assert op == "addCmcInfo"
        assert text(body, "cmcInfo/code") == "1234"

    def test_get_unwraps(self, ucm):
        ucm.recorder.responses["getCmcInfo"] = {
            "return": {"cmcInfo": {"code": "1234", "description": "Test CMC"}}
        }
        result = ucm.get_cmc_info(code="1234")
        assert result["code"] == "1234"

    def test_list_returns_list(self, ucm):
        ucm.recorder.responses["listCmcInfo"] = {
            "return": {"cmcInfo": [{"code": "1234"}, {"code": "5678"}]}
        }
        result = ucm.get_cmc_infos()
        assert len(result) == 2

    def test_list_empty(self, ucm):
        ucm.recorder.responses["listCmcInfo"] = {"return": None}
        assert ucm.get_cmc_infos() == []

    def test_update(self, ucm):
        ucm.update_cmc_info(code="1234", description="Updated")
        op, _ = sent(ucm)
        assert op == "updateCmcInfo"

    def test_delete_by_code(self, ucm):
        ucm.delete_cmc_info(code="1234")
        op, body = sent(ucm)
        assert op == "removeCmcInfo"
        assert text(body, "code") == "1234"

    def test_delete_no_args_raises(self, ucm):
        with pytest.raises(ValueError):
            ucm.delete_cmc_info()


class TestElinGroup:
    def test_add_builds_wrapper(self, ucm):
        # XElinGroup requires elinNumbers.elinNumber items with a pattern field
        ucm.add_elin_group(
            name="ELIN1",
            elinNumbers={"elinNumber": [{"pattern": "9114445551234"}]},
        )
        op, body = sent(ucm)
        assert op == "addElinGroup"
        assert text(body, "elinGroup/name") == "ELIN1"

    def test_get_unwraps(self, ucm):
        ucm.recorder.responses["getElinGroup"] = {
            "return": {"elinGroup": {"name": "ELIN1"}}
        }
        assert ucm.get_elin_group(name="ELIN1") == {"name": "ELIN1"}

    def test_list_returns_list(self, ucm):
        ucm.recorder.responses["listElinGroup"] = {
            "return": {"elinGroup": [{"name": "ELIN1"}, {"name": "ELIN2"}]}
        }
        result = ucm.get_elin_groups()
        assert len(result) == 2

    def test_list_empty(self, ucm):
        ucm.recorder.responses["listElinGroup"] = {"return": None}
        assert ucm.get_elin_groups() == []

    def test_update(self, ucm):
        ucm.update_elin_group(name="ELIN1", description="Updated")
        op, _ = sent(ucm)
        assert op == "updateElinGroup"

    def test_delete(self, ucm):
        ucm.delete_elin_group(name="ELIN1")
        op, body = sent(ucm)
        assert op == "removeElinGroup"
        assert text(body, "name") == "ELIN1"


class TestExternalCallControlProfile:
    def test_add_builds_wrapper(self, ucm):
        ucm.add_external_call_control_profile(name="ECCP1", primaryUri="sip:eccp@10.0.0.1")
        op, body = sent(ucm)
        assert op == "addExternalCallControlProfile"
        assert text(body, "externalCallControlProfile/name") == "ECCP1"

    def test_get_unwraps(self, ucm):
        ucm.recorder.responses["getExternalCallControlProfile"] = {
            "return": {"externalCallControlProfile": {"name": "ECCP1"}}
        }
        assert ucm.get_external_call_control_profile(name="ECCP1") == {"name": "ECCP1"}

    def test_list_returns_list(self, ucm):
        ucm.recorder.responses["listExternalCallControlProfile"] = {
            "return": {"externalCallControlProfile": [{"name": "ECCP1"}]}
        }
        result = ucm.get_external_call_control_profiles()
        assert len(result) == 1

    def test_list_empty(self, ucm):
        ucm.recorder.responses["listExternalCallControlProfile"] = {"return": None}
        assert ucm.get_external_call_control_profiles() == []

    def test_update(self, ucm):
        # UpdateExternalCallControlProfileReq valid fields: newName, primaryUri, ...
        ucm.update_external_call_control_profile(name="ECCP1", newName="ECCP1-Updated")
        op, _ = sent(ucm)
        assert op == "updateExternalCallControlProfile"

    def test_delete(self, ucm):
        ucm.delete_external_call_control_profile(name="ECCP1")
        op, body = sent(ucm)
        assert op == "removeExternalCallControlProfile"
        assert text(body, "name") == "ECCP1"


class TestFacInfo:
    def test_add_builds_wrapper(self, ucm):
        ucm.add_fac_info(name="FAC1", code="1234", authorizationLevel=0)
        op, body = sent(ucm)
        assert op == "addFacInfo"
        assert text(body, "facInfo/name") == "FAC1"

    def test_get_unwraps(self, ucm):
        ucm.recorder.responses["getFacInfo"] = {
            "return": {"facInfo": {"name": "FAC1", "code": "1234"}}
        }
        assert ucm.get_fac_info(name="FAC1")["name"] == "FAC1"

    def test_list_returns_list(self, ucm):
        ucm.recorder.responses["listFacInfo"] = {
            "return": {"facInfo": [{"name": "FAC1"}, {"name": "FAC2"}]}
        }
        result = ucm.get_fac_infos()
        assert len(result) == 2

    def test_list_empty(self, ucm):
        ucm.recorder.responses["listFacInfo"] = {"return": None}
        assert ucm.get_fac_infos() == []

    def test_update(self, ucm):
        ucm.update_fac_info(name="FAC1", code="9999")
        op, _ = sent(ucm)
        assert op == "updateFacInfo"

    def test_delete(self, ucm):
        ucm.delete_fac_info(name="FAC1")
        op, body = sent(ucm)
        assert op == "removeFacInfo"
        assert text(body, "name") == "FAC1"


class TestTransPatternOptions:
    def test_get_unwraps(self, ucm):
        ucm.recorder.responses["getTransPatternOptions"] = {
            "return": {"transPattern": {"patternUrgency": "f"}}
        }
        result = ucm.get_trans_pattern_options()
        assert "patternUrgency" in result


class TestTransformationProfile:
    def test_add_builds_wrapper(self, ucm):
        ucm.add_transformation_profile(name="TP1")
        op, body = sent(ucm)
        assert op == "addTransformationProfile"
        assert text(body, "transformationProfile/name") == "TP1"

    def test_get_unwraps(self, ucm):
        ucm.recorder.responses["getTransformationProfile"] = {
            "return": {"transformationProfile": {"name": "TP1"}}
        }
        assert ucm.get_transformation_profile(name="TP1") == {"name": "TP1"}

    def test_list_returns_list(self, ucm):
        ucm.recorder.responses["listTransformationProfile"] = {
            "return": {"transformationProfile": [{"name": "TP1"}, {"name": "TP2"}]}
        }
        result = ucm.get_transformation_profiles()
        assert len(result) == 2

    def test_list_empty(self, ucm):
        ucm.recorder.responses["listTransformationProfile"] = {"return": None}
        assert ucm.get_transformation_profiles() == []

    def test_update(self, ucm):
        ucm.update_transformation_profile(name="TP1", description="Updated")
        op, _ = sent(ucm)
        assert op == "updateTransformationProfile"

    def test_delete(self, ucm):
        ucm.delete_transformation_profile(name="TP1")
        op, body = sent(ucm)
        assert op == "removeTransformationProfile"
        assert text(body, "name") == "TP1"


class TestH323Trunk:
    def test_add_builds_wrapper(self, ucm):
        # XH323Trunk requires: name, product, class, protocol, protocolSide, devicePoolName, locationName
        ucm.add_h323_trunk(
            name="H323_1",
            product="H.323 Client",
            **{"class": "Gateway"},
            protocol="H225",
            protocolSide="Network",
            devicePoolName="Default",
            locationName="Hub_None",
        )
        op, body = sent(ucm)
        assert op == "addH323Trunk"
        assert text(body, "h323Trunk/name") == "H323_1"

    def test_get_unwraps(self, ucm):
        ucm.recorder.responses["getH323Trunk"] = {
            "return": {"h323Trunk": {"name": "H323_1"}}
        }
        assert ucm.get_h323_trunk(name="H323_1") == {"name": "H323_1"}

    def test_list_returns_list(self, ucm):
        ucm.recorder.responses["listH323Trunk"] = {
            "return": {"h323Trunk": [{"name": "H323_1"}, {"name": "H323_2"}]}
        }
        result = ucm.get_h323_trunks()
        assert len(result) == 2

    def test_list_empty(self, ucm):
        ucm.recorder.responses["listH323Trunk"] = {"return": None}
        assert ucm.get_h323_trunks() == []

    def test_update(self, ucm):
        ucm.update_h323_trunk(name="H323_1", description="Updated")
        op, _ = sent(ucm)
        assert op == "updateH323Trunk"

    def test_delete(self, ucm):
        ucm.delete_h323_trunk(name="H323_1")
        op, body = sent(ucm)
        assert op == "removeH323Trunk"
        assert text(body, "name") == "H323_1"

    def test_reset(self, ucm):
        ucm.reset_h323_trunk(name="H323_1")
        op, body = sent(ucm)
        assert op == "resetH323Trunk"
        assert text(body, "name") == "H323_1"


class TestSipProfileOptions:
    def test_get_unwraps(self, ucm):
        ucm.recorder.responses["getSipProfileOptions"] = {
            "return": {"sipProfile": {"sipSessionRefreshMethod": "invite"}}
        }
        result = ucm.get_sip_profile_options()
        assert "sipSessionRefreshMethod" in result


class TestAnnouncement:
    def test_add_builds_wrapper(self, ucm):
        ucm.add_announcement(name="ANN1")
        op, body = sent(ucm)
        assert op == "addAnnouncement"
        assert text(body, "announcement/name") == "ANN1"

    def test_get_unwraps(self, ucm):
        ucm.recorder.responses["getAnnouncement"] = {
            "return": {"announcement": {"name": "ANN1"}}
        }
        assert ucm.get_announcement(name="ANN1") == {"name": "ANN1"}

    def test_list_returns_list(self, ucm):
        ucm.recorder.responses["listAnnouncement"] = {
            "return": {"announcement": [{"name": "ANN1"}, {"name": "ANN2"}]}
        }
        result = ucm.get_announcements()
        assert len(result) == 2

    def test_list_empty(self, ucm):
        ucm.recorder.responses["listAnnouncement"] = {"return": None}
        assert ucm.get_announcements() == []

    def test_update(self, ucm):
        ucm.update_announcement(name="ANN1", description="Updated")
        op, _ = sent(ucm)
        assert op == "updateAnnouncement"

    def test_delete(self, ucm):
        ucm.delete_announcement(name="ANN1")
        op, body = sent(ucm)
        assert op == "removeAnnouncement"
        assert text(body, "name") == "ANN1"


class TestAnnunciator:
    def test_get_unwraps(self, ucm):
        ucm.recorder.responses["getAnnunciator"] = {
            "return": {"annunciator": {"name": "ANN_SRV1"}}
        }
        assert ucm.get_annunciator(name="ANN_SRV1") == {"name": "ANN_SRV1"}

    def test_list_returns_list(self, ucm):
        ucm.recorder.responses["listAnnunciator"] = {
            "return": {"annunciator": [{"name": "ANN_SRV1"}]}
        }
        result = ucm.get_annunciators()
        assert result[0]["name"] == "ANN_SRV1"

    def test_list_empty(self, ucm):
        ucm.recorder.responses["listAnnunciator"] = {"return": None}
        assert ucm.get_annunciators() == []

    def test_update(self, ucm):
        ucm.update_annunciator(name="ANN_SRV1", description="Updated")
        op, _ = sent(ucm)
        assert op == "updateAnnunciator"


class TestAudioCodecPreferenceList:
    def test_add_builds_wrapper(self, ucm):
        # XAudioCodecPreferenceList requires: name, description, codecsInList.codecNames
        ucm.add_audio_codec_preference_list(
            name="ACPL1",
            description="Test codec list",
            codecsInList={"codecNames": ["G.711a"]},
        )
        op, body = sent(ucm)
        assert op == "addAudioCodecPreferenceList"
        assert text(body, "audioCodecPreferenceList/name") == "ACPL1"

    def test_get_unwraps(self, ucm):
        ucm.recorder.responses["getAudioCodecPreferenceList"] = {
            "return": {"audioCodecPreferenceList": {"name": "ACPL1"}}
        }
        assert ucm.get_audio_codec_preference_list(name="ACPL1") == {"name": "ACPL1"}

    def test_list_returns_list(self, ucm):
        ucm.recorder.responses["listAudioCodecPreferenceList"] = {
            "return": {"audioCodecPreferenceList": [{"name": "ACPL1"}, {"name": "ACPL2"}]}
        }
        result = ucm.get_audio_codec_preference_lists()
        assert len(result) == 2

    def test_list_empty(self, ucm):
        ucm.recorder.responses["listAudioCodecPreferenceList"] = {"return": None}
        assert ucm.get_audio_codec_preference_lists() == []

    def test_update(self, ucm):
        ucm.update_audio_codec_preference_list(name="ACPL1", description="Updated")
        op, _ = sent(ucm)
        assert op == "updateAudioCodecPreferenceList"

    def test_delete(self, ucm):
        ucm.delete_audio_codec_preference_list(name="ACPL1")
        op, body = sent(ucm)
        assert op == "removeAudioCodecPreferenceList"
        assert text(body, "name") == "ACPL1"


class TestConferenceNow:
    def test_add_builds_wrapper(self, ucm):
        ucm.add_conference_now(conferenceNowNumber="8300")
        op, body = sent(ucm)
        assert op == "addConferenceNow"
        assert text(body, "conferenceNow/conferenceNowNumber") == "8300"

    def test_get_unwraps(self, ucm):
        ucm.recorder.responses["getConferenceNow"] = {
            "return": {"conferenceNow": {"conferenceNowNumber": "8300"}}
        }
        result = ucm.get_conference_now(conferenceNowNumber="8300")
        assert result["conferenceNowNumber"] == "8300"

    def test_list_returns_list(self, ucm):
        ucm.recorder.responses["listConferenceNow"] = {
            "return": {"conferenceNow": [{"conferenceNowNumber": "8300"}]}
        }
        result = ucm.get_conference_nows()
        assert result[0]["conferenceNowNumber"] == "8300"

    def test_list_empty(self, ucm):
        ucm.recorder.responses["listConferenceNow"] = {"return": None}
        assert ucm.get_conference_nows() == []

    def test_update(self, ucm):
        ucm.update_conference_now(conferenceNowNumber="8300", description="Updated")
        op, _ = sent(ucm)
        assert op == "updateConferenceNow"

    def test_delete(self, ucm):
        # RemoveConferenceNowReq: uuid or (conferenceNowNumber + optional routePartitionName)
        ucm.delete_conference_now(conferenceNowNumber="8300")
        op, body = sent(ucm)
        assert op == "removeConferenceNow"
        assert text(body, "conferenceNowNumber") == "8300"


class TestFixedMohAudioSource:
    def test_get_unwraps(self, ucm):
        # GetFixedMohAudioSourceReq: name or uuid  (not sourceId)
        ucm.recorder.responses["getFixedMohAudioSource"] = {
            "return": {"fixedMohAudioSource": {"name": "Silence"}}
        }
        result = ucm.get_fixed_moh_audio_source(name="Silence")
        assert result["name"] == "Silence"

    def test_update(self, ucm):
        # UpdateFixedMohAudioSourceReq: name or uuid as identity
        ucm.update_fixed_moh_audio_source(name="Silence", multicast=False)
        op, _ = sent(ucm)
        assert op == "updateFixedMohAudioSource"


class TestInteractiveVoiceResponse:
    def test_get_unwraps(self, ucm):
        ucm.recorder.responses["getInteractiveVoiceResponse"] = {
            "return": {"interactiveVoiceResponse": {"name": "IVR1"}}
        }
        assert ucm.get_interactive_voice_response(name="IVR1") == {"name": "IVR1"}

    def test_list_returns_list(self, ucm):
        ucm.recorder.responses["listInteractiveVoiceResponse"] = {
            "return": {"interactiveVoiceResponse": [{"name": "IVR1"}, {"name": "IVR2"}]}
        }
        result = ucm.get_interactive_voice_responses()
        assert len(result) == 2

    def test_list_empty(self, ucm):
        ucm.recorder.responses["listInteractiveVoiceResponse"] = {"return": None}
        assert ucm.get_interactive_voice_responses() == []

    def test_update(self, ucm):
        ucm.update_interactive_voice_response(name="IVR1", description="Updated")
        op, _ = sent(ucm)
        assert op == "updateInteractiveVoiceResponse"


class TestCallerFilterList:
    def test_add_builds_wrapper(self, ucm):
        ucm.add_caller_filter_list(name="CFL1", isAllowedType=True)
        op, body = sent(ucm)
        assert op == "addCallerFilterList"
        assert text(body, "callerFilterList/name") == "CFL1"

    def test_get_unwraps(self, ucm):
        ucm.recorder.responses["getCallerFilterList"] = {
            "return": {"callerFilterList": {"name": "CFL1"}}
        }
        assert ucm.get_caller_filter_list(name="CFL1") == {"name": "CFL1"}

    def test_list_returns_list(self, ucm):
        ucm.recorder.responses["listCallerFilterList"] = {
            "return": {"callerFilterList": [{"name": "CFL1"}, {"name": "CFL2"}]}
        }
        result = ucm.get_caller_filter_lists()
        assert len(result) == 2

    def test_list_empty(self, ucm):
        ucm.recorder.responses["listCallerFilterList"] = {"return": None}
        assert ucm.get_caller_filter_lists() == []

    def test_update(self, ucm):
        ucm.update_caller_filter_list(name="CFL1", description="Updated")
        op, _ = sent(ucm)
        assert op == "updateCallerFilterList"

    def test_delete(self, ucm):
        ucm.delete_caller_filter_list(name="CFL1")
        op, body = sent(ucm)
        assert op == "removeCallerFilterList"
        assert text(body, "name") == "CFL1"


class TestEnterpriseFeatureAccessConfiguration:
    def test_add_builds_wrapper(self, ucm):
        ucm.add_enterprise_feature_access_configuration(pattern="*77")
        op, body = sent(ucm)
        assert op == "addEnterpriseFeatureAccessConfiguration"
        assert text(body, "enterpriseFeatureAccessConfiguration/pattern") == "*77"

    def test_get_unwraps(self, ucm):
        ucm.recorder.responses["getEnterpriseFeatureAccessConfiguration"] = {
            "return": {"enterpriseFeatureAccessConfiguration": {"pattern": "*77"}}
        }
        result = ucm.get_enterprise_feature_access_configuration(pattern="*77")
        assert result["pattern"] == "*77"

    def test_list_returns_list(self, ucm):
        ucm.recorder.responses["listEnterpriseFeatureAccessConfiguration"] = {
            "return": {
                "enterpriseFeatureAccessConfiguration": [
                    {"pattern": "*77"},
                    {"pattern": "*78"},
                ]
            }
        }
        result = ucm.get_enterprise_feature_access_configurations()
        assert len(result) == 2

    def test_list_empty(self, ucm):
        ucm.recorder.responses["listEnterpriseFeatureAccessConfiguration"] = {"return": None}
        assert ucm.get_enterprise_feature_access_configurations() == []

    def test_update(self, ucm):
        ucm.update_enterprise_feature_access_configuration(pattern="*77", description="Updated")
        op, _ = sent(ucm)
        assert op == "updateEnterpriseFeatureAccessConfiguration"

    def test_delete(self, ucm):
        # RemoveEnterpriseFeatureAccessConfigurationReq: uuid or pattern
        ucm.delete_enterprise_feature_access_configuration(pattern="*77")
        op, body = sent(ucm)
        assert op == "removeEnterpriseFeatureAccessConfiguration"
        assert text(body, "pattern") == "*77"


class TestTodAccess:
    def test_add_builds_wrapper(self, ucm):
        # XTodAccess requires name and ownerIdName
        ucm.add_tod_access(name="TOD1", ownerIdName="SomeOwner")
        op, body = sent(ucm)
        assert op == "addTodAccess"
        assert text(body, "todAccess/name") == "TOD1"

    def test_get_unwraps(self, ucm):
        ucm.recorder.responses["getTodAccess"] = {
            "return": {"todAccess": {"name": "TOD1"}}
        }
        assert ucm.get_tod_access(name="TOD1") == {"name": "TOD1"}

    def test_list_returns_list(self, ucm):
        ucm.recorder.responses["listTodAccess"] = {
            "return": {"todAccess": [{"name": "TOD1"}, {"name": "TOD2"}]}
        }
        result = ucm.get_tod_access_list()
        assert len(result) == 2

    def test_list_empty(self, ucm):
        ucm.recorder.responses["listTodAccess"] = {"return": None}
        assert ucm.get_tod_access_list() == []

    def test_update(self, ucm):
        ucm.update_tod_access(name="TOD1", description="Updated")
        op, _ = sent(ucm)
        assert op == "updateTodAccess"

    def test_delete(self, ucm):
        ucm.delete_tod_access(name="TOD1")
        op, body = sent(ucm)
        assert op == "removeTodAccess"
        assert text(body, "name") == "TOD1"
