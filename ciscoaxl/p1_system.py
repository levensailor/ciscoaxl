"""
P1 System Mixin — batch B5
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
"""


class P1System:
    """Mixin providing device settings, LDAP, system nodes, security,
    licensing, and voicemail port helpers."""

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
        """
        return self.client.getDefaultDeviceProfile(
            **self._identify(name=name, uuid=uuid)
        )["return"]["defaultDeviceProfile"]

    def get_default_device_profiles(self, tagfilter={"name": "", "description": ""}):
        """
        List default device profiles.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of defaultDeviceProfile dictionaries, empty when nothing matches
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
        """
        return self.client.updateDefaultDeviceProfile(**args)

    def remove_default_device_profile(self, name="", uuid=""):
        """
        Remove a default device profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: result dictionary
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
        """
        return self.client.getFeatureControlPolicy(
            **self._identify(name=name, uuid=uuid)
        )["return"]["featureControlPolicy"]

    def get_feature_control_policies(self, tagfilter={"name": "", "description": ""}):
        """
        List feature control policies.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of featureControlPolicy dictionaries, empty when nothing matches
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
        """
        return self.client.updateFeatureControlPolicy(**args)

    def remove_feature_control_policy(self, name="", uuid=""):
        """
        Remove a feature control policy.
        :param name: policy name (or uuid)
        :param uuid: policy uuid (or name)
        :return: result dictionary
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
        """
        return self.client.getFeatureGroupTemplate(
            **self._identify(name=name, uuid=uuid)
        )["return"]["featureGroupTemplate"]

    def get_feature_group_templates(self, tagfilter={"name": "", "description": ""}):
        """
        List feature group templates.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of featureGroupTemplate dictionaries, empty when nothing matches
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
        """
        return self.client.updateFeatureGroupTemplate(**args)

    def remove_feature_group_template(self, name="", uuid=""):
        """
        Remove a feature group template.
        :param name: template name (or uuid)
        :param uuid: template uuid (or name)
        :return: result dictionary
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
        """
        return self.client.updateIpPhoneServices(**args)

    def remove_ip_phone_service(self, serviceName="", uuid=""):
        """
        Remove an IP phone service.
        :param serviceName: service name (or uuid)
        :param uuid: service uuid (or serviceName)
        :return: result dictionary
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
        """
        return self.client.getLdapFilter(
            **self._identify(name=name, uuid=uuid)
        )["return"]["ldapFilter"]

    def get_ldap_filters(self, tagfilter={"name": "", "filter": ""}):
        """
        List LDAP filters.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of ldapFilter dictionaries, empty when nothing matches
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
        """
        return self.client.updateLdapFilter(**args)

    def remove_ldap_filter(self, name="", uuid=""):
        """
        Remove an LDAP filter.
        :param name: filter name (or uuid)
        :param uuid: filter uuid (or name)
        :return: result dictionary
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
        """
        if not uuid:
            raise ValueError("Provide uuid (LdapSearch has no name identifier)")
        return self.client.getLdapSearch(uuid=uuid)["return"]["ldapSearch"]

    def get_ldap_searches(self, tagfilter={"distinguishedName": ""}):
        """
        List LDAP search configurations.
        :param tagfilter: AXL returned tags to include, e.g. {'distinguishedName': ''}
        :return: list of ldapSearch dictionaries, empty when nothing matches
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
        """
        return self.client.updateLdapSyncCustomField(**args)

    def remove_ldap_sync_custom_field(self, ldapConfigurationName="", customUserField="", uuid=""):
        """
        Remove an LDAP sync custom field mapping.
        :param ldapConfigurationName: LDAP directory config name (required unless uuid provided)
        :param customUserField: CUCM user field (required unless uuid provided)
        :param uuid: custom field uuid (alternative to ldapConfigurationName+customUserField)
        :return: result dictionary
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
        """
        return self.client.getCallManager(
            **self._identify(name=name, uuid=uuid)
        )["return"]["callManager"]

    def get_call_managers(self, tagfilter={"name": "", "description": ""}):
        """
        List CallManager nodes.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of callManager dictionaries, empty when nothing matches
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
        """
        return self.client.updateCallManager(**args)

    def apply_call_manager(self, name="", uuid=""):
        """
        Apply CallManager configuration.
        :param name: node name (or uuid)
        :param uuid: node uuid (or name)
        :return: result dictionary
        """
        return self.client.applyCallManager(**self._identify(name=name, uuid=uuid))

    def reset_call_manager(self, name="", uuid=""):
        """
        Reset a CallManager node.
        :param name: node name (or uuid)
        :param uuid: node uuid (or name)
        :return: result dictionary
        """
        return self.client.resetCallManager(**self._identify(name=name, uuid=uuid))

    def restart_call_manager(self, name="", uuid=""):
        """
        Restart a CallManager node.
        :param name: node name (or uuid)
        :param uuid: node uuid (or name)
        :return: result dictionary
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
        :return: osVersion dictionary
        """
        return self.client.getOSVersion()["return"]["osVersion"]

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
        """
        return self.client.updateProcessNode(**args)

    def remove_process_node(self, name="", uuid=""):
        """
        Remove a process node.
        :param name: node name (or uuid)
        :param uuid: node uuid (or name)
        :return: result dictionary
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
        """
        return self.client.getCredentialPolicy(
            **self._identify(name=name, uuid=uuid)
        )["return"]["credentialPolicy"]

    def get_credential_policies(self, tagfilter={"name": ""}):
        """
        List credential policies.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of credentialPolicy dictionaries, empty when nothing matches
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
        """
        return self.client.updateCredentialPolicy(**args)

    def remove_credential_policy(self, name="", uuid=""):
        """
        Remove a credential policy.
        :param name: policy name (or uuid)
        :param uuid: policy uuid (or name)
        :return: result dictionary
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
        """
        return self.client.getCredentialPolicyDefault()["return"]["credentialPolicyDefault"]

    def update_credential_policy_default(self, **args):
        """
        Update the credential policy default configuration.
        :param credentialUser: default policy for user pins/passwords
        :param credentialApplicationUser: default policy for application users
        :return: result dictionary
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
        """
        return self.client.getLicensedUser(
            **self._identify(name=name, uuid=uuid)
        )["return"]["licensedUser"]

    def get_licensed_users(self, tagfilter={"userId": "", "lastName": ""}):
        """
        List licensed users.
        :param tagfilter: AXL returned tags to include, e.g. {'userId': ''}
        :return: list of licensedUser dictionaries, empty when nothing matches
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
        Get the Smart Licensing status.
        :return: smartLicenseStatus dictionary
        """
        return self.client.getSmartLicenseStatus()["return"]["smartLicenseStatus"]

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
        """
        return self.client.updateMessageWaiting(**args)

    def remove_message_waiting(self, pattern="", uuid=""):
        """
        Remove a message waiting number.
        :param pattern: DN pattern (or uuid)
        :param uuid: DN uuid (or pattern)
        :return: result dictionary
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
        """
        return self.client.getVoiceMailPort(
            **self._identify(name=name, uuid=uuid)
        )["return"]["voiceMailPort"]

    def get_voice_mail_ports(self, tagfilter={"name": "", "description": ""}):
        """
        List voice mail ports.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of voiceMailPort dictionaries, empty when nothing matches
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
        """
        return self.client.updateVoiceMailPort(**args)

    def remove_voice_mail_port(self, name="", uuid=""):
        """
        Remove a voice mail port.
        :param name: port name (or uuid)
        :param uuid: port uuid (or name)
        :return: result dictionary
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
        """
        return self.client.applyVoiceMailPort(**self._identify(name=name, uuid=uuid))

    def reset_voice_mail_port(self, name="", uuid=""):
        """
        Reset a voice mail port.
        :param name: port name (or uuid)
        :param uuid: port uuid (or name)
        :return: result dictionary
        """
        return self.client.resetVoiceMailPort(**self._identify(name=name, uuid=uuid))

    def restart_voice_mail_port(self, name="", uuid=""):
        """
        Restart a voice mail port.
        :param name: port name (or uuid)
        :param uuid: port uuid (or name)
        :return: result dictionary
        """
        return self.client.restartVoiceMailPort(**self._identify(name=name, uuid=uuid))
