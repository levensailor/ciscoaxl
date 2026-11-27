"""
P2 Batch B1 — Extended Media / Call-Control / Announcement mixin

Entities
--------
CalledPartyTracing, CmcInfo, ElinGroup, ExternalCallControlProfile,
FacInfo, TransPatternOptions, TransformationProfile, H323Trunk,
SipProfileOptions, Announcement, Annunciator, AudioCodecPreferenceList,
ConferenceNow, FixedMohAudioSource, InteractiveVoiceResponse,
CallerFilterList, EnterpriseFeatureAccessConfiguration, TodAccess
"""


class P2Media:
    """P2Media AXL wrappers — extended media, call-control, and announcement entities."""

    # ------------------------------------------------------------------
    # CalledPartyTracing
    # Identity: directorynumber or uuid  (no get, only add/list/remove)
    # ------------------------------------------------------------------

    def add_called_party_tracing(self, **args):
        """Add a CalledPartyTracing entry."""
        return self.client.addCalledPartyTracing(
            self._build_object("addCalledPartyTracing", "calledPartyTracing", args)
        )

    def get_called_party_tracings(self, tagfilter=None):
        """List CalledPartyTracing records. Returns [] when nothing matches."""
        tags = tagfilter if tagfilter is not None else {"directorynumber": ""}
        result = self.client.listCalledPartyTracing(
            {"directorynumber": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("calledPartyTracing") or []

    def delete_called_party_tracing(self, directorynumber="", uuid=""):
        """Delete a CalledPartyTracing by directorynumber or uuid."""
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
        """Add a CmcInfo entry."""
        return self.client.addCmcInfo(self._build_object("addCmcInfo", "cmcInfo", args))

    def get_cmc_info(self, **args):
        """Get a CmcInfo by code or uuid."""
        return self.client.getCmcInfo(**args)["return"]["cmcInfo"]

    def get_cmc_infos(self, tagfilter=None):
        """List CmcInfo records. Returns [] when nothing matches."""
        tags = tagfilter if tagfilter is not None else {"code": ""}
        result = self.client.listCmcInfo({"code": "%"}, returnedTags=tags)["return"]
        return (result or {}).get("cmcInfo") or []

    def update_cmc_info(self, **args):
        """Update a CmcInfo (identified by code or uuid)."""
        return self.client.updateCmcInfo(**args)

    def delete_cmc_info(self, code="", uuid=""):
        """Delete a CmcInfo by code or uuid."""
        if code:
            return self.client.removeCmcInfo(code=code)
        if uuid:
            return self.client.removeCmcInfo(uuid=uuid)
        raise ValueError("delete_cmc_info requires code or uuid")

    # ------------------------------------------------------------------
    # ElinGroup
    # ------------------------------------------------------------------

    def add_elin_group(self, **args):
        """Add an ElinGroup."""
        return self.client.addElinGroup(self._build_object("addElinGroup", "elinGroup", args))

    def get_elin_group(self, **args):
        """Get an ElinGroup by name or uuid."""
        return self.client.getElinGroup(**args)["return"]["elinGroup"]

    def get_elin_groups(self, tagfilter=None):
        """List ElinGroup records. Returns [] when nothing matches."""
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listElinGroup({"name": "%"}, returnedTags=tags)["return"]
        return (result or {}).get("elinGroup") or []

    def update_elin_group(self, **args):
        """Update an ElinGroup."""
        return self.client.updateElinGroup(**args)

    def delete_elin_group(self, name="", uuid=""):
        """Delete an ElinGroup by name or uuid."""
        return self.client.removeElinGroup(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------
    # ExternalCallControlProfile
    # ------------------------------------------------------------------

    def add_external_call_control_profile(self, **args):
        """Add an ExternalCallControlProfile."""
        return self.client.addExternalCallControlProfile(
            self._build_object("addExternalCallControlProfile", "externalCallControlProfile", args)
        )

    def get_external_call_control_profile(self, **args):
        """Get an ExternalCallControlProfile by name or uuid."""
        return self.client.getExternalCallControlProfile(**args)["return"][
            "externalCallControlProfile"
        ]

    def get_external_call_control_profiles(self, tagfilter=None):
        """List ExternalCallControlProfile records. Returns [] when nothing matches."""
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listExternalCallControlProfile(
            {"name": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("externalCallControlProfile") or []

    def update_external_call_control_profile(self, **args):
        """Update an ExternalCallControlProfile."""
        return self.client.updateExternalCallControlProfile(**args)

    def delete_external_call_control_profile(self, name="", uuid=""):
        """Delete an ExternalCallControlProfile by name or uuid."""
        return self.client.removeExternalCallControlProfile(
            **self._identify(name=name, uuid=uuid)
        )

    # ------------------------------------------------------------------
    # FacInfo
    # Identity: name or uuid
    # ------------------------------------------------------------------

    def add_fac_info(self, **args):
        """Add a FacInfo entry."""
        return self.client.addFacInfo(self._build_object("addFacInfo", "facInfo", args))

    def get_fac_info(self, **args):
        """Get a FacInfo by name or uuid."""
        return self.client.getFacInfo(**args)["return"]["facInfo"]

    def get_fac_infos(self, tagfilter=None):
        """List FacInfo records. Returns [] when nothing matches."""
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listFacInfo({"name": "%"}, returnedTags=tags)["return"]
        return (result or {}).get("facInfo") or []

    def update_fac_info(self, **args):
        """Update a FacInfo."""
        return self.client.updateFacInfo(**args)

    def delete_fac_info(self, name="", uuid=""):
        """Delete a FacInfo by name or uuid."""
        return self.client.removeFacInfo(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------
    # TransPatternOptions  (get-only — no add/update/remove/list)
    # ------------------------------------------------------------------

    def get_trans_pattern_options(self, **args):
        """Get translation-pattern option choices. Returns the ``transPattern`` object."""
        return self.client.getTransPatternOptions(**args)["return"]["transPattern"]

    # ------------------------------------------------------------------
    # TransformationProfile
    # ------------------------------------------------------------------

    def add_transformation_profile(self, **args):
        """Add a TransformationProfile."""
        return self.client.addTransformationProfile(
            self._build_object("addTransformationProfile", "transformationProfile", args)
        )

    def get_transformation_profile(self, **args):
        """Get a TransformationProfile by name or uuid."""
        return self.client.getTransformationProfile(**args)["return"]["transformationProfile"]

    def get_transformation_profiles(self, tagfilter=None):
        """List TransformationProfile records. Returns [] when nothing matches."""
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listTransformationProfile({"name": "%"}, returnedTags=tags)["return"]
        return (result or {}).get("transformationProfile") or []

    def update_transformation_profile(self, **args):
        """Update a TransformationProfile."""
        return self.client.updateTransformationProfile(**args)

    def delete_transformation_profile(self, name="", uuid=""):
        """Delete a TransformationProfile by name or uuid."""
        return self.client.removeTransformationProfile(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------
    # H323Trunk
    # ------------------------------------------------------------------

    def add_h323_trunk(self, **args):
        """Add an H323Trunk."""
        return self.client.addH323Trunk(
            self._build_object("addH323Trunk", "h323Trunk", args)
        )

    def get_h323_trunk(self, **args):
        """Get an H323Trunk by name or uuid."""
        return self.client.getH323Trunk(**args)["return"]["h323Trunk"]

    def get_h323_trunks(self, tagfilter=None):
        """List H323Trunk records. Returns [] when nothing matches."""
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listH323Trunk({"name": "%"}, returnedTags=tags)["return"]
        return (result or {}).get("h323Trunk") or []

    def update_h323_trunk(self, **args):
        """Update an H323Trunk."""
        return self.client.updateH323Trunk(**args)

    def delete_h323_trunk(self, name="", uuid=""):
        """Delete an H323Trunk by name or uuid."""
        return self.client.removeH323Trunk(**self._identify(name=name, uuid=uuid))

    def reset_h323_trunk(self, name="", uuid=""):
        """Reset an H323Trunk by name or uuid."""
        return self.client.resetH323Trunk(**self._identify(name=name, uuid=uuid))

    def restart_h323_trunk(self, name="", uuid=""):
        """Restart an H323Trunk by name or uuid."""
        return self.client.restartH323Trunk(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------
    # SipProfileOptions  (get-only)
    # ------------------------------------------------------------------

    def get_sip_profile_options(self, **args):
        """Get SIP profile option choices. Returns the ``sipProfile`` object."""
        return self.client.getSipProfileOptions(**args)["return"]["sipProfile"]

    # ------------------------------------------------------------------
    # Announcement
    # ------------------------------------------------------------------

    def add_announcement(self, **args):
        """Add an Announcement."""
        return self.client.addAnnouncement(
            self._build_object("addAnnouncement", "announcement", args)
        )

    def get_announcement(self, **args):
        """Get an Announcement by name or uuid."""
        return self.client.getAnnouncement(**args)["return"]["announcement"]

    def get_announcements(self, tagfilter=None):
        """List Announcement records. Returns [] when nothing matches."""
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listAnnouncement({"name": "%"}, returnedTags=tags)["return"]
        return (result or {}).get("announcement") or []

    def update_announcement(self, **args):
        """Update an Announcement."""
        return self.client.updateAnnouncement(**args)

    def delete_announcement(self, name="", uuid=""):
        """Delete an Announcement by name or uuid."""
        return self.client.removeAnnouncement(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------
    # Annunciator  (no add, no remove)
    # ------------------------------------------------------------------

    def get_annunciator(self, **args):
        """Get an Annunciator by name or uuid."""
        return self.client.getAnnunciator(**args)["return"]["annunciator"]

    def get_annunciators(self, tagfilter=None):
        """List Annunciator records. Returns [] when nothing matches."""
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listAnnunciator({"name": "%"}, returnedTags=tags)["return"]
        return (result or {}).get("annunciator") or []

    def update_annunciator(self, **args):
        """Update an Annunciator."""
        return self.client.updateAnnunciator(**args)

    # ------------------------------------------------------------------
    # AudioCodecPreferenceList
    # ------------------------------------------------------------------

    def add_audio_codec_preference_list(self, **args):
        """Add an AudioCodecPreferenceList."""
        return self.client.addAudioCodecPreferenceList(
            self._build_object("addAudioCodecPreferenceList", "audioCodecPreferenceList", args)
        )

    def get_audio_codec_preference_list(self, **args):
        """Get an AudioCodecPreferenceList by name or uuid."""
        return self.client.getAudioCodecPreferenceList(**args)["return"][
            "audioCodecPreferenceList"
        ]

    def get_audio_codec_preference_lists(self, tagfilter=None):
        """List AudioCodecPreferenceList records. Returns [] when nothing matches."""
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listAudioCodecPreferenceList(
            {"name": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("audioCodecPreferenceList") or []

    def update_audio_codec_preference_list(self, **args):
        """Update an AudioCodecPreferenceList."""
        return self.client.updateAudioCodecPreferenceList(**args)

    def delete_audio_codec_preference_list(self, name="", uuid=""):
        """Delete an AudioCodecPreferenceList by name or uuid."""
        return self.client.removeAudioCodecPreferenceList(
            **self._identify(name=name, uuid=uuid)
        )

    # ------------------------------------------------------------------
    # ConferenceNow
    # Identity: conferenceNowNumber (not name) for list; name/uuid for get/remove
    # ------------------------------------------------------------------

    def add_conference_now(self, **args):
        """Add a ConferenceNow entry."""
        return self.client.addConferenceNow(
            self._build_object("addConferenceNow", "conferenceNow", args)
        )

    def get_conference_now(self, **args):
        """Get a ConferenceNow by conferenceNowNumber/name or uuid."""
        return self.client.getConferenceNow(**args)["return"]["conferenceNow"]

    def get_conference_nows(self, tagfilter=None):
        """List ConferenceNow records. Returns [] when nothing matches."""
        tags = tagfilter if tagfilter is not None else {"conferenceNowNumber": ""}
        result = self.client.listConferenceNow(
            {"conferenceNowNumber": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("conferenceNow") or []

    def update_conference_now(self, **args):
        """Update a ConferenceNow."""
        return self.client.updateConferenceNow(**args)

    def delete_conference_now(self, conferenceNowNumber="", uuid=""):
        """Delete a ConferenceNow by conferenceNowNumber or uuid."""
        if conferenceNowNumber:
            return self.client.removeConferenceNow(conferenceNowNumber=conferenceNowNumber)
        if uuid:
            return self.client.removeConferenceNow(uuid=uuid)
        raise ValueError("delete_conference_now requires conferenceNowNumber or uuid")

    # ------------------------------------------------------------------
    # FixedMohAudioSource  (get/update only — no add/remove/list)
    # ------------------------------------------------------------------

    def get_fixed_moh_audio_source(self, **args):
        """Get a FixedMohAudioSource by sourceId or uuid."""
        return self.client.getFixedMohAudioSource(**args)["return"]["fixedMohAudioSource"]

    def update_fixed_moh_audio_source(self, **args):
        """Update a FixedMohAudioSource."""
        return self.client.updateFixedMohAudioSource(**args)

    # ------------------------------------------------------------------
    # InteractiveVoiceResponse  (no add, no remove)
    # ------------------------------------------------------------------

    def get_interactive_voice_response(self, **args):
        """Get an InteractiveVoiceResponse by name or uuid."""
        return self.client.getInteractiveVoiceResponse(**args)["return"][
            "interactiveVoiceResponse"
        ]

    def get_interactive_voice_responses(self, tagfilter=None):
        """List InteractiveVoiceResponse records. Returns [] when nothing matches."""
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listInteractiveVoiceResponse(
            {"name": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("interactiveVoiceResponse") or []

    def update_interactive_voice_response(self, **args):
        """Update an InteractiveVoiceResponse."""
        return self.client.updateInteractiveVoiceResponse(**args)

    # ------------------------------------------------------------------
    # CallerFilterList
    # ------------------------------------------------------------------

    def add_caller_filter_list(self, **args):
        """Add a CallerFilterList."""
        return self.client.addCallerFilterList(
            self._build_object("addCallerFilterList", "callerFilterList", args)
        )

    def get_caller_filter_list(self, **args):
        """Get a CallerFilterList by name or uuid."""
        return self.client.getCallerFilterList(**args)["return"]["callerFilterList"]

    def get_caller_filter_lists(self, tagfilter=None):
        """List CallerFilterList records. Returns [] when nothing matches."""
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listCallerFilterList({"name": "%"}, returnedTags=tags)["return"]
        return (result or {}).get("callerFilterList") or []

    def update_caller_filter_list(self, **args):
        """Update a CallerFilterList."""
        return self.client.updateCallerFilterList(**args)

    def delete_caller_filter_list(self, name="", uuid=""):
        """Delete a CallerFilterList by name or uuid."""
        return self.client.removeCallerFilterList(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------
    # EnterpriseFeatureAccessConfiguration
    # Identity: pattern or uuid  (list by pattern)
    # ------------------------------------------------------------------

    def add_enterprise_feature_access_configuration(self, **args):
        """Add an EnterpriseFeatureAccessConfiguration."""
        return self.client.addEnterpriseFeatureAccessConfiguration(
            self._build_object(
                "addEnterpriseFeatureAccessConfiguration",
                "enterpriseFeatureAccessConfiguration",
                args,
            )
        )

    def get_enterprise_feature_access_configuration(self, **args):
        """Get an EnterpriseFeatureAccessConfiguration by name or uuid."""
        return self.client.getEnterpriseFeatureAccessConfiguration(**args)["return"][
            "enterpriseFeatureAccessConfiguration"
        ]

    def get_enterprise_feature_access_configurations(self, tagfilter=None):
        """List EnterpriseFeatureAccessConfiguration records. Returns [] when nothing matches."""
        tags = tagfilter if tagfilter is not None else {"pattern": ""}
        result = self.client.listEnterpriseFeatureAccessConfiguration(
            {"pattern": "%"}, returnedTags=tags
        )["return"]
        return (result or {}).get("enterpriseFeatureAccessConfiguration") or []

    def update_enterprise_feature_access_configuration(self, **args):
        """Update an EnterpriseFeatureAccessConfiguration."""
        return self.client.updateEnterpriseFeatureAccessConfiguration(**args)

    def delete_enterprise_feature_access_configuration(self, pattern="", uuid=""):
        """Delete an EnterpriseFeatureAccessConfiguration by pattern or uuid."""
        if pattern:
            return self.client.removeEnterpriseFeatureAccessConfiguration(pattern=pattern)
        if uuid:
            return self.client.removeEnterpriseFeatureAccessConfiguration(uuid=uuid)
        raise ValueError("delete_enterprise_feature_access_configuration requires pattern or uuid")

    # ------------------------------------------------------------------
    # TodAccess
    # ------------------------------------------------------------------

    def add_tod_access(self, **args):
        """Add a TodAccess entry."""
        return self.client.addTodAccess(self._build_object("addTodAccess", "todAccess", args))

    def get_tod_access(self, **args):
        """Get a TodAccess by name or uuid."""
        return self.client.getTodAccess(**args)["return"]["todAccess"]

    def get_tod_access_list(self, tagfilter=None):
        """List TodAccess records. Returns [] when nothing matches."""
        tags = tagfilter if tagfilter is not None else {"name": ""}
        result = self.client.listTodAccess({"name": "%"}, returnedTags=tags)["return"]
        return (result or {}).get("todAccess") or []

    def update_tod_access(self, **args):
        """Update a TodAccess."""
        return self.client.updateTodAccess(**args)

    def delete_tod_access(self, name="", uuid=""):
        """Delete a TodAccess by name or uuid."""
        return self.client.removeTodAccess(**self._identify(name=name, uuid=uuid))
