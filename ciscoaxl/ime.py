"""Intercompany Media Engine (IME) wrappers.

Adds Intercompany Media Engine (IME) methods.

Included objects (all ops from WSDL):
  - ImeClient              : add, get, list, update, remove  (name/uuid)
  - ImeE164Transformation  : add, get, list, update, remove  (name/uuid)
  - ImeEnrolledPattern     : add, get, list, update, remove  (pattern/uuid)
  - ImeEnrolledPatternGroup: add, get, list, update, remove  (name/uuid)
  - ImeExclusionNumber     : add, get, list, update, remove  (pattern/uuid)
  - ImeExclusionNumberGroup: add, get, list, update, remove  (name/uuid)
  - ImeFeatureConfig       : get, update                     (singleton)
  - ImeFirewall            : add, get, list, update, remove  (name/uuid)
  - ImeLearnedRoutes       : get, update, remove             (uuid/e164Did)
  - ImeRouteFilterElement  : add, get, list, update, remove  (name/uuid)
  - ImeRouteFilterGroup    : add, get, list, update, remove  (name/uuid)
  - ImeServer              : add, get, list, update, remove  (name/uuid)
"""


class ImeMixin:
    """Intercompany Media Engine (IME) wrappers."""

    # ------------------------------------------------------------------ #
    # ImeServer                                                            #
    # ------------------------------------------------------------------ #

    def add_ime_server(self, **args):
        """
        Add an IME server.

        :param name: server name — required
        :param description: description
        :param ipAddress: server IP or hostname — required
        :param port: port (1024–65535, default 5620)
        :param deviceSecurityMode: e.g. 'Authenticated'
        :param applicationUser: associated application user
        :param reconnectInterval: reconnect interval in seconds (60–600, default 120)
        :return: result dict (uuid)
        

        Schema: `imeServer` -> `XImeServer`: `name` + `ipAddress` + `applicationUser`; optional `description`, `port`, `deviceSecurityMode`, `reconnectInterval`.
        """
        obj = self._build_object("addImeServer", "imeServer", args)
        return self.client.addImeServer(imeServer=obj)

    def get_ime_server(self, name="", uuid=""):
        """
        Get an IME server.

        :param name: server name (or uuid)
        :param uuid: server uuid (or name)
        :return: imeServer dict
        

        Schema: `GetImeServerReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getImeServer(
            **self._identify(name=name, uuid=uuid)
        )["return"]["imeServer"]

    def get_ime_servers(self, tagfilter=None):
        """
        List IME servers.

        :param tagfilter: AXL returned tags, e.g. {'name': ''}
        :return: list of imeServer dicts, empty when nothing matches
        

        Schema: `ListImeServerReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listImeServer(
            {"name": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("imeServer") or []

    def update_ime_server(self, **args):
        """
        Update an IME server.

        :param name: server name (or uuid)
        :param uuid: server uuid (or name)
        :return: result dict
        

        Schema: `UpdateImeServerReq`: optional `newName`, `description`, `ipAddress`, `port`, `deviceSecurityMode`, `applicationUser` and 1 more.
        """
        return self.client.updateImeServer(**args)

    def delete_ime_server(self, name="", uuid=""):
        """
        Delete an IME server.

        :param name: server name (or uuid)
        :param uuid: server uuid (or name)
        :return: result dict
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeImeServer(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------ #
    # ImeRouteFilterGroup                                                  #
    # ------------------------------------------------------------------ #

    def add_ime_route_filter_group(self, **args):
        """
        Add an IME route filter group.

        :param name: group name — required
        :param description: description
        :param groupTrustSetting: boolean, trust this group's routes
        :return: result dict (uuid)
        

        Schema: `imeRouteFilterGroup` -> `XImeRouteFilterGroup`: `name`; optional `description`, `groupTrustSetting`.
        """
        obj = self._build_object("addImeRouteFilterGroup", "imeRouteFilterGroup", args)
        return self.client.addImeRouteFilterGroup(imeRouteFilterGroup=obj)

    def get_ime_route_filter_group(self, name="", uuid=""):
        """
        Get an IME route filter group.

        :param name: group name (or uuid)
        :param uuid: group uuid (or name)
        :return: imeRouteFilterGroup dict
        

        Schema: `GetImeRouteFilterGroupReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getImeRouteFilterGroup(
            **self._identify(name=name, uuid=uuid)
        )["return"]["imeRouteFilterGroup"]

    def get_ime_route_filter_groups(self, tagfilter=None):
        """
        List IME route filter groups.

        :param tagfilter: AXL returned tags, e.g. {'name': ''}
        :return: list of imeRouteFilterGroup dicts, empty when nothing matches
        

        Schema: `ListImeRouteFilterGroupReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listImeRouteFilterGroup(
            {"name": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("imeRouteFilterGroup") or []

    def update_ime_route_filter_group(self, **args):
        """
        Update an IME route filter group.

        :param name: group name (or uuid)
        :param uuid: group uuid (or name)
        :return: result dict
        

        Schema: `UpdateImeRouteFilterGroupReq`: optional `newName`, `description`, `groupTrustSetting`.
        """
        return self.client.updateImeRouteFilterGroup(**args)

    def delete_ime_route_filter_group(self, name="", uuid=""):
        """
        Delete an IME route filter group.

        :param name: group name (or uuid)
        :param uuid: group uuid (or name)
        :return: result dict
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeImeRouteFilterGroup(
            **self._identify(name=name, uuid=uuid)
        )

    # ------------------------------------------------------------------ #
    # ImeRouteFilterElement                                                #
    # ------------------------------------------------------------------ #

    def add_ime_route_filter_element(self, **args):
        """
        Add an IME route filter element.

        :param name: element name — required
        :param description: description
        :param elementType: e.g. 'Domain'
        :param imeRouteFilterGroupName: parent filter group name — required
        :return: result dict (uuid)
        

        Schema: `imeRouteFilterElement` -> `XImeRouteFilterElement`: `name` + `imeRouteFilterGroupName`; optional `description`, `elementType`.
        """
        obj = self._build_object(
            "addImeRouteFilterElement", "imeRouteFilterElement", args
        )
        return self.client.addImeRouteFilterElement(imeRouteFilterElement=obj)

    def get_ime_route_filter_element(self, name="", uuid=""):
        """
        Get an IME route filter element.

        :param name: element name (or uuid)
        :param uuid: element uuid (or name)
        :return: imeRouteFilterElement dict
        

        Schema: `GetImeRouteFilterElementReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getImeRouteFilterElement(
            **self._identify(name=name, uuid=uuid)
        )["return"]["imeRouteFilterElement"]

    def get_ime_route_filter_elements(self, tagfilter=None):
        """
        List IME route filter elements.

        :param tagfilter: AXL returned tags, e.g. {'name': ''}
        :return: list of imeRouteFilterElement dicts, empty when nothing matches
        

        Schema: `ListImeRouteFilterElementReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listImeRouteFilterElement(
            {"name": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("imeRouteFilterElement") or []

    def update_ime_route_filter_element(self, **args):
        """
        Update an IME route filter element.

        :param name: element name (or uuid)
        :param uuid: element uuid (or name)
        :return: result dict
        

        Schema: `UpdateImeRouteFilterElementReq`: optional `newName`, `description`, `elementType`, `imeRouteFilterGroupName`.
        """
        return self.client.updateImeRouteFilterElement(**args)

    def delete_ime_route_filter_element(self, name="", uuid=""):
        """
        Delete an IME route filter element.

        :param name: element name (or uuid)
        :param uuid: element uuid (or name)
        :return: result dict
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeImeRouteFilterElement(
            **self._identify(name=name, uuid=uuid)
        )

    # ------------------------------------------------------------------ #
    # ImeClient                                                            #
    # ------------------------------------------------------------------ #

    def add_ime_client(self, **args):
        """
        Add an IME client.

        :param name: client name — required
        :param description: description
        :param domain: IME domain — required
        :param isActivated: boolean, activate on creation (default False)
        :param sipTrunkName: associated SIP trunk — required
        :param primaryImeServerName: primary IME server — required
        :param secondaryImeServerName: secondary IME server
        :param learnedRouteFilterGroupName: learned route filter group
        :param exclusionNumberGroupName: exclusion number group
        :param firewallName: firewall name
        :return: result dict (uuid)
        

        Schema: `imeClient` -> `XImeClient`: `name` + `domain` + `sipTrunkName` + `primaryImeServerName`; optional `description`, `isActivated`, `secondaryImeServerName`, `learnedRouteFilterGroupName`, `exclusionNumberGroupName`, `firewallName` and 2 more.
        """
        obj = self._build_object("addImeClient", "imeClient", args)
        return self.client.addImeClient(imeClient=obj)

    def get_ime_client(self, name="", uuid=""):
        """
        Get an IME client.

        :param name: client name (or uuid)
        :param uuid: client uuid (or name)
        :return: imeClient dict
        

        Schema: `GetImeClientReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getImeClient(
            **self._identify(name=name, uuid=uuid)
        )["return"]["imeClient"]

    def get_ime_clients(self, tagfilter=None):
        """
        List IME clients.

        :param tagfilter: AXL returned tags, e.g. {'name': ''}
        :return: list of imeClient dicts, empty when nothing matches
        

        Schema: `ListImeClientReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listImeClient(
            {"name": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("imeClient") or []

    def update_ime_client(self, **args):
        """
        Update an IME client.

        :param name: client name (or uuid)
        :param uuid: client uuid (or name)
        :return: result dict
        

        Schema: `UpdateImeClientReq`: optional `newName`, `description`, `domain`, `isActivated`, `sipTrunkName`, `primaryImeServerName` and 6 more.
        """
        return self.client.updateImeClient(**args)

    def delete_ime_client(self, name="", uuid=""):
        """
        Delete an IME client.

        :param name: client name (or uuid)
        :param uuid: client uuid (or name)
        :return: result dict
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeImeClient(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------ #
    # ImeEnrolledPattern                                                   #
    # Identity: pattern/uuid (NOT name/uuid)                              #
    # ------------------------------------------------------------------ #

    def add_ime_enrolled_pattern(self, **args):
        """
        Add an IME enrolled pattern.

        :param pattern: E.164 pattern — required
        :param description: description
        :param imeEnrolledPatternGroupName: parent pattern group
        :return: result dict (uuid)
        

        Schema: `imeEnrolledPattern` -> `XImeEnrolledPattern`: `pattern` + `imeEnrolledPatternGroupName`; optional `description`.
        """
        obj = self._build_object("addImeEnrolledPattern", "imeEnrolledPattern", args)
        return self.client.addImeEnrolledPattern(imeEnrolledPattern=obj)

    def get_ime_enrolled_pattern(self, pattern="", uuid=""):
        """
        Get an IME enrolled pattern.

        :param pattern: E.164 pattern (or uuid)
        :param uuid: pattern uuid (or pattern)
        :return: imeEnrolledPattern dict
        

        Schema: `GetImeEnrolledPatternReq`: optional `returnedTags`; one of `pattern`, or `uuid`.
        """
        if uuid:
            identifier = {"uuid": uuid}
        elif pattern:
            identifier = {"pattern": pattern}
        else:
            raise ValueError("Provide either pattern or uuid")
        return self.client.getImeEnrolledPattern(**identifier)["return"][
            "imeEnrolledPattern"
        ]

    def get_ime_enrolled_patterns(self, tagfilter=None):
        """
        List IME enrolled patterns.

        :param tagfilter: AXL returned tags, e.g. {'pattern': ''}
        :return: list of imeEnrolledPattern dicts, empty when nothing matches
        

        Schema: `ListImeEnrolledPatternReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"pattern": ""}
        result = self.client.listImeEnrolledPattern(
            {"pattern": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("imeEnrolledPattern") or []

    def update_ime_enrolled_pattern(self, **args):
        """
        Update an IME enrolled pattern.

        :param pattern: E.164 pattern (or uuid)
        :param uuid: pattern uuid (or pattern)
        :return: result dict
        

        Schema: `UpdateImeEnrolledPatternReq`: optional `newPattern`, `description`, `imeEnrolledPatternGroupName`; one of `uuid`, or `pattern`.
        """
        return self.client.updateImeEnrolledPattern(**args)

    def delete_ime_enrolled_pattern(self, pattern="", uuid=""):
        """
        Delete an IME enrolled pattern.

        :param pattern: E.164 pattern (or uuid)
        :param uuid: pattern uuid (or pattern)
        :return: result dict
        

        Schema: `RemoveImeEnrolledPatternReq`: one of `pattern`, or `uuid`.
        """
        if uuid:
            identifier = {"uuid": uuid}
        elif pattern:
            identifier = {"pattern": pattern}
        else:
            raise ValueError("Provide either pattern or uuid")
        return self.client.removeImeEnrolledPattern(**identifier)

    # ------------------------------------------------------------------ #
    # ImeEnrolledPatternGroup                                              #
    # ------------------------------------------------------------------ #

    def add_ime_enrolled_pattern_group(self, **args):
        """
        Add an IME enrolled pattern group.

        :param name: group name — required
        :param description: description
        :param fallbackProfileName: fallback profile
        :param isPatternAllAlias: boolean, treat all patterns as aliases
        :return: result dict (uuid)
        

        Schema: `imeEnrolledPatternGroup` -> `XImeEnrolledPatternGroup`: `name`; optional `description`, `fallbackProfileName`, `isPatternAllAlias`.
        """
        obj = self._build_object(
            "addImeEnrolledPatternGroup", "imeEnrolledPatternGroup", args
        )
        return self.client.addImeEnrolledPatternGroup(imeEnrolledPatternGroup=obj)

    def get_ime_enrolled_pattern_group(self, name="", uuid=""):
        """
        Get an IME enrolled pattern group.

        :param name: group name (or uuid)
        :param uuid: group uuid (or name)
        :return: imeEnrolledPatternGroup dict
        

        Schema: `GetImeEnrolledPatternGroupReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getImeEnrolledPatternGroup(
            **self._identify(name=name, uuid=uuid)
        )["return"]["imeEnrolledPatternGroup"]

    def get_ime_enrolled_pattern_groups(self, tagfilter=None):
        """
        List IME enrolled pattern groups.

        :param tagfilter: AXL returned tags, e.g. {'name': ''}
        :return: list of imeEnrolledPatternGroup dicts, empty when nothing matches
        

        Schema: `ListImeEnrolledPatternGroupReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listImeEnrolledPatternGroup(
            {"name": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("imeEnrolledPatternGroup") or []

    def update_ime_enrolled_pattern_group(self, **args):
        """
        Update an IME enrolled pattern group.

        :param name: group name (or uuid)
        :param uuid: group uuid (or name)
        :return: result dict
        

        Schema: `UpdateImeEnrolledPatternGroupReq`: optional `newName`, `description`, `fallbackProfileName`, `isPatternAllAlias`.
        """
        return self.client.updateImeEnrolledPatternGroup(**args)

    def delete_ime_enrolled_pattern_group(self, name="", uuid=""):
        """
        Delete an IME enrolled pattern group.

        :param name: group name (or uuid)
        :param uuid: group uuid (or name)
        :return: result dict
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeImeEnrolledPatternGroup(
            **self._identify(name=name, uuid=uuid)
        )

    # ------------------------------------------------------------------ #
    # ImeExclusionNumber                                                   #
    # Identity: pattern/uuid (NOT name/uuid)                              #
    # ------------------------------------------------------------------ #

    def add_ime_exclusion_number(self, **args):
        """
        Add an IME exclusion number.

        :param pattern: E.164 exclusion pattern — required
        :param description: description
        :param imeExclusionNumberGroupName: parent exclusion number group — required
        :return: result dict (uuid)
        

        Schema: `imeExclusionNumber` -> `XImeExclusionNumber`: `pattern` + `imeExclusionNumberGroupName`; optional `description`.
        """
        obj = self._build_object("addImeExclusionNumber", "imeExclusionNumber", args)
        return self.client.addImeExclusionNumber(imeExclusionNumber=obj)

    def get_ime_exclusion_number(self, pattern="", uuid=""):
        """
        Get an IME exclusion number.

        :param pattern: E.164 exclusion pattern (or uuid)
        :param uuid: exclusion number uuid (or pattern)
        :return: imeExclusionNumber dict
        

        Schema: `GetImeExclusionNumberReq`: optional `returnedTags`; one of `pattern`, or `uuid`.
        """
        if uuid:
            identifier = {"uuid": uuid}
        elif pattern:
            identifier = {"pattern": pattern}
        else:
            raise ValueError("Provide either pattern or uuid")
        return self.client.getImeExclusionNumber(**identifier)["return"][
            "imeExclusionNumber"
        ]

    def get_ime_exclusion_numbers(self, tagfilter=None):
        """
        List IME exclusion numbers.

        :param tagfilter: AXL returned tags, e.g. {'pattern': ''}
        :return: list of imeExclusionNumber dicts, empty when nothing matches
        

        Schema: `ListImeExclusionNumberReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"pattern": ""}
        result = self.client.listImeExclusionNumber(
            {"pattern": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("imeExclusionNumber") or []

    def update_ime_exclusion_number(self, **args):
        """
        Update an IME exclusion number.

        :param pattern: E.164 exclusion pattern (or uuid)
        :param uuid: exclusion number uuid (or pattern)
        :return: result dict
        

        Schema: `UpdateImeExclusionNumberReq`: optional `newPattern`, `description`, `imeExclusionNumberGroupName`; one of `uuid`, or `pattern`.
        """
        return self.client.updateImeExclusionNumber(**args)

    def delete_ime_exclusion_number(self, pattern="", uuid=""):
        """
        Delete an IME exclusion number.

        :param pattern: E.164 exclusion pattern (or uuid)
        :param uuid: exclusion number uuid (or pattern)
        :return: result dict
        

        Schema: `RemoveImeExclusionNumberReq`: one of `pattern`, or `uuid`.
        """
        if uuid:
            identifier = {"uuid": uuid}
        elif pattern:
            identifier = {"pattern": pattern}
        else:
            raise ValueError("Provide either pattern or uuid")
        return self.client.removeImeExclusionNumber(**identifier)

    # ------------------------------------------------------------------ #
    # ImeExclusionNumberGroup                                              #
    # ------------------------------------------------------------------ #

    def add_ime_exclusion_number_group(self, **args):
        """
        Add an IME exclusion number group.

        :param name: group name — required
        :param description: description
        :return: result dict (uuid)
        

        Schema: `imeExclusionNumberGroup` -> `XImeExclusionNumberGroup`: `name`; optional `description`.
        """
        obj = self._build_object(
            "addImeExclusionNumberGroup", "imeExclusionNumberGroup", args
        )
        return self.client.addImeExclusionNumberGroup(imeExclusionNumberGroup=obj)

    def get_ime_exclusion_number_group(self, name="", uuid=""):
        """
        Get an IME exclusion number group.

        :param name: group name (or uuid)
        :param uuid: group uuid (or name)
        :return: imeExclusionNumberGroup dict
        

        Schema: `GetImeExclusionNumberGroupReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getImeExclusionNumberGroup(
            **self._identify(name=name, uuid=uuid)
        )["return"]["imeExclusionNumberGroup"]

    def get_ime_exclusion_number_groups(self, tagfilter=None):
        """
        List IME exclusion number groups.

        :param tagfilter: AXL returned tags, e.g. {'name': ''}
        :return: list of imeExclusionNumberGroup dicts, empty when nothing matches
        

        Schema: `ListImeExclusionNumberGroupReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listImeExclusionNumberGroup(
            {"name": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("imeExclusionNumberGroup") or []

    def update_ime_exclusion_number_group(self, **args):
        """
        Update an IME exclusion number group.

        :param name: group name (or uuid)
        :param uuid: group uuid (or name)
        :return: result dict
        

        Schema: `UpdateImeExclusionNumberGroupReq`: optional `newName`, `description`.
        """
        return self.client.updateImeExclusionNumberGroup(**args)

    def delete_ime_exclusion_number_group(self, name="", uuid=""):
        """
        Delete an IME exclusion number group.

        :param name: group name (or uuid)
        :param uuid: group uuid (or name)
        :return: result dict
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeImeExclusionNumberGroup(
            **self._identify(name=name, uuid=uuid)
        )

    # ------------------------------------------------------------------ #
    # ImeFirewall                                                          #
    # ------------------------------------------------------------------ #

    def add_ime_firewall(self, **args):
        """
        Add an IME firewall.

        :param name: firewall name — required
        :param description: description
        :param ipAddress: firewall IP or hostname — required
        :param port: port (1024–65535)
        :return: result dict (uuid)
        

        Schema: `imeFirewall` -> `XImeFirewall`: `name` + `ipAddress`; optional `description`, `port`.
        """
        obj = self._build_object("addImeFirewall", "imeFirewall", args)
        return self.client.addImeFirewall(imeFirewall=obj)

    def get_ime_firewall(self, name="", uuid=""):
        """
        Get an IME firewall.

        :param name: firewall name (or uuid)
        :param uuid: firewall uuid (or name)
        :return: imeFirewall dict
        

        Schema: `GetImeFirewallReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getImeFirewall(
            **self._identify(name=name, uuid=uuid)
        )["return"]["imeFirewall"]

    def get_ime_firewalls(self, tagfilter=None):
        """
        List IME firewalls.

        :param tagfilter: AXL returned tags, e.g. {'name': ''}
        :return: list of imeFirewall dicts, empty when nothing matches
        

        Schema: `ListImeFirewallReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listImeFirewall(
            {"name": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("imeFirewall") or []

    def update_ime_firewall(self, **args):
        """
        Update an IME firewall.

        :param name: firewall name (or uuid)
        :param uuid: firewall uuid (or name)
        :return: result dict
        

        Schema: `UpdateImeFirewallReq`: optional `newName`, `description`, `ipAddress`, `port`.
        """
        return self.client.updateImeFirewall(**args)

    def delete_ime_firewall(self, name="", uuid=""):
        """
        Delete an IME firewall.

        :param name: firewall name (or uuid)
        :param uuid: firewall uuid (or name)
        :return: result dict
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeImeFirewall(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------ #
    # ImeE164Transformation                                                #
    # ------------------------------------------------------------------ #

    def add_ime_e164_transformation(self, **args):
        """
        Add an IME E.164 transformation.

        :param name: transformation name — required
        :param description: description
        :param callingPartyPrefixDigits: prefix digits to add
        :param callingPartyStripDigits: prefix digits to strip
        :param callingPartyMask: mask to apply
        :return: result dict (uuid)
        

        Schema: `imeE164Transformation` -> `XImeE164Transformation`: `name`; optional `description`, `cgpnTransformationCssName`, `isCgpnPreTransformation`, `cdpnTransformationCssName`, `isCdpnPreTransformation`, `incomingCgpnTransformationProfileName` and 1 more.
        """
        obj = self._build_object(
            "addImeE164Transformation", "imeE164Transformation", args
        )
        return self.client.addImeE164Transformation(imeE164Transformation=obj)

    def get_ime_e164_transformation(self, name="", uuid=""):
        """
        Get an IME E.164 transformation.

        :param name: transformation name (or uuid)
        :param uuid: transformation uuid (or name)
        :return: imeE164Transformation dict
        

        Schema: `GetImeE164TransformationReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getImeE164Transformation(
            **self._identify(name=name, uuid=uuid)
        )["return"]["imeE164Transformation"]

    def get_ime_e164_transformations(self, tagfilter=None):
        """
        List IME E.164 transformations.

        :param tagfilter: AXL returned tags, e.g. {'name': ''}
        :return: list of imeE164Transformation dicts, empty when nothing matches
        

        Schema: `ListImeE164TransformationReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listImeE164Transformation(
            {"name": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("imeE164Transformation") or []

    def update_ime_e164_transformation(self, **args):
        """
        Update an IME E.164 transformation.

        :param name: transformation name (or uuid)
        :param uuid: transformation uuid (or name)
        :return: result dict
        

        Schema: `UpdateImeE164TransformationReq`: optional `newName`, `description`, `cgpnTransformationCssName`, `isCgpnPreTransformation`, `cdpnTransformationCssName`, `isCdpnPreTransformation` and 2 more.
        """
        return self.client.updateImeE164Transformation(**args)

    def delete_ime_e164_transformation(self, name="", uuid=""):
        """
        Delete an IME E.164 transformation.

        :param name: transformation name (or uuid)
        :param uuid: transformation uuid (or name)
        :return: result dict
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeImeE164Transformation(
            **self._identify(name=name, uuid=uuid)
        )

    # ------------------------------------------------------------------ #
    # ImeFeatureConfig (singleton — no name/uuid identity)                #
    # ------------------------------------------------------------------ #

    def get_ime_feature_config(self):
        """
        Get the IME feature configuration (singleton, cluster-wide).

        :return: imeFeatureConfig dict
        """
        return self.client.getImeFeatureConfig()["return"]["imeFeatureConfig"]

    def update_ime_feature_config(self, **args):
        """
        Update the IME feature configuration.

        :param preventImeCallsFromAnalogGateways: boolean
        :param enableIntraDomain: boolean
        :param allowMwiNotification: boolean
        :param trunkConnectionTimer: integer
        :param firewallConnectionTimer: integer
        :param firewallTranscationTimer: integer
        :param firewallIdleTimer: integer
        :param failedCallAttemptThreshold: integer
        :param callFallbackAttemptThreshold: integer
        :param qualityTimer: integer
        :param useImeForOutboundCalls: boolean
        :return: result dict
        

        Schema: `UpdateImeFeatureConfigReq`: optional `preventImeCallsFromAnalogGateways`, `enableIntraDomain`, `allowMwiNotification`, `trunkConnectionTimer`, `firewallConnectionTimer`, `firewallTranscationTimer` and 5 more.
        """
        return self.client.updateImeFeatureConfig(**args)

    # ------------------------------------------------------------------ #
    # ImeLearnedRoutes                                                     #
    # Identity: uuid/e164Did (NOT name/uuid)                              #
    # ------------------------------------------------------------------ #

    def get_ime_learned_routes(self, e164Did="", uuid=""):
        """
        Get an IME learned route.

        :param e164Did: E.164 DID (or uuid)
        :param uuid: learned route uuid (or e164Did)
        :return: imeLearnedRoutes dict
        

        Schema: `GetImeLearnedRoutesReq`: optional `returnedTags`; one of `uuid`, or `e164Did`.
        """
        if uuid:
            identifier = {"uuid": uuid}
        elif e164Did:
            identifier = {"e164Did": e164Did}
        else:
            raise ValueError("Provide either e164Did or uuid")
        return self.client.getImeLearnedRoutes(**identifier)["return"][
            "imeLearnedRoutes"
        ]

    def update_ime_learned_routes(self, **args):
        """
        Update an IME learned route.

        :param e164Did: E.164 DID (or uuid)
        :param uuid: learned route uuid (or e164Did)
        :param adminEnabled: boolean, enable/disable this route
        :return: result dict
        

        Schema: `UpdateImeLearnedRoutesReq`: optional `adminEnabled`; one of `uuid`, or `e164Did`.
        """
        return self.client.updateImeLearnedRoutes(**args)

    def delete_ime_learned_routes(self, e164Did="", uuid=""):
        """
        Delete an IME learned route.

        :param e164Did: E.164 DID (or uuid)
        :param uuid: learned route uuid (or e164Did)
        :return: result dict
        

        Schema: `RemoveImeLearnedRoutesReq`: one of `uuid`, or `e164Did`.
        """
        if uuid:
            identifier = {"uuid": uuid}
        elif e164Did:
            identifier = {"e164Did": e164Did}
        else:
            raise ValueError("Provide either e164Did or uuid")
        return self.client.removeImeLearnedRoutes(**identifier)
