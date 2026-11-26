"""
P2 Batch B3 — Presence extended + Security extras mixin
Entities:
  Presence / IM&P:
    AssignedPresenceServers   (list only)
    AssignedPresenceUsers     (list only)
    UnassignedPresenceServers (list only)
    UnassignedPresenceUsers   (list only)
    PresenceUser              (assign / unassign only)
    PresenceRedundancyGroup   (full CRUD)
    ExpresswayCConfiguration  (full CRUD)
    MraServiceDomain          (full CRUD)

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


class P2PresenceSec:
    """Mixin providing Presence-extended and security-extra AXL helpers."""

    # ------------------------------------------------------------------ #
    # AssignedPresenceServers — list only                                 #
    # ------------------------------------------------------------------ #

    def get_assigned_presence_servers(
        self,
        tagfilter={"name": "", "description": "", "nodeUsage": "", "numUsers": ""},
    ):
        """
        List all assigned Presence servers.
        :param tagfilter: AXL returned tags to include
        :return: list of dicts, empty when nothing matches
        """
        response = self.client.listAssignedPresenceServers(
            {"name": "%"},
            returnedTags=tagfilter,
        )["return"]
        if response:
            return response["assignedPresenceServers"]
        return []

    # ------------------------------------------------------------------ #
    # UnassignedPresenceServers — list only                               #
    # ------------------------------------------------------------------ #

    def get_unassigned_presence_servers(
        self,
        tagfilter={"name": "", "description": "", "nodeUsage": ""},
    ):
        """
        List all unassigned Presence servers.
        :param tagfilter: AXL returned tags to include
        :return: list of dicts, empty when nothing matches
        """
        response = self.client.listUnassignedPresenceServers(
            {"name": "%"},
            returnedTags=tagfilter,
        )["return"]
        if response:
            return response["unassignedPresenceServers"]
        return []

    # ------------------------------------------------------------------ #
    # AssignedPresenceUsers — list only                                   #
    # ------------------------------------------------------------------ #

    def get_assigned_presence_users(
        self,
        tagfilter={"userid": "", "server": "", "presenceRedundancyGroup": ""},
    ):
        """
        List all assigned Presence users.
        :param tagfilter: AXL returned tags to include
        :return: list of dicts, empty when nothing matches
        """
        response = self.client.listAssignedPresenceUsers(
            {"userid": "%"},
            returnedTags=tagfilter,
        )["return"]
        if response:
            return response["assignedPresenceUsers"]
        return []

    # ------------------------------------------------------------------ #
    # UnassignedPresenceUsers — list only                                 #
    # ------------------------------------------------------------------ #

    def get_unassigned_presence_users(
        self,
        tagfilter={"userid": ""},
    ):
        """
        List all unassigned Presence users.
        :param tagfilter: AXL returned tags to include
        :return: list of dicts, empty when nothing matches
        """
        response = self.client.listUnassignedPresenceUsers(
            {"userid": "%"},
            returnedTags=tagfilter,
        )["return"]
        if response:
            return response["unassignedPresenceUsers"]
        return []

    # ------------------------------------------------------------------ #
    # PresenceUser — assign / unassign only                               #
    # ------------------------------------------------------------------ #

    def assign_presence_user(self, userid, server):
        """
        Assign a user to a Presence server.
        :param userid: end-user ID to assign
        :param server: Presence server name to assign the user to
        :return: result dict
        """
        return self.client.assignPresenceUser(userid=userid, server=server)

    def unassign_presence_user(self, userid):
        """
        Unassign a user from their Presence server.
        :param userid: end-user ID to unassign
        :return: result dict
        """
        return self.client.unassignPresenceUser(userid=userid)

    # ------------------------------------------------------------------ #
    # PresenceRedundancyGroup                                             #
    # ------------------------------------------------------------------ #

    def get_presence_redundancy_groups(
        self,
        tagfilter={
            "name": "",
            "description": "",
            "server1": "",
            "server2": "",
            "haEnabled": "",
        },
    ):
        """
        List all Presence Redundancy Groups.
        :param tagfilter: AXL returned tags to include
        :return: list of dicts, empty when nothing matches
        """
        response = self.client.listPresenceRedundancyGroup(
            {"name": "%"},
            returnedTags=tagfilter,
        )["return"]
        if response:
            return response["presenceRedundancyGroup"]
        return []

    def get_presence_redundancy_group(self, **args):
        """
        Get a Presence Redundancy Group.
        :param name: group name (or uuid)
        :param uuid: group uuid (or name)
        :return: result dict
        """
        return self.client.getPresenceRedundancyGroup(**args)["return"][
            "presenceRedundancyGroup"
        ]

    def add_presence_redundancy_group(self, **args):
        """
        Add a Presence Redundancy Group.
        :param name: group name — required
        :return: result dict
        """
        obj = self._build_object(
            "addPresenceRedundancyGroup", "presenceRedundancyGroup", args
        )
        return self.client.addPresenceRedundancyGroup(obj)

    def update_presence_redundancy_group(self, **args):
        """
        Update a Presence Redundancy Group.
        :param name: group name (or uuid)
        :param uuid: group uuid (or name)
        :return: result dict
        """
        return self.client.updatePresenceRedundancyGroup(**args)

    def delete_presence_redundancy_group(self, **args):
        """
        Delete a Presence Redundancy Group.
        :param name: group name (or uuid)
        :param uuid: group uuid (or name)
        :return: result dict
        """
        return self.client.removePresenceRedundancyGroup(**args)

    # ------------------------------------------------------------------ #
    # ExpresswayCConfiguration                                            #
    # ------------------------------------------------------------------ #

    def get_expressway_c_configurations(
        self,
        tagfilter={
            "HostNameOrIP": "",
            "description": "",
            "X509SubjectNameorSubjectAlternateName": "",
        },
    ):
        """
        List all Expressway-C configurations.
        :param tagfilter: AXL returned tags to include
        :return: list of dicts, empty when nothing matches
        """
        response = self.client.listExpresswayCConfiguration(
            {"HostNameOrIP": "%"},
            returnedTags=tagfilter,
        )["return"]
        if response:
            return response["expresswayCConfiguration"]
        return []

    def get_expressway_c_configuration(self, **args):
        """
        Get an Expressway-C configuration.
        :param HostNameOrIP: host name or IP (or uuid)
        :param uuid: config uuid (or HostNameOrIP)
        :return: result dict
        """
        return self.client.getExpresswayCConfiguration(**args)["return"][
            "expresswayCConfiguration"
        ]

    def add_expressway_c_configuration(self, **args):
        """
        Add an Expressway-C configuration.
        :param HostNameOrIP: host name or IP — required
        :return: result dict
        """
        obj = self._build_object(
            "addExpresswayCConfiguration", "expresswayCConfiguration", args
        )
        return self.client.addExpresswayCConfiguration(obj)

    def update_expressway_c_configuration(self, **args):
        """
        Update an Expressway-C configuration.
        :param HostNameOrIP: host name or IP (or uuid)
        :param uuid: config uuid (or HostNameOrIP)
        :return: result dict
        """
        return self.client.updateExpresswayCConfiguration(**args)

    def delete_expressway_c_configuration(self, **args):
        """
        Delete an Expressway-C configuration.
        :param HostNameOrIP: host name or IP (or uuid)
        :param uuid: config uuid (or HostNameOrIP)
        :return: result dict
        """
        return self.client.removeExpresswayCConfiguration(**args)

    # ------------------------------------------------------------------ #
    # MraServiceDomain                                                    #
    # ------------------------------------------------------------------ #

    def get_mra_service_domains(
        self,
        tagfilter={"name": "", "isDefault": "", "serviceDomains": ""},
    ):
        """
        List all MRA Service Domains.
        :param tagfilter: AXL returned tags to include
        :return: list of dicts, empty when nothing matches
        """
        response = self.client.listMraServiceDomain(
            {"name": "%"},
            returnedTags=tagfilter,
        )["return"]
        if response:
            return response["mraServiceDomain"]
        return []

    def get_mra_service_domain(self, **args):
        """
        Get an MRA Service Domain.
        :param name: domain name (or uuid)
        :param uuid: domain uuid (or name)
        :return: result dict
        """
        return self.client.getMraServiceDomain(**args)["return"]["mraServiceDomain"]

    def add_mra_service_domain(self, **args):
        """
        Add an MRA Service Domain.
        :param name: domain name — required
        :return: result dict
        """
        obj = self._build_object("addMraServiceDomain", "mraServiceDomain", args)
        return self.client.addMraServiceDomain(obj)

    def update_mra_service_domain(self, **args):
        """
        Update an MRA Service Domain.
        :param name: domain name (or uuid)
        :param uuid: domain uuid (or name)
        :return: result dict
        """
        return self.client.updateMraServiceDomain(**args)

    def delete_mra_service_domain(self, **args):
        """
        Delete an MRA Service Domain.
        :param name: domain name (or uuid)
        :param uuid: domain uuid (or name)
        :return: result dict
        """
        return self.client.removeMraServiceDomain(**args)

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
        """
        return self.client.updateApplicationUserCapfProfile(**args)

    def delete_application_user_capf_profile(self, **args):
        """
        Delete an Application User CAPF Profile.
        :param instanceId: CAPF instance ID (or uuid)
        :param uuid: profile uuid (or instanceId)
        :return: result dict
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
        """
        obj = self._build_object("addEndUserCapfProfile", "endUserCapfProfile", args)
        return self.client.addEndUserCapfProfile(obj)

    def update_end_user_capf_profile(self, **args):
        """
        Update an End User CAPF Profile.
        :param instanceId: CAPF instance ID (or uuid)
        :param uuid: profile uuid (or instanceId)
        :return: result dict
        """
        return self.client.updateEndUserCapfProfile(**args)

    def delete_end_user_capf_profile(self, **args):
        """
        Delete an End User CAPF Profile.
        :param instanceId: CAPF instance ID (or uuid)
        :param uuid: profile uuid (or instanceId)
        :return: result dict
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
        """
        return self.client.getSecureConfig(**args)["return"]["secureConfig"]

    def update_secure_config(self, **args):
        """
        Update a Secure Config entry.
        :param name: config name (or uuid)
        :param uuid: config uuid (or name)
        :return: result dict
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
        """
        return self.client.getSipRealm(**args)["return"]["sipRealm"]

    def add_sip_realm(self, **args):
        """
        Add a SIP Realm.
        :param realm: realm name — required
        :param userid: user ID — required
        :param digestCredentials: credentials — required
        :return: result dict
        """
        obj = self._build_object("addSipRealm", "sipRealm", args)
        return self.client.addSipRealm(obj)

    def update_sip_realm(self, **args):
        """
        Update a SIP Realm.
        :param realm: realm name (or uuid)
        :param uuid: realm uuid (or realm)
        :return: result dict
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
        """
        return self.client.getTvsCertificate(**args)["return"]["tvsCertificate"]

    def update_tvs_certificate(self, **args):
        """
        Update a TVS Certificate.
        :param uuid: certificate uuid — required for update
        :return: result dict
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
        """
        return self.client.getVpnGateway(**args)["return"]["vpnGateway"]

    def add_vpn_gateway(self, **args):
        """
        Add a VPN Gateway.
        :param name: gateway name — required
        :param url: gateway URL — required
        :return: result dict
        """
        obj = self._build_object("addVpnGateway", "vpnGateway", args)
        return self.client.addVpnGateway(obj)

    def update_vpn_gateway(self, **args):
        """
        Update a VPN Gateway.
        :param name: gateway name (or uuid)
        :param uuid: gateway uuid (or name)
        :return: result dict
        """
        return self.client.updateVpnGateway(**args)

    def delete_vpn_gateway(self, **args):
        """
        Delete a VPN Gateway.
        :param name: gateway name (or uuid)
        :param uuid: gateway uuid (or name)
        :return: result dict
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
        """
        return self.client.getVpnGroup(**args)["return"]["vpnGroup"]

    def add_vpn_group(self, **args):
        """
        Add a VPN Group.
        :param name: group name — required
        :return: result dict
        """
        obj = self._build_object("addVpnGroup", "vpnGroup", args)
        return self.client.addVpnGroup(obj)

    def update_vpn_group(self, **args):
        """
        Update a VPN Group.
        :param name: group name (or uuid)
        :param uuid: group uuid (or name)
        :return: result dict
        """
        return self.client.updateVpnGroup(**args)

    def delete_vpn_group(self, **args):
        """
        Delete a VPN Group.
        :param name: group name (or uuid)
        :param uuid: group uuid (or name)
        :return: result dict
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
        """
        return self.client.getVpnProfile(**args)["return"]["vpnProfile"]

    def add_vpn_profile(self, **args):
        """
        Add a VPN Profile.
        :param name: profile name — required
        :return: result dict
        """
        obj = self._build_object("addVpnProfile", "vpnProfile", args)
        return self.client.addVpnProfile(obj)

    def update_vpn_profile(self, **args):
        """
        Update a VPN Profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: result dict
        """
        return self.client.updateVpnProfile(**args)

    def delete_vpn_profile(self, **args):
        """
        Delete a VPN Profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: result dict
        """
        return self.client.removeVpnProfile(**args)
