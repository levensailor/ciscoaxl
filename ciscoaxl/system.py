"""System, device defaults, LDAP, licensing, NTP, syslog, and application server wrappers.

Adds device settings, LDAP, system/node, security/licensing, and voicemail methods.

Included groups:
  Device settings:
    - DefaultDeviceProfile   : add, get, list, update, remove
    - DeviceDefaults         : get, list, update
    - EnterprisePhoneConfig  : get, update
    - FeatureControlPolicy   : add, get, list, update, remove
    - FeatureGroupTemplate   : add, get, list, update, remove
    - IpPhoneServices        : add, get, list, update, remove
    - SoftKeySet             : get, update

  LDAP:
    - LdapAuthentication     : get, update
    - LdapFilter             : add, get, list, update, remove
    - LdapSearch             : get, list, update
    - LdapSyncCustomField    : add, get, list, update, remove
    - LdapSystem             : get, update

  System:
    - CallManager            : get, list, update, apply, reset, restart
    - ConfigEnterpriseParameters : apply
    - EnterpriseParameters   : reset, restart
    - OSVersion              : get
    - ProcessNode            : add, get, update, remove
      (listProcessNode already in axl.py as list_process_nodes — not duplicated)
    - ProcessNodeService     : get, list, update
    - ServiceParameter       : get, list, update

  Security/licensing/VM:
    - CredentialPolicy       : add, get, list, update, remove
    - CredentialPolicyDefault: get, update
    - LicensedUser           : get, list
    - SmartLicenseStatus     : get
    - MessageWaiting         : add, get, list, update, remove
    - VoiceMailPort          : add, get, list, update, remove, apply, reset, restart

Adds application, change, NTP, syslog, authentication, and self-provisioning helpers.

Included groups:
  Application / Softkey:
    - ApplicationToSoftkeyTemplate  : add, remove
    - ApplicationServer             : add, get, list, update, remove
    - AppServerInfo                 : add, get, update, remove

  Options / Counts (read-only):
    - DeviceProfileOptions          : get
    - LineOptions                   : get
    - PhoneOptions                  : get
    - NumDevices                    : get

  Change notification:
    - Change                        : list_changes (listChange)

  Reset operations:
    - EnterpriseParametersReset     : do (doEnterpriseParametersReset)
    - ServiceParametersReset        : do (doServiceParametersReset)

  NTP / Syslog:
    - PhoneNtp                      : add, get, list, update, remove
    - SyslogConfiguration           : get, update

  SQL:
    - SQLQueryInactive              : sql_query_inactive (executeSQLQueryInactive)

  Users:
    - AuthenticateUser              : do (doAuthenticateUser)
    - CustomUserField               : add, get, list, update, remove

  Self-provisioning:
    - SelfProvisioning              : update
"""


