"""Device settings and template wrappers (AXL 15.0+).

Mixin class providing AXL wrappers for:
- CommonDeviceConfig
- CommonPhoneConfig
- PhoneButtonTemplate
- SoftKeyTemplate
- UniversalDeviceTemplate
- UniversalLineTemplate
"""


class TemplatesMixin:
    """Device settings and template wrappers (AXL 15.0+)."""

    # ------------------------------------------------------------------ #
    # CommonDeviceConfig                                                   #
    # ------------------------------------------------------------------ #

    def get_common_device_configs(self, tagfilter={"name": ""}):
        """
        List Common Device Configs
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of commonDeviceConfig dicts, empty when nothing matches
        """
        return self.client.listCommonDeviceConfig(
            {"name": "%"}, returnedTags=tagfilter
        )["return"]["commonDeviceConfig"]

    def get_common_device_config(self, **args):
        """
        Get a Common Device Config
        :param name: config name (or uuid)
        :return: commonDeviceConfig dict
        """
        return self.client.getCommonDeviceConfig(**args)["return"]["commonDeviceConfig"]

    def add_common_device_config(self, **args):
        """
        Add a Common Device Config
        :param name: config name (required)
        :return: result dict
        """
        return self.client.addCommonDeviceConfig(
            self._build_object("addCommonDeviceConfig", "commonDeviceConfig", args)
        )

    def update_common_device_config(self, **args):
        """
        Update a Common Device Config
        :param name: config name (or uuid)
        :return: result dict
        """
        return self.client.updateCommonDeviceConfig(**args)

    def delete_common_device_config(self, name="", uuid=""):
        """
        Delete a Common Device Config
        :param name: config name (or use uuid)
        :param uuid: config uuid (or use name)
        :return: result dict
        """
        return self.client.removeCommonDeviceConfig(**self._identify(name=name, uuid=uuid))

    def apply_common_device_config(self, name="", uuid=""):
        """
        Apply a Common Device Config
        :param name: config name (or use uuid)
        :param uuid: config uuid (or use name)
        :return: result dict
        """
        return self.client.applyCommonDeviceConfig(**self._identify(name=name, uuid=uuid))

    def reset_common_device_config(self, name="", uuid=""):
        """
        Reset a Common Device Config
        :param name: config name (or use uuid)
        :param uuid: config uuid (or use name)
        :return: result dict
        """
        return self.client.resetCommonDeviceConfig(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------ #
    # CommonPhoneConfig                                                    #
    # ------------------------------------------------------------------ #

    def get_common_phone_configs(self, tagfilter={"name": ""}):
        """
        List Common Phone Configs
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of commonPhoneConfig dicts, empty when nothing matches
        """
        return self.client.listCommonPhoneConfig(
            {"name": "%"}, returnedTags=tagfilter
        )["return"]["commonPhoneConfig"]

    def get_common_phone_config(self, **args):
        """
        Get a Common Phone Config
        :param name: config name (or uuid)
        :return: commonPhoneConfig dict
        """
        return self.client.getCommonPhoneConfig(**args)["return"]["commonPhoneConfig"]

    def add_common_phone_config(self, **args):
        """
        Add a Common Phone Config
        :param name: config name (required)
        :return: result dict
        """
        return self.client.addCommonPhoneConfig(
            self._build_object("addCommonPhoneConfig", "commonPhoneConfig", args)
        )

    def update_common_phone_config(self, **args):
        """
        Update a Common Phone Config
        :param name: config name (or uuid)
        :return: result dict
        """
        return self.client.updateCommonPhoneConfig(**args)

    def delete_common_phone_config(self, name="", uuid=""):
        """
        Delete a Common Phone Config
        :param name: config name (or use uuid)
        :param uuid: config uuid (or use name)
        :return: result dict
        """
        return self.client.removeCommonPhoneConfig(**self._identify(name=name, uuid=uuid))

    def apply_common_phone_config(self, name="", uuid=""):
        """
        Apply a Common Phone Config
        :param name: config name (or use uuid)
        :param uuid: config uuid (or use name)
        :return: result dict
        """
        return self.client.applyCommonPhoneConfig(**self._identify(name=name, uuid=uuid))

    def reset_common_phone_config(self, name="", uuid=""):
        """
        Reset a Common Phone Config
        :param name: config name (or use uuid)
        :param uuid: config uuid (or use name)
        :return: result dict
        """
        return self.client.resetCommonPhoneConfig(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------ #
    # PhoneButtonTemplate                                                  #
    # ------------------------------------------------------------------ #

    def get_phone_button_templates(self, tagfilter={"name": ""}):
        """
        List Phone Button Templates
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of phoneButtonTemplate dicts, empty when nothing matches
        """
        return self.client.listPhoneButtonTemplate(
            {"name": "%"}, returnedTags=tagfilter
        )["return"]["phoneButtonTemplate"]

    def get_phone_button_template(self, **args):
        """
        Get a Phone Button Template
        :param name: template name (or uuid)
        :return: phoneButtonTemplate dict
        """
        return self.client.getPhoneButtonTemplate(**args)["return"]["phoneButtonTemplate"]

    def add_phone_button_template(self, **args):
        """
        Add a Phone Button Template
        :param name: template name (required)
        :return: result dict
        """
        return self.client.addPhoneButtonTemplate(
            self._build_object("addPhoneButtonTemplate", "phoneButtonTemplate", args)
        )

    def update_phone_button_template(self, **args):
        """
        Update a Phone Button Template
        :param name: template name (or uuid)
        :return: result dict
        """
        return self.client.updatePhoneButtonTemplate(**args)

    def delete_phone_button_template(self, name="", uuid=""):
        """
        Delete a Phone Button Template
        :param name: template name (or use uuid)
        :param uuid: template uuid (or use name)
        :return: result dict
        """
        return self.client.removePhoneButtonTemplate(**self._identify(name=name, uuid=uuid))

    def apply_phone_button_template(self, name="", uuid=""):
        """
        Apply a Phone Button Template
        :param name: template name (or use uuid)
        :param uuid: template uuid (or use name)
        :return: result dict
        """
        return self.client.applyPhoneButtonTemplate(**self._identify(name=name, uuid=uuid))

    def restart_phone_button_template(self, name="", uuid=""):
        """
        Restart phones using a Phone Button Template
        :param name: template name (or use uuid)
        :param uuid: template uuid (or use name)
        :return: result dict
        """
        return self.client.restartPhoneButtonTemplate(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------ #
    # SoftKeyTemplate                                                      #
    # ------------------------------------------------------------------ #

    def get_soft_key_templates(self, tagfilter={"name": ""}):
        """
        List Soft Key Templates
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of softKeyTemplate dicts, empty when nothing matches
        """
        return self.client.listSoftKeyTemplate(
            {"name": "%"}, returnedTags=tagfilter
        )["return"]["softKeyTemplate"]

    def get_soft_key_template(self, **args):
        """
        Get a Soft Key Template
        :param name: template name (or uuid)
        :return: softKeyTemplate dict
        """
        return self.client.getSoftKeyTemplate(**args)["return"]["softKeyTemplate"]

    def add_soft_key_template(self, **args):
        """
        Add a Soft Key Template
        :param name: template name (required)
        :return: result dict
        """
        return self.client.addSoftKeyTemplate(
            self._build_object("addSoftKeyTemplate", "softKeyTemplate", args)
        )

    def update_soft_key_template(self, **args):
        """
        Update a Soft Key Template
        :param name: template name (or uuid)
        :return: result dict
        """
        return self.client.updateSoftKeyTemplate(**args)

    def delete_soft_key_template(self, name="", uuid=""):
        """
        Delete a Soft Key Template
        :param name: template name (or use uuid)
        :param uuid: template uuid (or use name)
        :return: result dict
        """
        return self.client.removeSoftKeyTemplate(**self._identify(name=name, uuid=uuid))

    def apply_soft_key_template(self, name="", uuid=""):
        """
        Apply a Soft Key Template
        :param name: template name (or use uuid)
        :param uuid: template uuid (or use name)
        :return: result dict
        """
        return self.client.applySoftKeyTemplate(**self._identify(name=name, uuid=uuid))

    def restart_soft_key_template(self, name="", uuid=""):
        """
        Restart phones using a Soft Key Template
        :param name: template name (or use uuid)
        :param uuid: template uuid (or use name)
        :return: result dict
        """
        return self.client.restartSoftKeyTemplate(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------ #
    # UniversalDeviceTemplate                                             #
    # ------------------------------------------------------------------ #

    def get_universal_device_templates(self, tagfilter={"name": ""}):
        """
        List Universal Device Templates
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of universalDeviceTemplate dicts, empty when nothing matches
        """
        return self.client.listUniversalDeviceTemplate(
            {"name": "%"}, returnedTags=tagfilter
        )["return"]["universalDeviceTemplate"]

    def get_universal_device_template(self, **args):
        """
        Get a Universal Device Template
        :param name: template name (or uuid)
        :return: universalDeviceTemplate dict
        """
        return self.client.getUniversalDeviceTemplate(**args)["return"]["universalDeviceTemplate"]

    def add_universal_device_template(self, **args):
        """
        Add a Universal Device Template
        :param name: template name (required)
        :return: result dict
        """
        return self.client.addUniversalDeviceTemplate(
            self._build_object("addUniversalDeviceTemplate", "universalDeviceTemplate", args)
        )

    def update_universal_device_template(self, **args):
        """
        Update a Universal Device Template
        :param name: template name (or uuid)
        :return: result dict
        """
        return self.client.updateUniversalDeviceTemplate(**args)

    def delete_universal_device_template(self, name="", uuid=""):
        """
        Delete a Universal Device Template
        :param name: template name (or use uuid)
        :param uuid: template uuid (or use name)
        :return: result dict
        """
        return self.client.removeUniversalDeviceTemplate(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------ #
    # UniversalLineTemplate                                               #
    # ------------------------------------------------------------------ #

    def get_universal_line_templates(self, tagfilter={"name": ""}):
        """
        List Universal Line Templates
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of universalLineTemplate dicts, empty when nothing matches
        """
        return self.client.listUniversalLineTemplate(
            {"name": "%"}, returnedTags=tagfilter
        )["return"]["universalLineTemplate"]

    def get_universal_line_template(self, **args):
        """
        Get a Universal Line Template
        :param name: template name (or uuid)
        :return: universalLineTemplate dict
        """
        return self.client.getUniversalLineTemplate(**args)["return"]["universalLineTemplate"]

    def add_universal_line_template(self, **args):
        """
        Add a Universal Line Template
        :param name: template name (required)
        :return: result dict
        """
        return self.client.addUniversalLineTemplate(
            self._build_object("addUniversalLineTemplate", "universalLineTemplate", args)
        )

    def update_universal_line_template(self, **args):
        """
        Update a Universal Line Template
        :param name: template name (or uuid)
        :return: result dict
        """
        return self.client.updateUniversalLineTemplate(**args)

    def delete_universal_line_template(self, name="", uuid=""):
        """
        Delete a Universal Line Template
        :param name: template name (or use uuid)
        :param uuid: template uuid (or use name)
        :return: result dict
        """
        return self.client.removeUniversalLineTemplate(**self._identify(name=name, uuid=uuid))
