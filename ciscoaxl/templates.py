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
        

        Schema: `ListCommonDeviceConfigReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        return self.client.listCommonDeviceConfig(
            {"name": "%"}, returnedTags=tagfilter
        )["return"]["commonDeviceConfig"]

    def get_common_device_config(self, **args):
        """
        Get a Common Device Config
        :param name: config name (or uuid)
        :return: commonDeviceConfig dict
        

        Schema: `GetCommonDeviceConfigReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getCommonDeviceConfig(**args)["return"]["commonDeviceConfig"]

    def add_common_device_config(self, **args):
        """
        Add a Common Device Config
        :param name: config name (required)
        :return: result dict
        

        Schema: `commonDeviceConfig` -> `XCommonDeviceConfig`: `name`; optional `softkeyTemplateName`, `userLocale`, `networkHoldMohAudioSourceId`, `userHoldMohAudioSourceId`, `mlppDomainId`, `mlppIndicationStatus` and 10 more.
        """
        return self.client.addCommonDeviceConfig(
            self._build_object("addCommonDeviceConfig", "commonDeviceConfig", args)
        )

    def update_common_device_config(self, **args):
        """
        Update a Common Device Config
        :param name: config name (or uuid)
        :return: result dict
        

        Schema: `UpdateCommonDeviceConfigReq`: optional `newName`, `softkeyTemplateName`, `userLocale`, `networkHoldMohAudioSourceId`, `userHoldMohAudioSourceId`, `mlppDomainId` and 11 more.
        """
        return self.client.updateCommonDeviceConfig(**args)

    def delete_common_device_config(self, name="", uuid=""):
        """
        Delete a Common Device Config
        :param name: config name (or use uuid)
        :param uuid: config uuid (or use name)
        :return: result dict
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeCommonDeviceConfig(**self._identify(name=name, uuid=uuid))

    def apply_common_device_config(self, name="", uuid=""):
        """
        Apply a Common Device Config
        :param name: config name (or use uuid)
        :param uuid: config uuid (or use name)
        :return: result dict
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.applyCommonDeviceConfig(**self._identify(name=name, uuid=uuid))

    def reset_common_device_config(self, name="", uuid=""):
        """
        Reset a Common Device Config
        :param name: config name (or use uuid)
        :param uuid: config uuid (or use name)
        :return: result dict
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
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
        

        Schema: `ListCommonPhoneConfigReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        return self.client.listCommonPhoneConfig(
            {"name": "%"}, returnedTags=tagfilter
        )["return"]["commonPhoneConfig"]

    def get_common_phone_config(self, **args):
        """
        Get a Common Phone Config
        :param name: config name (or uuid)
        :return: commonPhoneConfig dict
        

        Schema: `GetCommonPhoneConfigReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getCommonPhoneConfig(**args)["return"]["commonPhoneConfig"]

    def add_common_phone_config(self, **args):
        """
        Add a Common Phone Config
        :param name: config name (required)
        :return: result dict
        

        Schema: `commonPhoneConfig` -> `XCommonPhoneConfig`: `name`; optional `description`, `unlockPwd`, `dndOption`, `dndAlertingType`, `backgroundImage`, `phonePersonalization` and 10 more.
        """
        return self.client.addCommonPhoneConfig(
            self._build_object("addCommonPhoneConfig", "commonPhoneConfig", args)
        )

    def update_common_phone_config(self, **args):
        """
        Update a Common Phone Config
        :param name: config name (or uuid)
        :return: result dict
        

        Schema: `UpdateCommonPhoneConfigReq`: optional `newName`, `description`, `unlockPwd`, `dndOption`, `dndAlertingType`, `backgroundImage` and 11 more.
        """
        return self.client.updateCommonPhoneConfig(**args)

    def delete_common_phone_config(self, name="", uuid=""):
        """
        Delete a Common Phone Config
        :param name: config name (or use uuid)
        :param uuid: config uuid (or use name)
        :return: result dict
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeCommonPhoneConfig(**self._identify(name=name, uuid=uuid))

    def apply_common_phone_config(self, name="", uuid=""):
        """
        Apply a Common Phone Config
        :param name: config name (or use uuid)
        :param uuid: config uuid (or use name)
        :return: result dict
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.applyCommonPhoneConfig(**self._identify(name=name, uuid=uuid))

    def reset_common_phone_config(self, name="", uuid=""):
        """
        Reset a Common Phone Config
        :param name: config name (or use uuid)
        :param uuid: config uuid (or use name)
        :return: result dict
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
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
        

        Schema: `ListPhoneButtonTemplateReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        return self.client.listPhoneButtonTemplate(
            {"name": "%"}, returnedTags=tagfilter
        )["return"]["phoneButtonTemplate"]

    def get_phone_button_template(self, **args):
        """
        Get a Phone Button Template
        :param name: template name (or uuid)
        :return: phoneButtonTemplate dict
        

        Schema: `GetPhoneButtonTemplateReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getPhoneButtonTemplate(**args)["return"]["phoneButtonTemplate"]

    def add_phone_button_template(self, **args):
        """
        Add a Phone Button Template
        :param name: template name (required)
        :return: result dict
        

        Schema: `phoneButtonTemplate` -> `XPhoneButtonTemplate`: `name` + `basePhoneTemplateName`; optional `buttons`.
        """
        return self.client.addPhoneButtonTemplate(
            self._build_object("addPhoneButtonTemplate", "phoneButtonTemplate", args)
        )

    def update_phone_button_template(self, **args):
        """
        Update a Phone Button Template
        :param name: template name (or uuid)
        :return: result dict
        

        Schema: `UpdatePhoneButtonTemplateReq`: optional `newName`, `buttons`.
        """
        return self.client.updatePhoneButtonTemplate(**args)

    def delete_phone_button_template(self, name="", uuid=""):
        """
        Delete a Phone Button Template
        :param name: template name (or use uuid)
        :param uuid: template uuid (or use name)
        :return: result dict
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removePhoneButtonTemplate(**self._identify(name=name, uuid=uuid))

    def apply_phone_button_template(self, name="", uuid=""):
        """
        Apply a Phone Button Template
        :param name: template name (or use uuid)
        :param uuid: template uuid (or use name)
        :return: result dict
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.applyPhoneButtonTemplate(**self._identify(name=name, uuid=uuid))

    def restart_phone_button_template(self, name="", uuid=""):
        """
        Restart phones using a Phone Button Template
        :param name: template name (or use uuid)
        :param uuid: template uuid (or use name)
        :return: result dict
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
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
        

        Schema: `ListSoftKeyTemplateReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        return self.client.listSoftKeyTemplate(
            {"name": "%"}, returnedTags=tagfilter
        )["return"]["softKeyTemplate"]

    def get_soft_key_template(self, **args):
        """
        Get a Soft Key Template
        :param name: template name (or uuid)
        :return: softKeyTemplate dict
        

        Schema: `GetSoftKeyTemplateReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getSoftKeyTemplate(**args)["return"]["softKeyTemplate"]

    def add_soft_key_template(self, **args):
        """
        Add a Soft Key Template
        :param name: template name (required)
        :return: result dict
        

        Schema: `softKeyTemplate` -> `XSoftKeyTemplate`: `name` + `description` + `baseSoftkeyTemplateName`; optional `isDefault`.
        """
        return self.client.addSoftKeyTemplate(
            self._build_object("addSoftKeyTemplate", "softKeyTemplate", args)
        )

    def update_soft_key_template(self, **args):
        """
        Update a Soft Key Template
        :param name: template name (or uuid)
        :return: result dict
        

        Schema: `UpdateSoftKeyTemplateReq`: optional `newName`, `description`, `isDefault`.
        """
        return self.client.updateSoftKeyTemplate(**args)

    def delete_soft_key_template(self, name="", uuid=""):
        """
        Delete a Soft Key Template
        :param name: template name (or use uuid)
        :param uuid: template uuid (or use name)
        :return: result dict
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeSoftKeyTemplate(**self._identify(name=name, uuid=uuid))

    def apply_soft_key_template(self, name="", uuid=""):
        """
        Apply a Soft Key Template
        :param name: template name (or use uuid)
        :param uuid: template uuid (or use name)
        :return: result dict
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.applySoftKeyTemplate(**self._identify(name=name, uuid=uuid))

    def restart_soft_key_template(self, name="", uuid=""):
        """
        Restart phones using a Soft Key Template
        :param name: template name (or use uuid)
        :param uuid: template uuid (or use name)
        :return: result dict
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
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
        

        Schema: `ListUniversalDeviceTemplateReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        return self.client.listUniversalDeviceTemplate(
            {"name": "%"}, returnedTags=tagfilter
        )["return"]["universalDeviceTemplate"]

    def get_universal_device_template(self, **args):
        """
        Get a Universal Device Template
        :param name: template name (or uuid)
        :return: universalDeviceTemplate dict
        

        Schema: `GetUniversalDeviceTemplateReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getUniversalDeviceTemplate(**args)["return"]["universalDeviceTemplate"]

    def add_universal_device_template(self, **args):
        """
        Add a Universal Device Template
        :param name: template name (required)
        :return: result dict
        

        Schema: `universalDeviceTemplate` -> `XUniversalDeviceTemplate`: `name` + `devicePool` + `deviceSecurityProfile` + `sipProfile` + `phoneButtonTemplate` + `commonPhoneProfile` + `phonePersonalization` + `mtpPreferredOriginatingCodec` + `outboundCallRollover` + `useTrustedRelayPoint` + `certificateOperation` + `authenticationMode` + `keySize` + `servicesProvisioning` + `packetCaptureMode` + `mlppIndication` + `mlppPreemption` + `dndOption` + `blfPresenceGroup` + `blfAudibleAlertSettingPhoneBusy` + `blfAudibleAlertSettingPhoneIdle` + `location` + `deviceMobilityMode` + `joinAcrossLines` + `alwaysUsePrimeLine` + `alwaysUsePrimeLineForVoiceMessage` + `singleButtonBarge` + `builtInBridge` + `privacy`; optional `deviceDescription`, `sipDialRules`, `callingSearchSpace`, `callingPartyTransformationCSSForInboundCalls`, `callingPartyTransformationCSSForOutboundCalls`, `reroutingCallingSearchSpace` and 58 more.
        """
        return self.client.addUniversalDeviceTemplate(
            self._build_object("addUniversalDeviceTemplate", "universalDeviceTemplate", args)
        )

    def update_universal_device_template(self, **args):
        """
        Update a Universal Device Template
        :param name: template name (or uuid)
        :return: result dict
        

        Schema: `UpdateUniversalDeviceTemplateReq`: optional `newName`, `deviceDescription`, `devicePool`, `deviceSecurityProfile`, `sipProfile`, `phoneButtonTemplate` and 87 more.
        """
        return self.client.updateUniversalDeviceTemplate(**args)

    def delete_universal_device_template(self, name="", uuid=""):
        """
        Delete a Universal Device Template
        :param name: template name (or use uuid)
        :param uuid: template uuid (or use name)
        :return: result dict
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
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
        

        Schema: `ListUniversalLineTemplateReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        return self.client.listUniversalLineTemplate(
            {"name": "%"}, returnedTags=tagfilter
        )["return"]["universalLineTemplate"]

    def get_universal_line_template(self, **args):
        """
        Get a Universal Line Template
        :param name: template name (or uuid)
        :return: universalLineTemplate dict
        

        Schema: `GetUniversalLineTemplateReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getUniversalLineTemplate(**args)["return"]["universalLineTemplate"]

    def add_universal_line_template(self, **args):
        """
        Add a Universal Line Template
        :param name: template name (required)
        :return: result dict
        

        Schema: `universalLineTemplate` -> `XUniversalLineTemplate`: `name` + `blfPresenceGroup` + `partyEntranceTone` + `autoAnswer`; optional `urgentPriority`, `lineDescription`, `routePartition`, `voiceMailProfile`, `callingSearchSpace`, `alertingName` and 46 more.
        """
        return self.client.addUniversalLineTemplate(
            self._build_object("addUniversalLineTemplate", "universalLineTemplate", args)
        )

    def update_universal_line_template(self, **args):
        """
        Update a Universal Line Template
        :param name: template name (or uuid)
        :return: result dict
        

        Schema: `UpdateUniversalLineTemplateReq`: optional `newName`, `urgentPriority`, `lineDescription`, `routePartition`, `voiceMailProfile`, `callingSearchSpace` and 50 more.
        """
        return self.client.updateUniversalLineTemplate(**args)

    def delete_universal_line_template(self, name="", uuid=""):
        """
        Delete a Universal Line Template
        :param name: template name (or use uuid)
        :param uuid: template uuid (or use name)
        :return: result dict
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeUniversalLineTemplate(**self._identify(name=name, uuid=uuid))
