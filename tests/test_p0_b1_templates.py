"""Offline tests for P0 batch B1 — device settings / template wrappers.

Covers: CommonDeviceConfig, CommonPhoneConfig, PhoneButtonTemplate,
        SoftKeyTemplate, UniversalDeviceTemplate, UniversalLineTemplate

Run with: pytest tests/test_p0_b1_templates.py -q
"""
import pytest

from tests.test_offline_requests import make_ucm, sent, text, has


@pytest.fixture
def ucm():
    return make_ucm("15.0")


# ------------------------------------------------------------------ #
# CommonDeviceConfig                                                   #
# ------------------------------------------------------------------ #

class TestCommonDeviceConfig:
    def test_add_common_device_config_builds_message(self, ucm):
        ucm.add_common_device_config(name="TestCDC")
        op, body = sent(ucm)
        assert op == "addCommonDeviceConfig"
        assert text(body, "commonDeviceConfig/name") == "TestCDC"

    def test_get_common_device_config_unwraps(self, ucm):
        ucm.recorder.responses["getCommonDeviceConfig"] = {
            "return": {"commonDeviceConfig": {"name": "TestCDC", "softkeyTemplateName": None}}
        }
        result = ucm.get_common_device_config(name="TestCDC")
        assert result["name"] == "TestCDC"

    def test_get_common_device_configs_empty_list(self, ucm):
        ucm.recorder.responses["listCommonDeviceConfig"] = {"return": None}
        assert ucm.get_common_device_configs() == []

    def test_delete_common_device_config(self, ucm):
        ucm.delete_common_device_config(name="TestCDC")
        op, body = sent(ucm)
        assert op == "removeCommonDeviceConfig"
        assert text(body, "name") == "TestCDC"

    def test_apply_common_device_config(self, ucm):
        ucm.apply_common_device_config(name="TestCDC")
        op, body = sent(ucm)
        assert op == "applyCommonDeviceConfig"
        assert text(body, "name") == "TestCDC"

    def test_reset_common_device_config(self, ucm):
        ucm.reset_common_device_config(name="TestCDC")
        op, body = sent(ucm)
        assert op == "resetCommonDeviceConfig"
        assert text(body, "name") == "TestCDC"

    def test_apply_common_device_config_by_uuid(self, ucm):
        ucm.apply_common_device_config(uuid="{11111111-0000-0000-0000-000000000001}")
        op, body = sent(ucm)
        assert op == "applyCommonDeviceConfig"
        assert text(body, "uuid") == "{11111111-0000-0000-0000-000000000001}"
        assert not has(body, "name")

    def test_identify_requires_exactly_one(self, ucm):
        with pytest.raises(ValueError):
            ucm.apply_common_device_config()
        with pytest.raises(ValueError):
            ucm.apply_common_device_config(name="x", uuid="{a}")


# ------------------------------------------------------------------ #
# CommonPhoneConfig                                                    #
# ------------------------------------------------------------------ #

class TestCommonPhoneConfig:
    def test_add_common_phone_config_builds_message(self, ucm):
        ucm.add_common_phone_config(name="TestCPC")
        op, body = sent(ucm)
        assert op == "addCommonPhoneConfig"
        assert text(body, "commonPhoneConfig/name") == "TestCPC"

    def test_get_common_phone_config_unwraps(self, ucm):
        ucm.recorder.responses["getCommonPhoneConfig"] = {
            "return": {"commonPhoneConfig": {"name": "TestCPC"}}
        }
        result = ucm.get_common_phone_config(name="TestCPC")
        assert result["name"] == "TestCPC"

    def test_get_common_phone_configs_empty_list(self, ucm):
        ucm.recorder.responses["listCommonPhoneConfig"] = {"return": None}
        assert ucm.get_common_phone_configs() == []

    def test_delete_common_phone_config(self, ucm):
        ucm.delete_common_phone_config(name="TestCPC")
        op, body = sent(ucm)
        assert op == "removeCommonPhoneConfig"
        assert text(body, "name") == "TestCPC"

    def test_apply_common_phone_config(self, ucm):
        ucm.apply_common_phone_config(name="TestCPC")
        op, body = sent(ucm)
        assert op == "applyCommonPhoneConfig"
        assert text(body, "name") == "TestCPC"

    def test_reset_common_phone_config(self, ucm):
        ucm.reset_common_phone_config(name="TestCPC")
        op, body = sent(ucm)
        assert op == "resetCommonPhoneConfig"
        assert text(body, "name") == "TestCPC"


