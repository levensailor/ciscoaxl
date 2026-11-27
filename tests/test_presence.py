"""Offline request tests for ciscoaxl/presence.py.

Run with: pytest tests/test_presence.py
"""
import pytest

from test_offline_requests import make_ucm, sent, text, has


@pytest.fixture
def ucm():
    return make_ucm("15.0")


class TestServiceProfile:
    def test_get_service_profiles_returns_list(self, ucm):
        ucm.recorder.responses["listServiceProfile"] = {
            "return": {"serviceProfile": [{"name": "SP1"}, {"name": "SP2"}]}
        }
        result = ucm.get_service_profiles()
        assert len(result) == 2
        assert result[0]["name"] == "SP1"

    def test_get_service_profiles_empty(self, ucm):
        ucm.recorder.responses["listServiceProfile"] = {"return": None}
        assert ucm.get_service_profiles() == []

    def test_get_service_profile_unwraps(self, ucm):
        ucm.recorder.responses["getServiceProfile"] = {
            "return": {"serviceProfile": {"name": "SP1"}}
        }
        assert ucm.get_service_profile(name="SP1") == {"name": "SP1"}

    def test_add_service_profile_builds_wrapper(self, ucm):
        ucm.add_service_profile(name="SP1")
        op, body = sent(ucm)
        assert op == "addServiceProfile"
        assert text(body, "serviceProfile/name") == "SP1"

    def test_update_service_profile(self, ucm):
        ucm.update_service_profile(name="SP1", description="Updated")
        op, _ = sent(ucm)
        assert op == "updateServiceProfile"

    def test_delete_service_profile(self, ucm):
        ucm.delete_service_profile(name="SP1")
        op, body = sent(ucm)
        assert op == "removeServiceProfile"
        assert text(body, "name") == "SP1"


class TestUcService:
    def test_get_uc_services_returns_list(self, ucm):
        ucm.recorder.responses["listUcService"] = {
            "return": {"ucService": [{"name": "UC1"}]}
        }
        result = ucm.get_uc_services()
        assert result[0]["name"] == "UC1"

    def test_get_uc_services_empty(self, ucm):
        ucm.recorder.responses["listUcService"] = {"return": None}
        assert ucm.get_uc_services() == []

    def test_get_uc_service_unwraps(self, ucm):
        ucm.recorder.responses["getUcService"] = {
            "return": {"ucService": {"name": "UC1"}}
        }
        assert ucm.get_uc_service(name="UC1") == {"name": "UC1"}

    def test_add_uc_service_builds_wrapper(self, ucm):
        ucm.add_uc_service(
            name="UC1",
            serviceType="Voicemail",
            productType="Unity Connection",
            hostnameorip="voicemail.example.com",
        )
        op, body = sent(ucm)
        assert op == "addUcService"
        assert text(body, "ucService/name") == "UC1"
        assert text(body, "ucService/hostnameorip") == "voicemail.example.com"

    def test_update_uc_service(self, ucm):
        ucm.update_uc_service(name="UC1", description="desc")
        op, _ = sent(ucm)
        assert op == "updateUcService"

    def test_delete_uc_service(self, ucm):
        ucm.delete_uc_service(name="UC1")
        op, body = sent(ucm)
        assert op == "removeUcService"
        assert text(body, "name") == "UC1"

    def test_apply_uc_service_by_name(self, ucm):
        ucm.apply_uc_service(name="UC1")
        op, body = sent(ucm)
        assert op == "applyUcService"
        assert text(body, "name") == "UC1"

    def test_reset_uc_service_by_name(self, ucm):
        ucm.reset_uc_service(name="UC1")
        op, body = sent(ucm)
        assert op == "resetUcService"
        assert text(body, "name") == "UC1"

    def test_restart_uc_service_by_name(self, ucm):
        ucm.restart_uc_service(name="UC1")
        op, body = sent(ucm)
        assert op == "restartUcService"
        assert text(body, "name") == "UC1"

    def test_apply_uc_service_requires_name_or_uuid(self, ucm):
        with pytest.raises(ValueError):
            ucm.apply_uc_service()

    def test_apply_uc_service_rejects_both(self, ucm):
        with pytest.raises(ValueError):
            ucm.apply_uc_service(name="UC1", uuid="{11111111-2222-3333-4444-555555555555}")


