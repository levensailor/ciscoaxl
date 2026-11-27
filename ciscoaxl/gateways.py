"""Gateway, gateway endpoint, SIP normalization, and legacy gateway wrappers.

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

Adds legacy Catalyst voice-gateway, Gatekeeper, BRI endpoint, H.323 phone,
and VG224 methods.

Included groups:
  - CiscoCatalyst600024PortFXSGateway  : add, get, list, update, remove,
                                          apply, reset, restart
  - CiscoCatalyst6000E1VoIPGateway     : add, get, list, update, remove,
                                          apply, reset, restart
  - CiscoCatalyst6000T1VoIPGatewayPri  : add, get, list, update, remove,
                                          apply, reset, restart
  - CiscoCatalyst6000T1VoIPGatewayT1   : add, get, list, update, remove,
                                          apply, reset, restart
  - Gatekeeper                         : add, get, list, update, remove,
                                          apply, reset, restart
  - GatewayEndpointDigitalAccessBri    : add, get, update, remove
  - H323Phone                          : add, get, list, update, remove,
                                          apply, reset, restart
  - Vg224                              : add, get, update, remove,
                                          reset, restart

Notes:
  * CiscoCatalyst* and Gatekeeper / H323Phone are identified by name or uuid.
  * Vg224 is identified by domainName or uuid (matches Gateway pattern).
  * GatewayEndpointDigitalAccessBri is identified by name or uuid;
    the add wrapper element contains a domainName/gatewayUuid choice.
  * Vg224 has no listVg224 and no applyVg224 AXL operation.
"""


