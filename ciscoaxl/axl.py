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
from zeep import Client, Settings, Plugin
from zeep.transports import Transport
from zeep.cache import SqliteCache
from zeep.plugins import HistoryPlugin
from zeep.exceptions import Fault

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class axl(object):
    """
    The AXL class sets up the connection to the call manager with methods for configuring UCM.
    Tested with environment of;
    Python 3.6
    """

    def __init__(self, username, password, cucm, cucm_version, cucm_port=8443, strict_ssl=False):
        """
        :param username: axl username
        :param password: axl password
        :param cucm: UCM IP address
        :param cucm_version: UCM version
        :param cucm_port: UCM TCP port
        :param strict_ssl: do not work around an SSL failure, default False

        example usage:
        >>> from axl import AXL
        >>> ucm = AXL('axl_user', 'axl_pass', '192.168.200.10')
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
        self.client = axl_client.create_service(
            "{http://www.cisco.com/AXLAPIService/}AXLAPIBinding",
            f"https://{cucm}:{cucm_port}/axl/",
        )

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
        :param mini: return a list of tuples of location details
        :return: A list of dictionary's
        """
        try:
            return self.client.listLocation({"name": "%"}, returnedTags=tagfilter,)[
                "return"
            ]["location"]
        except Fault as e:
            return e

    def run_sql_query(self, query):
        result = {"num_rows": 0, "query": query}

        try:
            sql_result = self.client.executeSQLQuery(sql=query)
        except Exception as fault:
            sql_result = None
            self.last_exception = fault

        num_rows = 0
        result_rows = []

        if sql_result is not None:
            if sql_result["return"] is not None:
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
        """
        try:
            return self.client.executeSQLQuery(query)["return"]
        except Fault as e:
            return e

    def sql_update(self, query):
        """
        Execute SQL update
        :param query: SQL Update to execute
        :return: result dictionary
        """
        try:
            return self.client.executeSQLUpdate(query)["return"]
        except Fault as e:
            return e

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
        """
        try:
            return self.client.listLdapDirectory(
                {"name": "%"},
                returnedTags=tagfilter,
            )["return"]["ldapDirectory"]
        except Fault as e:
            return e

    def do_ldap_sync(self, uuid):
        """
        Do LDAP Sync
        :param uuid: uuid
        :return: result dictionary
        """
        try:
            return self.client.doLdapSync(uuid=uuid, sync=True)
        except Fault as e:
            return e

    def do_change_dnd_status(self, **args):
        """
        Do Change DND Status
        :param userID:
        :param status:
        :return: result dictionary
        """
        try:
            return self.client.doChangeDNDStatus(**args)
        except Fault as e:
            return e

    def do_device_login(self, **args):
        """
        Do Device Login
        :param deviceName:
        :param userId:
        :param profileName:
        :return: result dictionary
        """
        try:
            return self.client.doDeviceLogin(**args)
        except Fault as e:
            return e

    def do_device_logout(self, **args):
        """
        Do Device Logout
        :param device:
        :param userId:
        :return: result dictionary
        """
        try:
            return self.client.doDeviceLogout(**args)
        except Fault as e:
            return e

    def do_device_reset(self, name="", uuid=""):
        """
        Do Device Reset
        :param name: device name
        :param uuid: device uuid
        :return: result dictionary
        """
        if name != "" and uuid == "":
            try:
                return self.client.doDeviceReset(deviceName=name, isHardReset=True)
            except Fault as e:
                return e
        elif name == "" and uuid != "":
            try:
                return self.client.doDeviceReset(uuid=uuid, isHardReset=True)
            except Fault as e:
                return e

    def reset_sip_trunk(self, name="", uuid=""):
        """
        Reset SIP Trunk
        :param name: device name
        :param uuid: device uuid
        :return: result dictionary
        """
        if name != "" and uuid == "":
            try:
                return self.client.resetSipTrunk(name=name)
            except Fault as e:
                return e
        elif name == "" and uuid != "":
            try:
                return self.client.resetSipTrunk(uuid=uuid)
            except Fault as e:
                return e

    def get_location(self, **args):
        """
        Get device pool parameters
        :param name: location name
        :param uuid: location uuid
        :return: result dictionary
        """
        try:
            return self.client.getLocation(**args)
        except Fault as e:
            return e

    def add_location(
        self,
        name,
        kbits=512,
        video_kbits=-1,
        within_audio_bw=512,
        within_video_bw=-1,
        within_immersive_kbits=-1,
    ):
        """
        Add a location
        :param name: Name of the location to add
        :param cucm_version: ucm version
        :param kbits: ucm 8.5
        :param video_kbits: ucm 8.5
        :param within_audio_bw: ucm 10
        :param within_video_bw: ucm 10
        :param within_immersive_kbits: ucm 10
        :return: result dictionary
        """
        if (
            self.cucm_version == "8.6"
            or self.cucm_version == "9.0"
            or self.cucm_version == "9.5"
            or self.cucm_version == "10.0"
        ):
            try:
                return self.client.addLocation(
                    {
                        "name": name,
                        # CUCM 8.6
                        "kbits": kbits,
                        "videoKbits": video_kbits,
                    }
                )
            except Fault as e:
                return e
        else:
            try:
                betweenLocations = []
                betweenLocation = {}
                RLocationBetween = {}
                RLocationBetween["locationName"] = "Hub_None"
                RLocationBetween["weight"] = 0
                RLocationBetween["audioBandwidth"] = within_audio_bw
                RLocationBetween["videoBandwidth"] = within_video_bw
                RLocationBetween["immersiveBandwidth"] = within_immersive_kbits
                betweenLocation["betweenLocation"] = RLocationBetween
                betweenLocations.append(betweenLocation)

                return self.client.addLocation(
                    {
                        "name": name,
                        # CUCM 10.6
                        "withinAudioBandwidth": within_audio_bw,
                        "withinVideoBandwidth": within_video_bw,
                        "withinImmersiveKbits": within_immersive_kbits,
                        "betweenLocations": betweenLocations,
                    }
                )
            except Fault as e:
                return e

    def delete_location(self, **args):
        """
        Delete a location
        :param name: The name of the location to delete
        :param uuid: The uuid of the location to delete
        :return: result dictionary
        """
        try:
            return self.client.removeLocation(**args)
        except Fault as e:
            return e

    def update_location(self, **args):
        """
        Update a Location
        :param name:
        :param uuid:
        :param newName:
        :param withinAudioBandwidth:
        :param withinVideoBandwidth:
        :param withImmersiveKbits:
        :param betweenLocations:
        :return:
        """
        try:
            return self.client.updateLocation(**args)
        except Fault as e:
            return e

    def get_regions(self, tagfilter={"uuid": "", "name": ""}):
        """
        Get region details
        :param mini: return a list of tuples of region details
        :return: A list of dictionary's
        """
        try:
            return self.client.listRegion({"name": "%"}, returnedTags=tagfilter)[
                "return"
            ]["region"]
        except Fault as e:
            return e

    def get_region(self, **args):
        """
        Get region information
        :param name: Region name
        :return: result dictionary
        """
        try:
            return self.client.getRegion(**args)["return"]["region"]
        except Fault as e:
            return e

    def add_region(self, name):
        """
        Add a region
        :param name: Name of the region to add
        :return: result dictionary
        """
        try:
            return self.client.addRegion({"name": name})
        except Fault as e:
            return e

    def update_region(self, name="", newName="", moh_region=""):
        """
        Update region and assign region to all other regions
        :param name:
        :param uuid:
        :param moh_region:
        :return:
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
        try:
            return self.client.updateRegion(
                name=name,
                newName=newName,
                relatedRegions={"relatedRegion": region_list},
            )
        except Fault as e:
            return e

    def delete_region(self, **args):
        """
        Delete a location
        :param name: The name of the region to delete
        :param uuid: The uuid of the region to delete
        :return: result dictionary
        """
        try:
            return self.client.removeRegion(**args)
        except Fault as e:
            return e

    def get_srsts(self, tagfilter={"uuid": ""}):
        """
        Get all SRST details
        :param mini: return a list of tuples of SRST details
        :return: A list of dictionary's
        """
        try:
            return self.client.listSrst({"name": "%"}, returnedTags=tagfilter)[
                "return"
            ]["srst"]
        except Fault as e:
            return e

    def get_srst(self, **args):
        """
        Get SRST information
        :param name: SRST name
        :return: result dictionary
        """
        try:
            return self.client.getSrst(**args)["return"]["srst"]
        except Fault as e:
            return e

    def add_srst(self, name, ip_address, port=2000, sip_port=5060):
        """
        Add SRST
        :param name: SRST name
        :param ip_address: SRST ip address
        :param port: SRST port
        :param sip_port: SIP port
        :return: result dictionary
        """
        try:
            return self.client.addSrst(
                {
                    "name": name,
                    "port": port,
                    "ipAddress": ip_address,
                    "SipPort": sip_port,
                }
            )
        except Fault as e:
            return e

    def delete_srst(self, name):
        """
        Delete a SRST
        :param name: The name of the SRST to delete
        :return: result dictionary
        """
        try:
            return self.client.removeSrst(name=name)
        except Fault as e:
            return e

    def update_srst(self, name, newName=""):
        """
        Update a SRST
        :param srst: The name of the SRST to update
        :param newName: The new name of the SRST
        :return: result dictionary
        """
        try:
            return self.client.updateSrst(name=name, newName=newName)
        except Fault as e:
            return e

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
        :param mini: return a list of tuples of device pool info
        :return: a list of dictionary's of device pools information
        """
        try:
            return self.client.listDevicePool({"name": "%"}, returnedTags=tagfilter,)[
                "return"
            ]["devicePool"]
        except Fault as e:
            return e

    def get_device_pool(self, **args):
        """
        Get device pool parameters
        :param name: device pool name
        :return: result dictionary
        """
        try:
            return self.client.getDevicePool(**args)["return"]["devicePool"]
        except Fault as e:
            return e

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
    ):

        """
        Add a device pool
        :param device_pool: Device pool name
        :param date_time_group: Date time group name
        :param region: Region name
        :param location: Location name
        :param route_group: Route group name
        :param media_resource_group_list: Media resource group list name
        :param srst: SRST name
        :param cm_group: CM Group name
        :param network_locale: Network locale name
        :return: result dictionary
        """
        try:
            return self.client.addDevicePool(
                {
                    "name": name,
                    "dateTimeSettingName": date_time_group,  # update to state timezone
                    "regionName": region,
                    "locationName": location,
                    "localRouteGroup": {
                        "name": "Standard Local Route Group",
                        "value": route_group,
                    },
                    "mediaResourceListName": media_resource_group_list,
                    "srstName": srst,
                    "callManagerGroupName": cm_group,
                    "networkLocale": network_locale,
                }
            )
        except Fault as e:
            return e

    def update_device_pool(self, **args):
        """
        Update a device pools route group and media resource group list
        :param name:
        :param uuid:
        :param newName:
        :param mediaResourceGroupListName:
        :param dateTimeSettingName:
        :param callManagerGroupName:
        :param regionName:
        :param locationName:
        :param networkLocale:
        :param srstName:
        :param localRouteGroup:
        :param elinGroup:
        :param media_resource_group_list:
        :return:
        """
        try:
            return self.client.updateDevicePool(**args)
        except Fault as e:
            return e

    def delete_device_pool(self, **args):
        """
        Delete a Device pool
        :param device_pool: The name of the Device pool to delete
        :return: result dictionary
        """
        try:
            return self.client.removeDevicePool(**args)
        except Fault as e:
            return e

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
        :param mini: List of tuples of conference bridge details
        :return: results dictionary
        """
        try:
            return self.client.listConferenceBridge(
                {"name": "%"},
                returnedTags=tagfilter,
            )["return"]["conferenceBridge"]
        except Fault as e:
            return e

    def get_conference_bridge(self, **args):
        """
        Get conference bridge parameters
        :param name: conference bridge name
        :return: result dictionary
        """
        try:
            return self.client.getConferenceBridge(**args)["return"]["conferenceBridge"]
        except Fault as e:
            return e

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
        """
        try:
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
        except Fault as e:
            return e

    def update_conference_bridge(self, **args):
        """
        Update a conference bridge
        :param name: Conference bridge name
        :param newName: New Conference bridge name
        :param description: Conference bridge description
        :param device_pool: Device pool name
        :param location: Location name
        :param product: Conference bridge type
        :param security_profile: Conference bridge security type
        :return: result dictionary
        """
        try:
            return self.client.updateConferenceBridge(**args)
        except Fault as e:
            return e

    def delete_conference_bridge(self, name):
        """
        Delete a Conference bridge
        :param name: The name of the Conference bridge to delete
        :return: result dictionary
        """
        try:
            return self.client.removeConferenceBridge(name=name)
        except Fault as e:
            return e

    def get_transcoders(
        self, tagfilter={"name": "", "description": "", "devicePoolName": ""}
    ):
        """
        Get transcoders
        :param mini: List of tuples of transcoder details
        :return: results dictionary
        """
        try:
            return self.client.listTranscoder({"name": "%"}, returnedTags=tagfilter,)[
                "return"
            ]["transcoder"]
        except Fault as e:
            return e

    def get_transcoder(self, **args):
        """
        Get conference bridge parameters
        :param name: transcoder name
        :return: result dictionary
        """
        try:
            return self.client.getTranscoder(**args)["return"]["transcoder"]
        except Fault as e:
            return e

    def add_transcoder(
        self,
        name,
        description="",
        device_pool="Default",
        product="Cisco IOS Enhanced Media Termination Point",
    ):
        """
        Add a transcoder
        :param transcoder: Transcoder name
        :param description: Transcoder description
        :param device_pool: Transcoder device pool
        :param product: Trancoder product
        :return: result dictionary
        """
        try:
            return self.client.addTranscoder(
                {
                    "name": name,
                    "description": description,
                    "devicePoolName": device_pool,
                    "product": product,
                }
            )
        except Fault as e:
            return e

    def update_transcoder(self, **args):
        """
        Add a transcoder
        :param name: Transcoder name
        :param newName: New Transcoder name
        :param description: Transcoder description
        :param device_pool: Transcoder device pool
        :param product: Trancoder product
        :return: result dictionary
        """
        try:
            return self.client.updateTranscoder(**args)
        except Fault as e:
            return e

    def delete_transcoder(self, name):
        """
        Delete a Transcoder
        :param name: The name of the Transcoder to delete
        :return: result dictionary
        """
        try:
            return self.client.removeTranscoder(name=name)
        except Fault as e:
            return e

    def get_mtps(self, tagfilter={"name": "", "description": "", "devicePoolName": ""}):
        """
        Get mtps
        :param mini: List of tuples of transcoder details
        :return: results dictionary
        """
        try:
            return self.client.listMtp({"name": "%"}, returnedTags=tagfilter,)[
                "return"
            ]["mtp"]
        except Fault as e:
            return e

    def get_mtp(self, **args):
        """
        Get mtp parameters
        :param name: transcoder name
        :return: result dictionary
        """
        try:
            return self.client.getMtp(**args)["return"]["mtp"]
        except Fault as e:
            return e

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
        """
        try:
            return self.client.addMtp(
                {
                    "name": name,
                    "description": description,
                    "devicePoolName": device_pool,
                    "mtpType": mtpType,
                }
            )
        except Fault as e:
            return e

    def update_mtp(self, **args):
        """
        Update an MTP
        :param name: MTP name
        :param newName: New MTP name
        :param description: MTP description
        :param device_pool: MTP device pool
        :param mtpType: MTP Type
        :return: result dictionary
        """
        try:
            return self.client.updateMtp(**args)
        except Fault as e:
            return e

    def delete_mtp(self, name):
        """
        Delete an MTP
        :param name: The name of the Transcoder to delete
        :return: result dictionary
        """
        try:
            return self.client.removeMtp(name=name)
        except Fault as e:
            return e

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
        :param mini: List of tuples of H323 Gateway details
        :return: results dictionary
        """
        try:
            return self.client.listH323Gateway({"name": "%"}, returnedTags=tagfilter,)[
                "return"
            ]["h323Gateway"]
        except Fault as e:
            return e

    def get_h323_gateway(self, **args):
        """
        Get H323 Gateway parameters
        :param name: H323 Gateway name
        :return: result dictionary
        """
        try:
            return self.client.getH323Gateway(**args)["return"]["h323Gateway"]
        except Fault as e:
            return e

    def add_h323_gateway(self, **args):
        """
        Add H323 gateway
        :param h323_gateway:
        :param description:
        :param device_pool:
        :param location:
        :param media_resource_group_list: Media resource group list name
        :param prefix_dn:
        :param sig_digits: Significant digits, 99 = ALL
        :param css:
        :param aar_css:
        :param aar_neighborhood:
        :param product:
        :param protocol:
        :param protocol_side:
        :param pstn_access:
        :param redirect_in_num_ie:
        :param redirect_out_num_ie:
        :param cld_party_ie_num_type:
        :param clng_party_ie_num_type:
        :param clng_party_nat_pre:
        :param clng_party_inat_prefix:
        :param clng_party_unknown_prefix:
        :param clng_party_sub_prefix:
        :param clng_party_nat_strip_digits:
        :param clng_party_inat_strip_digits:
        :param clng_party_unknown_strip_digits:
        :param clng_party_sub_strip_digits:
        :param clng_party_nat_trans_css:
        :param clng_party_inat_trans_css:
        :param clng_party_unknown_trans_css:
        :param clng_party_sub_trans_css:
        :return:
        """
        try:
            return self.client.addH323Gateway(**args)
        except Fault as e:
            return e

    def update_h323_gateway(self, **args):
        """

        :param name:
        :return:
        """
        try:
            return self.client.updateH323Gateway(**args)
        except Fault as e:
            return e

    def delete_h323_gateway(self, name):
        """
        Delete a H323 gateway
        :param name: The name of the H323 gateway to delete
        :return: result dictionary
        """
        try:
            return self.client.removeH323Gateway(name=name)
        except Fault as e:
            return e

    def get_route_groups(self, tagfilter={"name": "", "distributionAlgorithm": ""}):
        """
        Get route groups
        :param mini: return a list of tuples of route group details
        :return: A list of dictionary's
        """
        try:
            return self.client.listRouteGroup({"name": "%"}, returnedTags=tagfilter)[
                "return"
            ]["routeGroup"]
        except Fault as e:
            return e

    def get_route_group(self, **args):
        """
        Get route group
        :param name: route group name
        :param uuid: route group uuid
        :return: result dictionary
        """
        try:
            return self.client.getRouteGroup(**args)["return"]["routeGroup"]
        except Fault as e:
            return e

    def add_route_group(self, name, distribution_algorithm="Top Down", members=[]):
        """
        Add a route group
        :param name: Route group name
        :param distribution_algorithm: Top Down/Circular
        :param members: A list of devices to add (must already exist DUH!)
        """
        req = {
            "name": name,
            "distributionAlgorithm": distribution_algorithm,
            "members": {"member": []},
        }

        if members:
            [
                req["members"]["member"].append(
                    {
                        "deviceName": i,
                        "deviceSelectionOrder": members.index(i) + 1,
                        "port": 0,
                    }
                )
                for i in members
            ]

        try:
            return self.client.addRouteGroup(req)
        except Fault as e:
            return e

    def delete_route_group(self, **args):
        """
        Delete a Route group
        :param name: The name of the Route group to delete
        :return: result dictionary
        """
        try:
            return self.client.removeRouteGroup(**args)
        except Fault as e:
            return e

    def update_route_group(self, **args):
        """
        Update a Route group
        :param name: The name of the Route group to update
        :param distribution_algorithm: Top Down/Circular
        :param members: A list of devices to add (must already exist DUH!)
        :return: result dictionary
        """
        try:
            return self.client.updateRouteGroup(**args)
        except Fault as e:
            return e

    def get_route_lists(self, tagfilter={"name": "", "description": ""}):
        """
        Get route lists
        :param mini: return a list of tuples of route list details
        :return: A list of dictionary's
        """
        try:
            return self.client.listRouteList({"name": "%"}, returnedTags=tagfilter)[
                "return"
            ]["routeList"]
        except Fault as e:
            return e

    def get_route_list(self, **args):
        """
        Get route list
        :param name: route list name
        :param uuid: route list uuid
        :return: result dictionary
        """
        try:
            return self.client.getRouteList(**args)["return"]["routeList"]
        except Fault as e:
            return e

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
        :param cm_group_name: Route list call mangaer group name
        :param route_list_enabled: Enable route list
        :param run_on_all_nodes: Run route list on all nodes
        :param members: A list of route groups
        :return: Result dictionary
        """
        req = {
            "name": name,
            "description": description,
            "callManagerGroupName": cm_group_name,
            "routeListEnabled": route_list_enabled,
            "runOnEveryNode": run_on_all_nodes,
            "members": {"member": []},
        }

        if members:
            [
                req["members"]["member"].append(
                    {
                        "routeGroupName": i,
                        "selectionOrder": members.index(i) + 1,
                        "calledPartyTransformationMask": "",
                        "callingPartyTransformationMask": "",
                        "digitDiscardInstructionName": "",
                        "callingPartyPrefixDigits": "",
                        "prefixDigitsOut": "",
                        "useFullyQualifiedCallingPartyNumber": "Default",
                        "callingPartyNumberingPlan": "Cisco CallManager",
                        "callingPartyNumberType": "Cisco CallManager",
                        "calledPartyNumberingPlan": "Cisco CallManager",
                        "calledPartyNumberType": "Cisco CallManager",
                    }
                )
                for i in members
            ]

        try:
            return self.client.addRouteList(req)
        except Fault as e:
            return e

    def delete_route_list(self, **args):
        """
        Delete a Route list
        :param name: The name of the Route list to delete
        :param uuid: The uuid of the Route list to delete
        :return: result dictionary
        """
        try:
            return self.client.removeRouteList(**args)
        except Fault as e:
            return e

    def update_route_list(self, **args):
        """
        Update a Route list
        :param name: The name of the Route list to update
        :param uuid: The uuid of the Route list to update
        :param description: Route list description
        :param cm_group_name: Route list call mangaer group name
        :param route_list_enabled: Enable route list
        :param run_on_all_nodes: Run route list on all nodes
        :param members: A list of route groups
        :return: result dictionary
        """
        try:
            return self.client.updateRouteList(**args)
        except Fault as e:
            return e

    def get_partitions(self, tagfilter={"name": "", "description": ""}):
        """
        Get partitions
        :param mini: return a list of tuples of partition details
        :return: A list of dictionary's
        """
        try:
            return self.client.listRoutePartition(
                {"name": "%"}, returnedTags=tagfilter
            )["return"]["routePartition"]
        except Fault as e:
            return e

    def get_partition(self, **args):
        """
        Get partition details
        :param partition: Partition name
        :param uuid: UUID name
        :return: result dictionary
        """
        try:
            return self.client.getRoutePartition(**args)["return"]["routePartition"]
        except Fault as e:
            return e

    def add_partition(self, name, description="", time_schedule_name="All the time"):
        """
        Add a partition
        :param name: Name of the partition to add
        :param description: Partition description
        :param time_schedule_name: Name of the time schedule to use
        :return: result dictionary
        """
        try:
            return self.client.addRoutePartition(
                {
                    "name": name,
                    "description": description,
                    "timeScheduleIdName": time_schedule_name,
                }
            )
        except Fault as e:
            return e

    def delete_partition(self, **args):
        """
        Delete a partition
        :param partition: The name of the partition to delete
        :return: result dictionary
        """
        try:
            return self.client.removeRoutePartition(**args)
        except Fault as e:
            return e

    def update_partition(self, **args):
        """
        Update calling search space
        :param uuid: CSS UUID
        :param name: CSS Name
        :param description:
        :param newName:
        :param timeScheduleIdName:
        :param useOriginatingDeviceTimeZone:
        :param timeZone:
        :return: result dictionary
        """
        try:
            return self.client.updateRoutePartition(**args)
        except Fault as e:
            return e

    def get_calling_search_spaces(self, tagfilter={"name": "", "description": ""}):
        """
        Get calling search spaces
        :param mini: return a list of tuples of css details
        :return: A list of dictionary's
        """
        try:
            return self.client.listCss({"name": "%"}, returnedTags=tagfilter)["return"][
                "css"
            ]
        except Fault as e:
            return e

    def get_calling_search_space(self, **args):
        """
        Get Calling search space details
        :param name: Calling search space name
        :param uuid: Calling search space uuid
        :return: result dictionary
        """
        try:
            return self.client.getCss(**args)["return"]["css"]
        except Fault as e:
            return e

    def add_calling_search_space(self, name, description="", members=[]):
        """
        Add a Calling search space
        :param name: Name of the CSS to add
        :param description: Calling search space description
        :param members: A list of partitions to add to the CSS
        :return: result dictionary
        """
        req = {
            "name": name,
            "description": description,
            "members": {"member": []},
        }
        if members:
            [
                req["members"]["member"].append(
                    {
                        "routePartitionName": i,
                        "index": members.index(i) + 1,
                    }
                )
                for i in members
            ]

        try:
            return self.client.addCss(req)
        except Fault as e:
            return e

    def delete_calling_search_space(self, **args):
        """
        Delete a Calling search space
        :param calling_search_space: The name of the partition to delete
        :return: result dictionary
        """
        try:
            return self.client.removeCss(**args)
        except Fault as e:
            return e

    def update_calling_search_space(self, **args):
        """
        Update calling search space
        :param uuid: CSS UUID
        :param name: CSS Name
        :param description:
        :param newName:
        :param members:
        :param removeMembers:
        :param addMembers:
        :return: result dictionary
        """
        try:
            return self.client.updateCss(**args)
        except Fault as e:
            return e

    def get_route_patterns(
        self, tagfilter={"pattern": "", "description": "", "uuid": ""}
    ):
        """
        Get route patterns
        :param mini: return a list of tuples of route pattern details
        :return: A list of dictionary's
        """
        try:
            return self.client.listRoutePattern(
                {"pattern": "%"},
                returnedTags=tagfilter,
            )["return"]["routePattern"]
        except Fault as e:
            return e

    def get_route_pattern(self, pattern="", uuid=""):
        """
        Get route pattern
        :param pattern: route pattern
        :param uuid: route pattern uuid
        :return: result dictionary
        """
        if uuid == "" and pattern != "":
            # Cant get pattern directly so get UUID first
            try:
                uuid = self.client.listRoutePattern(
                    {"pattern": pattern}, returnedTags={"uuid": ""}
                )
            except Fault as e:
                return e
            if "return" in uuid and uuid["return"] is not None:
                uuid = uuid["return"]["routePattern"][0]["uuid"]
                try:
                    return self.client.getRoutePattern(uuid=uuid)["return"][
                        "routePattern"
                    ]
                except Fault as e:
                    return e

        elif uuid != "" and pattern == "":
            try:
                return self.client.getRoutePattern(uuid=uuid)
            except Fault as e:
                return e

    def add_route_pattern(
        self,
        pattern,
        gateway="",
        route_list="",
        description="",
        partition="",
        blockEnable=False,
        patternUrgency=False,
        releaseClause="Call Rejected",
    ):
        """
        Add a route pattern
        :param pattern: Route pattern - required
        :param gateway: Destination gateway - required
        :param route_list: Destination route list - required
               Either a gateway or route list can be used at the same time
        :param description: Route pattern description
        :param partition: Route pattern partition
        :return: result dictionary
        """

        req = {
            "pattern": pattern,
            "description": description,
            "destination": {},
            "routePartitionName": partition,
            "blockEnable": blockEnable,
            "releaseClause": releaseClause,
            "useCallingPartyPhoneMask": "Default",
            "networkLocation": "OnNet",
        }

        if gateway == "" and route_list == "":
            return "Either a gateway OR route list, is a required parameter"

        elif gateway != "" and route_list != "":
            return "Enter a gateway OR route list, not both"

        elif gateway != "":
            req["destination"].update({"gatewayName": gateway})
        elif route_list != "":
            req["destination"].update({"routeListName": route_list})
        try:
            return self.client.addRoutePattern(req)
        except Fault as e:
            return e

    def delete_route_pattern(self, **args):
        """
        Delete a route pattern
        :param uuid: The pattern uuid
        :param pattern: The pattern of the route to delete
        :param partition: The name of the partition
        :return: result dictionary
        """
        try:
            return self.client.removeRoutePattern(**args)
        except Fault as e:
            return e

    def update_route_pattern(self, **args):
        """
        Update a route pattern
        :param uuid: The pattern uuid
        :param pattern: The pattern of the route to update
        :param partition: The name of the partition
        :param gateway: Destination gateway - required
        :param route_list: Destination route list - required
               Either a gateway or route list can be used at the same time
        :param description: Route pattern description
        :param partition: Route pattern partition
        :return: result dictionary
        """
        try:
            return self.client.updateRoutePattern(**args)
        except Fault as e:
            return e

    def get_media_resource_groups(self, tagfilter={"name": "", "description": ""}):
        """
        Get media resource groups
        :param mini: return a list of tuples of route pattern details
        :return: A list of dictionary's
        """
        try:
            return self.client.listMediaResourceGroup(
                {"name": "%"}, returnedTags=tagfilter
            )["return"]["mediaResourceGroup"]
        except Fault as e:
            return e

    def get_media_resource_group(self, **args):
        """
        Get a media resource group details
        :param media_resource_group: Media resource group name
        :return: result dictionary
        """
        try:
            return self.client.getMediaResourceGroup(**args)["return"][
                "mediaResourceGroup"
            ]
        except Fault as e:
            return e

    def add_media_resource_group(
        self, name, description="", multicast="false", members=[]
    ):
        """
        Add a media resource group
        :param name: Media resource group name
        :param description: Media resource description
        :param multicast: Mulicast enabled
        :param members: Media resource group members
        :return: result dictionary
        """
        req = {
            "name": name,
            "description": description,
            "multicast": multicast,
            "members": {"member": []},
        }

        if members:
            [req["members"]["member"].append({"deviceName": i}) for i in members]

        try:
            return self.client.addMediaResourceGroup(req)
        except Fault as e:
            return e

    def update_media_resource_group(self, **args):
        """
        Update a media resource group
        :param name: Media resource group name
        :param description: Media resource description
        :param multicast: Mulicast enabled
        :param members: Media resource group members
        :return: result dictionary
        """
        try:
            return self.client.updateMediaResourceGroup(**args)
        except Fault as e:
            return e

    def delete_media_resource_group(self, name):
        """
        Delete a Media resource group
        :param media_resource_group: The name of the media resource group to delete
        :return: result dictionary
        """
        try:
            return self.client.removeMediaResourceGroup(name=name)
        except Fault as e:
            return e

    def get_media_resource_group_lists(self, tagfilter={"name": ""}):
        """
        Get media resource groups
        :param mini: return a list of tuples of route pattern details
        :return: A list of dictionary's
        """
        try:
            return self.client.listMediaResourceList(
                {"name": "%"}, returnedTags=tagfilter
            )["return"]["mediaResourceList"]
        except Fault as e:
            return e

    def get_media_resource_group_list(self, name):
        """
        Get a media resource group list details
        :param name: Media resource group list name
        :return: result dictionary
        """
        try:
            return self.client.getMediaResourceList(name=name)
        except Fault as e:
            return e

    def add_media_resource_group_list(self, name, members=[]):
        """
        Add a media resource group list
        :param media_resource_group_list: Media resource group list name
        :param members: A list of members
        :return:
        """
        req = {"name": name, "members": {"member": []}}

        if members:
            [
                req["members"]["member"].append(
                    {"order": members.index(i), "mediaResourceGroupName": i}
                )
                for i in members
            ]
        try:
            return self.client.addMediaResourceList(req)
        except Fault as e:
            return e

    def update_media_resource_group_list(self, **args):
        """
        Update a media resource group list
        :param name: Media resource group name
        :param description: Media resource description
        :param multicast: Mulicast enabled
        :param members: Media resource group members
        :return: result dictionary
        """
        try:
            return self.client.updateMediaResourceList(**args)
        except Fault as e:
            return e

    def delete_media_resource_group_list(self, name):
        """
        Delete a Media resource group list
        :param name: The name of the media resource group list to delete
        :return: result dictionary
        """
        try:
            return self.client.removeMediaResourceList(name=name)
        except Fault as e:
            return e

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
        :param mini: return a list of tuples of directory number details
        :return: A list of dictionary's
        """
        try:
            return self.client.listLine({"pattern": "%"}, returnedTags=tagfilter,)[
                "return"
            ]["line"]
        except Fault as e:
            return e

    def get_directory_number(self, **args):
        """
        Get directory number details
        :param name:
        :param partition:
        :return: result dictionary
        """
        try:
            return self.client.getLine(**args)["return"]["line"]
        except Fault as e:
            return e

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
        """
        try:
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
        except Fault as e:
            return e

    def delete_directory_number(self, pattern="", routePartitionName="", uuid=""):
        """
        Delete a directory number
        :param directory_number: The name of the directory number to delete
        :return: result dictionary
        """
        if uuid != "":
            try:
                return self.client.removeLine(uuid=uuid)
            except Fault as e:
                return e
        else:
            try:
                return self.client.removeLine(
                    pattern=pattern, routePartitionName=routePartitionName
                )
            except Fault as e:
                return e

    def update_directory_number(self, **args):
        """
        Update a directory number
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
        """
        try:
            return self.client.updateLine(**args)
        except Fault as e:
            return e

    def get_cti_route_points(self, tagfilter={"name": "", "description": ""}):
        """
        Get CTI route points
        :param mini: return a list of tuples of CTI route point details
        :return: A list of dictionary's
        """
        try:
            return self.client.listCtiRoutePoint({"name": "%"}, returnedTags=tagfilter)[
                "return"
            ]["ctiRoutePoint"]
        except Fault as e:
            return e

    def get_cti_route_point(self, **args):
        """
        Get CTI route point details
        :param name: CTI route point name
        :param uuid: CTI route point uuid
        :return: result dictionary
        """
        try:
            return self.client.getCtiRoutePoint(**args)["return"]["ctiRoutePoint"]
        except Fault as e:
            return e

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
        :param protocol_slide: CTI protocol slide
        :param use_trusted_relay_point: Use trusted relay point: (Default, On, Off)
        :param lines: A list of tuples of [(directory_number, partition)]
        :return:
        """

        req = {
            "name": name,
            "description": description,
            "product": product,
            "class": dev_class,
            "protocol": protocol,
            "protocolSide": protocol_slide,
            "commonDeviceConfigName": common_device_config,
            "callingSearchSpaceName": css,
            "devicePoolName": device_pool,
            "locationName": location,
            "useTrustedRelayPoint": use_trusted_relay_point,
            "lines": {"line": []},
        }

        if lines:
            [
                req["lines"]["line"].append(
                    {
                        "index": lines.index(i) + 1,
                        "dirn": {"pattern": i[0], "routePartitionName": i[1]},
                    }
                )
                for i in lines
            ]

        try:
            return self.client.addCtiRoutePoint(req)
        except Fault as e:
            return e

    def delete_cti_route_point(self, **args):
        """
        Delete a CTI route point
        :param cti_route_point: The name of the CTI route point to delete
        :return: result dictionary
        """
        try:
            return self.client.removeCtiRoutePoint(**args)
        except Fault as e:
            return e

    def update_cti_route_point(self, **args):
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
        :param protocol_slide: CTI protocol slide
        :param use_trusted_relay_point: Use trusted relay point: (Default, On, Off)
        :param lines: A list of tuples of [(directory_number, partition)]
        :return:
        """
        try:
            return self.client.updateCtiRoutePoint(**args)
        except Fault as e:
            return e

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
        """
        try:
            return self.client.getPhone(**args)["return"]["phone"]
        except Fault as e:
            return e

    def add_phone(
        self,
        name,
        description="",
        product="Cisco 7941",
        device_pool="Default",
        location="Hub_None",
        phone_template="Standard 8861 SIP",
        common_device_config="",
	css="",
        aar_css="",
        subscribe_css="",
        ownerUserName="",
	securityProfileName="",
        lines=[],
        dev_class="Phone",
        protocol="SCCP",
        softkey_template="Standard User",
        enable_em="true",
        em_service_name="Extension Mobility",
        em_service_url=False,
        em_url_button_enable=False,
        em_url_button_index="1",
        em_url_label="Press here to logon",
        ehook_enable=1,
	enableActivationID = 'True',
    	allowMraMode = 'True',
    ):
        """
        lines takes a list of Tuples with properties for each line EG:

                                               display                           external
            DN     partition    display        ascii          label               mask
        [('77777', 'LINE_PT', 'Jim Smith', 'Jim Smith', 'Jim Smith - 77777', '0294127777')]
        Add A phone
        :param name:
        :param description:
        :param product:
        :param device_pool:
        :param location:
        :param phone_template:
        :param common_device_config:
        :param css:
        :param aar_css:
        :param subscribe_css:
	:param ownerUserName:
        :param lines:
        :param dev_class:
        :param protocol:
        :param softkey_template:
        :param enable_em:
        :param em_service_name:
        :param em_service_url:
        :param em_url_button_enable:
        :param em_url_button_index:
        :param em_url_label:
        :param ehook_enable:
	:param enableactivationid:
	:param allowmramode:
        :return:
        """

        req = {
            "name": name,
            "description": description,
            "product": product,
            "class": dev_class,
            "protocol": protocol,
            "protocolSide": "User",
            "commonDeviceConfigName": common_device_config,
            "commonPhoneConfigName": "Standard Common Phone Profile",
	    "softkeyTemplateName": softkey_template,
            "phoneTemplateName": phone_template,
            "devicePoolName": device_pool,
            "locationName": location,
            "useTrustedRelayPoint": "Off",
            "builtInBridgeStatus": "Default",
            "certificateOperation": "No Pending Operation",
            "packetCaptureMode": "None",
            "deviceMobilityMode": "Default",
            "enableExtensionMobility": enable_em,
            "callingSearchSpaceName": css,
            "automatedAlternateRoutingCssName": aar_css,
            "subscribeCallingSearchSpaceName": subscribe_css,
	    "ownerUserName": ownerUserName,
	    "enableActivationID": True,
	    "allowMraMode": True,
            "lines": {"line": []},
            "services": {"service": []},
            "vendorConfig": [{"ehookEnable": ehook_enable}],
        }

        if lines:
            [
                req["lines"]["line"].append(
                    {
                        "index": lines.index(i) + 1,
                        "dirn": {"pattern": i[0], "routePartitionName": i[1]},
                        "display": i[2],
                        "displayAscii": i[3],
                        "label": i[4],
                        "e164Mask": i[5],
                    }
                )
                for i in lines
            ]

        if em_service_url:
            req["services"]["service"].append(
                [
                    {
                        "telecasterServiceName": em_service_name,
                        "name": em_service_name,
                        "url": "http://{0}:8080/emapp/EMAppServlet?device=#DEVICENAME#&EMCC=#EMCC#".format(
                            self.cucm
                        ),
                    }
                ]
            )

        if em_url_button_enable:
            req["services"]["service"][0].update(
                {"urlButtonIndex": em_url_button_index, "urlLabel": em_url_label}
            )
        try:
            return self.client.addPhone(req)
        except Fault as e:
            return e

    def delete_phone(self, **args):
        """
        Delete a phone
        :param phone: The name of the phone to delete
        :return: result dictionary
        """
        try:
            return self.client.removePhone(**args)
        except Fault as e:
            return e

    def update_phone(self, **args):

        """
        lines takes a list of Tuples with properties for each line EG:

                                               display                           external
            DN     partition    display        ascii          label               mask
        [('77777', 'LINE_PT', 'Jim Smith', 'Jim Smith', 'Jim Smith - 77777', '0294127777')]
        Add A phone
        :param name:
        :param description:
        :param product:
        :param device_pool:
        :param location:
        :param phone_template:
        :param common_device_config:
        :param css:
        :param aar_css:
        :param subscribe_css:
        :param lines:
        :param dev_class:
        :param protocol:
        :param softkey_template:
        :param enable_em:
        :param em_service_name:
        :param em_service_url:
        :param em_url_button_enable:
        :param em_url_button_index:
        :param em_url_label:
        :param ehook_enable:
        :return:
        """
        try:
            return self.client.updatePhone(**args)
        except Fault as e:
            return e

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
        :param mini: return a list of tuples of device profile details
        :return: A list of dictionary's
        """
        try:
            return self.client.listDeviceProfile(
                {"name": "%"},
                returnedTags=tagfilter,
            )["return"]["deviceProfile"]
        except Fault as e:
            return e

    def get_device_profile(self, **args):
        """
        Get device profile parameters
        :param name: profile name
        :param uuid: profile uuid
        :return: result dictionary
        """
        try:
            return self.client.getDeviceProfile(**args)["return"]["deviceProfile"]
        except Fault as e:
            return e

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
        :param name:
        :param description:
        :param product:
        :param phone_template:
        :param lines:
        :param dev_class:
        :param protocol:
        :param softkey_template:
        :param em_service_name:
        :return:
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
            "lines": {"line": []},
        }

        if lines:
            [
                req["lines"]["line"].append(
                    {
                        "index": lines.index(i) + 1,
                        "dirn": {"pattern": i[0], "routePartitionName": i[1]},
                        "display": i[2],
                        "displayAscii": i[3],
                        "label": i[4],
                        "e164Mask": i[5],
                    }
                )
                for i in lines
            ]

        try:
            blah = self.client.addDeviceProfile(req)
            return blah
        except Fault as e:
            return e

    def delete_device_profile(self, **args):
        """
        Delete a device profile
        :param profile: The name of the device profile to delete
        :return: result dictionary
        """
        try:
            return self.client.removeDeviceProfile(**args)
        except Fault as e:
            return e

    def update_device_profile(self, **args):
        """
        Update A Device profile for use with extension mobility
        lines takes a list of Tuples with properties for each line EG:

                                               display                           external
            DN     partition    display        ascii          label               mask
        [('77777', 'LINE_PT', 'Jim Smith', 'Jim Smith', 'Jim Smith - 77777', '0294127777')]
        :param profile:
        :param description:
        :param product:
        :param phone_template:
        :param lines:
        :param dev_class:
        :param protocol:
        :param softkey_template:
        :param em_service_name:
        :return:
        """
        try:
            return self.client.updateDeviceProfile(**args)
        except Fault as e:
            return e

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

    def get_user(self, userid):
        """
        Get user parameters
        :param user_id: profile name
        :return: result dictionary
        """
        try:
            return self.client.getUser(userid=userid)["return"]["user"]
        except Fault as e:
            return e

    def add_user(
        self,
        userid,
        lastName,
        firstName,
        presenceGroupName="Standard Presence group",
        phoneProfiles=[],
    ):
        """
        Add a user
        :param user_id: User ID of the user to add
        :param first_name: First name of the user to add
        :param last_name: Last name of the user to add
        :return: result dictionary
        """

        try:
            return self.client.addUser(
                {
                    "userid": userid,
                    "lastName": lastName,
                    "firstName": firstName,
                    "presenceGroupName": presenceGroupName,
                    "phoneProfiles": phoneProfiles,
                }
            )
        except Fault as e:
            return e

    def update_user(self, **args):
        """
        Update end user for credentials
        :param userid: User ID
        :param password: Web interface password
        :param pin: Extension mobility PIN
        :return: result dictionary
        """
        try:
            return self.client.updateUser(**args)
        except Fault as e:
            return e

    def update_user_em(
        self, user_id, device_profile, default_profile, subscribe_css, primary_extension
    ):
        """
        Update end user for extension mobility
        :param user_id: User ID
        :param device_profile: Device profile name
        :param default_profile: Default profile name
        :param subscribe_css: Subscribe CSS
        :param primary_extension: Primary extension, must be a number from the device profile
        :return: result dictionary
        """
        try:
            resp = self.client.getDeviceProfile(name=device_profile)
        except Fault as e:
            return e
        if "return" in resp and resp["return"] is not None:
            uuid = resp["return"]["deviceProfile"]["uuid"]
            try:
                return self.client.updateUser(
                    userid=user_id,
                    phoneProfiles={"profileName": {"uuid": uuid}},
                    defaultProfile=default_profile,
                    subscribeCallingSearchSpaceName=subscribe_css,
                    primaryExtension={"pattern": primary_extension},
                    associatedGroups={"userGroup": {"name": "Standard CCM End Users"}},
                )
            except Fault as e:
                return e
        else:
            return "Device Profile not found for user"

    def update_user_credentials(self, userid, password="", pin=""):  # nosec
        """
        Update end user for credentials
        :param userid: User ID
        :param password: Web interface password
        :param pin: Extension mobility PIN
        :return: result dictionary
        """

        if password == "" and pin == "":  # nosec
            return "Password and/or Pin are required"

        elif password != "" and pin != "":  # nosec
            try:
                return self.client.updateUser(
                    userid=userid, password=password, pin=pin
                )  # nosec
            except Fault as e:
                return e

        elif password != "":  # nosec
            try:
                return self.client.updateUser(userid=userid, password=password)
            except Fault as e:
                return e

        elif pin != "":
            try:
                return self.client.updateUser(userid=userid, pin=pin)
            except Fault as e:
                return e

    def delete_user(self, **args):
        """
        Delete a user
        :param userid: The name of the user to delete
        :return: result dictionary
        """
        try:
            return self.client.removeUser(**args)
        except Fault as e:
            return e

    def get_translations(self):
        """
        Get translation patterns
        :param mini: return a list of tuples of route pattern details
        :return: A list of dictionary's
        """
        try:
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
        except Fault as e:
            return e

    def get_translation(self, pattern="", routePartitionName="", uuid=""):
        """
        Get translation pattern
        :param pattern: translation pattern to match
        :param routePartitionName: routePartitionName required if searching pattern
        :param uuid: translation pattern uuid
        :return: result dictionary
        """

        if pattern != "" and routePartitionName != "" and uuid == "":
            try:
                return self.client.getTransPattern(
                    pattern=pattern,
                    routePartitionName=routePartitionName,
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
                )
            except Fault as e:
                return e
        elif uuid != "" and pattern == "" and routePartitionName == "":
            try:
                return self.client.getTransPattern(
                    uuid=uuid,
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
                )
            except Fault as e:
                return e
        else:
            return "must specify either uuid OR pattern and partition"

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
        :return: result dictionary
        """
        try:
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
                }
            )
        except Fault as e:
            return e

    def delete_translation(self, pattern="", partition="", uuid=""):
        """
        Delete a translation pattern
        :param pattern: The pattern of the route to delete
        :param partition: The name of the partition
        :param uuid: Required if pattern and partition are not specified
        :return: result dictionary
        """

        if pattern != "" and partition != "" and uuid == "":
            try:
                return self.client.removeTransPattern(
                    pattern=pattern, routePartitionName=partition
                )
            except Fault as e:
                return e
        elif uuid != "" and pattern == "" and partition == "":
            try:
                return self.client.removeTransPattern(uuid=uuid)
            except Fault as e:
                return e
        else:
            return "must specify either uuid OR pattern and partition"

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
        Update a translation pattern
        :param uuid: UUID or Translation + Partition Required
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
        :return: result dictionary
        """

        args = {}
        if description != "":
            args["description"] = description
        if pattern != "" and partition != "" and uuid == "":
            args["pattern"] = pattern
            args["routePartitionName"] = partition
        if pattern == "" and partition == "" and uuid != "":
            args["uuid"] = uuid
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
        try:
            return self.client.updateTransPattern(**args)
        except Fault as e:
            return e

    def list_route_plan(self, pattern=""):
        """
        List Route Plan
        :param pattern: Route Plan Contains Pattern
        :return: results dictionary
        """
        try:
            return self.client.listRoutePlan(
                {"dnOrPattern": "%" + pattern + "%"},
                returnedTags={
                    "dnOrPattern": "",
                    "partition": "",
                    "type": "",
                    "routeDetail": "",
                },
            )["return"]["routePlan"]
        except Fault as e:
            return e

    def list_route_plan_specific(self, pattern=""):
        """
        List Route Plan
        :param pattern: Route Plan Contains Pattern
        :return: results dictionary
        """
        try:
            return self.client.listRoutePlan(
                {"dnOrPattern": pattern},
                returnedTags={
                    "dnOrPattern": "",
                    "partition": "",
                    "type": "",
                    "routeDetail": "",
                },
            )
        except Fault as e:
            return e

    def get_called_party_xforms(self):
        """
        Get called party xforms
        :param mini: return a list of tuples of called party transformation pattern details
        :return: A list of dictionary's
        """
        try:
            return self.client.listCalledPartyTransformationPattern(
                {"pattern": "%"},
                returnedTags={"pattern": "", "description": "", "uuid": ""},
            )["return"]["calledPartyTransformationPattern"]
        except Fault as e:
            return e

    def get_called_party_xform(self, **args):
        """
        Get called party xform details
        :param name:
        :param partition:
        :param uuid:
        :return: result dictionary
        """
        try:
            return self.client.getCalledPartyTransformationPattern(**args)["return"][
                "calledPartyTransformationPattern"
            ]
        except Fault as e:
            return e

    def add_called_party_xform(
        self,
        pattern="",
        description="",
        partition="",
        calledPartyPrefixDigits="",
        calledPartyTransformationMask="",
        digitDiscardInstructionName="",
    ):
        """
        Add a called party transformation pattern
        :param pattern: pattern - required
        :param routePartitionName: partition required
        :param description: Route pattern description
        :param calledPartyTransformationmask:
        :param dialPlanName:
        :param digitDiscardInstructionName:
        :param routeFilterName:
        :param calledPartyPrefixDigits:
        :param calledPartyNumberingPlan:
        :param calledPartyNumberType:
        :param mlppPreemptionDisabled: does anyone use this?
        :return: result dictionary
        """
        try:
            return self.client.addCalledPartyTransformationPattern(
                {
                    "pattern": pattern,
                    "description": description,
                    "routePartitionName": partition,
                    "calledPartyPrefixDigits": calledPartyPrefixDigits,
                    "calledPartyTransformationMask": calledPartyTransformationMask,
                    "digitDiscardInstructionName": digitDiscardInstructionName,
                }
            )
        except Fault as e:
            return e

    def delete_called_party_xform(self, **args):
        """
        Delete a called party transformation pattern
        :param uuid: The pattern uuid
        :param pattern: The pattern of the transformation to delete
        :param partition: The name of the partition
        :return: result dictionary
        """
        try:
            return self.client.removeCalledPartyTransformationPattern(**args)
        except Fault as e:
            return e

    def update_called_party_xform(self, **args):
        """
        Update a called party transformation
        :param uuid: required unless pattern and routePartitionName is given
        :param pattern: pattern - required
        :param routePartitionName: partition required
        :param description: Route pattern description
        :param calledPartyTransformationmask:
        :param dialPlanName:
        :param digitDiscardInstructionName:
        :param routeFilterName:
        :param calledPartyPrefixDigits:
        :param calledPartyNumberingPlan:
        :param calledPartyNumberType:
        :param mlppPreemptionDisabled: does anyone use this?
        :return: result dictionary
        :return: result dictionary
        """
        try:
            return self.client.updateCalledPartyTransformationPattern(**args)
        except Fault as e:
            return e

    def get_calling_party_xforms(self):
        """
        Get calling party xforms
        :param mini: return a list of tuples of calling party transformation pattern details
        :return: A list of dictionary's
        """
        try:
            return self.client.listCallingPartyTransformationPattern(
                {"pattern": "%"},
                returnedTags={"pattern": "", "description": "", "uuid": ""},
            )["return"]["callingPartyTransformationPattern"]
        except Fault as e:
            return e

    def get_calling_party_xform(self, **args):
        """
        Get calling party xform details
        :param name:
        :param partition:
        :param uuid:
        :return: result dictionary
        """
        try:
            return self.client.getCallingPartyTransformationPattern(**args)["return"][
                "callingPartyTransformationPattern"
            ]
        except Fault as e:
            return e

    def add_calling_party_xform(
        self,
        pattern="",
        description="",
        partition="",
        callingPartyPrefixDigits="",
        callingPartyTransformationMask="",
        digitDiscardInstructionName="",
    ):
        """
        Add a calling party transformation pattern
        :param pattern: pattern - required
        :param routePartitionName: partition required
        :param description: Route pattern description
        :param callingPartyTransformationmask:
        :param dialPlanName:
        :param digitDiscardInstructionName:
        :param routeFilterName:
        :param callingPartyPrefixDigits:
        :param callingPartyNumberingPlan:
        :param callingPartyNumberType:
        :param mlppPreemptionDisabled: does anyone use this?
        :return: result dictionary
        """
        try:
            return self.client.addCallingPartyTransformationPattern(
                {
                    "pattern": pattern,
                    "description": description,
                    "routePartitionName": partition,
                    "callingPartyPrefixDigits": callingPartyPrefixDigits,
                    "callingPartyTransformationMask": callingPartyTransformationMask,
                    "digitDiscardInstructionName": digitDiscardInstructionName,
                }
            )
        except Fault as e:
            return e

    def delete_calling_party_xform(self, **args):
        """
        Delete a calling party transformation pattern
        :param uuid: The pattern uuid
        :param pattern: The pattern of the transformation to delete
        :param partition: The name of the partition
        :return: result dictionary
        """
        try:
            return self.client.removeCallingPartyTransformationPattern(**args)
        except Fault as e:
            return e

    def update_calling_party_xform(self, **args):
        """
        Update a calling party transformation
        :param uuid: required unless pattern and routePartitionName is given
        :param pattern: pattern - required
        :param routePartitionName: partition required
        :param description: Route pattern description
        :param callingPartyTransformationMask:
        :param dialPlanName:
        :param digitDiscardInstructionName:
        :param routeFilterName:
        :param calledPartyPrefixDigits:
        :param calledPartyNumberingPlan:
        :param calledPartyNumberType:
        :param mlppPreemptionDisabled: does anyone use this?
        :return: result dictionary
        :return: result dictionary
        """
        try:
            return self.client.updateCallingPartyTransformationPattern(**args)
        except Fault as e:
            return e

    def get_sip_trunks(
        self, tagfilter={"name": "", "sipProfileName": "", "callingSearchSpaceName": ""}
    ):
        try:
            return self.client.listSipTrunk({"name": "%"}, returnedTags=tagfilter)[
                "return"
            ]["sipTrunk"]
        except Fault as e:
            return e

    def get_sip_trunk(self, **args):
        """
        Get sip trunk
        :param name:
        :param uuid:
        :return: result dictionary
        """
        try:
            return self.client.getSipTrunk(**args)["return"]["sipTrunk"]
        except Fault as e:
            return e

    def update_sip_trunk(self, **args):
        """
        Update a SIP Trunk
        :param name:
        :param uuid:
        :param newName:
        :param description:
        :param callingSearchSpaceName:
        :param devicePoolName:
        :param locationName:
        :param sipProfileName:
        :param mtpRequired:

        :return:
        """
        try:
            return self.client.updateSipTrunk(**args)
        except Fault as e:
            return e

    def delete_sip_trunk(self, **args):
        try:
            return self.client.removeSipTrunk(**args)
        except Fault as e:
            return e

    def get_sip_security_profile(self, name):
        try:
            return self.client.getSipTrunkSecurityProfile(name=name)["return"]
        except Fault as e:
            return e

    def get_sip_profile(self, name):
        try:
            return self.client.getSipProfile(name=name)["return"]
        except Fault as e:
            return e

    def add_sip_trunk(self, **args):
        """
        Add a SIP Trunk
        :param name:
        :param description:
        :param product:
        :param protocol:
        :param protocolSide:
        :param callingSearchSpaceName:
        :param devicePoolName:
        :param securityProfileName:
        :param sipProfileName:
        :param destinations: param destination:
        :param runOnEveryNode:

        :return:
        """
        try:
            return self.client.addSipTrunk(**args)
        except Fault as e:
            return e

    def list_process_nodes(self):
        try:
            return self.client.listProcessNode(
                {"name": "%", "processNodeRole": "CUCM Voice/Video"},
                returnedTags={"name": ""},
            )["return"]["processNode"]
        except Fault as e:
            return e

    def add_call_manager_group(self, name, members):
        """
        Add call manager group
        :param name: name of cmg
        :param members[]: array of members
        :return: result dictionary
        """

        try:
            return self.client.addCallManagerGroup({"name": name, "members": members})
        except Fault as e:
            return e

    def get_call_manager_group(self, name):
        """
        Get call manager group
        :param name: name of cmg
        :return: result dictionary
        """
        try:
            return self.client.getCallManagerGroup(name=name)
        except Fault as e:
            return e

    def get_call_manager_groups(self):
        """
        Get call manager groups
        :param name: name of cmg
        :return: result dictionary
        """
        try:
            return self.client.listCallManagerGroup(
                {"name": "%"}, returnedTags={"name": ""}
            )["return"]["callManagerGroup"]
        except Fault as e:
            return e

    def update_call_manager_group(self, **args):
        """
        Update call manager group
        :param name: name of cmg
        :return: result dictionary
        """
        try:
            return self.client.listCallManagerGroup({**args}, returnedTags={"name": ""})
        except Fault as e:
            return e

    def delete_call_manager_group(self, name):
        """
        Delete call manager group
        :param name: name of cmg
        :return: result dictionary
        """
        try:
            return self.client.removeCallManagerGroup({"name": name})
        except Fault as e:
            return e

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
        :param mini: return a list of tuples of hunt pilot details
        :return: A list of dictionary's
        """
        try:
            response = self.client.listHuntPilot(
                {"pattern": "%"},
                returnedTags=tagfilter,
            )["return"]
            if response:
                return response["huntPilot"]
            else:
                return response
        except Fault as e:
            return e

    def get_hunt_pilot(self, **args):
        """
        Get hunt pilot details
        :param name:
        :param partition:
        :return: result dictionary
        """
        try:
            return self.client.getHuntPilot(**args)["return"]["huntPilot"]
        except Fault as e:
            return e

    def add_hunt_pilot(self, **args):
        """
        Add a Hunt Pilot minimal params needed
        :param pattern: pattern - required
        :param routePartitionName: partition required
        :param description: Hunt Pilot pattern description
        :param useCallingPartyPhoneMask: "Off" or "On"
        :param blockEnable: boolean (true or false)
        :param huntListName:
        :return: result dictionary
        """
        try:
            return self.client.addHuntPilot({**args})
        except Fault as e:
            return e

    def update_hunt_pilot(self, **args):
        """
        Update a Hunt Pilot
        :param pattern: pattern - required
        :param routePartitionName: partition required
        :param description: Hunt Pilot pattern description
        :param useCallingPartyPhoneMask: "Off" or "On"
        :param blockEnable: boolean (true or false)
        :param huntListName:
        :return:
        """
        try:
            return self.client.updateHuntPilot(**args)
        except Fault as e:
            return e

    def delete_hunt_pilot(self, **args):
        """
        Delete a Hunt Pilot
        :param uuid: The pattern uuid
        :param pattern: The pattern of the transformation to delete
        :param partition: The name of the partition
        :return: result dictionary
        """
        try:
            return self.client.removeHuntPilot(**args)
        except Fault as e:
            return e

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
        :param mini: return a list of tuples of hunt pilot details
        :return: A list of dictionary's
        """
        try:
            response = self.client.listHuntList(
                {"name": "%"},
                returnedTags=tagfilter,
            )["return"]
            if response:
                return response["huntList"]
            else:
                return response
        except Fault as e:
            return e

    def get_hunt_list(self, **args):
        """
        Get hunt list details
        :param name:
        :param partition:
        :return: result dictionary
        """
        try:
            return self.client.getHuntList(**args)["return"]["huntList"]
        except Fault as e:
            return e

    def add_hunt_list(self, **args):
        """
        Add a Hunt list minimal params needed
        :param name: - required
        :param callManagerGroup: - required
        :param description: str
        :param routeListEnabled: bool
        :param voiceMailUsage: bool
        :return: result dictionary
        """
        try:
            return self.client.addHuntList({**args})
        except Fault as e:
            return e

    def update_hunt_list(self, **args):
        """
        Update a Hunt List
        :param name: - required
        :param callManagerGroup: - required
        :param description: str
        :param routeListEnabled: bool
        :param voiceMailUsage: bool
        :return:
        """
        try:
            return self.client.updateHuntList(**args)
        except Fault as e:
            return e

    def delete_hunt_list(self, **args):
        """
        Delete a Hunt List
        :param name: - required
        :return: result dictionary
        """
        try:
            return self.client.removeHuntList(**args)
        except Fault as e:
            return e

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
        :param mini: return a list of tuples of hunt pilot details
        :return: A list of dictionary's
        """
        try:
            response = self.client.listLineGroup(
                {"name": "%"},
                returnedTags=tagfilter,
            )["return"]
            if response:
                return response["lineGroup"]
            else:
                return response
        except Fault as e:
            return e

    def get_line_group(self, **args):
        """
        Get line group details
        :param name:
        :return: result dictionary
        """
        try:
            return self.client.getLineGroup(**args)["return"]["lineGroup"]
        except Fault as e:
            return e

    def add_line_group(self, **args):
        """
        Add a Line Group minimal params needed
        :param name: - required
        :param distributionAlgorithm: "Longest Idle Time", "Broadcast" etc...
        :param rnaReversionTimeOut:
        :param huntAlgorithmNoAnswer: "Try next member; then, try next group in Hunt List",
        :param huntAlgorithmBusy: "Try next member; then, try next group in Hunt List",
        :param huntAlgorithmNotAvailable: "Try next member; then, try next group in Hunt List",
        :param members: dict for each member directory number
        :return: result dictionary
        """
        try:
            return self.client.addLineGroup({**args})
        except Fault as e:
            return e

    def update_line_group(self, **args):
        """
        Update a Line Group
        :param name: - required
        :param distributionAlgorithm: "Longest Idle Time", "Broadcast" etc...
        :param rnaReversionTimeOut:
        :param huntAlgorithmNoAnswer: "Try next member; then, try next group in Hunt List",
        :param huntAlgorithmBusy: "Try next member; then, try next group in Hunt List",
        :param huntAlgorithmNotAvailable: "Try next member; then, try next group in Hunt List",
        :param members: dict for each member directory number
        :return: result dictionary
        :return:
        """
        try:
            return self.client.updateLineGroup(**args)
        except Fault as e:
            return e

    def delete_line_group(self, **args):
        """
        Delete a Line Group
        :param name: - required
        :return: result dictionary
        """
        try:
            return self.client.removeLineGroup(**args)
        except Fault as e:
            return e

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
        :param pattern: return a list of tuples of hunt pilot details
        :return: A list of dictionary's
        """
        try:
            response = self.client.listCallPickupGroup(
                {"pattern": "%"},
                returnedTags=tagfilter,
            )["return"]
            if response:
                return response["callPickupGroup"]
            else:
                return response
        except Fault as e:
            return e

    def get_call_pickup_group(self, **args):
        """
        Get call pickup group details
        :param pattern:
        :param name:
        :param
        :return: result dictionary
        """
        try:
            return self.client.getCallPickupGroup(**args)["return"]["callPickupGroup"]
        except Fault as e:
            return e

    def add_call_pickup_group(self, **args):
        """
        Add a Call Pickup Group minimal params needed
        :param name: - required
        :param pattern: - required
        :param description:
        :param usage:
        :param routePartitionName:
        :param pickupNotification:
        :param pickupNotificationTimer:
        :param callInfoForPickupNotification:
        :param members:
        :return: result dictionary
        """
        try:
            return self.client.addCallPickupGroup({**args})
        except Fault as e:
            return e

    def update_call_pickup_group(self, **args):
        """
        Update a Call Pickup Group
        :param name:
        :param pattern:
        :param description:
        :param usage:
        :param routePartitionName:
        :param pickupNotification:
        :param pickupNotificationTimer:
        :param callInfoForPickupNotification:
        :param members:
        :return: result dictionary
        """
        try:
            return self.client.updateCallPickupGroup(**args)
        except Fault as e:
            return e

    def delete_call_pickup_group(self, **args):
        """
        Delete a Call Pickup Group
        :param name: - required
        :return: result dictionary
        """
        try:
            return self.client.removeCallPickupGroup(**args)
        except Fault as e:
            return e
