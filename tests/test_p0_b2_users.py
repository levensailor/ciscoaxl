"""Offline tests for P0 Batch B2 — user-related AXL wrappers.

Run with: uv run python -m pytest tests/test_p0_b2_users.py -q
"""
import pytest
from zeep.exceptions import Fault

from tests.test_offline_requests import make_ucm, sent, text, has


# ---------------------------------------------------------------------------
# Shared fixture
# ---------------------------------------------------------------------------

@pytest.fixture
def ucm():
    return make_ucm("15.0")


# ---------------------------------------------------------------------------
# AppUser
# ---------------------------------------------------------------------------

class TestAppUser:
    def test_get_app_users_returns_list(self, ucm):
        ucm.recorder.responses["listAppUser"] = {
            "return": {"appUser": [{"userid": "svc_account"}]}
        }
        result = ucm.get_app_users()
        assert isinstance(result, list)
        assert result[0]["userid"] == "svc_account"

    def test_get_app_users_empty(self, ucm):
        ucm.recorder.responses["listAppUser"] = {"return": None}
        assert ucm.get_app_users() == []

    def test_get_app_user_unwraps(self, ucm):
        ucm.recorder.responses["getAppUser"] = {
            "return": {"appUser": {"userid": "svc_account"}}
        }
        result = ucm.get_app_user(userid="svc_account")
        assert result["userid"] == "svc_account"

    def test_add_app_user_sends_correct_op(self, ucm):
        ucm.add_app_user(userid="svc_account")
        op, body = sent(ucm)
        assert op == "addAppUser"
        assert text(body, "appUser/userid") == "svc_account"

    def test_update_app_user_sends_correct_op(self, ucm):
        ucm.update_app_user(userid="svc_account", password="secret")
        op, body = sent(ucm)
        assert op == "updateAppUser"
        assert text(body, "userid") == "svc_account"

    def test_delete_app_user_sends_remove_op(self, ucm):
        ucm.delete_app_user(userid="svc_account")
        op, body = sent(ucm)
        assert op == "removeAppUser"
        assert text(body, "userid") == "svc_account"


# ---------------------------------------------------------------------------
# UserGroup
# ---------------------------------------------------------------------------

class TestUserGroup:
    def test_get_user_groups_returns_list(self, ucm):
        ucm.recorder.responses["listUserGroup"] = {
            "return": {"userGroup": [{"name": "Standard CCM End Users"}]}
        }
        result = ucm.get_user_groups()
        assert isinstance(result, list)
        assert result[0]["name"] == "Standard CCM End Users"

    def test_get_user_groups_empty(self, ucm):
        ucm.recorder.responses["listUserGroup"] = {"return": None}
        assert ucm.get_user_groups() == []

    def test_get_user_group_unwraps(self, ucm):
        ucm.recorder.responses["getUserGroup"] = {
            "return": {"userGroup": {"name": "Standard CCM End Users"}}
        }
        result = ucm.get_user_group(name="Standard CCM End Users")
        assert result["name"] == "Standard CCM End Users"

    def test_add_user_group_sends_correct_op(self, ucm):
        ucm.add_user_group(name="TestGroup")
        op, body = sent(ucm)
        assert op == "addUserGroup"
        assert text(body, "userGroup/name") == "TestGroup"

    def test_update_user_group_sends_correct_op(self, ucm):
        ucm.update_user_group(name="TestGroup", newName="TestGroupRenamed")
        op, body = sent(ucm)
        assert op == "updateUserGroup"
        assert text(body, "name") == "TestGroup"

    def test_delete_user_group_sends_remove_op(self, ucm):
        ucm.delete_user_group(name="TestGroup")
        op, body = sent(ucm)
        assert op == "removeUserGroup"
        assert text(body, "name") == "TestGroup"


# ---------------------------------------------------------------------------
# UserPhoneAssociation (add only)
# ---------------------------------------------------------------------------

class TestUserPhoneAssociation:
    def test_add_user_phone_association_sends_correct_op(self, ucm):
        ucm.add_user_phone_association(
            userId="jsmith",
            lastName="Smith",
            productType="Cisco 8861",
            name="SEP001122334455",
            e164Mask=None,
            extension="1000",
        )
        op, body = sent(ucm)
        assert op == "addUserPhoneAssociation"
        assert text(body, "userPhoneAssociation/userId") == "jsmith"


# ---------------------------------------------------------------------------
# UserProfileProvision
# ---------------------------------------------------------------------------

