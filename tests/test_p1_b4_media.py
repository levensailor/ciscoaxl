"""
Offline tests for P1 Batch B4 — Media / Mobility / Presence mixin.

Entities: MeetMe, MohAudioSource, MohServer, RecordingProfile, RegionMatrix,
          DeviceMobility, DeviceMobilityGroup, MobileVoiceAccess, Mobility,
          MobilityProfile, PhysicalLocation, PresenceGroup

Run with: pytest tests/test_p1_b4_media.py
"""
import pytest
from zeep.exceptions import Fault

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from test_offline_requests import make_ucm, sent, text, has


# ---------------------------------------------------------------------------
# MeetMe
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# MohAudioSource (no add, identified by sourceId/uuid)
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# MohServer (no add, no remove)
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# RecordingProfile
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# RegionMatrix (update only)
# ---------------------------------------------------------------------------
class TestRegionMatrix:
    def test_update_region_matrix(self, ucm):
        ucm.update_region_matrix(regionAName="RegionA", regionBName="RegionB", bandwidth="64")
        op, body = sent(ucm)
        assert op == "updateRegionMatrix"
        assert text(body, "regionAName") == "RegionA"
        assert text(body, "regionBName") == "RegionB"


# ---------------------------------------------------------------------------
# DeviceMobility
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# DeviceMobilityGroup
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# MobileVoiceAccess (identified by pattern/uuid)
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# Mobility (no remove, no list; identified by handoffNumber/DTMFNumber)
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# MobilityProfile
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# PhysicalLocation
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# PresenceGroup
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# Shared fixture
# ---------------------------------------------------------------------------
@pytest.fixture
def ucm():
    return make_ucm("15.0")
