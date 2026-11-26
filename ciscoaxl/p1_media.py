"""
P1 Batch B4 — Media / Mobility / Presence mixin

Entities
--------
Media:
  MeetMe, MohAudioSource, MohServer, RecordingProfile, RegionMatrix

Mobility / Presence:
  DeviceMobility, DeviceMobilityGroup, MobileVoiceAccess, Mobility,
  MobilityProfile, PhysicalLocation, PresenceGroup
"""


class P1Media:
    """P1Media AXL wrappers — Media, Mobility, and Presence entities."""

    # ------------------------------------------------------------------
    # MeetMe
    # ------------------------------------------------------------------

    def add_meet_me(self, **args):
        """Add a MeetMe conference number."""
        return self.client.addMeetMe(self._build_object("addMeetMe", "meetMe", args))

    def get_meet_me(self, **args):
        """Get a MeetMe by pattern/partition or uuid."""
        return self.client.getMeetMe(**args)["return"]["meetMe"]

    def get_meet_mes(self, tagfilter=None):
        """List all MeetMe records. Returns [] when nothing matches."""
        tags = tagfilter if tagfilter is not None else {"pattern": ""}
        result = self.client.listMeetMe({"pattern": "%"}, returnedTags=tags)["return"]
        return (result or {}).get("meetMe") or []

    def update_meet_me(self, **args):
        """Update a MeetMe."""
        return self.client.updateMeetMe(**args)

    def delete_meet_me(self, name="", uuid=""):
        """Delete a MeetMe by name (pattern) or uuid."""
        return self.client.removeMeetMe(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------
    # MohAudioSource  (no add — read-only source registry)
    # Note: identity is sourceId or uuid, not name.
    # ------------------------------------------------------------------

    def get_moh_audio_source(self, **args):
        """Get a MohAudioSource by sourceId or uuid."""
        return self.client.getMohAudioSource(**args)["return"]["mohAudioSource"]

    def get_moh_audio_sources(self, tagfilter=None):
        """List all MohAudioSource records. Returns [] when nothing matches."""
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listMohAudioSource({"name": "%"}, returnedTags=tags)["return"]
        return (result or {}).get("mohAudioSource") or []

    def update_moh_audio_source(self, **args):
        """Update a MohAudioSource (identified by sourceId or uuid)."""
        return self.client.updateMohAudioSource(**args)

    def delete_moh_audio_source(self, source_id=None, uuid=""):
        """Delete a MohAudioSource by sourceId or uuid."""
        if source_id:
            return self.client.removeMohAudioSource(sourceId=source_id)
        if uuid:
            return self.client.removeMohAudioSource(uuid=uuid)
        raise ValueError("delete_moh_audio_source requires source_id or uuid")

    # ------------------------------------------------------------------
    # MohServer  (no add, no remove)
    # ------------------------------------------------------------------

    def get_moh_server(self, **args):
        """Get a MohServer by name or uuid."""
        return self.client.getMohServer(**args)["return"]["mohServer"]

    def get_moh_servers(self, tagfilter=None):
        """List all MohServer records. Returns [] when nothing matches."""
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listMohServer({"name": "%"}, returnedTags=tags)["return"]
        return (result or {}).get("mohServer") or []

    def update_moh_server(self, **args):
        """Update a MohServer."""
        return self.client.updateMohServer(**args)

    # ------------------------------------------------------------------
    # RecordingProfile
    # ------------------------------------------------------------------

    def add_recording_profile(self, **args):
        """Add a RecordingProfile."""
        return self.client.addRecordingProfile(
            self._build_object("addRecordingProfile", "recordingProfile", args)
        )

    def get_recording_profile(self, **args):
        """Get a RecordingProfile by name or uuid."""
        return self.client.getRecordingProfile(**args)["return"]["recordingProfile"]

    def get_recording_profiles(self, tagfilter=None):
        """List all RecordingProfiles. Returns [] when nothing matches."""
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listRecordingProfile({"name": "%"}, returnedTags=tags)["return"]
        return (result or {}).get("recordingProfile") or []

    def update_recording_profile(self, **args):
        """Update a RecordingProfile."""
        return self.client.updateRecordingProfile(**args)

    def delete_recording_profile(self, name="", uuid=""):
        """Delete a RecordingProfile by name or uuid."""
        return self.client.removeRecordingProfile(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------
    # RegionMatrix  (update only)
    # Identified by (regionAName + regionBName) or uuid.
    # ------------------------------------------------------------------

    def update_region_matrix(self, **args):
        """Update a RegionMatrix entry (regionAName + regionBName or uuid)."""
        return self.client.updateRegionMatrix(**args)

    # ------------------------------------------------------------------
    # DeviceMobility
    # ------------------------------------------------------------------

    def add_device_mobility(self, **args):
        """Add a DeviceMobility record."""
        return self.client.addDeviceMobility(
            self._build_object("addDeviceMobility", "deviceMobility", args)
        )

    def get_device_mobility(self, **args):
        """Get a DeviceMobility by name or uuid."""
        return self.client.getDeviceMobility(**args)["return"]["deviceMobility"]

    def get_device_mobilities(self, tagfilter=None):
        """List all DeviceMobility records. Returns [] when nothing matches."""
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listDeviceMobility({"name": "%"}, returnedTags=tags)["return"]
        return (result or {}).get("deviceMobility") or []

    def update_device_mobility(self, **args):
        """Update a DeviceMobility."""
        return self.client.updateDeviceMobility(**args)

    def delete_device_mobility(self, name="", uuid=""):
        """Delete a DeviceMobility by name or uuid."""
        return self.client.removeDeviceMobility(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------
    # DeviceMobilityGroup
    # ------------------------------------------------------------------

    def add_device_mobility_group(self, **args):
        """Add a DeviceMobilityGroup."""
        return self.client.addDeviceMobilityGroup(
            self._build_object("addDeviceMobilityGroup", "deviceMobilityGroup", args)
        )

    def get_device_mobility_group(self, **args):
        """Get a DeviceMobilityGroup by name or uuid."""
        return self.client.getDeviceMobilityGroup(**args)["return"]["deviceMobilityGroup"]

    def get_device_mobility_groups(self, tagfilter=None):
        """List all DeviceMobilityGroups. Returns [] when nothing matches."""
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listDeviceMobilityGroup({"name": "%"}, returnedTags=tags)["return"]
        return (result or {}).get("deviceMobilityGroup") or []

    def update_device_mobility_group(self, **args):
        """Update a DeviceMobilityGroup."""
        return self.client.updateDeviceMobilityGroup(**args)

    def delete_device_mobility_group(self, name="", uuid=""):
        """Delete a DeviceMobilityGroup by name or uuid."""
        return self.client.removeDeviceMobilityGroup(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------
    # MobileVoiceAccess
    # Note: identified by pattern or uuid (not name).
    # ------------------------------------------------------------------

    def add_mobile_voice_access(self, **args):
        """Add a MobileVoiceAccess entry."""
        return self.client.addMobileVoiceAccess(
            self._build_object("addMobileVoiceAccess", "mobileVoiceAccess", args)
        )

    def get_mobile_voice_access(self, **args):
        """Get a MobileVoiceAccess by pattern or uuid."""
        return self.client.getMobileVoiceAccess(**args)["return"]["mobileVoiceAccess"]

    def update_mobile_voice_access(self, **args):
        """Update a MobileVoiceAccess."""
        return self.client.updateMobileVoiceAccess(**args)

    def delete_mobile_voice_access(self, pattern="", uuid=""):
        """Delete a MobileVoiceAccess by pattern or uuid."""
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
        """Add a Mobility configuration."""
        return self.client.addMobility(self._build_object("addMobility", "mobility", args))

    def get_mobility(self, **args):
        """Get Mobility config by handoffNumber or DTMFNumber."""
        return self.client.getMobility(**args)["return"]["mobility"]

    def update_mobility(self, **args):
        """Update a Mobility configuration."""
        return self.client.updateMobility(**args)

    # ------------------------------------------------------------------
    # MobilityProfile
    # ------------------------------------------------------------------

    def add_mobility_profile(self, **args):
        """Add a MobilityProfile."""
        return self.client.addMobilityProfile(
            self._build_object("addMobilityProfile", "mobilityProfile", args)
        )

    def get_mobility_profile(self, **args):
        """Get a MobilityProfile by name or uuid."""
        return self.client.getMobilityProfile(**args)["return"]["mobilityProfile"]

    def get_mobility_profiles(self, tagfilter=None):
        """List all MobilityProfiles. Returns [] when nothing matches."""
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listMobilityProfile({"name": "%"}, returnedTags=tags)["return"]
        return (result or {}).get("mobilityProfile") or []

    def update_mobility_profile(self, **args):
        """Update a MobilityProfile."""
        return self.client.updateMobilityProfile(**args)

    def delete_mobility_profile(self, name="", uuid=""):
        """Delete a MobilityProfile by name or uuid."""
        return self.client.removeMobilityProfile(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------
    # PhysicalLocation
    # ------------------------------------------------------------------

    def add_physical_location(self, **args):
        """Add a PhysicalLocation."""
        return self.client.addPhysicalLocation(
            self._build_object("addPhysicalLocation", "physicalLocation", args)
        )

    def get_physical_location(self, **args):
        """Get a PhysicalLocation by name or uuid."""
        return self.client.getPhysicalLocation(**args)["return"]["physicalLocation"]

    def get_physical_locations(self, tagfilter=None):
        """List all PhysicalLocations. Returns [] when nothing matches."""
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listPhysicalLocation({"name": "%"}, returnedTags=tags)["return"]
        return (result or {}).get("physicalLocation") or []

    def update_physical_location(self, **args):
        """Update a PhysicalLocation."""
        return self.client.updatePhysicalLocation(**args)

    def delete_physical_location(self, name="", uuid=""):
        """Delete a PhysicalLocation by name or uuid."""
        return self.client.removePhysicalLocation(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------
    # PresenceGroup
    # ------------------------------------------------------------------

    def add_presence_group(self, **args):
        """Add a PresenceGroup."""
        return self.client.addPresenceGroup(
            self._build_object("addPresenceGroup", "presenceGroup", args)
        )

    def get_presence_group(self, **args):
        """Get a PresenceGroup by name or uuid."""
        return self.client.getPresenceGroup(**args)["return"]["presenceGroup"]

    def get_presence_groups(self, tagfilter=None):
        """List all PresenceGroups. Returns [] when nothing matches."""
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listPresenceGroup({"name": "%"}, returnedTags=tags)["return"]
        return (result or {}).get("presenceGroup") or []

    def update_presence_group(self, **args):
        """Update a PresenceGroup."""
        return self.client.updatePresenceGroup(**args)

    def delete_presence_group(self, name="", uuid=""):
        """Delete a PresenceGroup by name or uuid."""
        return self.client.removePresenceGroup(**self._identify(name=name, uuid=uuid))