class TestUserProfileProvision:
    def test_get_user_profile_provisions_returns_list(self, ucm):
        ucm.recorder.responses["listUserProfileProvision"] = {
            "return": {"userProfileProvision": [{"name": "Default Profile"}]}
        }
        result = ucm.get_user_profile_provisions()
        assert isinstance(result, list)
        assert result[0]["name"] == "Default Profile"

    def test_get_user_profile_provisions_empty(self, ucm):
        ucm.recorder.responses["listUserProfileProvision"] = {"return": None}
        assert ucm.get_user_profile_provisions() == []

    def test_get_user_profile_provision_unwraps(self, ucm):
        ucm.recorder.responses["getUserProfileProvision"] = {
            "return": {"userProfileProvision": {"name": "Default Profile"}}
        }
        result = ucm.get_user_profile_provision(name="Default Profile")
        assert result["name"] == "Default Profile"

    def test_add_user_profile_provision_sends_correct_op(self, ucm):
        ucm.add_user_profile_provision(name="MyProfile")
        op, body = sent(ucm)
        assert op == "addUserProfileProvision"
        assert text(body, "userProfileProvision/name") == "MyProfile"

    def test_update_user_profile_provision_sends_correct_op(self, ucm):
        ucm.update_user_profile_provision(name="MyProfile", description="Updated")
        op, body = sent(ucm)
        assert op == "updateUserProfileProvision"

    def test_delete_user_profile_provision_sends_remove_op(self, ucm):
        ucm.delete_user_profile_provision(name="MyProfile")
        op, body = sent(ucm)
        assert op == "removeUserProfileProvision"
        assert text(body, "name") == "MyProfile"


# ---------------------------------------------------------------------------
# RemoteDestination
# ---------------------------------------------------------------------------

class TestRemoteDestination:
    def test_get_remote_destinations_returns_list(self, ucm):
        ucm.recorder.responses["listRemoteDestination"] = {
            "return": {"remoteDestination": [{"name": "Mobile", "destination": "+15550001234"}]}
        }
        result = ucm.get_remote_destinations()
        assert isinstance(result, list)
        assert result[0]["destination"] == "+15550001234"

    def test_get_remote_destinations_empty(self, ucm):
        ucm.recorder.responses["listRemoteDestination"] = {"return": None}
        assert ucm.get_remote_destinations() == []

    def test_get_remote_destination_unwraps(self, ucm):
        ucm.recorder.responses["getRemoteDestination"] = {
            "return": {"remoteDestination": {"name": "Mobile", "destination": "+15550001234"}}
        }
        # RemoteDestination is identified by destination or uuid (not name)
        result = ucm.get_remote_destination(destination="+15550001234")
        assert result["destination"] == "+15550001234"

    def test_add_remote_destination_sends_correct_op(self, ucm):
        ucm.add_remote_destination(
            name="Mobile",
            destination="+15550001234",
            ownerUserId="jsmith",
        )
        op, body = sent(ucm)
        assert op == "addRemoteDestination"
        assert text(body, "remoteDestination/destination") == "+15550001234"

    def test_update_remote_destination_sends_correct_op(self, ucm):
        ucm.update_remote_destination(destination="+15550001234", newDestination="+15559999999")
        op, body = sent(ucm)
        assert op == "updateRemoteDestination"

    def test_delete_remote_destination_sends_remove_op(self, ucm):
        ucm.delete_remote_destination(destination="+15550001234")
        op, body = sent(ucm)
        assert op == "removeRemoteDestination"
        assert text(body, "destination") == "+15550001234"


# ---------------------------------------------------------------------------
# RemoteDestinationProfile
# ---------------------------------------------------------------------------

class TestRemoteDestinationProfile:
    def test_get_remote_destination_profiles_returns_list(self, ucm):
        ucm.recorder.responses["listRemoteDestinationProfile"] = {
            "return": {"remoteDestinationProfile": [{"name": "RDP_jsmith"}]}
        }
        result = ucm.get_remote_destination_profiles()
        assert isinstance(result, list)
        assert result[0]["name"] == "RDP_jsmith"

    def test_get_remote_destination_profiles_empty(self, ucm):
        ucm.recorder.responses["listRemoteDestinationProfile"] = {"return": None}
        assert ucm.get_remote_destination_profiles() == []

    def test_get_remote_destination_profile_unwraps(self, ucm):
        ucm.recorder.responses["getRemoteDestinationProfile"] = {
            "return": {"remoteDestinationProfile": {"name": "RDP_jsmith"}}
        }
        result = ucm.get_remote_destination_profile(name="RDP_jsmith")
        assert result["name"] == "RDP_jsmith"

    def test_add_remote_destination_profile_sends_correct_op(self, ucm):
        ucm.add_remote_destination_profile(
            name="RDP_jsmith",
            product="Remote Destination Profile",
            **{"class": "Remote Destination Profile"},
            protocol="Remote Destination",
        )
        op, body = sent(ucm)
        assert op == "addRemoteDestinationProfile"
        assert text(body, "remoteDestinationProfile/name") == "RDP_jsmith"

    def test_update_remote_destination_profile_sends_correct_op(self, ucm):
        ucm.update_remote_destination_profile(name="RDP_jsmith", description="Updated")
        op, body = sent(ucm)
        assert op == "updateRemoteDestinationProfile"

    def test_delete_remote_destination_profile_sends_remove_op(self, ucm):
        ucm.delete_remote_destination_profile(name="RDP_jsmith")
        op, body = sent(ucm)
        assert op == "removeRemoteDestinationProfile"
        assert text(body, "name") == "RDP_jsmith"
