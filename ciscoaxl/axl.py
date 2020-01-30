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

from requests import Session 
from requests.auth import HTTPBasicAuth 
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

    def __init__(self, username, password, cucm, cucm_version):
        """
        :param username: axl username
        :param password: axl password
        :param cucm: UCM IP address
        :param cucm_version: UCM version

        example usage:
        >>> from axl import AXL
        >>> ucm = AXL('axl_user', 'axl_pass', '192.168.200.10')
        """

        cwd = os.path.dirname(os.path.abspath(__file__))
        if os.name == "posix":
            wsdl = Path(f"{cwd}/schema/{cucm_version}/AXLAPI.wsdl").as_uri()
            print(os.name)
        else:
            print(os.name)
            wsdl = str(Path(f"{cwd}/schema/{cucm_version}/AXLAPI.wsdl").absolute())
        session = Session() 
        session.verify = False 
        session.auth = HTTPBasicAuth(username, password) 
        settings = Settings(strict=False, xml_huge_tree=True) 
        transport = Transport(session=session, timeout=10, cache=SqliteCache()) 
        axl_client = Client(wsdl, settings=settings, transport=transport) 

        self.wsdl = wsdl
        self.username = username
        self.password = password
        self.wsdl = wsdl
        self.cucm = cucm
        self.cucm_version = cucm_version
        self.UUID_PATTERN = re.compile(r'^[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$', re.IGNORECASE)
        self.client = axl_client.create_service("{http://www.cisco.com/AXLAPIService/}AXLAPIBinding", f"https://{cucm}:8443/axl/")

    def get_locations(self):
        """
        Get location details
        :param mini: return a list of tuples of location details
        :return: A list of dictionary's
        """
        try:
            return self.client.listLocation(
                    {'name': '%'}, returnedTags={
                        'name': '',
                        'withinAudioBandwidth': '',
                        'withinVideoBandwidth': '',
                        'withinImmersiveKbits': '',
                    })['return']['location']
        except Fault as e:
            return e

    def execute_sql_query(self, query):
        """
        Execute SQL query
        :param query: SQL Query to execute
        :return: result dictionary
        """
        try:
            return self.client.executeSQLQuery(query)['return']
        except Fault as e:
            return e

    def execute_sql_update(self, query):
        """
        Execute SQL update
        :param query: SQL Update to execute
        :return: result dictionary
        """
        try:
            return self.client.executeSQLUpdate(query)
        except Fault as e:
            return e

    def get_ldap_dir(self):
        """
        Get LDAP Syncs
        :return: result dictionary
        """
        try:
            return self.client.listLdapDirectory(
                    {'name': '%'}, returnedTags={
                            'name': '',
                            'ldapDn': '',
                            'userSearchBase': '',
                    })['return']['ldapDirectory']
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

    def do_change_dnd_status(self, userID, status):
        """
        Do Change DND Status
        :param userID:
        :param status:
        :return: result dictionary
        """
        try:
            return self.client.doChangeDNDStatus(userID=userID, status=status)
        except Fault as e:
            return e

    def do_device_login(self, device, userId):
        """
        Do Device Login
        :param device:
        :param userId:
        :return: result dictionary
        """
        try:
            return self.client.doDeviceLogin(deviceName=device, userId=userId)
        except Fault as e:
            return e

    def do_device_logout(self, device, userId):
        """
        Do Device Logout
        :param device:
        :param userId:
        :return: result dictionary
        """
        try:
            return self.client.doDeviceLogout(deviceName=device, userId=userId)
        except Fault as e:
            return e

    def do_device_reset(self, name='', uuid=''):
        """
        Do Device Reset
        :param name: device name
        :param uuid: device uuid
        :return: result dictionary
        """
        if name != '' and uuid == '':
            try:
                return self.client.doDeviceReset(deviceName=name, isHardReset=True)
            except Fault as e:
                return e
        elif name == '' and uuid != '':
            try:
                return self.client.doDeviceReset(uuid=uuid, isHardReset=True)
            except Fault as e:
                return e

    def reset_sip_trunk(self, name='', uuid=''):
        """
        Reset SIP Trunk
        :param name: device name
        :param uuid: device uuid
        :return: result dictionary
        """
        if name != '' and uuid == '':
            try:
                return self.client.resetSipTrunk(name=name)
            except Fault as e:
                return e
        elif name == '' and uuid != '':
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

    def add_location(self,
                     name,
                     kbits=512,
                     video_kbits=-1,
                     within_audio_bw=512,
                     within_video_bw=-1,
                     within_immersive_kbits=-1):
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
        if int(self.cucm_version) >= 10:
            try:
                return self.client.addLocation({
                    'name': name,
                    # CUCM 10.6
                    'withinAudioBandwidth': within_audio_bw,
                    'withinVideoBandwidth': within_video_bw,
                    'withinImmersiveKbits': within_immersive_kbits,
                })
            except Fault as e:
                return e
        else:
            try:
                return self.client.addLocation({
                    'name': name,
                    # CUCM 8.6
                    'kbits': kbits,
                    'videoKbits': video_kbits,
                })
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

    def get_regions(self):
        """
        Get region details
        :param mini: return a list of tuples of region details
        :return: A list of dictionary's
        """
        try:
            return self.client.listRegion({'name': '%'}, returnedTags={'_uuid': '', 'name': ''})[1]['return']['region']
        except Fault as e:
            return e

    def get_region(self, **args):
        """
        Get region information
        :param name: Region name
        :return: result dictionary
        """
        try:
            return self.client.getRegion(**args)
        except Fault as e:
            return e

    def add_region(self, region):
        """
        Add a region
        :param region: Name of the region to add
        :return: result dictionary
        """
        try:
            return self.client.addRegion({'name': region})
        except Fault as e:
            return e

    def update_region(self, name='', uuid='', moh_region=''):
        """
        Update region and assign region to all other regions
        :param name:
        :param uuid:
        :param moh_region:
        :return:
        """
        # Get all Regions
        all_regions = self.client.listRegion({'name': '%'}, returnedTags={'name': ''})

        # Make list of region names
        region_names = [str(i['name']) for i in all_regions[1]['return']['region']]

        # Build list of dictionaries to add to region api call
        region_list = []

        for i in region_names:
            # Highest codec within a region
            if i == name:
                region_list.append({
                    'regionName': i,
                    'bandwidth': '256 kbps',
                    'videoBandwidth': '-1',
                    'immersiveVideoBandwidth': '-1',
                    'lossyNetwork': 'Use System Default',
                })

            # Music on hold region name
            elif i == moh_region:
                region_list.append({
                    'regionName': i,
                    'bandwidth': '64 kbps',
                    'videoBandwidth': '-1',
                    'immersiveVideoBandwidth': '-1',
                    'lossyNetwork': 'Use System Default',
                })

            # All else G.711
            else:
                region_list.append({
                    'regionName': i,
                    'bandwidth': '64 kbps',
                    'videoBandwidth': '-1',
                    'immersiveVideoBandwidth': '-1',
                    'lossyNetwork': 'Use System Default',
                })

        if name != '' and uuid == '':
            try:
                return self.client.updateRegion(name=name,relatedRegions={'relatedRegion': region_list})
            except Fault as e:
                return e
        elif name == '' and uuid != '':
            try:
                return self.client.updateRegion(uuid=uuid,relatedRegions={'relatedRegion': region_list})
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

    def get_srsts(self):
        """
        Get all SRST details
        :param mini: return a list of tuples of SRST details
        :return: A list of dictionary's
        """
        try:
            return self.client.listSrst({'name': '%'}, returnedTags={'_uuid': ''})['return']['srst']
        except Fault as e:
            return e

    def get_srst(self, srst):
        """
        Get SRST information
        :param srst: SRST name
        :return: result dictionary
        """
        try:
            return self.client.getSrst(name=srst)
        except Fault as e:
            return e

    def add_srst(self, srst, ip_address, port=2000, sip_port=5060):
        """
        Add SRST
        :param srst: SRST name
        :param ip_address: SRST ip address
        :param port: SRST port
        :param sip_port: SIP port
        :return: result dictionary
        """
        try:
            return self.client.addSrst({
            'name': srst,
            'port': port,
            'ipAddress': ip_address,
            'SipPort': sip_port,
        })
        except Fault as e:
            return e

    def delete_srst(self, srst):
        """
        Delete a SRST
        :param srst: The name of the SRST to delete
        :return: result dictionary
        """
        try:
            return self.client.removeSrst(name=srst)
        except Fault as e:
            return e

    def get_device_pools(self):
        """
        Get a dictionary of device pools
        :param mini: return a list of tuples of device pool info
        :return: a list of dictionary's of device pools information
        """
        try:
            return self.client.listDevicePool(
                {'name': '%'}, returnedTags={
                    'name': '',
                    'dateTimeSettingName': '',
                    'callManagerGroupName': '',
                    'mediaResourceListName': '',
                    'regionName': '',
                    'srstName': '',
                    # 'localRouteGroup': [0],
                })['return']['devicePool']
        except Fault as e:
            return e

    def get_device_pool(self, **args):
        """
        Get device pool parameters
        :param device_pool: device pool name
        :return: result dictionary
        """
        try:
            return self.client.getDevicePool(**args)
        except Fault as e:
            return e

    def add_device_pool(self,
                        device_pool,
                        date_time_group='CMLocal',
                        region='Default',
                        location='',
                        route_group='',
                        media_resource_group_list='',
                        srst='Disable',
                        cm_group='Default',
                        network_locale=''):

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
            return self.client.addDevicePool({
                'name': device_pool,
                'dateTimeSettingName': date_time_group,  # update to state timezone
                'regionName': region,
                'locationName': location,
                'localRouteGroup': {'name': 'Standard Local Route Group', 'value': route_group},
                'mediaResourceListName': media_resource_group_list,
                'srstName': srst,
                'callManagerGroupName': cm_group,
                'networkLocale': network_locale,
            })
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

    def get_conference_bridges(self):
        """
        Get conference bridges
        :param mini: List of tuples of conference bridge details
        :return: results dictionary
        """
        try:
            return self.client.listConferenceBridge(
                {'name': '%'},
                returnedTags={'name': '',
                              'description': '',
                              'devicePoolName': '',
                              'locationName': ''})['return']['conferenceBridge']
        except Fault as e:
            return e

    def get_conference_bridge(self, conference_bridge):
        """
        Get conference bridge parameters
        :param conference_bridge: conference bridge name
        :return: result dictionary
        """
        try:
            return self.client.getConferenceBridge(name=conference_bridge)
        except Fault as e:
            return e

    def add_conference_bridge(self,
                              conference_bridge,
                              description='',
                              device_pool='Default',
                              location='Hub_None',
                              product='Cisco IOS Enhanced Conference Bridge',
                              security_profile='Non Secure Conference Bridge'):
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
            return self.client.addConferenceBridge({
                'name': conference_bridge,
                'description': description,
                'devicePoolName': device_pool,
                'locationName': location,
                'product': product,
                'securityProfileName': security_profile
            })
        except Fault as e:
            return e

    def delete_conference_bridge(self, conference_bridge):
        """
        Delete a Conference bridge
        :param conference_bridge: The name of the Conference bridge to delete
        :return: result dictionary
        """
        try:
            return self.client.removeConferenceBridge(name=conference_bridge)
        except Fault as e:
            return e

    def get_transcoders(self):
        """
        Get transcoders
        :param mini: List of tuples of transcoder details
        :return: results dictionary
        """
        try:
            return self.client.listTranscoder(
                {'name': '%'},
                returnedTags={'name': '',
                              'description': '',
                              'devicePoolName': ''})['return']['transcoder']
        except Fault as e:
            return e

    def get_transcoder(self, transcoder):
        """
        Get conference bridge parameters
        :param transcoder: conference bridge name
        :return: result dictionary
        """
        try:
            return self.client.getTranscoder(name=transcoder)
        except Fault as e:
            return e

    def add_transcoder(self,
                       transcoder,
                       description='',
                       device_pool='Default',
                       product='Cisco IOS Enhanced Media Termination Point'):
        """
        Add a transcoder
        :param transcoder: Transcoder name
        :param description: Transcoder description
        :param device_pool: Transcoder device pool
        :param product: Trancoder product
        :return: result dictionary
        """
        try:
            return self.client.addTranscoder({
                'name': transcoder,
                'description': description,
                'devicePoolName': device_pool,
                'product': product,
            })
        except Fault as e:
            return e

    def delete_transcoder(self, transcoder):
        """
        Delete a Transcoder
        :param transcoder: The name of the Transcoder to delete
        :return: result dictionary
        """
        try:
            return self.client.removeTranscoder(name=transcoder)
        except Fault as e:
            return e

    def get_h323_gateways(self):
        """
        Get H323 Gateways
        :param mini: List of tuples of H323 Gateway details
        :return: results dictionary
        """
        try:
            return self.client.listH323Gateway(
                {'name': '%'},
                returnedTags={'name': '',
                              'description': '',
                              'devicePoolName': '',
                              'locationName': '',
                              'sigDigits': ''})['return']['h323Gateway']
        except Fault as e:
            return e

    def get_h323_gateway(self, h323_gateway):
        """
        Get H323 Gateway parameters
        :param h323_gateway: H323 Gateway name
        :return: result dictionary
        """
        try:
            return self.client.getH323Gateway(name=h323_gateway)
        except Fault as e:
            return e

    def add_h323_gateway(self,
                         h323_gateway,
                         description='',
                         device_pool='Default',
                         location='Hub_None',
                         media_resource_group_list='',
                         prefix_dn='',
                         sig_digits='99',
                         css='',
                         aar_css='',
                         aar_neighborhood='',
                         product='H.323 Gateway',
                         protocol='H.225',
                         protocol_side='Network',
                         pstn_access='true',
                         redirect_in_num_ie='false',
                         redirect_out_num_ie='false',
                         cld_party_ie_num_type='Unknown',
                         clng_party_ie_num_type='Unknown',
                         clng_party_nat_pre='',
                         clng_party_inat_prefix='',
                         clng_party_unknown_prefix='',
                         clng_party_sub_prefix='',
                         clng_party_nat_strip_digits='',
                         clng_party_inat_strip_digits='',
                         clng_party_unknown_strip_digits='',
                         clng_party_sub_strip_digits='',
                         clng_party_nat_trans_css='',
                         clng_party_inat_trans_css='',
                         clng_party_unknown_trans_css='',
                         clng_party_sub_trans_css=''):
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
            return self.client.addH323Gateway({
                'name': h323_gateway,
                'description': description,
                'product': product,
                'protocol': protocol,
                'protocolSide': protocol_side,
                'callingSearchSpaceName': css,
                'automatedAlternateRoutingCssName': aar_css,
                'devicePoolName': device_pool,
                'locationName': location,
                'mediaResourceListName': media_resource_group_list,
                'aarNeighborhoodName': aar_neighborhood,
                'pstnAccess': pstn_access,
                'sigDigits': sig_digits,
                'prefixDn': prefix_dn,
                'redirectInboundNumberIe': redirect_in_num_ie,
                'redirectOutboundNumberIe': redirect_out_num_ie,
                'calledPartyIeNumberType': cld_party_ie_num_type,
                'callingPartyIeNumberType': clng_party_ie_num_type,
                'callingPartyNationalPrefix': clng_party_nat_pre,
                'callingPartyInternationalPrefix': clng_party_inat_prefix,
                'callingPartyUnknownPrefix': clng_party_unknown_prefix,
                'callingPartySubscriberPrefix': clng_party_sub_prefix,
                'callingPartyNationalStripDigits': clng_party_nat_strip_digits,
                'callingPartyInternationalStripDigits': clng_party_inat_strip_digits,
                'callingPartyUnknownStripDigits': clng_party_unknown_strip_digits,
                'callingPartySubscriberStripDigits': clng_party_sub_strip_digits,
                'callingPartyNationalTransformationCssName': clng_party_nat_trans_css,
                'callingPartyInternationalTransformationCssName': clng_party_inat_trans_css,
                'callingPartyUnknownTransformationCssName': clng_party_unknown_trans_css,
                'callingPartySubscriberTransformationCssName': clng_party_sub_trans_css
            })
        except Fault as e:
            return e

    def update_h323_gateway_mrgl(self, h323_gateway, media_resource_group_list):
        """

        :param h323_gateway:
        :param media_resource_group_list:
        :return:
        """
        try:
            return self.client.updateH323Gateway(
                name=h323_gateway,
                mediaResourceListName=media_resource_group_list,
        )
        except Fault as e:
            return e

    def delete_h323_gateway(self, h323_gateway):
        """
        Delete a H323 gateway
        :param h323_gateway: The name of the H323 gateway to delete
        :return: result dictionary
        """
        try:
            return self.client.removeH323Gateway(name=h323_gateway)
        except Fault as e:
            return e

    def get_route_groups(self):
        """
        Get route groups
        :param mini: return a list of tuples of route group details
        :return: A list of dictionary's
        """
        try:
            return self.client.listRouteGroup(
                {'name': '%'}, returnedTags={'name': '', 'distributionAlgorithm': ''})['return']['routeGroup']
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
            return self.client.getRouteGroup(**args)
        except Fault as e:
            return e

    def add_route_group(self,
                        name,
                        distribution_algorithm='Top Down',
                        members=[]):
        """
        Add a route group
        :param name: Route group name
        :param distribution_algorithm: Top Down/Circular
        :param members: A list of devices to add (must already exist DUH!)
        """
        req = {
            'name': name,
            'distributionAlgorithm': distribution_algorithm,
            'members': {'member': []},
        }

        if members:
            [req['members']['member'].append({
                'deviceName': i,
                'deviceSelectionOrder': members.index(i) + 1,
                'port': 0
            }) for i in members]

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

    def get_route_lists(self):
        """
        Get route lists
        :param mini: return a list of tuples of route list details
        :return: A list of dictionary's
        """
        try:
            return self.client.listRouteList(
                {'name': '%'}, returnedTags={'name': '', 'description': ''})['return']['routeList']
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
            return self.client.getRouteList(**args)
        except Fault as e:
            return e

    def add_route_list(self,
                       name,
                       description='',
                       cm_group_name='Default',
                       route_list_enabled='true',
                       run_on_all_nodes='false',
                       members=[]):

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
            'name': name,
            'description': description,
            'callManagerGroupName': cm_group_name,
            'routeListEnabled': route_list_enabled,
            'runOnEveryNode': run_on_all_nodes,
            'members': {'member': []},
        }

        if members:
            [req['members']['member'].append({
                'routeGroupName': i,
                'selectionOrder': members.index(i) + 1,
                'calledPartyTransformationMask': '',
                'callingPartyTransformationMask': '',
                'digitDiscardInstructionName': '',
                'callingPartyPrefixDigits': '',
                'prefixDigitsOut': '',
                'useFullyQualifiedCallingPartyNumber': 'Default',
                'callingPartyNumberingPlan': 'Cisco CallManager',
                'callingPartyNumberType': 'Cisco CallManager',
                'calledPartyNumberingPlan': 'Cisco CallManager',
                'calledPartyNumberType': 'Cisco CallManager',
            }) for i in members]

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

    def get_partitions(self):
        """
        Get partitions
        :param mini: return a list of tuples of partition details
        :return: A list of dictionary's
        """
        try:
            return self.client.listRoutePartition(
                {'name': '%'}, returnedTags={
                    'name': '', 'description': ''})['return']['routePartition']
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
            return self.client.getRoutePartition(**args)
        except Fault as e:
            return e

    def add_partition(self,
                      name,
                      description='',
                      time_schedule_name='All the time'):
        """
        Add a partition
        :param name: Name of the partition to add
        :param description: Partition description
        :param time_schedule_name: Name of the time schedule to use
        :return: result dictionary
        """
        try:
            return self.client.addRoutePartition({
                'name': name,
                'description': description,
                'timeScheduleIdName': time_schedule_name,
            })
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


    def get_calling_search_spaces(self):
        """
        Get calling search spaces
        :param mini: return a list of tuples of css details
        :return: A list of dictionary's
        """
        try:
            return self.client.listCss({'name': '%'}, returnedTags={'name': '', 'description': ''})['return']['css']
        except Fault as e:
            return e

    def get_calling_search_space(self, **css):
        """
        Get Calling search space details
        :param name: Calling search space name
        :param uuid: Calling search space uuid
        :return: result dictionary
        """
        try:
            return self.client.getCss(**css)
        except Fault as e:
            return e

    def add_calling_search_space(self,
                                 name,
                                 description='',
                                 members=[]):
        """
        Add a Calling search space
        :param name: Name of the CSS to add
        :param description: Calling search space description
        :param members: A list of partitions to add to the CSS
        :return: result dictionary
        """
        req = {
            'name': name,
            'description': description,
            'members': {'member': []},
        }
        if members:
            [req['members']['member'].append({
                'routePartitionName': i,
                'index': members.index(i) + 1,
            }) for i in members]
        
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

    def get_route_patterns(self):
        """
        Get route patterns
        :param mini: return a list of tuples of route pattern details
        :return: A list of dictionary's
        """
        try:
            return self.client.listRoutePattern({'pattern': '%'}, 
            returnedTags={'pattern': '', 'description': '', '_uuid': ''})['return']['routePattern']
        except Fault as e:
            return e

    def get_route_pattern(self, pattern='', uuid=''):
        """
        Get route pattern
        :param pattern: route pattern
        :param uuid: route pattern uuid
        :return: result dictionary
        """
        if uuid == '' and pattern != '':
        # Cant get pattern directly so get UUID first
            try:
                uuid = self.client.listRoutePattern({'pattern': pattern}, returnedTags={'uuid': ''})
            except Fault as e:
                return e
            if 'return' in uuid and uuid['return'] is not None:
                uuid = uuid['return']['routePattern'][0]['uuid']
                try:
                    return self.client.getRoutePattern(uuid=uuid)
                except Fault as e:
                    return e

        elif uuid != '' and pattern == '':
            try:
                return self.client.getRoutePattern(uuid=uuid)
            except Fault as e:
                return e

    def add_route_pattern(self,
                          pattern,
                          gateway='',
                          route_list='',
                          description='',
                          partition='',
                          blockEnable=False,
                          patternUrgency=False,
                          releaseClause='Call Rejected'):
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
            'pattern': pattern,
            'description': description,
            'destination': {},
            'routePartitionName': partition,
            'blockEnable': blockEnable,
            'releaseClause': releaseClause
        }

        if gateway == '' and route_list == '':
            return 'Either a gateway OR route list, is a required parameter'

        elif gateway != '' and route_list != '':
            return 'Enter a gateway OR route list, not both'

        elif gateway != '':
            req['destination'].update({'gatewayName': gateway})
        elif route_list != '':
            req['destination'].update({'routeListName': route_list})
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

    def get_media_resource_groups(self):
        """
        Get media resource groups
        :param mini: return a list of tuples of route pattern details
        :return: A list of dictionary's
        """
        try:
            return self.client.listMediaResourceGroup({'name': '%'}, 
            returnedTags={'name': '', 'description': ''})['return']['mediaResourceGroup']
        except Fault as e:
            return e

    def get_media_resource_group(self, media_resource_group):
        """
        Get a media resource group details
        :param media_resource_group: Media resource group name
        :return: result dictionary
        """
        try:
            return self.client.getMediaResourceGroup(name=media_resource_group)
        except Fault as e:
            return e

    def add_media_resource_group(self,
                                 media_resource_group,
                                 description='',
                                 multicast='false',
                                 members=[]):
        """
        Add a media resource group
        :param media_resource_group: Media resource group name
        :param description: Media resource description
        :param multicast: Mulicast enabled
        :param members: Media resource group members
        :return: result dictionary
        """
        req = {
            'name': media_resource_group,
            'description': description,
            'multicast': multicast,
            'members': {'member': []}
        }

        if members:
            [req['members']['member'].append({'deviceName': i}) for i in members]

        try:
            return self.client.addMediaResourceGroup(req)
        except Fault as e:
            return e

    def delete_media_resource_group(self, media_resource_group):
        """
        Delete a Media resource group
        :param media_resource_group: The name of the media resource group to delete
        :return: result dictionary
        """
        try:
            return self.client.removeMediaResourceGroup(name=media_resource_group)
        except Fault as e:
            return e

    def get_media_resource_group_lists(self):
        """
        Get media resource groups
        :param mini: return a list of tuples of route pattern details
        :return: A list of dictionary's
        """
        try:
            return self.client.listMediaResourceList({'name': '%'}, 
            returnedTags={'name': ''})['return']['mediaResourceList']
        except Fault as e:
            return e

    def get_media_resource_group_list(self, media_resource_group_list):
        """
        Get a media resource group list details
        :param media_resource_group_list: Media resource group list name
        :return: result dictionary
        """
        try:
            return self.client.getMediaResourceList(name=media_resource_group_list)
        except Fault as e:
            return e

    def add_media_resource_group_list(self, media_resource_group_list, members=[]):
        """
        Add a media resource group list
        :param media_resource_group_list: Media resource group list name
        :param members: A list of members
        :return:
        """
        req = {
            'name': media_resource_group_list,
            'members': {'member': []}
        }

        if members:
            [req['members']['member'].append({'order': members.index(i),
                                              'mediaResourceGroupName': i}) for i in members]
        try:
            return self.client.addMediaResourceList(req)
        except Fault as e:
            return e

    def delete_media_resource_group_list(self, media_resource_group_list):
        """
        Delete a Media resource group list
        :param media_resource_group_list: The name of the media resource group list to delete
        :return: result dictionary
        """
        try:
            return self.client.removeMediaResourceList(name=media_resource_group_list)
        except Fault as e:
            return e

    def get_directory_numbers(self):
        """
        Get directory numbers
        :param mini: return a list of tuples of directory number details
        :return: A list of dictionary's
        """
        try:
            return self.client.listLine({'pattern': '%'}, 
            returnedTags={'pattern': '', 'description': '', 'routePartitionName': ''})['return']['line']
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
            return self.client.getLine(**args)
        except Fault as e:
            return e

    def add_directory_number(self,
                             pattern,
                             partition='',
                             description='',
                             alerting_name='',
                             ascii_alerting_name='',
                             shared_line_css='',
                             aar_neighbourhood='',
                             call_forward_css='',
                             vm_profile_name='NoVoiceMail',
                             aar_destination_mask='',
                             call_forward_destination='',
                             forward_all_to_vm='false',
                             forward_all_destination='',
                             forward_to_vm='false'):
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
            return self.client.addLine({
                'pattern': pattern,
                'routePartitionName': partition,
                'description': description,
                'alertingName': alerting_name,
                'asciiAlertingName': ascii_alerting_name,
                'voiceMailProfileName': vm_profile_name,
                'shareLineAppearanceCssName': shared_line_css,
                'aarNeighborhoodName': aar_neighbourhood,
                'aarDestinationMask': aar_destination_mask,
                'callForwardAll': {
                    'forwardToVoiceMail': forward_all_to_vm,
                    'callingSearchSpaceName': call_forward_css,
                    'destination': forward_all_destination,
                },
                'callForwardBusy': {
                    'forwardToVoiceMail': forward_to_vm,
                    'callingSearchSpaceName': call_forward_css,
                    'destination': call_forward_destination,
                },
                'callForwardBusyInt': {
                    'forwardToVoiceMail': forward_to_vm,
                    'callingSearchSpaceName': call_forward_css,
                    'destination': call_forward_destination,
                },
                'callForwardNoAnswer': {
                    'forwardToVoiceMail': forward_to_vm,
                    'callingSearchSpaceName': call_forward_css,
                    'destination': call_forward_destination,
                },
                'callForwardNoAnswerInt': {
                    'forwardToVoiceMail': forward_to_vm,
                    'callingSearchSpaceName': call_forward_css,
                    'destination': call_forward_destination,
                },
                'callForwardNoCoverage': {
                    'forwardToVoiceMail': forward_to_vm,
                    'callingSearchSpaceName': call_forward_css,
                    'destination': call_forward_destination,
                },
                'callForwardNoCoverageInt': {
                    'forwardToVoiceMail': forward_to_vm,
                    'callingSearchSpaceName': call_forward_css,
                    'destination': call_forward_destination,
                },
                'callForwardOnFailure': {
                    'forwardToVoiceMail': forward_to_vm,
                    'callingSearchSpaceName': call_forward_css,
                    'destination': call_forward_destination,
                },
                'callForwardNotRegistered': {
                    'forwardToVoiceMail': forward_to_vm,
                    'callingSearchSpaceName': call_forward_css,
                    'destination': call_forward_destination,
                },
                'callForwardNotRegisteredInt': {
                    'forwardToVoiceMail': forward_to_vm,
                    'callingSearchSpaceName': call_forward_css,
                    'destination': call_forward_destination,
                }
        })
        except Fault as e:
            return e

    def delete_directory_number(self, uuid):
        """
        Delete a directory number
        :param directory_number: The name of the directory number to delete
        :return: result dictionary
        """
        try:
            return self.client.removeLine(uuid=uuid)
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

    def get_cti_route_points(self):
        """
        Get CTI route points
        :param mini: return a list of tuples of CTI route point details
        :return: A list of dictionary's
        """
        try:
            return self.client.listCtiRoutePoint({'name': '%'}, 
            returnedTags={'name': '', 'description': ''})['return']['ctiRoutePoint']
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
            return self.client.getCtiRoutePoint(**args)
        except Fault as e:
            return e

    def add_cti_route_point(self,
                            name,
                            description='',
                            device_pool='Default',
                            location='Hub_None',
                            common_device_config='',
                            css='',
                            product='CTI Route Point',
                            dev_class='CTI Route Point',
                            protocol='SCCP',
                            protocol_slide='User',
                            use_trusted_relay_point='Default',
                            lines=[]):
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
            'name': name,
            'description': description,
            'product': product,
            'class': dev_class,
            'protocol': protocol,
            'protocolSide': protocol_slide,
            'commonDeviceConfigName': common_device_config,
            'callingSearchSpaceName': css,
            'devicePoolName': device_pool,
            'locationName': location,
            'useTrustedRelayPoint': use_trusted_relay_point,
            'lines': {'line': []}
        }

        if lines:
            [req['lines']['line'].append({
                'index': lines.index(i) + 1,
                'dirn': {
                    'pattern': i[0], 
                    'routePartitionName': i[1]}
            }) for i in lines]

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

    def get_phones(self, first=1000, skip=0):
        """
        Get phone details
        :param mini: return a list of tuples of phone details
        :return: A list of dictionaries. If > 1000 records are returned, a list of list of dictionaries will be returned
        """
        paginated = []
        try:
            return self.client.listPhone(
                    {'name': '%'}, returnedTags={
                        'name': '',
                        'product': '',
                        'protocol': '',
                        'locationName': '',
                    }, first=first, skip=skip)['return']['phone']
        except Fault as e:
            return e

            if len(resp) >= 1000:
                skip=first+skip
                first+=first
                paginated.append(resp)
                self.get_phones(first=first, skip=skip)
            else:
                if first > 1000:
                    return paginated
                else:
                    return resp

    def get_phone(self, **args):
        """
        Get device profile parameters
        :param phone: profile name
        :return: result dictionary
        """
        try:
            return self.client.getPhone(**args)['return']['phone']
        except Fault as e:
            return e

    def add_phone(self,
                  name,
                  description='',
                  product='Cisco 7941',
                  device_pool='Default',
                  location='Hub_None',
                  phone_template='Standard 8861 SIP',
                  common_device_config='',
                  css='',
                  aar_css='',
                  subscribe_css='',
                  securityProfileName='',
                  lines=[],
                  dev_class='Phone',
                  protocol='SCCP',
                  softkey_template='Standard User',
                  enable_em='true',
                  em_service_name='Extension Mobility',
                  em_service_url=False,
                  em_url_button_enable=False,
                  em_url_button_index='1',
                  em_url_label='Press here to logon',
                  ehook_enable=1):
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

        req = {
            'name': name,
            'description': description,
            'product': product,
            'class': dev_class,
            'protocol': protocol,
            'commonDeviceConfigName': common_device_config,
            'softkeyTemplateName': softkey_template,
            'phoneTemplateName': phone_template,
            'devicePoolName': device_pool,
            'locationName': location,
            'enableExtensionMobility': enable_em,
            'callingSearchSpaceName': css,
            'automatedAlternateRoutingCssName': aar_css,
            'subscribeCallingSearchSpaceName': subscribe_css,
            'lines': {'line': []},
            'services': {'service': []},
            'vendorConfig': [{
                'ehookEnable': ehook_enable
            }]
        }

        if lines:
            [req['lines']['line'].append({
                'index': lines.index(i) + 1,
                'dirn': {
                    'pattern': i[0],
                    'routePartitionName': i[1]
                },
                'display': i[2],
                'displayAscii': i[3],
                'label': i[4],
                'e164Mask': i[5]
            }) for i in lines]

        if em_service_url:
            req['services']['service'].append([{
                'telecasterServiceName': em_service_name,
                'name': em_service_name,
                'url': 'http://{0}:8080/emapp/EMAppServlet?device=#DEVICENAME#&EMCC=#EMCC#'.format(self.cucm),
            }])

        if em_url_button_enable:
            req['services']['service'][0].update({'urlButtonIndex': em_url_button_index, 'urlLabel': em_url_label})

        try:
            resp = self.client.addPhone(req)
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

    def get_device_profiles(self):
        """
        Get device profile details
        :param mini: return a list of tuples of device profile details
        :return: A list of dictionary's
        """
        try:
            return self.client.listDeviceProfile(
                    {'name': '%'}, returnedTags={
                        'name': '',
                        'product': '',
                        'protocol': '',
                        'phoneTemplateName': '',
                    })['return']['deviceProfile']
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
            return self.client.getDeviceProfile(**args)
        except Fault as e:
            return e

    def add_device_profile(self,
                           profile,
                           description='',
                           product='Cisco 7962',
                           phone_template='Standard 7962G SCCP',
                           dev_class='Device Profile',
                           protocol='SCCP',
                           softkey_template='Standard User',
                           em_service_name='Extension Mobility',
                           lines=[]):
        """
        Add A Device profile for use with extension mobility
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

        req = {
            'name': profile,
            'description': description,
            'product': product,
            'class': dev_class,
            'protocol': protocol,
            'softkeyTemplateName': softkey_template,
            'phoneTemplateName': phone_template,
            'lines': {'line': []},
            'services': {'service': [{
                'telecasterServiceName': em_service_name,
                'name': em_service_name,
                'url': 'http://{0}:8080/emapp/EMAppServlet?device=#DEVICENAME#&EMCC=#EMCC#'.format(self.cucm),
            }]},
        }

        if lines:
            [req['lines']['line'].append({
                'index': lines.index(i) + 1,
                'dirn': {
                    'pattern': i[0],
                    'routePartitionName': i[1]
                },
                'display': i[2],
                'displayAscii': i[3],
                'label': i[4],
                'e164Mask': i[5]
            }) for i in lines]

        try:
            return self.client.addDeviceProfile(req)
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

    def update_device_profile(self,**args):
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

    def get_users(self):
        """
        Get users details
        :param mini: return a list of tuples of user details
        :return: A list of dictionary's
        """
        try:
            return self.client.listUser(
                    {'userid': '%'}, returnedTags={
                        'userid': '',
                        'firstName': '',
                        'lastName': '',
                    })['return']['user']
        except Fault as e:
            return e

    def get_user(self, user_id):
        """
        Get user parameters
        :param user_id: profile name
        :return: result dictionary
        """
        try:
            return self.client.getUser(userid=user_id)
        except Fault as e:
            return e

    def add_user(self,
                 user_id,
                 last_name,
                 first_name,
                 presenceGroupName='Standard Presence group'
                 ):
        """
        Add a user
        :param user_id: User ID of the user to add
        :param first_name: First name of the user to add
        :param last_name: Last name of the user to add
        :return: result dictionary
        """
        try:
            return self.client.addUser({
                'userid': user_id,
                'last_name': last_name,
                'first_name': first_name,
                'presenceGroupName': presenceGroupName
            })
        except Fault as e:
            return e

    def update_user(self, **args):
        """
        Update end user for credentials
        :param user_id: User ID
        :param password: Web interface password
        :param pin: Extension mobility PIN
        :return: result dictionary
        """
        try:
            return self.client.updateUser(**args)
        except Fault as e:
            return e

    def update_user_em(self,
                       user_id,
                       device_profile,
                       default_profile,
                       subscribe_css,
                       primary_extension):
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
        if 'return' in resp and resp['return'] is not None:
            uuid = resp['return']['deviceProfile']['uuid']
            try:
                return self.client.updateUser(
                    userid=user_id,
                    phoneProfiles={'profileName': {'_uuid': uuid}},
                    defaultProfile=default_profile,
                    subscribeCallingSearchSpaceName=subscribe_css,
                    primaryExtension={'pattern': primary_extension},
                    associatedGroups={'userGroup': {'name': 'Standard CCM End Users'}}
            )
            except Fault as e:
                return e
        else:
            return 'Device Profile not found for user'

    def update_user_credentials(self,
                                user_id,
                                password='',
                                pin=''):
        """
        Update end user for credentials
        :param user_id: User ID
        :param password: Web interface password
        :param pin: Extension mobility PIN
        :return: result dictionary
        """

        if password == '' and pin == '':
            return 'Password and/or Pin are required'

        elif password != '' and pin != '':
            try:
                return self.client.updateUser(userid=user_id,password=password,pin=pin)
            except Fault as e:
                return e

        elif password != '':
            try:
                return self.client.updateUser(userid=user_id,password=password)
            except Fault as e:
                return e

        elif pin != '':
            try:
                return self.client.updateUser(userid=user_id,pin=pin)
            except Fault as e:
                return e

    def delete_user(self, **args):
        """
        Delete a user
        :param user_id: The name of the user to delete
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
                {'pattern': '%'}, returnedTags={
                    'pattern': '', 
                    'description': '', 
                    '_uuid': '', 
                    'routePartitionName': '',
                    'callingSearchSpaceName': '',
                    'useCallingPartyPhoneMask': '',
                    'patternUrgency': '',
                    'provideOutsideDialtone': '',
                    'prefixDigitsOut': '',
                    'calledPartyTransformationMask': '',
                    'callingPartyTransformationMask': '',
                    'digitDiscardInstructionName': '',
                    'callingPartyPrefixDigits': '',
                    'provideOutsideDialtone': '' })['return']['transPattern']
        except Fault as e:
            return e


    def get_translation(self, pattern='', partition='', uuid=''):
        """
        Get translation pattern
        :param pattern: translation pattern to match
        :param partition: partition required if searching pattern
        :param uuid: translation pattern uuid
        :return: result dictionary
        """

        if pattern != '' and partition != '' and uuid == '':
            try:
                return self.client.getTransPattern(pattern=pattern,routePartitionName=partition,
                    returnedTags={
                        'pattern': '', 
                        'description': '', 
                        'routePartitionName': '',
                        'callingSearchSpaceName': '',
                        'useCallingPartyPhoneMask': '',
                        'patternUrgency': '',
                        'provideOutsideDialtone': '',
                        'prefixDigitsOut': '',
                        'calledPartyTransformationMask': '',
                        'callingPartyTransformationMask': '',
                        'digitDiscardInstructionName': '',
                        'callingPartyPrefixDigits': ''})
            except Fault as e:
                return e
        elif uuid != '' and pattern == '' and partition == '':
            try:
                return self.client.getTransPattern(uuid=uuid, 
                returnedTags={
                    'pattern': '', 
                    'description': '', 
                    'routePartitionName': '',
                    'callingSearchSpaceName': '',
                    'useCallingPartyPhoneMask': '',
                    'patternUrgency': '',
                    'provideOutsideDialtone': '',
                    'prefixDigitsOut': '',
                    'calledPartyTransformationMask': '',
                    'callingPartyTransformationMask': '',
                    'digitDiscardInstructionName': '',
                    'callingPartyPrefixDigits': ''})
            except Fault as e:
                return e
        else: 
            return "must specify either uuid OR pattern and partition"

    def add_translation(self,
                        pattern,
                        partition,
                        description='',
                        usage='Translation',
                        callingSearchSpaceName='',
                        useCallingPartyPhoneMask='Off',
                        patternUrgency='f',
                        provideOutsideDialtone='f',
                        prefixDigitsOut='',
                        calledPartyTransformationMask='',
                        callingPartyTransformationMask='',
                        digitDiscardInstructionName='',
                        callingPartyPrefixDigits='',
                        blockEnable='f',
                        routeNextHopByCgpn='f'
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
            return self.client.addTransPattern({
                'pattern': pattern, 
                'description': description,
                'routePartitionName': partition,
                'usage': usage,
                'callingSearchSpaceName': callingSearchSpaceName,
                'useCallingPartyPhoneMask': useCallingPartyPhoneMask,
                'patternUrgency': patternUrgency,
                'provideOutsideDialtone': provideOutsideDialtone,
                'prefixDigitsOut': prefixDigitsOut,
                'calledPartyTransformationMask': calledPartyTransformationMask,
                'callingPartyTransformationMask': callingPartyTransformationMask,
                'digitDiscardInstructionName': digitDiscardInstructionName,
                'callingPartyPrefixDigits': callingPartyPrefixDigits,
                'blockEnable': blockEnable
            })
        except Fault as e:
            return e

    def delete_translation(self, pattern='', partition='', uuid=''):
        """
        Delete a translation pattern
        :param pattern: The pattern of the route to delete
        :param partition: The name of the partition
        :param uuid: Required if pattern and partition are not specified
        :return: result dictionary
        """

        if pattern != '' and partition != '' and uuid == '':
            try:
                return self.client.removeTransPattern(pattern=pattern, routePartitionName=partition)
            except Fault as e:
                return e
        elif uuid != '' and pattern == '' and partition == '':
            try:
                return self.client.removeTransPattern(uuid=uuid)
            except Fault as e:
                return e
        else: 
            return "must specify either uuid OR pattern and partition"

    def update_translation(self,
                        pattern='',
                        partition='',
                        uuid='',
                        newPattern='',
                        description='',
                        newRoutePartitionName='',
                        callingSearchSpaceName='',
                        useCallingPartyPhoneMask='',
                        patternUrgency='',
                        provideOutsideDialtone='',
                        prefixDigitsOut='',
                        calledPartyTransformationMask='',
                        callingPartyTransformationMask='',
                        digitDiscardInstructionName='',
                        callingPartyPrefixDigits='',
                        blockEnable=''
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
        if description != '':
            args['description'] = description
        if pattern != '' and partition != '' and uuid == '':
            args['pattern'] = pattern
            args['routePartitionName'] = partition
        if pattern == '' and partition == '' and uuid != '':
            args['uuid'] = uuid
        if newPattern != '':
            args['newPattern'] = newPattern
        if newRoutePartitionName != '':
            args['newRoutePartitionName'] = newRoutePartitionName
        if callingSearchSpaceName != '':
            args['callingSearchSpaceName'] = callingSearchSpaceName
        if useCallingPartyPhoneMask != '':
            args['useCallingPartyPhoneMask'] = useCallingPartyPhoneMask
        if digitDiscardInstructionName != '':
            args['digitDiscardInstructionName'] = digitDiscardInstructionName
        if callingPartyTransformationMask != '':
            args['callingPartyTransformationMask'] = callingPartyTransformationMask            
        if calledPartyTransformationMask != '':
            args['calledPartyTransformationMask'] = calledPartyTransformationMask
        if patternUrgency != '':
            args['patternUrgency'] = patternUrgency
        if provideOutsideDialtone != '':
            args['provideOutsideDialtone'] = provideOutsideDialtone
        if prefixDigitsOut != '':
            args['prefixDigitsOut'] = prefixDigitsOut
        if callingPartyPrefixDigits != '':
            args['callingPartyPrefixDigits'] = callingPartyPrefixDigits
        if blockEnable != '':
            args['blockEnable'] = blockEnable
        try:
            return self.client.updateTransPattern(**args)
        except Fault as e:
            return e

    def list_route_plan(self, pattern=''):
        """
        List Route Plan
        :param pattern: Route Plan Contains Pattern
        :return: results dictionary
        """
        try:
            return self.client.listRoutePlan(
                {'dnOrPattern': '%'+pattern+'%'}, 
                returnedTags={
                    'dnOrPattern': '',
                    'partition': '',
                    'type': '',
                    'routeDetail': ''
                })
        except Fault as e:
            return e

    def list_route_plan_specific(self, pattern=''):
        """
        List Route Plan
        :param pattern: Route Plan Contains Pattern
        :return: results dictionary
        """
        try:
            return self.client.listRoutePlan({'dnOrPattern': pattern}, 
                returnedTags={
                    'dnOrPattern': '',
                    'partition': '',
                    'type': '',
                    'routeDetail': ''
            })
        except Fault as e:
            return e

    def get_called_party_xforms(self):
        """
        Get called party xforms
        :param mini: return a list of tuples of called party transformation pattern details
        :return: A list of dictionary's
        """
        try:
            return self.client.listCalledPartyTransformationPattern({'pattern': '%'}, 
                returnedTags={
                    'pattern': '', 'description': '', 'uuid': ''})['return']['calledPartyTransformationPattern']
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
            return self.client.getCalledPartyTransformationPattern(**args)
        except Fault as e:
            return e


    def add_called_party_xform(self, **args):
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
            return self.client.addCalledPartyTransformationPattern(**args)
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
            return self.client.listCallingPartyTransformationPattern({'pattern': '%'}, 
            returnedTags={
                'pattern': '', 'description': '', 'uuid': ''})['return']['callingPartyTransformationPattern']
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
            return self.client.getCallingPartyTransformationPattern(**args)
        except Fault as e:
            return e

    def add_calling_party_xform(self, **args):
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
            return self.client.addCallingPartyTransformationPattern(**args)
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
            return self.client.updateCallingPartyTransformationPattern(**args)
        except Fault as e:
            return e

    def get_sip_trunks(self):
        try:
            return self.client.listSipTrunk({'name': '%'}, 
                returnedTags={
                    'name': '',
                    'sipProfileName': '',
                    'callingSearchSpaceName': '',
                })['return']['sipTrunk']
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
            return self.client.getSipTrunk(**args)
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

    def update_dhcp_subnet(self, **args):
        """
        Update DHCP Subnet
        :param uuid:
        :param dhcpServerName:
        :param subnetIpAddress:
        :param subnetMask:
        :param domainName:
        :param tftpServerName:
        :param primaryTftpServerIpAddress:
        :param secondaryTftpServerIpAddress:
        :param primaryRouterIpAddress:
        :param primaryStartIpAddress:
        :param primaryEndIpAddress:
        :param secondaryStartIpAddress:
        :param secondaryEndIpAddress:

        :return:
        """
        try:
            return self.client.updateDhcpSubnet(**args)
        except Fault as e:
            return e

    def list_process_nodes(self):
        try:
            return self.client.listProcessNode({'name': '%', 'processNodeRole': 'CUCM Voice/Video'}, 
                returnedTags={'name': ''})['return']['processNode']
        except Fault as e:
            return e
        
    def add_call_manager_group(self, **args):
        """
        Add call manager group
        :param name: name of cmg
        :param members[]: array of mbmers
        :return: result dictionary
        """
        try:
            return self.client.addCallManagerGroup({**args})
        except Fault as e:
            return e