class GatewaysMixin:
    """Gateway, gateway endpoint, SIP normalization, and legacy gateway wrappers."""

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

    # ------------------------------------------------------------------ #
    # Internal helper (domain-name style, same as Gateway)                #
    # ------------------------------------------------------------------ #

    def _identify_domain(self, domainName="", uuid=""):
        """
        Build a domainName-or-uuid identifier.

        :param domainName: device domain name (or uuid)
        :param uuid: device uuid (or domainName)
        :return: {'domainName': domainName} or {'uuid': uuid}
        :raises ValueError: if both or neither are provided
        """
        if bool(domainName) == bool(uuid):
            raise ValueError("Provide exactly one of domainName or uuid")
        return {"domainName": domainName} if domainName else {"uuid": uuid}

    # ------------------------------------------------------------------ #
    # CiscoCatalyst600024PortFXSGateway                                   #
    # ------------------------------------------------------------------ #

    def add_cisco_catalyst600024_port_fxs_gateway(self, **args):
        """
        Add a Cisco Catalyst 6000 24-port FXS gateway.

        :param name: device name — required
        :param description: description
        :param product: gateway product string — required
        :param protocol: gateway protocol — required
        :param callManagerGroupName: associated CM group
        :return: result dictionary (uuid)
        """
        gw = self._build_object(
            "addCiscoCatalyst600024PortFXSGateway",
            "ciscoCatalyst600024PortFXSGateway",
            args,
        )
        return self.client.addCiscoCatalyst600024PortFXSGateway(
            ciscoCatalyst600024PortFXSGateway=gw
        )

    def get_cisco_catalyst600024_port_fxs_gateway(self, name="", uuid=""):
        """
        Get a Cisco Catalyst 6000 24-port FXS gateway.

        :param name: device name (or uuid)
        :param uuid: device uuid (or name)
        :return: ciscoCatalyst600024PortFXSGateway dictionary
        """
        return self.client.getCiscoCatalyst600024PortFXSGateway(
            **self._identify(name=name, uuid=uuid)
        )["return"]["ciscoCatalyst600024PortFXSGateway"]

    def get_cisco_catalyst600024_port_fxs_gateways(
        self, tagfilter={"name": "", "description": ""}
    ):
        """
        List Cisco Catalyst 6000 24-port FXS gateways.

        :param tagfilter: AXL returned tags to include
        :return: list of ciscoCatalyst600024PortFXSGateway dicts, empty on no results
        """
        result = self.client.listCiscoCatalyst600024PortFXSGateway(
            {"name": "%"}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("ciscoCatalyst600024PortFXSGateway", []) or []

    def update_cisco_catalyst600024_port_fxs_gateway(self, **args):
        """
        Update a Cisco Catalyst 6000 24-port FXS gateway.

        :param name: device name (or uuid)
        :param uuid: device uuid (or name)
        :return: result dictionary
        """
        return self.client.updateCiscoCatalyst600024PortFXSGateway(**args)

    def remove_cisco_catalyst600024_port_fxs_gateway(self, name="", uuid=""):
        """
        Remove a Cisco Catalyst 6000 24-port FXS gateway.

        :param name: device name (or uuid)
        :param uuid: device uuid (or name)
        :return: result dictionary
        """
        return self.client.removeCiscoCatalyst600024PortFXSGateway(
            **self._identify(name=name, uuid=uuid)
        )

    def apply_cisco_catalyst600024_port_fxs_gateway(self, name="", uuid=""):
        """
        Apply Cisco Catalyst 6000 24-port FXS gateway configuration.

        :param name: device name (or uuid)
        :param uuid: device uuid (or name)
        :return: result dictionary
        """
        return self.client.applyCiscoCatalyst600024PortFXSGateway(
            **self._identify(name=name, uuid=uuid)
        )

    def reset_cisco_catalyst600024_port_fxs_gateway(self, name="", uuid=""):
        """
        Reset a Cisco Catalyst 6000 24-port FXS gateway.

        :param name: device name (or uuid)
        :param uuid: device uuid (or name)
        :return: result dictionary
        """
        return self.client.resetCiscoCatalyst600024PortFXSGateway(
            **self._identify(name=name, uuid=uuid)
        )

    def restart_cisco_catalyst600024_port_fxs_gateway(self, name="", uuid=""):
        """
        Restart a Cisco Catalyst 6000 24-port FXS gateway.

        :param name: device name (or uuid)
        :param uuid: device uuid (or name)
        :return: result dictionary
        """
        return self.client.restartCiscoCatalyst600024PortFXSGateway(
            **self._identify(name=name, uuid=uuid)
        )

    # ------------------------------------------------------------------ #
    # CiscoCatalyst6000E1VoIPGateway                                      #
    # ------------------------------------------------------------------ #

    def add_cisco_catalyst6000_e1_voip_gateway(self, **args):
        """
        Add a Cisco Catalyst 6000 E1 VoIP gateway.

        :param name: device name — required
        :param description: description
        :param product: gateway product string — required
        :param protocol: gateway protocol — required
        :return: result dictionary (uuid)
        """
        gw = self._build_object(
            "addCiscoCatalyst6000E1VoIPGateway",
            "ciscoCatalyst6000E1VoIPGateway",
            args,
        )
        return self.client.addCiscoCatalyst6000E1VoIPGateway(
            ciscoCatalyst6000E1VoIPGateway=gw
        )

    def get_cisco_catalyst6000_e1_voip_gateway(self, name="", uuid=""):
        """
        Get a Cisco Catalyst 6000 E1 VoIP gateway.

        :param name: device name (or uuid)
        :param uuid: device uuid (or name)
        :return: ciscoCatalyst6000E1VoIPGateway dictionary
        """
        return self.client.getCiscoCatalyst6000E1VoIPGateway(
            **self._identify(name=name, uuid=uuid)
        )["return"]["ciscoCatalyst6000E1VoIPGateway"]

    def get_cisco_catalyst6000_e1_voip_gateways(
        self, tagfilter={"name": "", "description": ""}
    ):
        """
        List Cisco Catalyst 6000 E1 VoIP gateways.

        :param tagfilter: AXL returned tags to include
        :return: list of ciscoCatalyst6000E1VoIPGateway dicts, empty on no results
        """
        result = self.client.listCiscoCatalyst6000E1VoIPGateway(
            {"name": "%"}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("ciscoCatalyst6000E1VoIPGateway", []) or []

    def update_cisco_catalyst6000_e1_voip_gateway(self, **args):
        """
        Update a Cisco Catalyst 6000 E1 VoIP gateway.

        :param name: device name (or uuid)
        :param uuid: device uuid (or name)
        :return: result dictionary
        """
        return self.client.updateCiscoCatalyst6000E1VoIPGateway(**args)

    def remove_cisco_catalyst6000_e1_voip_gateway(self, name="", uuid=""):
        """
        Remove a Cisco Catalyst 6000 E1 VoIP gateway.

        :param name: device name (or uuid)
        :param uuid: device uuid (or name)
        :return: result dictionary
        """
        return self.client.removeCiscoCatalyst6000E1VoIPGateway(
            **self._identify(name=name, uuid=uuid)
        )

    def apply_cisco_catalyst6000_e1_voip_gateway(self, name="", uuid=""):
        """
        Apply Cisco Catalyst 6000 E1 VoIP gateway configuration.

        :param name: device name (or uuid)
        :param uuid: device uuid (or name)
        :return: result dictionary
        """
        return self.client.applyCiscoCatalyst6000E1VoIPGateway(
            **self._identify(name=name, uuid=uuid)
        )

    def reset_cisco_catalyst6000_e1_voip_gateway(self, name="", uuid=""):
        """
        Reset a Cisco Catalyst 6000 E1 VoIP gateway.

        :param name: device name (or uuid)
        :param uuid: device uuid (or name)
        :return: result dictionary
        """
        return self.client.resetCiscoCatalyst6000E1VoIPGateway(
            **self._identify(name=name, uuid=uuid)
        )

    def restart_cisco_catalyst6000_e1_voip_gateway(self, name="", uuid=""):
        """
        Restart a Cisco Catalyst 6000 E1 VoIP gateway.

        :param name: device name (or uuid)
        :param uuid: device uuid (or name)
        :return: result dictionary
        """
        return self.client.restartCiscoCatalyst6000E1VoIPGateway(
            **self._identify(name=name, uuid=uuid)
        )

    # ------------------------------------------------------------------ #
    # CiscoCatalyst6000T1VoIPGatewayPri                                   #
    # ------------------------------------------------------------------ #

    def add_cisco_catalyst6000_t1_voip_gateway_pri(self, **args):
        """
        Add a Cisco Catalyst 6000 T1 VoIP gateway (PRI).

        :param name: device name — required
        :param description: description
        :param product: gateway product string — required
        :param protocol: gateway protocol — required
        :return: result dictionary (uuid)
        """
        gw = self._build_object(
            "addCiscoCatalyst6000T1VoIPGatewayPri",
            "ciscoCatalyst6000T1VoIPGatewayPri",
            args,
        )
        return self.client.addCiscoCatalyst6000T1VoIPGatewayPri(
            ciscoCatalyst6000T1VoIPGatewayPri=gw
        )

    def get_cisco_catalyst6000_t1_voip_gateway_pri(self, name="", uuid=""):
        """
        Get a Cisco Catalyst 6000 T1 VoIP gateway (PRI).

        :param name: device name (or uuid)
        :param uuid: device uuid (or name)
        :return: ciscoCatalyst6000T1VoIPGatewayPri dictionary
        """
        return self.client.getCiscoCatalyst6000T1VoIPGatewayPri(
            **self._identify(name=name, uuid=uuid)
        )["return"]["ciscoCatalyst6000T1VoIPGatewayPri"]

    def get_cisco_catalyst6000_t1_voip_gateway_pris(
        self, tagfilter={"name": "", "description": ""}
    ):
        """
        List Cisco Catalyst 6000 T1 VoIP gateways (PRI).

        :param tagfilter: AXL returned tags to include
        :return: list of ciscoCatalyst6000T1VoIPGatewayPri dicts, empty on no results
        """
        result = self.client.listCiscoCatalyst6000T1VoIPGatewayPri(
            {"name": "%"}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("ciscoCatalyst6000T1VoIPGatewayPri", []) or []

    def update_cisco_catalyst6000_t1_voip_gateway_pri(self, **args):
        """
        Update a Cisco Catalyst 6000 T1 VoIP gateway (PRI).

        :param name: device name (or uuid)
        :param uuid: device uuid (or name)
        :return: result dictionary
        """
        return self.client.updateCiscoCatalyst6000T1VoIPGatewayPri(**args)

    def remove_cisco_catalyst6000_t1_voip_gateway_pri(self, name="", uuid=""):
        """
        Remove a Cisco Catalyst 6000 T1 VoIP gateway (PRI).

        :param name: device name (or uuid)
        :param uuid: device uuid (or name)
        :return: result dictionary
        """
        return self.client.removeCiscoCatalyst6000T1VoIPGatewayPri(
            **self._identify(name=name, uuid=uuid)
        )

    def apply_cisco_catalyst6000_t1_voip_gateway_pri(self, name="", uuid=""):
        """
        Apply Cisco Catalyst 6000 T1 VoIP gateway (PRI) configuration.

        :param name: device name (or uuid)
        :param uuid: device uuid (or name)
        :return: result dictionary
        """
        return self.client.applyCiscoCatalyst6000T1VoIPGatewayPri(
            **self._identify(name=name, uuid=uuid)
        )

    def reset_cisco_catalyst6000_t1_voip_gateway_pri(self, name="", uuid=""):
        """
        Reset a Cisco Catalyst 6000 T1 VoIP gateway (PRI).

        :param name: device name (or uuid)
        :param uuid: device uuid (or name)
        :return: result dictionary
        """
        return self.client.resetCiscoCatalyst6000T1VoIPGatewayPri(
            **self._identify(name=name, uuid=uuid)
        )

    def restart_cisco_catalyst6000_t1_voip_gateway_pri(self, name="", uuid=""):
        """
        Restart a Cisco Catalyst 6000 T1 VoIP gateway (PRI).

        :param name: device name (or uuid)
        :param uuid: device uuid (or name)
        :return: result dictionary
        """
        return self.client.restartCiscoCatalyst6000T1VoIPGatewayPri(
            **self._identify(name=name, uuid=uuid)
        )

    # ------------------------------------------------------------------ #
    # CiscoCatalyst6000T1VoIPGatewayT1                                    #
    # ------------------------------------------------------------------ #

    def add_cisco_catalyst6000_t1_voip_gateway_t1(self, **args):
        """
        Add a Cisco Catalyst 6000 T1 VoIP gateway (T1).

        :param name: device name — required
        :param description: description
        :param product: gateway product string — required
        :param protocol: gateway protocol — required
        :return: result dictionary (uuid)
        """
        gw = self._build_object(
            "addCiscoCatalyst6000T1VoIPGatewayT1",
            "ciscoCatalyst6000T1VoIPGatewayT1",
            args,
        )
        return self.client.addCiscoCatalyst6000T1VoIPGatewayT1(
            ciscoCatalyst6000T1VoIPGatewayT1=gw
        )

    def get_cisco_catalyst6000_t1_voip_gateway_t1(self, name="", uuid=""):
        """
        Get a Cisco Catalyst 6000 T1 VoIP gateway (T1).

        :param name: device name (or uuid)
        :param uuid: device uuid (or name)
        :return: ciscoCatalyst6000T1VoIPGatewayT1 dictionary
        """
        return self.client.getCiscoCatalyst6000T1VoIPGatewayT1(
            **self._identify(name=name, uuid=uuid)
        )["return"]["ciscoCatalyst6000T1VoIPGatewayT1"]

    def get_cisco_catalyst6000_t1_voip_gateway_t1s(
        self, tagfilter={"name": "", "description": ""}
    ):
        """
        List Cisco Catalyst 6000 T1 VoIP gateways (T1).

        :param tagfilter: AXL returned tags to include
        :return: list of ciscoCatalyst6000T1VoIPGatewayT1 dicts, empty on no results
        """
        result = self.client.listCiscoCatalyst6000T1VoIPGatewayT1(
            {"name": "%"}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("ciscoCatalyst6000T1VoIPGatewayT1", []) or []

    def update_cisco_catalyst6000_t1_voip_gateway_t1(self, **args):
        """
        Update a Cisco Catalyst 6000 T1 VoIP gateway (T1).

        :param name: device name (or uuid)
        :param uuid: device uuid (or name)
        :return: result dictionary
        """
        return self.client.updateCiscoCatalyst6000T1VoIPGatewayT1(**args)

    def remove_cisco_catalyst6000_t1_voip_gateway_t1(self, name="", uuid=""):
        """
        Remove a Cisco Catalyst 6000 T1 VoIP gateway (T1).

        :param name: device name (or uuid)
        :param uuid: device uuid (or name)
        :return: result dictionary
        """
        return self.client.removeCiscoCatalyst6000T1VoIPGatewayT1(
            **self._identify(name=name, uuid=uuid)
        )

    def apply_cisco_catalyst6000_t1_voip_gateway_t1(self, name="", uuid=""):
        """
        Apply Cisco Catalyst 6000 T1 VoIP gateway (T1) configuration.

        :param name: device name (or uuid)
        :param uuid: device uuid (or name)
        :return: result dictionary
        """
        return self.client.applyCiscoCatalyst6000T1VoIPGatewayT1(
            **self._identify(name=name, uuid=uuid)
        )

    def reset_cisco_catalyst6000_t1_voip_gateway_t1(self, name="", uuid=""):
        """
        Reset a Cisco Catalyst 6000 T1 VoIP gateway (T1).

        :param name: device name (or uuid)
        :param uuid: device uuid (or name)
        :return: result dictionary
        """
        return self.client.resetCiscoCatalyst6000T1VoIPGatewayT1(
            **self._identify(name=name, uuid=uuid)
        )

    def restart_cisco_catalyst6000_t1_voip_gateway_t1(self, name="", uuid=""):
        """
        Restart a Cisco Catalyst 6000 T1 VoIP gateway (T1).

        :param name: device name (or uuid)
        :param uuid: device uuid (or name)
        :return: result dictionary
        """
        return self.client.restartCiscoCatalyst6000T1VoIPGatewayT1(
            **self._identify(name=name, uuid=uuid)
        )

    # ------------------------------------------------------------------ #
    # Gatekeeper                                                           #
    # ------------------------------------------------------------------ #

    def add_gatekeeper(self, **args):
        """
        Add a gatekeeper.

        :param name: gatekeeper name — required
        :param description: description
        :param rrqTimeToLive: RRQ time-to-live in seconds
        :return: result dictionary (uuid)
        """
        gk = self._build_object("addGatekeeper", "gatekeeper", args)
        return self.client.addGatekeeper(gatekeeper=gk)

    def get_gatekeeper(self, name="", uuid=""):
        """
        Get a gatekeeper.

        :param name: gatekeeper name (or uuid)
        :param uuid: gatekeeper uuid (or name)
        :return: gatekeeper dictionary
        """
        return self.client.getGatekeeper(
            **self._identify(name=name, uuid=uuid)
        )["return"]["gatekeeper"]

    def get_gatekeepers(self, tagfilter={"name": "", "description": ""}):
        """
        List gatekeepers.

        :param tagfilter: AXL returned tags to include
        :return: list of gatekeeper dicts, empty on no results
        """
        result = self.client.listGatekeeper(
            {"name": "%"}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("gatekeeper", []) or []

    def update_gatekeeper(self, **args):
        """
        Update a gatekeeper.

        :param name: gatekeeper name (or uuid)
        :param uuid: gatekeeper uuid (or name)
        :return: result dictionary
        """
        return self.client.updateGatekeeper(**args)

    def remove_gatekeeper(self, name="", uuid=""):
        """
        Remove a gatekeeper.

        :param name: gatekeeper name (or uuid)
        :param uuid: gatekeeper uuid (or name)
        :return: result dictionary
        """
        return self.client.removeGatekeeper(**self._identify(name=name, uuid=uuid))

    def apply_gatekeeper(self, name="", uuid=""):
        """
        Apply gatekeeper configuration.

        :param name: gatekeeper name (or uuid)
        :param uuid: gatekeeper uuid (or name)
        :return: result dictionary
        """
        return self.client.applyGatekeeper(**self._identify(name=name, uuid=uuid))

    def reset_gatekeeper(self, name="", uuid=""):
        """
        Reset a gatekeeper.

        :param name: gatekeeper name (or uuid)
        :param uuid: gatekeeper uuid (or name)
        :return: result dictionary
        """
        return self.client.resetGatekeeper(**self._identify(name=name, uuid=uuid))

    def restart_gatekeeper(self, name="", uuid=""):
        """
        Restart a gatekeeper.

        :param name: gatekeeper name (or uuid)
        :param uuid: gatekeeper uuid (or name)
        :return: result dictionary
        """
        return self.client.restartGatekeeper(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------ #
    # GatewayEndpointDigitalAccessBri                                     #
    # ------------------------------------------------------------------ #

    def add_gateway_endpoint_digital_access_bri(self, **args):
        """
        Add a gateway digital-access BRI endpoint.

        :param domainName: parent gateway domain name — required (or gatewayUuid)
        :param gatewayUuid: parent gateway uuid — required (or domainName)
        :param unit: slot index on the gateway
        :param subunit: subunit index
        :param index: port index
        :return: result dictionary (uuid)
        """
        ep = self._build_object(
            "addGatewayEndpointDigitalAccessBri",
            "gatewayEndpointDigitalAccessBri",
            args,
        )
        return self.client.addGatewayEndpointDigitalAccessBri(
            gatewayEndpointDigitalAccessBri=ep
        )

    def get_gateway_endpoint_digital_access_bri(self, name="", uuid=""):
        """
        Get a gateway digital-access BRI endpoint.

        :param name: endpoint name (or uuid)
        :param uuid: endpoint uuid (or name)
        :return: gatewayEndpointDigitalAccessBri dictionary
        """
        return self.client.getGatewayEndpointDigitalAccessBri(
            **self._identify(name=name, uuid=uuid)
        )["return"]["gatewayEndpointDigitalAccessBri"]

    def update_gateway_endpoint_digital_access_bri(self, **args):
        """
        Update a gateway digital-access BRI endpoint.

        :param name: endpoint name (or uuid)
        :param uuid: endpoint uuid (or name)
        :return: result dictionary
        """
        return self.client.updateGatewayEndpointDigitalAccessBri(**args)

    def remove_gateway_endpoint_digital_access_bri(self, name="", uuid=""):
        """
        Remove a gateway digital-access BRI endpoint.

        :param name: endpoint name (or uuid)
        :param uuid: endpoint uuid (or name)
        :return: result dictionary
        """
        return self.client.removeGatewayEndpointDigitalAccessBri(
            **self._identify(name=name, uuid=uuid)
        )

    # ------------------------------------------------------------------ #
    # H323Phone                                                            #
    # ------------------------------------------------------------------ #

    def add_h323_phone(self, **args):
        """
        Add an H.323 phone.

        :param name: device name — required
        :param description: description
        :param product: device product — required
        :param devicePoolName: device pool — required
        :return: result dictionary (uuid)
        """
        phone = self._build_object("addH323Phone", "h323Phone", args)
        return self.client.addH323Phone(h323Phone=phone)

    def get_h323_phone(self, name="", uuid=""):
        """
        Get an H.323 phone.

        :param name: device name (or uuid)
        :param uuid: device uuid (or name)
        :return: h323Phone dictionary
        """
        return self.client.getH323Phone(
            **self._identify(name=name, uuid=uuid)
        )["return"]["h323Phone"]

    def get_h323_phones(self, tagfilter={"name": "", "description": ""}):
        """
        List H.323 phones.

        :param tagfilter: AXL returned tags to include
        :return: list of h323Phone dicts, empty on no results
        """
        result = self.client.listH323Phone(
            {"name": "%"}, returnedTags=tagfilter
        )["return"]
        if result is None:
            return []
        return result.get("h323Phone", []) or []

    def update_h323_phone(self, **args):
        """
        Update an H.323 phone.

        :param name: device name (or uuid)
        :param uuid: device uuid (or name)
        :return: result dictionary
        """
        return self.client.updateH323Phone(**args)

    def remove_h323_phone(self, name="", uuid=""):
        """
        Remove an H.323 phone.

        :param name: device name (or uuid)
        :param uuid: device uuid (or name)
        :return: result dictionary
        """
        return self.client.removeH323Phone(**self._identify(name=name, uuid=uuid))

    def apply_h323_phone(self, name="", uuid=""):
        """
        Apply H.323 phone configuration.

        :param name: device name (or uuid)
        :param uuid: device uuid (or name)
        :return: result dictionary
        """
        return self.client.applyH323Phone(**self._identify(name=name, uuid=uuid))

    def reset_h323_phone(self, name="", uuid=""):
        """
        Reset an H.323 phone.

        :param name: device name (or uuid)
        :param uuid: device uuid (or name)
        :return: result dictionary
        """
        return self.client.resetH323Phone(**self._identify(name=name, uuid=uuid))

    def restart_h323_phone(self, name="", uuid=""):
        """
        Restart an H.323 phone.

        :param name: device name (or uuid)
        :param uuid: device uuid (or name)
        :return: result dictionary
        """
        return self.client.restartH323Phone(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------ #
    # Vg224                                                                #
    # ------------------------------------------------------------------ #

    def add_vg224(self, **args):
        """
        Add a VG224 gateway.

        :param domainName: gateway domain name — required
        :param description: description
        :param product: gateway product, e.g. 'Cisco VG224' — required
        :param protocol: gateway protocol — required
        :param callManagerGroupName: associated CM group
        :return: result dictionary (uuid)
        """
        gw = self._build_object("addVg224", "vg224", args)
        return self.client.addVg224(vg224=gw)

    def get_vg224(self, domainName="", uuid=""):
        """
        Get a VG224 gateway.

        :param domainName: gateway domain name (or uuid)
        :param uuid: gateway uuid (or domainName)
        :return: vg224 dictionary
        """
        return self.client.getVg224(
            **self._identify_domain(domainName=domainName, uuid=uuid)
        )["return"]["vg224"]

    def update_vg224(self, **args):
        """
        Update a VG224 gateway.

        :param domainName: gateway domain name (or uuid)
        :param uuid: gateway uuid (or domainName)
        :return: result dictionary
        """
        return self.client.updateVg224(**args)

    def remove_vg224(self, domainName="", uuid=""):
        """
        Remove a VG224 gateway.

        :param domainName: gateway domain name (or uuid)
        :param uuid: gateway uuid (or domainName)
        :return: result dictionary
        """
        return self.client.removeVg224(
            **self._identify_domain(domainName=domainName, uuid=uuid)
        )

    def reset_vg224(self, domainName="", uuid=""):
        """
        Reset a VG224 gateway.

        :param domainName: gateway domain name (or uuid)
        :param uuid: gateway uuid (or domainName)
        :return: result dictionary
        """
        return self.client.resetVg224(
            **self._identify_domain(domainName=domainName, uuid=uuid)
        )

    def restart_vg224(self, domainName="", uuid=""):
        """
        Restart a VG224 gateway.

        :param domainName: gateway domain name (or uuid)
        :param uuid: gateway uuid (or domainName)
        :return: result dictionary
        """
        return self.client.restartVg224(
            **self._identify_domain(domainName=domainName, uuid=uuid)
        )
