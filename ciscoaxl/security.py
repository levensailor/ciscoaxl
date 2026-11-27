"""Security profile, CAPF, VPN, LDAP, date/time, and phone lifecycle wrappers.

Adds security-profile, date/time, LDAP, version, registration, and phone-lifecycle methods.

Included groups:
  - PhoneSecurityProfile : add, get, list, update, delete, apply, reset
  - SipProfile           : add, list, update, delete, apply, restart
                           (get_sip_profile already lives in axl.py)
  - SipTrunkSecurityProfile : add, list, update, delete, apply, reset
                              (get_sip_security_profile already lives in axl.py)
  - DateTimeGroup        : add, get, list, update, delete, apply, reset
  - LdapDirectory        : add, get, update, delete
                           (get_ldap_dir / listLdapDirectory already lives in axl.py)
  - LdapSyncStatus       : get
  - CCMVersion           : get
  - RegistrationDynamic  : get, list
  - Phone lifecycle      : apply, reset, restart, lock, wipe
                           (phone add/get/update/delete already live in axl.py)

Security / CAPF / VPN:
  ApplicationUserCapfProfile (full CRUD)
  EndUserCapfProfile         (full CRUD)
  SecureConfig               (get / update)
  SipRealm                   (full CRUD)
  TvsCertificate             (get / update / list)
  VpnGateway                 (full CRUD)
  VpnGroup                   (full CRUD)
  VpnProfile                 (full CRUD)
"""


