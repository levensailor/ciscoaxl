"""Dial-plan wrappers.

Covered entities:
  AarGroup, AarGroupMatrix (update only), ApplicationDialRules,
  DirectedCallPark, DirectoryLookupDialRules, LocalRouteGroup,
  RouteFilter, SipDialRules, SipRoutePattern

Schema notes (15.0):
  - DirectedCallPark identity: pattern + routePartitionName (optional) OR uuid
    list searchCriteria uses 'pattern' (not 'name')
  - SipRoutePattern identity: pattern + routePartitionName (BOTH required) OR uuid
    list searchCriteria uses 'pattern' (not 'name')
  - AarGroupMatrix: no list/get/add/remove; update identifies by
    aarGroupFromName + aarGroupToName OR uuid
  - All remaining objects use name/uuid identity and name list search
"""


class DialPlanMixin:
    """Dial-plan wrappers."""

    # ------------------------------------------------------------------
    # AarGroup
    # ------------------------------------------------------------------

    def add_aar_group(self, **args):
        """
        Add an AAR group.
        :param name: AAR group name - required
        :return: result dictionary
        

        Schema: `aarGroup` -> `XAarGroup`: `name`.
        """
        return self.client.addAarGroup(
            self._build_object("addAarGroup", "aarGroup", args)
        )

    def get_aar_group(self, **args):
        """
        Get a single AAR group.
        :param name: AAR group name
        :param uuid: AAR group uuid
        :return: aarGroup dictionary
        

        Schema: `GetAarGroupReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getAarGroup(**args)["return"]["aarGroup"]

    def get_aar_groups(self, tagfilter=None):
        """
        List all AAR groups.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of aarGroup dictionaries, empty when nothing matches
        

        Schema: `ListAarGroupReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listAarGroup(
            {"name": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("aarGroup") or []

    def update_aar_group(self, **args):
        """
        Update an AAR group.
        :param name: AAR group name (or uuid)
        :param uuid: AAR group uuid (or name)
        :return: result dictionary
        

        Schema: `UpdateAarGroupReq`: optional `newName`.
        """
        return self.client.updateAarGroup(**args)

    def delete_aar_group(self, name="", uuid=""):
        """
        Delete an AAR group by name or uuid.
        :param name: AAR group name
        :param uuid: AAR group uuid
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeAarGroup(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------
    # AarGroupMatrix  (update only — no add/get/list/remove in schema)
    # ------------------------------------------------------------------

    def update_aar_group_matrix(self, **args):
        """
        Update an AAR group matrix entry.
        Identify by aarGroupFromName + aarGroupToName OR uuid.
        :param aarGroupFromName: source AAR group name
        :param aarGroupToName: destination AAR group name
        :param uuid: matrix entry uuid
        :param prefixDigit: new prefix digit value
        :return: result dictionary
        

        Schema: `UpdateAarGroupMatrixReq`: optional `prefixDigit`; one of `uuid`, or (`aarGroupFromName` + `aarGroupToName`).
        """
        return self.client.updateAarGroupMatrix(**args)

    # ------------------------------------------------------------------
    # ApplicationDialRules
    # ------------------------------------------------------------------

    def add_application_dial_rules(self, **args):
        """
        Add an application dial rule.
        :param name: rule name - required
        :return: result dictionary
        

        Schema: `applicationDialRules` -> `XApplicationDialRules`: `name` + `numberOfDigits` + `digitsToBeRemoved` + `priority`; optional `description`, `numberBeginWith`, `prefixPattern`.
        """
        return self.client.addApplicationDialRules(
            self._build_object("addApplicationDialRules", "applicationDialRules", args)
        )

    def get_application_dial_rules(self, **args):
        """
        Get a single application dial rule.
        :param name: rule name
        :param uuid: rule uuid
        :return: applicationDialRules dictionary
        

        Schema: `GetApplicationDialRulesReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getApplicationDialRules(**args)["return"][
            "applicationDialRules"
        ]

    def get_application_dial_rules_list(self, tagfilter=None):
        """
        List all application dial rules.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of applicationDialRules dictionaries, empty when nothing matches
        

        Schema: `ListApplicationDialRulesReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listApplicationDialRules(
            {"name": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("applicationDialRules") or []

    def update_application_dial_rules(self, **args):
        """
        Update an application dial rule.
        :param name: rule name (or uuid)
        :param uuid: rule uuid (or name)
        :return: result dictionary
        

        Schema: `UpdateApplicationDialRulesReq`: optional `newName`, `description`, `numberBeginWith`, `numberOfDigits`, `digitsToBeRemoved`, `prefixPattern` and 1 more.
        """
        return self.client.updateApplicationDialRules(**args)

    def delete_application_dial_rules(self, name="", uuid=""):
        """
        Delete an application dial rule by name or uuid.
        :param name: rule name
        :param uuid: rule uuid
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeApplicationDialRules(
            **self._identify(name=name, uuid=uuid)
        )

    # ------------------------------------------------------------------
    # DirectedCallPark
    # Schema identity: pattern + routePartitionName (optional) OR uuid
    # List search: pattern
    # ------------------------------------------------------------------

    def add_directed_call_park(self, **args):
        """
        Add a directed call park.
        :param pattern: park code pattern - required
        :param retrievalPrefix: retrieval prefix - required
        :return: result dictionary
        

        Schema: `directedCallPark` -> `XDirectedCallPark`: `pattern` + `retrievalPrefix`; optional `description`, `routePartitionName`, `reversionPattern`, `revertCssName`.
        """
        return self.client.addDirectedCallPark(
            self._build_object("addDirectedCallPark", "directedCallPark", args)
        )

    def get_directed_call_park(self, **args):
        """
        Get a single directed call park.
        :param pattern: park code pattern
        :param routePartitionName: partition name (optional with pattern)
        :param uuid: directed call park uuid
        :return: directedCallPark dictionary
        

        Schema: `GetDirectedCallParkReq`: optional `returnedTags`; one of `uuid`, or (`pattern`; optional `routePartitionName`).
        """
        return self.client.getDirectedCallPark(**args)["return"]["directedCallPark"]

    def get_directed_call_parks(self, tagfilter=None):
        """
        List all directed call parks.
        List searchCriteria uses 'pattern' (not 'name').
        :param tagfilter: AXL returned tags to include, e.g. {'pattern': ''}
        :return: list of directedCallPark dictionaries, empty when nothing matches
        

        Schema: `ListDirectedCallParkReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"pattern": ""}
        result = self.client.listDirectedCallPark(
            {"pattern": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("directedCallPark") or []

    def update_directed_call_park(self, **args):
        """
        Update a directed call park.
        :param pattern: park code pattern (or uuid)
        :param routePartitionName: partition (optional with pattern)
        :param uuid: directed call park uuid (or pattern)
        :return: result dictionary
        

        Schema: `UpdateDirectedCallParkReq`: optional `newPattern`, `description`, `newRoutePartitionName`, `retrievalPrefix`, `reversionPattern`, `revertCssName`; one of `uuid`, or (`pattern`; optional `routePartitionName`).
        """
        return self.client.updateDirectedCallPark(**args)

    def delete_directed_call_park(self, **args):
        """
        Delete a directed call park.
        :param pattern: park code pattern
        :param routePartitionName: partition name (optional with pattern)
        :param uuid: directed call park uuid
        :return: result dictionary
        

        Schema: `RemoveDirectedCallParkReq`: one of `uuid`, or (`pattern`; optional `routePartitionName`).
        """
        return self.client.removeDirectedCallPark(**args)

    def apply_directed_call_park(self, **args):
        """
        Apply a directed call park.
        :param pattern: park code pattern
        :param routePartitionName: partition name (optional with pattern)
        :param uuid: directed call park uuid
        :return: result dictionary
        

        Schema: `ApplyDirectedCallParkReq`: one of `uuid`, or (`pattern`; optional `routePartitionName`).
        """
        return self.client.applyDirectedCallPark(**args)

    def reset_directed_call_park(self, **args):
        """
        Reset a directed call park.
        :param pattern: park code pattern
        :param routePartitionName: partition name (optional with pattern)
        :param uuid: directed call park uuid
        :return: result dictionary
        

        Schema: `ResetDirectedCallParkReq`: one of `uuid`, or (`pattern`; optional `routePartitionName`).
        """
        return self.client.resetDirectedCallPark(**args)

    # ------------------------------------------------------------------
    # DirectoryLookupDialRules
    # ------------------------------------------------------------------

    def add_directory_lookup_dial_rules(self, **args):
        """
        Add a directory lookup dial rule.
        :param name: rule name - required
        :return: result dictionary
        

        Schema: `directoryLookupDialRules` -> `XDirectoryLookupDialRules`: `name` + `numberOfDigits` + `digitsToBeRemoved` + `priority`; optional `description`, `numberBeginWith`, `prefixPattern`.
        """
        return self.client.addDirectoryLookupDialRules(
            self._build_object(
                "addDirectoryLookupDialRules", "directoryLookupDialRules", args
            )
        )

    def get_directory_lookup_dial_rules(self, **args):
        """
        Get a single directory lookup dial rule.
        :param name: rule name
        :param uuid: rule uuid
        :return: directoryLookupDialRules dictionary
        

        Schema: `GetDirectoryLookupDialRulesReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getDirectoryLookupDialRules(**args)["return"][
            "directoryLookupDialRules"
        ]

    def get_directory_lookup_dial_rules_list(self, tagfilter=None):
        """
        List all directory lookup dial rules.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of directoryLookupDialRules dictionaries, empty when nothing matches
        

        Schema: `ListDirectoryLookupDialRulesReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listDirectoryLookupDialRules(
            {"name": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("directoryLookupDialRules") or []

    def update_directory_lookup_dial_rules(self, **args):
        """
        Update a directory lookup dial rule.
        :param name: rule name (or uuid)
        :param uuid: rule uuid (or name)
        :return: result dictionary
        

        Schema: `UpdateDirectoryLookupDialRulesReq`: optional `newName`, `description`, `numberBeginWith`, `numberOfDigits`, `digitsToBeRemoved`, `prefixPattern` and 1 more.
        """
        return self.client.updateDirectoryLookupDialRules(**args)

    def delete_directory_lookup_dial_rules(self, name="", uuid=""):
        """
        Delete a directory lookup dial rule by name or uuid.
        :param name: rule name
        :param uuid: rule uuid
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeDirectoryLookupDialRules(
            **self._identify(name=name, uuid=uuid)
        )

    # ------------------------------------------------------------------
    # LocalRouteGroup
    # ------------------------------------------------------------------

    def add_local_route_group(self, **args):
        """
        Add a local route group.
        :param name: local route group name - required
        :return: result dictionary
        

        Schema: `localRouteGroup` -> `XLocalRouteGroup`: optional `name`, `description`.
        """
        return self.client.addLocalRouteGroup(
            self._build_object("addLocalRouteGroup", "localRouteGroup", args)
        )

    def get_local_route_group(self, **args):
        """
        Get a single local route group.
        :param name: local route group name
        :param uuid: local route group uuid
        :return: localRouteGroup dictionary
        

        Schema: `GetLocalRouteGroupReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getLocalRouteGroup(**args)["return"]["localRouteGroup"]

    def get_local_route_groups(self, tagfilter=None):
        """
        List all local route groups.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of localRouteGroup dictionaries, empty when nothing matches
        

        Schema: `ListLocalRouteGroupReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listLocalRouteGroup(
            {"name": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("localRouteGroup") or []

    def update_local_route_group(self, **args):
        """
        Update a local route group.
        UpdateLocalRouteGroupReq wraps all fields under a 'localRouteGroup' element.
        :param name: local route group name (or uuid)
        :param uuid: local route group uuid (or name)
        :param newName: new name
        :param newDescription: new description
        :return: result dictionary
        

        Schema: `UpdateLocalRouteGroupReq`: optional `localRouteGroup`.
        """
        # Schema wraps identity + new values inside a localRouteGroup sub-element
        if "localRouteGroup" not in args:
            args = {"localRouteGroup": args}
        return self.client.updateLocalRouteGroup(**args)

    def delete_local_route_group(self, name="", uuid=""):
        """
        Delete a local route group by name or uuid.
        :param name: local route group name
        :param uuid: local route group uuid
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeLocalRouteGroup(
            **self._identify(name=name, uuid=uuid)
        )

    # ------------------------------------------------------------------
    # RouteFilter
    # ------------------------------------------------------------------

    def add_route_filter(self, **args):
        """
        Add a route filter.
        :param name: route filter name - required
        :return: result dictionary
        

        Schema: `routeFilter` -> `XRouteFilter`: `name` + `dialPlanName` + `members`.
        """
        return self.client.addRouteFilter(
            self._build_object("addRouteFilter", "routeFilter", args)
        )

    def get_route_filter(self, **args):
        """
        Get a single route filter.
        :param name: route filter name
        :param uuid: route filter uuid
        :return: routeFilter dictionary
        

        Schema: `GetRouteFilterReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getRouteFilter(**args)["return"]["routeFilter"]

    def get_route_filters(self, tagfilter=None):
        """
        List all route filters.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of routeFilter dictionaries, empty when nothing matches
        

        Schema: `ListRouteFilterReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listRouteFilter(
            {"name": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("routeFilter") or []

    def update_route_filter(self, **args):
        """
        Update a route filter.
        :param name: route filter name (or uuid)
        :param uuid: route filter uuid (or name)
        :return: result dictionary
        

        Schema: `UpdateRouteFilterReq`: optional `newName`, `dialPlanName`, optional choice of (optional `removeMembers`, `addMembers`), or `members`.
        """
        return self.client.updateRouteFilter(**args)

    def delete_route_filter(self, name="", uuid=""):
        """
        Delete a route filter by name or uuid.
        :param name: route filter name
        :param uuid: route filter uuid
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeRouteFilter(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------
    # SipDialRules
    # ------------------------------------------------------------------

    def add_sip_dial_rules(self, **args):
        """
        Add a SIP dial rule.
        :param name: SIP dial rule name - required
        :return: result dictionary
        

        Schema: `sipDialRules` -> `XSipDialRules`: `dialPattern` + `name`; optional `description`, `patterns`, `plars`.
        """
        return self.client.addSipDialRules(
            self._build_object("addSipDialRules", "sipDialRules", args)
        )

    def get_sip_dial_rules(self, **args):
        """
        Get a single SIP dial rule.
        :param name: SIP dial rule name
        :param uuid: SIP dial rule uuid
        :return: sipDialRules dictionary
        

        Schema: `GetSipDialRulesReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getSipDialRules(**args)["return"]["sipDialRules"]

    def get_sip_dial_rules_list(self, tagfilter=None):
        """
        List all SIP dial rules.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of sipDialRules dictionaries, empty when nothing matches
        

        Schema: `ListSipDialRulesReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listSipDialRules(
            {"name": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("sipDialRules") or []

    def update_sip_dial_rules(self, **args):
        """
        Update a SIP dial rule.
        :param name: SIP dial rule name (or uuid)
        :param uuid: SIP dial rule uuid (or name)
        :return: result dictionary
        

        Schema: `UpdateSipDialRulesReq`: optional `newName`, `description`, optional choice of (optional `removePatterns`, `addPatterns`), or `patterns`, optional choice of (optional `removePlars`, `addPlars`), or `plars`.
        """
        return self.client.updateSipDialRules(**args)

    def delete_sip_dial_rules(self, name="", uuid=""):
        """
        Delete a SIP dial rule by name or uuid.
        :param name: SIP dial rule name
        :param uuid: SIP dial rule uuid
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeSipDialRules(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------
    # SipRoutePattern
    # Schema identity: pattern + routePartitionName (BOTH required) OR uuid
    # List search: pattern
    # ------------------------------------------------------------------

    def add_sip_route_pattern(self, **args):
        """
        Add a SIP route pattern.
        :param pattern: pattern - required
        :param usage: pattern usage - required
        :param routePartitionName: partition name - required
        :return: result dictionary
        

        Schema: `sipRoutePattern` -> `XSipRoutePattern`: `pattern` + `usage` + `routePartitionName` + `useCallingPartyPhoneMask` + `sipTrunkName`; optional `description`, `blockEnable`, `callingPartyTransformationMask`, `callingPartyPrefixDigits`, `callingLinePresentationBit`, `callingNamePresentationBit` and 6 more.
        """
        return self.client.addSipRoutePattern(
            self._build_object("addSipRoutePattern", "sipRoutePattern", args)
        )

    def get_sip_route_pattern(self, **args):
        """
        Get a single SIP route pattern.
        :param pattern: pattern
        :param routePartitionName: partition name (required with pattern)
        :param uuid: SIP route pattern uuid
        :return: sipRoutePattern dictionary
        

        Schema: `GetSipRoutePatternReq`: optional `returnedTags`; one of `uuid`, or (`pattern` + `routePartitionName`).
        """
        return self.client.getSipRoutePattern(**args)["return"]["sipRoutePattern"]

    def get_sip_route_patterns(self, tagfilter=None):
        """
        List all SIP route patterns.
        List searchCriteria uses 'pattern' (not 'name').
        :param tagfilter: AXL returned tags to include, e.g. {'pattern': ''}
        :return: list of sipRoutePattern dictionaries, empty when nothing matches
        

        Schema: `ListSipRoutePatternReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"pattern": ""}
        result = self.client.listSipRoutePattern(
            {"pattern": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("sipRoutePattern") or []

    def update_sip_route_pattern(self, **args):
        """
        Update a SIP route pattern.
        :param pattern: pattern (or uuid)
        :param routePartitionName: partition name (required with pattern)
        :param uuid: SIP route pattern uuid (or pattern+partition)
        :return: result dictionary
        

        Schema: `UpdateSipRoutePatternReq`: optional `newPattern`, `description`, `newRoutePartitionName`, `blockEnable`, `callingPartyTransformationMask`, `useCallingPartyPhoneMask` and 10 more; one of `uuid`, or (`pattern` + `routePartitionName`).
        """
        return self.client.updateSipRoutePattern(**args)

    def delete_sip_route_pattern(self, **args):
        """
        Delete a SIP route pattern.
        :param pattern: pattern
        :param routePartitionName: partition name (required with pattern)
        :param uuid: SIP route pattern uuid
        :return: result dictionary
        

        Schema: `RemoveSipRoutePatternReq`: one of `uuid`, or (`pattern` + `routePartitionName`).
        """
        return self.client.removeSipRoutePattern(**args)
