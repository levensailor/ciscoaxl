"""
P3 Niche A — Batch B5
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
"""


class P3NicheA:
    """Mixin: geo-location, billing, cloud onboarding, DDI, dial-plan,
    alias sync, feature configs, fallback, and handoff AXL operations."""

    # ------------------------------------------------------------------ #
    # GeoLocation                                                          #
    # ------------------------------------------------------------------ #

    def add_geo_location(self, **args):
        """
        Add a geo location.
        :param name: geo location name — required
        :return: result dictionary (uuid)
        """
        obj = self._build_object("addGeoLocation", "geoLocation", args)
        return self.client.addGeoLocation(geoLocation=obj)

    def get_geo_location(self, name="", uuid=""):
        """
        Get a single geo location.
        :param name: geo location name
        :param uuid: geo location uuid
        :return: geoLocation dictionary
        """
        return self.client.getGeoLocation(
            **self._identify(name=name, uuid=uuid)
        )["return"]["geoLocation"]

    def get_geo_locations(self, tagfilter=None):
        """
        List all geo locations.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of geoLocation dictionaries, empty when nothing matches
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
        """
        obj = self._build_object("addGeoLocationFilter", "geoLocationFilter", args)
        return self.client.addGeoLocationFilter(geoLocationFilter=obj)

    def get_geo_location_filter(self, name="", uuid=""):
        """
        Get a single geo location filter.
        :param name: filter name
        :param uuid: filter uuid
        :return: geoLocationFilter dictionary
        """
        return self.client.getGeoLocationFilter(
            **self._identify(name=name, uuid=uuid)
        )["return"]["geoLocationFilter"]

    def get_geo_location_filters(self, tagfilter=None):
        """
        List all geo location filters.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of geoLocationFilter dictionaries, empty when nothing matches
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
        """
        obj = self._build_object("addGeoLocationPolicy", "geoLocationPolicy", args)
        return self.client.addGeoLocationPolicy(geoLocationPolicy=obj)

    def get_geo_location_policy(self, name="", uuid=""):
        """
        Get a single geo location policy.
        :param name: policy name
        :param uuid: policy uuid
        :return: geoLocationPolicy dictionary
        """
        return self.client.getGeoLocationPolicy(
            **self._identify(name=name, uuid=uuid)
        )["return"]["geoLocationPolicy"]

    def get_geo_location_policies(self, tagfilter=None):
        """
        List all geo location policies.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of geoLocationPolicy dictionaries, empty when nothing matches
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
        """
        obj = self._build_object("addBillingServer", "billingServer", args)
        return self.client.addBillingServer(billingServer=obj)

    def get_billing_server(self, uuid):
        """
        Get a billing server by uuid.
        :param uuid: billing server uuid — required
        :return: billingServer dictionary
        """
        return self.client.getBillingServer(uuid=uuid)["return"]["billingServer"]

    def get_billing_servers(self, tagfilter=None):
        """
        List all billing servers.
        :param tagfilter: AXL returned tags to include, e.g. {'hostName': ''}
        :return: list of billingServer dictionaries, empty when nothing matches
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
        """
        return self.client.updateBillingServer(uuid=uuid, **args)

    def delete_billing_server(self, uuid):
        """
        Delete a billing server by uuid.
        :param uuid: billing server uuid — required
        :return: result dictionary
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
        """
        return self.client.getCumaServerSecurityProfile(
            **self._identify(name=name, uuid=uuid)
        )["return"]["cumaServerSecurityProfile"]

    def get_cuma_server_security_profiles(self, tagfilter=None):
        """
        List all CUMA server security profiles.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of cumaServerSecurityProfile dictionaries, empty when nothing matches
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
        """
        obj = self._build_object("addCustomer", "customer", args)
        return self.client.addCustomer(customer=obj)

    def get_customer(self, name="", uuid=""):
        """
        Get a single customer record.
        :param name: customer name
        :param uuid: customer uuid
        :return: customer dictionary
        """
        return self.client.getCustomer(
            **self._identify(name=name, uuid=uuid)
        )["return"]["customer"]

    def get_customers(self, tagfilter=None):
        """
        List all customer records.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of customer dictionaries, empty when nothing matches
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
        """
        return self.client.getDdi(uuid=uuid)["return"]["ddi"]

    def get_ddis(self, tagfilter=None):
        """
        List all DDI entries.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of ddi dictionaries, empty when nothing matches
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
        """
        return self.client.getDialPlan(
            **self._identify(name=name, uuid=uuid)
        )["return"]["dialPlan"]

    def get_dial_plans(self, tagfilter=None):
        """
        List all dial plans.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of dialPlan dictionaries, empty when nothing matches
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
        """
        return self.client.getDirNumberAliasLookupandSync(
            **self._identify(name=name, uuid=uuid)
        )["return"]["dirNumberAliasLookupandSync"]

    def get_dir_number_alias_lookup_and_sync_list(self, tagfilter=None):
        """
        List all directory number alias lookup and sync entries.
        :param tagfilter: AXL returned tags to include, e.g. {'ldapConfigName': ''}
        :return: list of dirNumberAliasLookupandSync dictionaries, empty when nothing matches
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
        """
        return self.client.getEmccFeatureConfig()["return"]["emccFeatureConfig"]

    def update_emcc_feature_config(self, **args):
        """
        Update EMCC feature configuration.
        :return: result dictionary
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
        """
        obj = self._build_object("addFallbackProfile", "fallbackProfile", args)
        return self.client.addFallbackProfile(fallbackProfile=obj)

    def get_fallback_profile(self, name="", uuid=""):
        """
        Get a single fallback profile.
        :param name: profile name
        :param uuid: profile uuid
        :return: fallbackProfile dictionary
        """
        return self.client.getFallbackProfile(
            **self._identify(name=name, uuid=uuid)
        )["return"]["fallbackProfile"]

    def get_fallback_profiles(self, tagfilter=None):
        """
        List all fallback profiles.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of fallbackProfile dictionaries, empty when nothing matches
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