class SecurityMixin:
    """Security profile, CAPF, VPN, LDAP, date/time, and phone lifecycle wrappers."""

    # ------------------------------------------------------------------ #
    # PhoneSecurityProfile                                                 #
    # ------------------------------------------------------------------ #

    def add_phone_security_profile(self, **args):
        """
        Add a phone security profile.
        :param name: profile name — required
        :param description: description
        :param deviceSecurityMode: e.g. 'Non Secure', 'Authenticated', 'Encrypted'
        :param authenticationMode: e.g. 'By Null String', 'By Authentication String'
        :param keySize: e.g. '1024', '2048'
        :param transportType: e.g. 'TCP+UDP', 'TLS'
        :return: result dictionary (uuid)
        

        Schema: `phoneSecurityProfile` -> `XPhoneSecurityProfile`: `phoneType` + `protocol` + `name`; optional `description`, `deviceSecurityMode`, `authenticationMode`, `keySize`, `keyOrder`, `ecKeySize` and 7 more.
        """
        profile = self._build_object(
            "addPhoneSecurityProfile",
            "phoneSecurityProfile",
            args,
        )
        return self.client.addPhoneSecurityProfile(phoneSecurityProfile=profile)

    def get_phone_security_profile(self, name="", uuid=""):
        """
        Get a phone security profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: phone security profile dictionary
        

        Schema: `GetPhoneSecurityProfileReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getPhoneSecurityProfile(
            **self._identify(name=name, uuid=uuid)
        )["return"]["phoneSecurityProfile"]

    def get_phone_security_profiles(
        self, tagfilter={"name": "", "description": ""}
    ):
        """
        List phone security profiles.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of phone security profile dictionaries, empty when nothing matches
        

        Schema: `ListPhoneSecurityProfileReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        return self.client.listPhoneSecurityProfile(
            {"name": "%"}, returnedTags=tagfilter
        )["return"]["phoneSecurityProfile"]

    def update_phone_security_profile(self, **args):
        """
        Update a phone security profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :param newName: new profile name
        :param description: description
        :return: result dictionary
        

        Schema: `UpdatePhoneSecurityProfileReq`: optional `newName`, `description`, `deviceSecurityMode`, `authenticationMode`, `keySize`, `keyOrder` and 8 more.
        """
        return self.client.updatePhoneSecurityProfile(**args)

    def delete_phone_security_profile(self, name="", uuid=""):
        """
        Delete a phone security profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removePhoneSecurityProfile(
            **self._identify(name=name, uuid=uuid)
        )

    def apply_phone_security_profile(self, name="", uuid=""):
        """
        Apply a phone security profile (push config to associated phones).
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.applyPhoneSecurityProfile(
            **self._identify(name=name, uuid=uuid)
        )

    def reset_phone_security_profile(self, name="", uuid=""):
        """
        Reset a phone security profile (reset associated phones).
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.resetPhoneSecurityProfile(
            **self._identify(name=name, uuid=uuid)
        )

    # ------------------------------------------------------------------ #
    # SipProfile  (get_sip_profile already in axl.py — not duplicated)   #
    # ------------------------------------------------------------------ #

    def add_sip_profile(self, **args):
        """
        Add a SIP profile.
        :param name: profile name — required
        :param description: description
        :return: result dictionary (uuid)
        

        Schema: `sipProfile` -> `XSipProfile`: `name` + `sipBandwidthModifier` + `userAgentServerHeaderInfo` + `dialStringInterpretation` + `callingLineIdentification` + `sipSessionRefreshMethod` + `earlyOfferSuppVoiceCall` + `cucmVersionInSipHeader` + `confidentialAccessLevelHeaders`; optional `description`, `defaultTelephonyEventPayloadType`, `redirectByApplication`, `ringing180`, `timerInvite`, `timerRegisterDelta` and 76 more.
        """
        profile = self._build_object(
            "addSipProfile",
            "sipProfile",
            args,
        )
        return self.client.addSipProfile(sipProfile=profile)

    def get_sip_profiles(self, tagfilter={"name": "", "description": ""}):
        """
        List SIP profiles.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of SIP profile dictionaries, empty when nothing matches
        

        Schema: `ListSipProfileReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        return self.client.listSipProfile(
            {"name": "%"}, returnedTags=tagfilter
        )["return"]["sipProfile"]

    def update_sip_profile(self, **args):
        """
        Update a SIP profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :param newName: new profile name
        :return: result dictionary
        

        Schema: `UpdateSipProfileReq`: optional `newName`, `description`, `defaultTelephonyEventPayloadType`, `redirectByApplication`, `ringing180`, `timerInvite` and 85 more.
        """
        return self.client.updateSipProfile(**args)

    def delete_sip_profile(self, name="", uuid=""):
        """
        Delete a SIP profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeSipProfile(**self._identify(name=name, uuid=uuid))

    def apply_sip_profile(self, name="", uuid=""):
        """
        Apply a SIP profile (push config to associated trunks/phones).
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.applySipProfile(**self._identify(name=name, uuid=uuid))

    def restart_sip_profile(self, name="", uuid=""):
        """
        Restart devices associated with a SIP profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.restartSipProfile(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------ #
    # SipTrunkSecurityProfile                                             #
    # (get_sip_security_profile already in axl.py — not duplicated)      #
    # ------------------------------------------------------------------ #

    def add_sip_trunk_security_profile(self, **args):
        """
        Add a SIP trunk security profile.
        :param name: profile name — required
        :param description: description
        :param deviceSecurityMode: e.g. 'Non Secure', 'Authenticated', 'Encrypted'
        :param incomingTransport: e.g. 'TCP+UDP', 'TLS'
        :param outgoingTransport: e.g. 'TCP', 'TLS'
        :return: result dictionary (uuid)
        

        Schema: `sipTrunkSecurityProfile` -> `XSipTrunkSecurityProfile`: `name` + `sipV150OutboundSdpOfferFiltering`; optional `description`, `securityMode`, `incomingTransport`, `outgoingTransport`, `digestAuthentication`, `noncePolicyTime` and 9 more.
        """
        profile = self._build_object(
            "addSipTrunkSecurityProfile",
            "sipTrunkSecurityProfile",
            args,
        )
        return self.client.addSipTrunkSecurityProfile(
            sipTrunkSecurityProfile=profile
        )

    def get_sip_trunk_security_profiles(
        self, tagfilter={"name": "", "description": ""}
    ):
        """
        List SIP trunk security profiles.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of SIP trunk security profile dictionaries
        

        Schema: `ListSipTrunkSecurityProfileReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        return self.client.listSipTrunkSecurityProfile(
            {"name": "%"}, returnedTags=tagfilter
        )["return"]["sipTrunkSecurityProfile"]

    def update_sip_trunk_security_profile(self, **args):
        """
        Update a SIP trunk security profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :param newName: new profile name
        :return: result dictionary
        

        Schema: `UpdateSipTrunkSecurityProfileReq`: optional `newName`, `description`, `securityMode`, `incomingTransport`, `outgoingTransport`, `digestAuthentication` and 11 more.
        """
        return self.client.updateSipTrunkSecurityProfile(**args)

    def delete_sip_trunk_security_profile(self, name="", uuid=""):
        """
        Delete a SIP trunk security profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeSipTrunkSecurityProfile(
            **self._identify(name=name, uuid=uuid)
        )

    def apply_sip_trunk_security_profile(self, name="", uuid=""):
        """
        Apply a SIP trunk security profile (push config to associated trunks).
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.applySipTrunkSecurityProfile(
            **self._identify(name=name, uuid=uuid)
        )

    def reset_sip_trunk_security_profile(self, name="", uuid=""):
        """
        Reset devices associated with a SIP trunk security profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.resetSipTrunkSecurityProfile(
            **self._identify(name=name, uuid=uuid)
        )

    # ------------------------------------------------------------------ #
    # DateTimeGroup                                                        #
    # ------------------------------------------------------------------ #

    def add_date_time_group(self, **args):
        """
        Add a date/time group.
        :param name: group name — required
        :param timeZone: CUCM time-zone string, default 'Europe/London'
        :param separator: date separator character, default '/'
        :param dateformat: date display format, default 'M/D/YA'
        :param timeFormat: time format, default '12-hour'
        :return: result dictionary (uuid)
        

        Schema: `dateTimeGroup` -> `XDateTimeGroup`: `name` + `timeZone` + `separator` + `dateformat` + `timeFormat`; optional `phoneNtpReferences`.
        """
        dtg = self._build_object(
            "addDateTimeGroup",
            "dateTimeGroup",
            args,
            defaults={
                "separator": "/",
                "dateformat": "M/D/YA",
                "timeFormat": "12-hour",
            },
        )
        return self.client.addDateTimeGroup(dateTimeGroup=dtg)

    def get_date_time_group(self, name="", uuid=""):
        """
        Get a date/time group.
        :param name: group name (or uuid)
        :param uuid: group uuid (or name)
        :return: date/time group dictionary
        

        Schema: `GetDateTimeGroupReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getDateTimeGroup(
            **self._identify(name=name, uuid=uuid)
        )["return"]["dateTimeGroup"]

    def get_date_time_groups(self, tagfilter={"name": "", "timeZone": ""}):
        """
        List date/time groups.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of date/time group dictionaries, empty when nothing matches
        

        Schema: `ListDateTimeGroupReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        return self.client.listDateTimeGroup(
            {"name": "%"}, returnedTags=tagfilter
        )["return"]["dateTimeGroup"]

    def update_date_time_group(self, **args):
        """
        Update a date/time group.
        :param name: group name (or uuid)
        :param uuid: group uuid (or name)
        :param newName: new group name
        :param timeZone: CUCM time-zone string
        :return: result dictionary
        

        Schema: `UpdateDateTimeGroupReq`: optional `newName`, `timeZone`, `separator`, `dateformat`, `timeFormat`, optional choice of (optional `removePhoneNtpReferences`, `addPhoneNtpReferences`), or `phoneNtpReferences`.
        """
        return self.client.updateDateTimeGroup(**args)

    def delete_date_time_group(self, name="", uuid=""):
        """
        Delete a date/time group.
        :param name: group name (or uuid)
        :param uuid: group uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeDateTimeGroup(
            **self._identify(name=name, uuid=uuid)
        )

    def apply_date_time_group(self, name="", uuid=""):
        """
        Apply a date/time group (push config to associated device pools).
        :param name: group name (or uuid)
        :param uuid: group uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.applyDateTimeGroup(
            **self._identify(name=name, uuid=uuid)
        )

    def reset_date_time_group(self, name="", uuid=""):
        """
        Reset devices associated with a date/time group.
        :param name: group name (or uuid)
        :param uuid: group uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.resetDateTimeGroup(
            **self._identify(name=name, uuid=uuid)
        )

    # ------------------------------------------------------------------ #
    # LdapDirectory                                                        #
    # (get_ldap_dir / listLdapDirectory already in axl.py — not dupl.)   #
    # ------------------------------------------------------------------ #

    def add_ldap_directory(self, **args):
        """
        Add an LDAP directory sync configuration.
        :param name: directory name — required
        :param ldapDn: bind DN
        :param ldapPassword: bind password
        :param ldapServer: LDAP host {'hostName': ..., 'port': ...}
        :param userSearchBase: user search base DN
        :return: result dictionary (uuid)
        

        Schema: `ldapDirectory` -> `XLdapDirectory`: `name` + `ldapDn` + `ldapPassword` + `userSearchBase` + `intervalValue` + `nextExecTime` + `servers`; optional `repeatable`, `scheduleUnit`, `middleName`, `phoneNumber`, `mailId`, `ldapFilter` and 9 more.
        """
        ldap = self._build_object(
            "addLdapDirectory",
            "ldapDirectory",
            args,
        )
        return self.client.addLdapDirectory(ldapDirectory=ldap)

    def get_ldap_directory(self, name="", uuid=""):
        """
        Get a single LDAP directory configuration.
        :param name: directory name (or uuid)
        :param uuid: directory uuid (or name)
        :return: LDAP directory dictionary
        

        Schema: `GetLdapDirectoryReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getLdapDirectory(
            **self._identify(name=name, uuid=uuid)
        )["return"]["ldapDirectory"]

    def update_ldap_directory(self, **args):
        """
        Update an LDAP directory sync configuration.
        :param name: directory name (or uuid)
        :param uuid: directory uuid (or name)
        :param ldapDn: bind DN
        :param ldapPassword: bind password
        :param userSearchBase: user search base DN
        :return: result dictionary
        

        Schema: `UpdateLdapDirectoryReq`: optional `newName`, `ldapDn`, `ldapPassword`, `userSearchBase`, `repeatable`, `intervalValue` and 12 more.
        """
        return self.client.updateLdapDirectory(**args)

    def delete_ldap_directory(self, name="", uuid=""):
        """
        Delete an LDAP directory sync configuration.
        :param name: directory name (or uuid)
        :param uuid: directory uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeLdapDirectory(
            **self._identify(name=name, uuid=uuid)
        )

    # ------------------------------------------------------------------ #
    # LdapSyncStatus                                                       #
    # ------------------------------------------------------------------ #

    def get_ldap_sync_status(self, name="", uuid=""):
        """
        Get the current LDAP sync status for a directory.
        :param name: directory name (or uuid)
        :param uuid: directory uuid (or name)
        :return: sync status value string
        

        Schema: `GetLdapSyncStatusReq`: one of `name`, or `uuid`.
        """
        return self.client.getLdapSyncStatus(
            **self._identify(name=name, uuid=uuid)
        )["return"]

    # ------------------------------------------------------------------ #
    # CCMVersion                                                           #
    # ------------------------------------------------------------------ #

    def get_ccm_version(self, process_node_name=""):
        """
        Get the CUCM component version.
        :param process_node_name: specific publisher/subscriber hostname; leave blank for
                                  the connected node.
        :return: result dictionary with 'componentVersion' → {'version': ...}
        

        Schema: `GetCCMVersionReq`: optional `processNodeName`.
        """
        kwargs = {}
        if process_node_name:
            kwargs["processNodeName"] = process_node_name
        return self.client.getCCMVersion(**kwargs)["return"]

    # ------------------------------------------------------------------ #
    # RegistrationDynamic                                                  #
    # ------------------------------------------------------------------ #

    def get_registration_dynamic(self, device="", uuid="", tagfilter=None):
        """
        Get dynamic registration data for a device.
        :param device: device name (or uuid)
        :param uuid: device uuid (or device name)
        :param tagfilter: optional dict of returned tags
        :return: registrationDynamic dictionary
        

        Schema: `GetRegistrationDynamicReq`: optional `returnedTags`; one of `device`, or `uuid`.
        """
        if bool(device) == bool(uuid):
            raise ValueError("Provide exactly one of device or uuid")
        identifier = {"device": device} if device else {"uuid": uuid}
        kwargs = dict(identifier)
        if tagfilter:
            kwargs["returnedTags"] = tagfilter
        return self.client.getRegistrationDynamic(**kwargs)["return"][
            "registrationDynamic"
        ]

    def get_registrations_dynamic(self, search_device="%", tagfilter={"device": ""}):
        """
        List dynamic registration data.
        :param search_device: device name search pattern, default '%' (all)
        :param tagfilter: AXL returned tags to include, e.g. {'device': ''}
        :return: list of registrationDynamic dictionaries, empty when nothing matches
        

        Schema: `ListRegistrationDynamicReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        return self.client.listRegistrationDynamic(
            {"device": search_device}, returnedTags=tagfilter
        )["return"]["registrationDynamic"]

    # ------------------------------------------------------------------ #
    # Phone lifecycle                                                      #
    # (get/add/update/delete phone already in axl.py — not duplicated)   #
    # ------------------------------------------------------------------ #

    def apply_phone(self, name="", uuid=""):
        """
        Apply phone configuration (push pending config to the device).
        :param name: device name (or uuid)
        :param uuid: device uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.applyPhone(**self._identify(name=name, uuid=uuid))

    def reset_phone(self, name="", uuid=""):
        """
        Reset a phone (factory reset / full restart).
        :param name: device name (or uuid)
        :param uuid: device uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.resetPhone(**self._identify(name=name, uuid=uuid))

    def restart_phone(self, name="", uuid=""):
        """
        Restart a phone (soft restart, preserves config).
        :param name: device name (or uuid)
        :param uuid: device uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.restartPhone(**self._identify(name=name, uuid=uuid))

    def lock_phone(self, name="", uuid=""):
        """
        Lock a phone (Mobile Connect / MDM lock).
        :param name: device name (or uuid)
        :param uuid: device uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.lockPhone(**self._identify(name=name, uuid=uuid))

    def wipe_phone(self, name="", uuid=""):
        """
        Wipe a phone (Mobile Connect / MDM remote wipe).
        :param name: device name (or uuid)
        :param uuid: device uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.wipePhone(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------ #
    # ApplicationUserCapfProfile                                          #
    # ------------------------------------------------------------------ #

    def get_application_user_capf_profiles(
        self,
        tagfilter={
            "applicationUser": "",
            "instanceId": "",
            "certificateOperation": "",
            "authenticationMode": "",
            "authenticationString": "",
        },
    ):
        """
        List all Application User CAPF Profiles.
        :param tagfilter: AXL returned tags to include
        :return: list of dicts, empty when nothing matches
        

        Schema: `ListApplicationUserCapfProfileReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        response = self.client.listApplicationUserCapfProfile(
            {"applicationUser": "%"},
            returnedTags=tagfilter,
        )["return"]
        if response:
            return response["applicationUserCapfProfile"]
        return []

    def get_application_user_capf_profile(self, **args):
        """
        Get an Application User CAPF Profile.
        :param instanceId: CAPF instance ID (or uuid)
        :param uuid: profile uuid (or instanceId)
        :return: result dict
        

        Schema: `GetApplicationUserCapfProfileReq`: optional `returnedTags`; one of `instanceId`, or `uuid`.
        """
        return self.client.getApplicationUserCapfProfile(**args)["return"][
            "applicationUserCapfProfile"
        ]

    def add_application_user_capf_profile(self, **args):
        """
        Add an Application User CAPF Profile.
        :param applicationUser: application user name — required
        :param instanceId: CAPF instance ID — required
        :return: result dict
        

        Schema: `applicationUserCapfProfile` -> `XApplicationUserCapfProfile`: `applicationUser` + `instanceId` + `certificateOperation` + `authenticationMode` + `keySize`; optional `authenticationString`, `keyOrder`, `ecKeySize`, `operationCompletion`.
        """
        obj = self._build_object(
            "addApplicationUserCapfProfile", "applicationUserCapfProfile", args
        )
        return self.client.addApplicationUserCapfProfile(obj)

    def update_application_user_capf_profile(self, **args):
        """
        Update an Application User CAPF Profile.
        :param instanceId: CAPF instance ID (or uuid)
        :param uuid: profile uuid (or instanceId)
        :return: result dict
        

        Schema: `UpdateApplicationUserCapfProfileReq`: optional `certificateOperation`, `authenticationMode`, `authenticationString`, `keySize`, `keyOrder`, `ecKeySize` and 1 more; one of `uuid`, or `instanceId`.
        """
        return self.client.updateApplicationUserCapfProfile(**args)

    def delete_application_user_capf_profile(self, **args):
        """
        Delete an Application User CAPF Profile.
        :param instanceId: CAPF instance ID (or uuid)
        :param uuid: profile uuid (or instanceId)
        :return: result dict
        

        Schema: `RemoveApplicationUserCapfProfileReq`: one of `instanceId`, or `uuid`.
        """
        return self.client.removeApplicationUserCapfProfile(**args)

    # ------------------------------------------------------------------ #
    # EndUserCapfProfile                                                  #
    # ------------------------------------------------------------------ #

    def get_end_user_capf_profiles(
        self,
        tagfilter={
            "endUserId": "",
            "instanceId": "",
            "certificationOperation": "",
            "authenticationMode": "",
            "authenticationString": "",
        },
    ):
        """
        List all End User CAPF Profiles.
        :param tagfilter: AXL returned tags to include
        :return: list of dicts, empty when nothing matches
        

        Schema: `ListEndUserCapfProfileReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        response = self.client.listEndUserCapfProfile(
            {"endUserId": "%"},
            returnedTags=tagfilter,
        )["return"]
        if response:
            return response["endUserCapfProfile"]
        return []

    def get_end_user_capf_profile(self, **args):
        """
        Get an End User CAPF Profile.
        :param instanceId: CAPF instance ID (or uuid)
        :param uuid: profile uuid (or instanceId)
        :return: result dict
        

        Schema: `GetEndUserCapfProfileReq`: optional `returnedTags`; one of `instanceId`, or `uuid`.
        """
        return self.client.getEndUserCapfProfile(**args)["return"][
            "endUserCapfProfile"
        ]

    def add_end_user_capf_profile(self, **args):
        """
        Add an End User CAPF Profile.
        :param endUserId: end-user ID — required
        :param instanceId: CAPF instance ID — required
        :return: result dict
        

        Schema: `endUserCapfProfile` -> `XEndUserCapfProfile`: `endUserId` + `instanceId` + `certificationOperation` + `authenticationMode` + `keySize`; optional `authenticationString`, `keyOrder`, `ecKeySize`, `operationCompletion`.
        """
        obj = self._build_object("addEndUserCapfProfile", "endUserCapfProfile", args)
        return self.client.addEndUserCapfProfile(obj)

    def update_end_user_capf_profile(self, **args):
        """
        Update an End User CAPF Profile.
        :param instanceId: CAPF instance ID (or uuid)
        :param uuid: profile uuid (or instanceId)
        :return: result dict
        

        Schema: `UpdateEndUserCapfProfileReq`: optional `certificationOperation`, `authenticationMode`, `authenticationString`, `keySize`, `keyOrder`, `ecKeySize` and 1 more; one of `uuid`, or `instanceId`.
        """
        return self.client.updateEndUserCapfProfile(**args)

    def delete_end_user_capf_profile(self, **args):
        """
        Delete an End User CAPF Profile.
        :param instanceId: CAPF instance ID (or uuid)
        :param uuid: profile uuid (or instanceId)
        :return: result dict
        

        Schema: `RemoveEndUserCapfProfileReq`: one of `instanceId`, or `uuid`.
        """
        return self.client.removeEndUserCapfProfile(**args)

    # ------------------------------------------------------------------ #
    # SecureConfig — get / update (no add / delete / list in AXL schema) #
    # ------------------------------------------------------------------ #

    def get_secure_config(self, **args):
        """
        Get a Secure Config entry.
        :param name: config name (or uuid)
        :param uuid: config uuid (or name)
        :return: result dict
        

        Schema: `GetSecureConfigReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getSecureConfig(**args)["return"]["secureConfig"]

    def update_secure_config(self, **args):
        """
        Update a Secure Config entry.
        :param name: config name (or uuid)
        :param uuid: config uuid (or name)
        :return: result dict
        

        Schema: `UpdateSecureConfigReq`: optional `value`.
        """
        return self.client.updateSecureConfig(**args)

    # ------------------------------------------------------------------ #
    # SipRealm                                                            #
    # ------------------------------------------------------------------ #

    def get_sip_realms(
        self,
        tagfilter={"realm": "", "userid": "", "digestCredentials": ""},
    ):
        """
        List all SIP Realms.
        :param tagfilter: AXL returned tags to include
        :return: list of dicts, empty when nothing matches
        

        Schema: `ListSipRealmReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        response = self.client.listSipRealm(
            {"realm": "%"},
            returnedTags=tagfilter,
        )["return"]
        if response:
            return response["sipRealm"]
        return []

    def get_sip_realm(self, **args):
        """
        Get a SIP Realm.
        :param realm: realm name (or uuid)
        :param uuid: realm uuid (or realm)
        :return: result dict
        

        Schema: `GetSipRealmReq`: optional `returnedTags`; one of `realm`, or `uuid`.
        """
        return self.client.getSipRealm(**args)["return"]["sipRealm"]

    def add_sip_realm(self, **args):
        """
        Add a SIP Realm.
        :param realm: realm name — required
        :param userid: user ID — required
        :param digestCredentials: credentials — required
        :return: result dict
        

        Schema: `sipRealm` -> `XSipRealm`: `realm` + `userid` + `digestCredentials`.
        """
        obj = self._build_object("addSipRealm", "sipRealm", args)
        return self.client.addSipRealm(obj)

    def update_sip_realm(self, **args):
        """
        Update a SIP Realm.
        :param realm: realm name (or uuid)
        :param uuid: realm uuid (or realm)
        :return: result dict
        

        Schema: `UpdateSipRealmReq`: optional `newRealm`, `userid`, `digestCredentials`; one of `uuid`, or `realm`.
        """
        return self.client.updateSipRealm(**args)

    def delete_sip_realm(self, **args):
        """
        Delete a SIP Realm.
        :param realm: realm name (or uuid)
        :param uuid: realm uuid (or realm)
        :return: result dict

        Note: ``userid`` is NOT part of the AXL removeSipRealm key; pass only
        ``realm`` or ``uuid``.
        

        Schema: `RemoveSipRealmReq`: one of `realm`, or `uuid`.
        """
        return self.client.removeSipRealm(**args)

    # ------------------------------------------------------------------ #
    # TvsCertificate — get / update / list (no add / delete in AXL)      #
    # ------------------------------------------------------------------ #

    def get_tvs_certificates(
        self,
        tagfilter={
            "subjectName": "",
            "issuerName": "",
            "serialNumber": "",
            "timeToLive": "",
            "ipv4Address": "",
        },
    ):
        """
        List all TVS Certificates.
        :param tagfilter: AXL returned tags to include
        :return: list of dicts, empty when nothing matches
        

        Schema: `ListTvsCertificateReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        response = self.client.listTvsCertificate(
            {"subjectName": "%"},
            returnedTags=tagfilter,
        )["return"]
        if response:
            return response["tvsCertificate"]
        return []

    def get_tvs_certificate(self, **args):
        """
        Get a TVS Certificate.
        :param uuid: certificate uuid
        :param issuerName: issuer name (alternative to uuid)
        :param serialNumber: serial number (alternative to uuid)
        :return: result dict
        

        Schema: `GetTvsCertificateReq`: optional `returnedTags`; one of `uuid`, or (`issuerName` + `serialNumber`).
        """
        return self.client.getTvsCertificate(**args)["return"]["tvsCertificate"]

    def update_tvs_certificate(self, **args):
        """
        Update a TVS Certificate.
        :param uuid: certificate uuid — required for update
        :return: result dict
        

        Schema: `UpdateTvsCertificateReq`: optional `timeToLive`; one of `uuid`, or (`issuerName` + `serialNumber`).
        """
        return self.client.updateTvsCertificate(**args)

    # ------------------------------------------------------------------ #
    # VpnGateway                                                          #
    # ------------------------------------------------------------------ #

    def get_vpn_gateways(
        self,
        tagfilter={"name": "", "description": "", "url": ""},
    ):
        """
        List all VPN Gateways.
        :param tagfilter: AXL returned tags to include
        :return: list of dicts, empty when nothing matches
        

        Schema: `ListVpnGatewayReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        response = self.client.listVpnGateway(
            {"name": "%"},
            returnedTags=tagfilter,
        )["return"]
        if response:
            return response["vpnGateway"]
        return []

    def get_vpn_gateway(self, **args):
        """
        Get a VPN Gateway.
        :param name: gateway name (or uuid)
        :param uuid: gateway uuid (or name)
        :return: result dict
        

        Schema: `GetVpnGatewayReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getVpnGateway(**args)["return"]["vpnGateway"]

    def add_vpn_gateway(self, **args):
        """
        Add a VPN Gateway.
        :param name: gateway name — required
        :param url: gateway URL — required
        :return: result dict
        

        Schema: `vpnGateway` -> `XVpnGateway`: `name` + `url` + `certificates`; optional `description`.
        """
        obj = self._build_object("addVpnGateway", "vpnGateway", args)
        return self.client.addVpnGateway(obj)

    def update_vpn_gateway(self, **args):
        """
        Update a VPN Gateway.
        :param name: gateway name (or uuid)
        :param uuid: gateway uuid (or name)
        :return: result dict
        

        Schema: `UpdateVpnGatewayReq`: optional `newName`, `description`, `url`, `certificates`.
        """
        return self.client.updateVpnGateway(**args)

    def delete_vpn_gateway(self, **args):
        """
        Delete a VPN Gateway.
        :param name: gateway name (or uuid)
        :param uuid: gateway uuid (or name)
        :return: result dict
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeVpnGateway(**args)

    # ------------------------------------------------------------------ #
    # VpnGroup                                                            #
    # ------------------------------------------------------------------ #

    def get_vpn_groups(
        self,
        tagfilter={"name": "", "description": ""},
    ):
        """
        List all VPN Groups.
        :param tagfilter: AXL returned tags to include
        :return: list of dicts, empty when nothing matches
        

        Schema: `ListVpnGroupReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        response = self.client.listVpnGroup(
            {"name": "%"},
            returnedTags=tagfilter,
        )["return"]
        if response:
            return response["vpnGroup"]
        return []

    def get_vpn_group(self, **args):
        """
        Get a VPN Group.
        :param name: group name (or uuid)
        :param uuid: group uuid (or name)
        :return: result dict
        

        Schema: `GetVpnGroupReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getVpnGroup(**args)["return"]["vpnGroup"]

    def add_vpn_group(self, **args):
        """
        Add a VPN Group.
        :param name: group name — required
        :return: result dict
        

        Schema: `vpnGroup` -> `XVpnGroup`: `name`; optional `description`, `vpnGateways`.
        """
        obj = self._build_object("addVpnGroup", "vpnGroup", args)
        return self.client.addVpnGroup(obj)

    def update_vpn_group(self, **args):
        """
        Update a VPN Group.
        :param name: group name (or uuid)
        :param uuid: group uuid (or name)
        :return: result dict
        

        Schema: `UpdateVpnGroupReq`: optional `newName`, `description`, `vpnGateways`.
        """
        return self.client.updateVpnGroup(**args)

    def delete_vpn_group(self, **args):
        """
        Delete a VPN Group.
        :param name: group name (or uuid)
        :param uuid: group uuid (or name)
        :return: result dict
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeVpnGroup(**args)

    # ------------------------------------------------------------------ #
    # VpnProfile                                                          #
    # ------------------------------------------------------------------ #

    def get_vpn_profiles(
        self,
        tagfilter={
            "name": "",
            "description": "",
            "autoNetworkDetection": "",
            "mtu": "",
            "failToConnect": "",
        },
    ):
        """
        List all VPN Profiles.
        :param tagfilter: AXL returned tags to include
        :return: list of dicts, empty when nothing matches
        

        Schema: `ListVpnProfileReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        response = self.client.listVpnProfile(
            {"name": "%"},
            returnedTags=tagfilter,
        )["return"]
        if response:
            return response["vpnProfile"]
        return []

    def get_vpn_profile(self, **args):
        """
        Get a VPN Profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: result dict
        

        Schema: `GetVpnProfileReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getVpnProfile(**args)["return"]["vpnProfile"]

    def add_vpn_profile(self, **args):
        """
        Add a VPN Profile.
        :param name: profile name — required
        :return: result dict
        

        Schema: `vpnProfile` -> `XVpnProfile`: `name`; optional `description`, `autoNetworkDetection`, `mtu`, `failToConnect`, `clientAuthentication`, `pwdPersistant` and 1 more.
        """
        obj = self._build_object("addVpnProfile", "vpnProfile", args)
        return self.client.addVpnProfile(obj)

    def update_vpn_profile(self, **args):
        """
        Update a VPN Profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: result dict
        

        Schema: `UpdateVpnProfileReq`: optional `newName`, `description`, `autoNetworkDetection`, `mtu`, `failToConnect`, `clientAuthentication` and 2 more.
        """
        return self.client.updateVpnProfile(**args)

    def delete_vpn_profile(self, **args):
        """
        Delete a VPN Profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: result dict
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeVpnProfile(**args)
