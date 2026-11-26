"""
P2 System Mixin — batch B4
Adds application, change, NTP, syslog, authentication, and self-provisioning helpers.

Included groups:
  Application / Softkey:
    - ApplicationToSoftkeyTemplate  : add, remove
    - ApplicationServer             : add, get, list, update, remove
    - AppServerInfo                 : add, get, update, remove

  Options / Counts (read-only):
    - DeviceProfileOptions          : get
    - LineOptions                   : get
    - PhoneOptions                  : get
    - NumDevices                    : get

  Change notification:
    - Change                        : list_changes (listChange)

  Reset operations:
    - EnterpriseParametersReset     : do (doEnterpriseParametersReset)
    - ServiceParametersReset        : do (doServiceParametersReset)

  NTP / Syslog:
    - PhoneNtp                      : add, get, list, update, remove
    - SyslogConfiguration           : get, update

  SQL:
    - SQLQueryInactive              : sql_query_inactive (executeSQLQueryInactive)

  Users:
    - AuthenticateUser              : do (doAuthenticateUser)
    - CustomUserField               : add, get, list, update, remove

  Self-provisioning:
    - SelfProvisioning              : update
"""


class P2System:
    """Mixin providing application servers, change notification, NTP, syslog,
    authentication, custom user fields, and self-provisioning helpers."""

    # ------------------------------------------------------------------ #
    # ApplicationToSoftkeyTemplate                                         #
    # ------------------------------------------------------------------ #

    def add_application_to_softkey_template(self, **args):
        """
        Associate an application with a softkey template.
        :param softKeyTemplateName: softkey template name — required
        :param standardSoftKeyTemplateName: standard template name reference
        :return: result dictionary (uuid)
        """
        obj = self._build_object(
            "addApplicationToSoftkeyTemplate",
            "applicationToSoftkeyTemplate",
            args,
        )
        return self.client.addApplicationToSoftkeyTemplate(
            applicationToSoftkeyTemplate=obj
        )

    def remove_application_to_softkey_template(
        self, softKeyTemplateName, applicationName=""
    ):
        """
        Remove an application-to-softkey-template association.
        AXL does not expose a uuid identifier for this operation; use names.
        :param softKeyTemplateName: softkey template name — required
        :param applicationName: application name
        :return: result dictionary
        """
        return self.client.removeApplicationToSoftkeyTemplate(
            softKeyTemplateName=softKeyTemplateName,
            applicationName=applicationName,
        )

    # ------------------------------------------------------------------ #
    # DeviceProfileOptions (get only — no list in AXL)                    #
    # ------------------------------------------------------------------ #

    def get_device_profile_options(self, uuid):
        """
        Get device-profile option choices for a device profile UUID.
        :param uuid: device profile uuid — required
        :return: deviceProfileOptions dictionary
        """
        return self.client.getDeviceProfileOptions(uuid=uuid)["return"][
            "deviceProfileOptions"
        ]

    # ------------------------------------------------------------------ #
    # LineOptions (get only — no list in AXL)                             #
    # ------------------------------------------------------------------ #

    def get_line_options(self, uuid):
        """
        Get line option choices for a directory-number UUID.
        :param uuid: line (directory number) uuid — required
        :return: line options dictionary
        """
        return self.client.getLineOptions(uuid=uuid)["return"]["line"]

    # ------------------------------------------------------------------ #
    # NumDevices (get only — no list in AXL)                              #
    # ------------------------------------------------------------------ #

    def get_num_devices(self, device_class):
        """
        Get the number of registered devices of the specified class.
        :param device_class: device class string — required (e.g. 'Phone', 'Gateway')
                             maps to AXL 'class' element (required by schema)
        :return: integer count or result dictionary
        """
        return self.client.getNumDevices(**{"class": device_class})["return"]

    # ------------------------------------------------------------------ #
    # PhoneOptions (get only — no list in AXL)                            #
    # ------------------------------------------------------------------ #

    def get_phone_options(self, uuid):
        """
        Get phone option choices for a phone UUID.
        :param uuid: phone uuid — required
        :return: phone options dictionary
        """
        return self.client.getPhoneOptions(uuid=uuid)["return"]["phone"]

    # ------------------------------------------------------------------ #
    # AppServerInfo                                                        #
    # ------------------------------------------------------------------ #

    def add_app_server_info(self, **args):
        """
        Add application-server content info.
        :param appServerName: application server name reference — required
        :param appServerContent: content type
        :param content: content payload
        :return: result dictionary (uuid)
        """
        obj = self._build_object("addAppServerInfo", "appServerInfo", args)
        return self.client.addAppServerInfo(appServerInfo=obj)

    def get_app_server_info(self, uuid):
        """
        Get application-server info record.
        :param uuid: app server info uuid — required
        :return: appServerInfo dictionary
        """
        return self.client.getAppServerInfo(uuid=uuid)["return"]["appServerInfo"]

    def update_app_server_info(self, **args):
        """
        Update application-server info record.
        :param uuid: app server info uuid — required
        :param appServerName: new app server name reference
        :param appServerContent: content type
        :param content: content payload
        :return: result dictionary
        """
        return self.client.updateAppServerInfo(**args)

    def remove_app_server_info(self, uuid):
        """
        Remove application-server info record.
        :param uuid: app server info uuid — required
        :return: result dictionary
        """
        return self.client.removeAppServerInfo(uuid=uuid)

    # ------------------------------------------------------------------ #
    # ApplicationServer                                                    #
    # ------------------------------------------------------------------ #

    def add_application_server(self, **args):
        """
        Add an application server.
        :param appServerType: server type — required
        :param name: server name — required
        :param ipAddress: server IP address
        :param url: server URL
        :param endUserUrl: end-user URL
        :param processNodeName: associated process node
        :return: result dictionary (uuid)
        """
        obj = self._build_object("addApplicationServer", "applicationServer", args)
        return self.client.addApplicationServer(applicationServer=obj)

    def get_application_server(self, uuid):
        """
        Get an application server.
        :param uuid: application server uuid — required
        :return: applicationServer dictionary
        """
        return self.client.getApplicationServer(uuid=uuid)["return"][
            "applicationServer"
        ]

    def get_application_servers(
        self,
        search_name="%",
        tagfilter={"name": "", "ipAddress": "", "appServerType": ""},
    ):
        """
        List application servers.
        :param search_name: name search pattern, default '%' (all)
        :param tagfilter: AXL returned tags to include
        :return: list of applicationServer dictionaries, empty when nothing matches
        """
        result = self.client.listApplicationServer(
            {"name": search_name}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("applicationServer") or []

    def update_application_server(self, **args):
        """
        Update an application server.
        :param uuid: application server uuid — required
        :param newName: new name
        :param ipAddress: new IP address
        :return: result dictionary
        """
        return self.client.updateApplicationServer(**args)

    def remove_application_server(self, uuid):
        """
        Remove an application server.
        :param uuid: application server uuid — required
        :return: result dictionary
        """
        return self.client.removeApplicationServer(uuid=uuid)

    # ------------------------------------------------------------------ #
    # Change (listChange for change notification)                          #
    # ------------------------------------------------------------------ #

    def list_changes(self, startChangeId=None, objectList=None):
        """
        List change notifications.
        For the first call, omit startChangeId.  For subsequent calls pass a
        dict of ``{"_value_1": <nextStartChangeId int>, "queueId": "<queueId>"}``
        as returned in the prior response's ``queueInfo``.

        :param startChangeId: optional StartChangeId dict from prior queueInfo
        :param objectList: list of XChangeType strings to filter (default: all)
        :return: dict with 'queueInfo' and 'changes' keys (no 'return' wrapper)
        """
        kwargs = {}
        if startChangeId is not None:
            kwargs["startChangeId"] = startChangeId
        if objectList is not None:
            kwargs["objectList"] = objectList
        # listChange does NOT wrap its result in a 'return' key;
        # the zeep response dict already has 'queueInfo' and 'changes' at the top.
        return self.client.listChange(**kwargs)

    # ------------------------------------------------------------------ #
    # EnterpriseParametersReset (do* operation)                           #
    # ------------------------------------------------------------------ #

    def do_enterprise_parameters_reset(self):
        """
        Trigger a reset of enterprise parameters.
        :return: result dictionary
        """
        return self.client.doEnterpriseParametersReset()

    # ------------------------------------------------------------------ #
    # PhoneNtp                                                             #
    # ------------------------------------------------------------------ #

    def add_phone_ntp(self, **args):
        """
        Add a phone NTP server.
        :param ipAddress: IPv4 address of the NTP server
        :param ipv6Address: IPv6 address of the NTP server
        :param description: description
        :param mode: NTP mode
        :return: result dictionary (uuid)
        """
        obj = self._build_object("addPhoneNtp", "phoneNtp", args)
        return self.client.addPhoneNtp(phoneNtp=obj)

    def get_phone_ntp(self, uuid="", ipAddress="", ipv6Address=""):
        """
        Get a phone NTP server.
        AXL requires either uuid OR both ipAddress+ipv6Address (one may be an
        empty string; the other must be non-empty).

        :param uuid: NTP server uuid
        :param ipAddress: IPv4 address (use with ipv6Address="")
        :param ipv6Address: IPv6 address (use with ipAddress="")
        :return: phoneNtp dictionary
        """
        if uuid:
            kwargs = {"uuid": uuid}
        elif ipAddress or ipv6Address:
            kwargs = {"ipAddress": ipAddress, "ipv6Address": ipv6Address}
        else:
            raise ValueError("Provide uuid or at least one of ipAddress/ipv6Address")
        return self.client.getPhoneNtp(**kwargs)["return"]["phoneNtp"]

    def get_phone_ntps(
        self,
        search_ipAddress="%",
        tagfilter={"ipAddress": "", "ipv6Address": "", "description": "", "mode": ""},
    ):
        """
        List phone NTP servers.
        :param search_ipAddress: IP address search pattern, default '%' (all)
        :param tagfilter: AXL returned tags to include
        :return: list of phoneNtp dictionaries, empty when nothing matches
        """
        result = self.client.listPhoneNtp(
            {"ipAddress": search_ipAddress}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("phoneNtp") or []

    def update_phone_ntp(self, **args):
        """
        Update a phone NTP server.
        :param uuid: NTP server uuid (or ipAddress/ipv6Address)
        :param ipAddress: IPv4 address identifier
        :param ipv6Address: IPv6 address identifier
        :param newIpAddress: new IPv4 address
        :param newIpv6Address: new IPv6 address
        :return: result dictionary
        """
        return self.client.updatePhoneNtp(**args)

    def remove_phone_ntp(self, uuid="", ipAddress="", ipv6Address=""):
        """
        Remove a phone NTP server.
        AXL requires either uuid OR both ipAddress+ipv6Address (one may be "").

        :param uuid: NTP server uuid
        :param ipAddress: IPv4 address (use with ipv6Address="")
        :param ipv6Address: IPv6 address (use with ipAddress="")
        :return: result dictionary
        """
        if uuid:
            kwargs = {"uuid": uuid}
        elif ipAddress or ipv6Address:
            kwargs = {"ipAddress": ipAddress, "ipv6Address": ipv6Address}
        else:
            raise ValueError("Provide uuid or at least one of ipAddress/ipv6Address")
        return self.client.removePhoneNtp(**kwargs)

    # ------------------------------------------------------------------ #
    # SQLQueryInactive                                                     #
    # ------------------------------------------------------------------ #

    def sql_query_inactive(self, query):
        """
        Execute a SQL query against the inactive CUCM database node.
        Returns the same structure as sql_query / run_sql_query.

        :param query: SQL query string
        :return: {'num_rows': int, 'query': str, 'rows': [{column: value}]}
        """
        result = {"num_rows": 0, "query": query}

        sql_result = self.client.executeSQLQueryInactive(sql=query)

        num_rows = 0
        result_rows = []

        if sql_result is not None and sql_result["return"] is not None:
            for row in sql_result["return"]["row"]:
                row_dict = {}
                for column in row:
                    row_dict[column.tag] = column.text
                result_rows.append(row_dict)
                num_rows += 1

        result["num_rows"] = num_rows
        if num_rows > 0:
            result["rows"] = result_rows

        return result

    # ------------------------------------------------------------------ #
    # ServiceParametersReset (do* operation)                              #
    # ------------------------------------------------------------------ #

    def do_service_parameters_reset(self, processNodeName, service):
        """
        Trigger a reset of service parameters on a node.
        :param processNodeName: node hostname/IP
        :param service: service name
        :return: result dictionary
        """
        return self.client.doServiceParametersReset(
            processNodeName=processNodeName, service=service
        )

    # ------------------------------------------------------------------ #
    # SyslogConfiguration                                                  #
    # ------------------------------------------------------------------ #

    def get_syslog_configuration(self, serverName, serviceGroup, service, tagfilter=None):
        """
        Get syslog configuration for a server/service.
        :param serverName: syslog server name — required
        :param serviceGroup: service group — required
        :param service: service name — required
        :param tagfilter: AXL returned tags to include (optional)
        :return: syslogConfiguration dictionary
        """
        kwargs = {
            "serverName": serverName,
            "serviceGroup": serviceGroup,
            "service": service,
        }
        if tagfilter is not None:
            kwargs["returnedTags"] = tagfilter
        return self.client.getSyslogConfiguration(**kwargs)["return"][
            "syslogConfiguration"
        ]

    def update_syslog_configuration(self, serverName, serviceGroup, service, **args):
        """
        Update syslog configuration for a server/service.
        :param serverName: syslog server name — required
        :param serviceGroup: service group — required
        :param service: service name — required
        :param alarmConfigs: alarm configuration list
        :param EndPointAlarm: boolean, enable endpoint alarm
        :return: result dictionary
        """
        return self.client.updateSyslogConfiguration(
            serverName=serverName,
            serviceGroup=serviceGroup,
            service=service,
            **args,
        )

    # ------------------------------------------------------------------ #
    # AuthenticateUser (do* operation)                                    #
    # ------------------------------------------------------------------ #

    def do_authenticate_user(self, userid, password=None, pin=None):
        """
        Authenticate an end-user against CUCM.
        :param userid: end-user ID — required
        :param password: user password (or pin)
        :param pin: user PIN (or password)
        :return: dict with 'userAuthenticated' and optionally 'code', 'daysToExpiry'
        """
        kwargs = {"userid": userid}
        if password is not None:
            kwargs["password"] = password
        if pin is not None:
            kwargs["pin"] = pin
        return self.client.doAuthenticateUser(**kwargs)["return"]

    # ------------------------------------------------------------------ #
    # CustomUserField                                                      #
    # ------------------------------------------------------------------ #

    def add_custom_user_field(self, **args):
        """
        Add a custom user field definition.
        :param field: field name — required
        :return: result dictionary (uuid)
        """
        obj = self._build_object("addCustomUserField", "customUserField", args)
        return self.client.addCustomUserField(customUserField=obj)

    def get_custom_user_field(self, field="", uuid=""):
        """
        Get a custom user field definition.
        :param field: field name (or uuid)
        :param uuid: field uuid (or field name)
        :return: customUserField dictionary
        """
        if uuid:
            kwargs = {"uuid": uuid}
        elif field:
            kwargs = {"field": field}
        else:
            raise ValueError("Provide exactly one of field or uuid")
        return self.client.getCustomUserField(**kwargs)["return"]["customUserField"]

    def get_custom_user_fields(self, tagfilter={"field": ""}):
        """
        List custom user field definitions.
        :param tagfilter: AXL returned tags to include, e.g. {'field': ''}
        :return: list of customUserField dictionaries, empty when nothing matches
        """
        result = self.client.listCustomUserField(
            {"field": "%"}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("customUserField") or []

    def update_custom_user_field(self, **args):
        """
        Update a custom user field definition.
        :param uuid: field uuid (or field name)
        :param field: field name identifier
        :param newField: new field name
        :return: result dictionary
        """
        return self.client.updateCustomUserField(**args)

    def remove_custom_user_field(self, field="", uuid=""):
        """
        Remove a custom user field definition.
        :param field: field name (or uuid)
        :param uuid: field uuid (or field name)
        :return: result dictionary
        """
        if uuid:
            kwargs = {"uuid": uuid}
        elif field:
            kwargs = {"field": field}
        else:
            raise ValueError("Provide exactly one of field or uuid")
        return self.client.removeCustomUserField(**kwargs)

    # ------------------------------------------------------------------ #
    # SelfProvisioning (update only in AXL)                               #
    # ------------------------------------------------------------------ #

    def update_self_provisioning(self, **args):
        """
        Update self-provisioning settings.
        :param requireAuthentication: require auth for self-provisioning
        :param allowAuthentication: allow auth
        :param authenticationCode: shared authentication code
        :param ctiRoutePoint: CTI route point name
        :param applicationUser: application user name
        :return: result dictionary
        """
        return self.client.updateSelfProvisioning(**args)