class TestVoiceMailPilot:
    def test_get_voice_mail_pilots_returns_list(self, ucm):
        ucm.recorder.responses["listVoiceMailPilot"] = {
            "return": {"voiceMailPilot": [{"dirn": "5000"}, {"dirn": "5001"}]}
        }
        result = ucm.get_voice_mail_pilots()
        assert len(result) == 2

    def test_get_voice_mail_pilots_empty(self, ucm):
        ucm.recorder.responses["listVoiceMailPilot"] = {"return": None}
        assert ucm.get_voice_mail_pilots() == []

    def test_get_voice_mail_pilot_unwraps(self, ucm):
        ucm.recorder.responses["getVoiceMailPilot"] = {
            "return": {"voiceMailPilot": {"dirn": "5000"}}
        }
        assert ucm.get_voice_mail_pilot(dirn="5000") == {"dirn": "5000"}

    def test_add_voice_mail_pilot_builds_wrapper(self, ucm):
        ucm.add_voice_mail_pilot(dirn="5000")
        op, body = sent(ucm)
        assert op == "addVoiceMailPilot"
        assert text(body, "voiceMailPilot/dirn") == "5000"

    def test_update_voice_mail_pilot(self, ucm):
        ucm.update_voice_mail_pilot(dirn="5000", isDefault=True)
        op, _ = sent(ucm)
        assert op == "updateVoiceMailPilot"

    def test_delete_voice_mail_pilot(self, ucm):
        ucm.delete_voice_mail_pilot(dirn="5000")
        op, body = sent(ucm)
        assert op == "removeVoiceMailPilot"
        assert text(body, "dirn") == "5000"


class TestVoiceMailProfile:
    def test_get_voice_mail_profiles_returns_list(self, ucm):
        ucm.recorder.responses["listVoiceMailProfile"] = {
            "return": {"voiceMailProfile": [{"name": "VMP1"}]}
        }
        result = ucm.get_voice_mail_profiles()
        assert result[0]["name"] == "VMP1"

    def test_get_voice_mail_profiles_empty(self, ucm):
        ucm.recorder.responses["listVoiceMailProfile"] = {"return": None}
        assert ucm.get_voice_mail_profiles() == []

    def test_get_voice_mail_profile_unwraps(self, ucm):
        ucm.recorder.responses["getVoiceMailProfile"] = {
            "return": {"voiceMailProfile": {"name": "VMP1"}}
        }
        assert ucm.get_voice_mail_profile(name="VMP1") == {"name": "VMP1"}

    def test_add_voice_mail_profile_builds_wrapper(self, ucm):
        ucm.add_voice_mail_profile(name="VMP1", voiceMailPilot={"dirn": "5000"})
        op, body = sent(ucm)
        assert op == "addVoiceMailProfile"
        assert text(body, "voiceMailProfile/name") == "VMP1"
        assert text(body, "voiceMailProfile/voiceMailPilot/dirn") == "5000"

    def test_update_voice_mail_profile(self, ucm):
        ucm.update_voice_mail_profile(name="VMP1", description="desc")
        op, _ = sent(ucm)
        assert op == "updateVoiceMailProfile"

    def test_delete_voice_mail_profile(self, ucm):
        ucm.delete_voice_mail_profile(name="VMP1")
        op, body = sent(ucm)
        assert op == "removeVoiceMailProfile"
        assert text(body, "name") == "VMP1"

    def test_apply_voice_mail_profile_by_name(self, ucm):
        ucm.apply_voice_mail_profile(name="VMP1")
        op, body = sent(ucm)
        assert op == "applyVoiceMailProfile"
        assert text(body, "name") == "VMP1"

    def test_reset_voice_mail_profile_by_name(self, ucm):
        ucm.reset_voice_mail_profile(name="VMP1")
        op, body = sent(ucm)
        assert op == "resetVoiceMailProfile"
        assert text(body, "name") == "VMP1"

    def test_restart_voice_mail_profile_by_name(self, ucm):
        ucm.restart_voice_mail_profile(name="VMP1")
        op, body = sent(ucm)
        assert op == "restartVoiceMailProfile"
        assert text(body, "name") == "VMP1"

    def test_apply_requires_name_or_uuid(self, ucm):
        with pytest.raises(ValueError):
            ucm.apply_voice_mail_profile()

    def test_reset_requires_name_or_uuid(self, ucm):
        with pytest.raises(ValueError):
            ucm.reset_voice_mail_profile()

    def test_restart_requires_name_or_uuid(self, ucm):
        with pytest.raises(ValueError):
            ucm.restart_voice_mail_profile()


