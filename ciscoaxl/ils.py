"""Intercluster Lookup Service (ILS) and Smart Licensing wrappers.

Adds ILS (Intercluster Lookup Service) and Smart Licensing methods.

Included groups:
  ILS federation objects:
    - AdvertisedPatterns         : add, get, list, update, remove
    - IlsConfig                  : get, update
    - ImportedDirectoryUriCatalogs: add, get, list, update, remove
    - RemoteCluster              : add, get, list, update, remove

  ILS/cluster actions:
    - doUpdateRemoteCluster      : force-sync remote cluster data

  Smart Licensing:
    - doSmartEntitlementRequest  : send entitlement request to CSSM/Satellite
    - doSmartLicenseDeRegister   : de-register from CSSM
    - doSmartLicenseReRegister   : force re-register with CSSM
    - doSmartLicenseRegister     : register with CSSM
    - doSmartLicenseRenewAuthorization : renew license authorization
    - doSmartLicenseRenewRegistration  : renew license registration

  License usage:
    - doUpdateLicenseUsage       : trigger a license usage update
"""


class IlsMixin:
    """Intercluster Lookup Service (ILS) and Smart Licensing wrappers."""

    # ------------------------------------------------------------------ #
    # AdvertisedPatterns                                                   #
    # ------------------------------------------------------------------ #

    def add_advertised_pattern(self, **args):
        """
        Add an advertised pattern.
        :param pattern: pattern string — required
        :param description: description
        :param patternType: e.g. 'Enterprise Number'
        :param hostedRoutePSTNRule: PSTN failover rule
        :param pstnFailStrip: digits to strip on PSTN fail (integer)
        :param pstnFailPrepend: digits to prepend on PSTN fail
        :return: result dictionary (uuid)
        

        Schema: `advertisedPatterns` -> `XAdvertisedPatterns`: `pattern` + `pstnFailStrip`; optional `description`, `patternType`, `hostedRoutePSTNRule`, `pstnFailPrepend`.
        """
        obj = self._build_object(
            "addAdvertisedPatterns",
            "advertisedPatterns",
            args,
        )
        return self.client.addAdvertisedPatterns(advertisedPatterns=obj)

    def get_advertised_pattern(self, pattern="", uuid=""):
        """
        Get an advertised pattern.
        :param pattern: pattern string (or uuid)
        :param uuid: pattern uuid (or pattern)
        :return: advertisedPatterns dictionary
        

        Schema: `GetAdvertisedPatternsReq`: optional `returnedTags`; one of `pattern`, or `uuid`.
        """
        if bool(pattern) == bool(uuid):
            raise ValueError("Provide exactly one of pattern or uuid")
        identifier = {"pattern": pattern} if pattern else {"uuid": uuid}
        return self.client.getAdvertisedPatterns(**identifier)["return"]["advertisedPatterns"]

    def get_advertised_patterns(self, tagfilter={"pattern": "", "description": ""}):
        """
        List advertised patterns.
        :param tagfilter: AXL returned tags to include, e.g. {'pattern': ''}
        :return: list of advertisedPatterns dictionaries, empty when nothing matches
        

        Schema: `ListAdvertisedPatternsReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listAdvertisedPatterns(
            {"pattern": "%"}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("advertisedPatterns") or []

    def update_advertised_pattern(self, **args):
        """
        Update an advertised pattern.
        :param pattern: pattern string (or uuid)
        :param uuid: pattern uuid (or pattern)
        :param description: new description
        :return: result dictionary
        

        Schema: `UpdateAdvertisedPatternsReq`: optional `description`, `newPattern`, `patternType`, `hostedRoutePSTNRule`, `pstnFailStrip`, `pstnFailPrepend`; one of `uuid`, or `pattern`.
        """
        return self.client.updateAdvertisedPatterns(**args)

    def remove_advertised_pattern(self, pattern="", uuid=""):
        """
        Remove an advertised pattern.
        :param pattern: pattern string (or uuid)
        :param uuid: pattern uuid (or pattern)
        :return: result dictionary
        

        Schema: `RemoveAdvertisedPatternsReq`: one of `pattern`, or `uuid`.
        """
        if bool(pattern) == bool(uuid):
            raise ValueError("Provide exactly one of pattern or uuid")
        identifier = {"pattern": pattern} if pattern else {"uuid": uuid}
        return self.client.removeAdvertisedPatterns(**identifier)

    # ------------------------------------------------------------------ #
    # IlsConfig                                                            #
    # ------------------------------------------------------------------ #

    _ILS_CONFIG_TAGS = {
        "clusterId": "",
        "lastContactTime": "",
        "clusterUriString": "",
        "role": "",
        "lastDataRecieved": "",
        "syncronizationStatus": "",
    }

    def get_ils_config(self, clusterId="", tagfilter=None):
        """
        Get the ILS configuration.
        :param clusterId: cluster ID (optional; omit to get local cluster config)
        :param tagfilter: dict of NewIlsConfig fields to return; defaults to all known fields
        :return: ilsConfig dictionary
        

        Schema: `GetIlsConfigReq`: `returnedTags`; optional `clusterId`.
        """
        if tagfilter is None:
            tagfilter = self._ILS_CONFIG_TAGS
        kwargs = {"returnedTags": tagfilter}
        if clusterId:
            kwargs["clusterId"] = clusterId
        return self.client.getIlsConfig(**kwargs)["return"]["ilsConfig"]

    def update_ils_config(self, **args):
        """
        Update the ILS configuration.
        :param role: ILS role, e.g. 'Hub Cluster' or 'Spoke Cluster'
        :param registrationServer: ILS registration server address
        :param activateIls: boolean, activate ILS (dummy tag per WSDL)
        :return: result dictionary
        

        Schema: `UpdateIlsConfigReq`: `role` + `registrationServer` + `activateIls` + `synchronizeClustersEvery` + `activatedServers` + `deactivatedServers` + `useTls` + `enableUsePassword` + `usePassword`.
        """
        return self.client.updateIlsConfig(**args)

    # ------------------------------------------------------------------ #
    # ImportedDirectoryUriCatalogs                                         #
    # ------------------------------------------------------------------ #

    def add_imported_directory_uri_catalog(self, **args):
        """
        Add an imported directory URI catalog.
        :param name: catalog name — required
        :param description: description
        :param routeString: route string — required
        :param lastLoadedFileName: last loaded file name
        :param fileLoadDateTime: file load timestamp
        :return: result dictionary (uuid)
        

        Schema: `importedDirectoryUriCatalogs` -> `XImportedDirectoryUriCatalogs`: `name` + `routeString`; optional `description`, `lastLoadedFileName`, `fileLoadDateTime`.
        """
        obj = self._build_object(
            "addImportedDirectoryUriCatalogs",
            "importedDirectoryUriCatalogs",
            args,
        )
        return self.client.addImportedDirectoryUriCatalogs(
            importedDirectoryUriCatalogs=obj
        )

    def get_imported_directory_uri_catalog(self, name="", uuid=""):
        """
        Get an imported directory URI catalog.
        :param name: catalog name (or uuid)
        :param uuid: catalog uuid (or name)
        :return: importedDirectoryUriCatalogs dictionary
        

        Schema: `GetImportedDirectoryUriCatalogsReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getImportedDirectoryUriCatalogs(
            **self._identify(name=name, uuid=uuid)
        )["return"]["importedDirectoryUriCatalogs"]

    def get_imported_directory_uri_catalogs(
        self, tagfilter={"name": "", "description": "", "routeString": ""}
    ):
        """
        List imported directory URI catalogs.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of importedDirectoryUriCatalogs dictionaries, empty when nothing matches
        

        Schema: `ListImportedDirectoryUriCatalogsReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listImportedDirectoryUriCatalogs(
            {"name": "%"}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("importedDirectoryUriCatalogs") or []

    def update_imported_directory_uri_catalog(self, **args):
        """
        Update an imported directory URI catalog.
        :param name: catalog name (or uuid)
        :param uuid: catalog uuid (or name)
        :param newName: new catalog name
        :param description: new description
        :param routeString: new route string
        :return: result dictionary
        

        Schema: `UpdateImportedDirectoryUriCatalogsReq`: optional `newName`, `description`, `routeString`.
        """
        return self.client.updateImportedDirectoryUriCatalogs(**args)

    def remove_imported_directory_uri_catalog(self, name="", uuid=""):
        """
        Remove an imported directory URI catalog.
        :param name: catalog name (or uuid)
        :param uuid: catalog uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeImportedDirectoryUriCatalogs(
            **self._identify(name=name, uuid=uuid)
        )

    # ------------------------------------------------------------------ #
    # RemoteCluster                                                        #
    # ------------------------------------------------------------------ #

    def add_remote_cluster(self, **args):
        """
        Add a remote cluster.
        :param clusterId: cluster ID — required
        :param fullyQualifiedName: FQDN or IP — required
        :param description: description
        :param emcc: EMCC service member config (dict)
        :param pstnAccess: PSTN access service member config (dict)
        :param rsvpAgent: RSVP agent service member config (dict)
        :param tftp: TFTP service member config (dict)
        :param lbm: LBM service member config (dict)
        :param uds: UDS service member config (dict)
        :return: result dictionary (uuid)
        

        Schema: `remoteCluster` -> `XRemoteCluster`: `clusterId` + `fullyQualifiedName`; optional `description`, `emcc`, `pstnAccess`, `rsvpAgent`, `tftp`, `lbm` and 1 more.
        """
        obj = self._build_object(
            "addRemoteCluster",
            "remoteCluster",
            args,
        )
        return self.client.addRemoteCluster(remoteCluster=obj)

    def get_remote_cluster(self, clusterId="", uuid=""):
        """
        Get a remote cluster.
        :param clusterId: cluster ID (or uuid)
        :param uuid: cluster uuid (or clusterId)
        :return: remoteCluster dictionary
        

        Schema: `GetRemoteClusterReq`: optional `returnedTags`; one of `clusterId`, or `uuid`.
        """
        if uuid:
            identifier = {"uuid": uuid}
        elif clusterId:
            identifier = {"clusterId": clusterId}
        else:
            raise ValueError("Provide either clusterId or uuid")
        return self.client.getRemoteCluster(**identifier)["return"]["remoteCluster"]

    def get_remote_clusters(self, tagfilter={"clusterId": "", "description": ""}):
        """
        List remote clusters.
        :param tagfilter: AXL returned tags to include, e.g. {'clusterId': ''}
        :return: list of remoteCluster dictionaries, empty when nothing matches
        

        Schema: `ListRemoteClusterReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listRemoteCluster(
            {"clusterId": "%"}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("remoteCluster") or []

    def update_remote_cluster(self, **args):
        """
        Update a remote cluster.
        :param clusterId: cluster ID (or uuid)
        :param uuid: cluster uuid (or clusterId)
        :param emcc: EMCC service member config (dict)
        :param pstnAccess: PSTN access service member config (dict)
        :param rsvpAgent: RSVP agent service member config (dict)
        :param tftp: TFTP service member config (dict)
        :param lbm: LBM service member config (dict)
        :param uds: UDS service member config (dict)
        :return: result dictionary
        

        Schema: `UpdateRemoteClusterReq`: optional `emcc`, `pstnAccess`, `rsvpAgent`, `tftp`, `lbm`, `uds`; one of `uuid`, or `clusterId`.
        """
        return self.client.updateRemoteCluster(**args)

    def remove_remote_cluster(self, clusterId="", uuid=""):
        """
        Remove a remote cluster.
        :param clusterId: cluster ID (or uuid)
        :param uuid: cluster uuid (or clusterId)
        :return: result dictionary
        

        Schema: `RemoveRemoteClusterReq`: one of `clusterId`, or `uuid`.
        """
        if uuid:
            identifier = {"uuid": uuid}
        elif clusterId:
            identifier = {"clusterId": clusterId}
        else:
            raise ValueError("Provide either clusterId or uuid")
        return self.client.removeRemoteCluster(**identifier)

    # ------------------------------------------------------------------ #
    # doUpdateRemoteCluster                                                #
    # ------------------------------------------------------------------ #

    def do_update_remote_cluster(self, server, clusterId):
        """
        Force-synchronise remote cluster data from a specific server.
        :param server: server address (hostname or IP) — required
        :param clusterId: remote cluster ID — required
        :return: result value string
        

        Schema: `DoUpdateRemoteClusterReq`: `server` + `clusterId`.
        """
        return self.client.doUpdateRemoteCluster(server=server, clusterId=clusterId)

    # ------------------------------------------------------------------ #
    # Smart Licensing — do* actions                                        #
    # ------------------------------------------------------------------ #

    def do_smart_entitlement_request(self):
        """
        Send an entitlement request to Cisco Smart Software Manager or satellite.
        :return: result string ('Success' or 'Failure')
        """
        return self.client.doSmartEntitlementRequest()

    def do_smart_license_de_register(self):
        """
        De-register this CUCM cluster from Cisco Smart Software Manager.
        :return: result string ('Success' or 'Failure')
        """
        return self.client.doSmartLicenseDeRegister()

    def do_smart_license_re_register(self, token):
        """
        Force re-register with Cisco Smart Software Manager (cluster already registered).
        :param token: smart license registration token — required
        :return: result string ('Success' or 'Failure')
        

        Schema: `DoSmartLicenseReRegisterReq`: `token`.
        """
        return self.client.doSmartLicenseReRegister(token=token)

    def do_smart_license_register(self, token, force):
        """
        Register this CUCM cluster with Cisco Smart Software Manager or satellite.
        :param token: smart license registration token — required
        :param force: boolean, force registration even if already registered — required
        :return: result string ('Success' or 'Failure')
        

        Schema: `DoSmartLicenseRegisterReq`: `token` + `force`.
        """
        return self.client.doSmartLicenseRegister(token=token, force=force)

    def do_smart_license_renew_authorization(self):
        """
        Renew Smart License authorization with Cisco Smart Software Manager.
        :return: result string ('Success' or 'Failure')
        """
        return self.client.doSmartLicenseRenewAuthorization()

    def do_smart_license_renew_registration(self):
        """
        Renew Smart License registration with Cisco Smart Software Manager.
        :return: result string ('Success' or 'Failure')
        """
        return self.client.doSmartLicenseRenewRegistration()

    # ------------------------------------------------------------------ #
    # License usage                                                        #
    # ------------------------------------------------------------------ #

    def do_update_license_usage(self):
        """
        Trigger a license usage update on this CUCM cluster.
        :return: result string ('true' or 'false')
        """
        return self.client.doUpdateLicenseUsage()
