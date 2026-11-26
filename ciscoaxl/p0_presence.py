"""
P0 Batch B3 — Presence / Scheduling / Park mixin
Entities: ServiceProfile, UcService, VoiceMailPilot, VoiceMailProfile,
          TimePeriod, TimeSchedule, CallPark
"""


class P0Presence:
    # ------------------------------------------------------------------
    # ServiceProfile
    # ------------------------------------------------------------------

    def get_service_profiles(
        self,
        tagfilter={"name": "", "description": "", "isDefault": ""},
    ):
        """
        List all Service Profiles.
        :param tagfilter: AXL returned tags to include
        :return: list of dicts, empty when nothing matches
        """
        response = self.client.listServiceProfile(
            {"name": "%"},
            returnedTags=tagfilter,
        )["return"]
        if response:
            return response["serviceProfile"]
        return []

    def get_service_profile(self, **args):
        """
        Get a Service Profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: result dict
        """
        return self.client.getServiceProfile(**args)["return"]["serviceProfile"]

    def add_service_profile(self, **args):
        """
        Add a Service Profile.
        :param name: profile name — required
        :return: result dict
        """
        obj = self._build_object("addServiceProfile", "serviceProfile", args)
        return self.client.addServiceProfile(obj)

    def update_service_profile(self, **args):
        """
        Update a Service Profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: result dict
        """
        return self.client.updateServiceProfile(**args)

    def delete_service_profile(self, **args):
        """
        Delete a Service Profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: result dict
        """
        return self.client.removeServiceProfile(**args)

    # ------------------------------------------------------------------
    # UcService
    # ------------------------------------------------------------------

    def get_uc_services(
        self,
        tagfilter={"name": "", "description": "", "serviceType": "", "productType": ""},
    ):
        """
        List all UC Services.
        :param tagfilter: AXL returned tags to include
        :return: list of dicts, empty when nothing matches
        """
        response = self.client.listUcService(
            {"name": "%"},
            returnedTags=tagfilter,
        )["return"]
        if response:
            return response["ucService"]
        return []

    def get_uc_service(self, **args):
        """
        Get a UC Service.
        :param name: service name (or uuid)
        :param uuid: service uuid (or name)
        :return: result dict
        """
        return self.client.getUcService(**args)["return"]["ucService"]

    def add_uc_service(self, **args):
        """
        Add a UC Service.
        :param name: service name — required
        :param serviceType: service type — required
        :return: result dict
        """
        obj = self._build_object("addUcService", "ucService", args)
        return self.client.addUcService(obj)

    def update_uc_service(self, **args):
        """
        Update a UC Service.
        :param name: service name (or uuid)
        :param uuid: service uuid (or name)
        :return: result dict
        """
        return self.client.updateUcService(**args)

    def delete_uc_service(self, **args):
        """
        Delete a UC Service.
        :param name: service name (or uuid)
        :param uuid: service uuid (or name)
        :return: result dict
        """
        return self.client.removeUcService(**args)

    def apply_uc_service(self, name="", uuid=""):
        """
        Apply a UC Service to its subscribers.
        :param name: service name (or uuid)
        :param uuid: service uuid (or name)
        :return: result dict
        """
        return self.client.applyUcService(**self._identify(name=name, uuid=uuid))

    def reset_uc_service(self, name="", uuid=""):
        """
        Reset a UC Service.
        :param name: service name (or uuid)
        :param uuid: service uuid (or name)
        :return: result dict
        """
        return self.client.resetUcService(**self._identify(name=name, uuid=uuid))

    def restart_uc_service(self, name="", uuid=""):
        """
        Restart a UC Service.
        :param name: service name (or uuid)
        :param uuid: service uuid (or name)
        :return: result dict
        """
        return self.client.restartUcService(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------
    # VoiceMailPilot
    # VoiceMailPilot identity: dirn + optional cssName (not name/uuid for get/delete)
    # ------------------------------------------------------------------

    def get_voice_mail_pilots(
        self,
        tagfilter={"dirn": "", "description": "", "cssName": "", "isDefault": ""},
    ):
        """
        List all Voice Mail Pilots.
        :param tagfilter: AXL returned tags to include
        :return: list of dicts, empty when nothing matches
        """
        response = self.client.listVoiceMailPilot(
            {"dirn": "%"},
            returnedTags=tagfilter,
        )["return"]
        if response:
            return response["voiceMailPilot"]
        return []

    def get_voice_mail_pilot(self, **args):
        """
        Get a Voice Mail Pilot.
        :param dirn: pilot directory number (or uuid)
        :param cssName: calling search space name — optional
        :param uuid: pilot uuid (or dirn)
        :return: result dict
        """
        return self.client.getVoiceMailPilot(**args)["return"]["voiceMailPilot"]

    def add_voice_mail_pilot(self, **args):
        """
        Add a Voice Mail Pilot.
        :param dirn: directory number — required
        :param isDefault: set as default pilot, default False
        :return: result dict
        """
        obj = self._build_object(
            "addVoiceMailPilot", "voiceMailPilot", args, defaults={"isDefault": False}
        )
        return self.client.addVoiceMailPilot(obj)

    def update_voice_mail_pilot(self, **args):
        """
        Update a Voice Mail Pilot.
        :param dirn: directory number (or uuid)
        :param uuid: pilot uuid (or dirn)
        :return: result dict
        """
        return self.client.updateVoiceMailPilot(**args)

    def delete_voice_mail_pilot(self, **args):
        """
        Delete a Voice Mail Pilot.
        :param dirn: directory number (or uuid)
        :param cssName: calling search space name — optional
        :param uuid: pilot uuid (or dirn)
        :return: result dict
        """
        return self.client.removeVoiceMailPilot(**args)

    # ------------------------------------------------------------------
    # VoiceMailProfile
    # ------------------------------------------------------------------

    def get_voice_mail_profiles(
        self,
        tagfilter={"name": "", "description": "", "isDefault": ""},
    ):
        """
        List all Voice Mail Profiles.
        :param tagfilter: AXL returned tags to include
        :return: list of dicts, empty when nothing matches
        """
        response = self.client.listVoiceMailProfile(
            {"name": "%"},
            returnedTags=tagfilter,
        )["return"]
        if response:
            return response["voiceMailProfile"]
        return []

    def get_voice_mail_profile(self, **args):
        """
        Get a Voice Mail Profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: result dict
        """
        return self.client.getVoiceMailProfile(**args)["return"]["voiceMailProfile"]

    def add_voice_mail_profile(self, **args):
        """
        Add a Voice Mail Profile.
        :param name: profile name — required
        :return: result dict
        """
        obj = self._build_object("addVoiceMailProfile", "voiceMailProfile", args)
        return self.client.addVoiceMailProfile(obj)

    def update_voice_mail_profile(self, **args):
        """
        Update a Voice Mail Profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: result dict
        """
        return self.client.updateVoiceMailProfile(**args)

    def delete_voice_mail_profile(self, **args):
        """
        Delete a Voice Mail Profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: result dict
        """
        return self.client.removeVoiceMailProfile(**args)

    def apply_voice_mail_profile(self, name="", uuid=""):
        """
        Apply a Voice Mail Profile to its subscribers.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: result dict
        """
        return self.client.applyVoiceMailProfile(**self._identify(name=name, uuid=uuid))

    def reset_voice_mail_profile(self, name="", uuid=""):
        """
        Reset a Voice Mail Profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: result dict
        """
        return self.client.resetVoiceMailProfile(**self._identify(name=name, uuid=uuid))

    def restart_voice_mail_profile(self, name="", uuid=""):
        """
        Restart a Voice Mail Profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: result dict
        """
        return self.client.restartVoiceMailProfile(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------
    # TimePeriod
    # ------------------------------------------------------------------

    def get_time_periods(
        self,
        tagfilter={"name": "", "description": ""},
    ):
        """
        List all Time Periods.
        :param tagfilter: AXL returned tags to include
        :return: list of dicts, empty when nothing matches
        """
        response = self.client.listTimePeriod(
            {"name": "%"},
            returnedTags=tagfilter,
        )["return"]
        if response:
            return response["timePeriod"]
        return []

    def get_time_period(self, **args):
        """
        Get a Time Period.
        :param name: time period name (or uuid)
        :param uuid: time period uuid (or name)
        :return: result dict
        """
        return self.client.getTimePeriod(**args)["return"]["timePeriod"]

    def add_time_period(self, **args):
        """
        Add a Time Period.
        :param name: time period name — required
        :return: result dict
        """
        obj = self._build_object("addTimePeriod", "timePeriod", args)
        return self.client.addTimePeriod(obj)

    def update_time_period(self, **args):
        """
        Update a Time Period.
        :param name: time period name (or uuid)
        :param uuid: time period uuid (or name)
        :return: result dict
        """
        return self.client.updateTimePeriod(**args)

    def delete_time_period(self, **args):
        """
        Delete a Time Period.
        :param name: time period name (or uuid)
        :param uuid: time period uuid (or name)
        :return: result dict
        """
        return self.client.removeTimePeriod(**args)

    # ------------------------------------------------------------------
    # TimeSchedule
    # ------------------------------------------------------------------

    def get_time_schedules(
        self,
        tagfilter={"name": "", "description": ""},
    ):
        """
        List all Time Schedules.
        :param tagfilter: AXL returned tags to include
        :return: list of dicts, empty when nothing matches
        """
        response = self.client.listTimeSchedule(
            {"name": "%"},
            returnedTags=tagfilter,
        )["return"]
        if response:
            return response["timeSchedule"]
        return []

    def get_time_schedule(self, **args):
        """
        Get a Time Schedule.
        :param name: time schedule name (or uuid)
        :param uuid: time schedule uuid (or name)
        :return: result dict
        """
        return self.client.getTimeSchedule(**args)["return"]["timeSchedule"]

    def add_time_schedule(self, **args):
        """
        Add a Time Schedule.
        :param name: time schedule name — required
        :return: result dict
        """
        obj = self._build_object("addTimeSchedule", "timeSchedule", args)
        return self.client.addTimeSchedule(obj)

    def update_time_schedule(self, **args):
        """
        Update a Time Schedule.
        :param name: time schedule name (or uuid)
        :param uuid: time schedule uuid (or name)
        :return: result dict
        """
        return self.client.updateTimeSchedule(**args)

    def delete_time_schedule(self, **args):
        """
        Delete a Time Schedule.
        :param name: time schedule name (or uuid)
        :param uuid: time schedule uuid (or name)
        :return: result dict
        """
        return self.client.removeTimeSchedule(**args)

    # ------------------------------------------------------------------
    # CallPark
    # Identity: pattern + optional routePartitionName  -OR-  uuid
    # ------------------------------------------------------------------

    def get_call_parks(
        self,
        tagfilter={
            "pattern": "",
            "description": "",
            "routePartitionName": "",
            "callManagerName": "",
        },
    ):
        """
        List all Call Park entries.
        :param tagfilter: AXL returned tags to include
        :return: list of dicts, empty when nothing matches
        """
        response = self.client.listCallPark(
            {"pattern": "%"},
            returnedTags=tagfilter,
        )["return"]
        if response:
            return response["callPark"]
        return []

    def get_call_park(self, **args):
        """
        Get a Call Park entry.
        :param pattern: call park pattern (or uuid)
        :param routePartitionName: partition — optional (AXL name: routePartitionName)
        :param uuid: call park uuid (or pattern)
        :return: result dict
        """
        return self.client.getCallPark(**args)["return"]["callPark"]

    def add_call_park(self, **args):
        """
        Add a Call Park entry.
        :param pattern: pattern — required
        :param callManagerName: Unified CM name — required
        :param routePartitionName: partition — optional
        :return: result dict
        """
        obj = self._build_object("addCallPark", "callPark", args)
        return self.client.addCallPark(obj)

    def update_call_park(self, **args):
        """
        Update a Call Park entry.
        :param pattern: call park pattern (or uuid)
        :param routePartitionName: partition — optional
        :param uuid: call park uuid (or pattern)
        :return: result dict
        """
        return self.client.updateCallPark(**args)

    def delete_call_park(self, **args):
        """
        Delete a Call Park entry.
        :param pattern: call park pattern (or uuid)
        :param routePartitionName: partition — optional
        :param uuid: call park uuid (or pattern)
        :return: result dict
        """
        return self.client.removeCallPark(**args)