class TestTimePeriod:
    def test_get_time_periods_returns_list(self, ucm):
        ucm.recorder.responses["listTimePeriod"] = {
            "return": {"timePeriod": [{"name": "TP1"}, {"name": "TP2"}]}
        }
        result = ucm.get_time_periods()
        assert len(result) == 2

    def test_get_time_periods_empty(self, ucm):
        ucm.recorder.responses["listTimePeriod"] = {"return": None}
        assert ucm.get_time_periods() == []

    def test_get_time_period_unwraps(self, ucm):
        ucm.recorder.responses["getTimePeriod"] = {
            "return": {"timePeriod": {"name": "TP1"}}
        }
        assert ucm.get_time_period(name="TP1") == {"name": "TP1"}

    def test_add_time_period_builds_wrapper(self, ucm):
        ucm.add_time_period(name="TP1")
        op, body = sent(ucm)
        assert op == "addTimePeriod"
        assert text(body, "timePeriod/name") == "TP1"

    def test_update_time_period(self, ucm):
        ucm.update_time_period(name="TP1", description="desc")
        op, _ = sent(ucm)
        assert op == "updateTimePeriod"

    def test_delete_time_period(self, ucm):
        ucm.delete_time_period(name="TP1")
        op, body = sent(ucm)
        assert op == "removeTimePeriod"
        assert text(body, "name") == "TP1"


class TestTimeSchedule:
    def test_get_time_schedules_returns_list(self, ucm):
        ucm.recorder.responses["listTimeSchedule"] = {
            "return": {"timeSchedule": [{"name": "TS1"}]}
        }
        result = ucm.get_time_schedules()
        assert result[0]["name"] == "TS1"

    def test_get_time_schedules_empty(self, ucm):
        ucm.recorder.responses["listTimeSchedule"] = {"return": None}
        assert ucm.get_time_schedules() == []

    def test_get_time_schedule_unwraps(self, ucm):
        ucm.recorder.responses["getTimeSchedule"] = {
            "return": {"timeSchedule": {"name": "TS1"}}
        }
        assert ucm.get_time_schedule(name="TS1") == {"name": "TS1"}

    def test_add_time_schedule_builds_wrapper(self, ucm):
        ucm.add_time_schedule(name="TS1", members={"member": [{"timePeriodName": "TP1"}]})
        op, body = sent(ucm)
        assert op == "addTimeSchedule"
        assert text(body, "timeSchedule/name") == "TS1"

    def test_update_time_schedule(self, ucm):
        ucm.update_time_schedule(name="TS1", description="desc")
        op, _ = sent(ucm)
        assert op == "updateTimeSchedule"

    def test_delete_time_schedule(self, ucm):
        ucm.delete_time_schedule(name="TS1")
        op, body = sent(ucm)
        assert op == "removeTimeSchedule"
        assert text(body, "name") == "TS1"


