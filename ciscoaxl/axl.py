"""
Class to interface with cisco ucm axl api.
Author: Jeff Levensailor
Version: 0.1
Dependencies:
 - zeep: https://python-zeep.readthedocs.io/en/master/

Links:
 - https://developer.cisco.com/site/axl/
"""

import sys
from pathlib import Path
import os
import json
from requests import Session
from requests.exceptions import SSLError, ConnectionError
import re
import urllib3
from lxml import etree
from zeep import Client, Settings, Plugin
from zeep.transports import Transport
from zeep.cache import SqliteCache
from zeep.plugins import HistoryPlugin
from zeep.exceptions import Fault

from ciscoaxl.aliases import AliasingService, apply_aliases, fill_required, translate
from ciscoaxl.templates import TemplatesMixin
from ciscoaxl.users import UsersMixin
from ciscoaxl.presence import PresenceMixin
from ciscoaxl.security import SecurityMixin
from ciscoaxl.lifecycle import LifecycleMixin
from ciscoaxl.dialplan import DialPlanMixin
from ciscoaxl.gateways import GatewaysMixin
from ciscoaxl.media import MediaMixin
from ciscoaxl.system import SystemMixin
from ciscoaxl.ils import IlsMixin
from ciscoaxl.ime import ImeMixin
from ciscoaxl.ccd_saf import CcdSafMixin
from ciscoaxl.network import NetworkMixin
from ciscoaxl.niche import NicheMixin

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@apply_aliases
class axl(
    TemplatesMixin,
    UsersMixin,
    PresenceMixin,
    SecurityMixin,
    LifecycleMixin,
    DialPlanMixin,
    GatewaysMixin,
    MediaMixin,
    SystemMixin,
    IlsMixin,
    ImeMixin,
    CcdSafMixin,
    NetworkMixin,
    NicheMixin,
):
    """
    The AXL class sets up the connection to the call manager with methods for configuring UCM.
    Tested with environment of;
    Python 3.6
    """

    def __init__(self, username, password, cucm, cucm_version, cucm_port=8443, strict_ssl=False):
        """
        :param username: axl username
        :param password: axl password
        :param cucm: UCM IP address or hostname
        :param cucm_version: AXL schema version folder: 8.5, 9.1, 10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 14.0, 15.0
        :param cucm_port: UCM TCP port, default 8443
        :param strict_ssl: raise on certificate errors instead of retrying unverified, default False

        AXL faults raise zeep.exceptions.Fault. Friendly argument names (partition, device_pool, css...)
        are converted to AXL element names before each request; AXL names also work.

        example usage:
        >>> from ciscoaxl import axl
        >>> ucm = axl('axl_user', 'axl_pass', '192.168.200.10', '15.0')
        """

        cwd = os.path.dirname(os.path.abspath(__file__))
        if os.name == "posix":
            wsdl = Path(f"{cwd}/schema/{cucm_version}/AXLAPI.wsdl").as_uri()
        else:
            wsdl = str(Path(f"{cwd}/schema/{cucm_version}/AXLAPI.wsdl").absolute())
        session = Session()
        session.auth = (username, password)

        # validate session before assigning to Transport
        url = f"https://{cucm}:{cucm_port}/axl/"
        try:
            ret_code = session.get(url, stream=True, timeout=10).status_code
        except SSLError:
            if strict_ssl:
                raise

            # retry with verify set False
            session.close()
            session = Session()
            session.auth = (username, password)
            session.verify = False
            ret_code = session.get(url, stream=True, timeout=10).status_code
        except ConnectionError:
            raise Exception(f"{url} cannot be found, please try again") from None
        if ret_code == 401:
            raise Exception(
                "[401 Unauthorized]: Please check your username and password"
            )
        elif ret_code == 403:
            raise Exception(
                f"[403 Forbidden]: Please ensure the user '{username}' has AXL access set up"
            )
        elif ret_code == 404:
            raise Exception(
                f"[404 Not Found]: AXL not found, please check your URL ({url})"
            )

        settings = Settings(
            strict=False, xml_huge_tree=True, xsd_ignore_sequence_order=True
        )
        transport = Transport(session=session, timeout=10, cache=SqliteCache())
        axl_client = Client(wsdl, settings=settings, transport=transport)

        self._zeep = axl_client
        self.username = username
        self.password = password
        self.wsdl = wsdl
        self.cucm = cucm
        self.cucm_version = cucm_version
        self.UUID_PATTERN = re.compile(
            r"^[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$", re.IGNORECASE
        )
        service = axl_client.create_service(
            "{http://www.cisco.com/AXLAPIService/}AXLAPIBinding",
            f"https://{cucm}:{cucm_port}/axl/",
        )
        self.client = AliasingService(axl_client, service)

    def _schema_fields(self, operation, wrapper=None):
        """
        Element names accepted by an AXL operation in the loaded schema version
        :param operation: AXL operation name, e.g. 'addPhone'
        :param wrapper: optional wrapper element to descend into, e.g. 'phone'
        :return: set of element names
        """
        request_type = self.client._operations[operation].input.body.type
        if wrapper is not None:
            request_type = dict(request_type.elements)[wrapper].type
        return {name for name, _ in request_type.elements}

    def _build_object(self, operation, wrapper, args, defaults=None):
        """
        Build an add* request object: translate friendly names, apply method defaults,
        then fill remaining required elements from the schema defaults
        :param operation: AXL operation name, e.g. 'addSipTrunk'
        :param wrapper: wrapper element of the request, e.g. 'sipTrunk'
        :param args: caller arguments (friendly or AXL names)
        :param defaults: method defaults using AXL names, overridden by args
        :return: request object for the wrapper element
        """
        request_type = self.client._operations[operation].input.body.type
        object_type = dict(request_type.elements)[wrapper].type
        merged = {**(defaults or {}), **translate(args, object_type)}
        return fill_required(merged, object_type)

    def get_locations(
        self,
        tagfilter={
            "name": "",
            "withinAudioBandwidth": "",
            "withinVideoBandwidth": "",
            "withinImmersiveKbits": "",
        },
    ):
        """
        Get location details
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of dictionaries, empty when nothing matches
        

        Schema: `ListLocationReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        return self.client.listLocation({"name": "%"}, returnedTags=tagfilter,)[
            "return"
        ]["location"]

    def run_sql_query(self, query):
        """
        Execute a SQL query and return rows as dictionaries.
        :param query: SQL Query to execute
        :return: {'num_rows': int, 'query': str, 'rows': [{column: value}]} ('rows' only when num_rows > 0)
        :raises zeep.exceptions.Fault: on AXL error
        

        Schema: `ExecuteSQLQueryReq`: `sql`.
        """
        result = {"num_rows": 0, "query": query}

        sql_result = self.client.executeSQLQuery(sql=query)

        num_rows = 0
        result_rows = []

        if sql_result is not None and sql_result["return"] is not None:
            for row in sql_result["return"]["row"]:
                result_rows.append({})
                for column in row:
                    result_rows[num_rows][column.tag] = column.text
                num_rows += 1

        result["num_rows"] = num_rows
        if num_rows > 0:
            result["rows"] = result_rows

        return result

    def sql_query(self, query):
        """
        Execute SQL query
        :param query: SQL Query to execute
        :return: result dictionary
        

        Schema: `ExecuteSQLQueryReq`: `sql`.
        """
        return self.client.executeSQLQuery(query)["return"]

    def sql_update(self, query):
        """
        Execute SQL update
        :param query: SQL Update to execute
        :return: result dictionary
        

        Schema: `ExecuteSQLUpdateReq`: `sql`.
        """
        return self.client.executeSQLUpdate(query)["return"]

    def get_ldap_dir(
        self,
        tagfilter={
            "name": "",
            "ldapDn": "",
            "userSearchBase": "",
        },
    ):
        """
        Get LDAP Syncs
        :return: result dictionary
        

        Schema: `ListLdapDirectoryReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        return self.client.listLdapDirectory(
            {"name": "%"},
            returnedTags=tagfilter,
        )["return"]["ldapDirectory"]

    def do_ldap_sync(self, uuid="", name="", sync=True):
        """
        Start or cancel an LDAP directory sync
        :param uuid: LDAP directory uuid (or use name)
        :param name: LDAP directory name (or use uuid)
        :param sync: True starts a sync, False cancels a running sync
        :return: result dictionary
        

        Schema: `DoLdapSyncReq`: `sync`; one of `name`, or `uuid`.
        """
        identifier = self._identify(name=name, uuid=uuid)
        return self.client.doLdapSync(**identifier, sync=sync)

    def do_change_dnd_status(self, **args):
        """
        Change Do Not Disturb status for a user
        :param userID: user ID (or uuid)
        :param uuid: user uuid (or userID)
        :param status: DND on/off, boolean (AXL name: dndStatus) - required
        :return: result dictionary
        

        Schema: `DoChangeDNDStatusReq`: `dndStatus`; one of `userID`, or `uuid`.
        """
        return self.client.doChangeDNDStatus(**args)

    def do_device_login(self, **args):
        """
        Log a user into a device with Extension Mobility
        :param device: device name or uuid (AXL name: deviceName) - required
        :param loginDuration: login duration in seconds, 0 for no limit - required
        :param profileName: device profile name - required
        :param userId: user ID - required
        :return: result dictionary
        

        Schema: `DoDeviceLoginReq`: `deviceName` + `loginDuration` + `profileName` + `userId`.
        """
        return self.client.doDeviceLogin(**args)

    def do_device_logout(self, **args):
        """
        Log the Extension Mobility user out of a device
        :param device: device name or uuid (AXL name: deviceName) - required
        :return: result dictionary
        

        Schema: `DoDeviceLogoutReq`: `deviceName`.
        """
        return self.client.doDeviceLogout(**args)

    def do_device_reset(self, name="", uuid="", hard_reset=True):
        """
        Reset a device
        :param name: device name (or use uuid)
        :param uuid: device uuid (or use name)
        :param hard_reset: True for a hard reset (reboot), False for a restart
        :return: result dictionary
        

        Schema: `DoDeviceResetReq`: `deviceName`; one of `isHardReset`, or `deviceResetType`.
        """
        identifier = self._identify(name=name, uuid=uuid)
        device = identifier.get("name") or identifier.get("uuid")
        return self.client.doDeviceReset(deviceName=device, isHardReset=hard_reset)

    def reset_sip_trunk(self, name="", uuid=""):
        """
        Reset SIP Trunk
        :param name: trunk name (or use uuid)
        :param uuid: trunk uuid (or use name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.resetSipTrunk(**self._identify(name=name, uuid=uuid))

    @staticmethod
    def _lines(lines):
        """
        Convert line tuples into the AXL lines structure
        :param lines: list of tuples (pattern, partition[, display, displayAscii, label, e164Mask])
                      or AXL line dictionaries
        :return: {'line': [...]}
        """
        fields = ("display", "displayAscii", "label", "e164Mask")
        converted = []
        for index, line in enumerate(lines, start=1):
            if isinstance(line, dict):
                converted.append({"index": index, **line})
                continue
            entry = {
                "index": index,
                "dirn": {"pattern": line[0], "routePartitionName": line[1] or None},
            }
            entry.update(dict(zip(fields, line[2:])))
            converted.append(entry)
        return {"line": converted}

    def _with_lines(self, args):
        """
        Convert a 'lines' argument given as tuples into the AXL structure, leaving AXL dicts alone
        :param args: method keyword arguments
        :return: args with lines converted
        """
        if isinstance(args.get("lines"), list):
            args["lines"] = self._lines(args["lines"])
        return args

    def _identify(self, name="", uuid=""):
        """
        Build the name-or-uuid identifier AXL expects, requiring exactly one of them
        :param name: object name
        :param uuid: object uuid
        :return: {'name': name} or {'uuid': uuid}
        """
        if bool(name) == bool(uuid):
            raise ValueError("Provide exactly one of name or uuid")
        return {"name": name} if name else {"uuid": uuid}

    def get_location(self, **args):
        """
        Get location parameters
        :param name: location name
        :param uuid: location uuid
        :return: location dictionary
        

        Schema: `GetLocationReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getLocation(**args)["return"]["location"]

    def add_location(
        self,
        name,
        kbits=512,
        video_kbits=-1,
        within_audio_bw=512,
        within_video_bw=-1,
        within_immersive_kbits=-1,
        hub_location="Hub_None",
    ):
        """
        Add a location
        :param name: Name of the location to add
        :param kbits: audio bandwidth, used only by schemas without withinAudioBandwidth (8.5)
        :param video_kbits: video bandwidth, used only by schemas without withinAudioBandwidth (8.5)
        :param within_audio_bw: audio bandwidth within the location (9.1 and later)
        :param within_video_bw: video bandwidth within the location (9.1 and later)
        :param within_immersive_kbits: immersive bandwidth within the location (9.1 and later)
        :param hub_location: location linked to this one (9.1 and later)
        :return: result dictionary
        

        Schema: `location` -> `XLocation`: `name` + `withinAudioBandwidth` + `withinVideoBandwidth` + `withinImmersiveKbits` + `betweenLocations`; optional `relatedLocations`.
        """
        if "withinAudioBandwidth" not in self._schema_fields("addLocation", "location"):
            return self.client.addLocation(
                {"name": name, "kbits": kbits, "videoKbits": video_kbits}
            )
        return self.client.addLocation(
            {
                "name": name,
                "withinAudioBandwidth": within_audio_bw,
                "withinVideoBandwidth": within_video_bw,
                "withinImmersiveKbits": within_immersive_kbits,
                "betweenLocations": {
                    "betweenLocation": [
                        {
                            "locationName": hub_location,
                            "weight": 0,
                            "audioBandwidth": within_audio_bw,
                            "videoBandwidth": within_video_bw,
                            "immersiveBandwidth": within_immersive_kbits,
                        }
                    ]
                },
            }
        )

    def delete_location(self, **args):
        """
        Delete a location
        :param name: The name of the location to delete
        :param uuid: The uuid of the location to delete
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeLocation(**args)

    def update_location(self, **args):
        """
        Update a Location
        :param name: location name (or uuid)
        :param uuid: location uuid (or name)
        :param newName: new location name
        :param withinAudioBandwidth: audio bandwidth within the location
        :param withinVideoBandwidth: video bandwidth within the location
        :param withinImmersiveKbits: immersive bandwidth within the location
        :param betweenLocations: {'betweenLocation': [{'locationName', 'weight', 'audioBandwidth', 'videoBandwidth', 'immersiveBandwidth'}]}
        :return: result dictionary
        

        Schema: `UpdateLocationReq`: optional `newName`, `relatedLocations`, `withinAudioBandwidth`, `withinVideoBandwidth`, `withinImmersiveKbits`, `betweenLocations`.
        """
        return self.client.updateLocation(**args)

    def get_regions(self, tagfilter={"uuid": "", "name": ""}):
        """
        Get region details
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of dictionaries, empty when nothing matches
        

        Schema: `ListRegionReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        return self.client.listRegion({"name": "%"}, returnedTags=tagfilter)[
            "return"
        ]["region"]

    def get_region(self, **args):
        """
        Get region information
        :param name: Region name
        :return: result dictionary
        

        Schema: `GetRegionReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getRegion(**args)["return"]["region"]

    def add_region(self, name):
        """
        Add a region
        :param name: Name of the region to add
        :return: result dictionary
        

        Schema: `region` -> `XRegion`: `name`; optional `relatedRegions`, `defaultCodec`.
        """
        return self.client.addRegion({"name": name})

    def update_region(self, name, newName=None, moh_region=""):
        """
        Update region and assign region to all other regions.
        Overwrites every relationship of this region: 256 kbps within itself, 64 kbps to all others.
        :param name: region name
        :param newName: new region name, omitted when None
        :param moh_region: music on hold region name
        :return: result dictionary
        

        Schema: `UpdateRegionReq`: optional `newName`, `relatedRegions`.
        """
        # Get all Regions
        all_regions = self.client.listRegion({"name": "%"}, returnedTags={"name": ""})
        # Make list of region names
        region_names = [str(i["name"]) for i in all_regions["return"]["region"]]
        # Build list of dictionaries to add to region api call
        region_list = []

        for i in region_names:
            # Highest codec within a region
            if i == name:
                region_list.append(
                    {
                        "regionName": i,
                        "bandwidth": "256 kbps",
                        "videoBandwidth": "-1",
                        "immersiveVideoBandwidth": "-1",
                        "lossyNetwork": "Use System Default",
                    }
                )

            # Music on hold region name
            elif i == moh_region:
                region_list.append(
                    {
                        "regionName": i,
                        "bandwidth": "64 kbps",
                        "videoBandwidth": "-1",
                        "immersiveVideoBandwidth": "-1",
                        "lossyNetwork": "Use System Default",
                    }
                )

            # All else G.711
            else:
                region_list.append(
                    {
                        "regionName": i,
                        "bandwidth": "64 kbps",
                        "videoBandwidth": "-1",
                        "immersiveVideoBandwidth": "-1",
                        "lossyNetwork": "Use System Default",
                    }
                )
        update = {"name": name, "relatedRegions": {"relatedRegion": region_list}}
        if newName:
            update["newName"] = newName
        return self.client.updateRegion(**update)

    def delete_region(self, **args):
        """
        Delete a region
        :param name: The name of the region to delete
        :param uuid: The uuid of the region to delete
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeRegion(**args)

    def get_srsts(self, tagfilter={"uuid": ""}):
        """
        Get all SRST details
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of dictionaries, empty when nothing matches
        

        Schema: `ListSrstReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        return self.client.listSrst({"name": "%"}, returnedTags=tagfilter)[
            "return"
        ]["srst"]

    def get_srst(self, **args):
        """
        Get SRST information
        :param name: SRST name
        :return: result dictionary
        

        Schema: `GetSrstReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getSrst(**args)["return"]["srst"]

    def add_srst(self, name, ip_address, port=2000, sip_port=5060):
        """
        Add SRST
        :param name: SRST name
        :param ip_address: SRST ip address
        :param port: SRST port
        :param sip_port: SIP port
        :return: result dictionary
        

        Schema: `srst` -> `XSrst`: `name` + `port` + `ipAddress` + `SipPort`; optional `ipv6Address`, `SipNetwork`, `isSecure`.
        """
        return self.client.addSrst(
            {
                "name": name,
                "port": port,
                "ipAddress": ip_address,
                "SipPort": sip_port,
            }
        )

    def delete_srst(self, name="", uuid=""):
        """
        Delete a SRST
        :param name: The name of the SRST to delete (or uuid)
        :param uuid: The uuid of the SRST to delete (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeSrst(**self._identify(name=name, uuid=uuid))

    def update_srst(self, name="", newName=None, uuid="", **args):
        """
        Update a SRST
        :param name: The name of the SRST to update (or uuid)
        :param newName: The new name of the SRST, omitted when None
        :param uuid: The uuid of the SRST to update (or name)
        :param ipAddress: SRST IP address
        :param port: SRST port
        :param SipPort: SIP port
        :return: result dictionary
        

        Schema: `UpdateSrstReq`: optional `newName`, `port`, `ipAddress`, `ipv6Address`, `SipNetwork`, `SipPort` and 1 more.
        """
        if newName:
            args["newName"] = newName
        return self.client.updateSrst(**self._identify(name=name, uuid=uuid), **args)

    def get_device_pools(
        self,
        tagfilter={
            "name": "",
            "dateTimeSettingName": "",
            "callManagerGroupName": "",
            "mediaResourceListName": "",
            "regionName": "",
            "srstName": "",
            # 'localRouteGroup': [0],
        },
    ):
        """
        Get a dictionary of device pools
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: a list of dictionary's of device pools information
        

        Schema: `ListDevicePoolReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        return self.client.listDevicePool({"name": "%"}, returnedTags=tagfilter,)[
            "return"
        ]["devicePool"]

    def get_device_pool(self, **args):
        """
        Get device pool parameters
        :param name: device pool name
        :return: result dictionary
        

        Schema: `GetDevicePoolReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getDevicePool(**args)["return"]["devicePool"]

    def add_device_pool(
        self,
        name,
        date_time_group="CMLocal",
        region="Default",
        location="Hub_None",
        route_group="",
        media_resource_group_list="",
        srst="Disable",
        cm_group="Default",
        network_locale="",
        aar_group=None,
        local_route_group_name="Standard Local Route Group",
    ):

        """
        Add a device pool
        :param name: Device pool name
        :param date_time_group: Date time group name
        :param region: Region name
        :param location: Location name
        :param route_group: Route group used as the local route group, omitted when empty
        :param media_resource_group_list: Media resource group list name
        :param srst: SRST name
        :param cm_group: CM Group name
        :param network_locale: Network locale name
        :param aar_group: AAR group name, None for no AAR group
        :param local_route_group_name: Local route group slot that route_group fills
        :return: result dictionary
        

        Schema: `devicePool` -> `XDevicePool`: `name` + `dateTimeSettingName` + `callManagerGroupName` + `regionName` + `srstName` + `aarNeighborhoodName`; optional `autoSearchSpaceName`, `mediaResourceListName`, `networkLocale`, `connectionMonitorDuration`, `automatedAlternateRoutingCssName`, `locationName` and 44 more.
        """
        device_pool = {
            "name": name,
            "dateTimeSettingName": date_time_group,
            "regionName": region,
            "locationName": location,
            "mediaResourceListName": media_resource_group_list,
            "srstName": srst,
            "callManagerGroupName": cm_group,
            "networkLocale": network_locale,
            "aarNeighborhoodName": aar_group,
        }
        if route_group:
            device_pool["localRouteGroup"] = {
                "name": local_route_group_name,
                "value": route_group,
            }
        return self.client.addDevicePool(device_pool)

    def update_device_pool(self, **args):
        """
        Update a device pool
        :param name: device pool name (or uuid)
        :param uuid: device pool uuid (or name)
        :param newName: new device pool name
        :param media_resource_group_list: media resource group list name (AXL name: mediaResourceListName)
        :param date_time_group: date/time group name (AXL name: dateTimeSettingName)
        :param cm_group: Unified CM group name (AXL name: callManagerGroupName)
        :param region: region name (AXL name: regionName)
        :param location: location name (AXL name: locationName)
        :param network_locale: network locale (AXL name: networkLocale)
        :param srst: SRST name (AXL name: srstName)
        :param localRouteGroup: {'name': 'Standard Local Route Group', 'value': route group name}
        :param elinGroup: ELIN group name
        :return: result dictionary
        

        Schema: `UpdateDevicePoolReq`: optional `newName`, `autoSearchSpaceName`, `dateTimeSettingName`, `callManagerGroupName`, `mediaResourceListName`, `regionName` and 50 more.
        """
        return self.client.updateDevicePool(**args)

    def delete_device_pool(self, **args):
        """
        Delete a Device pool
        :param device_pool: The name of the Device pool to delete (or name / uuid)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeDevicePool(**args)

    def get_conference_bridges(
        self,
        tagfilter={
            "name": "",
            "description": "",
            "devicePoolName": "",
            "locationName": "",
        },
    ):
        """
        Get conference bridges
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: results dictionary
        

        Schema: `ListConferenceBridgeReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        return self.client.listConferenceBridge(
            {"name": "%"},
            returnedTags=tagfilter,
        )["return"]["conferenceBridge"]

    def get_conference_bridge(self, **args):
        """
        Get conference bridge parameters
        :param name: conference bridge name
        :return: result dictionary
        

        Schema: `GetConferenceBridgeReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getConferenceBridge(**args)["return"]["conferenceBridge"]

    def add_conference_bridge(
        self,
        name,
        description="",
        device_pool="Default",
        location="Hub_None",
        product="Cisco IOS Enhanced Conference Bridge",
        security_profile="Non Secure Conference Bridge",
    ):
        """
        Add a conference bridge
        :param conference_bridge: Conference bridge name
        :param description: Conference bridge description
        :param device_pool: Device pool name
        :param location: Location name
        :param product: Conference bridge type
        :param security_profile: Conference bridge security type
        :return: result dictionary
        

        Schema: `conferenceBridge` -> `XConferenceBridge`: `name` + `product` + `devicePoolName` + `locationName`; optional `description`, `commonDeviceConfigName`, `subUnit`, `loadInformation`, `vendorConfig`, `maximumCapacity` and 18 more.
        """
        return self.client.addConferenceBridge(
            {
                "name": name,
                "description": description,
                "devicePoolName": device_pool,
                "locationName": location,
                "product": product,
                "securityProfileName": security_profile,
            }
        )

    def update_conference_bridge(self, **args):
        """
        Update a conference bridge
        :param name: Conference bridge name (or uuid)
        :param uuid: Conference bridge uuid (or name)
        :param newName: New Conference bridge name
        :param description: Conference bridge description
        :param device_pool: Device pool name (AXL name: devicePoolName)
        :param location: Location name (AXL name: locationName)
        :param security_profile: Conference bridge security profile (AXL name: securityProfileName)
        :return: result dictionary
        

        Schema: `UpdateConferenceBridgeReq`: optional `newName`, `description`, `product`, `devicePoolName`, `commonDeviceConfigName`, `locationName` and 21 more.
        """
        return self.client.updateConferenceBridge(**args)

    def delete_conference_bridge(self, name="", uuid=""):
        """
        Delete a Conference bridge
        :param name: The name of the Conference bridge to delete (or uuid)
        :param uuid: The uuid of the Conference bridge to delete (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeConferenceBridge(**self._identify(name=name, uuid=uuid))

    def get_transcoders(
        self, tagfilter={"name": "", "description": "", "devicePoolName": ""}
    ):
        """
        Get transcoders
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: results dictionary
        

        Schema: `ListTranscoderReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        return self.client.listTranscoder({"name": "%"}, returnedTags=tagfilter,)[
            "return"
        ]["transcoder"]

    def get_transcoder(self, **args):
        """
        Get transcoder parameters
        :param name: transcoder name (or uuid)
        :param uuid: transcoder uuid (or name)
        :return: result dictionary
        

        Schema: `GetTranscoderReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getTranscoder(**args)["return"]["transcoder"]

    def add_transcoder(
        self,
        name,
        description="",
        device_pool="Default",
        product="Cisco IOS Enhanced Media Termination Point",
        load_information=None,
    ):
        """
        Add a transcoder
        :param name: Transcoder name
        :param description: Transcoder description
        :param device_pool: Transcoder device pool
        :param product: Transcoder product
        :param load_information: firmware load, None for the system default
        :return: result dictionary
        

        Schema: `transcoder` -> `XTranscoder`: `name` + `product` + `devicePoolName` + `loadInformation`; optional `description`, `subUnit`, `commonDeviceConfigName`, `vendorConfig`, `isTrustedRelayPoint`, `maximumCapacity`.
        """
        return self.client.addTranscoder(
            {
                "name": name,
                "description": description,
                "devicePoolName": device_pool,
                "product": product,
                "loadInformation": load_information,
            }
        )

    def update_transcoder(self, **args):
        """
        Update a transcoder (product can't be changed after creation)
        :param name: Transcoder name (or uuid)
        :param uuid: Transcoder uuid (or name)
        :param newName: New Transcoder name
        :param description: Transcoder description
        :param device_pool: Transcoder device pool (AXL name: devicePoolName)
        :return: result dictionary
        

        Schema: `UpdateTranscoderReq`: optional `newName`, `description`, `devicePoolName`, `commonDeviceConfigName`, `loadInformation`, `vendorConfig` and 2 more.
        """
        return self.client.updateTranscoder(**args)

    def delete_transcoder(self, name="", uuid=""):
        """
        Delete a Transcoder
        :param name: The name of the Transcoder to delete (or uuid)
        :param uuid: The uuid of the Transcoder to delete (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeTranscoder(**self._identify(name=name, uuid=uuid))

    def get_mtps(self, tagfilter={"name": "", "description": "", "devicePoolName": ""}):
        """
        Get mtps
        :param tagfilter: AXL returned tags to include, e.g. {'name': '', 'description': ''}
        :return: list of MTP dictionaries
        

        Schema: `ListMtpReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        return self.client.listMtp({"name": "%"}, returnedTags=tagfilter,)[
            "return"
        ]["mtp"]

    def get_mtp(self, **args):
        """
        Get mtp parameters
        :param name: MTP name (or uuid)
        :param uuid: MTP uuid (or name)
        :return: result dictionary
        

        Schema: `GetMtpReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getMtp(**args)["return"]["mtp"]

    def add_mtp(
        self,
        name,
        description="",
        device_pool="Default",
        mtpType="Cisco IOS Enhanced Media Termination Point",
    ):
        """
        Add an mtp
        :param name: MTP name
        :param description: MTP description
        :param device_pool: MTP device pool
        :param mtpType: MTP Type
        :return: result dictionary
        

        Schema: `mtp` -> `XMtp`: `mtpType` + `name` + `devicePoolName`; optional `description`, `trustedRelayPoint`.
        """
        return self.client.addMtp(
            {
                "name": name,
                "description": description,
                "devicePoolName": device_pool,
                "mtpType": mtpType,
            }
        )

    def update_mtp(self, **args):
        """
        Update an MTP (mtpType can't be changed after creation)
        :param name: MTP name (or uuid)
        :param uuid: MTP uuid (or name)
        :param newName: New MTP name
        :param description: MTP description
        :param device_pool: MTP device pool (AXL name: devicePoolName)
        :param trustedRelayPoint: boolean
        :return: result dictionary
        

        Schema: `UpdateMtpReq`: optional `newName`, `description`, `devicePoolName`, `trustedRelayPoint`.
        """
        return self.client.updateMtp(**args)

    def delete_mtp(self, name="", uuid=""):
        """
        Delete an MTP
        :param name: The name of the MTP to delete (or uuid)
        :param uuid: The uuid of the MTP to delete (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeMtp(**self._identify(name=name, uuid=uuid))

    def get_h323_gateways(
        self,
        tagfilter={
            "name": "",
            "description": "",
            "devicePoolName": "",
            "locationName": "",
            "sigDigits": "",
        },
    ):
        """
        Get H323 Gateways
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: results dictionary
        

        Schema: `ListH323GatewayReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        return self.client.listH323Gateway({"name": "%"}, returnedTags=tagfilter,)[
            "return"
        ]["h323Gateway"]

    def get_h323_gateway(self, **args):
        """
        Get H323 Gateway parameters
        :param name: H323 Gateway name
        :return: result dictionary
        

        Schema: `GetH323GatewayReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getH323Gateway(**args)["return"]["h323Gateway"]

    def add_h323_gateway(self, **args):
        """
        Add H323 gateway. Friendly names and AXL element names are both accepted;
        required elements not given use the schema defaults.
        :param h323_gateway: gateway name, usually the IP address (AXL name: name) - required
        :param description: description
        :param device_pool: device pool name (AXL name: devicePoolName) - required
        :param location: location name (AXL name: locationName), default Hub_None
        :param media_resource_group_list: Media resource group list name (AXL name: mediaResourceListName)
        :param prefix_dn: prefix DN (AXL name: prefixDn)
        :param sig_digits: Significant digits, 99 = ALL (AXL name: sigDigits)
        :param css: calling search space (AXL name: callingSearchSpaceName)
        :param aar_css: AAR calling search space (AXL name: automatedAlternateRoutingCssName)
        :param aar_neighborhood: AAR group (AXL name: aarNeighborhoodName)
        :param product: default 'H.323 Gateway'
        :param protocol: default 'H.225'
        :param protocol_side: default 'Network' (AXL name: protocolSide)
        :param pstn_access: boolean (AXL name: pstnAccess)
        :param redirect_in_num_ie: boolean (AXL name: redirectInboundNumberIe)
        :param redirect_out_num_ie: boolean (AXL name: redirectOutboundNumberIe)
        :param cld_party_ie_num_type: (AXL name: calledPartyIeNumberType)
        :param clng_party_ie_num_type: (AXL name: callingPartyIeNumberType)
        :param clng_party_nat_pre: (AXL name: callingPartyNationalPrefix)
        :param clng_party_inat_prefix: (AXL name: callingPartyInternationalPrefix)
        :param clng_party_unknown_prefix: (AXL name: callingPartyUnknownPrefix)
        :param clng_party_sub_prefix: (AXL name: callingPartySubscriberPrefix)
        :param clng_party_nat_strip_digits: (AXL name: callingPartyNationalStripDigits)
        :param clng_party_inat_strip_digits: (AXL name: callingPartyInternationalStripDigits)
        :param clng_party_unknown_strip_digits: (AXL name: callingPartyUnknownStripDigits)
        :param clng_party_sub_strip_digits: (AXL name: callingPartySubscriberStripDigits)
        :param clng_party_nat_trans_css: (AXL name: callingPartyNationalTransformationCssName)
        :param clng_party_inat_trans_css: (AXL name: callingPartyInternationalTransformationCssName)
        :param clng_party_unknown_trans_css: (AXL name: callingPartyUnknownTransformationCssName)
        :param clng_party_sub_trans_css: (AXL name: callingPartySubscriberTransformationCssName)
        :return: result dictionary
        

        Schema: `h323Gateway` -> `XH323Gateway`: `name` + `product` + `class` + `protocol` + `protocolSide` + `devicePoolName` + `locationName` + `tunneledProtocol` + `useTrustedRelayPoint` + `packetCaptureMode` + `callingPartySelection` + `callingLineIdPresentation` + `signalingPort` + `calledPartyIeNumberType` + `callingPartyIeNumberType` + `calledNumberingPlan` + `callingNumberingPlan`; optional `description`, `callingSearchSpaceName`, `commonDeviceConfigName`, `networkLocation`, `mediaResourceListName`, `automatedAlternateRoutingCssName` and 69 more.
        """
        gateway = self._build_object(
            "addH323Gateway",
            "h323Gateway",
            args,
            defaults={
                "product": "H.323 Gateway",
                "class": "Gateway",
                "protocol": "H.225",
                "protocolSide": "Network",
                "locationName": "Hub_None",
            },
        )
        return self.client.addH323Gateway(gateway)

    def update_h323_gateway(self, **args):
        """
        Update an H323 gateway. Accepts the same friendly names as add_h323_gateway.
        :param name: gateway name (or uuid)
        :param uuid: gateway uuid (or name)
        :param newName: new gateway name
        :return: result dictionary
        

        Schema: `UpdateH323GatewayReq`: optional `newName`, `description`, `callingSearchSpaceName`, `devicePoolName`, `commonDeviceConfigName`, `networkLocation` and 82 more.
        """
        return self.client.updateH323Gateway(**args)

    def delete_h323_gateway(self, name="", uuid=""):
        """
        Delete a H323 gateway
        :param name: The name of the H323 gateway to delete (or uuid)
        :param uuid: The uuid of the H323 gateway to delete (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeH323Gateway(**self._identify(name=name, uuid=uuid))

    def get_route_groups(self, tagfilter={"name": "", "distributionAlgorithm": ""}):
        """
        Get route groups
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of dictionaries, empty when nothing matches
        

        Schema: `ListRouteGroupReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        return self.client.listRouteGroup({"name": "%"}, returnedTags=tagfilter)[
            "return"
        ]["routeGroup"]

    def get_route_group(self, **args):
        """
        Get route group
        :param name: route group name
        :param uuid: route group uuid
        :return: result dictionary
        

        Schema: `GetRouteGroupReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getRouteGroup(**args)["return"]["routeGroup"]

    def add_route_group(self, name, distribution_algorithm="Top Down", members=[]):
        """
        Add a route group
        :param name: Route group name
        :param distribution_algorithm: Top Down, Circular, Longest Idle Time or Broadcast
        :param members: A list of existing gateway/trunk device names, in selection order
        :return: result dictionary
        

        Schema: `routeGroup` -> `XRouteGroup`: `distributionAlgorithm` + `members` + `name`.
        """
        req = {
            "name": name,
            "distributionAlgorithm": distribution_algorithm,
            "members": {
                "member": [
                    {"deviceName": device, "deviceSelectionOrder": order, "port": 0}
                    for order, device in enumerate(members, start=1)
                ]
            },
        }
        return self.client.addRouteGroup(req)

    def delete_route_group(self, **args):
        """
        Delete a Route group
        :param name: The name of the Route group to delete (or uuid)
        :param uuid: The uuid of the Route group to delete (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeRouteGroup(**args)

    def update_route_group(self, **args):
        """
        Update a Route group
        :param name: The name of the Route group to update (or uuid)
        :param uuid: The uuid of the Route group to update (or name)
        :param newName: new route group name
        :param distribution_algorithm: Top Down, Circular, Longest Idle Time or Broadcast
        :param members: replaces all members: {'member': [{'deviceName', 'deviceSelectionOrder', 'port'}]}
        :param addMembers: members to add, same shape as members (instead of members)
        :param removeMembers: members to remove, same shape as members (instead of members)
        :return: result dictionary
        

        Schema: `UpdateRouteGroupReq`: optional `distributionAlgorithm`, optional choice of (optional `removeMembers`, `addMembers`), or `members`, `newName`.
        """
        return self.client.updateRouteGroup(**args)

    def get_route_lists(self, tagfilter={"name": "", "description": ""}):
        """
        Get route lists
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of dictionaries, empty when nothing matches
        

        Schema: `ListRouteListReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        return self.client.listRouteList({"name": "%"}, returnedTags=tagfilter)[
            "return"
        ]["routeList"]

    def get_route_list(self, **args):
        """
        Get route list
        :param name: route list name
        :param uuid: route list uuid
        :return: result dictionary
        

        Schema: `GetRouteListReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getRouteList(**args)["return"]["routeList"]

    def add_route_list(
        self,
        name,
        description="",
        cm_group_name="Default",
        route_list_enabled="true",
        run_on_all_nodes="false",
        members=[],
    ):

        """
        Add a route list
        :param name: Route list name
        :param description: Route list description
        :param cm_group_name: Route list call manager group name
        :param route_list_enabled: Enable route list
        :param run_on_all_nodes: Run route list on all nodes
        :param members: A list of route group names, in selection order
        :return: Result dictionary
        

        Schema: `routeList` -> `XRouteList`: `name` + `callManagerGroupName`; optional `description`, `routeListEnabled`, `members`, `runOnEveryNode`.
        """
        req = {
            "name": name,
            "description": description,
            "callManagerGroupName": cm_group_name,
            "routeListEnabled": route_list_enabled,
            "runOnEveryNode": run_on_all_nodes,
            "members": {
                "member": [
                    {
                        "routeGroupName": group,
                        "selectionOrder": order,
                        "useFullyQualifiedCallingPartyNumber": "Default",
                        "callingPartyNumberingPlan": "Cisco CallManager",
                        "callingPartyNumberType": "Cisco CallManager",
                        "calledPartyNumberingPlan": "Cisco CallManager",
                        "calledPartyNumberType": "Cisco CallManager",
                    }
                    for order, group in enumerate(members, start=1)
                ]
            },
        }
        return self.client.addRouteList(req)

    def delete_route_list(self, **args):
        """
        Delete a Route list
        :param name: The name of the Route list to delete
        :param uuid: The uuid of the Route list to delete
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeRouteList(**args)

    def update_route_list(self, **args):
        """
        Update a Route list
        :param name: The name of the Route list to update (or uuid)
        :param uuid: The uuid of the Route list to update (or name)
        :param newName: new route list name
        :param description: Route list description
        :param cm_group_name: Route list call manager group name (AXL name: callManagerGroupName)
        :param route_list_enabled: Enable route list (AXL name: routeListEnabled)
        :param run_on_all_nodes: Run route list on all nodes (AXL name: runOnEveryNode)
        :param members: replaces all members: {'member': [{'routeGroupName', 'selectionOrder', 'useFullyQualifiedCallingPartyNumber'}]}
        :param addMembers: members to add, same shape as members (instead of members)
        :param removeMembers: members to remove, same shape as members (instead of members)
        :return: result dictionary
        

        Schema: `UpdateRouteListReq`: optional `newName`, `description`, `callManagerGroupName`, `routeListEnabled`, optional choice of (optional `removeMembers`, `addMembers`), or `members`, `runOnEveryNode`.
        """
        return self.client.updateRouteList(**args)

    def get_partitions(self, tagfilter={"name": "", "description": ""}):
        """
        Get partitions
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of dictionaries, empty when nothing matches
        

        Schema: `ListRoutePartitionReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        return self.client.listRoutePartition(
            {"name": "%"}, returnedTags=tagfilter
        )["return"]["routePartition"]

    def get_partition(self, **args):
        """
        Get partition details
        :param partition: Partition name (AXL name: name)
        :param uuid: Partition uuid
        :return: result dictionary
        

        Schema: `GetRoutePartitionReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getRoutePartition(**args)["return"]["routePartition"]

    def add_partition(self, name, description="", time_schedule_name=None):
        """
        Add a partition
        :param name: Name of the partition to add
        :param description: Partition description, max 50 characters
        :param time_schedule_name: Name of an existing time schedule, None for always active
        :return: result dictionary
        

        Schema: `routePartition` -> `XRoutePartition`: `name`; optional `description`, `timeScheduleIdName`, `useOriginatingDeviceTimeZone`, `timeZone`, `partitionUsage`.
        """
        partition = {"name": name, "description": description}
        if time_schedule_name:
            partition["timeScheduleIdName"] = time_schedule_name
        return self.client.addRoutePartition(partition)

    def delete_partition(self, **args):
        """
        Delete a partition
        :param partition: The name of the partition to delete (AXL name: name)
        :param uuid: The uuid of the partition to delete
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeRoutePartition(**args)

    def update_partition(self, **args):
        """
        Update a partition
        :param uuid: Partition uuid (or name)
        :param name: Partition name (or uuid)
        :param description: Partition description, max 50 characters
        :param newName: new partition name
        :param timeScheduleIdName: time schedule name
        :param useOriginatingDeviceTimeZone: boolean
        :param timeZone: time zone when not using the originating device's
        :return: result dictionary
        

        Schema: `UpdateRoutePartitionReq`: optional `newName`, `description`, `timeScheduleIdName`, `useOriginatingDeviceTimeZone`, `timeZone`.
        """
        return self.client.updateRoutePartition(**args)

    def get_calling_search_spaces(self, tagfilter={"name": "", "description": ""}):
        """
        Get calling search spaces
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of dictionaries, empty when nothing matches
        

        Schema: `ListCssReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        return self.client.listCss({"name": "%"}, returnedTags=tagfilter)["return"][
            "css"
        ]

    def get_calling_search_space(self, **args):
        """
        Get Calling search space details
        :param name: Calling search space name
        :param uuid: Calling search space uuid
        :return: result dictionary
        

        Schema: `GetCssReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getCss(**args)["return"]["css"]

    def add_calling_search_space(self, name, description="", members=[]):
        """
        Add a Calling search space
        :param name: Name of the CSS to add
        :param description: Calling search space description
        :param members: A list of partitions to add to the CSS
        :return: result dictionary
        

        Schema: `css` -> `XCss`: `name`; optional `description`, `members`, `partitionUsage`.
        """
        req = {
            "name": name,
            "description": description,
            "members": {
                "member": [
                    {"routePartitionName": partition, "index": index}
                    for index, partition in enumerate(members, start=1)
                ]
            },
        }
        return self.client.addCss(req)

    def delete_calling_search_space(self, **args):
        """
        Delete a Calling search space
        :param calling_search_space: The name of the calling search space to delete (AXL name: name)
        :param uuid: The uuid of the calling search space to delete
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeCss(**args)

    def update_calling_search_space(self, **args):
        """
        Update calling search space
        :param uuid: CSS uuid (or name)
        :param name: CSS name (or uuid)
        :param description: CSS description, max 50 characters
        :param newName: new CSS name
        :param members: replaces all members: {'member': [{'routePartitionName', 'index'}]}
        :param addMembers: members to add, same shape as members (instead of members)
        :param removeMembers: members to remove, same shape as members (instead of members)
        :return: result dictionary
        

        Schema: `UpdateCssReq`: optional `description`, optional choice of (optional `removeMembers`, `addMembers`), or `members`, `newName`.
        """
        return self.client.updateCss(**args)

    def get_route_patterns(
        self, tagfilter={"pattern": "", "description": "", "uuid": ""}
    ):
        """
        Get route patterns
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of dictionaries, empty when nothing matches
        

        Schema: `ListRoutePatternReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        return self.client.listRoutePattern(
            {"pattern": "%"},
            returnedTags=tagfilter,
        )["return"]["routePattern"]

    def get_route_pattern(self, pattern="", uuid="", partition=""):
        """
        Get route pattern
        :param pattern: route pattern (or uuid)
        :param uuid: route pattern uuid (or pattern)
        :param partition: route pattern partition; when omitted, the first pattern match in any partition is returned
        :return: route pattern dictionary
        

        Schema: `GetRoutePatternReq`: optional `returnedTags`; one of `uuid`, or (`pattern` + `routePartitionName` + `dialPlanName` + `routeFilterName`).
        """
        if bool(pattern) == bool(uuid):
            raise ValueError("Provide exactly one of pattern or uuid")
        if pattern and partition:
            identifier = {
                "pattern": pattern,
                "routePartitionName": partition,
                "dialPlanName": None,
                "routeFilterName": None,
            }
        elif pattern:
            matches = self.client.listRoutePattern(
                {"pattern": pattern}, returnedTags={"uuid": ""}
            )["return"]["routePattern"]
            if not matches:
                raise LookupError(f"Route pattern '{pattern}' not found")
            identifier = {"uuid": matches[0]["uuid"]}
        else:
            identifier = {"uuid": uuid}
        return self.client.getRoutePattern(**identifier)["return"]["routePattern"]

    def add_route_pattern(
        self,
        pattern,
        gateway="",
        route_list="",
        description="",
        partition="",
        blockEnable=False,
        patternUrgency=False,
        releaseClause="No Error",
    ):
        """
        Add a route pattern
        :param pattern: Route pattern - required
        :param gateway: Destination gateway - provide exactly one of gateway or route_list
        :param route_list: Destination route list - provide exactly one of gateway or route_list
        :param description: Route pattern description
        :param partition: Route pattern partition
        :param blockEnable: block the pattern instead of routing it
        :param patternUrgency: route immediately on match (urgent priority)
        :param releaseClause: release cause when blocked, e.g. 'Call Rejected'; default 'No Error'
        :return: result dictionary
        

        Schema: `routePattern` -> `XRoutePattern`: `pattern` + `routePartitionName` + `blockEnable` + `useCallingPartyPhoneMask` + `dialPlanName` + `digitDiscardInstructionName` + `networkLocation` + `prefixDigitsOut` + `routeFilterName` + `destination`; optional `description`, `calledPartyTransformationMask`, `callingPartyTransformationMask`, `callingPartyPrefixDigits`, `patternUrgency`, `callingLinePresentationBit` and 22 more.
        """
        if bool(gateway) == bool(route_list):
            raise ValueError("Provide exactly one of gateway or route_list")
        destination = {"gatewayName": gateway} if gateway else {"routeListName": route_list}

        req = {
            "pattern": pattern,
            "description": description,
            "destination": destination,
            "routePartitionName": partition,
            "blockEnable": blockEnable,
            "patternUrgency": patternUrgency,
            "releaseClause": releaseClause,
            "useCallingPartyPhoneMask": "Default",
            "networkLocation": "OnNet",
        }
        return self.client.addRoutePattern(req)

    def delete_route_pattern(self, **args):
        """
        Delete a route pattern
        :param uuid: The pattern uuid (or pattern + partition)
        :param pattern: The pattern of the route to delete
        :param partition: The name of the partition (AXL name: routePartitionName)
        :param dialPlanName: dial plan, usually omitted
        :param routeFilterName: route filter, usually omitted
        :return: result dictionary
        

        Schema: `RemoveRoutePatternReq`: one of `uuid`, or (`pattern` + `routePartitionName` + `dialPlanName` + `routeFilterName`).
        """
        if "uuid" not in args:
            args.setdefault("dialPlanName", None)
            args.setdefault("routeFilterName", None)
        return self.client.removeRoutePattern(**args)

    def update_route_pattern(self, **args):
        """
        Update a route pattern
        :param uuid: The pattern uuid (or pattern + partition)
        :param pattern: The pattern of the route to update
        :param partition: The name of the partition (AXL name: routePartitionName)
        :param newPattern: new pattern
        :param new_partition: new partition (AXL name: newRoutePartitionName)
        :param gateway: Destination gateway (AXL name: destination.gatewayName)
        :param route_list: Destination route list (AXL name: destination.routeListName)
               Provide at most one of gateway or route_list
        :param description: Route pattern description
        :return: result dictionary
        

        Schema: `UpdateRoutePatternReq`: optional `newPattern`, `description`, `newRoutePartitionName`, `blockEnable`, `calledPartyTransformationMask`, `callingPartyTransformationMask` and 32 more; one of `uuid`, or (`pattern` + `routePartitionName` + `dialPlanName` + `routeFilterName`).
        """
        if "uuid" not in args:
            args.setdefault("dialPlanName", None)
            args.setdefault("routeFilterName", None)
        return self.client.updateRoutePattern(**args)

    def get_media_resource_groups(self, tagfilter={"name": "", "description": ""}):
        """
        Get media resource groups
        :param tagfilter: AXL returned tags to include, e.g. {'name': '', 'description': ''}
        :return: list of media resource group dictionaries
        

        Schema: `ListMediaResourceGroupReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        return self.client.listMediaResourceGroup(
            {"name": "%"}, returnedTags=tagfilter
        )["return"]["mediaResourceGroup"]

    def get_media_resource_group(self, **args):
        """
        Get a media resource group details
        :param media_resource_group: Media resource group name (AXL name: name)
        :param uuid: Media resource group uuid
        :return: result dictionary
        

        Schema: `GetMediaResourceGroupReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getMediaResourceGroup(**args)["return"][
            "mediaResourceGroup"
        ]

    def add_media_resource_group(
        self, name, description="", multicast="false", members=[]
    ):
        """
        Add a media resource group
        :param name: Media resource group name
        :param description: Media resource description
        :param multicast: Multicast enabled
        :param members: list of media resource device names
        :return: result dictionary
        

        Schema: `mediaResourceGroup` -> `XMediaResourceGroup`: `name` + `multicast` + `members`; optional `description`.
        """
        req = {
            "name": name,
            "description": description,
            "multicast": multicast,
            "members": {"member": [{"deviceName": device} for device in members]},
        }
        return self.client.addMediaResourceGroup(req)

    def update_media_resource_group(self, **args):
        """
        Update a media resource group
        :param name: Media resource group name (or uuid)
        :param uuid: Media resource group uuid (or name)
        :param newName: new media resource group name
        :param description: Media resource description
        :param multicast: Multicast enabled
        :param members: replaces all members: {'member': [{'deviceName': name}]}
        :param addMembers: members to add, same shape as members (instead of members)
        :param removeMembers: members to remove, same shape as members (instead of members)
        :return: result dictionary
        

        Schema: `UpdateMediaResourceGroupReq`: optional `newName`, `description`, `multicast`, optional choice of (optional `removeMembers`, `addMembers`), or `members`.
        """
        return self.client.updateMediaResourceGroup(**args)

    def delete_media_resource_group(self, name="", uuid=""):
        """
        Delete a Media resource group
        :param name: The name of the media resource group to delete (or uuid)
        :param uuid: The uuid of the media resource group to delete (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeMediaResourceGroup(**self._identify(name=name, uuid=uuid))

    def get_media_resource_group_lists(self, tagfilter={"name": ""}):
        """
        Get media resource group lists
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of media resource group list dictionaries
        

        Schema: `ListMediaResourceListReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        return self.client.listMediaResourceList(
            {"name": "%"}, returnedTags=tagfilter
        )["return"]["mediaResourceList"]

    def get_media_resource_group_list(self, name="", uuid=""):
        """
        Get a media resource group list details
        :param name: Media resource group list name (or uuid)
        :param uuid: Media resource group list uuid (or name)
        :return: media resource group list dictionary
        

        Schema: `GetMediaResourceListReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getMediaResourceList(**self._identify(name=name, uuid=uuid))[
            "return"
        ]["mediaResourceList"]

    def add_media_resource_group_list(self, name, members=[]):
        """
        Add a media resource group list
        :param name: Media resource group list name
        :param members: list of media resource group names, in priority order
        :return: result dictionary
        

        Schema: `mediaResourceList` -> `XMediaResourceList`: `name` + `members`.
        """
        req = {
            "name": name,
            "members": {
                "member": [
                    {"order": order, "mediaResourceGroupName": group}
                    for order, group in enumerate(members)
                ]
            },
        }
        return self.client.addMediaResourceList(req)

    def update_media_resource_group_list(self, **args):
        """
        Update a media resource group list
        :param name: Media resource group list name (or uuid)
        :param uuid: Media resource group list uuid (or name)
        :param newName: new media resource group list name
        :param members: replaces all members: {'member': [{'mediaResourceGroupName', 'order'}]}
        :param addMembers: members to add, same shape as members (instead of members)
        :param removeMembers: members to remove, same shape as members (instead of members)
        :return: result dictionary
        

        Schema: `UpdateMediaResourceListReq`: optional `newName`, optional choice of (optional `removeMembers`, `addMembers`), or `members`.
        """
        return self.client.updateMediaResourceList(**args)

    def delete_media_resource_group_list(self, name="", uuid=""):
        """
        Delete a Media resource group list
        :param name: The name of the media resource group list to delete (or uuid)
        :param uuid: The uuid of the media resource group list to delete (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeMediaResourceList(**self._identify(name=name, uuid=uuid))

    def get_directory_numbers(
        self,
        tagfilter={
            "pattern": "",
            "description": "",
            "routePartitionName": "",
        },
    ):
        """
        Get directory numbers
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of dictionaries, empty when nothing matches
        

        Schema: `ListLineReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        return self.client.listLine({"pattern": "%"}, returnedTags=tagfilter,)[
            "return"
        ]["line"]

    def get_directory_number(self, **args):
        """
        Get directory number details
        :param pattern: directory number pattern (or uuid)
        :param uuid: directory number uuid (or pattern + partition)
        :param partition: route partition name, optional (AXL name: routePartitionName)
        :return: result dictionary
        

        Schema: `GetLineReq`: optional `returnedTags`; one of `uuid`, or (`pattern`; optional `routePartitionName`).
        """
        return self.client.getLine(**args)["return"]["line"]

    def add_directory_number(
        self,
        pattern,
        partition="",
        description="",
        alerting_name="",
        ascii_alerting_name="",
        shared_line_css="",
        aar_neighbourhood="",
        call_forward_css="",
        vm_profile_name="NoVoiceMail",
        aar_destination_mask="",
        call_forward_destination="",
        forward_all_to_vm="false",
        forward_all_destination="",
        forward_to_vm="false",
    ):
        """
        Add a directory number
        :param pattern: Directory number
        :param partition: Route partition name
        :param description: Directory number description
        :param alerting_name: Alerting name
        :param ascii_alerting_name: ASCII alerting name
        :param shared_line_css: Calling search space
        :param aar_neighbourhood: AAR group
        :param call_forward_css: Call forward calling search space
        :param vm_profile_name: Voice mail profile
        :param aar_destination_mask: AAR destination mask
        :param call_forward_destination: Call forward destination
        :param forward_all_to_vm: Forward all to voice mail checkbox
        :param forward_all_destination: Forward all destination
        :param forward_to_vm: Forward to voice mail checkbox
        :return: result dictionary
        

        Schema: `line` -> `XLine`: `pattern` + `usage`; optional `description`, `routePartitionName`, `aarNeighborhoodName`, `aarDestinationMask`, `aarKeepCallHistory`, `aarVoiceMailEnabled` and 49 more.
        """
        return self.client.addLine(
            {
                "pattern": pattern,
                "routePartitionName": partition,
                "description": description,
                "alertingName": alerting_name,
                "asciiAlertingName": ascii_alerting_name,
                "voiceMailProfileName": vm_profile_name,
                "shareLineAppearanceCssName": shared_line_css,
                "aarNeighborhoodName": aar_neighbourhood,
                "aarDestinationMask": aar_destination_mask,
                "usage": "Device",
                "callForwardAll": {
                    "forwardToVoiceMail": forward_all_to_vm,
                    "callingSearchSpaceName": call_forward_css,
                    "secondaryCallingSearchSpaceName": None,
                    "destination": forward_all_destination,
                },
                "callForwardBusy": {
                    "forwardToVoiceMail": forward_to_vm,
                    "callingSearchSpaceName": call_forward_css,
                    "destination": call_forward_destination,
                },
                "callForwardBusyInt": {
                    "forwardToVoiceMail": forward_to_vm,
                    "callingSearchSpaceName": call_forward_css,
                    "destination": call_forward_destination,
                },
                "callForwardNoAnswer": {
                    "forwardToVoiceMail": forward_to_vm,
                    "callingSearchSpaceName": call_forward_css,
                    "destination": call_forward_destination,
                },
                "callForwardNoAnswerInt": {
                    "forwardToVoiceMail": forward_to_vm,
                    "callingSearchSpaceName": call_forward_css,
                    "destination": call_forward_destination,
                },
                "callForwardNoCoverage": {
                    "forwardToVoiceMail": forward_to_vm,
                    "callingSearchSpaceName": call_forward_css,
                    "destination": call_forward_destination,
                },
                "callForwardNoCoverageInt": {
                    "forwardToVoiceMail": forward_to_vm,
                    "callingSearchSpaceName": call_forward_css,
                    "destination": call_forward_destination,
                },
                "callForwardOnFailure": {
                    "forwardToVoiceMail": forward_to_vm,
                    "callingSearchSpaceName": call_forward_css,
                    "destination": call_forward_destination,
                },
                "callForwardNotRegistered": {
                    "forwardToVoiceMail": forward_to_vm,
                    "callingSearchSpaceName": call_forward_css,
                    "destination": call_forward_destination,
                },
                "callForwardNotRegisteredInt": {
                    "forwardToVoiceMail": forward_to_vm,
                    "callingSearchSpaceName": call_forward_css,
                    "destination": call_forward_destination,
                },
            }
        )

    def delete_directory_number(
        self, pattern="", routePartitionName="", uuid="", partition=""
    ):
        """
        Delete a directory number
        :param pattern: Directory number (or uuid)
        :param routePartitionName: Route partition name, same as partition
        :param uuid: Directory number uuid (or pattern)
        :param partition: Route partition name, empty for the <None> partition
        :return: result dictionary
        

        Schema: `RemoveLineReq`: one of `uuid`, or (`pattern`; optional `routePartitionName`).
        """
        if bool(pattern) == bool(uuid):
            raise ValueError("Provide exactly one of pattern or uuid")
        if uuid:
            return self.client.removeLine(uuid=uuid)
        return self.client.removeLine(
            pattern=pattern, routePartitionName=partition or routePartitionName or None
        )

    def update_directory_number(self, **args):
        """
        Update a directory number
        :param pattern: Directory number (or uuid)
        :param partition: Route partition name (AXL name: routePartitionName)
        :param uuid: Directory number uuid (or pattern + partition)
        :param newPattern: new directory number
        :param new_partition: new partition (AXL name: newRoutePartitionName)
        :param description: Directory number description
        :param alerting_name: Alerting name (AXL name: alertingName)
        :param ascii_alerting_name: ASCII alerting name (AXL name: asciiAlertingName)
        :param shared_line_css: Shared line appearance CSS (AXL name: shareLineAppearanceCssName)
        :param aar_neighbourhood: AAR group (AXL name: aarNeighborhoodName)
        :param vm_profile_name: Voice mail profile (AXL name: voiceMailProfileName)
        :param aar_destination_mask: AAR destination mask (AXL name: aarDestinationMask)
        :param callForwardAll: {'forwardToVoiceMail', 'callingSearchSpaceName', 'destination'}
        :param callForwardBusy: same shape as callForwardAll; likewise callForwardNoAnswer, callForwardNotRegistered, etc.
        :return: result dictionary
        

        Schema: `UpdateLineReq`: optional `newPattern`, `description`, `newRoutePartitionName`, `aarNeighborhoodName`, `aarDestinationMask`, `aarKeepCallHistory` and 50 more; one of `uuid`, or (`pattern`; optional `routePartitionName`).
        """
        return self.client.updateLine(**args)

    def get_cti_route_points(self, tagfilter={"name": "", "description": ""}):
        """
        Get CTI route points
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of dictionaries, empty when nothing matches
        

        Schema: `ListCtiRoutePointReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        return self.client.listCtiRoutePoint({"name": "%"}, returnedTags=tagfilter)[
            "return"
        ]["ctiRoutePoint"]

    def get_cti_route_point(self, **args):
        """
        Get CTI route point details
        :param name: CTI route point name
        :param uuid: CTI route point uuid
        :return: result dictionary
        

        Schema: `GetCtiRoutePointReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getCtiRoutePoint(**args)["return"]["ctiRoutePoint"]

    def add_cti_route_point(
        self,
        name,
        description="",
        device_pool="Default",
        location="Hub_None",
        common_device_config="",
        css="",
        product="CTI Route Point",
        dev_class="CTI Route Point",
        protocol="SCCP",
        protocol_slide="User",
        use_trusted_relay_point="Default",
        lines=[],
        protocol_side=None,
    ):
        """
        Add CTI route point
        lines should be a list of tuples containing the pattern and partition
        EG: [('77777', 'AU_PHONE_PT')]
        :param name: CTI route point name
        :param description: CTI route point description
        :param device_pool: Device pool name
        :param location: Location name
        :param common_device_config: Common device config name
        :param css: Calling search space name
        :param product: CTI device type
        :param dev_class: CTI device type
        :param protocol: CTI protocol
        :param protocol_side: protocol side, default 'User'
        :param protocol_slide: deprecated misspelling of protocol_side
        :param use_trusted_relay_point: Use trusted relay point: (Default, On, Off)
        :param lines: A list of tuples of [(directory_number, partition)]
        :return: result dictionary
        

        Schema: `ctiRoutePoint` -> `XCtiRoutePoint`: `name` + `product` + `class` + `protocol` + `protocolSide` + `devicePoolName` + `locationName` + `useTrustedRelayPoint`; optional `description`, `callingSearchSpaceName`, `commonDeviceConfigName`, `mediaResourceListName`, `networkHoldMohAudioSourceId`, `userHoldMohAudioSourceId` and 5 more.
        """

        req = {
            "name": name,
            "description": description,
            "product": product,
            "class": dev_class,
            "protocol": protocol,
            "protocolSide": protocol_side or protocol_slide,
            "commonDeviceConfigName": common_device_config,
            "callingSearchSpaceName": css,
            "devicePoolName": device_pool,
            "locationName": location,
            "useTrustedRelayPoint": use_trusted_relay_point,
        }
        if lines:
            req["lines"] = self._lines(lines)

        return self.client.addCtiRoutePoint(req)

    def delete_cti_route_point(self, **args):
        """
        Delete a CTI route point
        :param cti_route_point: The name of the CTI route point to delete (AXL name: name)
        :param uuid: The uuid of the CTI route point to delete
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeCtiRoutePoint(**args)

    def update_cti_route_point(self, **args):
        """
        Update CTI route point (product, class and protocol can't be changed after creation)
        lines can be a list of tuples containing the pattern and partition
        EG: [('77777', 'AU_PHONE_PT')]
        :param name: CTI route point name (or uuid)
        :param uuid: CTI route point uuid (or name)
        :param newName: new CTI route point name
        :param description: CTI route point description
        :param device_pool: Device pool name
        :param location: Location name
        :param common_device_config: Common device config name
        :param css: Calling search space name
        :param protocol_side: protocol side
        :param use_trusted_relay_point: Use trusted relay point: (Default, On, Off)
        :param lines: replaces all lines: list of tuples [(directory_number, partition)]
        :return: result dictionary
        

        Schema: `UpdateCtiRoutePointReq`: optional `newName`, `description`, `protocol`, `protocolSide`, `callingSearchSpaceName`, `devicePoolName` and 11 more.
        """
        return self.client.updateCtiRoutePoint(**self._with_lines(args))

    def get_phones(
        self,
        query={"name": "%"},
        tagfilter={
            "name": "",
            "product": "",
            "description": "",
            "protocol": "",
            "locationName": "",
            "callingSearchSpaceName": "",
        },
    ):
        """
        Get phones, paging through results 1000 at a time
        :param query: AXL search criteria, e.g. {'name': 'SEP%'} or {'devicePoolName': 'Default'}
        :param tagfilter: AXL returned tags to include, e.g. {'name': '', 'product': ''}
        :return: list of phone dictionaries, empty when nothing matches
        

        Schema: `ListPhoneReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        skip = 0
        a = []

        def inner(skip):
            while True:
                res = self.client.listPhone(
                    searchCriteria=query, returnedTags=tagfilter, first=1000, skip=skip
                )["return"]
                skip = skip + 1000
                if res is not None and "phone" in res:
                    yield res["phone"]
                else:
                    break

        for each in inner(skip):
            a.extend(each)
        return a

    def get_phone(self, **args):
        """
        Get device profile parameters
        :param phone: profile name
        :return: result dictionary
        

        Schema: `GetPhoneReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getPhone(**args)["return"]["phone"]

    def add_phone(
        self,
        name,
        description="",
        product="Cisco 8861",
        device_pool="Default",
        location="Hub_None",
        phone_template="Standard 8861 SIP",
        common_device_config="",
        css="",
        aar_css="",
        subscribe_css="",
        owner_user_name="",
        security_profile_name="",
        lines=[],
        dev_class="Phone",
        protocol="SIP",
        softkey_template="Standard User",
        enable_em="true",
        em_service_name="Extension Mobility",
        em_service_url=False,
        em_url_button_enable=False,
        em_url_button_index="1",
        em_url_label="Press here to logon",
        ehook_enable=None,
        enable_activation_id=False,
        allow_mra_mode=False,
        sip_profile="Standard SIP Profile",
        common_phone_config="Standard Common Phone Profile",
    ):
        """
        lines takes a list of Tuples with properties for each line EG:

                                               display                           external
            DN     partition    display        ascii          label               mask
        [('77777', 'LINE_PT', 'Jim Smith', 'Jim Smith', 'Jim Smith - 77777', '0294127777')]
        Add A phone
        :param name: device name, e.g. SEP001122334455
        :param description: description
        :param product: phone model, e.g. 'Cisco 8861'
        :param device_pool: device pool name
        :param location: location name
        :param phone_template: phone button template matching product and protocol
        :param common_device_config: common device configuration name
        :param css: calling search space
        :param aar_css: AAR calling search space
        :param subscribe_css: presence subscribe calling search space
        :param owner_user_name: owner user ID (AXL name: ownerUserName)
        :param security_profile_name: security profile; SIP phones default to '<product> - Standard SIP Non-Secure Profile' (AXL name: securityProfileName)
        :param lines: list of line tuples, see above
        :param dev_class: device class, default 'Phone'
        :param protocol: 'SIP' or 'SCCP'
        :param softkey_template: softkey template name
        :param enable_em: allow Extension Mobility logins
        :param em_service_name: Extension Mobility IP phone service name
        :param em_service_url: subscribe the phone to the Extension Mobility service
        :param em_url_button_enable: also add the service as a URL button (needs em_service_url)
        :param em_url_button_index: URL button index
        :param em_url_label: URL button label
        :param ehook_enable: set the vendor config ehookEnable value (1 or 0); omitted when None
        :param enable_activation_id: onboard with an activation code (12.5 and later schemas; AXL name: enableActivationID)
        :param allow_mra_mode: allow MRA activation-code onboarding (12.5 and later schemas; AXL name: allowMraMode)
        :param sip_profile: SIP profile, used when protocol is SIP
        :param common_phone_config: common phone profile name
        :return: result dictionary
        

        Schema: `phone` -> `XPhone`: `name` + `product` + `class` + `protocol` + `protocolSide` + `devicePoolName` + `commonPhoneConfigName` + `locationName` + `useTrustedRelayPoint` + `phoneTemplateName` + `primaryPhoneName` + `builtInBridgeStatus` + `packetCaptureMode` + `certificateOperation` + `deviceMobilityMode`; optional `description`, `callingSearchSpaceName`, `commonDeviceConfigName`, `networkLocation`, `mediaResourceListName`, `networkHoldMohAudioSourceId` and 105 more.
        """

        req = {
            "name": name,
            "description": description,
            "product": product,
            "class": dev_class,
            "protocol": protocol,
            "protocolSide": "User",
            "commonDeviceConfigName": common_device_config,
            "commonPhoneConfigName": common_phone_config,
            "softkeyTemplateName": softkey_template,
            "phoneTemplateName": phone_template,
            "devicePoolName": device_pool,
            "locationName": location,
            "primaryPhoneName": None,
            "useTrustedRelayPoint": "Off",
            "builtInBridgeStatus": "Default",
            "certificateOperation": "No Pending Operation",
            "packetCaptureMode": "None",
            "deviceMobilityMode": "Default",
            "enableExtensionMobility": enable_em,
            "callingSearchSpaceName": css,
            "automatedAlternateRoutingCssName": aar_css,
            "subscribeCallingSearchSpaceName": subscribe_css,
            "ownerUserName": owner_user_name,
        }

        if protocol == "SIP":
            req["sipProfileName"] = sip_profile
            req["securityProfileName"] = (
                security_profile_name or f"{product} - Standard SIP Non-Secure Profile"
            )
        elif security_profile_name:
            req["securityProfileName"] = security_profile_name

        phone_fields = self._schema_fields("addPhone", "phone")
        for field, value in (
            ("enableActivationID", enable_activation_id),
            ("allowMraMode", allow_mra_mode),
        ):
            if field in phone_fields:
                req[field] = str(value).lower() in ("true", "t", "1")

        if lines:
            req["lines"] = self._lines(lines)

        if em_service_url:
            service = {
                "telecasterServiceName": em_service_name,
                "name": em_service_name,
                "url": "http://{0}:8080/emapp/EMAppServlet?device=#DEVICENAME#&EMCC=#EMCC#".format(
                    self.cucm
                ),
            }
            if em_url_button_enable:
                service.update(
                    {"urlButtonIndex": em_url_button_index, "urlLabel": em_url_label}
                )
            req["services"] = {"service": [service]}

        if ehook_enable is not None:
            ehook = etree.Element("ehookEnable")
            ehook.text = str(ehook_enable)
            req["vendorConfig"] = {"_value_1": [ehook]}

        return self.client.addPhone(req)

    def delete_phone(self, **args):
        """
        Delete a phone
        :param phone: The name of the phone to delete (AXL name: name)
        :param uuid: The uuid of the phone to delete
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removePhone(**args)

    def update_phone(self, **args):

        """
        Update a phone (product, class and protocol can't be changed after creation)
        lines can be a list of Tuples with properties for each line EG:

                                               display                           external
            DN     partition    display        ascii          label               mask
        [('77777', 'LINE_PT', 'Jim Smith', 'Jim Smith', 'Jim Smith - 77777', '0294127777')]
        :param name: device name (or uuid)
        :param uuid: device uuid (or name)
        :param newName: new device name
        :param description: description
        :param device_pool: device pool name
        :param location: location name
        :param phone_template: phone button template
        :param common_device_config: common device configuration name
        :param css: calling search space
        :param aar_css: AAR calling search space
        :param subscribe_css: presence subscribe calling search space
        :param lines: replaces all lines: list of line tuples, see above
        :param addLines: lines to add, AXL structure {'line': [...]} (instead of lines)
        :param removeLines: lines to remove, AXL structure {'line': [...]} (instead of lines)
        :param softkey_template: softkey template name
        :param enable_em: allow Extension Mobility logins
        :param security_profile: security profile name
        :param sip_profile: SIP profile name
        :return: result dictionary
        

        Schema: `UpdatePhoneReq`: optional `newName`, `description`, `callingSearchSpaceName`, `devicePoolName`, `commonDeviceConfigName`, `commonPhoneConfigName` and 115 more.
        """
        return self.client.updatePhone(**self._with_lines(args))

    def get_device_profiles(
        self,
        tagfilter={
            "name": "",
            "product": "",
            "protocol": "",
            "phoneTemplateName": "",
        },
    ):
        """
        Get device profile details
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of dictionaries, empty when nothing matches
        

        Schema: `ListDeviceProfileReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        return self.client.listDeviceProfile(
            {"name": "%"},
            returnedTags=tagfilter,
        )["return"]["deviceProfile"]

    def get_device_profile(self, **args):
        """
        Get device profile parameters
        :param name: profile name
        :param uuid: profile uuid
        :return: result dictionary
        

        Schema: `GetDeviceProfileReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getDeviceProfile(**args)["return"]["deviceProfile"]

    def add_device_profile(
        self,
        name,
        description="",
        product="Cisco 7962",
        phone_template="Standard 7962G SCCP",
        dev_class="Device Profile",
        protocol="SCCP",
        protocolSide="User",
        softkey_template="Standard User",
        em_service_name="Extension Mobility",
        lines=[],
    ):
        """
        Add A Device profile for use with extension mobility
        lines takes a list of Tuples with properties for each line EG:

                                               display                           external
            DN     partition    display        ascii          label               mask
        [('77777', 'LINE_PT', 'Jim Smith', 'Jim Smith', 'Jim Smith - 77777', '0294127777')]
        :param name: device profile name
        :param description: description
        :param product: phone model the profile is for
        :param phone_template: phone button template matching product and protocol
        :param lines: list of line tuples, see above
        :param dev_class: device class, default 'Device Profile'
        :param protocol: 'SIP' or 'SCCP'
        :param protocolSide: protocol side, default 'User'
        :param softkey_template: softkey template name
        :param em_service_name: Extension Mobility service to subscribe, None for no services
        :return: result dictionary
        

        Schema: `deviceProfile` -> `XDeviceProfile`: `name` + `product` + `class` + `protocol` + `protocolSide` + `phoneTemplateName`; optional `description`, `userHoldMohAudioSourceId`, `vendorConfig`, `traceFlag`, `mlppDomainId`, `mlppIndicationStatus` and 21 more.
        """

        req = {
            "name": name,
            "description": description,
            "product": product,
            "class": dev_class,
            "protocol": protocol,
            "protocolSide": protocolSide,
            "softkeyTemplateName": softkey_template,
            "phoneTemplateName": phone_template,
        }
        if lines:
            req["lines"] = self._lines(lines)
        if em_service_name:
            req["services"] = {
                "service": [
                    {"telecasterServiceName": em_service_name, "name": em_service_name}
                ]
            }

        return self.client.addDeviceProfile(req)

    def delete_device_profile(self, **args):
        """
        Delete a device profile
        :param profile: The name of the device profile to delete (AXL name: name)
        :param uuid: The uuid of the device profile to delete
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeDeviceProfile(**args)

    def update_device_profile(self, **args):
        """
        Update A Device profile for use with extension mobility
        (product, class and protocol can't be changed after creation)
        lines can be a list of Tuples with properties for each line EG:

                                               display                           external
            DN     partition    display        ascii          label               mask
        [('77777', 'LINE_PT', 'Jim Smith', 'Jim Smith', 'Jim Smith - 77777', '0294127777')]
        :param profile: device profile name (AXL name: name)
        :param uuid: device profile uuid
        :param newName: new device profile name
        :param description: description
        :param phone_template: phone button template
        :param softkey_template: softkey template name
        :param lines: replaces all lines: list of line tuples, see above
        :param services: {'service': [{'telecasterServiceName', 'name'}]}
        :return: result dictionary
        

        Schema: `UpdateDeviceProfileReq`: optional `newName`, `description`, `userHoldMohAudioSourceId`, `vendorConfig`, `mlppDomainId`, `mlppIndicationStatus` and 22 more.
        """
        return self.client.updateDeviceProfile(**self._with_lines(args))

    def get_users(self, tagfilter={"userid": "", "firstName": "", "lastName": ""}):
        """
        Get users details
        Parameters
        -------
        tagfilter : dictionary, optional
            userid: None or uuid of user
            firstName: None or first name of user
            lastName: None or last name of user
        
        Returns
        -------
        users
            A list of Users
        

        Schema: `ListUserReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        skip = 0
        a = []

        def inner(skip):
            while True:
                res = self.client.listUser(
                    {"userid": "%"}, returnedTags=tagfilter, first=1000, skip=skip
                )["return"]
                skip = skip + 1000
                if res is not None and "user" in res:
                    yield res["user"]
                else:
                    break

        for each in inner(skip):
            a.extend(each)
        return a

    def get_user(self, userid="", user_id="", uuid=""):
        """
        Get user parameters
        :param userid: User ID (or uuid)
        :param user_id: same as userid
        :param uuid: user uuid (or userid)
        :return: user dictionary
        

        Schema: `GetUserReq`: optional `returnedTags`; one of `userid`, or `uuid`.
        """
        userid = userid or user_id
        if bool(userid) == bool(uuid):
            raise ValueError("Provide exactly one of userid or uuid")
        identifier = {"userid": userid} if userid else {"uuid": uuid}
        return self.client.getUser(**identifier)["return"]["user"]

    def add_user(
        self,
        userid="",
        lastName="",
        firstName="",
        presenceGroupName="Standard Presence group",
        phoneProfiles=[],
        user_id="",
        last_name="",
        first_name="",
    ):
        """
        Add a user
        :param userid: User ID of the user to add (or user_id) - required
        :param lastName: Last name of the user to add (or last_name) - required
        :param firstName: First name of the user to add (or first_name) - optional
        :param presenceGroupName: presence group name
        :param phoneProfiles: list of device profile names to associate
        :return: result dictionary
        

        Schema: `user` -> `XUser`: `lastName` + `userid` + `presenceGroupName`; optional `firstName`, `displayName`, `middleName`, `emMaxLoginTime`, `password`, `pin` and 50 more.
        """
        userid = userid or user_id
        lastName = lastName or last_name
        firstName = firstName or first_name
        if not userid or not lastName:
            raise ValueError("userid and lastName are required")

        user = {
            "userid": userid,
            "lastName": lastName,
            "presenceGroupName": presenceGroupName,
        }
        if firstName:
            user["firstName"] = firstName
        if phoneProfiles:
            user["phoneProfiles"] = {"profileName": list(phoneProfiles)}
        return self.client.addUser(user)

    def update_user(self, **args):
        """
        Update an end user. Any updatable XUser field is accepted.
        :param userid: User ID (or uuid; user_id also works)
        :param uuid: user uuid (or userid)
        :param password: Web interface password
        :param pin: Extension mobility PIN
        :param first_name: first name (AXL name: firstName)
        :param last_name: last name (AXL name: lastName)
        :param associatedGroups: replaces all groups: {'userGroup': [{'name': group}]}
        :param phoneProfiles: replaces all device profiles: {'profileName': [name, ...]}
        :return: result dictionary
        

        Schema: `UpdateUserReq`: optional `firstName`, `displayName`, `middleName`, `lastName`, `emMaxLoginTime`, `newUserid` and 53 more; one of `uuid`, or `userid`.
        """
        return self.client.updateUser(**args)

    def update_user_em(
        self,
        user_id,
        device_profile,
        default_profile,
        subscribe_css,
        primary_extension,
        user_group="Standard CCM End Users",
        primary_extension_partition=None,
    ):
        """
        Update end user for extension mobility. The device profile and user group are added
        to the user's existing profiles and groups.
        :param user_id: User ID
        :param device_profile: Device profile name
        :param default_profile: Default profile name
        :param subscribe_css: Subscribe CSS
        :param primary_extension: Primary extension, must be a number from the device profile
        :param user_group: user group to add, None to leave groups unchanged
        :param primary_extension_partition: partition of the primary extension
        :return: result dictionary
        

        Schema: `UpdateUserReq`: optional `firstName`, `displayName`, `middleName`, `lastName`, `emMaxLoginTime`, `newUserid` and 53 more; one of `uuid`, or `userid`.
        """
        profile_uuid = self.client.getDeviceProfile(name=device_profile)["return"][
            "deviceProfile"
        ]["uuid"]
        user = self.client.getUser(
            userid=user_id,
            returnedTags={
                "phoneProfiles": {"profileName": ""},
                "associatedGroups": {"userGroup": {"name": ""}},
            },
        )["return"]["user"]

        profiles = [
            {"uuid": profile["uuid"]}
            for profile in ((user["phoneProfiles"] or {}).get("profileName") or [])
            if profile["uuid"]
        ]
        if profile_uuid.lower() not in {p["uuid"].lower() for p in profiles}:
            profiles.append({"uuid": profile_uuid})

        primary = {"pattern": primary_extension}
        if primary_extension_partition:
            primary["routePartitionName"] = primary_extension_partition

        update = {
            "userid": user_id,
            "phoneProfiles": {"profileName": profiles},
            "defaultProfile": default_profile,
            "subscribeCallingSearchSpaceName": subscribe_css,
            "primaryExtension": primary,
        }
        if user_group:
            groups = [
                group["name"]
                for group in ((user["associatedGroups"] or {}).get("userGroup") or [])
            ]
            if user_group not in groups:
                groups.append(user_group)
            update["associatedGroups"] = {
                "userGroup": [{"name": group} for group in groups]
            }
        return self.client.updateUser(**update)

    def update_user_credentials(self, userid, password="", pin=""):  # nosec
        """
        Update end user for credentials
        :param userid: User ID
        :param password: Web interface password
        :param pin: Extension mobility PIN
        :return: result dictionary
        

        Schema: `UpdateUserReq`: optional `firstName`, `displayName`, `middleName`, `lastName`, `emMaxLoginTime`, `newUserid` and 53 more; one of `uuid`, or `userid`.
        """
        if password == "" and pin == "":  # nosec
            raise ValueError("Password and/or Pin are required")

        credentials = {"userid": userid}
        if password != "":  # nosec
            credentials["password"] = password
        if pin != "":
            credentials["pin"] = pin
        return self.client.updateUser(**credentials)

    def delete_user(self, **args):
        """
        Delete a user
        :param userid: The user ID of the user to delete (or uuid; user_id also works)
        :param uuid: The uuid of the user to delete
        :return: result dictionary
        

        Schema: `RemoveUserReq`: one of `userid`, or `uuid`.
        """
        return self.client.removeUser(**args)

    def get_translations(self):
        """
        Get translation patterns
        :return: list of dictionaries, empty when nothing matches
        

        Schema: `ListTransPatternReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        return self.client.listTransPattern(
            {"pattern": "%"},
            returnedTags={
                "pattern": "",
                "description": "",
                "uuid": "",
                "routePartitionName": "",
                "callingSearchSpaceName": "",
                "useCallingPartyPhoneMask": "",
                "patternUrgency": "",
                "provideOutsideDialtone": "",
                "prefixDigitsOut": "",
                "calledPartyTransformationMask": "",
                "callingPartyTransformationMask": "",
                "digitDiscardInstructionName": "",
                "callingPartyPrefixDigits": "",
            },
        )["return"]["transPattern"]

    def _pattern_identifier(self, pattern="", partition="", uuid=""):
        """
        Build the uuid-or-pattern identifier for pattern-based objects
        :param pattern: pattern (or uuid)
        :param partition: partition of the pattern, empty for the <None> partition
        :param uuid: uuid (or pattern)
        :return: {'uuid': uuid} or {'pattern': pattern, 'routePartitionName': partition}
        """
        if bool(pattern) == bool(uuid):
            raise ValueError("Provide exactly one of pattern or uuid")
        if uuid:
            return {"uuid": uuid}
        return {"pattern": pattern, "routePartitionName": partition or None}

    def get_translation(self, pattern="", routePartitionName="", uuid="", partition=""):
        """
        Get translation pattern
        :param pattern: translation pattern to match (or uuid)
        :param routePartitionName: partition of the pattern, same as partition
        :param uuid: translation pattern uuid (or pattern)
        :param partition: partition of the pattern, empty for the <None> partition
        :return: translation pattern dictionary
        

        Schema: `GetTransPatternReq`: optional `returnedTags`; one of `uuid`, or (`pattern` + `routePartitionName`; optional `dialPlanName`, `routeFilterName`).
        """
        identifier = self._pattern_identifier(
            pattern, partition or routePartitionName, uuid
        )
        return self.client.getTransPattern(
            **identifier,
            returnedTags={
                "pattern": "",
                "description": "",
                "routePartitionName": "",
                "callingSearchSpaceName": "",
                "useCallingPartyPhoneMask": "",
                "patternUrgency": "",
                "provideOutsideDialtone": "",
                "prefixDigitsOut": "",
                "calledPartyTransformationMask": "",
                "callingPartyTransformationMask": "",
                "digitDiscardInstructionName": "",
                "callingPartyPrefixDigits": "",
            },
        )["return"]["transPattern"]

    def add_translation(
        self,
        pattern,
        partition,
        description="",
        usage="Translation",
        callingSearchSpaceName="",
        useCallingPartyPhoneMask="Off",
        patternUrgency="f",
        provideOutsideDialtone="f",
        prefixDigitsOut="",
        calledPartyTransformationMask="",
        callingPartyTransformationMask="",
        digitDiscardInstructionName="",
        callingPartyPrefixDigits="",
        blockEnable="f",
        routeNextHopByCgpn="f",
    ):
        """
        Add a translation pattern
        :param pattern: Translation pattern
        :param partition: Route Partition
        :param description: Description - optional
        :param usage: Usage
        :param callingSearchSpaceName: Calling Search Space - optional
        :param patternUrgency: Pattern Urgency - optional
        :param provideOutsideDialtone: Provide Outside Dial Tone - optional
        :param prefixDigitsOut: Prefix Digits Out - optional
        :param calledPartyTransformationMask: - optional
        :param callingPartyTransformationMask: - optional
        :param digitDiscardInstructionName: - optional
        :param callingPartyPrefixDigits: - optional
        :param blockEnable: - optional
        :param useCallingPartyPhoneMask: Off, On or Default - optional
        :param routeNextHopByCgpn: route next hop by calling party number - optional
        :return: result dictionary
        

        Schema: `transPattern` -> `XTransPattern`: `pattern` + `usage` + `routePartitionName`; optional `description`, `blockEnable`, `calledPartyTransformationMask`, `callingPartyTransformationMask`, `useCallingPartyPhoneMask`, `callingPartyPrefixDigits` and 24 more.
        """
        return self.client.addTransPattern(
            {
                "pattern": pattern,
                "description": description,
                "routePartitionName": partition,
                "usage": usage,
                "callingSearchSpaceName": callingSearchSpaceName,
                "useCallingPartyPhoneMask": useCallingPartyPhoneMask,
                "patternUrgency": patternUrgency,
                "provideOutsideDialtone": provideOutsideDialtone,
                "prefixDigitsOut": prefixDigitsOut,
                "calledPartyTransformationMask": calledPartyTransformationMask,
                "callingPartyTransformationMask": callingPartyTransformationMask,
                "digitDiscardInstructionName": digitDiscardInstructionName,
                "callingPartyPrefixDigits": callingPartyPrefixDigits,
                "blockEnable": blockEnable,
                "routeNextHopByCgpn": routeNextHopByCgpn,
            }
        )

    def delete_translation(self, pattern="", partition="", uuid=""):
        """
        Delete a translation pattern
        :param pattern: The pattern of the translation to delete (or uuid)
        :param partition: The name of the partition, empty for the <None> partition
        :param uuid: The uuid of the translation to delete (or pattern)
        :return: result dictionary
        

        Schema: `RemoveTransPatternReq`: one of `uuid`, or (`pattern` + `routePartitionName`; optional `dialPlanName`, `routeFilterName`).
        """
        return self.client.removeTransPattern(
            **self._pattern_identifier(pattern, partition, uuid)
        )

    def update_translation(
        self,
        pattern="",
        partition="",
        uuid="",
        newPattern="",
        description="",
        newRoutePartitionName="",
        callingSearchSpaceName="",
        useCallingPartyPhoneMask="",
        patternUrgency="",
        provideOutsideDialtone="",
        prefixDigitsOut="",
        calledPartyTransformationMask="",
        callingPartyTransformationMask="",
        digitDiscardInstructionName="",
        callingPartyPrefixDigits="",
        blockEnable="",
    ):
        """
        Update a translation pattern. Empty values are left unchanged.
        :param uuid: translation uuid (or pattern + partition)
        :param pattern: Translation pattern (or uuid)
        :param partition: Route Partition, empty for the <None> partition
        :param newPattern: new translation pattern - optional
        :param newRoutePartitionName: new partition - optional
        :param description: Description - optional
        :param callingSearchSpaceName: Calling Search Space - optional
        :param useCallingPartyPhoneMask: Off, On or Default - optional
        :param patternUrgency: Pattern Urgency - optional
        :param provideOutsideDialtone: Provide Outside Dial Tone - optional
        :param prefixDigitsOut: Prefix Digits Out - optional
        :param calledPartyTransformationMask: - optional
        :param callingPartyTransformationMask: - optional
        :param digitDiscardInstructionName: - optional
        :param callingPartyPrefixDigits: - optional
        :param blockEnable: - optional
        :return: result dictionary
        

        Schema: `UpdateTransPatternReq`: optional `newPattern`, `description`, `newRoutePartitionName`, `blockEnable`, `calledPartyTransformationMask`, `callingPartyTransformationMask` and 26 more; one of `uuid`, or (`pattern` + `routePartitionName`; optional `dialPlanName`, `routeFilterName`).
        """

        args = self._pattern_identifier(pattern, partition, uuid)
        if description != "":
            args["description"] = description
        if newPattern != "":
            args["newPattern"] = newPattern
        if newRoutePartitionName != "":
            args["newRoutePartitionName"] = newRoutePartitionName
        if callingSearchSpaceName != "":
            args["callingSearchSpaceName"] = callingSearchSpaceName
        if useCallingPartyPhoneMask != "":
            args["useCallingPartyPhoneMask"] = useCallingPartyPhoneMask
        if digitDiscardInstructionName != "":
            args["digitDiscardInstructionName"] = digitDiscardInstructionName
        if callingPartyTransformationMask != "":
            args["callingPartyTransformationMask"] = callingPartyTransformationMask
        if calledPartyTransformationMask != "":
            args["calledPartyTransformationMask"] = calledPartyTransformationMask
        if patternUrgency != "":
            args["patternUrgency"] = patternUrgency
        if provideOutsideDialtone != "":
            args["provideOutsideDialtone"] = provideOutsideDialtone
        if prefixDigitsOut != "":
            args["prefixDigitsOut"] = prefixDigitsOut
        if callingPartyPrefixDigits != "":
            args["callingPartyPrefixDigits"] = callingPartyPrefixDigits
        if blockEnable != "":
            args["blockEnable"] = blockEnable
        return self.client.updateTransPattern(**args)

    def list_route_plan(self, pattern=""):
        """
        List Route Plan
        :param pattern: Route Plan Contains Pattern
        :return: results dictionary
        

        Schema: `ListRoutePlanReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        return self.client.listRoutePlan(
            {"dnOrPattern": "%" + pattern + "%"},
            returnedTags={
                "dnOrPattern": "",
                "partition": "",
                "type": "",
                "routeDetail": "",
            },
        )["return"]["routePlan"]

    def list_route_plan_specific(self, pattern=""):
        """
        List Route Plan
        :param pattern: Route Plan Contains Pattern
        :return: list of route plan dictionaries, empty when nothing matches
        

        Schema: `ListRoutePlanReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listRoutePlan(
            {"dnOrPattern": pattern},
            returnedTags={
                "dnOrPattern": "",
                "partition": "",
                "type": "",
                "routeDetail": "",
            },
        )
        if result["return"] is None:
            return []
        return result["return"]["routePlan"]

    def get_called_party_xforms(self):
        """
        Get called party xforms
        :return: list of dictionaries, empty when nothing matches
        

        Schema: `ListCalledPartyTransformationPatternReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listCalledPartyTransformationPattern(
            {"pattern": "%"},
            returnedTags={"pattern": "", "description": "", "uuid": ""},
        )
        if result["return"] is None:
            return []
        return result["return"]["calledPartyTransformationPattern"]

    def _pattern_lookup(self, operation, args):
        """
        Complete a pattern-based identifier: when no uuid is given, default the optional
        dial plan and route filter keys to nil, as the AXL pattern choice requires them
        :param operation: AXL operation name
        :param args: method keyword arguments
        :return: args
        """
        fields = self._schema_fields(operation)
        if "uuid" not in args:
            for key in ("dialPlanName", "routeFilterName"):
                if key in fields:
                    args.setdefault(key, None)
        return args

    def get_called_party_xform(self, **args):
        """
        Get called party xform details
        :param pattern: transformation pattern (or uuid; name also works)
        :param partition: partition of the pattern (AXL name: routePartitionName)
        :param uuid: transformation uuid (or pattern + partition)
        :return: result dictionary
        

        Schema: `GetCalledPartyTransformationPatternReq`: optional `returnedTags`; one of `uuid`, or (`pattern` + `routePartitionName`; optional `dialPlanName`, `routeFilterName`).
        """
        args = self._pattern_lookup("getCalledPartyTransformationPattern", args)
        return self.client.getCalledPartyTransformationPattern(**args)["return"][
            "calledPartyTransformationPattern"
        ]

    def add_called_party_xform(
        self,
        pattern,
        description="",
        partition="",
        calledPartyPrefixDigits="",
        calledPartyTransformationMask="",
        digitDiscardInstructionName="",
        **args,
    ):
        """
        Add a called party transformation pattern
        :param pattern: pattern - required
        :param partition: partition, empty for the <None> partition
        :param description: transformation pattern description
        :param calledPartyPrefixDigits: prefix digits
        :param calledPartyTransformationMask: transformation mask
        :param digitDiscardInstructionName: digit discard instruction
        :param dialPlanName: optional
        :param routeFilterName: optional
        :param calledPartyNumberingPlan: optional
        :param calledPartyNumberType: optional
        :param mlppPreemptionDisabled: boolean, default false - optional
        :return: result dictionary
        

        Schema: `calledPartyTransformationPattern` -> `XCalledPartyTransformationPattern`: `pattern` + `routePartitionName`; optional `description`, `calledPartyTransformationMask`, `dialPlanName`, `digitDiscardInstructionName`, `routeFilterName`, `calledPartyPrefixDigits` and 3 more.
        """
        return self.client.addCalledPartyTransformationPattern(
            {
                "pattern": pattern,
                "description": description,
                "routePartitionName": partition or None,
                "calledPartyPrefixDigits": calledPartyPrefixDigits,
                "calledPartyTransformationMask": calledPartyTransformationMask,
                "digitDiscardInstructionName": digitDiscardInstructionName,
                **args,
            }
        )

    def delete_called_party_xform(self, **args):
        """
        Delete a called party transformation pattern
        :param uuid: The pattern uuid (or pattern + partition)
        :param pattern: The pattern of the transformation to delete
        :param partition: The name of the partition (AXL name: routePartitionName)
        :return: result dictionary
        

        Schema: `RemoveCalledPartyTransformationPatternReq`: one of `uuid`, or (`pattern` + `routePartitionName`; optional `dialPlanName`, `routeFilterName`).
        """
        args = self._pattern_lookup("removeCalledPartyTransformationPattern", args)
        return self.client.removeCalledPartyTransformationPattern(**args)

    def update_called_party_xform(self, **args):
        """
        Update a called party transformation
        :param uuid: transformation uuid (or pattern + partition)
        :param pattern: transformation pattern (or uuid)
        :param partition: partition of the pattern (AXL name: routePartitionName)
        :param newPattern: new pattern
        :param new_partition: new partition (AXL name: newRoutePartitionName)
        :param description: transformation pattern description
        :param calledPartyTransformationMask: transformation mask
        :param digitDiscardInstructionName: digit discard instruction
        :param calledPartyPrefixDigits: prefix digits
        :param calledPartyNumberingPlan: numbering plan
        :param calledPartyNumberType: number type
        :param mlppPreemptionDisabled: boolean, default false
        :return: result dictionary
        

        Schema: `UpdateCalledPartyTransformationPatternReq`: optional `newPattern`, `description`, `newRoutePartitionName`, `calledPartyTransformationMask`, `newDialPlanName`, `digitDiscardInstructionName` and 5 more; one of `uuid`, or (`pattern` + `routePartitionName`; optional `dialPlanName`, `routeFilterName`).
        """
        args = self._pattern_lookup("updateCalledPartyTransformationPattern", args)
        return self.client.updateCalledPartyTransformationPattern(**args)

    def get_calling_party_xforms(self):
        """
        Get calling party xforms
        :return: list of dictionaries, empty when nothing matches
        

        Schema: `ListCallingPartyTransformationPatternReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        return self.client.listCallingPartyTransformationPattern(
            {"pattern": "%"},
            returnedTags={"pattern": "", "description": "", "uuid": ""},
        )["return"]["callingPartyTransformationPattern"]

    def get_calling_party_xform(self, **args):
        """
        Get calling party xform details
        :param pattern: transformation pattern (or uuid; name also works)
        :param partition: partition of the pattern (AXL name: routePartitionName)
        :param uuid: transformation uuid (or pattern + partition)
        :return: result dictionary
        

        Schema: `GetCallingPartyTransformationPatternReq`: optional `returnedTags`; one of `uuid`, or (`pattern` + `routePartitionName`; optional `dialPlanName`, `routeFilterName`).
        """
        args = self._pattern_lookup("getCallingPartyTransformationPattern", args)
        return self.client.getCallingPartyTransformationPattern(**args)["return"][
            "callingPartyTransformationPattern"
        ]

    def add_calling_party_xform(
        self,
        pattern,
        description="",
        partition="",
        callingPartyPrefixDigits="",
        callingPartyTransformationMask="",
        digitDiscardInstructionName="",
        **args,
    ):
        """
        Add a calling party transformation pattern
        :param pattern: pattern - required
        :param partition: partition, empty for the <None> partition
        :param description: transformation pattern description
        :param callingPartyPrefixDigits: prefix digits
        :param callingPartyTransformationMask: transformation mask
        :param digitDiscardInstructionName: digit discard instruction
        :param dialPlanName: optional
        :param routeFilterName: optional
        :param callingPartyNumberingPlan: optional
        :param callingPartyNumberType: optional
        :param mlppPreemptionDisabled: boolean, default false - optional
        :return: result dictionary
        

        Schema: `callingPartyTransformationPattern` -> `XCallingPartyTransformationPattern`: `pattern` + `routePartitionName`; optional `description`, `callingPartyTransformationMask`, `useCallingPartyPhoneMask`, `dialPlanName`, `digitDiscardInstructionName`, `callingPartyPrefixDigits` and 5 more.
        """
        return self.client.addCallingPartyTransformationPattern(
            {
                "pattern": pattern,
                "description": description,
                "routePartitionName": partition or None,
                "callingPartyPrefixDigits": callingPartyPrefixDigits,
                "callingPartyTransformationMask": callingPartyTransformationMask,
                "digitDiscardInstructionName": digitDiscardInstructionName,
                **args,
            }
        )

    def delete_calling_party_xform(self, **args):
        """
        Delete a calling party transformation pattern
        :param uuid: The pattern uuid (or pattern + partition)
        :param pattern: The pattern of the transformation to delete
        :param partition: The name of the partition (AXL name: routePartitionName)
        :return: result dictionary
        

        Schema: `RemoveCallingPartyTransformationPatternReq`: one of `uuid`, or (`pattern` + `routePartitionName`; optional `dialPlanName`, `routeFilterName`).
        """
        args = self._pattern_lookup("removeCallingPartyTransformationPattern", args)
        return self.client.removeCallingPartyTransformationPattern(**args)

    def update_calling_party_xform(self, **args):
        """
        Update a calling party transformation
        :param uuid: transformation uuid (or pattern + partition)
        :param pattern: transformation pattern (or uuid)
        :param partition: partition of the pattern (AXL name: routePartitionName)
        :param newPattern: new pattern
        :param new_partition: new partition (AXL name: newRoutePartitionName)
        :param description: transformation pattern description
        :param callingPartyTransformationMask: transformation mask
        :param digitDiscardInstructionName: digit discard instruction
        :param callingPartyPrefixDigits: prefix digits
        :param callingPartyNumberingPlan: numbering plan
        :param callingPartyNumberType: number type
        :param useCallingPartyPhoneMask: Off, On or Default
        :param callingLinePresentationBit: Default, Allowed or Restricted
        :param mlppPreemptionDisabled: boolean, default false
        :return: result dictionary
        

        Schema: `UpdateCallingPartyTransformationPatternReq`: optional `newPattern`, `description`, `newRoutePartitionName`, `callingPartyTransformationMask`, `useCallingPartyPhoneMask`, `newDialPlanName` and 7 more; one of `uuid`, or (`pattern` + `routePartitionName`; optional `dialPlanName`, `routeFilterName`).
        """
        args = self._pattern_lookup("updateCallingPartyTransformationPattern", args)
        return self.client.updateCallingPartyTransformationPattern(**args)

    def get_sip_trunks(
        self, tagfilter={"name": "", "sipProfileName": "", "callingSearchSpaceName": ""}
    ):
        """
        Get SIP trunks
        :param tagfilter: AXL returned tags to include, e.g. {'name': '', 'sipProfileName': ''}
        :return: list of SIP trunk dictionaries
        

        Schema: `ListSipTrunkReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        return self.client.listSipTrunk({"name": "%"}, returnedTags=tagfilter)[
            "return"
        ]["sipTrunk"]

    def get_sip_trunk(self, **args):
        """
        Get sip trunk
        :param name: trunk name (or uuid)
        :param uuid: trunk uuid (or name)
        :return: result dictionary
        

        Schema: `GetSipTrunkReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getSipTrunk(**args)["return"]["sipTrunk"]

    def update_sip_trunk(self, **args):
        """
        Update a SIP Trunk (sipTrunkType can't be changed after creation)
        :param name: trunk name (or uuid)
        :param uuid: trunk uuid (or name)
        :param newName: new trunk name
        :param description: description
        :param css: calling search space (AXL name: callingSearchSpaceName)
        :param device_pool: device pool (AXL name: devicePoolName)
        :param location: location (AXL name: locationName)
        :param sip_profile: SIP profile (AXL name: sipProfileName)
        :param mtpRequired: boolean
        :param destinations: {'destination': [{'addressIpv4', 'port', 'sortOrder'}]}, max 16
        :return: result dictionary
        

        Schema: `UpdateSipTrunkReq`: optional `newName`, `description`, `callingSearchSpaceName`, `devicePoolName`, `commonDeviceConfigName`, `networkLocation` and 89 more.
        """
        return self.client.updateSipTrunk(**args)

    def delete_sip_trunk(self, **args):
        """
        Delete a SIP trunk
        :param name: trunk name (or uuid)
        :param uuid: trunk uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeSipTrunk(**args)

    def get_sip_security_profile(self, name="", uuid=""):
        """
        Get a SIP trunk security profile
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: SIP trunk security profile dictionary
        

        Schema: `GetSipTrunkSecurityProfileReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getSipTrunkSecurityProfile(
            **self._identify(name=name, uuid=uuid)
        )["return"]["sipTrunkSecurityProfile"]

    def get_sip_profile(self, name="", uuid=""):
        """
        Get a SIP profile
        :param name: profile name (or uuid)
        :param uuid: profile uuid (or name)
        :return: SIP profile dictionary
        

        Schema: `GetSipProfileReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getSipProfile(**self._identify(name=name, uuid=uuid))[
            "return"
        ]["sipProfile"]

    def add_sip_trunk(self, **args):
        """
        Add a SIP Trunk. Friendly names and AXL element names are both accepted;
        required elements not given use the schema defaults.
        :param name: trunk name - required
        :param description: description
        :param product: default 'SIP Trunk'
        :param dev_class: default 'Trunk' (AXL name: class)
        :param protocol: default 'SIP'
        :param protocol_side: default 'Network' (AXL name: protocolSide)
        :param css: calling search space (AXL name: callingSearchSpaceName)
        :param device_pool: device pool - required (AXL name: devicePoolName)
        :param location: location, default Hub_None (AXL name: locationName)
        :param security_profile: default 'Non Secure SIP Trunk Profile' (AXL name: securityProfileName)
        :param sip_profile: default 'Standard SIP Profile' (AXL name: sipProfileName)
        :param presenceGroupName: default 'Standard Presence group'
        :param destinations: {'destination': [{'addressIpv4', 'port', 'sortOrder'}]}, sortOrder required, max 16
        :param runOnEveryNode: boolean
        :return: result dictionary
        

        Schema: `sipTrunk` -> `XSipTrunk`: `name` + `product` + `class` + `protocol` + `protocolSide` + `devicePoolName` + `locationName` + `securityProfileName` + `sipProfileName` + `presenceGroupName` + `callingAndCalledPartyInfoFormat`; optional `description`, `callingSearchSpaceName`, `commonDeviceConfigName`, `networkLocation`, `mediaResourceListName`, `networkHoldMohAudioSourceId` and 84 more.
        """
        trunk = self._build_object(
            "addSipTrunk",
            "sipTrunk",
            args,
            defaults={
                "product": "SIP Trunk",
                "class": "Trunk",
                "protocol": "SIP",
                "protocolSide": "Network",
                "locationName": "Hub_None",
                "securityProfileName": "Non Secure SIP Trunk Profile",
                "sipProfileName": "Standard SIP Profile",
                "presenceGroupName": "Standard Presence group",
            },
        )
        return self.client.addSipTrunk(trunk)

    def list_process_nodes(self):
        """
        List the Unified CM call processing nodes
        :return: list of process node dictionaries with name
        

        Schema: `ListProcessNodeReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        return self.client.listProcessNode(
            {"name": "%", "processNodeRole": "CUCM Voice/Video"},
            returnedTags={"name": ""},
        )["return"]["processNode"]

    @staticmethod
    def _cm_group_members(members):
        """
        Convert a list of Unified CM names into the AXL members structure, leaving AXL dicts alone
        :param members: list of names in priority order, or {'member': [...]}
        :return: {'member': [{'callManagerName', 'priority'}]}
        """
        if isinstance(members, dict):
            return members
        return {
            "member": [
                {"callManagerName": name, "priority": priority}
                for priority, name in enumerate(members, start=1)
            ]
        }

    def add_call_manager_group(self, name, members):
        """
        Add call manager group
        :param name: name of cmg
        :param members: list of Unified CM names in priority order (at least one),
                        or {'member': [{'callManagerName', 'priority'}]}
        :return: result dictionary
        

        Schema: `callManagerGroup` -> `XCallManagerGroup`: `name` + `members`; optional `tftpDefault`.
        """
        return self.client.addCallManagerGroup(
            {"name": name, "members": self._cm_group_members(members)}
        )

    def get_call_manager_group(self, name="", uuid=""):
        """
        Get call manager group
        :param name: name of cmg (or uuid)
        :param uuid: uuid of cmg (or name)
        :return: call manager group dictionary
        

        Schema: `GetCallManagerGroupReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getCallManagerGroup(**self._identify(name=name, uuid=uuid))[
            "return"
        ]["callManagerGroup"]

    def get_call_manager_groups(self):
        """
        Get call manager groups
        :return: list of call manager group dictionaries with name, empty when nothing matches
        

        Schema: `ListCallManagerGroupReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        result = self.client.listCallManagerGroup(
            {"name": "%"}, returnedTags={"name": ""}
        )
        if result["return"] is None:
            return []
        return result["return"]["callManagerGroup"]

    def update_call_manager_group(self, **args):
        """
        Update call manager group
        :param name: name of cmg (or uuid)
        :param uuid: uuid of cmg (or name)
        :param newName: new name
        :param tftpDefault: boolean
        :param members: replaces all members: list of Unified CM names in priority order,
                        or {'member': [{'callManagerName', 'priority'}]}
        :param addMembers: members to add, {'member': [...]} (instead of members)
        :param removeMembers: members to remove, {'member': [...]} (instead of members)
        :return: result dictionary
        

        Schema: `UpdateCallManagerGroupReq`: optional `newName`, `tftpDefault`, optional choice of (optional `removeMembers`, `addMembers`), or `members`.
        """
        if "members" in args:
            args["members"] = self._cm_group_members(args["members"])
        return self.client.updateCallManagerGroup(**args)

    def delete_call_manager_group(self, name="", uuid=""):
        """
        Delete call manager group
        :param name: name of cmg (or uuid)
        :param uuid: uuid of cmg (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeCallManagerGroup(**self._identify(name=name, uuid=uuid))

    # Hunt Pilot Methods
    def get_hunt_pilots(
        self,
        tagfilter={
            "pattern": "",
            "description": "",
            "routePartitionName": "",
        },
    ):
        """
        Get hunt pilots
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of dictionaries, empty when nothing matches
        

        Schema: `ListHuntPilotReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        response = self.client.listHuntPilot(
            {"pattern": "%"},
            returnedTags=tagfilter,
        )["return"]
        if response:
            return response["huntPilot"]
        else:
            return []

    def get_hunt_pilot(self, **args):
        """
        Get hunt pilot details
        :param pattern: hunt pilot pattern (or uuid; name also works)
        :param partition: partition of the pattern (AXL name: routePartitionName)
        :param uuid: hunt pilot uuid (or pattern)
        :return: result dictionary
        

        Schema: `GetHuntPilotReq`: optional `returnedTags`; one of `uuid`, or (`pattern`; optional `routePartitionName`).
        """
        return self.client.getHuntPilot(**args)["return"]["huntPilot"]

    def add_hunt_pilot(self, **args):
        """
        Add a Hunt Pilot
        :param pattern: pattern - required
        :param hunt_list: hunt list name - required (AXL name: huntListName)
        :param partition: partition - optional (AXL name: routePartitionName)
        :param description: Hunt Pilot pattern description
        :param useCallingPartyPhoneMask: "Off", "On" or "Default" (default)
        :param blockEnable: boolean, default false
        :return: result dictionary
        

        Schema: `huntPilot` -> `XHuntPilot`: `pattern` + `blockEnable` + `useCallingPartyPhoneMask` + `huntListName`; optional `description`, `routePartitionName`, `calledPartyTransformationMask`, `callingPartyTransformationMask`, `callingPartyPrefixDigits`, `dialPlanName` and 26 more.
        """
        pilot = self._build_object(
            "addHuntPilot", "huntPilot", args, defaults={"blockEnable": False}
        )
        return self.client.addHuntPilot(pilot)

    def update_hunt_pilot(self, **args):
        """
        Update a Hunt Pilot
        :param uuid: hunt pilot uuid (or pattern)
        :param pattern: hunt pilot pattern (or uuid)
        :param partition: partition of the pattern - optional (AXL name: routePartitionName)
        :param newPattern: new pattern
        :param new_partition: new partition (AXL name: newRoutePartitionName)
        :param description: Hunt Pilot pattern description
        :param useCallingPartyPhoneMask: "Off", "On" or "Default"
        :param blockEnable: boolean
        :param hunt_list: hunt list name (AXL name: huntListName)
        :return: result dictionary
        

        Schema: `UpdateHuntPilotReq`: optional `newPattern`, `description`, `newRoutePartitionName`, `blockEnable`, `calledPartyTransformationMask`, `callingPartyTransformationMask` and 30 more; one of `uuid`, or (`pattern`; optional `routePartitionName`).
        """
        return self.client.updateHuntPilot(**args)

    def delete_hunt_pilot(self, **args):
        """
        Delete a Hunt Pilot
        :param uuid: The hunt pilot uuid (or pattern)
        :param pattern: The pattern of the hunt pilot to delete
        :param partition: The name of the partition (AXL name: routePartitionName)
        :return: result dictionary
        

        Schema: `RemoveHuntPilotReq`: one of `uuid`, or (`pattern`; optional `routePartitionName`).
        """
        return self.client.removeHuntPilot(**args)

    # Hunt List Methods
    def get_hunt_lists(
        self,
        tagfilter={
            "name": "",
            "callManagerGroupName": "",
            "routeListEnabled": "",
            "voiceMailUsage": "",
            "description": "",
        },
    ):
        """
        Get hunt lists
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of dictionaries, empty when nothing matches
        

        Schema: `ListHuntListReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        response = self.client.listHuntList(
            {"name": "%"},
            returnedTags=tagfilter,
        )["return"]
        if response:
            return response["huntList"]
        else:
            return []

    def get_hunt_list(self, **args):
        """
        Get hunt list details
        :param name: hunt list name (or uuid)
        :param uuid: hunt list uuid (or name)
        :return: result dictionary
        

        Schema: `GetHuntListReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getHuntList(**args)["return"]["huntList"]

    def add_hunt_list(self, **args):
        """
        Add a Hunt list
        :param name: - required
        :param callManagerGroup: Unified CM group - required (AXL name: callManagerGroupName)
        :param description: str
        :param routeListEnabled: bool
        :param voiceMailUsage: bool
        :param members: {'member': [{'lineGroupName', 'selectionOrder'}]}
        :return: result dictionary
        

        Schema: `huntList` -> `XHuntList`: `callManagerGroupName` + `name`; optional `description`, `routeListEnabled`, `voiceMailUsage`, `members`.
        """
        hunt_list = self._build_object("addHuntList", "huntList", args)
        return self.client.addHuntList(hunt_list)

    def update_hunt_list(self, **args):
        """
        Update a Hunt List
        :param name: hunt list name (or uuid)
        :param uuid: hunt list uuid (or name)
        :param newName: new name
        :param callManagerGroup: Unified CM group (AXL name: callManagerGroupName)
        :param description: str
        :param routeListEnabled: bool
        :param voiceMailUsage: bool
        :param members: replaces all members: {'member': [{'lineGroupName', 'selectionOrder'}]}
        :param addMembers: members to add, same shape as members (instead of members)
        :param removeMembers: members to remove, same shape as members (instead of members)
        :return: result dictionary
        

        Schema: `UpdateHuntListReq`: optional `description`, `callManagerGroupName`, `routeListEnabled`, `voiceMailUsage`, optional choice of (optional `removeMembers`, `addMembers`), or `members`, `newName`.
        """
        return self.client.updateHuntList(**args)

    def delete_hunt_list(self, **args):
        """
        Delete a Hunt List
        :param name: hunt list name (or uuid)
        :param uuid: hunt list uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeHuntList(**args)

    # Line Group Methods
    def get_line_groups(
        self,
        tagfilter={
            "name": "",
            "distributionAlgorithm": "",
            "rnaReversionTimeOut": "",
            "huntAlgorithmNoAnswer": "",
            "huntAlgorithmBusy": "",
            "huntAlgorithmNotAvailable": "",
            "autoLogOffHunt": "",
        },
    ):
        """
        Get Line Groups
        :param tagfilter: AXL returned tags to include, e.g. {'name': ''}
        :return: list of dictionaries, empty when nothing matches
        

        Schema: `ListLineGroupReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        response = self.client.listLineGroup(
            {"name": "%"},
            returnedTags=tagfilter,
        )["return"]
        if response:
            return response["lineGroup"]
        else:
            return []

    def get_line_group(self, **args):
        """
        Get line group details
        :param name: line group name (or uuid)
        :param uuid: line group uuid (or name)
        :return: result dictionary
        

        Schema: `GetLineGroupReq`: optional `returnedTags`; one of `name`, or `uuid`.
        """
        return self.client.getLineGroup(**args)["return"]["lineGroup"]

    def add_line_group(self, **args):
        """
        Add a Line Group. Settings not given use the schema defaults shown.
        :param name: - required
        :param distributionAlgorithm: Top Down, Circular, Longest Idle Time (default) or Broadcast
        :param rnaReversionTimeOut: ring no answer reversion timeout in seconds, default 10
        :param huntAlgorithmNoAnswer: default "Try next member; then, try next group in Hunt List"
        :param huntAlgorithmBusy: default "Try next member; then, try next group in Hunt List"
        :param huntAlgorithmNotAvailable: default "Try next member; then, try next group in Hunt List"
        :param members: {'member': [{'lineSelectionOrder', 'directoryNumber': {'pattern', 'routePartitionName'}}]}
        :return: result dictionary
        

        Schema: `lineGroup` -> `XLineGroup`: `distributionAlgorithm` + `rnaReversionTimeOut` + `huntAlgorithmNoAnswer` + `huntAlgorithmBusy` + `huntAlgorithmNotAvailable` + `name`; optional `members`, `autoLogOffHunt`.
        """
        line_group = self._build_object("addLineGroup", "lineGroup", args)
        return self.client.addLineGroup(line_group)

    def update_line_group(self, **args):
        """
        Update a Line Group
        :param name: line group name (or uuid)
        :param uuid: line group uuid (or name)
        :param newName: new name
        :param distributionAlgorithm: Top Down, Circular, Longest Idle Time or Broadcast
        :param rnaReversionTimeOut: ring no answer reversion timeout in seconds
        :param huntAlgorithmNoAnswer: e.g. "Try next member; then, try next group in Hunt List"
        :param huntAlgorithmBusy: e.g. "Try next member; then, try next group in Hunt List"
        :param huntAlgorithmNotAvailable: e.g. "Try next member; then, try next group in Hunt List"
        :param autoLogOffHunt: boolean
        :param members: replaces all members: {'member': [{'lineSelectionOrder', 'directoryNumber': {'pattern', 'routePartitionName'}}]}
        :param addMembers: members to add, same shape as members (instead of members)
        :param removeMembers: members to remove, same shape as members (instead of members)
        :return: result dictionary
        

        Schema: `UpdateLineGroupReq`: optional `distributionAlgorithm`, `rnaReversionTimeOut`, `huntAlgorithmNoAnswer`, `huntAlgorithmBusy`, `huntAlgorithmNotAvailable`, optional choice of (optional `removeMembers`, `addMembers`), or `members` and 2 more.
        """
        return self.client.updateLineGroup(**args)

    def delete_line_group(self, **args):
        """
        Delete a Line Group
        :param name: line group name (or uuid)
        :param uuid: line group uuid (or name)
        :return: result dictionary
        

        Schema: `NameAndGUIDRequest`: one of `name`, or `uuid`.
        """
        return self.client.removeLineGroup(**args)

    # Call Pickup Group Methods
    def get_call_pickup_groups(
        self,
        tagfilter={
            "name": "",
            "pattern": "",
            "description": "",
            "usage": "",
            "routePartitionName": "",
            "pickupNotification": "",
            "pickupNotificationTimer": "",
            "callInfoForPickupNotification": "",
        },
    ):
        """
        Get Call Pickup Groups
        :param tagfilter: AXL returned tags to include, e.g. {'name': '', 'pattern': ''}
        :return: list of call pickup group dictionaries
        

        Schema: `ListCallPickupGroupReq`: `searchCriteria` + `returnedTags`; optional `skip`, `first`.
        """
        response = self.client.listCallPickupGroup(
            {"pattern": "%"},
            returnedTags=tagfilter,
        )["return"]
        if response:
            return response["callPickupGroup"]
        else:
            return []

    def get_call_pickup_group(self, **args):
        """
        Get call pickup group details. Identify by uuid, name, or pattern + partition.
        :param name: call pickup group name
        :param pattern: call pickup group number
        :param partition: partition of the pattern (AXL name: routePartitionName)
        :param uuid: call pickup group uuid
        :return: result dictionary
        

        Schema: `GetCallPickupGroupReq`: optional `returnedTags`; one of `uuid`, or `name`, or (`pattern`; optional `routePartitionName`).
        """
        return self.client.getCallPickupGroup(**args)["return"]["callPickupGroup"]

    def add_call_pickup_group(self, **args):
        """
        Add a Call Pickup Group
        :param name: - required
        :param pattern: - required
        :param description:
        :param partition: partition of the pattern (AXL name: routePartitionName)
        :param pickupNotification:
        :param pickupNotificationTimer:
        :param callInfoForPickupNotification:
        :param members: {'member': [{'priority': 1, 'pickupGroupName': name}]}; priority starts at 1
                        and the group can't list itself
        :return: result dictionary
        

        Schema: `callPickupGroup` -> `XCallPickupGroup`: `pattern` + `name`; optional `description`, `routePartitionName`, `members`, `pickupNotification`, `pickupNotificationTimer`, `callInfoForPickupNotification`.
        """
        args.pop("usage", None)
        return self.client.addCallPickupGroup({**args})

    def update_call_pickup_group(self, **args):
        """
        Update a Call Pickup Group. Identify by uuid, name, or pattern + partition.
        :param name: call pickup group name
        :param uuid: call pickup group uuid
        :param pattern: call pickup group number
        :param partition: partition of the pattern (AXL name: routePartitionName)
        :param newName: new name
        :param newPattern: new number
        :param new_partition: new partition (AXL name: newRoutePartitionName)
        :param description:
        :param pickupNotification:
        :param pickupNotificationTimer:
        :param callInfoForPickupNotification:
        :param members: replaces all members: {'member': [{'priority', 'pickupGroupName'}]}
        :param addMembers: members to add, same shape as members (instead of members)
        :param removeMembers: members to remove, same shape as members (instead of members)
        :return: result dictionary
        

        Schema: `UpdateCallPickupGroupReq`: optional `newPattern`, `description`, `newRoutePartitionName`, optional choice of (optional `removeMembers`, `addMembers`), or `members`, `pickupNotification`, `pickupNotificationTimer` and 2 more; one of `uuid`, or `name`, or (`pattern`; optional `routePartitionName`).
        """
        args.pop("usage", None)
        return self.client.updateCallPickupGroup(**args)

    def delete_call_pickup_group(self, **args):
        """
        Delete a Call Pickup Group. Identify by uuid, name, or pattern + partition.
        :param name: call pickup group name
        :param uuid: call pickup group uuid
        :param pattern: call pickup group number
        :param partition: partition of the pattern (AXL name: routePartitionName)
        :return: result dictionary
        

        Schema: `RemoveCallPickupGroupReq`: one of `uuid`, or `name`, or (`pattern`; optional `routePartitionName`).
        """
        return self.client.removeCallPickupGroup(**args)
