"""Apply / reset / restart wrappers and activation-code objects.

Mixin class providing AXL lifecycle operations for:
- CtiRoutePoint, Line, HuntList, RouteList, RoutePartition
- H323Gateway, SipTrunk (restart only), Srst
- ConferenceBridge, Mtp, Region, Transcoder
- CallManagerGroup, DevicePool

New object surfaces (no get/update in AXL schema):
- PhoneActivationCode  (add, list, remove)
- UnassignedDevice     (list only)
"""


class LifecycleMixin:
    """Apply / reset / restart wrappers and activation-code objects."""

    # ------------------------------------------------------------------ #
    # CtiRoutePoint lifecycle                                              #
    # ------------------------------------------------------------------ #

    def apply_cti_route_point(self, name="", uuid=""):
        """
        Apply a CTI Route Point
        :param name: CTI route point name (or use uuid)
        :param uuid: CTI route point uuid (or use name)
        :return: result dict
        """
        return self.client.applyCtiRoutePoint(**self._identify(name=name, uuid=uuid))

    def reset_cti_route_point(self, name="", uuid=""):
        """
        Reset a CTI Route Point
        :param name: CTI route point name (or use uuid)
        :param uuid: CTI route point uuid (or use name)
        :return: result dict
        """
        return self.client.resetCtiRoutePoint(**self._identify(name=name, uuid=uuid))

    def restart_cti_route_point(self, name="", uuid=""):
        """
        Restart a CTI Route Point
        :param name: CTI route point name (or use uuid)
        :param uuid: CTI route point uuid (or use name)
        :return: result dict
        """
        return self.client.restartCtiRoutePoint(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------ #
    # Line lifecycle  (ApplyLineReq/ResetLineReq/RestartLineReq use        #
    # pattern+routePartitionName OR uuid — not name)                       #
    # ------------------------------------------------------------------ #

    def _identify_line(self, pattern="", partition="", uuid=""):
        """
        Build the line identifier AXL expects: uuid OR pattern[+routePartitionName].
        Exactly one of (uuid) or (pattern) must be supplied.
        :param pattern: directory number pattern
        :param partition: route partition name (optional when pattern given)
        :param uuid: line uuid
        :return: kwargs dict suitable for applyLine / resetLine / restartLine
        """
        if bool(uuid) == bool(pattern):
            raise ValueError("Provide exactly one of pattern or uuid")
        if uuid:
            return {"uuid": uuid}
        result = {"pattern": pattern}
        if partition:
            result["routePartitionName"] = partition
        return result

    def apply_line(self, pattern="", partition="", uuid=""):
        """
        Apply a Line (directory number)
        :param pattern: directory number pattern (or use uuid)
        :param partition: route partition name (optional with pattern)
        :param uuid: line uuid (or use pattern)
        :return: result dict
        """
        return self.client.applyLine(**self._identify_line(pattern=pattern, partition=partition, uuid=uuid))

    def reset_line(self, pattern="", partition="", uuid=""):
        """
        Reset a Line (directory number)
        :param pattern: directory number pattern (or use uuid)
        :param partition: route partition name (optional with pattern)
        :param uuid: line uuid (or use pattern)
        :return: result dict
        """
        return self.client.resetLine(**self._identify_line(pattern=pattern, partition=partition, uuid=uuid))

    def restart_line(self, pattern="", partition="", uuid=""):
        """
        Restart a Line (directory number)
        :param pattern: directory number pattern (or use uuid)
        :param partition: route partition name (optional with pattern)
        :param uuid: line uuid (or use pattern)
        :return: result dict
        """
        return self.client.restartLine(**self._identify_line(pattern=pattern, partition=partition, uuid=uuid))

    # ------------------------------------------------------------------ #
    # HuntList lifecycle                                                   #
    # ------------------------------------------------------------------ #

    def apply_hunt_list(self, name="", uuid=""):
        """
        Apply a Hunt List
        :param name: hunt list name (or use uuid)
        :param uuid: hunt list uuid (or use name)
        :return: result dict
        """
        return self.client.applyHuntList(**self._identify(name=name, uuid=uuid))

    def reset_hunt_list(self, name="", uuid=""):
        """
        Reset a Hunt List
        :param name: hunt list name (or use uuid)
        :param uuid: hunt list uuid (or use name)
        :return: result dict
        """
        return self.client.resetHuntList(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------ #
    # RouteList lifecycle                                                  #
    # ------------------------------------------------------------------ #

    def apply_route_list(self, name="", uuid=""):
        """
        Apply a Route List
        :param name: route list name (or use uuid)
        :param uuid: route list uuid (or use name)
        :return: result dict
        """
        return self.client.applyRouteList(**self._identify(name=name, uuid=uuid))

    def reset_route_list(self, name="", uuid=""):
        """
        Reset a Route List
        :param name: route list name (or use uuid)
        :param uuid: route list uuid (or use name)
        :return: result dict
        """
        return self.client.resetRouteList(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------ #
    # RoutePartition lifecycle                                             #
    # ------------------------------------------------------------------ #

    def apply_route_partition(self, name="", uuid=""):
        """
        Apply a Route Partition
        :param name: partition name (or use uuid)
        :param uuid: partition uuid (or use name)
        :return: result dict
        """
        return self.client.applyRoutePartition(**self._identify(name=name, uuid=uuid))

    def restart_route_partition(self, name="", uuid=""):
        """
        Restart a Route Partition
        :param name: partition name (or use uuid)
        :param uuid: partition uuid (or use name)
        :return: result dict
        """
        return self.client.restartRoutePartition(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------ #
    # H323Gateway lifecycle                                                #
    # ------------------------------------------------------------------ #

    def apply_h323_gateway(self, name="", uuid=""):
        """
        Apply an H.323 Gateway
        :param name: gateway name/IP (or use uuid)
        :param uuid: gateway uuid (or use name)
        :return: result dict
        """
        return self.client.applyH323Gateway(**self._identify(name=name, uuid=uuid))

    def reset_h323_gateway(self, name="", uuid=""):
        """
        Reset an H.323 Gateway
        :param name: gateway name/IP (or use uuid)
        :param uuid: gateway uuid (or use name)
        :return: result dict
        """
        return self.client.resetH323Gateway(**self._identify(name=name, uuid=uuid))

    def restart_h323_gateway(self, name="", uuid=""):
        """
        Restart an H.323 Gateway
        :param name: gateway name/IP (or use uuid)
        :param uuid: gateway uuid (or use name)
        :return: result dict
        """
        return self.client.restartH323Gateway(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------ #
    # SipTrunk lifecycle (reset_sip_trunk is in axl.py; restart only here)#
    # ------------------------------------------------------------------ #

    def restart_sip_trunk(self, name="", uuid=""):
        """
        Restart a SIP Trunk
        :param name: trunk name (or use uuid)
        :param uuid: trunk uuid (or use name)
        :return: result dict
        """
        return self.client.restartSipTrunk(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------ #
    # Srst lifecycle                                                       #
    # ------------------------------------------------------------------ #

    def apply_srst(self, name="", uuid=""):
        """
        Apply an SRST reference
        :param name: SRST name (or use uuid)
        :param uuid: SRST uuid (or use name)
        :return: result dict
        """
        return self.client.applySrst(**self._identify(name=name, uuid=uuid))

    def reset_srst(self, name="", uuid=""):
        """
        Reset an SRST reference
        :param name: SRST name (or use uuid)
        :param uuid: SRST uuid (or use name)
        :return: result dict
        """
        return self.client.resetSrst(**self._identify(name=name, uuid=uuid))

    def restart_srst(self, name="", uuid=""):
        """
        Restart an SRST reference
        :param name: SRST name (or use uuid)
        :param uuid: SRST uuid (or use name)
        :return: result dict
        """
        return self.client.restartSrst(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------ #
    # ConferenceBridge lifecycle                                           #
    # ------------------------------------------------------------------ #

    def apply_conference_bridge(self, name="", uuid=""):
        """
        Apply a Conference Bridge
        :param name: conference bridge name (or use uuid)
        :param uuid: conference bridge uuid (or use name)
        :return: result dict
        """
        return self.client.applyConferenceBridge(**self._identify(name=name, uuid=uuid))

    def reset_conference_bridge(self, name="", uuid=""):
        """
        Reset a Conference Bridge
        :param name: conference bridge name (or use uuid)
        :param uuid: conference bridge uuid (or use name)
        :return: result dict
        """
        return self.client.resetConferenceBridge(**self._identify(name=name, uuid=uuid))

    def restart_conference_bridge(self, name="", uuid=""):
        """
        Restart a Conference Bridge
        :param name: conference bridge name (or use uuid)
        :param uuid: conference bridge uuid (or use name)
        :return: result dict
        """
        return self.client.restartConferenceBridge(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------ #
    # Mtp lifecycle                                                        #
    # ------------------------------------------------------------------ #

    def apply_mtp(self, name="", uuid=""):
        """
        Apply an MTP resource
        :param name: MTP name (or use uuid)
        :param uuid: MTP uuid (or use name)
        :return: result dict
        """
        return self.client.applyMtp(**self._identify(name=name, uuid=uuid))

    def reset_mtp(self, name="", uuid=""):
        """
        Reset an MTP resource
        :param name: MTP name (or use uuid)
        :param uuid: MTP uuid (or use name)
        :return: result dict
        """
        return self.client.resetMtp(**self._identify(name=name, uuid=uuid))

    def restart_mtp(self, name="", uuid=""):
        """
        Restart an MTP resource
        :param name: MTP name (or use uuid)
        :param uuid: MTP uuid (or use name)
        :return: result dict
        """
        return self.client.restartMtp(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------ #
    # Region lifecycle                                                     #
    # ------------------------------------------------------------------ #

    def apply_region(self, name="", uuid=""):
        """
        Apply a Region
        :param name: region name (or use uuid)
        :param uuid: region uuid (or use name)
        :return: result dict
        """
        return self.client.applyRegion(**self._identify(name=name, uuid=uuid))

    def restart_region(self, name="", uuid=""):
        """
        Restart a Region
        :param name: region name (or use uuid)
        :param uuid: region uuid (or use name)
        :return: result dict
        """
        return self.client.restartRegion(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------ #
    # Transcoder lifecycle                                                 #
    # ------------------------------------------------------------------ #

    def apply_transcoder(self, name="", uuid=""):
        """
        Apply a Transcoder
        :param name: transcoder name (or use uuid)
        :param uuid: transcoder uuid (or use name)
        :return: result dict
        """
        return self.client.applyTranscoder(**self._identify(name=name, uuid=uuid))

    def reset_transcoder(self, name="", uuid=""):
        """
        Reset a Transcoder
        :param name: transcoder name (or use uuid)
        :param uuid: transcoder uuid (or use name)
        :return: result dict
        """
        return self.client.resetTranscoder(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------ #
    # CallManagerGroup lifecycle                                           #
    # ------------------------------------------------------------------ #

    def apply_call_manager_group(self, name="", uuid=""):
        """
        Apply a Call Manager Group
        :param name: call manager group name (or use uuid)
        :param uuid: call manager group uuid (or use name)
        :return: result dict
        """
        return self.client.applyCallManagerGroup(**self._identify(name=name, uuid=uuid))

    def reset_call_manager_group(self, name="", uuid=""):
        """
        Reset a Call Manager Group
        :param name: call manager group name (or use uuid)
        :param uuid: call manager group uuid (or use name)
        :return: result dict
        """
        return self.client.resetCallManagerGroup(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------ #
    # DevicePool lifecycle                                                 #
    # ------------------------------------------------------------------ #

    def apply_device_pool(self, name="", uuid=""):
        """
        Apply a Device Pool
        :param name: device pool name (or use uuid)
        :param uuid: device pool uuid (or use name)
        :return: result dict
        """
        return self.client.applyDevicePool(**self._identify(name=name, uuid=uuid))

    def reset_device_pool(self, name="", uuid=""):
        """
        Reset a Device Pool
        :param name: device pool name (or use uuid)
        :param uuid: device pool uuid (or use name)
        :return: result dict
        """
        return self.client.resetDevicePool(**self._identify(name=name, uuid=uuid))

    def restart_device_pool(self, name="", uuid=""):
        """
        Restart a Device Pool
        :param name: device pool name (or use uuid)
        :param uuid: device pool uuid (or use name)
        :return: result dict
        """
        return self.client.restartDevicePool(**self._identify(name=name, uuid=uuid))

    # ------------------------------------------------------------------ #
    # PhoneActivationCode  (add / list / remove — no get/update in schema)#
    # Search criteria: phoneName, userId (not name).                       #
    # Remove by: activationCode or uuid.                                   #
    # ------------------------------------------------------------------ #

    def add_phone_activation_code(self, **args):
        """
        Add a Phone Activation Code
        :param args: AXL phoneActivationCode fields
        :return: result dict
        """
        return self.client.addPhoneActivationCode(
            self._build_object("addPhoneActivationCode", "phoneActivationCode", args)
        )

    def get_phone_activation_codes(self, phone_name="", user_id="", tagfilter=None):
        """
        List Phone Activation Codes
        Search criteria are phoneName and/or userId (the XSD uses these names, not 'name').
        At least one must be supplied; pass empty strings to wildcard with '%'.
        :param phone_name: device name filter (supports % wildcard), default '%'
        :param user_id: user ID filter (supports % wildcard)
        :param tagfilter: returned tags dict, default {'phoneName': ''}
        :return: list of phoneActivationCode dicts, empty when nothing matches
        """
        if tagfilter is None:
            tagfilter = {"phoneName": ""}
        search = {}
        if phone_name:
            search["phoneName"] = phone_name
        if user_id:
            search["userId"] = user_id
        # At least one search element is required by the schema
        if not search:
            search["phoneName"] = "%"
        result = self.client.listPhoneActivationCode(
            search, returnedTags=tagfilter
        )["return"]
        return (result or {}).get("phoneActivationCode") or []

    def delete_phone_activation_code(self, activation_code="", uuid=""):
        """
        Remove a Phone Activation Code by activation code string or uuid.
        (The schema uses activationCode, not name.)
        :param activation_code: the activation code string (or use uuid)
        :param uuid: activation code uuid (or use activation_code)
        :return: result dict
        """
        if bool(activation_code) == bool(uuid):
            raise ValueError("Provide exactly one of activation_code or uuid")
        if activation_code:
            return self.client.removePhoneActivationCode(activationCode=activation_code)
        return self.client.removePhoneActivationCode(uuid=uuid)

    # ------------------------------------------------------------------ #
    # UnassignedDevice  (list only)                                        #
    # Search criteria: name, description.                                  #
    # ------------------------------------------------------------------ #

    def get_unassigned_devices(self, name="", description="", tagfilter=None):
        """
        List Unassigned Devices
        :param name: device name filter (supports % wildcard), default '%'
        :param description: description filter (supports % wildcard)
        :param tagfilter: returned tags dict, default {'name': ''}
        :return: list of unassignedDevice dicts, empty when nothing matches
        """
        if tagfilter is None:
            tagfilter = {"name": ""}
        search = {}
        if name:
            search["name"] = name
        if description:
            search["description"] = description
        if not search:
            search["name"] = "%"
        result = self.client.listUnassignedDevice(
            search, returnedTags=tagfilter
        )["return"]
        return (result or {}).get("unassignedDevice") or []