class TestCallPark:
    def test_get_call_parks_returns_list(self, ucm):
        ucm.recorder.responses["listCallPark"] = {
            "return": {"callPark": [{"pattern": "1234"}, {"pattern": "1235"}]}
        }
        result = ucm.get_call_parks()
        assert len(result) == 2

    def test_get_call_parks_empty(self, ucm):
        ucm.recorder.responses["listCallPark"] = {"return": None}
        assert ucm.get_call_parks() == []

    def test_get_call_park_unwraps(self, ucm):
        ucm.recorder.responses["getCallPark"] = {
            "return": {"callPark": {"pattern": "1234"}}
        }
        assert ucm.get_call_park(pattern="1234") == {"pattern": "1234"}

    def test_add_call_park_builds_wrapper(self, ucm):
        ucm.add_call_park(pattern="1234", callManagerName="cucm-pub")
        op, body = sent(ucm)
        assert op == "addCallPark"
        assert text(body, "callPark/pattern") == "1234"
        assert text(body, "callPark/callManagerName") == "cucm-pub"

    def test_update_call_park(self, ucm):
        ucm.update_call_park(pattern="1234", description="Park here")
        op, _ = sent(ucm)
        assert op == "updateCallPark"

    def test_delete_call_park_by_pattern(self, ucm):
        ucm.delete_call_park(pattern="1234")
        op, body = sent(ucm)
        assert op == "removeCallPark"
        assert text(body, "pattern") == "1234"

    def test_delete_call_park_by_uuid(self, ucm):
        ucm.delete_call_park(uuid="{11111111-2222-3333-4444-555555555555}")
        op, body = sent(ucm)
        assert op == "removeCallPark"
        assert text(body, "uuid") == "{11111111-2222-3333-4444-555555555555}"

    def test_get_call_park_with_partition(self, ucm):
        ucm.get_call_park(pattern="1234", routePartitionName="Park_PT")
        op, body = sent(ucm)
        assert op == "getCallPark"
        assert text(body, "pattern") == "1234"
        assert text(body, "routePartitionName") == "Park_PT"


class TestAssignedPresenceServers:
    def test_get_assigned_presence_servers_returns_list(self, ucm):
        ucm.recorder.responses["listAssignedPresenceServers"] = {
            "return": {"assignedPresenceServers": [{"name": "imp-pub"}, {"name": "imp-sub"}]}
        }
        result = ucm.get_assigned_presence_servers()
        op, body = sent(ucm)
        assert op == "listAssignedPresenceServers"
        assert len(result) == 2
        assert result[0]["name"] == "imp-pub"

    def test_get_assigned_presence_servers_empty(self, ucm):
        ucm.recorder.responses["listAssignedPresenceServers"] = {"return": None}
        assert ucm.get_assigned_presence_servers() == []


class TestUnassignedPresenceServers:
    def test_get_unassigned_presence_servers_returns_list(self, ucm):
        ucm.recorder.responses["listUnassignedPresenceServers"] = {
            "return": {"unassignedPresenceServers": [{"name": "imp-new"}]}
        }
        result = ucm.get_unassigned_presence_servers()
        op, body = sent(ucm)
        assert op == "listUnassignedPresenceServers"
        assert len(result) == 1

    def test_get_unassigned_presence_servers_empty(self, ucm):
        ucm.recorder.responses["listUnassignedPresenceServers"] = {"return": None}
        assert ucm.get_unassigned_presence_servers() == []


class TestAssignedPresenceUsers:
    def test_get_assigned_presence_users_returns_list(self, ucm):
        ucm.recorder.responses["listAssignedPresenceUsers"] = {
            "return": {
                "assignedPresenceUsers": [
                    {"userid": "jsmith", "server": "imp-pub"},
                    {"userid": "jdoe", "server": "imp-pub"},
                ]
            }
        }
        result = ucm.get_assigned_presence_users()
        op, body = sent(ucm)
        assert op == "listAssignedPresenceUsers"
        assert len(result) == 2

    def test_get_assigned_presence_users_empty(self, ucm):
        ucm.recorder.responses["listAssignedPresenceUsers"] = {"return": None}
        assert ucm.get_assigned_presence_users() == []


