"""Presence, IM&P, scheduling, call park, and voicemail wrappers.

Entities: ServiceProfile, UcService, VoiceMailPilot, VoiceMailProfile,
          TimePeriod, TimeSchedule, CallPark

Presence / IM&P:
  AssignedPresenceServers   (list only)
  AssignedPresenceUsers     (list only)
  UnassignedPresenceServers (list only)
  UnassignedPresenceUsers   (list only)
  PresenceUser              (assign / unassign only)
  PresenceRedundancyGroup   (full CRUD)
  ExpresswayCConfiguration  (full CRUD)
  MraServiceDomain          (full CRUD)
"""


class PresenceMixin:
    """Presence, IM&P, scheduling, call park, and voicemail wrappers."""

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
        

        Schema: `ListServiceProfileReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
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
        

        Schema: `GetServiceProfileReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getServiceProfile(**args)["return"]["serviceProfile"]

    def add_service_profile(self, **args):
        """
        Add a Service Profile.
        :param name: profile name — required
        :return: result dict
        

        Schema: `serviceProfile` -> `XServiceProfile`: `name`; optional `description`, `isDefault`, `serviceProfileInfos`.
        """
        obj = self._build_object("addServiceProfile", "serviceProfile", args)
        return self.client.addServiceProfile(obj)

    def update_service_profile(self, **args):
        """
        Update a Service Profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: result dict
        

        Schema: `UpdateServiceProfileReq`: optional `newName`, `description`, `isDefault`, `serviceProfileInfos`.
        """
        return self.client.updateServiceProfile(**args)

    def delete_service_profile(self, **args):
        """
        Delete a Service Profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: result dict
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
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
        

        Schema: `ListUcServiceReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
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
        

        Schema: `GetUcServiceReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getUcService(**args)["return"]["ucService"]

    def add_uc_service(self, **args):
        """
        Add a UC Service.
        :param name: service name — required
        :param serviceType: service type — required
        :return: result dict
        

        Schema: `ucService` -> `XUcService`: `serviceType` + `productType` + `name` + `hostnameorip`; optional `description`, `port`, `protocol`, `ucServiceXml`.
        """
        obj = self._build_object("addUcService", "ucService", args)
        return self.client.addUcService(obj)

    def update_uc_service(self, **args):
        """
        Update a UC Service.
        :param name: service name (or uuid)
        :param uuid: service uuid (or name)
        :return: result dict
        

        Schema: `UpdateUcServiceReq`: optional `newName`, `description`, `hostnameorip`, `port`, `protocol`, `ucServiceXml`.
        """
        return self.client.updateUcService(**args)

    def delete_uc_service(self, **args):
        """
        Delete a UC Service.
        :param name: service name (or uuid)
        :param uuid: service uuid (or name)
        :return: result dict
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeUcService(**args)

    def apply_uc_service(self, name="", uuid=""):
        """
        Apply a UC Service to its subscribers.
        :param name: service name (or uuid)
        :param uuid: service uuid (or name)
        :return: result dict
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.applyUcService(**self._identify(name=name, uuid=uuid))

    def reset_uc_service(self, name="", uuid=""):
        """
        Reset a UC Service.
        :param name: service name (or uuid)
        :param uuid: service uuid (or name)
        :return: result dict
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.resetUcService(**self._identify(name=name, uuid=uuid))

    def restart_uc_service(self, name="", uuid=""):
        """
        Restart a UC Service.
        :param name: service name (or uuid)
        :param uuid: service uuid (or name)
        :return: result dict
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
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
        

        Schema: `ListVoiceMailPilotReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
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
        

        Schema: `GetVoiceMailPilotReq`: optional `returnedTags`; one of `uuid`, or (`dirn`; optional `cssName`).
        """
        return self.client.getVoiceMailPilot(**args)["return"]["voiceMailPilot"]

    def add_voice_mail_pilot(self, **args):
        """
        Add a Voice Mail Pilot.
        :param dirn: directory number — required
        :param isDefault: set as default pilot, default False
        :return: result dict
        

        Schema: `voiceMailPilot` -> `XVoiceMailPilot`: `dirn` + `isDefault`; optional `description`, `cssName`.
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
        

        Schema: `UpdateVoiceMailPilotReq`: optional `newDirn`, `description`, `newCssName`, `isDefault`; one of `uuid`, or (`dirn`; optional `cssName`).
        """
        return self.client.updateVoiceMailPilot(**args)

    def delete_voice_mail_pilot(self, **args):
        """
        Delete a Voice Mail Pilot.
        :param dirn: directory number (or uuid)
        :param cssName: calling search space name — optional
        :param uuid: pilot uuid (or dirn)
        :return: result dict
        

        Schema: `RemoveVoiceMailPilotReq`: one of `uuid`, or (`dirn`; optional `cssName`).
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
        

        Schema: `ListVoiceMailProfileReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
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
        

        Schema: `GetVoiceMailProfileReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getVoiceMailProfile(**args)["return"]["voiceMailProfile"]

    def add_voice_mail_profile(self, **args):
        """
        Add a Voice Mail Profile.
        :param name: profile name — required
        :return: result dict
        

        Schema: `voiceMailProfile` -> `XVoiceMailProfile`: `name` + `voiceMailPilot`; optional `description`, `isDefault`, `voiceMailboxMask`.
        """
        obj = self._build_object("addVoiceMailProfile", "voiceMailProfile", args)
        return self.client.addVoiceMailProfile(obj)

    def update_voice_mail_profile(self, **args):
        """
        Update a Voice Mail Profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: result dict
        

        Schema: `UpdateVoiceMailProfileReq`: optional `newName`, `description`, `isDefault`, `voiceMailboxMask`, `voiceMailPilot`.
        """
        return self.client.updateVoiceMailProfile(**args)

    def delete_voice_mail_profile(self, **args):
        """
        Delete a Voice Mail Profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: result dict
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeVoiceMailProfile(**args)

    def apply_voice_mail_profile(self, name="", uuid=""):
        """
        Apply a Voice Mail Profile to its subscribers.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: result dict
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.applyVoiceMailProfile(**self._identify(name=name, uuid=uuid))

    def reset_voice_mail_profile(self, name="", uuid=""):
        """
        Reset a Voice Mail Profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: result dict
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.resetVoiceMailProfile(**self._identify(name=name, uuid=uuid))

    def restart_voice_mail_profile(self, name="", uuid=""):
        """
        Restart a Voice Mail Profile.
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: result dict
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
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
        

        Schema: `ListTimePeriodReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
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
        

        Schema: `GetTimePeriodReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getTimePeriod(**args)["return"]["timePeriod"]

    def add_time_period(self, **args):
        """
        Add a Time Period.
        :param name: time period name — required
        :return: result dict
        

        Schema: `timePeriod` -> `XTimePeriod`: `name`; optional `startTime`, `endTime`, `startDay`, `endDay`, `monthOfYear`, `dayOfMonth` and 5 more.
        """
        obj = self._build_object("addTimePeriod", "timePeriod", args)
        return self.client.addTimePeriod(obj)

    def update_time_period(self, **args):
        """
        Update a Time Period.
        :param name: time period name (or uuid)
        :param uuid: time period uuid (or name)
        :return: result dict
        

        Schema: `UpdateTimePeriodReq`: optional `newName`, `startTime`, `endTime`, `startDay`, `endDay`, `monthOfYear` and 4 more.
        """
        return self.client.updateTimePeriod(**args)

    def delete_time_period(self, **args):
        """
        Delete a Time Period.
        :param name: time period name (or uuid)
        :param uuid: time period uuid (or name)
        :return: result dict
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
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
        

        Schema: `ListTimeScheduleReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
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
        

        Schema: `GetTimeScheduleReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getTimeSchedule(**args)["return"]["timeSchedule"]

    def add_time_schedule(self, **args):
        """
        Add a Time Schedule.
        :param name: time schedule name — required
        :return: result dict
        

        Schema: `timeSchedule` -> `XTimeSchedule`: `name` + `members`; optional `description`, `isPublished`, `timeScheduleCategory`, `todOwnerIdName`.
        """
        obj = self._build_object("addTimeSchedule", "timeSchedule", args)
        return self.client.addTimeSchedule(obj)

    def update_time_schedule(self, **args):
        """
        Update a Time Schedule.
        :param name: time schedule name (or uuid)
        :param uuid: time schedule uuid (or name)
        :return: result dict
        

        Schema: `UpdateTimeScheduleReq`: optional `newName`, optional choice of (optional `removeMembers`, `addMembers`), or `members`, `description`, `timeScheduleCategory`.
        """
        return self.client.updateTimeSchedule(**args)

    def delete_time_schedule(self, **args):
        """
        Delete a Time Schedule.
        :param name: time schedule name (or uuid)
        :param uuid: time schedule uuid (or name)
        :return: result dict
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
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
        

        Schema: `ListCallParkReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
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
        

        Schema: `GetCallParkReq`: optional `returnedTags`; one of `uuid`, or (`pattern`; optional `routePartitionName`).
        """
        return self.client.getCallPark(**args)["return"]["callPark"]

    def add_call_park(self, **args):
        """
        Add a Call Park entry.
        :param pattern: pattern — required
        :param callManagerName: Unified CM name — required
        :param routePartitionName: partition — optional
        :return: result dict
        

        Schema: `callPark` -> `XCallPark`: `pattern` + `callManagerName`; optional `description`, `routePartitionName`.
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
        

        Schema: `UpdateCallParkReq`: optional `newPattern`, `description`, `newRoutePartitionName`, `callManagerName`; one of `uuid`, or (`pattern`; optional `routePartitionName`).
        """
        return self.client.updateCallPark(**args)

    def delete_call_park(self, **args):
        """
        Delete a Call Park entry.
        :param pattern: call park pattern (or uuid)
        :param routePartitionName: partition — optional
        :param uuid: call park uuid (or pattern)
        :return: result dict
        

        Schema: `RemoveCallParkReq`: one of `uuid`, or (`pattern`; optional `routePartitionName`).
        """
        return self.client.removeCallPark(**args)

    # ------------------------------------------------------------------ #
    # AssignedPresenceServers — list only                                 #
    # ------------------------------------------------------------------ #

    def get_assigned_presence_servers(
        self,
        tagfilter={"name": "", "description": "", "nodeUsage": "", "numUsers": ""},
    ):
        """
        List all assigned Presence servers.
        :param tagfilter: AXL returned tags to include
        :return: list of dicts, empty when nothing matches
        

        Schema: `ListAssignedPresenceServersReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        response = self.client.listAssignedPresenceServers(
            {"name": "%"},
            returnedTags=tagfilter,
        )["return"]
        if response:
            return response["assignedPresenceServers"]
        return []

    # ------------------------------------------------------------------ #
    # UnassignedPresenceServers — list only                               #
    # ------------------------------------------------------------------ #

    def get_unassigned_presence_servers(
        self,
        tagfilter={"name": "", "description": "", "nodeUsage": ""},
    ):
        """
        List all unassigned Presence servers.
        :param tagfilter: AXL returned tags to include
        :return: list of dicts, empty when nothing matches
        

        Schema: `ListUnassignedPresenceServersReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        response = self.client.listUnassignedPresenceServers(
            {"name": "%"},
            returnedTags=tagfilter,
        )["return"]
        if response:
            return response["unassignedPresenceServers"]
        return []

    # ------------------------------------------------------------------ #
    # AssignedPresenceUsers — list only                                   #
    # ------------------------------------------------------------------ #

    def get_assigned_presence_users(
        self,
        tagfilter={"userid": "", "server": "", "presenceRedundancyGroup": ""},
    ):
        """
        List all assigned Presence users.
        :param tagfilter: AXL returned tags to include
        :return: list of dicts, empty when nothing matches
        

        Schema: `ListAssignedPresenceUsersReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        response = self.client.listAssignedPresenceUsers(
            {"userid": "%"},
            returnedTags=tagfilter,
        )["return"]
        if response:
            return response["assignedPresenceUsers"]
        return []

    # ------------------------------------------------------------------ #
    # UnassignedPresenceUsers — list only                                 #
    # ------------------------------------------------------------------ #

    def get_unassigned_presence_users(
        self,
        tagfilter={"userid": ""},
    ):
        """
        List all unassigned Presence users.
        :param tagfilter: AXL returned tags to include
        :return: list of dicts, empty when nothing matches
        

        Schema: `ListUnassignedPresenceUsersReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        response = self.client.listUnassignedPresenceUsers(
            {"userid": "%"},
            returnedTags=tagfilter,
        )["return"]
        if response:
            return response["unassignedPresenceUsers"]
        return []

    # ------------------------------------------------------------------ #
    # PresenceUser — assign / unassign only                               #
    # ------------------------------------------------------------------ #

    def assign_presence_user(self, userid, server):
        """
        Assign a user to a Presence server.
        :param userid: end-user ID to assign
        :param server: Presence server name to assign the user to
        :return: result dict
        

        Schema: `AssignPresenceUserReq`: `userid` + `server`.
        """
        return self.client.assignPresenceUser(userid=userid, server=server)

    def unassign_presence_user(self, userid):
        """
        Unassign a user from their Presence server.
        :param userid: end-user ID to unassign
        :return: result dict
        

        Schema: `UnassignPresenceUserReq`: `userid`.
        """
        return self.client.unassignPresenceUser(userid=userid)

    # ------------------------------------------------------------------ #
    # PresenceRedundancyGroup                                             #
    # ------------------------------------------------------------------ #

    def get_presence_redundancy_groups(
        self,
        tagfilter={
            "name": "",
            "description": "",
            "server1": "",
            "server2": "",
            "haEnabled": "",
        },
    ):
        """
        List all Presence Redundancy Groups.
        :param tagfilter: AXL returned tags to include
        :return: list of dicts, empty when nothing matches
        

        Schema: `ListPresenceRedundancyGroupReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        response = self.client.listPresenceRedundancyGroup(
            {"name": "%"},
            returnedTags=tagfilter,
        )["return"]
        if response:
            return response["presenceRedundancyGroup"]
        return []

    def get_presence_redundancy_group(self, **args):
        """
        Get a Presence Redundancy Group.
        :param name: group name (or uuid)
        :param uuid: group uuid (or name)
        :return: result dict
        

        Schema: `GetPresenceRedundancyGroupReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getPresenceRedundancyGroup(**args)["return"][
            "presenceRedundancyGroup"
        ]

    def add_presence_redundancy_group(self, **args):
        """
        Add a Presence Redundancy Group.
        :param name: group name — required
        :return: result dict
        

        Schema: `presenceRedundancyGroup` -> `XPresenceRedundancyGroup`: `name` + `server1`; optional `description`, `server2`, `haEnabled`.
        """
        obj = self._build_object(
            "addPresenceRedundancyGroup", "presenceRedundancyGroup", args
        )
        return self.client.addPresenceRedundancyGroup(obj)

    def update_presence_redundancy_group(self, **args):
        """
        Update a Presence Redundancy Group.
        :param name: group name (or uuid)
        :param uuid: group uuid (or name)
        :return: result dict
        

        Schema: `UpdatePresenceRedundancyGroupReq`: optional `newName`, `description`, `server1`, `server2`, `haEnabled`.
        """
        return self.client.updatePresenceRedundancyGroup(**args)

    def delete_presence_redundancy_group(self, **args):
        """
        Delete a Presence Redundancy Group.
        :param name: group name (or uuid)
        :param uuid: group uuid (or name)
        :return: result dict
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removePresenceRedundancyGroup(**args)

    # ------------------------------------------------------------------ #
    # ExpresswayCConfiguration                                            #
    # ------------------------------------------------------------------ #

    def get_expressway_c_configurations(
        self,
        tagfilter={
            "HostNameOrIP": "",
            "description": "",
            "X509SubjectNameorSubjectAlternateName": "",
        },
    ):
        """
        List all Expressway-C configurations.
        :param tagfilter: AXL returned tags to include
        :return: list of dicts, empty when nothing matches
        

        Schema: `ListExpresswayCConfigurationReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        response = self.client.listExpresswayCConfiguration(
            {"HostNameOrIP": "%"},
            returnedTags=tagfilter,
        )["return"]
        if response:
            return response["expresswayCConfiguration"]
        return []

    def get_expressway_c_configuration(self, **args):
        """
        Get an Expressway-C configuration.
        :param HostNameOrIP: host name or IP (or uuid)
        :param uuid: config uuid (or HostNameOrIP)
        :return: result dict
        

        Schema: `GetExpresswayCConfigurationReq`: optional `returnedTags`; one of `HostNameOrIP`, or `uuid`.
        """
        return self.client.getExpresswayCConfiguration(**args)["return"][
            "expresswayCConfiguration"
        ]

    def add_expressway_c_configuration(self, **args):
        """
        Add an Expressway-C configuration.
        :param HostNameOrIP: host name or IP — required
        :return: result dict
        

        Schema: `expresswayCConfiguration` -> `XExpresswayCConfiguration`: `HostNameOrIP`; optional `description`, `X509SubjectNameorSubjectAlternateName`.
        """
        obj = self._build_object(
            "addExpresswayCConfiguration", "expresswayCConfiguration", args
        )
        return self.client.addExpresswayCConfiguration(obj)

    def update_expressway_c_configuration(self, **args):
        """
        Update an Expressway-C configuration.
        :param HostNameOrIP: host name or IP (or uuid)
        :param uuid: config uuid (or HostNameOrIP)
        :return: result dict
        

        Schema: `UpdateExpresswayCConfigurationReq`: optional `newHostNameOrIP`, `description`, `X509SubjectNameorSubjectAlternateName`; one of `uuid`, or `HostNameOrIP`.
        """
        return self.client.updateExpresswayCConfiguration(**args)

    def delete_expressway_c_configuration(self, **args):
        """
        Delete an Expressway-C configuration.
        :param HostNameOrIP: host name or IP (or uuid)
        :param uuid: config uuid (or HostNameOrIP)
        :return: result dict
        

        Schema: `RemoveExpresswayCConfigurationReq`: one of `HostNameOrIP`, or `uuid`.
        """
        return self.client.removeExpresswayCConfiguration(**args)

    # ------------------------------------------------------------------ #
    # MraServiceDomain                                                    #
    # ------------------------------------------------------------------ #

    def get_mra_service_domains(
        self,
        tagfilter={"name": "", "isDefault": "", "serviceDomains": ""},
    ):
        """
        List all MRA Service Domains.
        :param tagfilter: AXL returned tags to include
        :return: list of dicts, empty when nothing matches
        

        Schema: `ListMraServiceDomainReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        response = self.client.listMraServiceDomain(
            {"name": "%"},
            returnedTags=tagfilter,
        )["return"]
        if response:
            return response["mraServiceDomain"]
        return []

    def get_mra_service_domain(self, **args):
        """
        Get an MRA Service Domain.
        :param name: domain name (or uuid)
        :param uuid: domain uuid (or name)
        :return: result dict
        

        Schema: `GetMraServiceDomainReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getMraServiceDomain(**args)["return"]["mraServiceDomain"]

    def add_mra_service_domain(self, **args):
        """
        Add an MRA Service Domain.
        :param name: domain name — required
        :return: result dict
        

        Schema: `mraServiceDomain` -> `XMraServiceDomain`: `name` + `serviceDomains`; optional `isDefault`.
        """
        obj = self._build_object("addMraServiceDomain", "mraServiceDomain", args)
        return self.client.addMraServiceDomain(obj)

    def update_mra_service_domain(self, **args):
        """
        Update an MRA Service Domain.
        :param name: domain name (or uuid)
        :param uuid: domain uuid (or name)
        :return: result dict
        

        Schema: `UpdateMraServiceDomainReq`: optional `newName`, `isDefault`, `serviceDomains`.
        """
        return self.client.updateMraServiceDomain(**args)

    def delete_mra_service_domain(self, **args):
        """
        Delete an MRA Service Domain.
        :param name: domain name (or uuid)
        :param uuid: domain uuid (or name)
        :return: result dict
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeMraServiceDomain(**args)