class SystemMixin:
    """System, device defaults, LDAP, licensing, NTP, syslog, and application server wrappers."""

    # ------------------------------------------------------------------ #
    # DefaultDeviceProfile                                                 #
    # ------------------------------------------------------------------ #

    def add_default_device_profile(self, **args):
        """
        Add a default device profile.
        :param name: profile name — required
        :param description: description
        :param userHoldMohAudioSourceId: MOH source id
        :return: result dictionary (uuid)
        

        Schema: `defaultDeviceProfile` -> `XDefaultDeviceProfile`: `name` + `product` + `class` + `protocol` + `protocolSide` + `phoneButtonTemplate` + `softkeyTemplate` + `privacy` + `mlppIndication` + `preemption`; optional `description`, `userHoldMohAudioSourceId`, `userLocale`, `singleButtonBarge`, `joinAcrossLines`, `ignorePi` and 7 more.
        """
        profile = self._build_object(
            "addDefaultDeviceProfile",
            "defaultDeviceProfile",
            args,
        )
        return self.client.addDefaultDeviceProfile(defaultDeviceProfile=profile)

    def get_default_device_profile(self, name="", uuid=""):
        """
        Get a default device profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: defaultDeviceProfile dictionary
        

        Schema: `GetDefaultDeviceProfileReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getDefaultDeviceProfile(
            **self._identify(name=name, uuid=uuid)
        )["return"]["defaultDeviceProfile"]

    def get_default_device_profiles(self, tagfilter={"name": "", "description": ""}):
        """
        List default device profiles.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of defaultDeviceProfile dictionaries, empty when nothing matches
        

        Schema: `ListDefaultDeviceProfileReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listDefaultDeviceProfile(
            {"name": "%"}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("defaultDeviceProfile") or []

    def update_default_device_profile(self, **args):
        """
        Update a default device profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :param newName: new profile name
        :return: result dictionary
        

        Schema: `UpdateDefaultDeviceProfileReq`: optional `description`, `userHoldMohAudioSourceId`, `userLocale`, `phoneButtonTemplate`, `softkeyTemplate`, `privacy` and 12 more.
        """
        return self.client.updateDefaultDeviceProfile(**args)

    def remove_default_device_profile(self, name="", uuid=""):
        """
        Remove a default device profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeDefaultDeviceProfile(
            **self._identify(name=name, uuid=uuid)
        )

    # ------------------------------------------------------------------ #
    # DeviceDefaults                                                       #
    # ------------------------------------------------------------------ #

    def get_device_defaults(self, Model="", Protocol="", uuid=""):
        """
        Get device defaults for a specific device type.
        :param Model: device model name (required unless uuid provided)
        :param Protocol: device protocol e.g. 'SCCP', 'SIP' (required unless uuid provided)
        :param uuid: device defaults uuid (alternative to Model+Protocol)
        :return: deviceDefaults dictionary
        

        Schema: `GetDeviceDefaultsReq`: optional `returnedTags`; one of `uuid`, or (`Model` + `Protocol`).
        """
        if uuid:
            kwargs = {"uuid": uuid}
        elif Model and Protocol:
            kwargs = {"Model": Model, "Protocol": Protocol}
        else:
            raise ValueError("Provide either uuid or both Model and Protocol")
        return self.client.getDeviceDefaults(**kwargs)["return"]["deviceDefaults"]

    def get_device_defaults_list(self, tagfilter={"Model": "", "Protocol": ""}):
        """
        List device defaults.
        :param tagfilter: AXL returned tags to include, e.g. {'Model': '', 'Protocol': ''}
        :return: list of deviceDefaults dictionaries, empty when nothing matches
        

        Schema: `ListDeviceDefaultsReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listDeviceDefaults(
            {"Model": "%"}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("deviceDefaults") or []

    def update_device_defaults(self, **args):
        """
        Update device defaults.
        :param Model: device model name (or uuid)
        :param Protocol: device protocol (or uuid)
        :param uuid: device defaults uuid (alternative to Model+Protocol)
        :return: result dictionary
        

        Schema: `UpdateDeviceDefaultsReq`: optional `LoadInformation`, `InactiveLoadInformation`, `DevicePoolName`, `PhoneButtonTemplate`, `VersionStamp`, `PreferActCodeOverAutoReg`; one of `uuid`, or (`Model` + `Protocol`).
        """
        return self.client.updateDeviceDefaults(**args)

    # ------------------------------------------------------------------ #
    # EnterprisePhoneConfig                                                #
    # ------------------------------------------------------------------ #

    def get_enterprise_phone_config(self):
        """
        Get the enterprise phone configuration.
        :return: enterprisePhoneConfig dictionary
        """
        return self.client.getEnterprisePhoneConfig()["return"]["enterprisePhoneConfig"]

    def update_enterprise_phone_config(self, **args):
        """
        Update the enterprise phone configuration.
        :return: result dictionary
        

        Schema: `UpdateEnterprisePhoneConfigReq`: optional `vendorConfig`.
        """
        return self.client.updateEnterprisePhoneConfig(**args)

    # ------------------------------------------------------------------ #
    # FeatureControlPolicy                                                 #
    # ------------------------------------------------------------------ #

    def add_feature_control_policy(self, **args):
        """
        Add a feature control policy.
        :param name: policy name — required
        :param description: description
        :return: result dictionary (uuid)
        

        Schema: `featureControlPolicy` -> `XFeatureControlPolicy`: `name`; optional `description`, `features`.
        """
        policy = self._build_object(
            "addFeatureControlPolicy",
            "featureControlPolicy",
            args,
        )
        return self.client.addFeatureControlPolicy(featureControlPolicy=policy)

    def get_feature_control_policy(self, name="", uuid=""):
        """
        Get a feature control policy.
        :param name: policy name (or uuid)
        :param uuid: policy uuid (or name)
        :return: featureControlPolicy dictionary
        

        Schema: `GetFeatureControlPolicyReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getFeatureControlPolicy(
            **self._identify(name=name, uuid=uuid)
        )["return"]["featureControlPolicy"]

    def get_feature_control_policies(self, tagfilter={"name": "", "description": ""}):
        """
        List feature control policies.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of featureControlPolicy dictionaries, empty when nothing matches
        

        Schema: `ListFeatureControlPolicyReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listFeatureControlPolicy(
            {"name": "%"}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("featureControlPolicy") or []

    def update_feature_control_policy(self, **args):
        """
        Update a feature control policy.
        :param name: policy name (or uuid)
        :param uuid: policy uuid (or name)
        :param newName: new policy name
        :return: result dictionary
        

        Schema: `UpdateFeatureControlPolicyReq`: optional `newName`, `description`, `features`.
        """
        return self.client.updateFeatureControlPolicy(**args)

    def remove_feature_control_policy(self, name="", uuid=""):
        """
        Remove a feature control policy.
        :param name: policy name (or uuid)
        :param uuid: policy uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeFeatureControlPolicy(
            **self._identify(name=name, uuid=uuid)
        )

    # ------------------------------------------------------------------ #
    # FeatureGroupTemplate                                                 #
    # ------------------------------------------------------------------ #

    def add_feature_group_template(self, **args):
        """
        Add a feature group template.
        :param name: template name — required
        :param description: description
        :return: result dictionary (uuid)
        

        Schema: `featureGroupTemplate` -> `XFeatureGroupTemplate`: `name` + `maxDeskPickupWait` + `remoteDestinationLimit` + `BLFPresenceGp`; optional `description`, `homeCluster`, `imAndUcPresenceEnable`, `serviceProfile`, `enableUserToHostConferenceNow`, `allowCTIControl` and 7 more.
        """
        template = self._build_object(
            "addFeatureGroupTemplate",
            "featureGroupTemplate",
            args,
        )
        return self.client.addFeatureGroupTemplate(featureGroupTemplate=template)

    def get_feature_group_template(self, name="", uuid=""):
        """
        Get a feature group template.
        :param name: template name (or uuid)
        :param uuid: template uuid (or name)
        :return: featureGroupTemplate dictionary
        

        Schema: `GetFeatureGroupTemplateReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getFeatureGroupTemplate(
            **self._identify(name=name, uuid=uuid)
        )["return"]["featureGroupTemplate"]

    def get_feature_group_templates(self, tagfilter={"name": "", "description": ""}):
        """
        List feature group templates.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of featureGroupTemplate dictionaries, empty when nothing matches
        

        Schema: `ListFeatureGroupTemplateReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listFeatureGroupTemplate(
            {"name": "%"}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("featureGroupTemplate") or []

    def update_feature_group_template(self, **args):
        """
        Update a feature group template.
        :param name: template name (or uuid)
        :param uuid: template uuid (or name)
        :param newName: new template name
        :return: result dictionary
        

        Schema: `UpdateFeatureGroupTemplateReq`: optional `newName`, `description`, `homeCluster`, `imAndUcPresenceEnable`, `serviceProfile`, `enableUserToHostConferenceNow` and 11 more.
        """
        return self.client.updateFeatureGroupTemplate(**args)

    def remove_feature_group_template(self, name="", uuid=""):
        """
        Remove a feature group template.
        :param name: template name (or uuid)
        :param uuid: template uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeFeatureGroupTemplate(
            **self._identify(name=name, uuid=uuid)
        )

    # ------------------------------------------------------------------ #
    # IpPhoneServices                                                      #
    # ------------------------------------------------------------------ #

    def add_ip_phone_service(self, **args):
        """
        Add an IP phone service.
        :param serviceName: service name — required
        :param serviceDescription: description
        :param serviceUrl: service URL
        :param serviceCategory: service category
        :param serviceType: service type
        :param serviceVendor: vendor name
        :param serviceVersion: version
        :return: result dictionary (uuid)
        

        Schema: `ipPhoneServices` -> `XIpPhoneServices`: `serviceName` + `asciiServiceName` + `serviceUrl` + `serviceCategory` + `serviceType`; optional `serviceDescription`, `secureServiceUrl`, `serviceVendor`, `serviceVersion`, `enabled`, `enterpriseSubscription` and 1 more.
        """
        service = self._build_object(
            "addIpPhoneServices",
            "ipPhoneServices",
            args,
        )
        return self.client.addIpPhoneServices(ipPhoneServices=service)

    def get_ip_phone_service(self, serviceName="", uuid=""):
        """
        Get an IP phone service.
        :param serviceName: service name (or uuid)
        :param uuid: service uuid (or serviceName)
        :return: ipPhoneServices dictionary
        

        Schema: `GetIpPhoneServicesReq`: optional `returnedTags`; one of `serviceName`, or `uuid`.
        """
        if bool(serviceName) == bool(uuid):
            raise ValueError("Provide exactly one of serviceName or uuid")
        identifier = {"serviceName": serviceName} if serviceName else {"uuid": uuid}
        return self.client.getIpPhoneServices(**identifier)["return"]["ipPhoneServices"]

    def get_ip_phone_services(self, tagfilter={"serviceName": "", "serviceDescription": ""}):
        """
        List IP phone services.
        :param tagfilter: AXL returned tags to include, e.g. {'serviceName': ''}
        :return: list of ipPhoneServices dictionaries, empty when nothing matches
        

        Schema: `ListIpPhoneServicesReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listIpPhoneServices(
            {"serviceName": "%"}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("ipPhoneServices") or []

    def update_ip_phone_service(self, **args):
        """
        Update an IP phone service.
        :param serviceName: service name (or uuid)
        :param uuid: service uuid (or serviceName)
        :param newServiceName: new service name
        :return: result dictionary
        

        Schema: `UpdateIpPhoneServicesReq`: optional `newServiceName`, `asciiServiceName`, `serviceDescription`, `serviceUrl`, `secureServiceUrl`, `serviceCategory` and 5 more; one of `uuid`, or `serviceName`.
        """
        return self.client.updateIpPhoneServices(**args)

    def remove_ip_phone_service(self, serviceName="", uuid=""):
        """
        Remove an IP phone service.
        :param serviceName: service name (or uuid)
        :param uuid: service uuid (or serviceName)
        :return: result dictionary
        

        Schema: `RemoveIpPhoneServicesReq`: one of `serviceName`, or `uuid`.
        """
        if bool(serviceName) == bool(uuid):
            raise ValueError("Provide exactly one of serviceName or uuid")
        identifier = {"serviceName": serviceName} if serviceName else {"uuid": uuid}
        return self.client.removeIpPhoneServices(**identifier)

    # ------------------------------------------------------------------ #
    # SoftKeySet                                                           #
    # ------------------------------------------------------------------ #

    def get_soft_key_set(self, name="", uuid=""):
        """
        Get a soft key set.
        :param name: soft key set name (or uuid)
        :param uuid: soft key set uuid (or name)
        :return: softKeySet dictionary
        

        Schema: `GetSoftKeySetReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getSoftKeySet(
            **self._identify(name=name, uuid=uuid)
        )["return"]["softKeySet"]

    def update_soft_key_set(self, **args):
        """
        Update a soft key set.
        :param name: soft key set name (or uuid)
        :param uuid: soft key set uuid (or name)
        :return: result dictionary
        

        Schema: `UpdateSoftKeySetReq`: optional optional choice of (optional `removeCallStates`, `addCallStates`), or `callStates`.
        """
        return self.client.updateSoftKeySet(**args)

    # ------------------------------------------------------------------ #
    # LdapAuthentication                                                   #
    # ------------------------------------------------------------------ #

    def get_ldap_authentication(self):
        """
        Get LDAP authentication configuration.
        :return: ldapAuthentication dictionary
        """
        return self.client.getLdapAuthentication()["return"]["ldapAuthentication"]

    def update_ldap_authentication(self, **args):
        """
        Update LDAP authentication configuration.
        :param distinguishedName: bind DN for authentication
        :param ldapPassword: bind password
        :param userSearchBase: user search base DN
        :param port: LDAP port number
        :param servers: LDAP server list
        :return: result dictionary
        

        Schema: `UpdateLdapAuthenticationReq`: optional `authenticateEndUsers`, `distinguishedName`, `ldapPassword`, `userSearchBase`, `servers`.
        """
        return self.client.updateLdapAuthentication(**args)

    # ------------------------------------------------------------------ #
    # LdapFilter                                                           #
    # ------------------------------------------------------------------ #

    def add_ldap_filter(self, **args):
        """
        Add an LDAP filter.
        :param name: filter name — required
        :param filter: LDAP filter string
        :return: result dictionary (uuid)
        

        Schema: `ldapFilter` -> `XLdapFilter`: `name` + `filter`.
        """
        ldap_filter = self._build_object(
            "addLdapFilter",
            "ldapFilter",
            args,
        )
        return self.client.addLdapFilter(ldapFilter=ldap_filter)

    def get_ldap_filter(self, name="", uuid=""):
        """
        Get an LDAP filter.
        :param name: filter name (or uuid)
        :param uuid: filter uuid (or name)
        :return: ldapFilter dictionary
        

        Schema: `GetLdapFilterReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getLdapFilter(
            **self._identify(name=name, uuid=uuid)
        )["return"]["ldapFilter"]

    def get_ldap_filters(self, tagfilter={"name": "", "filter": ""}):
        """
        List LDAP filters.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of ldapFilter dictionaries, empty when nothing matches
        

        Schema: `ListLdapFilterReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listLdapFilter(
            {"name": "%"}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("ldapFilter") or []

    def update_ldap_filter(self, **args):
        """
        Update an LDAP filter.
        :param name: filter name (or uuid)
        :param uuid: filter uuid (or name)
        :param newName: new filter name
        :param filter: new LDAP filter string
        :return: result dictionary
        

        Schema: `UpdateLdapFilterReq`: optional `newName`, `filter`.
        """
        return self.client.updateLdapFilter(**args)

    def remove_ldap_filter(self, name="", uuid=""):
        """
        Remove an LDAP filter.
        :param name: filter name (or uuid)
        :param uuid: filter uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeLdapFilter(
            **self._identify(name=name, uuid=uuid)
        )

    # ------------------------------------------------------------------ #
    # LdapSearch                                                           #
    # ------------------------------------------------------------------ #

    def get_ldap_search(self, uuid=""):
        """
        Get an LDAP search configuration.
        :param uuid: search config uuid — required (LdapSearch has no name field)
        :return: ldapSearch dictionary
        

        Schema: `GetLdapSearchReq`: optional `returnedTags`; one of `uuid`.
        """
        if not uuid:
            raise ValueError("Provide uuid (LdapSearch has no name identifier)")
        return self.client.getLdapSearch(uuid=uuid)["return"]["ldapSearch"]

    def get_ldap_searches(self, tagfilter={"distinguishedName": ""}):
        """
        List LDAP search configurations.
        :param tagfilter: AXL returned tags to include, e.g. {'distinguishedName': ''}
        :return: list of ldapSearch dictionaries, empty when nothing matches
        

        Schema: `ListLdapSearchReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listLdapSearch(
            {"distinguishedName": "%"}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("ldapSearch") or []

    def update_ldap_search(self, **args):
        """
        Update an LDAP search configuration.
        :param uuid: search config uuid — required
        :return: result dictionary
        

        Schema: `UpdateLdapSearchReq`: optional `enableDirectorySearch`, `distinguishedName`, `password`, `userSearchBase1`, `userSearchBase2`, `userSearchBase3` and 6 more; one of `uuid`.
        """
        return self.client.updateLdapSearch(**args)

    # ------------------------------------------------------------------ #
    # LdapSyncCustomField                                                  #
    # ------------------------------------------------------------------ #

    def add_ldap_sync_custom_field(self, **args):
        """
        Add an LDAP sync custom field mapping.
        :param ldapConfigurationName: LDAP directory config name — required
        :param customUserField: CUCM user field
        :param ldapUserField: LDAP attribute name
        :return: result dictionary (uuid)
        

        Schema: `ldapSyncCustomField` -> `XLdapSyncCustomField`: `ldapConfigurationName` + `customUserField` + `ldapUserField`.
        """
        field = self._build_object(
            "addLdapSyncCustomField",
            "ldapSyncCustomField",
            args,
        )
        return self.client.addLdapSyncCustomField(ldapSyncCustomField=field)

    def get_ldap_sync_custom_field(self, ldapConfigurationName="", customUserField="", uuid=""):
        """
        Get an LDAP sync custom field mapping.
        :param ldapConfigurationName: LDAP directory config name (required unless uuid provided)
        :param customUserField: CUCM user field (required unless uuid provided)
        :param uuid: custom field uuid (alternative to ldapConfigurationName+customUserField)
        :return: ldapSyncCustomField dictionary
        

        Schema: `GetLdapSyncCustomFieldReq`: optional `returnedTags`; one of `uuid`, or (`ldapConfigurationName` + `customUserField`).
        """
        if uuid:
            kwargs = {"uuid": uuid}
        elif ldapConfigurationName and customUserField:
            kwargs = {"ldapConfigurationName": ldapConfigurationName, "customUserField": customUserField}
        else:
            raise ValueError(
                "Provide either uuid or both ldapConfigurationName and customUserField"
            )
        return self.client.getLdapSyncCustomField(**kwargs)["return"]["ldapSyncCustomField"]

    def get_ldap_sync_custom_fields(self, tagfilter={"ldapUserField": ""}):
        """
        List LDAP sync custom field mappings.
        :param tagfilter: AXL returned tags to include
        :return: list of ldapSyncCustomField dictionaries, empty when nothing matches
        

        Schema: `ListLdapSyncCustomFieldReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listLdapSyncCustomField(
            {"ldapConfigurationName": "%"}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("ldapSyncCustomField") or []

    def update_ldap_sync_custom_field(self, **args):
        """
        Update an LDAP sync custom field mapping.
        :param ldapConfigurationName: LDAP directory config name — required
        :param customUserField: CUCM user field — required
        :param ldapUserField: new LDAP attribute to map
        :return: result dictionary
        

        Schema: `UpdateLdapSyncCustomFieldReq`: optional `ldapUserField`; one of `uuid`, or (`ldapConfigurationName` + `customUserField`).
        """
        return self.client.updateLdapSyncCustomField(**args)

    def remove_ldap_sync_custom_field(self, ldapConfigurationName="", customUserField="", uuid=""):
        """
        Remove an LDAP sync custom field mapping.
        :param ldapConfigurationName: LDAP directory config name (required unless uuid provided)
        :param customUserField: CUCM user field (required unless uuid provided)
        :param uuid: custom field uuid (alternative to ldapConfigurationName+customUserField)
        :return: result dictionary
        

        Schema: `RemoveLdapSyncCustomFieldReq`: one of `uuid`, or (`ldapConfigurationName` + `customUserField`).
        """
        if uuid:
            kwargs = {"uuid": uuid}
        elif ldapConfigurationName and customUserField:
            kwargs = {"ldapConfigurationName": ldapConfigurationName, "customUserField": customUserField}
        else:
            raise ValueError(
                "Provide either uuid or both ldapConfigurationName and customUserField"
            )
        return self.client.removeLdapSyncCustomField(**kwargs)

    # ------------------------------------------------------------------ #
    # LdapSystem                                                           #
    # ------------------------------------------------------------------ #

    def get_ldap_system(self):
        """
        Get the LDAP system configuration.
        :return: ldapSystem dictionary
        """
        return self.client.getLdapSystem()["return"]["ldapSystem"]

    def update_ldap_system(self, **args):
        """
        Update the LDAP system configuration.
        :param syncEnabled: boolean, enable LDAP sync
        :param ldapServer: LDAP server vendor
        :param userIdAttribute: LDAP attribute to use as CUCM user ID
        :return: result dictionary
        

        Schema: `UpdateLdapSystemReq`: optional `syncEnabled`, `ldapServer`, `userIdAttribute`.
        """
        return self.client.updateLdapSystem(**args)

    # ------------------------------------------------------------------ #
    # CallManager                                                          #
    # ------------------------------------------------------------------ #

    def get_call_manager(self, name="", uuid=""):
        """
        Get a CallManager node.
        :param name: node name (or uuid)
        :param uuid: node uuid (or name)
        :return: callManager dictionary
        

        Schema: `GetCallManagerReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getCallManager(
            **self._identify(name=name, uuid=uuid)
        )["return"]["callManager"]

    def get_call_managers(self, tagfilter={"name": "", "description": ""}):
        """
        List CallManager nodes.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of callManager dictionaries, empty when nothing matches
        

        Schema: `ListCallManagerReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listCallManager(
            {"name": "%"}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("callManager") or []

    def update_call_manager(self, **args):
        """
        Update a CallManager node.
        :param name: node name (or uuid)
        :param uuid: node uuid (or name)
        :return: result dictionary
        

        Schema: `UpdateCallManagerReq`: optional `newName`, `description`, `autoRegistration`, `ports`, `lbmGroup`.
        """
        return self.client.updateCallManager(**args)

    def apply_call_manager(self, name="", uuid=""):
        """
        Apply CallManager configuration.
        :param name: node name (or uuid)
        :param uuid: node uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.applyCallManager(**self._identify(name=name, uuid=uuid))

    def reset_call_manager(self, name="", uuid=""):
        """
        Reset a CallManager node.
        :param name: node name (or uuid)
        :param uuid: node uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.resetCallManager(**self._identify(name=name, uuid=uuid))

    def restart_call_manager(self, name="", uuid=""):
        """
        Restart a CallManager node.
        :param name: node name (or uuid)
        :param uuid: node uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.restartCallManager(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------ #
    # ConfigEnterpriseParameters                                           #
    # ------------------------------------------------------------------ #

    def apply_config_enterprise_parameters(self):
        """
        Apply enterprise parameters configuration to all nodes.
        :return: result dictionary
        """
        return self.client.applyConfigEnterpriseParameters()

    # ------------------------------------------------------------------ #
    # EnterpriseParameters                                                 #
    # ------------------------------------------------------------------ #

    def reset_enterprise_parameters(self):
        """
        Reset enterprise parameters to defaults.
        :return: result dictionary
        """
        return self.client.resetEnterpriseParameters()

    def restart_enterprise_parameters(self):
        """
        Restart services after enterprise parameter change.
        :return: result dictionary
        """
        return self.client.restartEnterpriseParameters()

    # ------------------------------------------------------------------ #
    # OSVersion                                                            #
    # ------------------------------------------------------------------ #

    def get_os_version(self):
        """
        Get the OS version of the connected node.
        :return: os dictionary (osName, osVersion)
        """
        return self.client.getOSVersion()["return"]["os"]

    # ------------------------------------------------------------------ #
    # ProcessNode                                                          #
    # (listProcessNode already in axl.py as list_process_nodes — not dup) #
    # ------------------------------------------------------------------ #

    def add_process_node(self, **args):
        """
        Add a process node.
        :param name: node hostname or IP — required
        :param description: description
        :param mac: MAC address
        :param ipv6Name: IPv6 address
        :param nodeUsage: node usage type
        :param lbmHubGroup: LBM hub group
        :return: result dictionary (uuid)
        

        Schema: `processNode` -> `XProcessNode`: `name` + `processNodeRole`; optional `description`, `mac`, `ipv6Name`, `lbmHubGroup`, `cupDomain`.
        """
        node = self._build_object(
            "addProcessNode",
            "processNode",
            args,
        )
        return self.client.addProcessNode(processNode=node)

    def get_process_node(self, name="", uuid=""):
        """
        Get a process node.
        :param name: node name (or uuid)
        :param uuid: node uuid (or name)
        :return: processNode dictionary
        

        Schema: `GetProcessNodeReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getProcessNode(
            **self._identify(name=name, uuid=uuid)
        )["return"]["processNode"]

    def update_process_node(self, **args):
        """
        Update a process node.
        :param name: node name (or uuid)
        :param uuid: node uuid (or name)
        :param newName: new node name
        :return: result dictionary
        

        Schema: `UpdateProcessNodeReq`: optional `newName`, `description`, `mac`, `ipv6Name`, `lbmHubGroup`, `cupDomain`.
        """
        return self.client.updateProcessNode(**args)

    def remove_process_node(self, name="", uuid=""):
        """
        Remove a process node.
        :param name: node name (or uuid)
        :param uuid: node uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeProcessNode(
            **self._identify(name=name, uuid=uuid)
        )

    # ------------------------------------------------------------------ #
    # ProcessNodeService                                                   #
    # ------------------------------------------------------------------ #

    def get_process_node_service(self, processNodeName, service_name):
        """
        Get a process node service.
        :param processNodeName: node hostname/IP — required
        :param service_name: service name — required (maps to AXL 'service' element)
        :return: processNodeService dictionary
        

        Schema: `GetProcessNodeServiceReq`: optional `returnedTags`; one of `uuid`, or (`processNodeName` + `service`).
        """
        return self.client.getProcessNodeService(
            **{"processNodeName": processNodeName, "service": service_name}
        )["return"]["processNodeService"]

    def get_process_node_services(
        self,
        search_processNodeName="%",
        tagfilter={"processNodeName": "", "service": "", "traceLevel": ""},
    ):
        """
        List process node services.
        :param search_processNodeName: node name search pattern, default '%' (all)
        :param tagfilter: AXL returned tags to include
        :return: list of processNodeService dictionaries, empty when nothing matches
        

        Schema: `ListProcessNodeServiceReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listProcessNodeService(
            {"processNodeName": search_processNodeName}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("processNodeService") or []

    def update_process_node_service(self, processNodeName, service_name, **args):
        """
        Update a process node service.
        :param processNodeName: node hostname/IP — required
        :param service_name: service name — required (maps to AXL 'service' element)
        :param traceLevel: trace level value
        :return: result dictionary
        

        Schema: `UpdateProcessNodeServiceReq`: optional `traceLevel`, `userCategories`, `enable`, `numFiles`, `maxFileSize`; one of `uuid`, or (`processNodeName` + `service`).
        """
        return self.client.updateProcessNodeService(
            **{"processNodeName": processNodeName, "service": service_name, **args}
        )

    # ------------------------------------------------------------------ #
    # ServiceParameter                                                     #
    # ------------------------------------------------------------------ #

    def get_service_parameter(self, processNodeName, service_name, name):
        """
        Get a service parameter value.
        :param processNodeName: node hostname/IP — required
        :param service_name: service name — required (maps to AXL 'service' element)
        :param name: parameter name — required
        :return: serviceParameter dictionary
        

        Schema: `GetServiceParameterReq`: optional `returnedTags`; one of `uuid`, or (`processNodeName` + `name` + `service`).
        """
        return self.client.getServiceParameter(
            **{"processNodeName": processNodeName, "service": service_name, "name": name}
        )["return"]["serviceParameter"]

    def get_service_parameters(
        self,
        search_processNodeName="%",
        search_service="%",
        tagfilter={"processNodeName": "", "service": "", "name": "", "value": ""},
    ):
        """
        List service parameters.
        :param search_processNodeName: node name search pattern, default '%' (all)
        :param search_service: service search pattern, default '%' (all)
        :param tagfilter: AXL returned tags to include
        :return: list of serviceParameter dictionaries, empty when nothing matches
        

        Schema: `ListServiceParameterReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listServiceParameter(
            {"processNodeName": search_processNodeName, "service": search_service},
            returnedTags=tagfilter,
        )["return"]
        if result is None:
            return []
        return result.get("serviceParameter") or []

    def update_service_parameter(self, processNodeName, service_name, name, value=None, **args):
        """
        Update a service parameter value.
        :param processNodeName: node hostname/IP — required
        :param service_name: service name — required (maps to AXL 'service' element)
        :param name: parameter name — required
        :param value: new parameter value
        :return: result dictionary
        

        Schema: `UpdateServiceParameterReq`: optional `value`; one of `uuid`, or (`processNodeName` + `name` + `service`).
        """
        kwargs = {"processNodeName": processNodeName, "service": service_name, "name": name}
        if value is not None:
            kwargs["value"] = value
        kwargs.update(args)
        return self.client.updateServiceParameter(**kwargs)

    # ------------------------------------------------------------------ #
    # CredentialPolicy                                                     #
    # ------------------------------------------------------------------ #

    def add_credential_policy(self, **args):
        """
        Add a credential policy.
        :param name: policy name — required
        :param description: description
        :param failedLogon: failed logon lockout count
        :param resetFailedLogonAttempts: reset failed attempts
        :param lockoutDuration: lockout duration in minutes
        :param credChangeDuration: forced change interval in days
        :param credExpiresAfter: expiry period in days
        :return: result dictionary (uuid)
        

        Schema: `credentialPolicy` -> `XCredentialPolicy`: `name` + `failedLogon` + `resetFailedLogonAttempts` + `lockoutDuration` + `credChangeDuration` + `credExpiresAfter` + `minCredLength` + `prevCredStoredNum` + `inactiveDaysAllowed` + `expiryWarningDays` + `trivialCredCheck` + `minCharsToChange`.
        """
        policy = self._build_object(
            "addCredentialPolicy",
            "credentialPolicy",
            args,
        )
        return self.client.addCredentialPolicy(credentialPolicy=policy)

    def get_credential_policy(self, name="", uuid=""):
        """
        Get a credential policy.
        :param name: policy name (or uuid)
        :param uuid: policy uuid (or name)
        :return: credentialPolicy dictionary
        

        Schema: `GetCredentialPolicyReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getCredentialPolicy(
            **self._identify(name=name, uuid=uuid)
        )["return"]["credentialPolicy"]

    def get_credential_policies(self, tagfilter={"name": ""}):
        """
        List credential policies.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of credentialPolicy dictionaries, empty when nothing matches
        

        Schema: `ListCredentialPolicyReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listCredentialPolicy(
            {"name": "%"}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("credentialPolicy") or []

    def update_credential_policy(self, **args):
        """
        Update a credential policy.
        :param name: policy name (or uuid)
        :param uuid: policy uuid (or name)
        :param newName: new policy name
        :return: result dictionary
        

        Schema: `UpdateCredentialPolicyReq`: optional `newName`, `failedLogon`, `resetFailedLogonAttempts`, `lockoutDuration`, `credChangeDuration`, `credExpiresAfter` and 6 more.
        """
        return self.client.updateCredentialPolicy(**args)

    def remove_credential_policy(self, name="", uuid=""):
        """
        Remove a credential policy.
        :param name: policy name (or uuid)
        :param uuid: policy uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeCredentialPolicy(
            **self._identify(name=name, uuid=uuid)
        )

    # ------------------------------------------------------------------ #
    # CredentialPolicyDefault                                              #
    # ------------------------------------------------------------------ #

    def get_credential_policy_default(self):
        """
        Get the credential policy default configuration.
        :return: credentialPolicyDefault dictionary
        

        Schema: `GetCredentialPolicyDefaultReq`: optional `returnedTags`; one of (`credentialUser` + `credentialType` + `credPolicyName`).
        """
        return self.client.getCredentialPolicyDefault()["return"]["credentialPolicyDefault"]

    def update_credential_policy_default(self, **args):
        """
        Update the credential policy default configuration.
        :param credentialUser: default policy for user pins/passwords
        :param credentialApplicationUser: default policy for application users
        :return: result dictionary
        

        Schema: `UpdateCredentialPolicyDefaultReq`: `credentialUser` + `credentialType` + `credPolicyName`; optional `newCredPolicyName`, `credentials`, `confirmCredentials`, `credUserCantChange`, `credUserMustChange`, `credDoesNotExpire`.
        """
        return self.client.updateCredentialPolicyDefault(**args)

    # ------------------------------------------------------------------ #
    # LicensedUser                                                         #
    # ------------------------------------------------------------------ #

    def get_licensed_user(self, name="", uuid=""):
        """
        Get a licensed user.
        :param name: user ID / name (or uuid)
        :param uuid: user uuid (or name)
        :return: licensedUser dictionary
        

        Schema: `GetLicensedUserReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getLicensedUser(
            **self._identify(name=name, uuid=uuid)
        )["return"]["licensedUser"]

    def get_licensed_users(self, tagfilter={"userId": "", "lastName": ""}):
        """
        List licensed users.
        :param tagfilter: AXL returned tags to include, e.g. {'userId': ''}
        :return: list of licensedUser dictionaries, empty when nothing matches
        

        Schema: `ListLicensedUserReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listLicensedUser(
            {"userId": "%"}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("licensedUser") or []

    # ------------------------------------------------------------------ #
    # SmartLicenseStatus                                                   #
    # ------------------------------------------------------------------ #

    def get_smart_license_status(self):
        """
        Get Smart Licensing details.

        AXL puts the overall status string on ``return``. This method
        returns the sibling ``LicenseDetails`` object. Read ``return`` on
        the raw SOAP response for that status string.
        :return: LicenseDetails dictionary
        """
        return self.client.getSmartLicenseStatus()["LicenseDetails"]

    # ------------------------------------------------------------------ #
    # MessageWaiting                                                       #
    # ------------------------------------------------------------------ #

    def add_message_waiting(self, **args):
        """
        Add a message waiting number.
        :param pattern: DN pattern — required
        :param description: description
        :param routePartitionName: partition name
        :param messageWaitingIndicator: MWI On/Off
        :param callingSearchSpaceName: CSS name
        :return: result dictionary (uuid)
        

        Schema: `messageWaiting` -> `XMessageWaiting`: `pattern` + `routePartitionName` + `messageWaitingIndicator`; optional `description`, `callingSearchSpaceName`.
        """
        mwi = self._build_object(
            "addMessageWaiting",
            "messageWaiting",
            args,
        )
        return self.client.addMessageWaiting(messageWaiting=mwi)

    def get_message_waiting(self, pattern="", uuid=""):
        """
        Get a message waiting number.
        :param pattern: DN pattern (or uuid)
        :param uuid: DN uuid (or pattern)
        :return: messageWaiting dictionary
        

        Schema: `GetMessageWaitingReq`: optional `returnedTags`; one of `uuid`, or (`pattern` + `routePartitionName`).
        """
        if bool(pattern) == bool(uuid):
            raise ValueError("Provide exactly one of pattern or uuid")
        identifier = {"pattern": pattern} if pattern else {"uuid": uuid}
        return self.client.getMessageWaiting(**identifier)["return"]["messageWaiting"]

    def get_message_waitings(self, tagfilter={"pattern": "", "description": ""}):
        """
        List message waiting numbers.
        :param tagfilter: AXL returned tags to include, e.g. {'pattern': ''}
        :return: list of messageWaiting dictionaries, empty when nothing matches
        

        Schema: `ListMessageWaitingReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listMessageWaiting(
            {"pattern": "%"}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("messageWaiting") or []

    def update_message_waiting(self, **args):
        """
        Update a message waiting number.
        :param pattern: DN pattern (or uuid)
        :param uuid: DN uuid (or pattern)
        :param description: description
        :return: result dictionary
        

        Schema: `UpdateMessageWaitingReq`: optional `newPattern`, `newRoutePartitionName`, `description`, `messageWaitingIndicator`, `callingSearchSpaceName`; one of `uuid`, or (`pattern` + `routePartitionName`).
        """
        return self.client.updateMessageWaiting(**args)

    def remove_message_waiting(self, pattern="", uuid=""):
        """
        Remove a message waiting number.
        :param pattern: DN pattern (or uuid)
        :param uuid: DN uuid (or pattern)
        :return: result dictionary
        

        Schema: `RemoveMessageWaitingReq`: one of `uuid`, or (`pattern` + `routePartitionName`).
        """
        if bool(pattern) == bool(uuid):
            raise ValueError("Provide exactly one of pattern or uuid")
        identifier = {"pattern": pattern} if pattern else {"uuid": uuid}
        return self.client.removeMessageWaiting(**identifier)

    # ------------------------------------------------------------------ #
    # VoiceMailPort                                                        #
    # ------------------------------------------------------------------ #

    def add_voice_mail_port(self, **args):
        """
        Add a voice mail port.
        :param name: port name — required
        :param description: description
        :param devicePoolName: device pool name
        :param commonDeviceConfigName: common device config
        :param locationName: location name
        :param voiceMailDn: voicemail directory number
        :return: result dictionary (uuid)
        

        Schema: `voiceMailPort` -> `XVoiceMailPort`: `name` + `product` + `class` + `protocol` + `protocolSide` + `devicePoolName` + `locationName` + `useTrustedRelayPoint` + `securityProfileName` + `dnPattern`; optional `description`, `callingSearchSpaceName`, `commonDeviceConfigName`, `preemption`, `geoLocationName`, `automatedAlternateRoutingCssName` and 6 more.
        """
        port = self._build_object(
            "addVoiceMailPort",
            "voiceMailPort",
            args,
        )
        return self.client.addVoiceMailPort(voiceMailPort=port)

    def get_voice_mail_port(self, name="", uuid=""):
        """
        Get a voice mail port.
        :param name: port name (or uuid)
        :param uuid: port uuid (or name)
        :return: voiceMailPort dictionary
        

        Schema: `GetVoiceMailPortReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getVoiceMailPort(
            **self._identify(name=name, uuid=uuid)
        )["return"]["voiceMailPort"]

    def get_voice_mail_ports(self, tagfilter={"name": "", "description": ""}):
        """
        List voice mail ports.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of voiceMailPort dictionaries, empty when nothing matches
        

        Schema: `ListVoiceMailPortReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listVoiceMailPort(
            {"name": "%"}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("voiceMailPort") or []

    def update_voice_mail_port(self, **args):
        """
        Update a voice mail port.
        :param name: port name (or uuid)
        :param uuid: port uuid (or name)
        :param newName: new port name
        :return: result dictionary
        

        Schema: `UpdateVoiceMailPortReq`: optional `newName`, `description`, `callingSearchSpaceName`, `devicePoolName`, `commonDeviceConfigName`, `locationName` and 11 more.
        """
        return self.client.updateVoiceMailPort(**args)

    def remove_voice_mail_port(self, name="", uuid=""):
        """
        Remove a voice mail port.
        :param name: port name (or uuid)
        :param uuid: port uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeVoiceMailPort(
            **self._identify(name=name, uuid=uuid)
        )

    def apply_voice_mail_port(self, name="", uuid=""):
        """
        Apply voice mail port configuration.
        :param name: port name (or uuid)
        :param uuid: port uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.applyVoiceMailPort(**self._identify(name=name, uuid=uuid))

    def reset_voice_mail_port(self, name="", uuid=""):
        """
        Reset a voice mail port.
        :param name: port name (or uuid)
        :param uuid: port uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.resetVoiceMailPort(**self._identify(name=name, uuid=uuid))

    def restart_voice_mail_port(self, name="", uuid=""):
        """
        Restart a voice mail port.
        :param name: port name (or uuid)
        :param uuid: port uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.restartVoiceMailPort(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------ #
    # ApplicationToSoftkeyTemplate                                         #
    # ------------------------------------------------------------------ #

    def add_application_to_softkey_template(self, **args):
        """
        Associate an application with a softkey template.
        :param softKeyTemplateName: softkey template name — required
        :param standardSoftKeyTemplateName: standard template name reference
        :return: result dictionary (uuid)
        

        Schema: `applicationToSoftkeyTemplate` -> `XApplicationToSoftKeyTemplate`: `softKeyTemplateName` + `standardSoftKeyTemplateName`.
        """
        obj = self._build_object(
            "addApplicationToSoftkeyTemplate",
            "applicationToSoftkeyTemplate",
            args,
        )
        return self.client.addApplicationToSoftkeyTemplate(
            applicationToSoftkeyTemplate=obj
        )

    def remove_application_to_softkey_template(
        self, softKeyTemplateName, applicationName=""
    ):
        """
        Remove an application-to-softkey-template association.
        AXL does not expose a uuid identifier for this operation; use names.
        :param softKeyTemplateName: softkey template name — required
        :param applicationName: application name
        :return: result dictionary
        

        Schema: `removeApplicationToSoftkeyTemplateReq`: `softKeyTemplateName` + `applicationName`.
        """
        return self.client.removeApplicationToSoftkeyTemplate(
            softKeyTemplateName=softKeyTemplateName,
            applicationName=applicationName,
        )

    # ------------------------------------------------------------------ #
    # DeviceProfileOptions (get only — no list in AXL)                    #
    # ------------------------------------------------------------------ #

    def get_device_profile_options(self, uuid):
        """
        Get device-profile option choices for a device profile UUID.
        :param uuid: device profile uuid — required
        :return: deviceProfile dictionary
        

        Schema: `GetDeviceProfileOptionsReq`: optional `returnedChoices`; one of `uuid`.
        """
        return self.client.getDeviceProfileOptions(uuid=uuid)["return"][
            "deviceProfile"
        ]

    # ------------------------------------------------------------------ #
    # LineOptions (get only — no list in AXL)                             #
    # ------------------------------------------------------------------ #

    def get_line_options(self, uuid):
        """
        Get line option choices for a directory-number UUID.
        :param uuid: line (directory number) uuid — required
        :return: line options dictionary
        

        Schema: `GetLineOptionsReq`: optional `returnedChoices`; one of `uuid`.
        """
        return self.client.getLineOptions(uuid=uuid)["return"]["line"]

    # ------------------------------------------------------------------ #
    # NumDevices (get only — no list in AXL)                              #
    # ------------------------------------------------------------------ #

    def get_num_devices(self, device_class):
        """
        Get the number of registered devices of the specified class.
        :param device_class: device class string — required (e.g. 'Phone', 'Gateway')
                             maps to AXL 'class' element (required by schema)
        :return: integer count or result dictionary
        

        Schema: `GetNumDevicesReq`: `class`.
        """
        return self.client.getNumDevices(**{"class": device_class})["return"]

    # ------------------------------------------------------------------ #
    # PhoneOptions (get only — no list in AXL)                            #
    # ------------------------------------------------------------------ #

    def get_phone_options(self, uuid):
        """
        Get phone option choices for a phone UUID.
        :param uuid: phone uuid — required
        :return: phone options dictionary
        

        Schema: `GetPhoneOptionsReq`: optional `returnedChoices`; one of `uuid`.
        """
        return self.client.getPhoneOptions(uuid=uuid)["return"]["phone"]

    # ------------------------------------------------------------------ #
    # AppServerInfo                                                        #
    # ------------------------------------------------------------------ #

    def add_app_server_info(self, **args):
        """
        Add application-server content info.
        :param appServerName: application server name reference — required
        :param appServerContent: content type
        :param content: content payload
        :return: result dictionary (uuid)
        

        Schema: `appServerInfo` -> `XAppServerInfo`: `appServerName` + `appServerContent`; optional `content`.
        """
        obj = self._build_object("addAppServerInfo", "appServerInfo", args)
        return self.client.addAppServerInfo(appServerInfo=obj)

    def get_app_server_info(self, uuid):
        """
        Get application-server info record.
        :param uuid: app server info uuid — required
        :return: appServerInfo dictionary
        

        Schema: `GetAppServerInfoReq`: optional `returnedTags`; `uuid`.
        """
        return self.client.getAppServerInfo(uuid=uuid)["return"]["appServerInfo"]

    def update_app_server_info(self, **args):
        """
        Update application-server info record.
        :param uuid: app server info uuid — required
        :param appServerName: new app server name reference
        :param appServerContent: content type
        :param content: content payload
        :return: result dictionary
        

        Schema: `UpdateAppServerInfoReq`: optional `appServerName`, `appServerContent`, `content`; one of `uuid`.
        """
        return self.client.updateAppServerInfo(**args)

    def remove_app_server_info(self, uuid):
        """
        Remove application-server info record.
        :param uuid: app server info uuid — required
        :return: result dictionary
        

        Schema: `RemoveAppServerInfoReq`: `uuid`.
        """
        return self.client.removeAppServerInfo(uuid=uuid)

    # ------------------------------------------------------------------ #
    # ApplicationServer                                                    #
    # ------------------------------------------------------------------ #

    def add_application_server(self, **args):
        """
        Add an application server.
        :param appServerType: server type — required
        :param name: server name — required
        :param ipAddress: server IP address
        :param url: server URL
        :param endUserUrl: end-user URL
        :param processNodeName: associated process node
        :return: result dictionary (uuid)
        

        Schema: `applicationServer` -> `XApplicationServer`: `appServerType` + `name`; optional `ipAddress`, `appUsers`, `url`, `endUserUrl`, `processNodeName`, `endUsers`.
        """
        obj = self._build_object("addApplicationServer", "applicationServer", args)
        return self.client.addApplicationServer(applicationServer=obj)

    def get_application_server(self, uuid):
        """
        Get an application server.
        :param uuid: application server uuid — required
        :return: applicationServer dictionary
        

        Schema: `GetApplicationServerReq`: optional `returnedTags`; one of `uuid`.
        """
        return self.client.getApplicationServer(uuid=uuid)["return"][
            "applicationServer"
        ]

    def get_application_servers(
        self,
        search_name="%",
        tagfilter={"name": "", "ipAddress": "", "appServerType": ""},
    ):
        """
        List application servers.
        :param search_name: name search pattern, default '%' (all)
        :param tagfilter: AXL returned tags to include
        :return: list of applicationServer dictionaries, empty when nothing matches
        

        Schema: `ListApplicationServerReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listApplicationServer(
            {"name": search_name}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("applicationServer") or []

    def update_application_server(self, **args):
        """
        Update an application server.
        :param uuid: application server uuid — required
        :param newName: new name
        :param ipAddress: new IP address
        :return: result dictionary
        

        Schema: `UpdateApplicationServerReq`: optional `newName`, `ipAddress`, optional choice of (optional `removeAppUsers`, `addAppUsers`), or `appUsers`, `url`, `endUserUrl`, `processNodeName` and 1 more; one of `uuid`.
        """
        return self.client.updateApplicationServer(**args)

    def remove_application_server(self, uuid):
        """
        Remove an application server.
        :param uuid: application server uuid — required
        :return: result dictionary
        

        Schema: `RemoveApplicationServerReq`: one of `uuid`.
        """
        return self.client.removeApplicationServer(uuid=uuid)

    # ------------------------------------------------------------------ #
    # Change (listChange for change notification)                          #
    # ------------------------------------------------------------------ #

    def list_changes(self, startChangeId=None, objectList=None):
        """
        List change notifications.
        For the first call, omit startChangeId.  For subsequent calls pass a
        dict of ``{"_value_1": <nextStartChangeId int>, "queueId": "<queueId>"}``
        as returned in the prior response's ``queueInfo``.

        :param startChangeId: optional StartChangeId dict from prior queueInfo
        :param objectList: list of XChangeType strings to filter (default: all)
        :return: dict with 'queueInfo' and 'changes' keys (no 'return' wrapper)
        

        Schema: `ListChangeReq`: optional `startChangeId`, `objectList`.
        """
        kwargs = {}
        if startChangeId is not None:
            kwargs["startChangeId"] = startChangeId
        if objectList is not None:
            kwargs["objectList"] = objectList
        # listChange does NOT wrap its result in a 'return' key;
        # the zeep response dict already has 'queueInfo' and 'changes' at the top.
        return self.client.listChange(**kwargs)

    # ------------------------------------------------------------------ #
    # EnterpriseParametersReset (do* operation)                           #
    # ------------------------------------------------------------------ #

    def do_enterprise_parameters_reset(self):
        """
        Trigger a reset of enterprise parameters.
        :return: result dictionary
        """
        return self.client.doEnterpriseParametersReset()

    # ------------------------------------------------------------------ #
    # PhoneNtp                                                             #
    # ------------------------------------------------------------------ #

    def add_phone_ntp(self, **args):
        """
        Add a phone NTP server.
        :param ipAddress: IPv4 address of the NTP server
        :param ipv6Address: IPv6 address of the NTP server
        :param description: description
        :param mode: NTP mode
        :return: result dictionary (uuid)
        

        Schema: `phoneNtp` -> `XPhoneNtp`: `ipAddress` + `ipv6Address` + `mode`; optional `description`.
        """
        obj = self._build_object("addPhoneNtp", "phoneNtp", args)
        return self.client.addPhoneNtp(phoneNtp=obj)

    def get_phone_ntp(self, uuid="", ipAddress="", ipv6Address=""):
        """
        Get a phone NTP server.
        AXL requires either uuid OR both ipAddress+ipv6Address (one may be an
        empty string; the other must be non-empty).

        :param uuid: NTP server uuid
        :param ipAddress: IPv4 address (use with ipv6Address="")
        :param ipv6Address: IPv6 address (use with ipAddress="")
        :return: phoneNtp dictionary
        

        Schema: `GetPhoneNtpReq`: optional `returnedTags`; one of `uuid`, or (`ipAddress` + `ipv6Address`).
        """
        if uuid:
            kwargs = {"uuid": uuid}
        elif ipAddress or ipv6Address:
            kwargs = {"ipAddress": ipAddress, "ipv6Address": ipv6Address}
        else:
            raise ValueError("Provide uuid or at least one of ipAddress/ipv6Address")
        return self.client.getPhoneNtp(**kwargs)["return"]["phoneNtp"]

    def get_phone_ntps(
        self,
        search_ipAddress="%",
        tagfilter={"ipAddress": "", "ipv6Address": "", "description": "", "mode": ""},
    ):
        """
        List phone NTP servers.
        :param search_ipAddress: IP address search pattern, default '%' (all)
        :param tagfilter: AXL returned tags to include
        :return: list of phoneNtp dictionaries, empty when nothing matches
        

        Schema: `ListPhoneNtpReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listPhoneNtp(
            {"ipAddress": search_ipAddress}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("phoneNtp") or []

    def update_phone_ntp(self, **args):
        """
        Update a phone NTP server.
        :param uuid: NTP server uuid (or ipAddress/ipv6Address)
        :param ipAddress: IPv4 address identifier
        :param ipv6Address: IPv6 address identifier
        :param newIpAddress: new IPv4 address
        :param newIpv6Address: new IPv6 address
        :return: result dictionary
        

        Schema: `UpdatePhoneNtpReq`: optional `newIpAddress`, `newIpv6Address`, `description`, `mode`; one of `uuid`, or (`ipAddress` + `ipv6Address`).
        """
        return self.client.updatePhoneNtp(**args)

    def remove_phone_ntp(self, uuid="", ipAddress="", ipv6Address=""):
        """
        Remove a phone NTP server.
        AXL requires either uuid OR both ipAddress+ipv6Address (one may be "").

        :param uuid: NTP server uuid
        :param ipAddress: IPv4 address (use with ipv6Address="")
        :param ipv6Address: IPv6 address (use with ipAddress="")
        :return: result dictionary
        

        Schema: `RemovePhoneNtpReq`: one of `uuid`, or (`ipAddress` + `ipv6Address`).
        """
        if uuid:
            kwargs = {"uuid": uuid}
        elif ipAddress or ipv6Address:
            kwargs = {"ipAddress": ipAddress, "ipv6Address": ipv6Address}
        else:
            raise ValueError("Provide uuid or at least one of ipAddress/ipv6Address")
        return self.client.removePhoneNtp(**kwargs)

    # ------------------------------------------------------------------ #
    # SQLQueryInactive                                                     #
    # ------------------------------------------------------------------ #

    def sql_query_inactive(self, query):
        """
        Execute a SQL query against the inactive CUCM database node.
        Returns the same structure as sql_query / run_sql_query.

        :param query: SQL query string
        :return: {'num_rows': int, 'query': str, 'rows': [{column: value}]}
        

        Schema: `executeSQLQueryInactiveReq`: `sql`.
        """
        result = {"num_rows": 0, "query": query}

        sql_result = self.client.executeSQLQueryInactive(sql=query)

        num_rows = 0
        result_rows = []

        if sql_result is not None and sql_result["return"] is not None:
            for row in sql_result["return"]["row"]:
                row_dict = {}
                for column in row:
                    row_dict[column.tag] = column.text
                result_rows.append(row_dict)
                num_rows += 1

        result["num_rows"] = num_rows
        if num_rows > 0:
            result["rows"] = result_rows

        return result

    # ------------------------------------------------------------------ #
    # ServiceParametersReset (do* operation)                              #
    # ------------------------------------------------------------------ #

    def do_service_parameters_reset(self, processNodeName, service):
        """
        Trigger a reset of service parameters on a node.
        :param processNodeName: node hostname/IP
        :param service: service name
        :return: result dictionary
        

        Schema: `DoServiceParametersResetReq`: `processNodeName` + `service`.
        """
        return self.client.doServiceParametersReset(
            processNodeName=processNodeName, service=service
        )

    # ------------------------------------------------------------------ #
    # SyslogConfiguration                                                  #
    # ------------------------------------------------------------------ #

    def get_syslog_configuration(self, serverName, serviceGroup, service, tagfilter=None):
        """
        Get syslog configuration for a server/service.
        :param serverName: syslog server name — required
        :param serviceGroup: service group — required
        :param service: service name — required
        :param tagfilter: AXL returned tags to include (optional)
        :return: syslogConfiguration dictionary
        

        Schema: `GetSyslogConfigurationReq`: optional `returnedTags`; `serverName` + `serviceGroup` + `service`.
        """
        kwargs = {
            "serverName": serverName,
            "serviceGroup": serviceGroup,
            "service": service,
        }
        if tagfilter is not None:
            kwargs["returnedTags"] = tagfilter
        return self.client.getSyslogConfiguration(**kwargs)["return"][
            "syslogConfiguration"
        ]

    def update_syslog_configuration(self, serverName, serviceGroup, service, **args):
        """
        Update syslog configuration for a server/service.
        :param serverName: syslog server name — required
        :param serviceGroup: service group — required
        :param service: service name — required
        :param alarmConfigs: alarm configuration list
        :param EndPointAlarm: boolean, enable endpoint alarm
        :return: result dictionary
        

        Schema: `UpdateSyslogConfigurationReq`: `alarmConfigs`; optional `EndPointAlarm`; `serverName` + `serviceGroup` + `service`.
        """
        return self.client.updateSyslogConfiguration(
            serverName=serverName,
            serviceGroup=serviceGroup,
            service=service,
            **args,
        )

    # ------------------------------------------------------------------ #
    # AuthenticateUser (do* operation)                                    #
    # ------------------------------------------------------------------ #

    def do_authenticate_user(self, userid, password=None, pin=None):
        """
        Authenticate an end-user against CUCM.
        :param userid: end-user ID — required
        :param password: user password (or pin)
        :param pin: user PIN (or password)
        :return: dict with 'userAuthenticated' and optionally 'code', 'daysToExpiry'
        

        Schema: `DoAuthenticateUserReq`: `userid`; one of `password`, or `pin`.
        """
        kwargs = {"userid": userid}
        if password is not None:
            kwargs["password"] = password
        if pin is not None:
            kwargs["pin"] = pin
        return self.client.doAuthenticateUser(**kwargs)["return"]

    # ------------------------------------------------------------------ #
    # CustomUserField                                                      #
    # ------------------------------------------------------------------ #

    def add_custom_user_field(self, **args):
        """
        Add a custom user field definition.
        :param field: field name — required
        :return: result dictionary (uuid)
        

        Schema: `customUserField` -> `XCustomUserField`: `field`.
        """
        obj = self._build_object("addCustomUserField", "customUserField", args)
        return self.client.addCustomUserField(customUserField=obj)

    def get_custom_user_field(self, field="", uuid=""):
        """
        Get a custom user field definition.
        :param field: field name (or uuid)
        :param uuid: field uuid (or field name)
        :return: customUserField dictionary
        

        Schema: `GetCustomUserFieldReq`: optional `returnedTags`; one of `field`, or `uuid`.
        """
        if uuid:
            kwargs = {"uuid": uuid}
        elif field:
            kwargs = {"field": field}
        else:
            raise ValueError("Provide exactly one of field or uuid")
        return self.client.getCustomUserField(**kwargs)["return"]["customUserField"]

    def get_custom_user_fields(self, tagfilter={"field": ""}):
        """
        List custom user field definitions.
        :param tagfilter: AXL returned tags to include, e.g. {'field': ''}
        :return: list of customUserField dictionaries, empty when nothing matches
        

        Schema: `ListCustomUserFieldReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listCustomUserField(
            {"field": "%"}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("customUserField") or []

    def update_custom_user_field(self, **args):
        """
        Update a custom user field definition.
        :param uuid: field uuid (or field name)
        :param field: field name identifier
        :param newField: new field name
        :return: result dictionary
        

        Schema: `UpdateCustomUserFieldReq`: optional `newField`; one of `uuid`, or `field`.
        """
        return self.client.updateCustomUserField(**args)

    def remove_custom_user_field(self, field="", uuid=""):
        """
        Remove a custom user field definition.
        :param field: field name (or uuid)
        :param uuid: field uuid (or field name)
        :return: result dictionary
        

        Schema: `RemoveCustomUserFieldReq`: one of `field`, or `uuid`.
        """
        if uuid:
            kwargs = {"uuid": uuid}
        elif field:
            kwargs = {"field": field}
        else:
            raise ValueError("Provide exactly one of field or uuid")
        return self.client.removeCustomUserField(**kwargs)

    # ------------------------------------------------------------------ #
    # SelfProvisioning (update only in AXL)                               #
    # ------------------------------------------------------------------ #

    def update_self_provisioning(self, **args):
        """
        Update self-provisioning settings.
        :param requireAuthentication: require auth for self-provisioning
        :param allowAuthentication: allow auth
        :param authenticationCode: shared authentication code
        :param ctiRoutePoint: CTI route point name
        :param applicationUser: application user name
        :return: result dictionary
        

        Schema: `UpdateSelfProvisioningReq`: optional `requireAuthentication`, `allowAuthentication`, `authenticationCode`, `ctiRoutePoint`, `applicationUser`, optional choice of (optional `removeLanguages`, `addLanguages`), or `languages`.
        """
        return self.client.updateSelfProvisioning(**args)
