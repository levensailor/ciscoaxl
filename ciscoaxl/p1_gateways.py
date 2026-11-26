"""
P1 Gateways Mixin — batch B3
Adds gateway, gateway-endpoint, and SIP-normalization methods.

Included groups:
  - Gateway                       : add, get, list, update, remove, apply, reset, restart
  - GatewayEndpointAnalogAccess   : add, get, update, remove
  - GatewayEndpointDigitalAccessPri : add, get, update, remove
  - GatewayEndpointDigitalAccessT1  : add, get, update, remove
  - GatewaySccpEndpoints          : add, get, update, remove
  - GatewaySubunits               : add, remove
  - UnitsToGateway                : add, remove
  - SIPNormalizationScript        : add, get, list, update, remove

Notes:
  * Gateway is identified by domainName (not name) or uuid.
  * Endpoint types (Analog/PRI/T1/SCCP) are identified by name or uuid.
  * GatewaySubunits / UnitsToGateway add use _build_object; remove accepts **args
    because their remove requests embed complex unit/subunit structures inline.
  * SIPNormalizationScript wrapper element is sIPNormalizationScript (capital I).
"""


class P1Gateways:
    """Mixin providing gateway, gateway-endpoint, and SIP-normalization helpers."""

    # ------------------------------------------------------------------ #
    # Internal helper                                                      #
    # ------------------------------------------------------------------ #

    def _identify_gateway(self, domainName="", uuid=""):
        """
        Build the domainName-or-uuid identifier used by Gateway operations.
        Gateway uses domainName (not name) as the primary identifier.

        :param domainName: gateway domain name / SCCP MAC address (or uuid)
        :param uuid: gateway uuid (or domainName)
        :return: {'domainName': domainName} or {'uuid': uuid}
        :raises ValueError: if both or neither are provided
        """
        if bool(domainName) == bool(uuid):
            raise ValueError("Provide exactly one of domainName or uuid")
        return {"domainName": domainName} if domainName else {"uuid": uuid}

    # ------------------------------------------------------------------ #
    # Gateway                                                              #
    # ------------------------------------------------------------------ #

    def add_gateway(self, **args):
        """
        Add a gateway (MGCP, SCCP, etc.).

        :param domainName: gateway FQDN or SCCP MAC address — required
        :param product: gateway product, e.g. 'Cisco VG200' — required
        :param protocol: gateway protocol, e.g. 'MGCP' or 'SCCP' — required
        :param callManagerGroupName: associated CM group — required
        :param description: description
        :return: result dictionary (uuid)
        """
        gw = self._build_object("addGateway", "gateway", args)
        return self.client.addGateway(gateway=gw)

    def get_gateway(self, domainName="", uuid=""):
        """
        Get a gateway.

        :param domainName: gateway domain name / SCCP MAC (or uuid)
        :param uuid: gateway uuid (or domainName)
        :return: gateway dictionary
        """
        return self.client.getGateway(
            **self._identify_gateway(domainName=domainName, uuid=uuid)
        )["return"]["gateway"]

    def get_gateways(self, tagfilter={"domainName": "", "description": ""}):
        """
        List gateways.

        :param tagfilter: AXL returned tags to include, e.g. {'domainName': ''}
        :return: list of gateway dictionaries, empty when nothing matches
        """
        result = self.client.listGateway(
            {"domainName": "%"}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("gateway", []) or []

    def update_gateway(self, **args):
        """
        Update a gateway.

        :param domainName: gateway domain name (or uuid)
        :param uuid: gateway uuid (or domainName)
        :param newDomainName: new domain name
        :param description: description
        :return: result dictionary
        """
        return self.client.updateGateway(**args)

    def remove_gateway(self, domainName="", uuid=""):
        """
        Remove a gateway.

        :param domainName: gateway domain name / SCCP MAC (or uuid)
        :param uuid: gateway uuid (or domainName)
        :return: result dictionary
        """
        return self.client.removeGateway(
            **self._identify_gateway(domainName=domainName, uuid=uuid)
        )

    def apply_gateway(self, domainName="", uuid=""):
        """
        Apply gateway configuration.

        :param domainName: gateway domain name / SCCP MAC (or uuid)
        :param uuid: gateway uuid (or domainName)
        :return: result dictionary
        """
        return self.client.applyGateway(
            **self._identify_gateway(domainName=domainName, uuid=uuid)
        )

    def reset_gateway(self, domainName="", uuid=""):
        """
        Reset a gateway.

        :param domainName: gateway domain name / SCCP MAC (or uuid)
        :param uuid: gateway uuid (or domainName)
        :return: result dictionary
        """
        return self.client.resetGateway(
            **self._identify_gateway(domainName=domainName, uuid=uuid)
        )

    def restart_gateway(self, domainName="", uuid=""):
        """
        Restart a gateway.

        :param domainName: gateway domain name / SCCP MAC (or uuid)
        :param uuid: gateway uuid (or domainName)
        :return: result dictionary
        """
        return self.client.restartGateway(
            **self._identify_gateway(domainName=domainName, uuid=uuid)
        )

    # ------------------------------------------------------------------ #
    # GatewayEndpointAnalogAccess                                          #
    # ------------------------------------------------------------------ #

    def add_gateway_endpoint_analog_access(self, **args):
        """
        Add a gateway analog-access endpoint.

        :param domainName: parent gateway domain name — required (or gatewayUuid)
        :param gatewayUuid: parent gateway uuid — required (or domainName)
        :param unit: slot index on the gateway
        :param subunit: subunit index
        :param index: port index
        :return: result dictionary (uuid)
        """
        ep = self._build_object(
            "addGatewayEndpointAnalogAccess",
            "gatewayEndpointAnalogAccess",
            args,
        )
        return self.client.addGatewayEndpointAnalogAccess(
            gatewayEndpointAnalogAccess=ep
        )

    def get_gateway_endpoint_analog_access(self, name="", uuid=""):
        """
        Get a gateway analog-access endpoint.

        :param name: endpoint name (or uuid)
        :param uuid: endpoint uuid (or name)
        :return: endpoint dictionary
        """
        return self.client.getGatewayEndpointAnalogAccess(
            **self._identify(name=name, uuid=uuid)
        )["return"]["gatewayEndpointAnalogAccess"]

    def update_gateway_endpoint_analog_access(self, **args):
        """
        Update a gateway analog-access endpoint.

        :param name: endpoint name (or uuid)
        :param uuid: endpoint uuid (or name)
        :param endpoint: nested endpoint update dict
        :return: result dictionary
        """
        return self.client.updateGatewayEndpointAnalogAccess(**args)

    def remove_gateway_endpoint_analog_access(self, name="", uuid=""):
        """
        Remove a gateway analog-access endpoint.

        :param name: endpoint name (or uuid)
        :param uuid: endpoint uuid (or name)
        :return: result dictionary
        """
        return self.client.removeGatewayEndpointAnalogAccess(
            **self._identify(name=name, uuid=uuid)
        )

    # ------------------------------------------------------------------ #
    # GatewayEndpointDigitalAccessPri                                      #
    # ------------------------------------------------------------------ #

    def add_gateway_endpoint_digital_access_pri(self, **args):
        """
        Add a gateway digital-access PRI endpoint.

        :param domainName: parent gateway domain name — required (or gatewayUuid)
        :param gatewayUuid: parent gateway uuid — required (or domainName)
        :param unit: slot index
        :param subunit: subunit index
        :param index: port index
        :return: result dictionary (uuid)
        """
        ep = self._build_object(
            "addGatewayEndpointDigitalAccessPri",
            "gatewayEndpointDigitalAccessPri",
            args,
        )
        return self.client.addGatewayEndpointDigitalAccessPri(
            gatewayEndpointDigitalAccessPri=ep
        )

    def get_gateway_endpoint_digital_access_pri(self, name="", uuid=""):
        """
        Get a gateway digital-access PRI endpoint.

        :param name: endpoint name (or uuid)
        :param uuid: endpoint uuid (or name)
        :return: endpoint dictionary
        """
        return self.client.getGatewayEndpointDigitalAccessPri(
            **self._identify(name=name, uuid=uuid)
        )["return"]["gatewayEndpointDigitalAccessPri"]

    def update_gateway_endpoint_digital_access_pri(self, **args):
        """
        Update a gateway digital-access PRI endpoint.

        :param name: endpoint name (or uuid)
        :param uuid: endpoint uuid (or name)
        :param endpoint: nested endpoint update dict
        :return: result dictionary
        """
        return self.client.updateGatewayEndpointDigitalAccessPri(**args)

    def remove_gateway_endpoint_digital_access_pri(self, name="", uuid=""):
        """
        Remove a gateway digital-access PRI endpoint.

        :param name: endpoint name (or uuid)
        :param uuid: endpoint uuid (or name)
        :return: result dictionary
        """
        return self.client.removeGatewayEndpointDigitalAccessPri(
            **self._identify(name=name, uuid=uuid)
        )

    # ------------------------------------------------------------------ #
    # GatewayEndpointDigitalAccessT1                                       #
    # ------------------------------------------------------------------ #

    def add_gateway_endpoint_digital_access_t1(self, **args):
        """
        Add a gateway digital-access T1 endpoint.

        :param domainName: parent gateway domain name — required (or gatewayUuid)
        :param gatewayUuid: parent gateway uuid — required (or domainName)
        :param unit: slot index
        :param subunit: subunit index
        :param index: port index
        :return: result dictionary (uuid)
        """
        ep = self._build_object(
            "addGatewayEndpointDigitalAccessT1",
            "gatewayEndpointDigitalAccessT1",
            args,
        )
        return self.client.addGatewayEndpointDigitalAccessT1(
            gatewayEndpointDigitalAccessT1=ep
        )

    def get_gateway_endpoint_digital_access_t1(self, name="", uuid=""):
        """
        Get a gateway digital-access T1 endpoint.

        :param name: endpoint name (or uuid)
        :param uuid: endpoint uuid (or name)
        :return: endpoint dictionary
        """
        return self.client.getGatewayEndpointDigitalAccessT1(
            **self._identify(name=name, uuid=uuid)
        )["return"]["gatewayEndpointDigitalAccessT1"]

    def update_gateway_endpoint_digital_access_t1(self, **args):
        """
        Update a gateway digital-access T1 endpoint.

        :param name: endpoint name (or uuid)
        :param uuid: endpoint uuid (or name)
        :param endpoint: nested endpoint update dict
        :return: result dictionary
        """
        return self.client.updateGatewayEndpointDigitalAccessT1(**args)

    def remove_gateway_endpoint_digital_access_t1(self, name="", uuid=""):
        """
        Remove a gateway digital-access T1 endpoint.

        :param name: endpoint name (or uuid)
        :param uuid: endpoint uuid (or name)
        :return: result dictionary
        """
        return self.client.removeGatewayEndpointDigitalAccessT1(
            **self._identify(name=name, uuid=uuid)
        )

    # ------------------------------------------------------------------ #
    # GatewaySccpEndpoints                                                 #
    # ------------------------------------------------------------------ #

    def add_gateway_sccp_endpoints(self, **args):
        """
        Add a gateway SCCP endpoints block.

        :param domainName: parent gateway MAC address — required (or gatewayUuid)
        :param gatewayUuid: parent gateway uuid — required (or domainName)
        :param unit: slot/unit index
        :param subunit: subunit index
        :param index: port index
        :return: result dictionary (uuid)
        """
        ep = self._build_object(
            "addGatewaySccpEndpoints",
            "gatewaySccpEndpoints",
            args,
        )
        return self.client.addGatewaySccpEndpoints(gatewaySccpEndpoints=ep)

    def get_gateway_sccp_endpoints(self, name="", uuid=""):
        """
        Get a gateway SCCP endpoints block.

        :param name: endpoint name (or uuid)
        :param uuid: endpoint uuid (or name)
        :return: gatewaySccpEndpoints dictionary
        """
        return self.client.getGatewaySccpEndpoints(
            **self._identify(name=name, uuid=uuid)
        )["return"]["gatewaySccpEndpoints"]

    def update_gateway_sccp_endpoints(self, **args):
        """
        Update a gateway SCCP endpoints block.

        :param name: endpoint name (or uuid)
        :param uuid: endpoint uuid (or name)
        :param endpoint: nested endpoint update dict
        :return: result dictionary
        """
        return self.client.updateGatewaySccpEndpoints(**args)

    def remove_gateway_sccp_endpoints(self, name="", uuid=""):
        """
        Remove a gateway SCCP endpoints block.

        :param name: endpoint name (or uuid)
        :param uuid: endpoint uuid (or name)
        :return: result dictionary
        """
        return self.client.removeGatewaySccpEndpoints(
            **self._identify(name=name, uuid=uuid)
        )

    # ------------------------------------------------------------------ #
    # GatewaySubunits                                                      #
    # ------------------------------------------------------------------ #

    def add_gateway_subunits(self, **args):
        """
        Add subunits to a gateway slot.

        :param domainName: gateway domain name / SCCP MAC (or gatewayUuid)
        :param gatewayUuid: gateway uuid (or domainName)
        :param unit: parent unit/slot index (integer)
        :param subunits: dict with list of subunit dicts, e.g.
                         {'subunit': [{'index': 0, 'product': '...'}]}
        :return: result dictionary
        """
        gs = self._build_object("addGatewaySubunits", "gatewaySubunits", args)
        return self.client.addGatewaySubunits(gatewaySubunits=gs)

    def remove_gateway_subunits(self, **args):
        """
        Remove subunits from a gateway slot.

        Pass keyword arguments matching the AXL RemoveGatewaySubunitsReq schema:

        :param domainName: gateway domain name / SCCP MAC (or gatewayUuid)
        :param gatewayUuid: gateway uuid (or domainName)
        :param unit: parent unit/slot index (non-negative integer)
        :param subunits: dict with list of subunit index dicts, e.g.
                         {'subunit': [{'index': 0}]}
        :return: result dictionary
        """
        return self.client.removeGatewaySubunits(**args)

    # ------------------------------------------------------------------ #
    # UnitsToGateway                                                       #
    # ------------------------------------------------------------------ #

    def add_units_to_gateway(self, **args):
        """
        Add units (slots/modules) to a gateway.

        :param domainName: gateway domain name / SCCP MAC (or gatewayUuid)
        :param gatewayUuid: gateway uuid (or domainName)
        :param units: dict with list of unit dicts, e.g.
                      {'unit': [{'index': 0, 'product': '...'}]}
        :return: result dictionary
        """
        utg = self._build_object("addUnitsToGateway", "unitsToGateway", args)
        return self.client.addUnitsToGateway(unitsToGateway=utg)

    def remove_units_to_gateway(self, **args):
        """
        Remove units from a gateway.

        Pass keyword arguments matching the AXL RemoveUnitsToGatewayReq schema:

        :param domainName: gateway domain name / SCCP MAC (or gatewayUuid)
        :param gatewayUuid: gateway uuid (or domainName)
        :param units: dict with list of unit index dicts, e.g.
                      {'unit': [{'index': 0}]}
        :return: result dictionary
        """
        return self.client.removeUnitsToGateway(**args)

    # ------------------------------------------------------------------ #
    # SIPNormalizationScript                                               #
    # ------------------------------------------------------------------ #

    def add_sip_normalization_script(self, **args):
        """
        Add a SIP normalisation script.

        :param name: script name — required
        :param content: Lua script content — required
        :param description: description
        :param scriptExecutionErrorRecoveryAction: e.g. 'Message Rollback Only'
        :param systemResourceErrorRecoveryAction: e.g. 'Disable Script'
        :param maxMemoryThreshold: memory limit, default '50'
        :param maxLuaInstructionsThreshold: instruction limit, default '1000'
        :return: result dictionary (uuid)
        """
        script = self._build_object(
            "addSIPNormalizationScript",
            "sIPNormalizationScript",
            args,
        )
        return self.client.addSIPNormalizationScript(
            sIPNormalizationScript=script
        )

    def get_sip_normalization_script(self, name="", uuid=""):
        """
        Get a SIP normalisation script.

        :param name: script name (or uuid)
        :param uuid: script uuid (or name)
        :return: sIPNormalizationScript dictionary
        """
        return self.client.getSIPNormalizationScript(
            **self._identify(name=name, uuid=uuid)
        )["return"]["sIPNormalizationScript"]

    def get_sip_normalization_scripts(
        self, tagfilter={"name": "", "description": ""}
    ):
        """
        List SIP normalisation scripts.

        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of sIPNormalizationScript dictionaries, empty when nothing matches
        """
        result = self.client.listSIPNormalizationScript(
            {"name": "%"}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("sIPNormalizationScript", []) or []

    def update_sip_normalization_script(self, **args):
        """
        Update a SIP normalisation script.

        :param name: script name (or uuid)
        :param uuid: script uuid (or name)
        :param newName: new script name
        :param content: new Lua content
        :param description: description
        :return: result dictionary
        """
        return self.client.updateSIPNormalizationScript(**args)

    def remove_sip_normalization_script(self, name="", uuid=""):
        """
        Remove a SIP normalisation script.

        :param name: script name (or uuid)
        :param uuid: script uuid (or name)
        :return: result dictionary
        """
        return self.client.removeSIPNormalizationScript(
            **self._identify(name=name, uuid=uuid)
        )
