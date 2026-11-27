"""Less common objects: geo-location, billing, MLPP, HTTP profiles, VoH, and more.

Adds geo-location, billing, pattern, cloud-onboarding, DDI, dial-plan,
alias-sync, feature config, fallback, and handoff helpers.

Covered entities:
  Geo / Location policy:
    - GeoLocation              : add, get, list, update, remove
    - GeoLocationFilter        : add, get, list, update, remove
    - GeoLocationPolicy        : add, get, list, update, remove

  Billing / Profile:
    - BillingServer            : add, get, list, update, remove
    - BlockedLearnedPatterns   : add, get, list, update, remove
    - CCAProfiles              : add, get, list, update, remove
    - CumaServerSecurityProfile: add, get, list, update, remove

  Cloud / Customer:
    - CiscoCloudOnboarding     : list, update  (singleton — no add/remove)
    - Customer                 : add, get, list, update, remove

  Read-only DDI / DialPlan:
    - Ddi                      : get, list  (schema has no add/update/remove)
    - DialPlan                 : get, list  (schema has no add/update/remove)
    - DialPlanTag              : get, list  (schema has no add/update/remove)

  Alias / Sync:
    - DirNumberAliasLookupandSync : add, get, list, update, remove

  Feature configs (singleton — no add/list/remove):
    - EmccFeatureConfig        : get, update
    - FallbackFeatureConfig    : get, update

  Fallback / Handoff:
    - FallbackProfile          : add, get, list, update, remove
    - HandoffConfiguration     : add, get, update, remove  (no list in schema)

Adds HTTP profiles, infrastructure devices, inter-cluster objects, IVR locales,
MLPP domains, mobile smart client profiles, network access profiles, page layout
preferences, phone type display instances, resource priority namespaces,
route partitions for learned patterns, SDP transparency profiles,
transport settings, and VoH servers.

Included groups:
  HttpProfile                    : add, get, update, remove   (no list in AXL)
  InfrastructureDevice           : add, get, list, update, remove
  InterClusterDirectoryUri       : update  (singleton, no add/get/remove)
  InterClusterServiceProfile     : get, update  (no add/remove)
  IvrUserLocale                  : add, get, list, update, remove
  MlppDomain                     : add, get, list, update, remove
  MobileSmartClientProfile       : get, list  (read-only in AXL)
  NetworkAccessProfile           : add, get, list, update, remove
  PageLayoutPreferences          : get, update  (no add/remove/list)
  PhoneTypeDisplayInstance       : get  (read-only in AXL)
  ResourcePriorityNamespace      : add, get, list, update, remove, reset, restart, apply
  ResourcePriorityNamespaceList  : add, get, list, update, remove, reset, restart, apply
  RoutePartitionsForLearnedPatterns : update  (singleton, no add/get/remove)
  SdpTransparencyProfile         : add, get, list, update, remove
  TransportSettings              : get  (singleton)
  UpdateTransportSettings        : do_update_transport_settings
  VohServer                      : add, get, list, update, remove
"""


