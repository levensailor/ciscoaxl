"""LBM, SNMP, DHCP, and wireless wrappers.

Adds LBM, SNMP, DHCP, and wireless (WLAN/WiFi) helpers.

Included groups:
  LBM:
    - LbmGroup              : add, get, list, update, remove
    - LbmHubGroup           : add, get, list, update, remove

  SNMP:
    - SNMPCommunityString   : add, get, update, remove
      (uses CommunityString / communityName identity — not standard NameAndGUID)
    - SNMPMIB2List          : get, update  (no add/remove/list in AXL)
    - SNMPUser              : add, get, update, remove
      (uses user / userName / User identity — vendor-specific element names)

  DHCP:
    - DhcpServer            : add, get, list, update, remove
      (get by uuid OR processNodeName)
    - DhcpSubnet            : add, get, list, update, remove
      (get by uuid OR dhcpServerName+subnetIpAddress)

  Wireless:
    - WLANProfile           : add, get, list, update, remove
    - WifiHotspot           : add, get, list, update, remove
    - WirelessAccessPointControllers : add, get, list, update, remove
    - WlanProfileGroup      : add, get, list, update, remove
"""


class NetworkMixin:
    """LBM, SNMP, DHCP, and wireless wrappers."""

    # ------------------------------------------------------------------ #
    # LbmGroup                                                             #
    # ------------------------------------------------------------------ #

    def add_lbm_group(self, **args):
        """
        Add an LBM group.
        :param name: group name — required
        :param Description: description
        :param ProcessnodeActive: active process node reference — required
        :param ProcessnodeStandby: standby process node reference
        :return: result dictionary (uuid)
        

        Schema: `lbmGroup` -> `XLbmGroup`: `name` + `ProcessnodeActive`; optional `Description`, `ProcessnodeStandby`.
        """
        obj = self._build_object("addLbmGroup", "lbmGroup", args)
        return self.client.addLbmGroup(lbmGroup=obj)

    def get_lbm_group(self, name="", uuid=""):
        """
        Get an LBM group.
        :param name: group name (or uuid)
        :param uuid: group uuid (or name)
        :return: lbmGroup dictionary
        

        Schema: `GetLbmGroupReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        if uuid:
            kwargs = {"uuid": uuid}
        elif name:
            kwargs = {"name": name}
        else:
            raise ValueError("Provide exactly one of name or uuid")
        return self.client.getLbmGroup(**kwargs)["return"]["lbmGroup"]

    def get_lbm_groups(
        self,
        search_name="%",
        tagfilter={"name": "", "Description": "", "ProcessnodeActive": ""},
    ):
        """
        List LBM groups.
        :param search_name: name search pattern, default '%' (all)
        :param tagfilter: AXL returned tags to include
        :return: list of lbmGroup dictionaries, empty when nothing matches
        

        Schema: `ListLbmGroupReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listLbmGroup(
            {"name": search_name}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("lbmGroup") or []

    def update_lbm_group(self, **args):
        """
        Update an LBM group.
        :param name: group name (or uuid) — required
        :param uuid: group uuid (or name)
        :param newName: new group name
        :param Description: new description
        :param ProcessnodeActive: new active process node
        :param ProcessnodeStandby: new standby process node
        :return: result dictionary
        

        Schema: `UpdateLbmGroupReq`: optional `newName`, `Description`, `ProcessnodeActive`, `ProcessnodeStandby`.
        """
        return self.client.updateLbmGroup(**args)

    def remove_lbm_group(self, name="", uuid=""):
        """
        Remove an LBM group.
        :param name: group name (or uuid)
        :param uuid: group uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        if uuid:
            kwargs = {"uuid": uuid}
        elif name:
            kwargs = {"name": name}
        else:
            raise ValueError("Provide exactly one of name or uuid")
        return self.client.removeLbmGroup(**kwargs)

    # ------------------------------------------------------------------ #
    # LbmHubGroup                                                          #
    # ------------------------------------------------------------------ #

    def add_lbm_hub_group(self, **args):
        """
        Add an LBM hub group.
        :param name: group name — required
        :param description: description
        :param member1: first member process node — required
        :param member2: second member process node
        :param member3: third member process node
        :return: result dictionary (uuid)
        

        Schema: `lbmHubGroup` -> `XLbmHubGroup`: `name` + `member1`; optional `description`, `member2`, `member3`, `members`.
        """
        obj = self._build_object("addLbmHubGroup", "lbmHubGroup", args)
        return self.client.addLbmHubGroup(lbmHubGroup=obj)

    def get_lbm_hub_group(self, name="", uuid=""):
        """
        Get an LBM hub group.
        :param name: group name (or uuid)
        :param uuid: group uuid (or name)
        :return: lbmHubGroup dictionary
        

        Schema: `GetLbmHubGroupReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        if uuid:
            kwargs = {"uuid": uuid}
        elif name:
            kwargs = {"name": name}
        else:
            raise ValueError("Provide exactly one of name or uuid")
        return self.client.getLbmHubGroup(**kwargs)["return"]["lbmHubGroup"]

    def get_lbm_hub_groups(
        self,
        search_name="%",
        tagfilter={"name": "", "description": "", "member1": ""},
    ):
        """
        List LBM hub groups.
        :param search_name: name search pattern, default '%' (all)
        :param tagfilter: AXL returned tags to include
        :return: list of lbmHubGroup dictionaries, empty when nothing matches
        

        Schema: `ListLbmHubGroupReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listLbmHubGroup(
            {"name": search_name}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("lbmHubGroup") or []

    def update_lbm_hub_group(self, **args):
        """
        Update an LBM hub group.
        :param name: group name (or uuid) — required
        :param uuid: group uuid (or name)
        :param newName: new group name
        :param description: new description
        :param member1: new first member
        :return: result dictionary
        

        Schema: `UpdateLbmHubGroupReq`: optional `newName`, `description`, `member1`, `member2`, `member3`, optional choice of (optional `removeMembers`, `addMembers`), or `members`.
        """
        return self.client.updateLbmHubGroup(**args)

    def remove_lbm_hub_group(self, name="", uuid=""):
        """
        Remove an LBM hub group.
        :param name: group name (or uuid)
        :param uuid: group uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        if uuid:
            kwargs = {"uuid": uuid}
        elif name:
            kwargs = {"name": name}
        else:
            raise ValueError("Provide exactly one of name or uuid")
        return self.client.removeLbmHubGroup(**kwargs)

    # ------------------------------------------------------------------ #
    # SNMPCommunityString                                                   #
    # AXL identity: add uses wrapper element "CommunityString",            #
    #               get uses top-level "communityName",                    #
    #               remove uses top-level "CommunityString" (string),      #
    #               update uses top-level "communityName" + "newValues".   #
    # ------------------------------------------------------------------ #

    def add_snmp_community_string(self, communityName, accessPrivilege, ArrayOfHosts):
        """
        Add an SNMP community string.
        :param communityName: community string name — required
        :param accessPrivilege: access privilege (e.g. 'ReadOnly') — required
        :param ArrayOfHosts: host restriction structure — required
        :return: result dictionary (message)
        

        Schema: `CommunityString` -> `RCommunityString`: `communityName` + `accessPrivilege` + `ArrayOfHosts`.
        """
        return self.client.addSNMPCommunityString(
            CommunityString={
                "communityName": communityName,
                "accessPrivilege": accessPrivilege,
                "ArrayOfHosts": ArrayOfHosts,
            }
        )

    def get_snmp_community_string(self, communityName):
        """
        Get an SNMP community string.
        :param communityName: community string name — required
        :return: SNMPCommunityString dictionary
        

        Schema: `GetSNMPCommunityStringReq`: `communityName`.
        """
        return self.client.getSNMPCommunityString(communityName=communityName)[
            "return"
        ]["SNMPCommunityString"]

    def update_snmp_community_string(self, communityName, **newValues):
        """
        Update an SNMP community string.
        :param communityName: community string name to update — required
        :param **newValues: fields to update passed as newValues wrapper
        :return: result dictionary (message)
        

        Schema: `UpdateSNMPCommunityStringReq`: `newValues`; optional `communityName`.
        """
        return self.client.updateSNMPCommunityString(
            communityName=communityName,
            newValues=newValues,
        )

    def remove_snmp_community_string(self, communityName):
        """
        Remove an SNMP community string.
        :param communityName: community string name — required
        :return: result dictionary (message)
        

        Schema: `RemoveSNMPCommunityStringReq`: `CommunityString`.
        """
        return self.client.removeSNMPCommunityString(CommunityString=communityName)

    # ------------------------------------------------------------------ #
    # SNMPMIB2List                                                          #
    # AXL: get-only by sysContact; update sets sysLocation + sysContact.   #
    # ------------------------------------------------------------------ #

    def get_snmp_mib2_list(self, sysContact):
        """
        Get the SNMP MIB2 list entry matching sysContact.
        :param sysContact: system contact string — required
        :return: SNMPMIB2List dictionary
        

        Schema: `GetSNMPMIB2ListReq`: `sysContact`.
        """
        return self.client.getSNMPMIB2List(sysContact=sysContact)["return"][
            "SNMPMIB2List"
        ]

    def update_snmp_mib2_list(self, sysLocation, sysContact):
        """
        Update the SNMP MIB2 list.
        :param sysLocation: system location string — required
        :param sysContact: system contact string — required
        :return: result dictionary (message)
        

        Schema: `UpdateSNMPMIB2ListReq`: `sysLocation` + `sysContact`.
        """
        return self.client.updateSNMPMIB2List(
            sysLocation=sysLocation, sysContact=sysContact
        )

    # ------------------------------------------------------------------ #
    # SNMPUser                                                              #
    # AXL identity: add/update wrap params in "user" element;              #
    #               get uses top-level "userName";                          #
    #               remove uses top-level "User".                           #
    # ------------------------------------------------------------------ #

    def add_snmp_user(self, **args):
        """
        Add an SNMP v3 user.
        :param userName: user name — required
        :param authRequired: auth required flag — required
        :param authPassword: authentication password — required
        :param authProtocol: authentication protocol — required
        :param privacyRequired: privacy required flag — required
        :param privacyPassword: privacy password — required
        :param privacyProtocol: privacy protocol — required
        :param accessPrivilege: access privilege — required
        :param ArrayOfHosts: host restriction structure — required
        :return: result dictionary (message)
        

        Schema: `user` -> `RSNMPUser`: `userName` + `authRequired` + `authPassword` + `authProtocol` + `privacyRequired` + `privacyPassword` + `privacyProtocol` + `accessPrivilege` + `ArrayOfHosts`.
        """
        return self.client.addSNMPUser(user=args)

    def get_snmp_user(self, userName):
        """
        Get an SNMP v3 user.
        :param userName: user name — required
        :return: SNMPUser dictionary
        

        Schema: `GetSNMPUserReq`: `userName`.
        """
        return self.client.getSNMPUser(userName=userName)["return"]["SNMPUser"]

    def update_snmp_user(self, **args):
        """
        Update an SNMP v3 user.
        :param userName: user name — required (identifies which user to update)
        :param authPassword: new authentication password
        :param privacyPassword: new privacy password
        :return: result dictionary (message)
        

        Schema: `user` -> `RSNMPUser`: `userName` + `authRequired` + `authPassword` + `authProtocol` + `privacyRequired` + `privacyPassword` + `privacyProtocol` + `accessPrivilege` + `ArrayOfHosts`.
        """
        return self.client.updateSNMPUser(user=args)

    def remove_snmp_user(self, userName):
        """
        Remove an SNMP v3 user.
        :param userName: user name — required
        :return: result dictionary (message)
        

        Schema: `RemoveSNMPUserReq`: `User`.
        """
        return self.client.removeSNMPUser(User=userName)

    # ------------------------------------------------------------------ #
    # DhcpServer                                                            #
    # AXL get/update: uuid OR processNodeName                               #
    # ------------------------------------------------------------------ #

    def add_dhcp_server(self, **args):
        """
        Add a DHCP server.
        :param processNodeName: associated process node — required
        :param arpCacheTimeout: ARP cache timeout — required (default 0)
        :param ipAddressLeaseTime: lease time — required (default 0)
        :param renewalTime: renewal time — required (default 0)
        :return: result dictionary (uuid)
        

        Schema: `dhcpServer` -> `XDhcpServer`: `processNodeName` + `arpCacheTimeout` + `ipAddressLeaseTime` + `renewalTime` + `rebindingTime`; optional `primaryDnsIpAddress`, `secondaryDnsIpAddress`, `primaryTftpServerIpAddress`, `secondaryTftpServerIpAddress`, `bootstrapServerIpAddress`, `domainName` and 1 more.
        """
        obj = self._build_object("addDhcpServer", "dhcpServer", args)
        return self.client.addDhcpServer(dhcpServer=obj)

    def get_dhcp_server(self, uuid="", processNodeName=""):
        """
        Get a DHCP server.
        :param uuid: server uuid (or processNodeName)
        :param processNodeName: process node name (or uuid)
        :return: dhcpServer dictionary
        

        Schema: `GetDhcpServerReq`: optional `returnedTags`; one of `processNodeName`, or `uuid`.
        """
        if uuid:
            kwargs = {"uuid": uuid}
        elif processNodeName:
            kwargs = {"processNodeName": processNodeName}
        else:
            raise ValueError("Provide exactly one of uuid or processNodeName")
        return self.client.getDhcpServer(**kwargs)["return"]["dhcpServer"]

    def get_dhcp_servers(
        self,
        search_processNodeName="%",
        tagfilter={"processNodeName": "", "primaryDnsIpAddress": ""},
    ):
        """
        List DHCP servers.
        :param search_processNodeName: process node name search pattern, default '%' (all)
        :param tagfilter: AXL returned tags to include
        :return: list of dhcpServer dictionaries, empty when nothing matches
        

        Schema: `ListDhcpServerReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listDhcpServer(
            {"processNodeName": search_processNodeName}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("dhcpServer") or []

    def update_dhcp_server(self, **args):
        """
        Update a DHCP server.
        :param uuid: server uuid (or processNodeName) — required
        :param processNodeName: process node name (or uuid)
        :param newProcessNodeName: new process node name
        :return: result dictionary
        

        Schema: `UpdateDhcpServerReq`: optional `newProcessNodeName`, `primaryDnsIpAddress`, `secondaryDnsIpAddress`, `primaryTftpServerIpAddress`, `secondaryTftpServerIpAddress`, `bootstrapServerIpAddress` and 6 more; one of `uuid`, or `processNodeName`.
        """
        return self.client.updateDhcpServer(**args)

    def remove_dhcp_server(self, uuid="", processNodeName=""):
        """
        Remove a DHCP server.
        :param uuid: server uuid (or processNodeName)
        :param processNodeName: process node name (or uuid)
        :return: result dictionary
        

        Schema: `RemoveDhcpServerReq`: one of `processNodeName`, or `uuid`.
        """
        if uuid:
            kwargs = {"uuid": uuid}
        elif processNodeName:
            kwargs = {"processNodeName": processNodeName}
        else:
            raise ValueError("Provide exactly one of uuid or processNodeName")
        return self.client.removeDhcpServer(**kwargs)

    # ------------------------------------------------------------------ #
    # DhcpSubnet                                                            #
    # AXL get: uuid OR (dhcpServerName + subnetIpAddress)                   #
    # ------------------------------------------------------------------ #

    def add_dhcp_subnet(self, **args):
        """
        Add a DHCP subnet.
        :param dhcpServerName: associated DHCP server — required
        :param subnetIpAddress: subnet IP address — required
        :param primaryStartIpAddress: start of primary IP range — required
        :param primaryEndIpAddress: end of primary IP range — required
        :param subnetMask: subnet mask — required
        :return: result dictionary (uuid)
        

        Schema: `dhcpSubnet` -> `XDhcpSubnet`: `dhcpServerName` + `subnetIpAddress` + `primaryStartIpAddress` + `primaryEndIpAddress` + `subnetMask`; optional `secondaryStartIpAddress`, `secondaryEndIpAddress`, `primaryRouterIpAddress`, `secondaryRouterIpAddress`, `domainName`, `primaryDnsIpAddress` and 9 more.
        """
        obj = self._build_object("addDhcpSubnet", "dhcpSubnet", args)
        return self.client.addDhcpSubnet(dhcpSubnet=obj)

    def get_dhcp_subnet(self, uuid="", dhcpServerName="", subnetIpAddress=""):
        """
        Get a DHCP subnet.
        :param uuid: subnet uuid
        :param dhcpServerName: DHCP server name (use with subnetIpAddress)
        :param subnetIpAddress: subnet IP address (use with dhcpServerName)
        :return: dhcpSubnet dictionary
        

        Schema: `GetDhcpSubnetReq`: optional `returnedTags`; one of `uuid`, or (`dhcpServerName` + `subnetIpAddress`).
        """
        if uuid:
            kwargs = {"uuid": uuid}
        elif dhcpServerName and subnetIpAddress:
            kwargs = {
                "dhcpServerName": dhcpServerName,
                "subnetIpAddress": subnetIpAddress,
            }
        else:
            raise ValueError(
                "Provide uuid, or both dhcpServerName and subnetIpAddress"
            )
        return self.client.getDhcpSubnet(**kwargs)["return"]["dhcpSubnet"]

    def get_dhcp_subnets(
        self,
        search_subnetIpAddress="%",
        tagfilter={"subnetIpAddress": "", "subnetMask": ""},
    ):
        """
        List DHCP subnets.
        AXL list criteria for DhcpSubnet does not include dhcpServerName; use
        subnetIpAddress for search filtering instead.
        :param search_subnetIpAddress: subnet IP address search pattern, default '%' (all)
        :param tagfilter: AXL returned tags to include
        :return: list of dhcpSubnet dictionaries, empty when nothing matches
        

        Schema: `ListDhcpSubnetReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listDhcpSubnet(
            {"subnetIpAddress": search_subnetIpAddress}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("dhcpSubnet") or []

    def update_dhcp_subnet(self, **args):
        """
        Update a DHCP subnet.
        :param uuid: subnet uuid (or dhcpServerName+subnetIpAddress) — required
        :param dhcpServerName: DHCP server name (use with subnetIpAddress)
        :param subnetIpAddress: subnet IP address (use with dhcpServerName)
        :return: result dictionary
        

        Schema: `UpdateDhcpSubnetReq`: optional `newDhcpServerName`, `newSubnetIpAddress`, `primaryStartIpAddress`, `primaryEndIpAddress`, `secondaryStartIpAddress`, `secondaryEndIpAddress` and 14 more; one of `uuid`, or (`dhcpServerName` + `subnetIpAddress`).
        """
        return self.client.updateDhcpSubnet(**args)

    def remove_dhcp_subnet(self, uuid="", dhcpServerName="", subnetIpAddress=""):
        """
        Remove a DHCP subnet.
        :param uuid: subnet uuid
        :param dhcpServerName: DHCP server name (use with subnetIpAddress)
        :param subnetIpAddress: subnet IP address (use with dhcpServerName)
        :return: result dictionary
        

        Schema: `RemoveDhcpSubnetReq`: one of `uuid`, or (`dhcpServerName` + `subnetIpAddress`).
        """
        if uuid:
            kwargs = {"uuid": uuid}
        elif dhcpServerName and subnetIpAddress:
            kwargs = {
                "dhcpServerName": dhcpServerName,
                "subnetIpAddress": subnetIpAddress,
            }
        else:
            raise ValueError(
                "Provide uuid, or both dhcpServerName and subnetIpAddress"
            )
        return self.client.removeDhcpSubnet(**kwargs)

    # ------------------------------------------------------------------ #
    # WLANProfile                                                           #
    # ------------------------------------------------------------------ #

    def add_wlan_profile(self, **args):
        """
        Add a WLAN profile.
        :param name: profile name — required
        :param ssid: SSID — required
        :param frequencyBand: frequency band (default 'Auto') — required
        :param userModifiable: user-modifiable flag (default 'Disallowed') — required
        :param authMethod: authentication method (default 'EAP-FAST') — required
        :return: result dictionary (uuid)
        

        Schema: `wLANProfile` -> `XWLANProfile`: `name` + `ssid` + `frequencyBand` + `userModifiable` + `authMethod`; optional `description`, `userName`, `password`, `pskPassphrase`, `wepKey`, `passwordDescription` and 1 more.
        """
        obj = self._build_object("addWLANProfile", "wLANProfile", args)
        return self.client.addWLANProfile(wLANProfile=obj)

    def get_wlan_profile(self, name="", uuid=""):
        """
        Get a WLAN profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: wLANProfile dictionary
        

        Schema: `GetWLANProfileReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        if uuid:
            kwargs = {"uuid": uuid}
        elif name:
            kwargs = {"name": name}
        else:
            raise ValueError("Provide exactly one of name or uuid")
        return self.client.getWLANProfile(**kwargs)["return"]["wLANProfile"]

    def get_wlan_profiles(
        self,
        search_name="%",
        tagfilter={"name": "", "description": "", "ssid": ""},
    ):
        """
        List WLAN profiles.
        :param search_name: name search pattern, default '%' (all)
        :param tagfilter: AXL returned tags to include
        :return: list of wLANProfile dictionaries, empty when nothing matches
        

        Schema: `ListWLANProfileReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listWLANProfile(
            {"name": search_name}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("wLANProfile") or []

    def update_wlan_profile(self, **args):
        """
        Update a WLAN profile.
        :param name: profile name (or uuid) — required
        :param uuid: profile uuid (or name)
        :param newName: new profile name
        :param ssid: new SSID
        :return: result dictionary
        

        Schema: `UpdateWLANProfileReq`: optional `newName`, `description`, `ssid`, `frequencyBand`, `userModifiable`, `authMethod` and 6 more.
        """
        return self.client.updateWLANProfile(**args)

    def remove_wlan_profile(self, name="", uuid=""):
        """
        Remove a WLAN profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        if uuid:
            kwargs = {"uuid": uuid}
        elif name:
            kwargs = {"name": name}
        else:
            raise ValueError("Provide exactly one of name or uuid")
        return self.client.removeWLANProfile(**kwargs)

    # ------------------------------------------------------------------ #
    # WifiHotspot                                                           #
    # ------------------------------------------------------------------ #

    def add_wifi_hotspot(self, **args):
        """
        Add a WiFi hotspot.
        :param name: hotspot name — required
        :param ssidPrefix: SSID prefix — required
        :param frequencyBand: frequency band (default 'Auto') — required
        :param authenticationMethod: authentication method (default 'None') — required
        :return: result dictionary (uuid)
        

        Schema: `wifiHotspot` -> `XWifiHotspot`: `name` + `ssidPrefix` + `frequencyBand` + `authenticationMethod`; optional `description`, `userModifiable`, `hostName`, `port`, `sharedSecret`, `pskPassPhrase` and 2 more.
        """
        obj = self._build_object("addWifiHotspot", "wifiHotspot", args)
        return self.client.addWifiHotspot(wifiHotspot=obj)

    def get_wifi_hotspot(self, name="", uuid=""):
        """
        Get a WiFi hotspot.
        :param name: hotspot name (or uuid)
        :param uuid: hotspot uuid (or name)
        :return: wifiHotspot dictionary
        

        Schema: `GetWifiHotspotReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        if uuid:
            kwargs = {"uuid": uuid}
        elif name:
            kwargs = {"name": name}
        else:
            raise ValueError("Provide exactly one of name or uuid")
        return self.client.getWifiHotspot(**kwargs)["return"]["wifiHotspot"]

    def get_wifi_hotspots(
        self,
        search_name="%",
        tagfilter={"name": "", "description": "", "ssidPrefix": ""},
    ):
        """
        List WiFi hotspots.
        :param search_name: name search pattern, default '%' (all)
        :param tagfilter: AXL returned tags to include
        :return: list of wifiHotspot dictionaries, empty when nothing matches
        

        Schema: `ListWifiHotspotReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listWifiHotspot(
            {"name": search_name}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("wifiHotspot") or []

    def update_wifi_hotspot(self, **args):
        """
        Update a WiFi hotspot.
        :param name: hotspot name (or uuid) — required
        :param uuid: hotspot uuid (or name)
        :param newName: new hotspot name
        :param ssidPrefix: new SSID prefix
        :return: result dictionary
        

        Schema: `UpdateWifiHotspotReq`: optional `newName`, `description`, `ssidPrefix`, `userModifiable`, `frequencyBand`, `authenticationMethod` and 6 more.
        """
        return self.client.updateWifiHotspot(**args)

    def remove_wifi_hotspot(self, name="", uuid=""):
        """
        Remove a WiFi hotspot.
        :param name: hotspot name (or uuid)
        :param uuid: hotspot uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        if uuid:
            kwargs = {"uuid": uuid}
        elif name:
            kwargs = {"name": name}
        else:
            raise ValueError("Provide exactly one of name or uuid")
        return self.client.removeWifiHotspot(**kwargs)

    # ------------------------------------------------------------------ #
    # WirelessAccessPointControllers                                        #
    # ------------------------------------------------------------------ #

    def add_wireless_access_point_controllers(self, **args):
        """
        Add a wireless access point controller.
        :param name: controller name — required
        :param snmpUserIdOrCommunityString: SNMP community string or user ID — required
        :param resyncInterval: resync interval in minutes (default 32) — required
        :return: result dictionary (uuid)
        

        Schema: `wirelessAccessPointControllers` -> `XWirelessAccessPointControllers`: `name` + `snmpUserIdOrCommunityString` + `resyncInterval`; optional `description`, `snmpVersion`, `snmpAuthenticationProtocol`, `snmpAuthenticationPassword`, `snmpPrivacyProtocol`, `snmpPrivacyPassword` and 3 more.
        """
        obj = self._build_object(
            "addWirelessAccessPointControllers",
            "wirelessAccessPointControllers",
            args,
        )
        return self.client.addWirelessAccessPointControllers(
            wirelessAccessPointControllers=obj
        )

    def get_wireless_access_point_controllers(self, name="", uuid=""):
        """
        Get a wireless access point controller.
        :param name: controller name (or uuid)
        :param uuid: controller uuid (or name)
        :return: wirelessAccessPointControllers dictionary
        

        Schema: `GetWirelessAccessPointControllersReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        if uuid:
            kwargs = {"uuid": uuid}
        elif name:
            kwargs = {"name": name}
        else:
            raise ValueError("Provide exactly one of name or uuid")
        return self.client.getWirelessAccessPointControllers(**kwargs)["return"][
            "wirelessAccessPointControllers"
        ]

    def get_wireless_access_point_controllers_list(
        self,
        search_name="%",
        tagfilter={"name": "", "description": "", "snmpUserIdOrCommunityString": ""},
    ):
        """
        List wireless access point controllers.
        :param search_name: name search pattern, default '%' (all)
        :param tagfilter: AXL returned tags to include
        :return: list of wirelessAccessPointControllers dictionaries, empty when nothing matches
        

        Schema: `ListWirelessAccessPointControllersReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listWirelessAccessPointControllers(
            {"name": search_name}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("wirelessAccessPointControllers") or []

    def update_wireless_access_point_controllers(self, **args):
        """
        Update a wireless access point controller.
        :param name: controller name (or uuid) — required
        :param uuid: controller uuid (or name)
        :param newName: new controller name
        :param snmpUserIdOrCommunityString: new SNMP community/user
        :return: result dictionary
        

        Schema: `UpdateWirelessAccessPointControllersReq`: optional `newName`, `description`, `snmpVersion`, `snmpUserIdOrCommunityString`, `snmpAuthenticationProtocol`, `snmpAuthenticationPassword` and 6 more.
        """
        return self.client.updateWirelessAccessPointControllers(**args)

    def remove_wireless_access_point_controllers(self, name="", uuid=""):
        """
        Remove a wireless access point controller.
        :param name: controller name (or uuid)
        :param uuid: controller uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        if uuid:
            kwargs = {"uuid": uuid}
        elif name:
            kwargs = {"name": name}
        else:
            raise ValueError("Provide exactly one of name or uuid")
        return self.client.removeWirelessAccessPointControllers(**kwargs)

    # ------------------------------------------------------------------ #
    # WlanProfileGroup                                                      #
    # ------------------------------------------------------------------ #

    def add_wlan_profile_group(self, **args):
        """
        Add a WLAN profile group.
        :param name: group name — required
        :param description: description — required
        :param members: member WLAN profiles
        :return: result dictionary (uuid)
        

        Schema: `wlanProfileGroup` -> `XWlanProfileGroup`: `name` + `description`; optional `members`.
        """
        obj = self._build_object("addWlanProfileGroup", "wlanProfileGroup", args)
        return self.client.addWlanProfileGroup(wlanProfileGroup=obj)

    def get_wlan_profile_group(self, name="", uuid=""):
        """
        Get a WLAN profile group.
        :param name: group name (or uuid)
        :param uuid: group uuid (or name)
        :return: wlanProfileGroup dictionary
        

        Schema: `GetWlanProfileGroupReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        if uuid:
            kwargs = {"uuid": uuid}
        elif name:
            kwargs = {"name": name}
        else:
            raise ValueError("Provide exactly one of name or uuid")
        return self.client.getWlanProfileGroup(**kwargs)["return"]["wlanProfileGroup"]

    def get_wlan_profile_groups(
        self,
        search_name="%",
        tagfilter={"name": "", "description": ""},
    ):
        """
        List WLAN profile groups.
        :param search_name: name search pattern, default '%' (all)
        :param tagfilter: AXL returned tags to include
        :return: list of wlanProfileGroup dictionaries, empty when nothing matches
        

        Schema: `ListWlanProfileGroupReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listWlanProfileGroup(
            {"name": search_name}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("wlanProfileGroup") or []

    def update_wlan_profile_group(self, **args):
        """
        Update a WLAN profile group.
        :param name: group name (or uuid) — required
        :param uuid: group uuid (or name)
        :param newName: new group name
        :param description: new description
        :return: result dictionary
        

        Schema: `UpdateWlanProfileGroupReq`: optional `newName`, `description`, optional choice of (optional `removeMembers`, `addMembers`), or `members`.
        """
        return self.client.updateWlanProfileGroup(**args)

    def remove_wlan_profile_group(self, name="", uuid=""):
        """
        Remove a WLAN profile group.
        :param name: group name (or uuid)
        :param uuid: group uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        if uuid:
            kwargs = {"uuid": uuid}
        elif name:
            kwargs = {"name": name}
        else:
            raise ValueError("Provide exactly one of name or uuid")
        return self.client.removeWlanProfileGroup(**kwargs)
