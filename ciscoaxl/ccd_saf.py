"""Call Control Discovery (CCD) and Service Advertisement Framework (SAF) wrappers.

Adds Cisco CCD (Cisco Call Director) and SAF (Service Advertisement Framework) methods.

Included groups:
  CCD objects:
    - CcdAdvertisingService   : add, get, list, update, remove
    - CcdFeatureConfig        : get, update
    - CcdHostedDN             : add, get, list, update, remove
    - CcdHostedDNGroup        : add, get, list, update, remove
    - CcdRequestingService    : add, get, update, remove

  SAF objects:
    - SafCcdPurgeBlockLearnedRoutes : add, get, list, update, remove
    - SafForwarder            : add, get, list, update, remove
    - SafSecurityProfile      : add, get, list, update, remove
"""


class CcdSafMixin:
    """Call Control Discovery (CCD) and Service Advertisement Framework (SAF) wrappers."""

    # ------------------------------------------------------------------ #
    # CcdAdvertisingService                                                #
    # ------------------------------------------------------------------ #

    def add_ccd_advertising_service(self, **args):
        """
        Add a CCD advertising service.
        :param name: service name — required
        :param description: description
        :param isActivated: boolean, activate the service
        :param hostDnGroup: hosted DN group name (FK) — required
        :param safSipTrunk: SAF SIP trunk name (FK)
        :param safH323Trunk: SAF H.323 trunk name (FK)
        :return: result dictionary (uuid)
        

        Schema: `ccdAdvertisingService` -> `XCcdAdvertisingService`: `name` + `hostDnGroup`; optional `description`, `isActivated`, `safSipTrunk`, `safH323Trunk`.
        """
        obj = self._build_object(
            "addCcdAdvertisingService",
            "ccdAdvertisingService",
            args,
        )
        return self.client.addCcdAdvertisingService(ccdAdvertisingService=obj)

    def get_ccd_advertising_service(self, name="", uuid=""):
        """
        Get a CCD advertising service.
        :param name: service name (or uuid)
        :param uuid: service uuid (or name)
        :return: ccdAdvertisingService dictionary
        

        Schema: `GetCcdAdvertisingServiceReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getCcdAdvertisingService(
            **self._identify(name=name, uuid=uuid)
        )["return"]["ccdAdvertisingService"]

    def get_ccd_advertising_services(
        self, tagfilter={"name": "", "description": ""}
    ):
        """
        List CCD advertising services.
        :param tagfilter: AXL returned tags to include
        :return: list of ccdAdvertisingService dictionaries, empty when nothing matches
        

        Schema: `ListCcdAdvertisingServiceReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listCcdAdvertisingService(
            {"name": "%"}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("ccdAdvertisingService") or []

    def update_ccd_advertising_service(self, **args):
        """
        Update a CCD advertising service.
        :param name: service name (or uuid)
        :param uuid: service uuid (or name)
        :param newName: new name
        :param description: new description
        :param isActivated: boolean
        :param hostDnGroup: hosted DN group name (FK)
        :param safSipTrunk: SAF SIP trunk name (FK)
        :param safH323Trunk: SAF H.323 trunk name (FK)
        :return: result dictionary
        

        Schema: `UpdateCcdAdvertisingServiceReq`: optional `newName`, `description`, `isActivated`, `hostDnGroup`, `safSipTrunk`, `safH323Trunk`.
        """
        return self.client.updateCcdAdvertisingService(**args)

    def remove_ccd_advertising_service(self, name="", uuid=""):
        """
        Remove a CCD advertising service.
        :param name: service name (or uuid)
        :param uuid: service uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeCcdAdvertisingService(
            **self._identify(name=name, uuid=uuid)
        )

    # ------------------------------------------------------------------ #
    # CcdFeatureConfig                                                     #
    # ------------------------------------------------------------------ #

    def get_ccd_feature_config(self, paramName, tagfilter=None):
        """
        Get a CCD feature configuration parameter.
        :param paramName: parameter name — required
        :param tagfilter: dict specifying fields to return; defaults to
                          {'ccdParamName': '', 'ccdParamValue': ''}
        :return: ccdFeatureConfig dictionary
        

        Schema: `GetCcdFeatureConfigReq`: `paramName` + `returnedTags`.
        """
        if tagfilter is None:
            tagfilter = {"ccdParamName": "", "ccdParamValue": ""}
        return self.client.getCcdFeatureConfig(
            paramName=paramName, returnedTags=tagfilter
        )["return"]["ccdFeatureConfig"]

    def update_ccd_feature_config(self, ccdParam):
        """
        Update one or more CCD feature configuration parameters.
        :param ccdParam: single dict or list of dicts with keys
                         ``ccdParamName`` and ``ccdParamValue`` — required
        :return: result message string
        

        Schema: `ccdParam` -> `RCcdParam`: optional `ccdParamName`, `ccdParamValue`.
        """
        if isinstance(ccdParam, dict):
            ccdParam = [ccdParam]
        return self.client.updateCcdFeatureConfig(ccdParam=ccdParam)

    # ------------------------------------------------------------------ #
    # CcdHostedDN                                                          #
    # ------------------------------------------------------------------ #

    def add_ccd_hosted_dn(self, **args):
        """
        Add a CCD hosted directory number.
        :param hostedPattern: pattern string — required
        :param description: description
        :param CcdHostedDnGroup: hosted DN group name (FK) — required
        :param pstnFailoverStripDigits: digits to strip on PSTN failover (integer)
        :param pstnFailoverPrependDigits: digits to prepend on PSTN failover
        :param usePstnFailover: boolean, use PSTN failover
        :return: result dictionary (uuid)
        

        Schema: `ccdHostedDN` -> `XCcdHostedDN`: `hostedPattern` + `CcdHostedDnGroup`; optional `description`, `pstnFailoverStripDigits`, `pstnFailoverPrependDigits`, `usePstnFailover`.
        """
        obj = self._build_object(
            "addCcdHostedDN",
            "ccdHostedDN",
            args,
        )
        return self.client.addCcdHostedDN(ccdHostedDN=obj)

    def get_ccd_hosted_dn(self, hostedPattern="", uuid=""):
        """
        Get a CCD hosted DN.
        :param hostedPattern: pattern string (or uuid)
        :param uuid: hosted DN uuid (or hostedPattern)
        :return: ccdHostedDN dictionary
        

        Schema: `GetCcdHostedDNReq`: optional `returnedTags`; one of `hostedPattern`, or `uuid`.
        """
        if bool(hostedPattern) == bool(uuid):
            raise ValueError("Provide exactly one of hostedPattern or uuid")
        identifier = {"hostedPattern": hostedPattern} if hostedPattern else {"uuid": uuid}
        return self.client.getCcdHostedDN(**identifier)["return"]["ccdHostedDN"]

    def get_ccd_hosted_dns(
        self, tagfilter={"hostedPattern": "", "description": ""}
    ):
        """
        List CCD hosted DNs.
        :param tagfilter: AXL returned tags to include
        :return: list of ccdHostedDN dictionaries, empty when nothing matches
        

        Schema: `ListCcdHostedDNReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listCcdHostedDN(
            {"hostedPattern": "%"}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("ccdHostedDN") or []

    def update_ccd_hosted_dn(self, **args):
        """
        Update a CCD hosted DN.
        :param hostedPattern: pattern string (or uuid)
        :param uuid: hosted DN uuid (or hostedPattern)
        :param newHostedPattern: new pattern string
        :param description: new description
        :param CcdHostedDnGroup: hosted DN group name (FK)
        :param pstnFailoverStripDigits: digits to strip (integer)
        :param pstnFailoverPrependDigits: digits to prepend
        :param usePstnFailover: boolean
        :return: result dictionary
        

        Schema: `UpdateCcdHostedDNReq`: optional `newHostedPattern`, `description`, `CcdHostedDnGroup`, `pstnFailoverStripDigits`, `pstnFailoverPrependDigits`, `usePstnFailover`; one of `uuid`, or `hostedPattern`.
        """
        return self.client.updateCcdHostedDN(**args)

    def remove_ccd_hosted_dn(self, hostedPattern="", uuid=""):
        """
        Remove a CCD hosted DN.
        :param hostedPattern: pattern string (or uuid)
        :param uuid: hosted DN uuid (or hostedPattern)
        :return: result dictionary
        

        Schema: `RemoveCcdHostedDNReq`: one of `hostedPattern`, or `uuid`.
        """
        if bool(hostedPattern) == bool(uuid):
            raise ValueError("Provide exactly one of hostedPattern or uuid")
        identifier = {"hostedPattern": hostedPattern} if hostedPattern else {"uuid": uuid}
        return self.client.removeCcdHostedDN(**identifier)

    # ------------------------------------------------------------------ #
    # CcdHostedDNGroup                                                     #
    # ------------------------------------------------------------------ #

    def add_ccd_hosted_dn_group(self, **args):
        """
        Add a CCD hosted DN group.
        :param name: group name — required
        :param description: description
        :param pstnFailoverStripDigits: digits to strip on PSTN failover (integer)
        :param pstnFailoverPrependDigits: digits to prepend on PSTN failover
        :param usePstnFailover: boolean, use PSTN failover
        :return: result dictionary (uuid)
        

        Schema: `ccdHostedDNGroup` -> `XCcdHostedDNGroup`: `name`; optional `description`, `pstnFailoverStripDigits`, `pstnFailoverPrependDigits`, `usePstnFailover`.
        """
        obj = self._build_object(
            "addCcdHostedDNGroup",
            "ccdHostedDNGroup",
            args,
        )
        return self.client.addCcdHostedDNGroup(ccdHostedDNGroup=obj)

    def get_ccd_hosted_dn_group(self, name="", uuid=""):
        """
        Get a CCD hosted DN group.
        :param name: group name (or uuid)
        :param uuid: group uuid (or name)
        :return: ccdHostedDNGroup dictionary
        

        Schema: `GetCcdHostedDNGroupReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getCcdHostedDNGroup(
            **self._identify(name=name, uuid=uuid)
        )["return"]["ccdHostedDNGroup"]

    def get_ccd_hosted_dn_groups(
        self, tagfilter={"name": "", "description": ""}
    ):
        """
        List CCD hosted DN groups.
        :param tagfilter: AXL returned tags to include
        :return: list of ccdHostedDNGroup dictionaries, empty when nothing matches
        

        Schema: `ListCcdHostedDNGroupReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listCcdHostedDNGroup(
            {"name": "%"}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("ccdHostedDNGroup") or []

    def update_ccd_hosted_dn_group(self, **args):
        """
        Update a CCD hosted DN group.
        :param name: group name (or uuid)
        :param uuid: group uuid (or name)
        :param newName: new name
        :param description: new description
        :param pstnFailoverStripDigits: digits to strip (integer)
        :param pstnFailoverPrependDigits: digits to prepend
        :param usePstnFailover: boolean
        :return: result dictionary
        

        Schema: `UpdateCcdHostedDNGroupReq`: optional `newName`, `description`, `pstnFailoverStripDigits`, `pstnFailoverPrependDigits`, `usePstnFailover`.
        """
        return self.client.updateCcdHostedDNGroup(**args)

    def remove_ccd_hosted_dn_group(self, name="", uuid=""):
        """
        Remove a CCD hosted DN group.
        :param name: group name (or uuid)
        :param uuid: group uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeCcdHostedDNGroup(
            **self._identify(name=name, uuid=uuid)
        )

    # ------------------------------------------------------------------ #
    # CcdRequestingService                                                 #
    # ------------------------------------------------------------------ #

    def add_ccd_requesting_service(self, **args):
        """
        Add a CCD requesting service.
        :param name: service name — required
        :param description: description
        :param isActivated: boolean, activate the service
        :param routePartitionName: route partition name (FK)
        :param learnedPatternPrefix: learned pattern prefix
        :param pstnPrefix: PSTN prefix
        :param associatedTrunks: trunk membership dict
        :return: result dictionary (uuid)
        

        Schema: `ccdRequestingService` -> `XCcdRequestingService`: `name`; optional `description`, `isActivated`, `routePartitionName`, `learnedPatternPrefix`, `pstnPrefix`, `associatedTrunks`.
        """
        obj = self._build_object(
            "addCcdRequestingService",
            "ccdRequestingService",
            args,
        )
        return self.client.addCcdRequestingService(ccdRequestingService=obj)

    def get_ccd_requesting_service(self, name="", uuid=""):
        """
        Get a CCD requesting service.
        :param name: service name (or uuid)
        :param uuid: service uuid (or name)
        :return: ccdRequestingService dictionary
        

        Schema: `GetCcdRequestingServiceReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getCcdRequestingService(
            **self._identify(name=name, uuid=uuid)
        )["return"]["ccdRequestingService"]

    def update_ccd_requesting_service(self, **args):
        """
        Update a CCD requesting service.
        :param name: service name (or uuid)
        :param uuid: service uuid (or name)
        :param newName: new name
        :param description: new description
        :param isActivated: boolean
        :param routePartitionName: route partition name (FK)
        :param learnedPatternPrefix: learned pattern prefix
        :param pstnPrefix: PSTN prefix
        :return: result dictionary
        

        Schema: `UpdateCcdRequestingServiceReq`: optional `newName`, `description`, `isActivated`, `routePartitionName`, `learnedPatternPrefix`, `pstnPrefix` and 1 more.
        """
        return self.client.updateCcdRequestingService(**args)

    def remove_ccd_requesting_service(self, name="", uuid=""):
        """
        Remove a CCD requesting service.
        :param name: service name (or uuid)
        :param uuid: service uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeCcdRequestingService(
            **self._identify(name=name, uuid=uuid)
        )

    # ------------------------------------------------------------------ #
    # SafCcdPurgeBlockLearnedRoutes                                        #
    # ------------------------------------------------------------------ #

    def add_saf_ccd_purge_block_learned_routes(self, **args):
        """
        Add a SAF CCD purge/block learned routes entry.
        :param learnedPattern: learned pattern (or learnedPatternPrefix) — required
        :param learnedPatternPrefix: learned pattern prefix (or learnedPattern)
        :param callControlIdentity: call control identity
        :param ipAddress: IP address
        :return: result dictionary (uuid)
        

        Schema: `safCcdPurgeBlockLearnedRoutes` -> `XSafCcdPurgeBlockLearnedRoutes`: optional `learnedPattern`, `learnedPatternPrefix`, `callControlIdentity`, `ipAddress`.
        """
        obj = self._build_object(
            "addSafCcdPurgeBlockLearnedRoutes",
            "safCcdPurgeBlockLearnedRoutes",
            args,
        )
        return self.client.addSafCcdPurgeBlockLearnedRoutes(
            safCcdPurgeBlockLearnedRoutes=obj
        )

    def get_saf_ccd_purge_block_learned_routes(self, uuid="", **kwargs):
        """
        Get a SAF CCD purge/block learned routes entry.
        :param uuid: entry uuid — required (or learnedPattern + learnedPatternPrefix)
        :param learnedPattern: learned pattern (alternative to uuid)
        :param learnedPatternPrefix: learned pattern prefix
        :param callControlIdentity: call control identity
        :param ipAddress: IP address
        :return: safCcdPurgeBlockLearnedRoutes dictionary
        

        Schema: `GetSafCcdPurgeBlockLearnedRoutesReq`: optional `returnedTags`; one of `uuid`, or (optional `learnedPattern`, `learnedPatternPrefix`, `callControlIdentity`, `ipAddress`).
        """
        if uuid:
            identifier = {"uuid": uuid}
        else:
            identifier = kwargs
        return self.client.getSafCcdPurgeBlockLearnedRoutes(
            **identifier
        )["return"]["safCcdPurgeBlockLearnedRoutes"]

    def get_saf_ccd_purge_block_learned_routes_list(
        self, tagfilter={"learnedPattern": "", "learnedPatternPrefix": ""}
    ):
        """
        List SAF CCD purge/block learned routes entries.
        :param tagfilter: AXL returned tags to include
        :return: list of safCcdPurgeBlockLearnedRoutes dictionaries, empty when nothing matches
        

        Schema: `ListSafCcdPurgeBlockLearnedRoutesReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listSafCcdPurgeBlockLearnedRoutes(
            {"learnedPattern": "%"}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("safCcdPurgeBlockLearnedRoutes") or []

    def update_saf_ccd_purge_block_learned_routes(self, **args):
        """
        Update a SAF CCD purge/block learned routes entry.
        :param uuid: entry uuid — required (or learnedPattern)
        :param learnedPattern: learned pattern (or uuid)
        :param learnedPatternPrefix: learned pattern prefix
        :param callControlIdentity: call control identity
        :param ipAddress: IP address
        :return: result dictionary
        

        Schema: `UpdateSafCcdPurgeBlockLearnedRoutesReq`: optional `newLearnedPattern`, `newLearnedPatternPrefix`, `newCallControlIdentity`, `newIpAddress`; one of `uuid`, or (optional `learnedPattern`, `learnedPatternPrefix`, `callControlIdentity`, `ipAddress`).
        """
        return self.client.updateSafCcdPurgeBlockLearnedRoutes(**args)

    def remove_saf_ccd_purge_block_learned_routes(self, uuid="", **kwargs):
        """
        Remove a SAF CCD purge/block learned routes entry.
        :param uuid: entry uuid (or learnedPattern + learnedPatternPrefix)
        :param learnedPattern: learned pattern
        :param learnedPatternPrefix: learned pattern prefix
        :param callControlIdentity: call control identity
        :param ipAddress: IP address
        :return: result dictionary
        

        Schema: `RemoveSafCcdPurgeBlockLearnedRoutesReq`: one of `uuid`, or (optional `learnedPattern`, `learnedPatternPrefix`, `callControlIdentity`, `ipAddress`).
        """
        if uuid:
            identifier = {"uuid": uuid}
        else:
            identifier = kwargs
        return self.client.removeSafCcdPurgeBlockLearnedRoutes(**identifier)

    # ------------------------------------------------------------------ #
    # SafForwarder                                                         #
    # ------------------------------------------------------------------ #

    def add_saf_forwarder(self, **args):
        """
        Add a SAF forwarder.
        :param name: forwarder name — required
        :param description: description
        :param clientLabel: client label — required
        :param safSecurityProfile: SAF security profile name (FK) — required
        :param ipAddress: IP address — required
        :param port: port number (default 5050)
        :param enableTcpKeepAlive: boolean (default True)
        :param safReconnectInterval: reconnect interval in seconds (default 20)
        :param safNotificationsWindowSize: notifications window size (default 7)
        :param associatedCucms: CUCM membership dict
        :return: result dictionary (uuid)
        

        Schema: `safForwarder` -> `XSafForwarder`: `name` + `clientLabel` + `safSecurityProfile` + `ipAddress`; optional `description`, `port`, `enableTcpKeepAlive`, `safReconnectInterval`, `safNotificationsWindowSize`, `associatedCucms`.
        """
        obj = self._build_object(
            "addSafForwarder",
            "safForwarder",
            args,
        )
        return self.client.addSafForwarder(safForwarder=obj)

    def get_saf_forwarder(self, name="", uuid=""):
        """
        Get a SAF forwarder.
        :param name: forwarder name (or uuid)
        :param uuid: forwarder uuid (or name)
        :return: safForwarder dictionary
        

        Schema: `GetSafForwarderReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getSafForwarder(
            **self._identify(name=name, uuid=uuid)
        )["return"]["safForwarder"]

    def get_saf_forwarders(
        self, tagfilter={"name": "", "description": ""}
    ):
        """
        List SAF forwarders.
        :param tagfilter: AXL returned tags to include
        :return: list of safForwarder dictionaries, empty when nothing matches
        

        Schema: `ListSafForwarderReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listSafForwarder(
            {"name": "%"}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("safForwarder") or []

    def update_saf_forwarder(self, **args):
        """
        Update a SAF forwarder.
        :param name: forwarder name (or uuid)
        :param uuid: forwarder uuid (or name)
        :param newName: new name
        :param description: new description
        :param clientLabel: client label
        :param safSecurityProfile: SAF security profile name (FK)
        :param ipAddress: IP address
        :param port: port number
        :param enableTcpKeepAlive: boolean
        :param safReconnectInterval: reconnect interval
        :param safNotificationsWindowSize: notifications window size
        :return: result dictionary
        

        Schema: `UpdateSafForwarderReq`: optional `newName`, `description`, `clientLabel`, `safSecurityProfile`, `ipAddress`, `port` and 4 more.
        """
        return self.client.updateSafForwarder(**args)

    def remove_saf_forwarder(self, name="", uuid=""):
        """
        Remove a SAF forwarder.
        :param name: forwarder name (or uuid)
        :param uuid: forwarder uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeSafForwarder(
            **self._identify(name=name, uuid=uuid)
        )

    # ------------------------------------------------------------------ #
    # SafSecurityProfile                                                   #
    # ------------------------------------------------------------------ #

    def add_saf_security_profile(self, **args):
        """
        Add a SAF security profile.
        :param name: profile name — required
        :param description: description
        :param userid: SAF user ID — required
        :param password: SAF password — required
        :return: result dictionary (uuid)
        

        Schema: `safSecurityProfile` -> `XSafSecurityProfile`: `name` + `userid` + `password`; optional `description`.
        """
        obj = self._build_object(
            "addSafSecurityProfile",
            "safSecurityProfile",
            args,
        )
        return self.client.addSafSecurityProfile(safSecurityProfile=obj)

    def get_saf_security_profile(self, name="", uuid=""):
        """
        Get a SAF security profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: safSecurityProfile dictionary
        

        Schema: `GetSafSecurityProfileReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getSafSecurityProfile(
            **self._identify(name=name, uuid=uuid)
        )["return"]["safSecurityProfile"]

    def get_saf_security_profiles(
        self, tagfilter={"name": "", "description": ""}
    ):
        """
        List SAF security profiles.
        :param tagfilter: AXL returned tags to include
        :return: list of safSecurityProfile dictionaries, empty when nothing matches
        

        Schema: `ListSafSecurityProfileReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listSafSecurityProfile(
            {"name": "%"}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("safSecurityProfile") or []

    def update_saf_security_profile(self, **args):
        """
        Update a SAF security profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :param newName: new name
        :param description: new description
        :param userid: SAF user ID
        :param password: SAF password
        :return: result dictionary
        

        Schema: `UpdateSafSecurityProfileReq`: optional `newName`, `description`, `userid`, `password`.
        """
        return self.client.updateSafSecurityProfile(**args)

    def remove_saf_security_profile(self, name="", uuid=""):
        """
        Remove a SAF security profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeSafSecurityProfile(
            **self._identify(name=name, uuid=uuid)
        )