class NicheMixin:
    """Less common objects: geo-location, billing, MLPP, HTTP profiles, VoH, and more."""

    # ------------------------------------------------------------------ #
    # GeoLocation                                                          #
    # ------------------------------------------------------------------ #

    def add_geo_location(self, **args):
        """
        Add a geo location.
        :param name: geo location name — required
        :return: result dictionary (uuid)
        

        Schema: `geoLocation` -> `XGeoLocation`: `name`; optional `country`, `description`, `nationalSubDivision`, `district`, `communityName`, `cityDivision` and 12 more.
        """
        obj = self._build_object("addGeoLocation", "geoLocation", args)
        return self.client.addGeoLocation(geoLocation=obj)

    def get_geo_location(self, name="", uuid=""):
        """
        Get a single geo location.
        :param name: geo location name
        :param uuid: geo location uuid
        :return: geoLocation dictionary
        

        Schema: `GetGeoLocationReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getGeoLocation(
            **self._identify(name=name, uuid=uuid)
        )["return"]["geoLocation"]

    def get_geo_locations(self, tagfilter=None):
        """
        List all geo locations.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of geoLocation dictionaries, empty when nothing matches
        

        Schema: `ListGeoLocationReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listGeoLocation(
            {"name": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("geoLocation") or []

    def update_geo_location(self, name="", uuid="", **args):
        """
        Update a geo location.
        :param name: geo location name (or uuid)
        :param uuid: geo location uuid (or name)
        :return: result dictionary
        

        Schema: `UpdateGeoLocationReq`: optional `newName`, `country`, `description`, `nationalSubDivision`, `district`, `communityName` and 13 more.
        """
        return self.client.updateGeoLocation(
            **self._identify(name=name, uuid=uuid), **args
        )

    def delete_geo_location(self, name="", uuid=""):
        """
        Delete a geo location by name or uuid.
        :param name: geo location name
        :param uuid: geo location uuid
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeGeoLocation(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------ #
    # GeoLocationFilter                                                    #
    # ------------------------------------------------------------------ #

    def add_geo_location_filter(self, **args):
        """
        Add a geo location filter.
        :param name: filter name — required
        :return: result dictionary (uuid)
        

        Schema: `geoLocationFilter` -> `XGeoLocationFilter`: `name`; optional `description`, `useCountry`, `useNationalSubDivision`, `useDistrict`, `useCommunityName`, `useCityDivision` and 12 more.
        """
        obj = self._build_object("addGeoLocationFilter", "geoLocationFilter", args)
        return self.client.addGeoLocationFilter(geoLocationFilter=obj)

    def get_geo_location_filter(self, name="", uuid=""):
        """
        Get a single geo location filter.
        :param name: filter name
        :param uuid: filter uuid
        :return: geoLocationFilter dictionary
        

        Schema: `GetGeoLocationFilterReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getGeoLocationFilter(
            **self._identify(name=name, uuid=uuid)
        )["return"]["geoLocationFilter"]

    def get_geo_location_filters(self, tagfilter=None):
        """
        List all geo location filters.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of geoLocationFilter dictionaries, empty when nothing matches
        

        Schema: `ListGeoLocationFilterReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listGeoLocationFilter(
            {"name": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("geoLocationFilter") or []

    def update_geo_location_filter(self, name="", uuid="", **args):
        """
        Update a geo location filter.
        :param name: filter name (or uuid)
        :param uuid: filter uuid (or name)
        :return: result dictionary
        

        Schema: `UpdateGeoLocationFilterReq`: optional `newName`, `description`, `useCountry`, `useNationalSubDivision`, `useDistrict`, `useCommunityName` and 13 more.
        """
        return self.client.updateGeoLocationFilter(
            **self._identify(name=name, uuid=uuid), **args
        )

    def delete_geo_location_filter(self, name="", uuid=""):
        """
        Delete a geo location filter by name or uuid.
        :param name: filter name
        :param uuid: filter uuid
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeGeoLocationFilter(
            **self._identify(name=name, uuid=uuid)
        )

    # ------------------------------------------------------------------ #
    # GeoLocationPolicy                                                    #
    # ------------------------------------------------------------------ #

    def add_geo_location_policy(self, **args):
        """
        Add a geo location policy.
        :param name: policy name — required
        :return: result dictionary (uuid)
        

        Schema: `geoLocationPolicy` -> `XGeoLocationPolicy`: `name`; optional `country`, `description`, `nationalSubDivision`, `district`, `communityName`, `cityDivision` and 13 more.
        """
        obj = self._build_object("addGeoLocationPolicy", "geoLocationPolicy", args)
        return self.client.addGeoLocationPolicy(geoLocationPolicy=obj)

    def get_geo_location_policy(self, name="", uuid=""):
        """
        Get a single geo location policy.
        :param name: policy name
        :param uuid: policy uuid
        :return: geoLocationPolicy dictionary
        

        Schema: `GetGeoLocationPolicyReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getGeoLocationPolicy(
            **self._identify(name=name, uuid=uuid)
        )["return"]["geoLocationPolicy"]

    def get_geo_location_policies(self, tagfilter=None):
        """
        List all geo location policies.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of geoLocationPolicy dictionaries, empty when nothing matches
        

        Schema: `ListGeoLocationPolicyReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listGeoLocationPolicy(
            {"name": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("geoLocationPolicy") or []

    def update_geo_location_policy(self, name="", uuid="", **args):
        """
        Update a geo location policy.
        :param name: policy name (or uuid)
        :param uuid: policy uuid (or name)
        :return: result dictionary
        

        Schema: `UpdateGeoLocationPolicyReq`: optional `newName`, `country`, `description`, `nationalSubDivision`, `district`, `communityName` and 14 more.
        """
        return self.client.updateGeoLocationPolicy(
            **self._identify(name=name, uuid=uuid), **args
        )

    def delete_geo_location_policy(self, name="", uuid=""):
        """
        Delete a geo location policy by name or uuid.
        :param name: policy name
        :param uuid: policy uuid
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeGeoLocationPolicy(
            **self._identify(name=name, uuid=uuid)
        )

    # ------------------------------------------------------------------ #
    # BillingServer                                                        #
    # ------------------------------------------------------------------ #

    def add_billing_server(self, **args):
        """
        Add a billing server.
        :param hostName: billing server hostname — required
        :return: result dictionary (uuid)
        

        Schema: `billingServer` -> `XBillingServer`: `hostName` + `userId` + `password` + `directory` + `billingServerProtocol`; optional `resendOnFailure`.
        """
        obj = self._build_object("addBillingServer", "billingServer", args)
        return self.client.addBillingServer(billingServer=obj)

    def get_billing_server(self, uuid):
        """
        Get a billing server by uuid.
        :param uuid: billing server uuid — required
        :return: billingServer dictionary
        

        Schema: `GetBillingServerReq`: `uuid`; optional `returnedTags`.
        """
        return self.client.getBillingServer(uuid=uuid)["return"]["billingServer"]

    def get_billing_servers(self, tagfilter=None):
        """
        List all billing servers.
        :param tagfilter: AXL returned tags to include, e.g. {'hostName': ''}
        :return: list of billingServer dictionaries, empty when nothing matches
        

        Schema: `ListBillingServerReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"hostName": ""}
        result = self.client.listBillingServer(
            {"hostName": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("billingServer") or []

    def update_billing_server(self, uuid, **args):
        """
        Update a billing server.
        :param uuid: billing server uuid — required
        :return: result dictionary
        

        Schema: `UpdateBillingServerReq`: `uuid`; optional `userId`, `password`, `resendOnFailure`, `billingServerProtocol`.
        """
        return self.client.updateBillingServer(uuid=uuid, **args)

    def delete_billing_server(self, uuid):
        """
        Delete a billing server by uuid.
        :param uuid: billing server uuid — required
        :return: result dictionary
        

        Schema: `RemoveBillingServerReq`: `uuid`.
        """
        return self.client.removeBillingServer(uuid=uuid)

    # ------------------------------------------------------------------ #
    # BlockedLearnedPatterns                                               #
    # ------------------------------------------------------------------ #

    def add_blocked_learned_patterns(self, **args):
        """
        Add a blocked learned patterns entry.
        :param pattern: pattern — required
        :return: result dictionary (uuid)
        

        Schema: `blockedLearnedPatterns` -> `XBlockedLearnedPatterns`: optional `description`, `pattern`, `prefix`, `clusterId`, `patternType`.
        """
        obj = self._build_object(
            "addBlockedLearnedPatterns", "blockedLearnedPatterns", args
        )
        return self.client.addBlockedLearnedPatterns(blockedLearnedPatterns=obj)

    def get_blocked_learned_patterns(self, pattern="", uuid=""):
        """
        Get a single blocked learned patterns entry.
        :param pattern: pattern string (identity)
        :param uuid: entry uuid
        :return: blockedLearnedPatterns dictionary

        Note: BlockedLearnedPatterns uses 'pattern' (not 'name') as the AXL name identifier.
        

        Schema: `GetBlockedLearnedPatternsReq`: optional `returnedTags`; one of `pattern`, or `uuid`.
        """
        if bool(pattern) == bool(uuid):
            raise ValueError("Provide exactly one of pattern or uuid")
        identifier = {"pattern": pattern} if pattern else {"uuid": uuid}
        return self.client.getBlockedLearnedPatterns(
            **identifier
        )["return"]["blockedLearnedPatterns"]

    def get_blocked_learned_patterns_list(self, tagfilter=None):
        """
        List all blocked learned patterns entries.
        :param tagfilter: AXL returned tags to include, e.g. {'pattern': ''}
        :return: list of blockedLearnedPatterns dictionaries, empty when nothing matches
        

        Schema: `ListBlockedLearnedPatternsReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"pattern": ""}
        result = self.client.listBlockedLearnedPatterns(
            {"pattern": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("blockedLearnedPatterns") or []

    def update_blocked_learned_patterns(self, pattern="", uuid="", **args):
        """
        Update a blocked learned patterns entry.
        :param pattern: pattern string (identity)
        :param uuid: entry uuid
        :return: result dictionary
        

        Schema: `UpdateBlockedLearnedPatternsReq`: optional `description`, `newPattern`, `prefix`, `clusterId`, `patternType`; one of `uuid`, or `pattern`.
        """
        if bool(pattern) == bool(uuid):
            raise ValueError("Provide exactly one of pattern or uuid")
        identifier = {"pattern": pattern} if pattern else {"uuid": uuid}
        return self.client.updateBlockedLearnedPatterns(**identifier, **args)

    def delete_blocked_learned_patterns(self, pattern="", uuid=""):
        """
        Delete a blocked learned patterns entry by pattern or uuid.
        :param pattern: pattern string (identity)
        :param uuid: entry uuid
        :return: result dictionary
        

        Schema: `RemoveBlockedLearnedPatternsReq`: one of `pattern`, or `uuid`.
        """
        if bool(pattern) == bool(uuid):
            raise ValueError("Provide exactly one of pattern or uuid")
        identifier = {"pattern": pattern} if pattern else {"uuid": uuid}
        return self.client.removeBlockedLearnedPatterns(**identifier)

    # ------------------------------------------------------------------ #
    # CCAProfiles                                                          #
    # ------------------------------------------------------------------ #

    def add_cca_profiles(self, **args):
        """
        Add a CCA profile.
        :param name: profile name — required
        :return: result dictionary (uuid)
        

        Schema: `cCAProfiles` -> `XCCAProfiles`: `ccaId` + `primarySoftSwitchId` + `objectClass`; optional `secondarySoftSwitchId`, `subscriberType`, `sipAliasSuffix`, `sipUserNameSuffix`.
        """
        obj = self._build_object("addCCAProfiles", "cCAProfiles", args)
        return self.client.addCCAProfiles(cCAProfiles=obj)

    def get_cca_profiles(self, ccaId="", uuid=""):
        """
        Get a single CCA profile.
        :param ccaId: CCA profile ID (AXL primary key — not 'name')
        :param uuid: profile uuid
        :return: cCAProfiles dictionary

        Note: CCAProfiles uses 'ccaId' (not 'name') as the AXL name identifier.
        

        Schema: `GetCCAProfilesReq`: optional `returnedTags`; one of `ccaId`, or `uuid`.
        """
        if bool(ccaId) == bool(uuid):
            raise ValueError("Provide exactly one of ccaId or uuid")
        identifier = {"ccaId": ccaId} if ccaId else {"uuid": uuid}
        return self.client.getCCAProfiles(**identifier)["return"]["cCAProfiles"]

    def get_cca_profiles_list(self, tagfilter=None):
        """
        List all CCA profiles.
        :param tagfilter: AXL returned tags to include, e.g. {'ccaId': ''}
        :return: list of cCAProfiles dictionaries, empty when nothing matches
        

        Schema: `ListCCAProfilesReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"ccaId": ""}
        result = self.client.listCCAProfiles(
            {"ccaId": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("cCAProfiles") or []

    def update_cca_profiles(self, ccaId="", uuid="", **args):
        """
        Update a CCA profile.
        :param ccaId: CCA profile ID (or uuid)
        :param uuid: profile uuid (or ccaId)
        :return: result dictionary
        

        Schema: `UpdateCCAProfilesReq`: optional `newCcaId`, `primarySoftSwitchId`, `secondarySoftSwitchId`, `objectClass`, `subscriberType`, `sipAliasSuffix` and 1 more; one of `uuid`, or `ccaId`.
        """
        if bool(ccaId) == bool(uuid):
            raise ValueError("Provide exactly one of ccaId or uuid")
        identifier = {"ccaId": ccaId} if ccaId else {"uuid": uuid}
        return self.client.updateCCAProfiles(**identifier, **args)

    def delete_cca_profiles(self, ccaId="", uuid=""):
        """
        Delete a CCA profile by ccaId or uuid.
        :param ccaId: CCA profile ID
        :param uuid: profile uuid
        :return: result dictionary
        

        Schema: `RemoveCCAProfilesReq`: one of `ccaId`, or `uuid`.
        """
        if bool(ccaId) == bool(uuid):
            raise ValueError("Provide exactly one of ccaId or uuid")
        identifier = {"ccaId": ccaId} if ccaId else {"uuid": uuid}
        return self.client.removeCCAProfiles(**identifier)

    # ------------------------------------------------------------------ #
    # CiscoCloudOnboarding  (singleton — no add / remove in schema)       #
    # ------------------------------------------------------------------ #

    def get_cisco_cloud_onboarding_list(self, tagfilter=None):
        """
        List Cisco Cloud Onboarding configuration(s).
        :param tagfilter: AXL returned tags to include
        :return: list of ciscoCloudOnboarding dictionaries, empty when nothing matches

        Note: listCiscoCloudOnboarding searchCriteria has no filterable fields; pass empty dict.
        

        Schema: `ListCiscoCloudOnboardingReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"orgId": ""}
        result = self.client.listCiscoCloudOnboarding(
            {}, returnedTags=tags
        )["return"]
        return (result or {}).get("ciscoCloudOnboarding") or []

    def update_cisco_cloud_onboarding(self, **args):
        """
        Update the Cisco Cloud Onboarding configuration.
        :return: result dictionary
        

        Schema: `UpdateCiscoCloudOnboardingReq`: optional `voucherExists`, `enablePushNotifications`, `enableHttpProxy`, `httpProxyAddress`, `proxyUsername`, `proxyPassword` and 9 more; one of `uuid`.
        """
        return self.client.updateCiscoCloudOnboarding(**args)

    # ------------------------------------------------------------------ #
    # CumaServerSecurityProfile                                            #
    # ------------------------------------------------------------------ #

    def add_cuma_server_security_profile(self, **args):
        """
        Add a CUMA server security profile.
        :param name: profile name — required
        :return: result dictionary (uuid)
        

        Schema: `cumaServerSecurityProfile` -> `XCumaServerSecurityProfile`: `name` + `securityMode` + `transportType` + `serverIpHostName`; optional `description`, `x509SubjectName`.
        """
        obj = self._build_object(
            "addCumaServerSecurityProfile", "cumaServerSecurityProfile", args
        )
        return self.client.addCumaServerSecurityProfile(
            cumaServerSecurityProfile=obj
        )

    def get_cuma_server_security_profile(self, name="", uuid=""):
        """
        Get a single CUMA server security profile.
        :param name: profile name
        :param uuid: profile uuid
        :return: cumaServerSecurityProfile dictionary
        

        Schema: `GetCumaServerSecurityProfileReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getCumaServerSecurityProfile(
            **self._identify(name=name, uuid=uuid)
        )["return"]["cumaServerSecurityProfile"]

    def get_cuma_server_security_profiles(self, tagfilter=None):
        """
        List all CUMA server security profiles.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of cumaServerSecurityProfile dictionaries, empty when nothing matches
        

        Schema: `ListCumaServerSecurityProfileReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listCumaServerSecurityProfile(
            {"name": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("cumaServerSecurityProfile") or []

    def update_cuma_server_security_profile(self, name="", uuid="", **args):
        """
        Update a CUMA server security profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: result dictionary
        

        Schema: `UpdateCumaServerSecurityProfileReq`: optional `newName`, `description`, `securityMode`, `transportType`, `x509SubjectName`, `serverIpHostName`.
        """
        return self.client.updateCumaServerSecurityProfile(
            **self._identify(name=name, uuid=uuid), **args
        )

    def delete_cuma_server_security_profile(self, name="", uuid=""):
        """
        Delete a CUMA server security profile by name or uuid.
        :param name: profile name
        :param uuid: profile uuid
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeCumaServerSecurityProfile(
            **self._identify(name=name, uuid=uuid)
        )

    # ------------------------------------------------------------------ #
    # Customer                                                             #
    # ------------------------------------------------------------------ #

    def add_customer(self, **args):
        """
        Add a customer record.
        :param name: customer name — required
        :return: result dictionary (uuid)
        

        Schema: `customer` -> `XCustomer`: `name`.
        """
        obj = self._build_object("addCustomer", "customer", args)
        return self.client.addCustomer(customer=obj)

    def get_customer(self, name="", uuid=""):
        """
        Get a single customer record.
        :param name: customer name
        :param uuid: customer uuid
        :return: customer dictionary
        

        Schema: `GetCustomerReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getCustomer(
            **self._identify(name=name, uuid=uuid)
        )["return"]["customer"]

    def get_customers(self, tagfilter=None):
        """
        List all customer records.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of customer dictionaries, empty when nothing matches
        

        Schema: `ListCustomerReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listCustomer(
            {"name": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("customer") or []

    def update_customer(self, name="", uuid="", **args):
        """
        Update a customer record.
        :param name: customer name (or uuid)
        :param uuid: customer uuid (or name)
        :return: result dictionary
        

        Schema: `UpdateCustomerReq`: optional `newName`.
        """
        return self.client.updateCustomer(
            **self._identify(name=name, uuid=uuid), **args
        )

    def delete_customer(self, name="", uuid=""):
        """
        Delete a customer record by name or uuid.
        :param name: customer name
        :param uuid: customer uuid
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeCustomer(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------ #
    # Ddi  (read-only — schema has no add/update/remove)                  #
    # ------------------------------------------------------------------ #

    def get_ddi(self, uuid):
        """
        Get a single DDI entry by uuid.
        :param uuid: DDI uuid — required
        :return: ddi dictionary
        

        Schema: `GetDdiReq`: optional `returnedTags`; one of `uuid`, or (`name` + `dialPlanName`).
        """
        return self.client.getDdi(uuid=uuid)["return"]["ddi"]

    def get_ddis(self, tagfilter=None):
        """
        List all DDI entries.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of ddi dictionaries, empty when nothing matches
        

        Schema: `ListDdiReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listDdi(
            {"name": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("ddi") or []

    # ------------------------------------------------------------------ #
    # DialPlan  (read-only — schema has no add/update/remove)             #
    # ------------------------------------------------------------------ #

    def get_dial_plan(self, name="", uuid=""):
        """
        Get a single dial plan.
        :param name: dial plan name
        :param uuid: dial plan uuid
        :return: dialPlan dictionary
        

        Schema: `GetDialPlanReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getDialPlan(
            **self._identify(name=name, uuid=uuid)
        )["return"]["dialPlan"]

    def get_dial_plans(self, tagfilter=None):
        """
        List all dial plans.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of dialPlan dictionaries, empty when nothing matches
        

        Schema: `ListDialPlanReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listDialPlan(
            {"name": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("dialPlan") or []

    # ------------------------------------------------------------------ #
    # DialPlanTag  (read-only — schema has no add/update/remove)          #
    # ------------------------------------------------------------------ #

    def get_dial_plan_tag(self, uuid="", name="", dialPlanName=""):
        """
        Get a single dial plan tag.
        :param uuid: tag uuid (preferred — use alone)
        :param name: tag name (requires dialPlanName when used)
        :param dialPlanName: associated dial plan name (required when name is supplied)
        :return: dialPlanTag dictionary

        Note: AXL requires either uuid alone, or both name + dialPlanName.
        

        Schema: `GetDialPlanTagReq`: optional `returnedTags`; one of `uuid`, or (`name` + `dialPlanName`).
        """
        if uuid:
            identifier = {"uuid": uuid}
        elif name and dialPlanName:
            identifier = {"name": name, "dialPlanName": dialPlanName}
        else:
            raise ValueError(
                "Provide either uuid, or both name and dialPlanName"
            )
        return self.client.getDialPlanTag(**identifier)["return"]["dialPlanTag"]

    def get_dial_plan_tags(self, tagfilter=None):
        """
        List all dial plan tags.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of dialPlanTag dictionaries, empty when nothing matches
        

        Schema: `ListDialPlanTagReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listDialPlanTag(
            {"name": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("dialPlanTag") or []

    # ------------------------------------------------------------------ #
    # DirNumberAliasLookupandSync                                          #
    # ------------------------------------------------------------------ #

    def add_dir_number_alias_lookup_and_sync(self, **args):
        """
        Add a directory number alias lookup and sync entry.
        :param name: entry name — required
        :return: result dictionary (uuid)
        

        Schema: `dirNumberAliasLookupandSync` -> `XDirNumberAliasLookupandSync`: `ldapConfigName` + `ldapManagerDisgName` + `ldapPassword` + `ldapUserSearch` + `servers`; optional `ldapDirectoryServerUsage`, `keepAliveSearch`, `keepAliveTime`, `sipAliasSuffix`, `enableCachingofRecords`, `cacheSizeforAliasLookup` and 1 more.
        """
        obj = self._build_object(
            "addDirNumberAliasLookupandSync",
            "dirNumberAliasLookupandSync",
            args,
        )
        return self.client.addDirNumberAliasLookupandSync(
            dirNumberAliasLookupandSync=obj
        )

    def get_dir_number_alias_lookup_and_sync(self, name="", uuid=""):
        """
        Get a single directory number alias lookup and sync entry.
        :param name: entry name
        :param uuid: entry uuid
        :return: dirNumberAliasLookupandSync dictionary
        

        Schema: `GetDirNumberAliasLookupandSyncReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getDirNumberAliasLookupandSync(
            **self._identify(name=name, uuid=uuid)
        )["return"]["dirNumberAliasLookupandSync"]

    def get_dir_number_alias_lookup_and_sync_list(self, tagfilter=None):
        """
        List all directory number alias lookup and sync entries.
        :param tagfilter: AXL returned tags to include, e.g. {'ldapConfigName': ''}
        :return: list of dirNumberAliasLookupandSync dictionaries, empty when nothing matches
        

        Schema: `ListDirNumberAliasLookupandSyncReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"ldapConfigName": ""}
        result = self.client.listDirNumberAliasLookupandSync(
            {"ldapConfigName": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("dirNumberAliasLookupandSync") or []

    def update_dir_number_alias_lookup_and_sync(self, name="", uuid="", **args):
        """
        Update a directory number alias lookup and sync entry.
        :param name: entry name (or uuid)
        :param uuid: entry uuid (or name)
        :return: result dictionary
        

        Schema: `UpdateDirNumberAliasLookupandSyncReq`: optional `ldapConfigName`, `ldapManagerDisgName`, `ldapPassword`, `ldapUserSearch`, `ldapDirectoryServerUsage`, `keepAliveSearch` and 6 more.
        """
        return self.client.updateDirNumberAliasLookupandSync(
            **self._identify(name=name, uuid=uuid), **args
        )

    def delete_dir_number_alias_lookup_and_sync(self, name="", uuid=""):
        """
        Delete a directory number alias lookup and sync entry by name or uuid.
        :param name: entry name
        :param uuid: entry uuid
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeDirNumberAliasLookupandSync(
            **self._identify(name=name, uuid=uuid)
        )

    # ------------------------------------------------------------------ #
    # EmccFeatureConfig  (singleton — no add/list/remove in schema)       #
    # ------------------------------------------------------------------ #

    def get_emcc_feature_config(self):
        """
        Get EMCC feature configuration (singleton).
        :return: emccFeatureConfig dictionary
        

        Schema: `GetEmccFeatureConfigReq`: optional `returnedTags`; one of `parameterName`, or `uuid`.
        """
        return self.client.getEmccFeatureConfig()["return"]["emccFeatureConfig"]

    def update_emcc_feature_config(self, **args):
        """
        Update EMCC feature configuration.
        :return: result dictionary
        

        Schema: `UpdateEmccFeatureConfigReq`: optional `value`; one of `uuid`, or `parameterName`.
        """
        return self.client.updateEmccFeatureConfig(**args)

    # ------------------------------------------------------------------ #
    # FallbackFeatureConfig  (singleton — no add/list/remove in schema)   #
    # ------------------------------------------------------------------ #

    def get_fallback_feature_config(self):
        """
        Get fallback feature configuration (singleton).
        :return: fallbackFeatureConfig dictionary
        """
        return self.client.getFallbackFeatureConfig()["return"][
            "fallbackFeatureConfig"
        ]

    def update_fallback_feature_config(self, **args):
        """
        Update fallback feature configuration.
        :return: result dictionary
        

        Schema: `UpdateFallbackFeatureConfigReq`: optional `enableFallbackForImeCalls`, `qosSensistivityLevel`, `dtmfCorrelationDigits`, `dtmfCollectionTimer`, `callAnswerTimer`, `clearImeCallDelayTimer` and 4 more.
        """
        return self.client.updateFallbackFeatureConfig(**args)

    # ------------------------------------------------------------------ #
    # FallbackProfile                                                      #
    # ------------------------------------------------------------------ #

    def add_fallback_profile(self, **args):
        """
        Add a fallback profile.
        :param name: profile name — required
        :return: result dictionary (uuid)
        

        Schema: `fallbackProfile` -> `XFallbackProfile`: `name` + `callCss`; optional `description`, `advertisedFallbackDirectoryE164Number`, `qosSensistivityLevel`, `callAnswerTimer`, `directoryNumberPartition`, `directoryNumber` and 1 more.
        """
        obj = self._build_object("addFallbackProfile", "fallbackProfile", args)
        return self.client.addFallbackProfile(fallbackProfile=obj)

    def get_fallback_profile(self, name="", uuid=""):
        """
        Get a single fallback profile.
        :param name: profile name
        :param uuid: profile uuid
        :return: fallbackProfile dictionary
        

        Schema: `GetFallbackProfileReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getFallbackProfile(
            **self._identify(name=name, uuid=uuid)
        )["return"]["fallbackProfile"]

    def get_fallback_profiles(self, tagfilter=None):
        """
        List all fallback profiles.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of fallbackProfile dictionaries, empty when nothing matches
        

        Schema: `ListFallbackProfileReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listFallbackProfile(
            {"name": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("fallbackProfile") or []

    def update_fallback_profile(self, name="", uuid="", **args):
        """
        Update a fallback profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: result dictionary
        

        Schema: `UpdateFallbackProfileReq`: optional `newName`, `description`, `advertisedFallbackDirectoryE164Number`, `qosSensistivityLevel`, `callCss`, `callAnswerTimer` and 3 more.
        """
        return self.client.updateFallbackProfile(
            **self._identify(name=name, uuid=uuid), **args
        )

    def delete_fallback_profile(self, name="", uuid=""):
        """
        Delete a fallback profile by name or uuid.
        :param name: profile name
        :param uuid: profile uuid
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeFallbackProfile(
            **self._identify(name=name, uuid=uuid)
        )

    # ------------------------------------------------------------------ #
    # HandoffConfiguration  (no list in schema)                           #
    # ------------------------------------------------------------------ #

    def add_handoff_configuration(self, **args):
        """
        Add a handoff configuration.
        :param pattern: DN pattern — required
        :param routePartitionName: route partition name (optional)
        :return: result dictionary (uuid)

        Note: HandoffConfiguration identity is 'pattern' + optional 'routePartitionName',
        not 'handoffType'.
        

        Schema: `handoffConfiguration` -> `XHandoffConfiguration`: `pattern`; optional `routePartitionName`.
        """
        obj = self._build_object(
            "addHandoffConfiguration", "handoffConfiguration", args
        )
        return self.client.addHandoffConfiguration(handoffConfiguration=obj)

    def get_handoff_configuration(self, uuid="", pattern="", routePartitionName=""):
        """
        Get a single handoff configuration.
        :param uuid: handoff configuration uuid (preferred)
        :param pattern: DN pattern (alternative identity)
        :param routePartitionName: route partition name (optional companion to pattern)
        :return: handoffConfiguration dictionary
        

        Schema: `GetHandoffConfigurationReq`: optional `returnedTags`; one of `uuid`, or (`pattern`; optional `routePartitionName`).
        """
        if uuid:
            identifier = {"uuid": uuid}
        elif pattern:
            identifier = {"pattern": pattern}
            if routePartitionName:
                identifier["routePartitionName"] = routePartitionName
        else:
            raise ValueError("Provide either uuid or pattern")
        return self.client.getHandoffConfiguration(**identifier)["return"][
            "handoffConfiguration"
        ]

    def update_handoff_configuration(self, uuid="", pattern="", routePartitionName="", **args):
        """
        Update a handoff configuration.
        :param uuid: handoff configuration uuid (preferred)
        :param pattern: DN pattern (alternative identity)
        :param routePartitionName: route partition name (optional companion to pattern)
        :return: result dictionary
        

        Schema: `UpdateHandoffConfigurationReq`: optional `newPattern`, `newRoutePartitionName`; one of `uuid`, or (`pattern`; optional `routePartitionName`).
        """
        if uuid:
            identifier = {"uuid": uuid}
        elif pattern:
            identifier = {"pattern": pattern}
            if routePartitionName:
                identifier["routePartitionName"] = routePartitionName
        else:
            raise ValueError("Provide either uuid or pattern")
        return self.client.updateHandoffConfiguration(**identifier, **args)

    def delete_handoff_configuration(self, uuid="", pattern="", routePartitionName=""):
        """
        Delete a handoff configuration.
        :param uuid: handoff configuration uuid (preferred)
        :param pattern: DN pattern (alternative identity)
        :param routePartitionName: route partition name (optional companion to pattern)
        :return: result dictionary
        

        Schema: `RemoveHandoffConfigurationReq`: one of `uuid`, or (`pattern`; optional `routePartitionName`).
        """
        if uuid:
            identifier = {"uuid": uuid}
        elif pattern:
            identifier = {"pattern": pattern}
            if routePartitionName:
                identifier["routePartitionName"] = routePartitionName
        else:
            raise ValueError("Provide either uuid or pattern")
        return self.client.removeHandoffConfiguration(**identifier)

    # ------------------------------------------------------------------ #
    # HttpProfile                                                          #
    # ------------------------------------------------------------------ #

    def add_http_profile(self, **args):
        """
        Add an HTTP profile.
        :param name: profile name — required
        :param userName: HTTP authentication username
        :param password: HTTP authentication password
        :param requestTimeout: request timeout value
        :param retryCount: retry count
        :param webServiceRootUri: web service root URI
        :return: result dictionary (uuid)
        

        Schema: `httpProfile` -> `XHttpProfile`: `name` + `userName` + `password` + `webServiceRootUri`; optional `requestTimeout`, `retryCount`.
        """
        obj = self._build_object("addHttpProfile", "httpProfile", args)
        return self.client.addHttpProfile(httpProfile=obj)

    def get_http_profile(self, name="", uuid=""):
        """
        Get an HTTP profile.
        :param name: profile name  (or uuid)
        :param uuid: profile uuid  (or name)
        :return: httpProfile dictionary
        

        Schema: `GetHttpProfileReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        if bool(name) == bool(uuid):
            raise ValueError("Provide exactly one of name or uuid")
        identifier = {"name": name} if name else {"uuid": uuid}
        return self.client.getHttpProfile(**identifier)["return"]["httpProfile"]

    def update_http_profile(self, **args):
        """
        Update an HTTP profile.
        :param name: profile name  (or uuid) — required
        :param uuid: profile uuid  (or name) — required
        :param newName: new profile name
        :param description: new description
        :return: result dictionary
        

        Schema: `UpdateHttpProfileReq`: optional `newName`, `userName`, `password`, `requestTimeout`, `retryCount`, `webServiceRootUri`.
        """
        return self.client.updateHttpProfile(**args)

    def remove_http_profile(self, name="", uuid=""):
        """
        Remove an HTTP profile.
        :param name: profile name  (or uuid)
        :param uuid: profile uuid  (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        if bool(name) == bool(uuid):
            raise ValueError("Provide exactly one of name or uuid")
        identifier = {"name": name} if name else {"uuid": uuid}
        return self.client.removeHttpProfile(**identifier)

    # ------------------------------------------------------------------ #
    # InfrastructureDevice                                                 #
    # ------------------------------------------------------------------ #

    def add_infrastructure_device(self, **args):
        """
        Add an infrastructure device.
        :param name: device name — required
        :param description: description
        :param ipv4Address: IPv4 address
        :param ipv6Address: IPv6 address
        :param deviceType: device type
        :return: result dictionary (uuid)
        

        Schema: `infrastructureDevice` -> `XInfrastructureDevice`: optional `name`, `ipv4Address`, `ipv6Address`, `bssidWithMask`, `wapLocation`, `isActive`.
        """
        obj = self._build_object(
            "addInfrastructureDevice", "infrastructureDevice", args
        )
        return self.client.addInfrastructureDevice(infrastructureDevice=obj)

    def get_infrastructure_device(self, uuid=""):
        """
        Get an infrastructure device.  AXL only supports lookup by uuid.
        :param uuid: device uuid — required
        :return: infrastructureDevice dictionary
        

        Schema: `GetInfrastructureDeviceReq`: optional `returnedTags`; one of `uuid`.
        """
        if not uuid:
            raise ValueError("uuid is required")
        return self.client.getInfrastructureDevice(uuid=uuid)["return"][
            "infrastructureDevice"
        ]

    def get_infrastructure_devices(
        self,
        search_name="%",
        tagfilter={"name": "", "isActive": ""},
    ):
        """
        List infrastructure devices.
        :param search_name: name search pattern, default '%' (all)
        :param tagfilter: AXL returned tags to include
        :return: list of infrastructureDevice dictionaries, empty when nothing matches
        

        Schema: `ListInfrastructureDeviceReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listInfrastructureDevice(
            {"name": search_name}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("infrastructureDevice") or []

    def update_infrastructure_device(self, uuid="", **args):
        """
        Update an infrastructure device.  AXL only supports update by uuid.
        :param uuid: device uuid — required
        :param newName: new device name
        :param description: new description
        :return: result dictionary
        

        Schema: `UpdateInfrastructureDeviceReq`: optional `newName`, `ipv4Address`, `ipv6Address`, `bssidWithMask`, `wapLocation`, `isActive`; one of `uuid`.
        """
        if not uuid:
            raise ValueError("uuid is required")
        return self.client.updateInfrastructureDevice(uuid=uuid, **args)

    def remove_infrastructure_device(self, uuid=""):
        """
        Remove an infrastructure device.  AXL only supports removal by uuid.
        :param uuid: device uuid — required
        :return: result dictionary
        

        Schema: `RemoveInfrastructureDeviceReq`: one of `uuid`.
        """
        if not uuid:
            raise ValueError("uuid is required")
        return self.client.removeInfrastructureDevice(uuid=uuid)

    # ------------------------------------------------------------------ #
    # InterClusterDirectoryUri (update-only singleton)                     #
    # ------------------------------------------------------------------ #

    def update_inter_cluster_directory_uri(self, **args):
        """
        Update the inter-cluster directory URI settings.
        AXL schema fields: ``exchangeDirectoryUri`` (boolean), ``routeString``.
        :param exchangeDirectoryUri: boolean, exchange directory URIs
        :param routeString: route string (max 50 chars)
        :return: result dictionary
        

        Schema: `UpdateInterClusterDirectoryUriReq`: `exchangeDirectoryUri` + `routeString`.
        """
        return self.client.updateInterClusterDirectoryUri(**args)

    # ------------------------------------------------------------------ #
    # InterClusterServiceProfile (get / update — no add / remove)         #
    # ------------------------------------------------------------------ #

    def get_inter_cluster_service_profile(self, interClusterService="", uuid=""):
        """
        Get an inter-cluster service profile.
        :param interClusterService: service identifier  (or uuid)
        :param uuid: profile uuid  (or interClusterService)
        :return: interClusterServiceProfile dictionary
        

        Schema: `GetInterClusterServiceProfileReq`: optional `returnedTags`; one of `interClusterService`, or `uuid`.
        """
        if bool(interClusterService) == bool(uuid):
            raise ValueError(
                "Provide exactly one of interClusterService or uuid"
            )
        identifier = (
            {"interClusterService": interClusterService}
            if interClusterService
            else {"uuid": uuid}
        )
        return self.client.getInterClusterServiceProfile(**identifier)["return"][
            "interClusterServiceProfile"
        ]

    def update_inter_cluster_service_profile(self, **args):
        """
        Update an inter-cluster service profile.
        :param interClusterService: service identifier  (or uuid) — required
        :param uuid: profile uuid  (or interClusterService) — required
        :param isActivated: boolean, activate profile
        :param sipTrunkName: SIP trunk name reference
        :return: result dictionary
        

        Schema: `UpdateInterClusterServiceProfileReq`: optional `isActivated`, `sipTrunkName`; one of `uuid`, or `interClusterService`.
        """
        return self.client.updateInterClusterServiceProfile(**args)

    # ------------------------------------------------------------------ #
    # IvrUserLocale                                                        #
    # ------------------------------------------------------------------ #

    def add_ivr_user_locale(self, **args):
        """
        Add an IVR user locale entry.
        AXL schema fields: ``userLocale`` (locale reference), ``orderIndex``.
        :param userLocale: locale reference — required
        :param orderIndex: ordering index
        :return: result dictionary (uuid)
        

        Schema: `ivrUserLocale` -> `XIvrUserLocale`: `userLocale` + `orderIndex`.
        """
        obj = self._build_object("addIvrUserLocale", "ivrUserLocale", args)
        return self.client.addIvrUserLocale(ivrUserLocale=obj)

    def get_ivr_user_locale(self, userLocale="", uuid=""):
        """
        Get an IVR user locale.
        :param userLocale: locale reference  (or uuid)
        :param uuid: locale uuid  (or userLocale)
        :return: ivrUserLocale dictionary
        

        Schema: `GetIvrUserLocaleReq`: optional `returnedTags`; one of `userLocale`, or `uuid`.
        """
        if bool(userLocale) == bool(uuid):
            raise ValueError("Provide exactly one of userLocale or uuid")
        identifier = {"userLocale": userLocale} if userLocale else {"uuid": uuid}
        return self.client.getIvrUserLocale(**identifier)["return"]["ivrUserLocale"]

    def get_ivr_user_locales(
        self,
        search_locale="%",
        tagfilter={"userLocale": "", "orderIndex": ""},
    ):
        """
        List IVR user locales.
        :param search_locale: userLocale search pattern, default '%' (all)
        :param tagfilter: AXL returned tags to include
        :return: list of ivrUserLocale dictionaries, empty when nothing matches
        

        Schema: `ListIvrUserLocaleReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listIvrUserLocale(
            {"userLocale": search_locale}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("ivrUserLocale") or []

    def update_ivr_user_locale(self, **args):
        """
        Update an IVR user locale.
        :param userLocale: locale reference  (or uuid) — required
        :param uuid: locale uuid  (or userLocale) — required
        :param newUserLocale: new locale reference
        :param orderIndex: new ordering index
        :return: result dictionary
        

        Schema: `UpdateIvrUserLocaleReq`: optional `newUserLocale`, `orderIndex`; one of `uuid`, or `userLocale`.
        """
        return self.client.updateIvrUserLocale(**args)

    def remove_ivr_user_locale(self, userLocale="", uuid=""):
        """
        Remove an IVR user locale.
        :param userLocale: locale reference  (or uuid)
        :param uuid: locale uuid  (or userLocale)
        :return: result dictionary
        

        Schema: `RemoveIvrUserLocaleReq`: one of `userLocale`, or `uuid`.
        """
        if bool(userLocale) == bool(uuid):
            raise ValueError("Provide exactly one of userLocale or uuid")
        identifier = {"userLocale": userLocale} if userLocale else {"uuid": uuid}
        return self.client.removeIvrUserLocale(**identifier)

    # ------------------------------------------------------------------ #
    # MlppDomain                                                           #
    # ------------------------------------------------------------------ #

    def add_mlpp_domain(self, **args):
        """
        Add an MLPP domain.
        AXL schema fields: ``domainName``, ``domainId``.
        :param domainName: domain name — required
        :param domainId: hex domain ID (6 hex chars) — required
        :return: result dictionary (uuid)
        

        Schema: `mlppDomain` -> `XMlppDomain`: `domainName` + `domainId`.
        """
        obj = self._build_object("addMlppDomain", "mlppDomain", args)
        return self.client.addMlppDomain(mlppDomain=obj)

    def get_mlpp_domain(self, domainName="", uuid=""):
        """
        Get an MLPP domain.
        :param domainName: domain name  (or uuid)
        :param uuid: domain uuid  (or domainName)
        :return: mlppDomain dictionary
        

        Schema: `GetMlppDomainReq`: optional `returnedTags`; one of `domainName`, or `uuid`.
        """
        if bool(domainName) == bool(uuid):
            raise ValueError("Provide exactly one of domainName or uuid")
        identifier = {"domainName": domainName} if domainName else {"uuid": uuid}
        return self.client.getMlppDomain(**identifier)["return"]["mlppDomain"]

    def get_mlpp_domains(
        self,
        search_name="%",
        tagfilter={"domainName": "", "domainId": ""},
    ):
        """
        List MLPP domains.
        :param search_name: domainName search pattern, default '%' (all)
        :param tagfilter: AXL returned tags to include
        :return: list of mlppDomain dictionaries, empty when nothing matches
        

        Schema: `ListMlppDomainReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listMlppDomain(
            {"domainName": search_name}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("mlppDomain") or []

    def update_mlpp_domain(self, **args):
        """
        Update an MLPP domain.
        :param domainName: domain name  (or uuid) — required
        :param uuid: domain uuid  (or domainName) — required
        :param newDomainName: new domain name
        :param domainId: new hex domain ID
        :return: result dictionary
        

        Schema: `UpdateMlppDomainReq`: optional `newDomainName`, `domainId`; one of `uuid`, or `domainName`.
        """
        return self.client.updateMlppDomain(**args)

    def remove_mlpp_domain(self, domainName="", uuid=""):
        """
        Remove an MLPP domain.
        :param domainName: domain name  (or uuid)
        :param uuid: domain uuid  (or domainName)
        :return: result dictionary
        

        Schema: `RemoveMlppDomainReq`: one of `domainName`, or `uuid`.
        """
        if bool(domainName) == bool(uuid):
            raise ValueError("Provide exactly one of domainName or uuid")
        identifier = {"domainName": domainName} if domainName else {"uuid": uuid}
        return self.client.removeMlppDomain(**identifier)

    # ------------------------------------------------------------------ #
    # MobileSmartClientProfile (get / list — read-only in AXL)            #
    # ------------------------------------------------------------------ #

    def get_mobile_smart_client_profile(self, name="", uuid=""):
        """
        Get a mobile smart client profile.
        :param name: profile name  (or uuid)
        :param uuid: profile uuid  (or name)
        :return: mobileSmartClientProfile dictionary
        

        Schema: `GetMobileSmartClientProfileReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        if bool(name) == bool(uuid):
            raise ValueError("Provide exactly one of name or uuid")
        identifier = {"name": name} if name else {"uuid": uuid}
        return self.client.getMobileSmartClientProfile(**identifier)["return"][
            "mobileSmartClientProfile"
        ]

    def get_mobile_smart_client_profiles(
        self,
        search_name="%",
        tagfilter={"name": "", "mobileSmartClient": "", "enableSnrUri": ""},
    ):
        """
        List mobile smart client profiles.
        :param search_name: name search pattern, default '%' (all)
        :param tagfilter: AXL returned tags to include
        :return: list of mobileSmartClientProfile dictionaries, empty when nothing matches
        

        Schema: `ListMobileSmartClientProfileReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listMobileSmartClientProfile(
            {"name": search_name}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("mobileSmartClientProfile") or []

    # ------------------------------------------------------------------ #
    # NetworkAccessProfile                                                 #
    # ------------------------------------------------------------------ #

    def add_network_access_profile(self, **args):
        """
        Add a network access profile.
        :param name: profile name — required
        :param description: description
        :return: result dictionary (uuid)
        

        Schema: `networkAccessProfile` -> `XNetworkAccessProfile`: `name` + `vpnRequired` + `proxySettings` + `proxyHostname` + `proxyPort`; optional `description`, `proxyRequiresAuthentication`, `provideSharedCredentials`, `username`, `password`.
        """
        obj = self._build_object(
            "addNetworkAccessProfile", "networkAccessProfile", args
        )
        return self.client.addNetworkAccessProfile(networkAccessProfile=obj)

    def get_network_access_profile(self, name="", uuid=""):
        """
        Get a network access profile.
        :param name: profile name  (or uuid)
        :param uuid: profile uuid  (or name)
        :return: networkAccessProfile dictionary
        

        Schema: `GetNetworkAccessProfileReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        if bool(name) == bool(uuid):
            raise ValueError("Provide exactly one of name or uuid")
        identifier = {"name": name} if name else {"uuid": uuid}
        return self.client.getNetworkAccessProfile(**identifier)["return"][
            "networkAccessProfile"
        ]

    def get_network_access_profiles(
        self,
        search_name="%",
        tagfilter={"name": "", "description": ""},
    ):
        """
        List network access profiles.
        :param search_name: name search pattern, default '%' (all)
        :param tagfilter: AXL returned tags to include
        :return: list of networkAccessProfile dictionaries, empty when nothing matches
        

        Schema: `ListNetworkAccessProfileReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listNetworkAccessProfile(
            {"name": search_name}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("networkAccessProfile") or []

    def update_network_access_profile(self, **args):
        """
        Update a network access profile.
        :param name: profile name  (or uuid) — required
        :param uuid: profile uuid  (or name) — required
        :param newName: new profile name
        :param description: new description
        :return: result dictionary
        

        Schema: `UpdateNetworkAccessProfileReq`: optional `newName`, `description`, `vpnRequired`, `proxySettings`, `proxyHostname`, `proxyPort` and 4 more.
        """
        return self.client.updateNetworkAccessProfile(**args)

    def remove_network_access_profile(self, name="", uuid=""):
        """
        Remove a network access profile.
        :param name: profile name  (or uuid)
        :param uuid: profile uuid  (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        if bool(name) == bool(uuid):
            raise ValueError("Provide exactly one of name or uuid")
        identifier = {"name": name} if name else {"uuid": uuid}
        return self.client.removeNetworkAccessProfile(**identifier)

    # ------------------------------------------------------------------ #
    # PageLayoutPreferences (get / update — no add / remove / list)       #
    # ------------------------------------------------------------------ #

    def get_page_layout_preferences(self, pageName=""):
        """
        Get the page layout preferences for a given page.
        :param pageName: page name — required by AXL schema
        :return: pageLayoutPreferences dictionary
        

        Schema: `GetPageLayoutPreferencesReq`: `pageName`; optional `returnedTags`.
        """
        return self.client.getPageLayoutPreferences(pageName=pageName)["return"][
            "pageLayoutPreferences"
        ]

    def update_page_layout_preferences(self, **args):
        """
        Update the page layout preferences.
        :param pageName: page name — required
        :param maxDevicesPerPage: maximum devices per page
        :return: result dictionary
        

        Schema: `UpdatePageLayoutPreferencesReq`: `pageName` + `pageSections`.
        """
        return self.client.updatePageLayoutPreferences(**args)

    # ------------------------------------------------------------------ #
    # PhoneTypeDisplayInstance (get only)                                 #
    # ------------------------------------------------------------------ #

    def get_phone_type_display_instance(self, productName="", protocol="", trunkType=""):
        """
        Get a phone type display instance.
        AXL schema requires ``productName`` and ``protocol``. ``trunkType``
        is optional and applies to some gateway endpoints. The response has
        no ``return`` wrapper; ``displayInstance`` is a string on the response.
        :param productName: phone model name — required
        :param protocol: protocol string — required
        :param trunkType: trunk type string — optional
        :return: displayInstance string
        

        Schema: `GetPhoneTypeDisplayInstanceReq`: `productName` + `protocol`; optional `trunkType`.
        """
        if not productName:
            raise ValueError("productName is required")
        if not protocol:
            raise ValueError("protocol is required")
        return self.client.getPhoneTypeDisplayInstance(
            productName=productName,
            protocol=protocol,
            trunkType=trunkType,
        )["displayInstance"]

    # ------------------------------------------------------------------ #
    # ResourcePriorityNamespace                                            #
    # ------------------------------------------------------------------ #

    def add_resource_priority_namespace(self, **args):
        """
        Add a resource priority namespace.
        AXL schema fields: ``namespace`` (max 10 chars), ``description``, ``isDefault``.
        :param namespace: namespace string — required
        :param description: description
        :param isDefault: boolean, mark as default
        :return: result dictionary (uuid)
        

        Schema: `resourcePriorityNamespace` -> `XResourcePriorityNamespace`: `namespace`; optional `description`, `isDefault`.
        """
        obj = self._build_object(
            "addResourcePriorityNamespace", "resourcePriorityNamespace", args
        )
        return self.client.addResourcePriorityNamespace(
            resourcePriorityNamespace=obj
        )

    def get_resource_priority_namespace(self, namespace="", uuid=""):
        """
        Get a resource priority namespace.
        :param namespace: namespace string  (or uuid)
        :param uuid: namespace uuid  (or namespace)
        :return: resourcePriorityNamespace dictionary
        

        Schema: `GetResourcePriorityNamespaceReq`: optional `returnedTags`; one of `namespace`, or `uuid`.
        """
        if bool(namespace) == bool(uuid):
            raise ValueError("Provide exactly one of namespace or uuid")
        identifier = {"namespace": namespace} if namespace else {"uuid": uuid}
        return self.client.getResourcePriorityNamespace(**identifier)["return"][
            "resourcePriorityNamespace"
        ]

    def get_resource_priority_namespaces(
        self,
        search_namespace="%",
        tagfilter={"namespace": "", "description": ""},
    ):
        """
        List resource priority namespaces.
        :param search_namespace: namespace search pattern, default '%' (all)
        :param tagfilter: AXL returned tags to include
        :return: list of resourcePriorityNamespace dictionaries, empty when nothing matches
        

        Schema: `ListResourcePriorityNamespaceReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listResourcePriorityNamespace(
            {"namespace": search_namespace}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("resourcePriorityNamespace") or []

    def update_resource_priority_namespace(self, **args):
        """
        Update a resource priority namespace.
        :param namespace: namespace string  (or uuid) — required
        :param uuid: namespace uuid  (or namespace) — required
        :param description: new description
        :return: result dictionary
        

        Schema: `UpdateResourcePriorityNamespaceReq`: optional `newNamespace`, `description`, `isDefault`; one of `uuid`, or `namespace`.
        """
        return self.client.updateResourcePriorityNamespace(**args)

    def remove_resource_priority_namespace(self, namespace="", uuid=""):
        """
        Remove a resource priority namespace.
        :param namespace: namespace string  (or uuid)
        :param uuid: namespace uuid  (or namespace)
        :return: result dictionary
        

        Schema: `RemoveResourcePriorityNamespaceReq`: one of `namespace`, or `uuid`.
        """
        if bool(namespace) == bool(uuid):
            raise ValueError("Provide exactly one of namespace or uuid")
        identifier = {"namespace": namespace} if namespace else {"uuid": uuid}
        return self.client.removeResourcePriorityNamespace(**identifier)

    def reset_resource_priority_namespace(self, namespace="", uuid=""):
        """
        Reset a resource priority namespace.
        :param namespace: namespace string  (or uuid)
        :param uuid: namespace uuid  (or namespace)
        :return: result dictionary
        

        Schema: `ResetResourcePriorityNamespaceReq`: one of `namespace`, or `uuid`.
        """
        if bool(namespace) == bool(uuid):
            raise ValueError("Provide exactly one of namespace or uuid")
        identifier = {"namespace": namespace} if namespace else {"uuid": uuid}
        return self.client.resetResourcePriorityNamespace(**identifier)

    def restart_resource_priority_namespace(self, namespace="", uuid=""):
        """
        Restart a resource priority namespace.
        :param namespace: namespace string  (or uuid)
        :param uuid: namespace uuid  (or namespace)
        :return: result dictionary
        

        Schema: `RestartResourcePriorityNamespaceReq`: one of `namespace`, or `uuid`.
        """
        if bool(namespace) == bool(uuid):
            raise ValueError("Provide exactly one of namespace or uuid")
        identifier = {"namespace": namespace} if namespace else {"uuid": uuid}
        return self.client.restartResourcePriorityNamespace(**identifier)

    def apply_resource_priority_namespace(self, namespace="", uuid=""):
        """
        Apply (activate) a resource priority namespace.
        :param namespace: namespace string  (or uuid)
        :param uuid: namespace uuid  (or namespace)
        :return: result dictionary
        

        Schema: `ApplyResourcePriorityNamespaceReq`: one of `namespace`, or `uuid`.
        """
        if bool(namespace) == bool(uuid):
            raise ValueError("Provide exactly one of namespace or uuid")
        identifier = {"namespace": namespace} if namespace else {"uuid": uuid}
        return self.client.applyResourcePriorityNamespace(**identifier)

    # ------------------------------------------------------------------ #
    # ResourcePriorityNamespaceList                                        #
    # ------------------------------------------------------------------ #

    def add_resource_priority_namespace_list(self, **args):
        """
        Add a resource priority namespace list.
        :param name: list name — required
        :param description: description
        :return: result dictionary (uuid)
        

        Schema: `resourcePriorityNamespaceList` -> `XResourcePriorityNamespaceList`: `name`; optional `description`, `members`.
        """
        obj = self._build_object(
            "addResourcePriorityNamespaceList",
            "resourcePriorityNamespaceList",
            args,
        )
        return self.client.addResourcePriorityNamespaceList(
            resourcePriorityNamespaceList=obj
        )

    def get_resource_priority_namespace_list(self, name="", uuid=""):
        """
        Get a resource priority namespace list.
        :param name: list name  (or uuid)
        :param uuid: list uuid  (or name)
        :return: resourcePriorityNamespaceList dictionary
        

        Schema: `GetResourcePriorityNamespaceListReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        if bool(name) == bool(uuid):
            raise ValueError("Provide exactly one of name or uuid")
        identifier = {"name": name} if name else {"uuid": uuid}
        return self.client.getResourcePriorityNamespaceList(**identifier)["return"][
            "resourcePriorityNamespaceList"
        ]

    def get_resource_priority_namespace_lists(
        self,
        search_name="%",
        tagfilter={"name": "", "description": ""},
    ):
        """
        List resource priority namespace lists.
        :param search_name: name search pattern, default '%' (all)
        :param tagfilter: AXL returned tags to include
        :return: list of resourcePriorityNamespaceList dictionaries, empty when nothing matches
        

        Schema: `ListResourcePriorityNamespaceListReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listResourcePriorityNamespaceList(
            {"name": search_name}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("resourcePriorityNamespaceList") or []

    def update_resource_priority_namespace_list(self, **args):
        """
        Update a resource priority namespace list.
        :param name: list name  (or uuid) — required
        :param uuid: list uuid  (or name) — required
        :param newName: new list name
        :param description: new description
        :return: result dictionary
        

        Schema: `UpdateResourcePriorityNamespaceListReq`: optional `newName`, `description`, optional choice of (optional `removeMembers`, `addMembers`), or `members`.
        """
        return self.client.updateResourcePriorityNamespaceList(**args)

    def remove_resource_priority_namespace_list(self, name="", uuid=""):
        """
        Remove a resource priority namespace list.
        :param name: list name  (or uuid)
        :param uuid: list uuid  (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        if bool(name) == bool(uuid):
            raise ValueError("Provide exactly one of name or uuid")
        identifier = {"name": name} if name else {"uuid": uuid}
        return self.client.removeResourcePriorityNamespaceList(**identifier)

    def reset_resource_priority_namespace_list(self, name="", uuid=""):
        """
        Reset a resource priority namespace list.
        :param name: list name  (or uuid)
        :param uuid: list uuid  (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        if bool(name) == bool(uuid):
            raise ValueError("Provide exactly one of name or uuid")
        identifier = {"name": name} if name else {"uuid": uuid}
        return self.client.resetResourcePriorityNamespaceList(**identifier)

    def restart_resource_priority_namespace_list(self, name="", uuid=""):
        """
        Restart a resource priority namespace list.
        :param name: list name  (or uuid)
        :param uuid: list uuid  (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        if bool(name) == bool(uuid):
            raise ValueError("Provide exactly one of name or uuid")
        identifier = {"name": name} if name else {"uuid": uuid}
        return self.client.restartResourcePriorityNamespaceList(**identifier)

    def apply_resource_priority_namespace_list(self, name="", uuid=""):
        """
        Apply (activate) a resource priority namespace list.
        :param name: list name  (or uuid)
        :param uuid: list uuid  (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        if bool(name) == bool(uuid):
            raise ValueError("Provide exactly one of name or uuid")
        identifier = {"name": name} if name else {"uuid": uuid}
        return self.client.applyResourcePriorityNamespaceList(**identifier)

    # ------------------------------------------------------------------ #
    # RoutePartitionsForLearnedPatterns (update-only singleton)           #
    # ------------------------------------------------------------------ #

    def update_route_partitions_for_learned_patterns(self, **args):
        """
        Update the route partitions for learned patterns.
        AXL schema fields: partitionForEnterpriseANo, partitionForE164ANo,
        partitionForEnterprisePatterns, partitionForE164Pattern,
        markLearnedEntAltNumbers, markLearnedE164AltNumbers,
        markFixedLengthEntPatterns, markVariableLengthEntPatterns,
        markFixedLengthE164Patterns, markVariableLengthE164Patterns.
        :param partitionForEnterpriseANo: route partition for enterprise alternate numbers
        :param partitionForE164ANo: route partition for E.164 alternate numbers
        :param partitionForEnterprisePatterns: route partition for enterprise patterns
        :param partitionForE164Pattern: route partition for E.164 patterns
        :return: result dictionary
        

        Schema: `UpdateRoutePartitionsForLearnedPatternsReq`: `partitionForEnterpriseANo` + `partitionForE164ANo` + `partitionForEnterprisePatterns` + `partitionForE164Pattern` + `markLearnedEntAltNumbers` + `markLearnedE164AltNumbers` + `markFixedLengthEntPatterns` + `markVariableLengthEntPatterns` + `markFixedLengthE164Patterns` + `markVariableLengthE164Patterns`.
        """
        return self.client.updateRoutePartitionsForLearnedPatterns(**args)

    # ------------------------------------------------------------------ #
    # SdpTransparencyProfile                                              #
    # ------------------------------------------------------------------ #

    def add_sdp_transparency_profile(self, **args):
        """
        Add an SDP transparency profile.
        :param name: profile name — required
        :param description: description
        :return: result dictionary (uuid)
        

        Schema: `sdpTransparencyProfile` -> `XSdpTransparencyProfile`: `name` + `attributeSet`; optional `description`.
        """
        obj = self._build_object(
            "addSdpTransparencyProfile", "sdpTransparencyProfile", args
        )
        return self.client.addSdpTransparencyProfile(sdpTransparencyProfile=obj)

    def get_sdp_transparency_profile(self, name="", uuid=""):
        """
        Get an SDP transparency profile.
        :param name: profile name  (or uuid)
        :param uuid: profile uuid  (or name)
        :return: sdpTransparencyProfile dictionary
        

        Schema: `GetSdpTransparencyProfileReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        if bool(name) == bool(uuid):
            raise ValueError("Provide exactly one of name or uuid")
        identifier = {"name": name} if name else {"uuid": uuid}
        return self.client.getSdpTransparencyProfile(**identifier)["return"][
            "sdpTransparencyProfile"
        ]

    def get_sdp_transparency_profiles(
        self,
        search_name="%",
        tagfilter={"name": "", "description": ""},
    ):
        """
        List SDP transparency profiles.
        :param search_name: name search pattern, default '%' (all)
        :param tagfilter: AXL returned tags to include
        :return: list of sdpTransparencyProfile dictionaries, empty when nothing matches
        

        Schema: `ListSdpTransparencyProfileReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listSdpTransparencyProfile(
            {"name": search_name}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("sdpTransparencyProfile") or []

    def update_sdp_transparency_profile(self, **args):
        """
        Update an SDP transparency profile.
        :param name: profile name  (or uuid) — required
        :param uuid: profile uuid  (or name) — required
        :param newName: new profile name
        :param description: new description
        :return: result dictionary
        

        Schema: `UpdateSdpTransparencyProfileReq`: optional `newName`, `description`.
        """
        return self.client.updateSdpTransparencyProfile(**args)

    def remove_sdp_transparency_profile(self, name="", uuid=""):
        """
        Remove an SDP transparency profile.
        :param name: profile name  (or uuid)
        :param uuid: profile uuid  (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        if bool(name) == bool(uuid):
            raise ValueError("Provide exactly one of name or uuid")
        identifier = {"name": name} if name else {"uuid": uuid}
        return self.client.removeSdpTransparencyProfile(**identifier)

    # ------------------------------------------------------------------ #
    # TransportSettings / UpdateTransportSettings                         #
    # ------------------------------------------------------------------ #

    def get_transport_settings(self):
        """
        Get cluster transport settings (singleton; no identifier).
        The SOAP ``return`` element is a status string. This method returns
        the sibling ``TransportSettings`` object.
        :return: TransportSettings dictionary
        """
        return self.client.getTransportSettings()["TransportSettings"]

    def do_update_transport_settings(self, **args):
        """
        Trigger a transport settings update (doUpdateTransportSettings).
        AXL schema fields: ``transportMode``, ``url``, ``httpHost``, ``httpPort``,
        ``enableProxyAuthentication``, ``proxyUserName``, ``proxyPassword``.
        :param transportMode: transport mode string
        :param url: URL string
        :param httpHost: HTTP proxy host
        :param httpPort: HTTP proxy port
        :param enableProxyAuthentication: enable proxy authentication (string)
        :param proxyUserName: proxy username
        :param proxyPassword: proxy password
        :return: result dictionary
        

        Schema: `DoUpdateTransportSettingsReq`: `transportMode` + `url` + `httpHost` + `httpPort`; optional `enableProxyAuthentication`, `proxyUserName`, `proxyPassword`.
        """
        return self.client.doUpdateTransportSettings(**args)

    # ------------------------------------------------------------------ #
    # VohServer                                                            #
    # ------------------------------------------------------------------ #

    def add_voh_server(self, **args):
        """
        Add a Video on Hold (VoH) server.
        AXL schema fields: ``name``, ``description``, ``sipTrunkName``, ``defaultVideoStreamId``.
        :param name: server name — required
        :param description: description
        :param sipTrunkName: SIP trunk name reference
        :param defaultVideoStreamId: default video stream ID
        :return: result dictionary (uuid)
        

        Schema: `vohServer` -> `XVohServer`: `name` + `sipTrunkName` + `defaultVideoStreamId`; optional `description`.
        """
        obj = self._build_object("addVohServer", "vohServer", args)
        return self.client.addVohServer(vohServer=obj)

    def get_voh_server(self, name="", uuid=""):
        """
        Get a VoH server.
        :param name: server name  (or uuid)
        :param uuid: server uuid  (or name)
        :return: vohServer dictionary
        

        Schema: `GetVohServerReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        if bool(name) == bool(uuid):
            raise ValueError("Provide exactly one of name or uuid")
        identifier = {"name": name} if name else {"uuid": uuid}
        return self.client.getVohServer(**identifier)["return"]["vohServer"]

    def get_voh_servers(
        self,
        search_name="%",
        tagfilter={"name": "", "description": "", "sipTrunkName": ""},
    ):
        """
        List VoH servers.
        :param search_name: name search pattern, default '%' (all)
        :param tagfilter: AXL returned tags to include
        :return: list of vohServer dictionaries, empty when nothing matches
        

        Schema: `ListVohServerReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listVohServer(
            {"name": search_name}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("vohServer") or []

    def update_voh_server(self, **args):
        """
        Update a VoH server.
        :param name: server name  (or uuid) — required
        :param uuid: server uuid  (or name) — required
        :param newName: new server name
        :param description: new description
        :return: result dictionary
        

        Schema: `UpdateVohServerReq`: optional `newName`, `description`, `sipTrunkName`, `defaultVideoStreamId`.
        """
        return self.client.updateVohServer(**args)

    def remove_voh_server(self, name="", uuid=""):
        """
        Remove a VoH server.
        :param name: server name  (or uuid)
        :param uuid: server uuid  (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        if bool(name) == bool(uuid):
            raise ValueError("Provide exactly one of name or uuid")
        identifier = {"name": name} if name else {"uuid": uuid}
        return self.client.removeVohServer(**identifier)