# ------------------------------------------------------------------ #
# PhoneButtonTemplate                                                  #
# ------------------------------------------------------------------ #

class TestPhoneButtonTemplate:
    def test_add_phone_button_template_builds_message(self, ucm):
        ucm.add_phone_button_template(
            name="TestPBT", basePhoneTemplateName="Standard 8945 SCCP"
        )
        op, body = sent(ucm)
        assert op == "addPhoneButtonTemplate"
        assert text(body, "phoneButtonTemplate/name") == "TestPBT"
        assert text(body, "phoneButtonTemplate/basePhoneTemplateName") == "Standard 8945 SCCP"

    def test_get_phone_button_template_unwraps(self, ucm):
        ucm.recorder.responses["getPhoneButtonTemplate"] = {
            "return": {"phoneButtonTemplate": {"name": "TestPBT", "basePhoneTemplateName": "Standard 8945 SCCP"}}
        }
        result = ucm.get_phone_button_template(name="TestPBT")
        assert result["name"] == "TestPBT"

    def test_get_phone_button_templates_empty_list(self, ucm):
        ucm.recorder.responses["listPhoneButtonTemplate"] = {"return": None}
        assert ucm.get_phone_button_templates() == []

    def test_delete_phone_button_template(self, ucm):
        ucm.delete_phone_button_template(name="TestPBT")
        op, body = sent(ucm)
        assert op == "removePhoneButtonTemplate"
        assert text(body, "name") == "TestPBT"

    def test_apply_phone_button_template(self, ucm):
        ucm.apply_phone_button_template(name="TestPBT")
        op, body = sent(ucm)
        assert op == "applyPhoneButtonTemplate"
        assert text(body, "name") == "TestPBT"

    def test_restart_phone_button_template(self, ucm):
        ucm.restart_phone_button_template(name="TestPBT")
        op, body = sent(ucm)
        assert op == "restartPhoneButtonTemplate"
        assert text(body, "name") == "TestPBT"


# ------------------------------------------------------------------ #
# SoftKeyTemplate                                                      #
# ------------------------------------------------------------------ #

class TestSoftKeyTemplate:
    def test_add_soft_key_template_builds_message(self, ucm):
        ucm.add_soft_key_template(
            name="TestSKT",
            description="Test Soft Key Template",
            baseSoftkeyTemplateName="Standard User",
        )
        op, body = sent(ucm)
        assert op == "addSoftKeyTemplate"
        assert text(body, "softKeyTemplate/name") == "TestSKT"
        assert text(body, "softKeyTemplate/description") == "Test Soft Key Template"
        assert text(body, "softKeyTemplate/baseSoftkeyTemplateName") == "Standard User"

    def test_get_soft_key_template_unwraps(self, ucm):
        ucm.recorder.responses["getSoftKeyTemplate"] = {
            "return": {"softKeyTemplate": {"name": "TestSKT", "description": "Test"}}
        }
        result = ucm.get_soft_key_template(name="TestSKT")
        assert result["name"] == "TestSKT"

    def test_get_soft_key_templates_empty_list(self, ucm):
        ucm.recorder.responses["listSoftKeyTemplate"] = {"return": None}
        assert ucm.get_soft_key_templates() == []

    def test_delete_soft_key_template(self, ucm):
        ucm.delete_soft_key_template(name="TestSKT")
        op, body = sent(ucm)
        assert op == "removeSoftKeyTemplate"
        assert text(body, "name") == "TestSKT"

    def test_apply_soft_key_template(self, ucm):
        ucm.apply_soft_key_template(name="TestSKT")
        op, body = sent(ucm)
        assert op == "applySoftKeyTemplate"
        assert text(body, "name") == "TestSKT"

    def test_restart_soft_key_template(self, ucm):
        ucm.restart_soft_key_template(name="TestSKT")
        op, body = sent(ucm)
        assert op == "restartSoftKeyTemplate"
        assert text(body, "name") == "TestSKT"

    def test_restart_soft_key_template_by_uuid(self, ucm):
        ucm.restart_soft_key_template(uuid="{22222222-0000-0000-0000-000000000002}")
        op, body = sent(ucm)
        assert op == "restartSoftKeyTemplate"
        assert text(body, "uuid") == "{22222222-0000-0000-0000-000000000002}"
        assert not has(body, "name")


