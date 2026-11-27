"""Media resource, mobility, announcement, and call-control wrappers.

Entities
--------
Media:
  MeetMe, MohAudioSource, MohServer, RecordingProfile, RegionMatrix

Mobility / Presence:
  DeviceMobility, DeviceMobilityGroup, MobileVoiceAccess, Mobility,
  MobilityProfile, PhysicalLocation, PresenceGroup

Call control / Announcements:
  CalledPartyTracing, CmcInfo, ElinGroup, ExternalCallControlProfile,
FacInfo, TransPatternOptions, TransformationProfile, H323Trunk,
SipProfileOptions, Announcement, Annunciator, AudioCodecPreferenceList,
ConferenceNow, FixedMohAudioSource, InteractiveVoiceResponse,
CallerFilterList, EnterpriseFeatureAccessConfiguration, TodAccess
"""


class MediaMixin:
    """Media resource, mobility, announcement, and call-control wrappers."""

    # ------------------------------------------------------------------
    # MeetMe
    # ------------------------------------------------------------------

    def add_meet_me(self, **args):
        """Add a MeetMe conference number.

        Schema: `meetMe` -> `XMeetMe`: `pattern` + `minimumSecurityLevel`; optional `description`, `routePartitionName`.
        """
        return self.client.addMeetMe(self._build_object("addMeetMe", "meetMe", args))

    def get_meet_me(self, **args):
        """Get a MeetMe by pattern/partition or uuid.

        Schema: `GetMeetMeReq`: optional `returnedTags`; one of `uuid`, or (`pattern`; optional `routePartitionName`).
        """
        return self.client.getMeetMe(**args)["return"]["meetMe"]

    def get_meet_mes(self, tagfilter=None):
        """List all MeetMe records. Returns [] when nothing matches.

        Schema: `ListMeetMeReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"pattern": ""}
        result = self.client.listMeetMe({"pattern": "%"}, returnedTags=tags)["return"]
        return (result or {}).get("meetMe") or []

    def update_meet_me(self, **args):
        """Update a MeetMe.

        Schema: `UpdateMeetMeReq`: optional `newPattern`, `description`, `newRoutePartitionName`, `minimumSecurityLevel`; one of `uuid`, or (`pattern`; optional `routePartitionName`).
        """
        return self.client.updateMeetMe(**args)

    def delete_meet_me(self, name="", uuid=""):
        """Delete a MeetMe by name (pattern) or uuid.

        Schema: `RemoveMeetMeReq`: one of `uuid`, or (`pattern`; optional `routePartitionName`).
        """
        return self.client.removeMeetMe(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------
    # MohAudioSource  (no add — read-only source registry)
    # Note: identity is sourceId or uuid, not name.
    # ------------------------------------------------------------------

    def get_moh_audio_source(self, **args):
        """Get a MohAudioSource by sourceId or uuid.

        Schema: `GetMohAudioSourceReq`: optional `returnedTags`; one of `sourceId`, or `uuid`.
        """
        return self.client.getMohAudioSource(**args)["return"]["mohAudioSource"]

    def get_moh_audio_sources(self, tagfilter=None):
        """List all MohAudioSource records. Returns [] when nothing matches.

        Schema: `ListMohAudioSourceReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listMohAudioSource({"name": "%"}, returnedTags=tags)["return"]
        return (result or {}).get("mohAudioSource") or []

    def update_moh_audio_source(self, **args):
        """Update a MohAudioSource (identified by sourceId or uuid).

        Schema: `UpdateMohAudioSourceReq`: optional `newName`, `sourceFile`, `multicast`, `mohFileStatus`, `initialAnnouncement`, `periodicAnnouncement` and 4 more; one of `uuid`, or `sourceId`.
        """
        return self.client.updateMohAudioSource(**args)

    def delete_moh_audio_source(self, source_id=None, uuid=""):
        """Delete a MohAudioSource by sourceId or uuid.

        Schema: `RemoveMohAudioSourceReq`: one of `sourceId`, or `uuid`.
        """
        if source_id:
            return self.client.removeMohAudioSource(sourceId=source_id)
        if uuid:
            return self.client.removeMohAudioSource(uuid=uuid)
        raise ValueError("delete_moh_audio_source requires source_id or uuid")

    # ------------------------------------------------------------------
    # MohServer  (no add, no remove)
    # ------------------------------------------------------------------

    def get_moh_server(self, **args):
        """Get a MohServer by name or uuid.

        Schema: `GetMohServerReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getMohServer(**args)["return"]["mohServer"]

    def get_moh_servers(self, tagfilter=None):
        """List all MohServer records. Returns [] when nothing matches.

        Schema: `ListMohServerReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listMohServer({"name": "%"}, returnedTags=tags)["return"]
        return (result or {}).get("mohServer") or []

    def update_moh_server(self, **args):
        """Update a MohServer.

        Schema: `UpdateMohServerReq`: optional `newName`, `description`, `devicePoolName`, `locationName`, `maxUnicastConnections`, `maxMulticastConnections` and 8 more.
        """
        return self.client.updateMohServer(**args)

    # ------------------------------------------------------------------
    # RecordingProfile
    # ------------------------------------------------------------------

    def add_recording_profile(self, **args):
        """Add a RecordingProfile.

        Schema: `recordingProfile` -> `XRecordingProfile`: `name` + `recorderDestination`; optional `recordingCssName`.
        """
        return self.client.addRecordingProfile(
            self._build_object("addRecordingProfile", "recordingProfile", args)
        )

    def get_recording_profile(self, **args):
        """Get a RecordingProfile by name or uuid.

        Schema: `GetRecordingProfileReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getRecordingProfile(**args)["return"]["recordingProfile"]

    def get_recording_profiles(self, tagfilter=None):
        """List all RecordingProfiles. Returns [] when nothing matches.

        Schema: `ListRecordingProfileReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listRecordingProfile({"name": "%"}, returnedTags=tags)["return"]
        return (result or {}).get("recordingProfile") or []

    def update_recording_profile(self, **args):
        """Update a RecordingProfile.

        Schema: `UpdateRecordingProfileReq`: optional `newName`, `recordingCssName`, `recorderDestination`.
        """
        return self.client.updateRecordingProfile(**args)

    def delete_recording_profile(self, name="", uuid=""):
        """Delete a RecordingProfile by name or uuid.

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeRecordingProfile(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------
    # RegionMatrix  (update only)
    # Identified by (regionAName + regionBName) or uuid.
    # ------------------------------------------------------------------

    def update_region_matrix(self, **args):
        """Update a RegionMatrix entry (regionAName + regionBName or uuid).

        Schema: `UpdateRegionMatrixReq`: optional `bandwidth`, `videoBandwidth`, `codecPreference`; one of `uuid`, or (`regionAName` + `regionBName`).
        """
        return self.client.updateRegionMatrix(**args)

    # ------------------------------------------------------------------
    # DeviceMobility
    # ------------------------------------------------------------------

    def add_device_mobility(self, **args):
        """Add a DeviceMobility record.

        Schema: `deviceMobility` -> `XDeviceMobility`: `name` + `subNetDetails` + `members`.
        """
        return self.client.addDeviceMobility(
            self._build_object("addDeviceMobility", "deviceMobility", args)
        )

    def get_device_mobility(self, **args):
        """Get a DeviceMobility by name or uuid.

        Schema: `GetDeviceMobilityReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getDeviceMobility(**args)["return"]["deviceMobility"]

    def get_device_mobilities(self, tagfilter=None):
        """List all DeviceMobility records. Returns [] when nothing matches.

        Schema: `ListDeviceMobilityReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listDeviceMobility({"name": "%"}, returnedTags=tags)["return"]
        return (result or {}).get("deviceMobility") or []

    def update_device_mobility(self, **args):
        """Update a DeviceMobility.

        Schema: `UpdateDeviceMobilityReq`: optional `newName`, `subNetDetails`, optional choice of (optional `removeMembers`, `addMembers`), or `members`.
        """
        return self.client.updateDeviceMobility(**args)

    def delete_device_mobility(self, name="", uuid=""):
        """Delete a DeviceMobility by name or uuid.

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeDeviceMobility(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------
    # DeviceMobilityGroup
    # ------------------------------------------------------------------

    def add_device_mobility_group(self, **args):
        """Add a DeviceMobilityGroup.

        Schema: `deviceMobilityGroup` -> `XDeviceMobilityGroup`: `name`; optional `description`.
        """
        return self.client.addDeviceMobilityGroup(
            self._build_object("addDeviceMobilityGroup", "deviceMobilityGroup", args)
        )

    def get_device_mobility_group(self, **args):
        """Get a DeviceMobilityGroup by name or uuid.

        Schema: `GetDeviceMobilityGroupReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getDeviceMobilityGroup(**args)["return"]["deviceMobilityGroup"]

    def get_device_mobility_groups(self, tagfilter=None):
        """List all DeviceMobilityGroups. Returns [] when nothing matches.

        Schema: `ListDeviceMobilityGroupReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listDeviceMobilityGroup({"name": "%"}, returnedTags=tags)["return"]
        return (result or {}).get("deviceMobilityGroup") or []

    def update_device_mobility_group(self, **args):
        """Update a DeviceMobilityGroup.

        Schema: `UpdateDeviceMobilityGroupReq`: optional `newName`, `description`.
        """
        return self.client.updateDeviceMobilityGroup(**args)

    def delete_device_mobility_group(self, name="", uuid=""):
        """Delete a DeviceMobilityGroup by name or uuid.

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeDeviceMobilityGroup(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------
    # MobileVoiceAccess
    # Note: identified by pattern or uuid (not name).
    # ------------------------------------------------------------------

    def add_mobile_voice_access(self, **args):
        """Add a MobileVoiceAccess entry.

        Schema: `mobileVoiceAccess` -> `XMobileVoiceAccess`: `pattern` + `locales`; optional `routePartitionName`.
        """
        return self.client.addMobileVoiceAccess(
            self._build_object("addMobileVoiceAccess", "mobileVoiceAccess", args)
        )

    def get_mobile_voice_access(self, **args):
        """Get a MobileVoiceAccess by pattern or uuid.

        Schema: `GetMobileVoiceAccessReq`: optional `returnedTags`; one of `pattern`, or `uuid`.
        """
        return self.client.getMobileVoiceAccess(**args)["return"]["mobileVoiceAccess"]

    def update_mobile_voice_access(self, **args):
        """Update a MobileVoiceAccess.

        Schema: `UpdateMobileVoiceAccessReq`: optional `newPattern`, `routePartitionName`, optional choice of (optional `removeLocales`, `addLocales`), or `locales`; one of `uuid`, or `pattern`.
        """
        return self.client.updateMobileVoiceAccess(**args)

    def delete_mobile_voice_access(self, pattern="", uuid=""):
        """Delete a MobileVoiceAccess by pattern or uuid.

        Schema: `RemoveMobileVoiceAccessReq`: one of `pattern`, or `uuid`.
        """
        if pattern:
            return self.client.removeMobileVoiceAccess(pattern=pattern)
        if uuid:
            return self.client.removeMobileVoiceAccess(uuid=uuid)
        raise ValueError("delete_mobile_voice_access requires pattern or uuid")

    # ------------------------------------------------------------------
    # Mobility  (no remove, no list)
    # Note: identified by handoffNumber or DTMFNumber.
    # ------------------------------------------------------------------

    def add_mobility(self, **args):
        """Add a Mobility configuration.

        Schema: `mobility` -> `XMobility`: `handoffNumber` + `DTMFNumber`; optional `handoffPartitionName`, `DTMFPartitionName`.
        """
        return self.client.addMobility(self._build_object("addMobility", "mobility", args))

    def get_mobility(self, **args):
        """Get Mobility config by handoffNumber or DTMFNumber.

        Schema: `GetMobilityReq`: optional `returnedTags`; optional `handoffNumber`, `DTMFNumber`.
        """
        return self.client.getMobility(**args)["return"]["mobility"]

    def update_mobility(self, **args):
        """Update a Mobility configuration.

        Schema: `UpdateMobilityReq`: optional `handoffNumber`, `DTMFNumber`; optional `newHandoffNumber`, `newHandoffPartitionName`, `newDTMFNumber`, `newDTMFPartitionName`.
        """
        return self.client.updateMobility(**args)

    # ------------------------------------------------------------------
    # MobilityProfile
    # ------------------------------------------------------------------

    def add_mobility_profile(self, **args):
        """Add a MobilityProfile.

        Schema: `mobilityProfile` -> `XMobilityProfile`: `name`; optional `description`, `mobileClientCallingOption`, `dvofServiceAccessNumber`, `dirn`, `dvorCallerId`.
        """
        return self.client.addMobilityProfile(
            self._build_object("addMobilityProfile", "mobilityProfile", args)
        )

    def get_mobility_profile(self, **args):
        """Get a MobilityProfile by name or uuid.

        Schema: `GetMobilityProfileReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getMobilityProfile(**args)["return"]["mobilityProfile"]

    def get_mobility_profiles(self, tagfilter=None):
        """List all MobilityProfiles. Returns [] when nothing matches.

        Schema: `ListMobilityProfileReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listMobilityProfile({"name": "%"}, returnedTags=tags)["return"]
        return (result or {}).get("mobilityProfile") or []

    def update_mobility_profile(self, **args):
        """Update a MobilityProfile.

        Schema: `UpdateMobilityProfileReq`: optional `newName`, `description`, `mobileClientCallingOption`, `dvofServiceAccessNumber`, `dirn`, `dvorCallerId`.
        """
        return self.client.updateMobilityProfile(**args)

    def delete_mobility_profile(self, name="", uuid=""):
        """Delete a MobilityProfile by name or uuid.

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeMobilityProfile(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------
    # PhysicalLocation
    # ------------------------------------------------------------------

    def add_physical_location(self, **args):
        """Add a PhysicalLocation.

        Schema: `physicalLocation` -> `XPhysicalLocation`: `name`; optional `description`.
        """
        return self.client.addPhysicalLocation(
            self._build_object("addPhysicalLocation", "physicalLocation", args)
        )

    def get_physical_location(self, **args):
        """Get a PhysicalLocation by name or uuid.

        Schema: `GetPhysicalLocationReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getPhysicalLocation(**args)["return"]["physicalLocation"]

    def get_physical_locations(self, tagfilter=None):
        """List all PhysicalLocations. Returns [] when nothing matches.

        Schema: `ListPhysicalLocationReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listPhysicalLocation({"name": "%"}, returnedTags=tags)["return"]
        return (result or {}).get("physicalLocation") or []

    def update_physical_location(self, **args):
        """Update a PhysicalLocation.

        Schema: `UpdatePhysicalLocationReq`: optional `newName`, `description`.
        """
        return self.client.updatePhysicalLocation(**args)

    def delete_physical_location(self, name="", uuid=""):
        """Delete a PhysicalLocation by name or uuid.

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removePhysicalLocation(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------
    # PresenceGroup
    # ------------------------------------------------------------------

    def add_presence_group(self, **args):
        """Add a PresenceGroup.

        Schema: `presenceGroup` -> `XPresenceGroup`: `name`; optional `description`, `presenceGroups`.
        """
        return self.client.addPresenceGroup(
            self._build_object("addPresenceGroup", "presenceGroup", args)
        )

    def get_presence_group(self, **args):
        """Get a PresenceGroup by name or uuid.

        Schema: `GetPresenceGroupReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getPresenceGroup(**args)["return"]["presenceGroup"]

    def get_presence_groups(self, tagfilter=None):
        """List all PresenceGroups. Returns [] when nothing matches.

        Schema: `ListPresenceGroupReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listPresenceGroup({"name": "%"}, returnedTags=tags)["return"]
        return (result or {}).get("presenceGroup") or []

    def update_presence_group(self, **args):
        """Update a PresenceGroup.

        Schema: `UpdatePresenceGroupReq`: optional `newName`, `description`, `presenceGroups`.
        """
        return self.client.updatePresenceGroup(**args)

    def delete_presence_group(self, name="", uuid=""):
        """Delete a PresenceGroup by name or uuid.

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removePresenceGroup(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------
    # CalledPartyTracing
    # Identity: directorynumber or uuid  (no get, only add/list/remove)
    # ------------------------------------------------------------------

    def add_called_party_tracing(self, **args):
        """Add a CalledPartyTracing entry.

        Schema: `calledPartyTracing` -> `XCalledPartyTracing`: `directorynumber`; optional `description`.
        """
        return self.client.addCalledPartyTracing(
            self._build_object("addCalledPartyTracing", "calledPartyTracing", args)
        )

    def get_called_party_tracings(self, tagfilter=None):
        """List CalledPartyTracing records. Returns [] when nothing matches.

        Schema: `ListCalledPartyTracingReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"directorynumber": ""}
        result = self.client.listCalledPartyTracing(
            {"directorynumber": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("calledPartyTracing") or []

    def delete_called_party_tracing(self, directorynumber="", uuid=""):
        """Delete a CalledPartyTracing by directorynumber or uuid.

        Schema: `RemoveCalledPartyTracingReq`: one of `directorynumber`, or `uuid`.
        """
        if directorynumber:
            return self.client.removeCalledPartyTracing(directorynumber=directorynumber)
        if uuid:
            return self.client.removeCalledPartyTracing(uuid=uuid)
        raise ValueError("delete_called_party_tracing requires directorynumber or uuid")

    # ------------------------------------------------------------------
    # CmcInfo
    # Identity: code or uuid  (not name)
    # ------------------------------------------------------------------

    def add_cmc_info(self, **args):
        """Add a CmcInfo entry.

        Schema: `cmcInfo` -> `XCmcInfo`: `code`; optional `description`.
        """
        return self.client.addCmcInfo(self._build_object("addCmcInfo", "cmcInfo", args))

    def get_cmc_info(self, **args):
        """Get a CmcInfo by code or uuid.

        Schema: `GetCmcInfoReq`: optional `returnedTags`; one of `code`, or `uuid`.
        """
        return self.client.getCmcInfo(**args)["return"]["cmcInfo"]

    def get_cmc_infos(self, tagfilter=None):
        """List CmcInfo records. Returns [] when nothing matches.

        Schema: `ListCmcInfoReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"code": ""}
        result = self.client.listCmcInfo({"code": "%"}, returnedTags=tags)["return"]
        return (result or {}).get("cmcInfo") or []

    def update_cmc_info(self, **args):
        """Update a CmcInfo (identified by code or uuid).

        Schema: `UpdateCmcInfoReq`: optional `newCode`, `description`; one of `uuid`, or `code`.
        """
        return self.client.updateCmcInfo(**args)

    def delete_cmc_info(self, code="", uuid=""):
        """Delete a CmcInfo by code or uuid.

        Schema: `RemoveCmcInfoReq`: one of `code`, or `uuid`.
        """
        if code:
            return self.client.removeCmcInfo(code=code)
        if uuid:
            return self.client.removeCmcInfo(uuid=uuid)
        raise ValueError("delete_cmc_info requires code or uuid")

    # ------------------------------------------------------------------
    # ElinGroup
    # ------------------------------------------------------------------

    def add_elin_group(self, **args):
        """Add an ElinGroup.

        Schema: `elinGroup` -> `XElinGroup`: `name` + `elinNumbers`; optional `description`.
        """
        return self.client.addElinGroup(self._build_object("addElinGroup", "elinGroup", args))

    def get_elin_group(self, **args):
        """Get an ElinGroup by name or uuid.

        Schema: `GetElinGroupReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getElinGroup(**args)["return"]["elinGroup"]

    def get_elin_groups(self, tagfilter=None):
        """List ElinGroup records. Returns [] when nothing matches.

        Schema: `ListElinGroupReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listElinGroup({"name": "%"}, returnedTags=tags)["return"]
        return (result or {}).get("elinGroup") or []

    def update_elin_group(self, **args):
        """Update an ElinGroup.

        Schema: `UpdateElinGroupReq`: optional `newName`, `description`, optional choice of (optional `removeElinNumbers`, `addElinNumbers`), or `elinNumbers`.
        """
        return self.client.updateElinGroup(**args)

    def delete_elin_group(self, name="", uuid=""):
        """Delete an ElinGroup by name or uuid.

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeElinGroup(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------
    # ExternalCallControlProfile
    # ------------------------------------------------------------------

    def add_external_call_control_profile(self, **args):
        """Add an ExternalCallControlProfile.

        Schema: `externalCallControlProfile` -> `XExternalCallControlProfile`: `name` + `primaryUri` + `callTreatmentOnFailure`; optional `secondaryUri`, `enableLoadBalancing`, `routingRequestTimer`, `diversionReroutingCssName`.
        """
        return self.client.addExternalCallControlProfile(
            self._build_object("addExternalCallControlProfile", "externalCallControlProfile", args)
        )

    def get_external_call_control_profile(self, **args):
        """Get an ExternalCallControlProfile by name or uuid.

        Schema: `GetExternalCallControlProfileReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getExternalCallControlProfile(**args)["return"][
            "externalCallControlProfile"
        ]

    def get_external_call_control_profiles(self, tagfilter=None):
        """List ExternalCallControlProfile records. Returns [] when nothing matches.

        Schema: `ListExternalCallControlProfileReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listExternalCallControlProfile(
            {"name": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("externalCallControlProfile") or []

    def update_external_call_control_profile(self, **args):
        """Update an ExternalCallControlProfile.

        Schema: `UpdateExternalCallControlProfileReq`: optional `newName`, `primaryUri`, `secondaryUri`, `enableLoadBalancing`, `routingRequestTimer`, `diversionReroutingCssName` and 1 more.
        """
        return self.client.updateExternalCallControlProfile(**args)

    def delete_external_call_control_profile(self, name="", uuid=""):
        """Delete an ExternalCallControlProfile by name or uuid.

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeExternalCallControlProfile(
            **self._identify(name=name, uuid=uuid)
        )

    # ------------------------------------------------------------------
    # FacInfo
    # Identity: name or uuid
    # ------------------------------------------------------------------

    def add_fac_info(self, **args):
        """Add a FacInfo entry.

        Schema: `facInfo` -> `XFacInfo`: `name` + `code` + `authorizationLevel`.
        """
        return self.client.addFacInfo(self._build_object("addFacInfo", "facInfo", args))

    def get_fac_info(self, **args):
        """Get a FacInfo by name or uuid.

        Schema: `GetFacInfoReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getFacInfo(**args)["return"]["facInfo"]

    def get_fac_infos(self, tagfilter=None):
        """List FacInfo records. Returns [] when nothing matches.

        Schema: `ListFacInfoReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listFacInfo({"name": "%"}, returnedTags=tags)["return"]
        return (result or {}).get("facInfo") or []

    def update_fac_info(self, **args):
        """Update a FacInfo.

        Schema: `UpdateFacInfoReq`: optional `newName`, `code`, `authorizationLevel`.
        """
        return self.client.updateFacInfo(**args)

    def delete_fac_info(self, name="", uuid=""):
        """Delete a FacInfo by name or uuid.

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeFacInfo(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------
    # TransPatternOptions  (get-only — no add/update/remove/list)
    # ------------------------------------------------------------------

    def get_trans_pattern_options(self, **args):
        """Get translation-pattern option choices. Returns the ``transPattern`` object.

        Schema: `GetTransPatternOptionsReq`: optional `returnedChoices`; one of `uuid`.
        """
        return self.client.getTransPatternOptions(**args)["return"]["transPattern"]

    # ------------------------------------------------------------------
    # TransformationProfile
    # ------------------------------------------------------------------

    def add_transformation_profile(self, **args):
        """Add a TransformationProfile.

        Schema: `transformationProfile` -> `XTransformationProfile`: `name`; optional `description`, `nationalStripDigits`, `internationalStripDigits`, `unknownStripDigits`, `subscriberStripDigits`, `nationalPrefix` and 7 more.
        """
        return self.client.addTransformationProfile(
            self._build_object("addTransformationProfile", "transformationProfile", args)
        )

    def get_transformation_profile(self, **args):
        """Get a TransformationProfile by name or uuid.

        Schema: `GetTransformationProfileReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getTransformationProfile(**args)["return"]["transformationProfile"]

    def get_transformation_profiles(self, tagfilter=None):
        """List TransformationProfile records. Returns [] when nothing matches.

        Schema: `ListTransformationProfileReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listTransformationProfile({"name": "%"}, returnedTags=tags)["return"]
        return (result or {}).get("transformationProfile") or []

    def update_transformation_profile(self, **args):
        """Update a TransformationProfile.

        Schema: `UpdateTransformationProfileReq`: optional `newName`, `description`, `nationalStripDigits`, `internationalStripDigits`, `unknownStripDigits`, `subscriberStripDigits` and 8 more.
        """
        return self.client.updateTransformationProfile(**args)

    def delete_transformation_profile(self, name="", uuid=""):
        """Delete a TransformationProfile by name or uuid.

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeTransformationProfile(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------
    # H323Trunk
    # ------------------------------------------------------------------

    def add_h323_trunk(self, **args):
        """Add an H323Trunk.

        Schema: `h323Trunk` -> `XH323Trunk`: `name` + `product` + `class` + `protocol` + `protocolSide` + `devicePoolName` + `locationName`; optional `description`, `callingSearchSpaceName`, `commonDeviceConfigName`, `networkLocation`, `mediaResourceListName`, `aarNeighborhoodName` and 87 more; one of `gateKeeperInfo`.
        """
        return self.client.addH323Trunk(
            self._build_object("addH323Trunk", "h323Trunk", args)
        )

    def get_h323_trunk(self, **args):
        """Get an H323Trunk by name or uuid.

        Schema: `GetH323TrunkReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getH323Trunk(**args)["return"]["h323Trunk"]

    def get_h323_trunks(self, tagfilter=None):
        """List H323Trunk records. Returns [] when nothing matches.

        Schema: `ListH323TrunkReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listH323Trunk({"name": "%"}, returnedTags=tags)["return"]
        return (result or {}).get("h323Trunk") or []

    def update_h323_trunk(self, **args):
        """Update an H323Trunk.

        Schema: `UpdateH323TrunkReq`: optional `newName`, `description`, `callingSearchSpaceName`, `devicePoolName`, `commonDeviceConfigName`, `networkLocation` and 91 more.
        """
        return self.client.updateH323Trunk(**args)

    def delete_h323_trunk(self, name="", uuid=""):
        """Delete an H323Trunk by name or uuid.

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeH323Trunk(**self._identify(name=name, uuid=uuid))

    def reset_h323_trunk(self, name="", uuid=""):
        """Reset an H323Trunk by name or uuid.

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.resetH323Trunk(**self._identify(name=name, uuid=uuid))

    def restart_h323_trunk(self, name="", uuid=""):
        """Restart an H323Trunk by name or uuid.

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.restartH323Trunk(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------
    # SipProfileOptions  (get-only)
    # ------------------------------------------------------------------

    def get_sip_profile_options(self, **args):
        """Get SIP profile option choices. Returns the ``sipProfile`` object.

        Schema: `GetSipProfileOptionsReq`: optional `returnedChoices`; one of `uuid`.
        """
        return self.client.getSipProfileOptions(**args)["return"]["sipProfile"]

    # ------------------------------------------------------------------
    # Announcement
    # ------------------------------------------------------------------

    def add_announcement(self, **args):
        """Add an Announcement.

        Schema: `announcement` -> `XAnnouncement`: `name`; optional `description`, `announcementFile`.
        """
        return self.client.addAnnouncement(
            self._build_object("addAnnouncement", "announcement", args)
        )

    def get_announcement(self, **args):
        """Get an Announcement by name or uuid.

        Schema: `GetAnnouncementReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getAnnouncement(**args)["return"]["announcement"]

    def get_announcements(self, tagfilter=None):
        """List Announcement records. Returns [] when nothing matches.

        Schema: `ListAnnouncementReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listAnnouncement({"name": "%"}, returnedTags=tags)["return"]
        return (result or {}).get("announcement") or []

    def update_announcement(self, **args):
        """Update an Announcement.

        Schema: `UpdateAnnouncementReq`: optional `newName`, `description`, `announcementFile`.
        """
        return self.client.updateAnnouncement(**args)

    def delete_announcement(self, name="", uuid=""):
        """Delete an Announcement by name or uuid.

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeAnnouncement(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------
    # Annunciator  (no add, no remove)
    # ------------------------------------------------------------------

    def get_annunciator(self, **args):
        """Get an Annunciator by name or uuid.

        Schema: `GetAnnunciatorReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getAnnunciator(**args)["return"]["annunciator"]

    def get_annunciators(self, tagfilter=None):
        """List Annunciator records. Returns [] when nothing matches.

        Schema: `ListAnnunciatorReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listAnnunciator({"name": "%"}, returnedTags=tags)["return"]
        return (result or {}).get("annunciator") or []

    def update_annunciator(self, **args):
        """Update an Annunciator.

        Schema: `UpdateAnnunciatorReq`: optional `newName`, `description`, `devicePoolName`, `locationName`, `useTrustedRelayPoint`.
        """
        return self.client.updateAnnunciator(**args)

    # ------------------------------------------------------------------
    # AudioCodecPreferenceList
    # ------------------------------------------------------------------

    def add_audio_codec_preference_list(self, **args):
        """Add an AudioCodecPreferenceList.

        Schema: `audioCodecPreferenceList` -> `XAudioCodecPreferenceList`: `name` + `description` + `codecsInList`.
        """
        return self.client.addAudioCodecPreferenceList(
            self._build_object("addAudioCodecPreferenceList", "audioCodecPreferenceList", args)
        )

    def get_audio_codec_preference_list(self, **args):
        """Get an AudioCodecPreferenceList by name or uuid.

        Schema: `GetAudioCodecPreferenceListReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getAudioCodecPreferenceList(**args)["return"][
            "audioCodecPreferenceList"
        ]

    def get_audio_codec_preference_lists(self, tagfilter=None):
        """List AudioCodecPreferenceList records. Returns [] when nothing matches.

        Schema: `ListAudioCodecPreferenceListReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listAudioCodecPreferenceList(
            {"name": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("audioCodecPreferenceList") or []

    def update_audio_codec_preference_list(self, **args):
        """Update an AudioCodecPreferenceList.

        Schema: `UpdateAudioCodecPreferenceListReq`: optional `newName`, `description`, `codecsInList`.
        """
        return self.client.updateAudioCodecPreferenceList(**args)

    def delete_audio_codec_preference_list(self, name="", uuid=""):
        """Delete an AudioCodecPreferenceList by name or uuid.

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeAudioCodecPreferenceList(
            **self._identify(name=name, uuid=uuid)
        )

    # ------------------------------------------------------------------
    # ConferenceNow
    # Identity: conferenceNowNumber (not name) for list; name/uuid for get/remove
    # ------------------------------------------------------------------

    def add_conference_now(self, **args):
        """Add a ConferenceNow entry.

        Schema: `conferenceNow` -> `XConferenceNow`: `conferenceNowNumber` + `maxWaitTimeForHost`; optional `routePartitionName`, `description`, `MohAudioSourceId`.
        """
        return self.client.addConferenceNow(
            self._build_object("addConferenceNow", "conferenceNow", args)
        )

    def get_conference_now(self, **args):
        """Get a ConferenceNow by conferenceNowNumber/name or uuid.

        Schema: `GetConferenceNowReq`: optional `returnedTags`; one of `uuid`, or (`conferenceNowNumber`; optional `routePartitionName`).
        """
        return self.client.getConferenceNow(**args)["return"]["conferenceNow"]

    def get_conference_nows(self, tagfilter=None):
        """List ConferenceNow records. Returns [] when nothing matches.

        Schema: `ListConferenceNowReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"conferenceNowNumber": ""}
        result = self.client.listConferenceNow(
            {"conferenceNowNumber": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("conferenceNow") or []

    def update_conference_now(self, **args):
        """Update a ConferenceNow.

        Schema: `UpdateConferenceNowReq`: optional `newConferenceNowNumber`, `newRoutePartitionName`, `description`, `maxWaitTimeForHost`, `MohAudioSourceId`; one of `uuid`, or (`conferenceNowNumber`; optional `routePartitionName`).
        """
        return self.client.updateConferenceNow(**args)

    def delete_conference_now(self, conferenceNowNumber="", uuid=""):
        """Delete a ConferenceNow by conferenceNowNumber or uuid.

        Schema: `RemoveConferenceNowReq`: one of `uuid`, or (`conferenceNowNumber`; optional `routePartitionName`).
        """
        if conferenceNowNumber:
            return self.client.removeConferenceNow(conferenceNowNumber=conferenceNowNumber)
        if uuid:
            return self.client.removeConferenceNow(uuid=uuid)
        raise ValueError("delete_conference_now requires conferenceNowNumber or uuid")

    # ------------------------------------------------------------------
    # FixedMohAudioSource  (get/update only — no add/remove/list)
    # ------------------------------------------------------------------

    def get_fixed_moh_audio_source(self, **args):
        """Get a FixedMohAudioSource by sourceId or uuid.

        Schema: `GetFixedMohAudioSourceReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getFixedMohAudioSource(**args)["return"]["fixedMohAudioSource"]

    def update_fixed_moh_audio_source(self, **args):
        """Update a FixedMohAudioSource.

        Schema: `UpdateFixedMohAudioSourceReq`: optional `newName`, `multicast`, `enable`, `initialAnnouncement`, `periodicAnnouncement`, `periodicAnnouncementInterval` and 2 more.
        """
        return self.client.updateFixedMohAudioSource(**args)

    # ------------------------------------------------------------------
    # InteractiveVoiceResponse  (no add, no remove)
    # ------------------------------------------------------------------

    def get_interactive_voice_response(self, **args):
        """Get an InteractiveVoiceResponse by name or uuid.

        Schema: `GetInteractiveVoiceResponseReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getInteractiveVoiceResponse(**args)["return"][
            "interactiveVoiceResponse"
        ]

    def get_interactive_voice_responses(self, tagfilter=None):
        """List InteractiveVoiceResponse records. Returns [] when nothing matches.

        Schema: `ListInteractiveVoiceResponseReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listInteractiveVoiceResponse(
            {"name": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("interactiveVoiceResponse") or []

    def update_interactive_voice_response(self, **args):
        """Update an InteractiveVoiceResponse.

        Schema: `UpdateInteractiveVoiceResponseReq`: optional `newName`, `description`, `devicePoolName`, `locationName`, `useTrustedRelayPoint`.
        """
        return self.client.updateInteractiveVoiceResponse(**args)

    # ------------------------------------------------------------------
    # CallerFilterList
    # ------------------------------------------------------------------

    def add_caller_filter_list(self, **args):
        """Add a CallerFilterList.

        Schema: `callerFilterList` -> `XCallerFilterList`: `name` + `isAllowedType`; optional `description`, `endUserIdName`, `members`.
        """
        return self.client.addCallerFilterList(
            self._build_object("addCallerFilterList", "callerFilterList", args)
        )

    def get_caller_filter_list(self, **args):
        """Get a CallerFilterList by name or uuid.

        Schema: `GetCallerFilterListReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getCallerFilterList(**args)["return"]["callerFilterList"]

    def get_caller_filter_lists(self, tagfilter=None):
        """List CallerFilterList records. Returns [] when nothing matches.

        Schema: `ListCallerFilterListReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listCallerFilterList({"name": "%"}, returnedTags=tags)["return"]
        return (result or {}).get("callerFilterList") or []

    def update_caller_filter_list(self, **args):
        """Update a CallerFilterList.

        Schema: `UpdateCallerFilterListReq`: optional `newName`, `description`, optional choice of (optional `removeMembers`, `addMembers`), or `members`.
        """
        return self.client.updateCallerFilterList(**args)

    def delete_caller_filter_list(self, name="", uuid=""):
        """Delete a CallerFilterList by name or uuid.

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeCallerFilterList(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------
    # EnterpriseFeatureAccessConfiguration
    # Identity: pattern or uuid  (list by pattern)
    # ------------------------------------------------------------------

    def add_enterprise_feature_access_configuration(self, **args):
        """Add an EnterpriseFeatureAccessConfiguration.

        Schema: `enterpriseFeatureAccessConfiguration` -> `XEnterpriseFeatureAccessConfiguration`: `pattern`; optional `routePartitionName`, `description`, `isDefaultEafNumber`.
        """
        return self.client.addEnterpriseFeatureAccessConfiguration(
            self._build_object(
                "addEnterpriseFeatureAccessConfiguration",
                "enterpriseFeatureAccessConfiguration",
                args,
            )
        )

    def get_enterprise_feature_access_configuration(self, **args):
        """Get an EnterpriseFeatureAccessConfiguration by name or uuid.

        Schema: `GetEnterpriseFeatureAccessConfigurationReq`: optional `returnedTags`; one of `uuid`, or (`pattern`; optional `routePartitionName`).
        """
        return self.client.getEnterpriseFeatureAccessConfiguration(**args)["return"][
            "enterpriseFeatureAccessConfiguration"
        ]

    def get_enterprise_feature_access_configurations(self, tagfilter=None):
        """List EnterpriseFeatureAccessConfiguration records. Returns [] when nothing matches.

        Schema: `ListEnterpriseFeatureAccessConfigurationReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"pattern": ""}
        result = self.client.listEnterpriseFeatureAccessConfiguration(
            {"pattern": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("enterpriseFeatureAccessConfiguration") or []

    def update_enterprise_feature_access_configuration(self, **args):
        """Update an EnterpriseFeatureAccessConfiguration.

        Schema: `UpdateEnterpriseFeatureAccessConfigurationReq`: optional `newPattern`, `newRoutePartitionName`, `description`, `isDefaultEafNumber`; one of `uuid`, or (`pattern`; optional `routePartitionName`).
        """
        return self.client.updateEnterpriseFeatureAccessConfiguration(**args)

    def delete_enterprise_feature_access_configuration(self, pattern="", uuid=""):
        """Delete an EnterpriseFeatureAccessConfiguration by pattern or uuid.

        Schema: `RemoveEnterpriseFeatureAccessConfigurationReq`: one of `uuid`, or (`pattern`; optional `routePartitionName`).
        """
        if pattern:
            return self.client.removeEnterpriseFeatureAccessConfiguration(pattern=pattern)
        if uuid:
            return self.client.removeEnterpriseFeatureAccessConfiguration(uuid=uuid)
        raise ValueError("delete_enterprise_feature_access_configuration requires pattern or uuid")

    # ------------------------------------------------------------------
    # TodAccess
    # ------------------------------------------------------------------

    def add_tod_access(self, **args):
        """Add a TodAccess entry.

        Schema: `todAccess` -> `XTodAccess`: `name` + `ownerIdName`; optional `description`, `members`.
        """
        return self.client.addTodAccess(self._build_object("addTodAccess", "todAccess", args))

    def get_tod_access(self, **args):
        """Get a TodAccess by name or uuid.

        Schema: `GetTodAccessReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getTodAccess(**args)["return"]["todAccess"]

    def get_tod_access_list(self, tagfilter=None):
        """List TodAccess records. Returns [] when nothing matches.

        Schema: `ListTodAccessReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listTodAccess({"name": "%"}, returnedTags=tags)["return"]
        return (result or {}).get("todAccess") or []

    def update_tod_access(self, **args):
        """Update a TodAccess.

        Schema: `UpdateTodAccessReq`: optional `newName`, `description`, `members`.
        """
        return self.client.updateTodAccess(**args)

    def delete_tod_access(self, name="", uuid=""):
        """Delete a TodAccess by name or uuid.

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeTodAccess(**self._identify(name=name, uuid=uuid))