class TestUnassignedPresenceUsers:
    def test_get_unassigned_presence_users_returns_list(self, ucm):
        ucm.recorder.responses["listUnassignedPresenceUsers"] = {
            "return": {"unassignedPresenceUsers": [{"userid": "jsmith"}]}
        }
        result = ucm.get_unassigned_presence_users()
        op, body = sent(ucm)
        assert op == "listUnassignedPresenceUsers"
        assert len(result) == 1

    def test_get_unassigned_presence_users_empty(self, ucm):
        ucm.recorder.responses["listUnassignedPresenceUsers"] = {"return": None}
        assert ucm.get_unassigned_presence_users() == []


class TestPresenceUser:
    def test_assign_presence_user(self, ucm):
        ucm.assign_presence_user(userid="jsmith", server="imp-pub")
        op, body = sent(ucm)
        assert op == "assignPresenceUser"
        assert text(body, "userid") == "jsmith"
        assert text(body, "server") == "imp-pub"

    def test_unassign_presence_user(self, ucm):
        ucm.unassign_presence_user(userid="jsmith")
        op, body = sent(ucm)
        assert op == "unassignPresenceUser"
        assert text(body, "userid") == "jsmith"


class TestPresenceRedundancyGroup:
    def test_add_presence_redundancy_group(self, ucm):
        ucm.add_presence_redundancy_group(name="PRG1", server1="imp-pub", server2="imp-sub")
        op, body = sent(ucm)
        assert op == "addPresenceRedundancyGroup"
        assert text(body, "presenceRedundancyGroup/name") == "PRG1"

    def test_get_presence_redundancy_group(self, ucm):
        ucm.recorder.responses["getPresenceRedundancyGroup"] = {
            "return": {"presenceRedundancyGroup": {"name": "PRG1"}}
        }
        result = ucm.get_presence_redundancy_group(name="PRG1")
        op, body = sent(ucm)
        assert op == "getPresenceRedundancyGroup"
        assert text(body, "name") == "PRG1"
        assert result == {"name": "PRG1"}

    def test_get_presence_redundancy_groups(self, ucm):
        ucm.recorder.responses["listPresenceRedundancyGroup"] = {
            "return": {"presenceRedundancyGroup": [{"name": "PRG1"}]}
        }
        result = ucm.get_presence_redundancy_groups()
        op, _ = sent(ucm)
        assert op == "listPresenceRedundancyGroup"
        assert result[0]["name"] == "PRG1"

    def test_get_presence_redundancy_groups_empty(self, ucm):
        ucm.recorder.responses["listPresenceRedundancyGroup"] = {"return": None}
        assert ucm.get_presence_redundancy_groups() == []

    def test_update_presence_redundancy_group(self, ucm):
        ucm.update_presence_redundancy_group(name="PRG1", description="Updated")
        op, body = sent(ucm)
        assert op == "updatePresenceRedundancyGroup"
        assert text(body, "name") == "PRG1"

    def test_delete_presence_redundancy_group(self, ucm):
        ucm.delete_presence_redundancy_group(name="PRG1")
        op, body = sent(ucm)
        assert op == "removePresenceRedundancyGroup"
        assert text(body, "name") == "PRG1"

    def test_delete_presence_redundancy_group_by_uuid(self, ucm):
        ucm.delete_presence_redundancy_group(uuid="{AAAA-1111}")
        op, body = sent(ucm)
        assert op == "removePresenceRedundancyGroup"
        assert text(body, "uuid") == "{AAAA-1111}"
        assert not has(body, "name")