# ------------------------------------------------------------------ #
# UniversalDeviceTemplate                                             #
# ------------------------------------------------------------------ #

class TestUniversalDeviceTemplate:
    def test_add_universal_device_template_builds_message(self, ucm):
        ucm.add_universal_device_template(
            name="TestUDT",
            commonPhoneProfile="Standard Common Phone Profile",
            blfPresenceGroup="Standard Presence group",
            location="Hub_None",
        )
        op, body = sent(ucm)
        assert op == "addUniversalDeviceTemplate"
        assert text(body, "universalDeviceTemplate/name") == "TestUDT"
        assert text(body, "universalDeviceTemplate/location") == "Hub_None"

    def test_get_universal_device_template_unwraps(self, ucm):
        ucm.recorder.responses["getUniversalDeviceTemplate"] = {
            "return": {"universalDeviceTemplate": {"name": "TestUDT", "location": "Hub_None"}}
        }
        result = ucm.get_universal_device_template(name="TestUDT")
        assert result["name"] == "TestUDT"

    def test_get_universal_device_templates_empty_list(self, ucm):
        ucm.recorder.responses["listUniversalDeviceTemplate"] = {"return": None}
        assert ucm.get_universal_device_templates() == []

    def test_delete_universal_device_template(self, ucm):
        ucm.delete_universal_device_template(name="TestUDT")
        op, body = sent(ucm)
        assert op == "removeUniversalDeviceTemplate"
        assert text(body, "name") == "TestUDT"

    def test_update_universal_device_template(self, ucm):
        ucm.update_universal_device_template(name="TestUDT", location="Branch")
        op, body = sent(ucm)
        assert op == "updateUniversalDeviceTemplate"
        assert text(body, "name") == "TestUDT"


# ------------------------------------------------------------------ #
# UniversalLineTemplate                                               #
# ------------------------------------------------------------------ #

class TestUniversalLineTemplate:
    def test_add_universal_line_template_builds_message(self, ucm):
        ucm.add_universal_line_template(
            name="TestULT",
            blfPresenceGroup="Standard Presence group",
        )
        op, body = sent(ucm)
        assert op == "addUniversalLineTemplate"
        assert text(body, "universalLineTemplate/name") == "TestULT"

    def test_get_universal_line_template_unwraps(self, ucm):
        ucm.recorder.responses["getUniversalLineTemplate"] = {
            "return": {"universalLineTemplate": {"name": "TestULT"}}
        }
        result = ucm.get_universal_line_template(name="TestULT")
        assert result["name"] == "TestULT"

    def test_get_universal_line_templates_empty_list(self, ucm):
        ucm.recorder.responses["listUniversalLineTemplate"] = {"return": None}
        assert ucm.get_universal_line_templates() == []

    def test_delete_universal_line_template(self, ucm):
        ucm.delete_universal_line_template(name="TestULT")
        op, body = sent(ucm)
        assert op == "removeUniversalLineTemplate"
        assert text(body, "name") == "TestULT"

    def test_update_universal_line_template(self, ucm):
        ucm.update_universal_line_template(name="TestULT", blfPresenceGroup="New Group")
        op, body = sent(ucm)
        assert op == "updateUniversalLineTemplate"
        assert text(body, "name") == "TestULT"
