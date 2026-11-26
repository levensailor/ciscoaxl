"""
P0 Security Mixin — batch B4
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
"""


class P0Security:
    """Mixin providing security-profile, date/time-group, LDAP, versioning,
    registration-dynamic, and phone-lifecycle helpers."""

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
        """
        return self.client.updatePhoneSecurityProfile(**args)

    def delete_phone_security_profile(self, name="", uuid=""):
        """
        Delete a phone security profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: result dictionary
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
        """
        return self.client.updateSipProfile(**args)

    def delete_sip_profile(self, name="", uuid=""):
        """
        Delete a SIP profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: result dictionary
        """
        return self.client.removeSipProfile(**self._identify(name=name, uuid=uuid))

    def apply_sip_profile(self, name="", uuid=""):
        """
        Apply a SIP profile (push config to associated trunks/phones).
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: result dictionary
        """
        return self.client.applySipProfile(**self._identify(name=name, uuid=uuid))

    def restart_sip_profile(self, name="", uuid=""):
        """
        Restart devices associated with a SIP profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: result dictionary
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
        """
        return self.client.updateSipTrunkSecurityProfile(**args)

    def delete_sip_trunk_security_profile(self, name="", uuid=""):
        """
        Delete a SIP trunk security profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: result dictionary
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
        """
        return self.client.getDateTimeGroup(
            **self._identify(name=name, uuid=uuid)
        )["return"]["dateTimeGroup"]

    def get_date_time_groups(self, tagfilter={"name": "", "timeZone": ""}):
        """
        List date/time groups.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of date/time group dictionaries, empty when nothing matches
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
        """
        return self.client.updateDateTimeGroup(**args)

    def delete_date_time_group(self, name="", uuid=""):
        """
        Delete a date/time group.
        :param name: group name (or uuid)
        :param uuid: group uuid (or name)
        :return: result dictionary
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
        """
        return self.client.updateLdapDirectory(**args)

    def delete_ldap_directory(self, name="", uuid=""):
        """
        Delete an LDAP directory sync configuration.
        :param name: directory name (or uuid)
        :param uuid: directory uuid (or name)
        :return: result dictionary
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
        """
        return self.client.applyPhone(**self._identify(name=name, uuid=uuid))

    def reset_phone(self, name="", uuid=""):
        """
        Reset a phone (factory reset / full restart).
        :param name: device name (or uuid)
        :param uuid: device uuid (or name)
        :return: result dictionary
        """
        return self.client.resetPhone(**self._identify(name=name, uuid=uuid))

    def restart_phone(self, name="", uuid=""):
        """
        Restart a phone (soft restart, preserves config).
        :param name: device name (or uuid)
        :param uuid: device uuid (or name)
        :return: result dictionary
        """
        return self.client.restartPhone(**self._identify(name=name, uuid=uuid))

    def lock_phone(self, name="", uuid=""):
        """
        Lock a phone (Mobile Connect / MDM lock).
        :param name: device name (or uuid)
        :param uuid: device uuid (or name)
        :return: result dictionary
        """
        return self.client.lockPhone(**self._identify(name=name, uuid=uuid))

    def wipe_phone(self, name="", uuid=""):
        """
        Wipe a phone (Mobile Connect / MDM remote wipe).
        :param name: device name (or uuid)
        :param uuid: device uuid (or name)
        :return: result dictionary
        """
        return self.client.wipePhone(**self._identify(name=name, uuid=uuid))