class TestExpresswayCConfiguration:
    def test_add_expressway_c_configuration(self, ucm):
        ucm.add_expressway_c_configuration(HostNameOrIP="exp-c.corp.com")
        op, body = sent(ucm)
        assert op == "addExpresswayCConfiguration"
        assert text(body, "expresswayCConfiguration/HostNameOrIP") == "exp-c.corp.com"

    def test_get_expressway_c_configuration(self, ucm):
        ucm.recorder.responses["getExpresswayCConfiguration"] = {
            "return": {"expresswayCConfiguration": {"HostNameOrIP": "exp-c.corp.com"}}
        }
        result = ucm.get_expressway_c_configuration(HostNameOrIP="exp-c.corp.com")
        op, body = sent(ucm)
        assert op == "getExpresswayCConfiguration"
        assert result == {"HostNameOrIP": "exp-c.corp.com"}

    def test_get_expressway_c_configurations(self, ucm):
        ucm.recorder.responses["listExpresswayCConfiguration"] = {
            "return": {"expresswayCConfiguration": [{"HostNameOrIP": "exp-c.corp.com"}]}
        }
        result = ucm.get_expressway_c_configurations()
        op, _ = sent(ucm)
        assert op == "listExpresswayCConfiguration"
        assert len(result) == 1

    def test_get_expressway_c_configurations_empty(self, ucm):
        ucm.recorder.responses["listExpresswayCConfiguration"] = {"return": None}
        assert ucm.get_expressway_c_configurations() == []

    def test_update_expressway_c_configuration(self, ucm):
        ucm.update_expressway_c_configuration(HostNameOrIP="exp-c.corp.com", description="Updated")
        op, body = sent(ucm)
        assert op == "updateExpresswayCConfiguration"

    def test_delete_expressway_c_configuration(self, ucm):
        ucm.delete_expressway_c_configuration(HostNameOrIP="exp-c.corp.com")
        op, body = sent(ucm)
        assert op == "removeExpresswayCConfiguration"


class TestMraServiceDomain:
    def test_add_mra_service_domain(self, ucm):
        ucm.add_mra_service_domain(name="corp.com", serviceDomains="corp.com")
        op, body = sent(ucm)
        assert op == "addMraServiceDomain"
        assert text(body, "mraServiceDomain/name") == "corp.com"

    def test_get_mra_service_domain(self, ucm):
        ucm.recorder.responses["getMraServiceDomain"] = {
            "return": {"mraServiceDomain": {"name": "corp.com"}}
        }
        result = ucm.get_mra_service_domain(name="corp.com")
        op, body = sent(ucm)
        assert op == "getMraServiceDomain"
        assert text(body, "name") == "corp.com"
        assert result == {"name": "corp.com"}

    def test_get_mra_service_domains(self, ucm):
        ucm.recorder.responses["listMraServiceDomain"] = {
            "return": {"mraServiceDomain": [{"name": "corp.com"}]}
        }
        result = ucm.get_mra_service_domains()
        op, _ = sent(ucm)
        assert op == "listMraServiceDomain"
        assert result[0]["name"] == "corp.com"

    def test_get_mra_service_domains_empty(self, ucm):
        ucm.recorder.responses["listMraServiceDomain"] = {"return": None}
        assert ucm.get_mra_service_domains() == []

    def test_update_mra_service_domain(self, ucm):
        ucm.update_mra_service_domain(name="corp.com", isDefault=True)
        op, body = sent(ucm)
        assert op == "updateMraServiceDomain"
        assert text(body, "name") == "corp.com"

    def test_delete_mra_service_domain(self, ucm):
        ucm.delete_mra_service_domain(name="corp.com")
        op, body = sent(ucm)
        assert op == "removeMraServiceDomain"
        assert text(body, "name") == "corp.com"

    def test_delete_mra_service_domain_by_uuid(self, ucm):
        ucm.delete_mra_service_domain(uuid="{BBBB-2222}")
        op, body = sent(ucm)
        assert op == "removeMraServiceDomain"
        assert text(body, "uuid") == "{BBBB-2222}"
