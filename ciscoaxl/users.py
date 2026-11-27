"""End user, application user, and remote destination wrappers.

Covered entities:
  AppUser, UserGroup, UserPhoneAssociation (add only),
  UserProfileProvision, RemoteDestination, RemoteDestinationProfile
"""


class UsersMixin:
    """End user, application user, and remote destination wrappers."""

    # ------------------------------------------------------------------
    # AppUser
    # ------------------------------------------------------------------

    def get_app_users(
        self,
        tagfilter={"userid": ""},
    ):
        """
        List all application users.
        :param tagfilter: AXL returned tags to include, e.g. {'userid': ''}
        :return: list of appUser dictionaries, empty when nothing matches
        

        Schema: `ListAppUserReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listAppUser(
            {"userid": "%"}, returnedTags=tagfilter
        )["return"]
        return (result or {}).get("appUser") or []

    def get_app_user(self, **args):
        """
        Get a single application user.
        :param userid: application user ID
        :param uuid: application user uuid
        :return: appUser dictionary
        

        Schema: `GetAppUserReq`: optional `returnedTags`; one of `userid`, or `uuid`.
        """
        return self.client.getAppUser(**args)["return"]["appUser"]

    def add_app_user(self, **args):
        """
        Add an application user.
        :param userid: application user ID - required
        :return: result dictionary
        

        Schema: `appUser` -> `XAppUser`: `userid`; optional `password`, `passwordCredentials`, `digestCredentials`, `presenceGroupName`, `acceptPresenceSubscription`, `acceptOutOfDialogRefer` and 5 more.
        """
        obj = self._build_object("addAppUser", "appUser", args)
        return self.client.addAppUser(appUser=obj)

    def update_app_user(self, **args):
        """
        Update an application user.
        :param userid: application user ID (or uuid)
        :param uuid: application user uuid (or userid)
        :return: result dictionary
        

        Schema: `UpdateAppUserReq`: optional `newUserid`, `password`, `passwordCredentials`, `digestCredentials`, `presenceGroupName`, `acceptPresenceSubscription` and 6 more; one of `uuid`, or `userid`.
        """
        return self.client.updateAppUser(**args)

    def delete_app_user(self, **args):
        """
        Delete an application user.
        :param userid: application user ID (or uuid)
        :param uuid: application user uuid (or userid)
        :return: result dictionary
        

        Schema: `RemoveAppUserReq`: one of `userid`, or `uuid`.
        """
        return self.client.removeAppUser(**args)

    # ------------------------------------------------------------------
    # UserGroup
    # ------------------------------------------------------------------

    def get_user_groups(
        self,
        tagfilter={"name": ""},
    ):
        """
        List all user groups.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of userGroup dictionaries, empty when nothing matches
        

        Schema: `ListUserGroupReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listUserGroup(
            {"name": "%"}, returnedTags=tagfilter
        )["return"]
        return (result or {}).get("userGroup") or []

    def get_user_group(self, **args):
        """
        Get a single user group.
        :param name: user group name
        :param uuid: user group uuid
        :return: userGroup dictionary
        

        Schema: `GetUserGroupReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getUserGroup(**args)["return"]["userGroup"]

    def add_user_group(self, **args):
        """
        Add a user group.
        :param name: user group name - required
        :return: result dictionary
        

        Schema: `userGroup` -> `XUserGroup`: `name`; optional `members`, `userRoles`.
        """
        obj = self._build_object("addUserGroup", "userGroup", args)
        return self.client.addUserGroup(userGroup=obj)

    def update_user_group(self, **args):
        """
        Update a user group.
        :param name: user group name (or uuid)
        :param uuid: user group uuid (or name)
        :return: result dictionary
        

        Schema: `UpdateUserGroupReq`: optional optional choice of (optional `removeMembers`, `addMembers`), or `members`, optional choice of (optional `removeUserRoles`, `addUserRoles`), or `userRoles`, `newName`.
        """
        return self.client.updateUserGroup(**args)

    def delete_user_group(self, **args):
        """
        Delete a user group.
        :param name: user group name (or uuid)
        :param uuid: user group uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeUserGroup(**args)

    # ------------------------------------------------------------------
    # UserPhoneAssociation  (add only per AXL schema)
    # ------------------------------------------------------------------

    def add_user_phone_association(self, **args):
        """
        Associate a phone with a user.
        :param userAssociation: user association details - required
        :return: result dictionary
        

        Schema: `userPhoneAssociation` -> `XUserPhoneAssociation`: `userId` + `lastName` + `productType` + `name` + `e164Mask` + `extension`; optional `password`, `pin`, `middleName`, `firstName`, `dnCssName`, `phoneCssName` and 5 more.
        """
        obj = self._build_object(
            "addUserPhoneAssociation", "userPhoneAssociation", args
        )
        return self.client.addUserPhoneAssociation(
            userPhoneAssociation=obj
        )

    # ------------------------------------------------------------------
    # UserProfileProvision
    # ------------------------------------------------------------------

    def get_user_profile_provisions(
        self,
        tagfilter={"name": "", "description": ""},
    ):
        """
        List all user profile provisions.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of userProfileProvision dictionaries, empty when nothing matches
        

        Schema: `ListUserProfileProvisionReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listUserProfileProvision(
            {"name": "%"}, returnedTags=tagfilter
        )["return"]
        return (result or {}).get("userProfileProvision") or []

    def get_user_profile_provision(self, **args):
        """
        Get a single user profile provision.
        :param name: user profile provision name
        :param uuid: user profile provision uuid
        :return: userProfileProvision dictionary
        

        Schema: `GetUserProfileProvisionReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getUserProfileProvision(**args)["return"][
            "userProfileProvision"
        ]

    def add_user_profile_provision(self, **args):
        """
        Add a user profile provision.
        :param name: user profile provision name - required
        :return: result dictionary
        

        Schema: `userProfileProvision` -> `XUserProfileProvision`: `name`; optional `description`, `deskPhones`, `mobileDevices`, `profile`, `universalLineTemplate`, `allowProvision` and 7 more.
        """
        obj = self._build_object(
            "addUserProfileProvision", "userProfileProvision", args
        )
        return self.client.addUserProfileProvision(
            userProfileProvision=obj
        )

    def update_user_profile_provision(self, **args):
        """
        Update a user profile provision.
        :param name: user profile provision name (or uuid)
        :param uuid: user profile provision uuid (or name)
        :return: result dictionary
        

        Schema: `UpdateUserProfileProvisionReq`: optional `newName`, `description`, `deskPhones`, `mobileDevices`, `profile`, `universalLineTemplate` and 8 more.
        """
        return self.client.updateUserProfileProvision(**args)

    def delete_user_profile_provision(self, **args):
        """
        Delete a user profile provision.
        :param name: user profile provision name (or uuid)
        :param uuid: user profile provision uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeUserProfileProvision(**args)

    # ------------------------------------------------------------------
    # RemoteDestination
    # ------------------------------------------------------------------

    def get_remote_destinations(
        self,
        tagfilter={"name": "", "destination": ""},
    ):
        """
        List all remote destinations.
        :param tagfilter: AXL returned tags to include, e.g. {'name': '', 'destination': ''}
        :return: list of remoteDestination dictionaries, empty when nothing matches
        

        Schema: `ListRemoteDestinationReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listRemoteDestination(
            {"name": "%"}, returnedTags=tagfilter
        )["return"]
        return (result or {}).get("remoteDestination") or []

    def get_remote_destination(self, **args):
        """
        Get a single remote destination.
        :param name: remote destination name
        :param uuid: remote destination uuid
        :return: remoteDestination dictionary
        

        Schema: `GetRemoteDestinationReq`: optional `returnedTags`; one of `destination`, or `uuid`.
        """
        return self.client.getRemoteDestination(**args)["return"][
            "remoteDestination"
        ]

    def add_remote_destination(self, **args):
        """
        Add a remote destination.
        :param name: remote destination name - required
        :param destination: destination number - required
        :return: result dictionary
        

        Schema: `remoteDestination` -> `XRemoteDestination`: `destination` + `answerTooSoonTimer` + `answerTooLateTimer` + `delayBeforeRingingCell` + `ownerUserId`; optional `name`, `enableUnifiedMobility`, `remoteDestinationProfileName`, `enableExtendAndConnect`, `ctiRemoteDeviceName`, `dualModeDeviceName` and 11 more.
        """
        obj = self._build_object(
            "addRemoteDestination", "remoteDestination", args
        )
        return self.client.addRemoteDestination(remoteDestination=obj)

    def update_remote_destination(self, **args):
        """
        Update a remote destination.
        :param name: remote destination name (or uuid)
        :param uuid: remote destination uuid (or name)
        :return: result dictionary
        

        Schema: `UpdateRemoteDestinationReq`: optional `newName`, `newDestination`, `answerTooSoonTimer`, `answerTooLateTimer`, `delayBeforeRingingCell`, `ownerUserId` and 16 more; one of `uuid`, or `destination`.
        """
        return self.client.updateRemoteDestination(**args)

    def delete_remote_destination(self, **args):
        """
        Delete a remote destination.
        :param name: remote destination name (or uuid)
        :param uuid: remote destination uuid (or name)
        :return: result dictionary
        

        Schema: `RemoveRemoteDestinationReq`: one of `destination`, or `uuid`.
        """
        return self.client.removeRemoteDestination(**args)

    # ------------------------------------------------------------------
    # RemoteDestinationProfile
    # ------------------------------------------------------------------

    def get_remote_destination_profiles(
        self,
        tagfilter={"name": "", "description": ""},
    ):
        """
        List all remote destination profiles.
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of remoteDestinationProfile dictionaries, empty when nothing matches
        

        Schema: `ListRemoteDestinationProfileReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listRemoteDestinationProfile(
            {"name": "%"}, returnedTags=tagfilter
        )["return"]
        return (result or {}).get("remoteDestinationProfile") or []

    def get_remote_destination_profile(self, **args):
        """
        Get a single remote destination profile.
        :param name: remote destination profile name
        :param uuid: remote destination profile uuid
        :return: remoteDestinationProfile dictionary
        

        Schema: `GetRemoteDestinationProfileReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getRemoteDestinationProfile(**args)["return"][
            "remoteDestinationProfile"
        ]

    def add_remote_destination_profile(self, **args):
        """
        Add a remote destination profile.
        :param name: remote destination profile name - required
        :return: result dictionary
        

        Schema: `remoteDestinationProfile` -> `XRemoteDestinationProfile`: `name` + `product` + `class` + `protocol` + `protocolSide` + `devicePoolName` + `callInfoPrivacyStatus` + `userId`; optional `description`, `callingSearchSpaceName`, `networkHoldMohAudioSourceId`, `userHoldMohAudioSourceId`, `lines`, `ignorePresentationIndicators` and 10 more.
        """
        obj = self._build_object(
            "addRemoteDestinationProfile", "remoteDestinationProfile", args
        )
        return self.client.addRemoteDestinationProfile(
            remoteDestinationProfile=obj
        )

    def update_remote_destination_profile(self, **args):
        """
        Update a remote destination profile.
        :param name: remote destination profile name (or uuid)
        :param uuid: remote destination profile uuid (or name)
        :return: result dictionary
        

        Schema: `UpdateRemoteDestinationProfileReq`: optional `newName`, `description`, `callingSearchSpaceName`, `devicePoolName`, `networkHoldMohAudioSourceId`, `userHoldMohAudioSourceId` and 14 more.
        """
        return self.client.updateRemoteDestinationProfile(**args)

    def delete_remote_destination_profile(self, **args):
        """
        Delete a remote destination profile.
        :param name: remote destination profile name (or uuid)
        :param uuid: remote destination profile uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeRemoteDestinationProfile(**args)
