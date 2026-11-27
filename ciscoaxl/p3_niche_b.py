"""
P3 Niche-B Mixin — batch B6
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


class P3NicheB:
    """Mixin providing HTTP profiles, infrastructure devices, inter-cluster objects,
    IVR locales, MLPP domains, mobile smart client profiles, network access profiles,
    page layout preferences, phone type display instances, resource priority namespaces,
    route partitions for learned patterns, SDP transparency profiles,
    transport settings, and VoH servers."""

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
        """
        obj = self._build_object("addHttpProfile", "httpProfile", args)
        return self.client.addHttpProfile(httpProfile=obj)

    def get_http_profile(self, name="", uuid=""):
        """
        Get an HTTP profile.
        :param name: profile name  (or uuid)
        :param uuid: profile uuid  (or name)
        :return: httpProfile dictionary
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
        """
        return self.client.updateHttpProfile(**args)

    def remove_http_profile(self, name="", uuid=""):
        """
        Remove an HTTP profile.
        :param name: profile name  (or uuid)
        :param uuid: profile uuid  (or name)
        :return: result dictionary
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
        """
        if not uuid:
            raise ValueError("uuid is required")
        return self.client.updateInfrastructureDevice(uuid=uuid, **args)

    def remove_infrastructure_device(self, uuid=""):
        """
        Remove an infrastructure device.  AXL only supports removal by uuid.
        :param uuid: device uuid — required
        :return: result dictionary
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
        """
        obj = self._build_object("addIvrUserLocale", "ivrUserLocale", args)
        return self.client.addIvrUserLocale(ivrUserLocale=obj)

    def get_ivr_user_locale(self, userLocale="", uuid=""):
        """
        Get an IVR user locale.
        :param userLocale: locale reference  (or uuid)
        :param uuid: locale uuid  (or userLocale)
        :return: ivrUserLocale dictionary
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
        """
        return self.client.updateIvrUserLocale(**args)

    def remove_ivr_user_locale(self, userLocale="", uuid=""):
        """
        Remove an IVR user locale.
        :param userLocale: locale reference  (or uuid)
        :param uuid: locale uuid  (or userLocale)
        :return: result dictionary
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
        """
        obj = self._build_object("addMlppDomain", "mlppDomain", args)
        return self.client.addMlppDomain(mlppDomain=obj)

    def get_mlpp_domain(self, domainName="", uuid=""):
        """
        Get an MLPP domain.
        :param domainName: domain name  (or uuid)
        :param uuid: domain uuid  (or domainName)
        :return: mlppDomain dictionary
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
        """
        return self.client.updateMlppDomain(**args)

    def remove_mlpp_domain(self, domainName="", uuid=""):
        """
        Remove an MLPP domain.
        :param domainName: domain name  (or uuid)
        :param uuid: domain uuid  (or domainName)
        :return: result dictionary
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
        """
        return self.client.updateNetworkAccessProfile(**args)

    def remove_network_access_profile(self, name="", uuid=""):
        """
        Remove a network access profile.
        :param name: profile name  (or uuid)
        :param uuid: profile uuid  (or name)
        :return: result dictionary
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
        """
        return self.client.updateResourcePriorityNamespace(**args)

    def remove_resource_priority_namespace(self, namespace="", uuid=""):
        """
        Remove a resource priority namespace.
        :param namespace: namespace string  (or uuid)
        :param uuid: namespace uuid  (or namespace)
        :return: result dictionary
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
        """
        return self.client.updateResourcePriorityNamespaceList(**args)

    def remove_resource_priority_namespace_list(self, name="", uuid=""):
        """
        Remove a resource priority namespace list.
        :param name: list name  (or uuid)
        :param uuid: list uuid  (or name)
        :return: result dictionary
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
        """
        return self.client.updateSdpTransparencyProfile(**args)

    def remove_sdp_transparency_profile(self, name="", uuid=""):
        """
        Remove an SDP transparency profile.
        :param name: profile name  (or uuid)
        :param uuid: profile uuid  (or name)
        :return: result dictionary
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
        """
        obj = self._build_object("addVohServer", "vohServer", args)
        return self.client.addVohServer(vohServer=obj)

    def get_voh_server(self, name="", uuid=""):
        """
        Get a VoH server.
        :param name: server name  (or uuid)
        :param uuid: server uuid  (or name)
        :return: vohServer dictionary
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
        """
        return self.client.updateVohServer(**args)

    def remove_voh_server(self, name="", uuid=""):
        """
        Remove a VoH server.
        :param name: server name  (or uuid)
        :param uuid: server uuid  (or name)
        :return: result dictionary
        """
        if bool(name) == bool(uuid):
            raise ValueError("Provide exactly one of name or uuid")
        identifier = {"name": name} if name else {"uuid": uuid}
        return self.client.removeVohServer(**identifier)
