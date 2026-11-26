"""
Offline tests for P2 Batch B1 — Extended Media / Call-Control / Announcement mixin.

Entities:
  CalledPartyTracing, CmcInfo, ElinGroup, ExternalCallControlProfile,
  FacInfo, TransPatternOptions, TransformationProfile, H323Trunk,
  SipProfileOptions, Announcement, Annunciator, AudioCodecPreferenceList,
  ConferenceNow, FixedMohAudioSource, InteractiveVoiceResponse,
  CallerFilterList, EnterpriseFeatureAccessConfiguration, TodAccess

Run with: pytest tests/test_p2_b1_media.py
"""
import pytest

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from test_offline_requests import make_ucm, sent, text, has


# ---------------------------------------------------------------------------
# CalledPartyTracing  (no get — only add/list/remove)
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# CmcInfo  (identity: code)
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# ElinGroup
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# ExternalCallControlProfile
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# FacInfo
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# TransPatternOptions (get-only)
# ---------------------------------------------------------------------------
class TestTransPatternOptions:
    def test_get_unwraps(self, ucm):
        ucm.recorder.responses["getTransPatternOptions"] = {
            "return": {"transPatternOptions": {"patternUrgency": "f"}}
        }
        result = ucm.get_trans_pattern_options()
        assert "patternUrgency" in result


# ---------------------------------------------------------------------------
# TransformationProfile
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# H323Trunk
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# SipProfileOptions (get-only)
# ---------------------------------------------------------------------------
class TestSipProfileOptions:
    def test_get_unwraps(self, ucm):
        ucm.recorder.responses["getSipProfileOptions"] = {
            "return": {"sipProfileOptions": {"sipSessionRefreshMethod": "invite"}}
        }
        result = ucm.get_sip_profile_options()
        assert "sipSessionRefreshMethod" in result


# ---------------------------------------------------------------------------
# Announcement
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# Annunciator (no add, no remove)
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# AudioCodecPreferenceList
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# ConferenceNow  (list by conferenceNowNumber)
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# FixedMohAudioSource (get/update only)
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# InteractiveVoiceResponse (no add, no remove)
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# CallerFilterList
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# EnterpriseFeatureAccessConfiguration  (list by pattern)
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# TodAccess
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# Shared fixture
# ---------------------------------------------------------------------------
@pytest.fixture
def ucm():
    return make_ucm("15.0")
