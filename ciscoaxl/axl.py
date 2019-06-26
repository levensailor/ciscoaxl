"""
Class to interface with cisco ucm axl api.
Author: Jeff Levensailor
Version: 1.0.0
Dependencies:
 - suds-jurko: https://bitbucket.org/jurko/suds

Links:
 - https://developer.cisco.com/site/axl/
"""

import sys
import pathlib
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
        wsdl = pathlib.PurePosixPath(f"{cwd}/schema/{cucm_version}/AXLAPI.wsdl").as_uri()
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

    def get_sip_profile(self, **args):
            """
            get_sip_profile parameters
            :param name: name
            :param uuid: uuid 
            :return: result dictionary
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.getSipProfile(**args)

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['sipProfile']
                return result

            except Fault as error:
                result['error'] = error
                return result

    def get_sip_profile_options(self, **args):
                """
                get_sip_profile_options parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getSipProfileOptions(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['sipProfile']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_sip_trunk_security_profile(self, **args):
                """
                get_sip_trunk_security_profile parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getSipTrunkSecurityProfile(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['sipTrunkSecurityProfile']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_time_period(self, **args):
                """
                get_time_period parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getTimePeriod(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['timePeriod']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_time_schedule(self, **args):
                """
                get_time_schedule parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getTimeSchedule(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['timeSchedule']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_tod_access(self, **args):
                """
                get_tod_access parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getTodAccess(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['todAccess']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_voice_mail_pilot(self, **args):
                """
                get_voice_mail_pilot parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getVoiceMailPilot(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['voiceMailPilot']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_process_node(self, **args):
                """
                get_process_node parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getProcessNode(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['processNode']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_caller_filter_list(self, **args):
                """
                get_caller_filter_list parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getCallerFilterList(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['callerFilterList']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_route_partition(self, **args):
                """
                get_route_partition parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getRoutePartition(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['routePartition']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_css(self, **args):
                """
                get_css parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getCss(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['css']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_call_manager(self, **args):
                """
                get_call_manager parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getCallManager(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['callManager']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_expressway_c_configuration(self, **args):
                """
                get_expressway_c_configuration parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getExpresswayCConfiguration(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['expresswayCConfiguration']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_media(self, **args):
                """
                get_media parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getMedia(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['mediaResourceGroup']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_media(self, **args):
                """
                get_media parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getMedia(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['mediaResourceList']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_region(self, **args):
                """
                get_region parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getRegion(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['region']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_aar_group(self, **args):
                """
                get_aar_group parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getAarGroup(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['aarGroup']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_physical_location(self, **args):
                """
                get_physical_location parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getPhysicalLocation(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['physicalLocation']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_customer(self, **args):
                """
                get_customer parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getCustomer(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['customer']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_route_group(self, **args):
                """
                get_route_group parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getRouteGroup(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['routeGroup']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_device_pool(self, **args):
                """
                get_device_pool parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getDevicePool(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['devicePool']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_device_mobility_group(self, **args):
                """
                get_device_mobility_group parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getDeviceMobilityGroup(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['deviceMobilityGroup']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_location(self, **args):
                """
                get_location parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getLocation(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['location']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_soft_key_template(self, **args):
                """
                get_soft_key_template parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getSoftKeyTemplate(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['softKeyTemplate']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_transcoder(self, **args):
                """
                get_transcoder parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getTranscoder(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['transcoder']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_common_device_config(self, **args):
                """
                get_common_device_config parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getCommonDeviceConfig(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['commonDeviceConfig']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get(self, **args):
                """
                get parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.get(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['resourcePriorityNamespace']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get(self, **args):
                """
                get parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.get(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['resourcePriorityNamespaceList']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_device_mobility(self, **args):
                """
                get_device_mobility parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getDeviceMobility(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['deviceMobility']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_cmc_info(self, **args):
                """
                get_cmc_info parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getCmcInfo(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['cmcInfo']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_credential_policy(self, **args):
                """
                get_credential_policy parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getCredentialPolicy(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['credentialPolicy']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_fac_info(self, **args):
                """
                get_fac_info parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getFacInfo(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['facInfo']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_hunt_list(self, **args):
                """
                get_hunt_list parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getHuntList(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['huntList']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_ivr_user_locale(self, **args):
                """
                get_ivr_user_locale parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getIvrUserLocale(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['ivrUserLocale']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_line_group(self, **args):
                """
                get_line_group parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getLineGroup(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['lineGroup']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_recording_profile(self, **args):
                """
                get_recording_profile parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getRecordingProfile(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['recordingProfile']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_route_filter(self, **args):
                """
                get_route_filter parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getRouteFilter(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['routeFilter']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_call_manager_group(self, **args):
                """
                get_call_manager_group parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getCallManagerGroup(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['callManagerGroup']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_user_group(self, **args):
                """
                get_user_group parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getUserGroup(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['userGroup']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_dial_plan(self, **args):
                """
                get_dial_plan parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getDialPlan(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['dialPlan']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_dial_plan_tag(self, **args):
                """
                get_dial_plan_tag parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getDialPlanTag(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['dialPlanTag']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_ddi(self, **args):
                """
                get_ddi parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getDdi(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['ddi']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_mobile_smart_client_profile(self, **args):
                """
                get_mobile_smart_client_profile parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getMobileSmartClientProfile(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['mobileSmartClientProfile']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_process_node_service(self, **args):
                """
                get_process_node_service parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getProcessNodeService(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['processNodeService']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_moh_audio_source(self, **args):
                """
                get_moh_audio_source parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getMohAudioSource(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['mohAudioSource']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_dhcp_server(self, **args):
                """
                get_dhcp_server parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getDhcpServer(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['dhcpServer']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_dhcp_subnet(self, **args):
                """
                get_dhcp_subnet parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getDhcpSubnet(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['dhcpSubnet']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_call_park(self, **args):
                """
                get_call_park parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getCallPark(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['callPark']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_directed_call_park(self, **args):
                """
                get_directed_call_park parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getDirectedCallPark(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['directedCallPark']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_meet_me(self, **args):
                """
                get_meet_me parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getMeetMe(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['meetMe']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_conference_now(self, **args):
                """
                get_conference_now parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getConferenceNow(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['conferenceNow']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_mobile_voice_access(self, **args):
                """
                get_mobile_voice_access parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getMobileVoiceAccess(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['mobileVoiceAccess']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_route_list(self, **args):
                """
                get_route_list parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getRouteList(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['routeList']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_user(self, **args):
                """
                get_user parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getUser(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['user']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_app_user(self, **args):
                """
                get_app_user parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getAppUser(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['appUser']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_sip_realm(self, **args):
                """
                get_sip_realm parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getSipRealm(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['sipRealm']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_phone_ntp(self, **args):
                """
                get_phone_ntp parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getPhoneNtp(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['phoneNtp']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_date_time_group(self, **args):
                """
                get_date_time_group parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getDateTimeGroup(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['dateTimeGroup']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_presence_group(self, **args):
                """
                get_presence_group parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getPresenceGroup(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['presenceGroup']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_geo_location(self, **args):
                """
                get_geo_location parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getGeoLocation(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['geoLocation']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_srst(self, **args):
                """
                get_srst parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getSrst(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['srst']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_mlpp_domain(self, **args):
                """
                get_mlpp_domain parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getMlppDomain(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['mlppDomain']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_cuma_server_security_profile(self, **args):
                """
                get_cuma_server_security_profile parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getCumaServerSecurityProfile(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['cumaServerSecurityProfile']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_application_server(self, **args):
                """
                get_application_server parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getApplicationServer(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['applicationServer']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_application_user_capf_profile(self, **args):
                """
                get_application_user_capf_profile parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getApplicationUserCapfProfile(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['applicationUserCapfProfile']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_end_user_capf_profile(self, **args):
                """
                get_end_user_capf_profile parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getEndUserCapfProfile(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['endUserCapfProfile']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_service_parameter(self, **args):
                """
                get_service_parameter parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getServiceParameter(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['serviceParameter']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_geo_location_filter(self, **args):
                """
                get_geo_location_filter parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getGeoLocationFilter(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['geoLocationFilter']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_voice_mail_profile(self, **args):
                """
                get_voice_mail_profile parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getVoiceMailProfile(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['voiceMailProfile']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_voice_mail_port(self, **args):
                """
                get_voice_mail_port parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getVoiceMailPort(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['voiceMailPort']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_gatekeeper(self, **args):
                """
                get_gatekeeper parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getGatekeeper(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['gatekeeper']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_phone_button_template(self, **args):
                """
                get_phone_button_template parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getPhoneButtonTemplate(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['phoneButtonTemplate']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_common_phone_config(self, **args):
                """
                get_common_phone_config parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getCommonPhoneConfig(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['commonPhoneConfig']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_message_waiting(self, **args):
                """
                get_message_waiting parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getMessageWaiting(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['messageWaiting']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_ip_phone_services(self, **args):
                """
                get_ip_phone_services parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getIpPhoneServices(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['ipPhoneServices']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_cti_route_point(self, **args):
                """
                get_cti_route_point parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getCtiRoutePoint(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['ctiRoutePoint']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_trans_pattern(self, **args):
                """
                get_trans_pattern parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getTransPattern(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['transPattern']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_trans_pattern_options(self, **args):
                """
                get_trans_pattern_options parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getTransPatternOptions(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['transPattern']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_calling_party_transformation_pattern(self, **args):
                """
                get_calling_party_transformation_pattern parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getCallingPartyTransformationPattern(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['callingPartyTransformationPattern']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_sip_route_pattern(self, **args):
                """
                get_sip_route_pattern parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getSipRoutePattern(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['sipRoutePattern']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_hunt_pilot(self, **args):
                """
                get_hunt_pilot parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getHuntPilot(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['huntPilot']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_route_pattern(self, **args):
                """
                get_route_pattern parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getRoutePattern(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['routePattern']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_application_dial_rules(self, **args):
                """
                get_application_dial_rules parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getApplicationDialRules(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['applicationDialRules']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_directory_lookup_dial_rules(self, **args):
                """
                get_directory_lookup_dial_rules parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getDirectoryLookupDialRules(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['directoryLookupDialRules']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_phone_security_profile(self, **args):
                """
                get_phone_security_profile parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getPhoneSecurityProfile(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['phoneSecurityProfile']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_sip_dial_rules(self, **args):
                """
                get_sip_dial_rules parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getSipDialRules(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['sipDialRules']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_conference_bridge(self, **args):
                """
                get_conference_bridge parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getConferenceBridge(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['conferenceBridge']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_annunciator(self, **args):
                """
                get_annunciator parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getAnnunciator(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['annunciator']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_interactive_voice(self, **args):
                """
                get_interactive_voice parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getInteractiveVoice(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['interactiveVoiceResponse']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_mtp(self, **args):
                """
                get_mtp parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getMtp(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['mtp']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_fixed_moh_audio_source(self, **args):
                """
                get_fixed_moh_audio_source parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getFixedMohAudioSource(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['fixedMohAudioSource']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_remote_destination_profile(self, **args):
                """
                get_remote_destination_profile parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getRemoteDestinationProfile(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['remoteDestinationProfile']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_line(self, **args):
                """
                get_line parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getLine(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['line']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_line_options(self, **args):
                """
                get_line_options parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getLineOptions(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['line']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_default_device_profile(self, **args):
                """
                get_default_device_profile parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getDefaultDeviceProfile(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['defaultDeviceProfile']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_h323_phone(self, **args):
                """
                get_h323_phone parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getH323Phone(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['h323Phone']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_moh_server(self, **args):
                """
                get_moh_server parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getMohServer(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['mohServer']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_h323_trunk(self, **args):
                """
                get_h323_trunk parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getH323Trunk(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['h323Trunk']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_phone(self, **args):
                """
                get_phone parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getPhone(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['phone']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_phone_options(self, **args):
                """
                get_phone_options parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getPhoneOptions(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['phone']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_h323_gateway(self, **args):
                """
                get_h323_gateway parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getH323Gateway(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['h323Gateway']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_device_profile(self, **args):
                """
                get_device_profile parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getDeviceProfile(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['deviceProfile']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_device_profile_options(self, **args):
                """
                get_device_profile_options parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getDeviceProfileOptions(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['deviceProfile']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_remote_destination(self, **args):
                """
                get_remote_destination parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getRemoteDestination(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['remoteDestination']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_vg224(self, **args):
                """
                get_vg224 parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getVg224(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['vg224']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_gateway(self, **args):
                """
                get_gateway parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getGateway(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['gateway']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_gateway_endpoint_analog_access(self, **args):
                """
                get_gateway_endpoint_analog_access parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getGatewayEndpointAnalogAccess(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['gatewayEndpointAnalogAccess']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_gateway_endpoint_digital_access_pri(self, **args):
                """
                get_gateway_endpoint_digital_access_pri parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getGatewayEndpointDigitalAccessPri(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['gatewayEndpointDigitalAccessPri']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_gateway_endpoint_digital_access_bri(self, **args):
                """
                get_gateway_endpoint_digital_access_bri parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getGatewayEndpointDigitalAccessBri(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['gatewayEndpointDigitalAccessBri']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_gateway_endpoint_digital_access_t1(self, **args):
                """
                get_gateway_endpoint_digital_access_t1 parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getGatewayEndpointDigitalAccessT1(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['gatewayEndpointDigitalAccessT1']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_cisco_catalyst600024_port_fxs_gateway(self, **args):
                """
                get_cisco_catalyst600024_port_fxs_gateway parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getCiscoCatalyst600024PortFXSGateway(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['ciscoCatalyst600024PortFXSGateway']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_cisco_catalyst6000_e1_vo_ip_gateway(self, **args):
                """
                get_cisco_catalyst6000_e1_vo_ip_gateway parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getCiscoCatalyst6000E1VoIPGateway(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['ciscoCatalyst6000E1VoIPGateway']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_cisco_catalyst6000_t1_vo_ip_gateway_pri(self, **args):
                """
                get_cisco_catalyst6000_t1_vo_ip_gateway_pri parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getCiscoCatalyst6000T1VoIPGatewayPri(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['ciscoCatalyst6000T1VoIPGatewayPri']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_cisco_catalyst6000_t1_vo_ip_gateway_t1(self, **args):
                """
                get_cisco_catalyst6000_t1_vo_ip_gateway_t1 parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getCiscoCatalyst6000T1VoIPGatewayT1(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['ciscoCatalyst6000T1VoIPGatewayT1']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_call_pickup_group(self, **args):
                """
                get_call_pickup_group parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getCallPickupGroup(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['callPickupGroup']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_geo_location_policy(self, **args):
                """
                get_geo_location_policy parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getGeoLocationPolicy(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['geoLocationPolicy']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_sip_trunk(self, **args):
                """
                get_sip_trunk parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getSipTrunk(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['sipTrunk']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_called_party_transformation_pattern(self, **args):
                """
                get_called_party_transformation_pattern parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getCalledPartyTransformationPattern(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['calledPartyTransformationPattern']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_external_call_control_profile(self, **args):
                """
                get_external_call_control_profile parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getExternalCallControlProfile(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['externalCallControlProfile']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_saf_security_profile(self, **args):
                """
                get_saf_security_profile parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getSafSecurityProfile(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['safSecurityProfile']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_saf_forwarder(self, **args):
                """
                get_saf_forwarder parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getSafForwarder(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['safForwarder']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_ccd_hosted_dn(self, **args):
                """
                get_ccd_hosted_dn parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getCcdHostedDN(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['ccdHostedDN']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_ccd_hosted_dn_group(self, **args):
                """
                get_ccd_hosted_dn_group parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getCcdHostedDNGroup(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['ccdHostedDNGroup']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_ccd_requesting_service(self, **args):
                """
                get_ccd_requesting_service parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getCcdRequestingService(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['ccdRequestingService']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_inter_cluster_service_profile(self, **args):
                """
                get_inter_cluster_service_profile parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getInterClusterServiceProfile(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['interClusterServiceProfile']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_remote_cluster(self, **args):
                """
                get_remote_cluster parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getRemoteCluster(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['remoteCluster']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_ccd_advertising_service(self, **args):
                """
                get_ccd_advertising_service parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getCcdAdvertisingService(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['ccdAdvertisingService']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_ldap_directory(self, **args):
                """
                get_ldap_directory parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getLdapDirectory(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['ldapDirectory']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_emcc_feature_config(self, **args):
                """
                get_emcc_feature_config parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getEmccFeatureConfig(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['emccFeatureConfig']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_saf_ccd_purge_block_learned_routes(self, **args):
                """
                get_saf_ccd_purge_block_learned_routes parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getSafCcdPurgeBlockLearnedRoutes(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['safCcdPurgeBlockLearnedRoutes']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_vpn_gateway(self, **args):
                """
                get_vpn_gateway parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getVpnGateway(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['vpnGateway']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_vpn_group(self, **args):
                """
                get_vpn_group parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getVpnGroup(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['vpnGroup']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_vpn_profile(self, **args):
                """
                get_vpn_profile parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getVpnProfile(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['vpnProfile']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_ime_server(self, **args):
                """
                get_ime_server parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getImeServer(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['imeServer']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_ime_route_filter_group(self, **args):
                """
                get_ime_route_filter_group parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getImeRouteFilterGroup(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['imeRouteFilterGroup']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_ime_route_filter_element(self, **args):
                """
                get_ime_route_filter_element parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getImeRouteFilterElement(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['imeRouteFilterElement']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_ime_client(self, **args):
                """
                get_ime_client parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getImeClient(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['imeClient']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_ime_enrolled_pattern(self, **args):
                """
                get_ime_enrolled_pattern parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getImeEnrolledPattern(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['imeEnrolledPattern']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_ime_enrolled_pattern_group(self, **args):
                """
                get_ime_enrolled_pattern_group parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getImeEnrolledPatternGroup(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['imeEnrolledPatternGroup']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_ime_exclusion_number(self, **args):
                """
                get_ime_exclusion_number parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getImeExclusionNumber(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['imeExclusionNumber']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_ime_exclusion_number_group(self, **args):
                """
                get_ime_exclusion_number_group parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getImeExclusionNumberGroup(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['imeExclusionNumberGroup']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_ime_firewall(self, **args):
                """
                get_ime_firewall parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getImeFirewall(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['imeFirewall']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_ime_e164_transformation(self, **args):
                """
                get_ime_e164_transformation parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getImeE164Transformation(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['imeE164Transformation']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_transformation_profile(self, **args):
                """
                get_transformation_profile parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getTransformationProfile(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['transformationProfile']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_fallback_profile(self, **args):
                """
                get_fallback_profile parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getFallbackProfile(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['fallbackProfile']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_ldap_filter(self, **args):
                """
                get_ldap_filter parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getLdapFilter(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['ldapFilter']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_tvs_certificate(self, **args):
                """
                get_tvs_certificate parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getTvsCertificate(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['tvsCertificate']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_feature_control_policy(self, **args):
                """
                get_feature_control_policy parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getFeatureControlPolicy(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['featureControlPolicy']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_mobility_profile(self, **args):
                """
                get_mobility_profile parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getMobilityProfile(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['mobilityProfile']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_enterprise_feature_access_configuration(self, **args):
                """
                get_enterprise_feature_access_configuration parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getEnterpriseFeatureAccessConfiguration(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['enterpriseFeatureAccessConfiguration']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_handoff_configuration(self, **args):
                """
                get_handoff_configuration parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getHandoffConfiguration(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['handoffConfiguration']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_sip_normalization_script(self, **args):
                """
                get_sip_normalization_script parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getSIPNormalizationScript(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['sIPNormalizationScript']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_custom_user_field(self, **args):
                """
                get_custom_user_field parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getCustomUserField(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['customUserField']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_gateway_sccp_endpoints(self, **args):
                """
                get_gateway_sccp_endpoints parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getGatewaySccpEndpoints(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['gatewaySccpEndpoints']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_lbm_group(self, **args):
                """
                get_lbm_group parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getLbmGroup(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['lbmGroup']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_announcement(self, **args):
                """
                get_announcement parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getAnnouncement(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['announcement']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_service_profile(self, **args):
                """
                get_service_profile parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getServiceProfile(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['serviceProfile']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_ldap_sync_custom_field(self, **args):
                """
                get_ldap_sync_custom_field parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getLdapSyncCustomField(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['ldapSyncCustomField']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_audio_codec_preference_list(self, **args):
                """
                get_audio_codec_preference_list parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getAudioCodecPreferenceList(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['audioCodecPreferenceList']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_uc_service(self, **args):
                """
                get_uc_service parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getUcService(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['ucService']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_lbm_hub_group(self, **args):
                """
                get_lbm_hub_group parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getLbmHubGroup(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['lbmHubGroup']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_imported_directory_uri_catalogs(self, **args):
                """
                get_imported_directory_uri_catalogs parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getImportedDirectoryUriCatalogs(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['importedDirectoryUriCatalogs']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_voh_server(self, **args):
                """
                get_voh_server parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getVohServer(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['vohServer']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_sdp_transparency_profile(self, **args):
                """
                get_sdp_transparency_profile parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getSdpTransparencyProfile(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['sdpTransparencyProfile']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_feature_group_template(self, **args):
                """
                get_feature_group_template parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getFeatureGroupTemplate(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['featureGroupTemplate']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_dir_number_alias_lookupand_sync(self, **args):
                """
                get_dir_number_alias_lookupand_sync parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getDirNumberAliasLookupandSync(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['dirNumberAliasLookupandSync']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_local_route_group(self, **args):
                """
                get_local_route_group parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getLocalRouteGroup(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['localRouteGroup']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_advertised_patterns(self, **args):
                """
                get_advertised_patterns parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getAdvertisedPatterns(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['advertisedPatterns']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_blocked_learned_patterns(self, **args):
                """
                get_blocked_learned_patterns parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getBlockedLearnedPatterns(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['blockedLearnedPatterns']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_cca_profiles(self, **args):
                """
                get_cca_profiles parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getCCAProfiles(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['cCAProfiles']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_universal_device_template(self, **args):
                """
                get_universal_device_template parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getUniversalDeviceTemplate(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['universalDeviceTemplate']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_user_profile_provision(self, **args):
                """
                get_user_profile_provision parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getUserProfileProvision(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['userProfileProvision']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_presence_redundancy_group(self, **args):
                """
                get_presence_redundancy_group parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getPresenceRedundancyGroup(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['presenceRedundancyGroup']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_wifi_hotspot(self, **args):
                """
                get_wifi_hotspot parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getWifiHotspot(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['wifiHotspot']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_wlan_profile_group(self, **args):
                """
                get_wlan_profile_group parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getWlanProfileGroup(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['wlanProfileGroup']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_wlan_profile(self, **args):
                """
                get_wlan_profile parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getWLANProfile(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['wLANProfile']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_universal_line_template(self, **args):
                """
                get_universal_line_template parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getUniversalLineTemplate(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['universalLineTemplate']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_network_access_profile(self, **args):
                """
                get_network_access_profile parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getNetworkAccessProfile(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['networkAccessProfile']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_licensed_user(self, **args):
                """
                get_licensed_user parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getLicensedUser(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['licensedUser']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_http_profile(self, **args):
                """
                get_http_profile parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getHttpProfile(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['httpProfile']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_elin_group(self, **args):
                """
                get_elin_group parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getElinGroup(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['elinGroup']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_secure_config(self, **args):
                """
                get_secure_config parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getSecureConfig(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['secureConfig']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_registration_dynamic(self, **args):
                """
                get_registration_dynamic parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getRegistrationDynamic(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['registrationDynamic']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_infrastructure_device(self, **args):
                """
                get_infrastructure_device parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getInfrastructureDevice(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['infrastructureDevice']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_ldap_search(self, **args):
                """
                get_ldap_search parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getLdapSearch(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['ldapSearch']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_wireless_access_point_controllers(self, **args):
                """
                get_wireless_access_point_controllers parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getWirelessAccessPointControllers(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['wirelessAccessPointControllers']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_device_defaults(self, **args):
                """
                get_device_defaults parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getDeviceDefaults(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['deviceDefaults']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_mra_service_domain(self, **args):
                """
                get_mra_service_domain parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getMraServiceDomain(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['mraServiceDomain']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_os_version(self, **args):
                """
                get_os_version parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getOSVersion(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['os']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_mobility(self, **args):
                """
                get_mobility parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getMobility(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['mobility']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_enterprise_phone_config(self, **args):
                """
                get_enterprise_phone_config parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getEnterprisePhoneConfig(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['enterprisePhoneConfig']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_ldap_system(self, **args):
                """
                get_ldap_system parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getLdapSystem(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['ldapSystem']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_ldap_authentication(self, **args):
                """
                get_ldap_authentication parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getLdapAuthentication(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['ldapAuthentication']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_ccm_version(self, **args):
                """
                get_ccm_version parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getCCMVersion(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['componentVersion']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_fallback_feature_config(self, **args):
                """
                get_fallback_feature_config parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getFallbackFeatureConfig(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['fallbackFeatureConfig']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_ime_learned_routes(self, **args):
                """
                get_ime_learned_routes parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getImeLearnedRoutes(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['imeLearnedRoutes']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_ime_feature_config(self, **args):
                """
                get_ime_feature_config parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getImeFeatureConfig(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['imeFeatureConfig']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_app_server_info(self, **args):
                """
                get_app_server_info parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getAppServerInfo(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['appServerInfo']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_soft_key_set(self, **args):
                """
                get_soft_key_set parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getSoftKeySet(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['softKeySet']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_syslog_configuration(self, **args):
                """
                get_syslog_configuration parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getSyslogConfiguration(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['syslogConfiguration']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_ils_config(self, **args):
                """
                get_ils_config parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getIlsConfig(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['ilsConfig']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_snmp_community_string(self, **args):
                """
                get_snmp_community_string parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getSNMPCommunityString(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['SNMPCommunityString']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_snmp_user(self, **args):
                """
                get_snmp_user parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getSNMPUser(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['SNMPUser']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_snmpmib2_list(self, **args):
                """
                get_snmpmib2_list parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getSNMPMIB2List(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['SNMPMIB2List']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_billing_server(self, **args):
                """
                get_billing_server parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getBillingServer(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['billingServer']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_ccd_feature_config(self, **args):
                """
                get_ccd_feature_config parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getCcdFeatureConfig(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['ccdFeatureConfig']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_page_layout_preferences(self, **args):
                """
                get_page_layout_preferences parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getPageLayoutPreferences(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['pageLayoutPreferences']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_credential_policy_default(self, **args):
                """
                get_credential_policy_default parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getCredentialPolicyDefault(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['credentialPolicyDefault']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_smart_license_status(self, **args):
                """
                get_smart_license_status parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getSmartLicenseStatus(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['SmartLicensing']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_smart_license_status(self, **args):
                """
                get_smart_license_status parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getSmartLicenseStatus(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['Registration']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_smart_license_status(self, **args):
                """
                get_smart_license_status parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getSmartLicenseStatus(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['Authorization']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result
                
    def get_smart_license_status(self, **args):
                """
                get_smart_license_status parameters
                :param name: name
                :param uuid: uuid 
                :return: result dictionary
                """
                result = {
                    'success': False,
                    'response': '',
                    'error': '',
                }
                try:
                    resp = self.client.getSmartLicenseStatus(**args)

                    if resp['return']:
                        result['success'] = True
                        result['response'] = resp['return']['LicenseStatus']
                    return result

                except Fault as error:
                    result['error'] = error
                    return result

    def do_authenticate_user(self, **args):
        """
        do_authenticate_user parameters
        :param userid: required
        :param password: password or pin required
        :param pin: password or pin required
        :return: result dictionary
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }
        try:
            resp = self.client.doAuthenticateUser(**args)
            if resp['return']:
                result['success'] = True
                result['response'] = resp['return']['userAuthenticated']
            return result

        except Fault as error:
            result['error'] = error
            return result

    def do_device_login(self, **args):
        """
        do_device_login parameters
        :param deviceName: The name or uuid of the phone that is being logged-into. Not nullable.
        :param loginDuration: The duration of the login. Not nullable.
        :param profileName: The name or uuid of the Device Profile to be used. Not nullable.
        :param userID: The LDAP RN of the user that is to be logged-into the phone. Not nullable.
        :return: result dictionary
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }
        try:
            resp = self.client.doDeviceLogin(**args)
            if resp['return']:
                result['success'] = True
                result['response'] = resp['return']
            return result

        except Fault as error:
            result['error'] = error
            return result

    def do_device_logout(self, **args):
        """
        do_device_logout parameters
        :param deviceName: The name or uuid of the phone that is being logged-out. Not nullable.
        :return: result dictionary
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }
        try:
            resp = self.client.doDeviceLogout(**args)
            if resp['return']:
                result['success'] = True
                result['response'] = resp['return']
            return result

        except Fault as error:
            result['error'] = error
            return result

    def do_device_reset(self, **args):
        """
        do_device_reset parameters
        :param deviceName: The name or UUID of the device to performs a reset on. Not nullable.
        :param isHardReset: True performs a hard reset. False performs a soft reset. Not nullable.
        :return: result dictionary
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }
        try:
            resp = self.client.doDeviceReset(**args)
            if resp['return']:
                result['success'] = True
                result['response'] = resp['return']
            return result

        except Fault as error:
            result['error'] = error
            return result

    def do_ldap_sync(self, **args):
        """
        do_ldap_sync parameters
        :param name: The Config Name of the Ldap Directory.
        :param uuid: The UUID of the Ldap Directory.
        :param sync: rue means start sync, false means cancel the sync which is currently under process
        :return: result dictionary
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }
        try:
            resp = self.client.doLdapSync(**args)
            if resp['return']:
                result['success'] = True
                result['response'] = resp['return']
            return result

        except Fault as error:
            result['error'] = error
            return result

    def do_change_dnd_status(self, **args):
        """
        do_change_dnd_status parameters
        :param userID: The userID of the User.
        :param uuid: The UUID of the Device.
        :param dndStatus: True means set dndStatus for device as true, false means set dndStatus for device as false
        :return: result dictionary
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }
        try:
            resp = self.client.doChangeDNDStatus(**args)
            if resp['return']:
                result['success'] = True
                result['response'] = resp['return']
            return result

        except Fault as error:
            result['error'] = error
            return result

    def execute_sql_query(self, query):
        """
        execute sql query parameters
        :param query: The SQL QUERY command
        :return: result dictionary
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }
        try:
            resp = self.client.executeSQLQuery(query)
            if resp['return']:
                result['success'] = True
                result['response'] = resp['return']
            return result

        except Fault as error:
            result['error'] = error
            return result

    def execute_sql_update(self, update):
        """
        execute sql update parameters
        :param update: The SQL UPDATE command
        :return: result dictionary
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }
        try:
            resp = self.client.executeSQLUpdate(update)
            if resp['return']:
                result['success'] = True
                result['response'] = resp['return']
            return result

        except Fault as error:
            result['error'] = error
            return result

    def remove_voice_mail_pilot(self, **args):
        """
        remove_voice_mail_pilot parameters
        :param uuid: uuid
        :param dirn: dirn
        :param cssName: cssName
        :return: result dictionary
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }
        try:
            resp = self.client.removeVoiceMailPilot(**args)

            if resp['return']:
                result['success'] = True
                result['response'] = resp['return']
            return result

        except Fault as error:
            result['error'] = error
            return result
        
    def remove_dhcp_subnet(self, **args):
        """
        remove_dhcp_subnet parameters
        :param uuid: uuid
        :param dhcpServerName: dhcpServerName
        :param subnetIpAddress: subnetIpAddress
        :return: result dictionary
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }
        try:
            resp = self.client.removeDhcpSubnet(**args)

            if resp['return']:
                result['success'] = True
                result['response'] = resp['return']
            return result

        except Fault as error:
            result['error'] = error
            return result
        
    def remove_call_park(self, **args):
        """
        remove_call_park parameters
        :param uuid: uuid
        :param pattern: pattern
        :param routePartitionName: routePartitionName
        :return: result dictionary
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }
        try:
            resp = self.client.removeCallPark(**args)

            if resp['return']:
                result['success'] = True
                result['response'] = resp['return']
            return result

        except Fault as error:
            result['error'] = error
            return result
        
    def remove_directed_call_park(self, **args):
        """
        remove_directed_call_park parameters
        :param uuid: uuid
        :param pattern: pattern
        :param routePartitionName: routePartitionName
        :return: result dictionary
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }
        try:
            resp = self.client.removeDirectedCallPark(**args)

            if resp['return']:
                result['success'] = True
                result['response'] = resp['return']
            return result

        except Fault as error:
            result['error'] = error
            return result
        
    def remove_meet_me(self, **args):
        """
        remove_meet_me parameters
        :param uuid: uuid
        :param pattern: pattern
        :param routePartitionName: routePartitionName
        :return: result dictionary
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }
        try:
            resp = self.client.removeMeetMe(**args)

            if resp['return']:
                result['success'] = True
                result['response'] = resp['return']
            return result

        except Fault as error:
            result['error'] = error
            return result
        
    def remove_conference_now(self, **args):
        """
        remove_conference_now parameters
        :param uuid: uuid
        :param conferenceNowNumber: conferenceNowNumber
        :param routePartitionName: routePartitionName
        :return: result dictionary
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }
        try:
            resp = self.client.removeConferenceNow(**args)

            if resp['return']:
                result['success'] = True
                result['response'] = resp['return']
            return result

        except Fault as error:
            result['error'] = error
            return result
        
    def remove_phone_ntp(self, **args):
        """
        remove_phone_ntp parameters
        :param uuid: uuid
        :param ipAddress: ipAddress
        :param ipv6Address: ipv6Address
        :return: result dictionary
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }
        try:
            resp = self.client.removePhoneNtp(**args)

            if resp['return']:
                result['success'] = True
                result['response'] = resp['return']
            return result

        except Fault as error:
            result['error'] = error
            return result
        
    def remove_message_waiting(self, **args):
        """
        remove_message_waiting parameters
        :param uuid: uuid
        :param pattern: pattern
        :param routePartitionName: routePartitionName
        :return: result dictionary
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }
        try:
            resp = self.client.removeMessageWaiting(**args)

            if resp['return']:
                result['success'] = True
                result['response'] = resp['return']
            return result

        except Fault as error:
            result['error'] = error
            return result
        
    def remove_trans_pattern(self, **args):
        """
        remove_trans_pattern parameters
        :param uuid: uuid
        :param pattern: pattern
        :param routePartitionName: routePartitionName
        :param dialPlanName: dialPlanName
        :param routeFilterName: routeFilterName
        :return: result dictionary
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }
        try:
            resp = self.client.removeTransPattern(**args)

            if resp['return']:
                result['success'] = True
                result['response'] = resp['return']
            return result

        except Fault as error:
            result['error'] = error
            return result
        
    def remove_calling_party_transformation_pattern(self, **args):
        """
        remove_calling_party_transformation_pattern parameters
        :param uuid: uuid
        :param pattern: pattern
        :param routePartitionName: routePartitionName
        :param dialPlanName: dialPlanName
        :param routeFilterName: routeFilterName
        :return: result dictionary
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }
        try:
            resp = self.client.removeCallingPartyTransformationPattern(**args)

            if resp['return']:
                result['success'] = True
                result['response'] = resp['return']
            return result

        except Fault as error:
            result['error'] = error
            return result
        
    def remove_sip_route_pattern(self, **args):
        """
        remove_sip_route_pattern parameters
        :param uuid: uuid
        :param pattern: pattern
        :param routePartitionName: routePartitionName
        :return: result dictionary
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }
        try:
            resp = self.client.removeSipRoutePattern(**args)

            if resp['return']:
                result['success'] = True
                result['response'] = resp['return']
            return result

        except Fault as error:
            result['error'] = error
            return result
        
    def remove_hunt_pilot(self, **args):
        """
        remove_hunt_pilot parameters
        :param uuid: uuid
        :param pattern: pattern
        :param routePartitionName: routePartitionName
        :return: result dictionary
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }
        try:
            resp = self.client.removeHuntPilot(**args)

            if resp['return']:
                result['success'] = True
                result['response'] = resp['return']
            return result

        except Fault as error:
            result['error'] = error
            return result
        
    def remove_route_pattern(self, **args):
        """
        remove_route_pattern parameters
        :param uuid: uuid
        :param pattern: pattern
        :param routePartitionName: routePartitionName
        :param dialPlanName: dialPlanName
        :param routeFilterName: routeFilterName
        :return: result dictionary
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }
        try:
            resp = self.client.removeRoutePattern(**args)

            if resp['return']:
                result['success'] = True
                result['response'] = resp['return']
            return result

        except Fault as error:
            result['error'] = error
            return result
        
    def remove_line(self, **args):
        """
        remove_line parameters
        :param uuid: uuid
        :param pattern: pattern
        :param routePartitionName: routePartitionName
        :return: result dictionary
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }
        try:
            resp = self.client.removeLine(**args)

            if resp['return']:
                result['success'] = True
                result['response'] = resp['return']
            return result

        except Fault as error:
            result['error'] = error
            return result
        
    def remove_call_pickup_group(self, **args):
        """
        remove_call_pickup_group parameters
        :param uuid: uuid
        :param pattern: pattern
        :param routePartitionName: routePartitionName
        :return: result dictionary
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }
        try:
            resp = self.client.removeCallPickupGroup(**args)

            if resp['return']:
                result['success'] = True
                result['response'] = resp['return']
            return result

        except Fault as error:
            result['error'] = error
            return result
        
    def remove_called_party_transformation_pattern(self, **args):
        """
        remove_called_party_transformation_pattern parameters
        :param uuid: uuid
        :param pattern: pattern
        :param routePartitionName: routePartitionName
        :param dialPlanName: dialPlanName
        :param routeFilterName: routeFilterName
        :return: result dictionary
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }
        try:
            resp = self.client.removeCalledPartyTransformationPattern(**args)

            if resp['return']:
                result['success'] = True
                result['response'] = resp['return']
            return result

        except Fault as error:
            result['error'] = error
            return result
        
    def remove_saf_ccd_purge_block_learned_routes(self, **args):
        """
        remove_saf_ccd_purge_block_learned_routes parameters
        :param uuid: uuid
        :param learnedPattern: learnedPattern
        :param learnedPatternPrefix: learnedPatternPrefix
        :param callControlIdentity: callControlIdentity
        :param ipAddress: ipAddress
        :return: result dictionary
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }
        try:
            resp = self.client.removeSafCcdPurgeBlockLearnedRoutes(**args)

            if resp['return']:
                result['success'] = True
                result['response'] = resp['return']
            return result

        except Fault as error:
            result['error'] = error
            return result
        
    def remove_enterprise_feature_access_configuration(self, **args):
        """
        remove_enterprise_feature_access_configuration parameters
        :param uuid: uuid
        :param pattern: pattern
        :param routePartitionName: routePartitionName
        :return: result dictionary
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }
        try:
            resp = self.client.removeEnterpriseFeatureAccessConfiguration(**args)

            if resp['return']:
                result['success'] = True
                result['response'] = resp['return']
            return result

        except Fault as error:
            result['error'] = error
            return result
        
    def remove_handoff_configuration(self, **args):
        """
        remove_handoff_configuration parameters
        :param uuid: uuid
        :param pattern: pattern
        :param routePartitionName: routePartitionName
        :return: result dictionary
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }
        try:
            resp = self.client.removeHandoffConfiguration(**args)

            if resp['return']:
                result['success'] = True
                result['response'] = resp['return']
            return result

        except Fault as error:
            result['error'] = error
            return result
        
    def remove_ldap_sync_custom_field(self, **args):
        """
        remove_ldap_sync_custom_field parameters
        :param uuid: uuid
        :param ldapConfigurationName: ldapConfigurationName
        :param customUserField: customUserField
        :return: result dictionary
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }
        try:
            resp = self.client.removeLdapSyncCustomField(**args)

            if resp['return']:
                result['success'] = True
                result['response'] = resp['return']
            return result

        except Fault as error:
            result['error'] = error
            return result

    def list_sip_profile(self, name=''):
            """
            list_sip_profile parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listSipProfile(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'defaultTelephonyEventPayloadType': '', 'redirectByApplication': '', 'ringing180': '', 'timerInvite': '', 'timerRegisterDelta': '', 'timerRegister': '', 'timerT1': '', 'timerT2': '', 'retryInvite': '', 'retryNotInvite': '', 'startMediaPort': '', 'stopMediaPort': '', 'callpickupListUri': '', 'callpickupGroupUri': '', 'meetmeServiceUrl': '', 'userInfo': '', 'dtmfDbLevel': '', 'callHoldRingback': '', 'anonymousCallBlock': '', 'callerIdBlock': '', 'dndControl': '', 'telnetLevel': '', 'timerKeepAlive': '', 'timerSubscribe': '', 'timerSubscribeDelta': '', 'maxRedirects': '', 'timerOffHookToFirstDigit': '', 'callForwardUri': '', 'abbreviatedDialUri': '', 'confJointEnable': '', 'rfc2543Hold': '', 'semiAttendedTransfer': '', 'enableVad': '', 'stutterMsgWaiting': '', 'callStats': '', 't38Invite': '', 'faxInvite': '', 'rerouteIncomingRequest': '', 'resourcePriorityNamespaceListName': '', 'enableAnatForEarlyOfferCalls': '', 'rsvpOverSip': '', 'fallbackToLocalRsvp': '', 'sipRe11XxEnabled': '', 'gClear': '', 'sendRecvSDPInMidCallInvite': '', 'enableOutboundOptionsPing': '', 'optionsPingIntervalWhenStatusOK': '', 'optionsPingIntervalWhenStatusNotOK': '', 'deliverConferenceBridgeIdentifier': '', 'sipOptionsRetryCount': '', 'sipOptionsRetryTimer': '', 'sipBandwidthModifier': '', 'enableUriOutdialSupport': '', 'userAgentServerHeaderInfo': '', 'allowPresentationSharingUsingBfcp': '', 'scriptParameters': '', 'isScriptTraceEnabled': '', 'sipNormalizationScript': '', 'allowiXApplicationMedia': '', 'dialStringInterpretation': '', 'acceptAudioCodecPreferences': '', 'mlppUserAuthorization': '', 'isAssuredSipServiceEnabled': '', 'resourcePriorityNamespace': '', 'useCallerIdCallerNameinUriOutgoingRequest': '', 'callingLineIdentification': '', 'rejectAnonymousIncomingCall': '', 'callpickupUri': '', 'rejectAnonymousOutgoingCall': '', 'videoCallTrafficClass': '', 'sdpTransparency': '', 'allowMultipleCodecs': '', 'sipSessionRefreshMethod': '', 'earlyOfferSuppVoiceCall': '', 'cucmVersionInSipHeader': '', 'confidentialAccessLevelHeaders': '', 'destRouteString': '', 'inactiveSDPRequired': '', 'allowRRAndRSBandwidthModifier': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['sipProfile']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_sip_trunk_security_profile(self, name=''):
            """
            list_sip_trunk_security_profile parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listSipTrunkSecurityProfile(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'securityMode': '', 'incomingTransport': '', 'outgoingTransport': '', 'digestAuthentication': '', 'noncePolicyTime': '', 'x509SubjectName': '', 'incomingPort': '', 'applLevelAuthentication': '', 'acceptPresenceSubscription': '', 'acceptOutOfDialogRefer': '', 'acceptUnsolicitedNotification': '', 'allowReplaceHeader': '', 'transmitSecurityStatus': '', 'sipV150OutboundSdpOfferFiltering': '', 'allowChargingHeader': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['sipTrunkSecurityProfile']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_time_period(self, name=''):
            """
            list_time_period parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listTimePeriod(
                    {'name': '%'+name}, returnedTags={'name': '', 'startTime': '', 'endTime': '', 'startDay': '', 'endDay': '', 'monthOfYear': '', 'dayOfMonth': '', 'description': '', 'isPublished': '', 'todOwnerIdName': '', 'dayOfMonthEnd': '', 'monthOfYearEnd': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['timePeriod']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_time_schedule(self, name=''):
            """
            list_time_schedule parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listTimeSchedule(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'isPublished': '', 'timeScheduleCategory': '', 'todOwnerIdName': '', 'timePeriodName': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['timeSchedule']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_tod_access(self, name=''):
            """
            list_tod_access parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            :param ownerIdName: ownerIdName
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listTodAccess(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'ownerIdName': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['todAccess']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_voice_mail_pilot(self, name=''):
            """
            list_voice_mail_pilot parameters
            :param uuid: uuid
            :param dirn: dirn
            :param description: description
            :param cssName: cssName
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listVoiceMailPilot(
                    {'name': '%'+name}, returnedTags={'dirn': '', 'description': '', 'cssName': '', 'isDefault': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['voiceMailPilot']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_process_node(self, name=''):
            """
            list_process_node parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            :param processNodeRole: processNodeRole
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listProcessNode(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'mac': '', 'ipv6Name': '', 'nodeUsage': '', 'lbmHubGroup': '', 'processNodeRole': '', 'processNodeName': '', 'service': '', 'traceLevel': '', 'userCategories': '', 'enable': '', 'numFiles': '', 'maxFileSize': '', 'isActive': '', 'lbmAssignedServices': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['processNode']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_caller_filter_list(self, name=''):
            """
            list_caller_filter_list parameters
            :param uuid: uuid
            :param name: name
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listCallerFilterList(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'isAllowedType': '', 'endUserIdName': '', 'DnMask': '', 'callerFilterMask': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['callerFilterList']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_route_partition(self, name=''):
            """
            list_route_partition parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listRoutePartition(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'dialPlanWizardGenId': '', 'timeScheduleIdName': '', 'useOriginatingDeviceTimeZone': '', 'timeZone': '', 'partitionUsage': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['routePartition']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_css(self, name=''):
            """
            list_css parameters
            :param uuid: uuid
            :param description: description
            :param partitionUsage: partitionUsage
            :param name: name
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listCss(
                    {'name': '%'+name}, returnedTags={'description': '', 'clause': '', 'dialPlanWizardGenId': '', 'partitionUsage': '', 'name': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['css']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_call_manager(self, name=''):
            """
            list_call_manager parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listCallManager(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'autoRegistration': '', 'processNodeName': '', 'lbmGroup': '', 'tftpDefault': '', 'callManagerName': '', 'priority': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['callManager']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_expressway_c_configuration(self, name=''):
            """
            list_expressway_c_configuration parameters
            :param uuid: uuid
            :param HostNameOrIP: HostNameOrIP
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listExpresswayCConfiguration(
                    {'name': '%'+name}, returnedTags={'HostNameOrIP': '', 'description': '', 'X509SubjectNameorSubjectAlternateName': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['expresswayCConfiguration']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_media_resource_group(self, name=''):
            """
            list_media_resource_group parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listMediaResourceGroup(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'multicast': '', 'deviceName': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['None']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_media_resource_list(self, name=''):
            """
            list_media_resource_list parameters
            :param uuid: uuid
            :param name: name
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listMediaResourceList(
                    {'name': '%'+name}, returnedTags={'name': '', 'clause': '', 'mediaResourceGroupName': '', 'order': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['None']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_region(self, name=''):
            """
            list_region parameters
            :param uuid: uuid
            :param name: name
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listRegion(
                    {'name': '%'+name}, returnedTags={'name': '', 'defaultCodec': '', 'bandwidth': '', 'videoBandwidth': '', 'regionAName': '', 'regionBName': '', 'codecPreference': '', 'regionName': '', 'lossyNetwork': '', 'immersiveVideoBandwidth': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['region']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_aar_group(self, name=''):
            """
            list_aar_group parameters
            :param uuid: uuid
            :param name: name
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listAarGroup(
                    {'name': '%'+name}, returnedTags={'name': '', 'prefixDigit': '', 'aarGroupFromName': '', 'aarGroupToName': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['aarGroup']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_physical_location(self, name=''):
            """
            list_physical_location parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listPhysicalLocation(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['physicalLocation']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_customer(self, name=''):
            """
            list_customer parameters
            :param uuid: uuid
            :param name: name
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listCustomer(
                    {'name': '%'+name}, returnedTags={'name': '', 'createTime': '', 'lastAuditTime': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['customer']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_route_group(self, name=''):
            """
            list_route_group parameters
            :param uuid: uuid
            :param name: name
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listRouteGroup(
                    {'name': '%'+name}, returnedTags={'dialPlanWizardGenld': '', 'distributionAlgorithm': '', 'name': '', 'deviceSelectionOrder': '', 'dialPlanWizardGenId': '', 'deviceName': '', 'port': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['routeGroup']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_device_pool(self, name=''):
            """
            list_device_pool parameters
            :param uuid: uuid
            :param name: name
            :param callManagerGroupName: callManagerGroupName
            :param regionName: regionName
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listDevicePool(
                    {'name': '%'+name}, returnedTags={'name': '', 'autoSearchSpaceName': '', 'dateTimeSettingName': '', 'callManagerGroupName': '', 'mediaResourceListName': '', 'regionName': '', 'networkLocale': '', 'srstName': '', 'connectionMonitorDuration': '', 'automatedAlternateRoutingCssName': '', 'aarNeighborhoodName': '', 'locationName': '', 'mobilityCssName': '', 'physicalLocationName': '', 'deviceMobilityGroupName': '', 'revertPriority': '', 'singleButtonBarge': '', 'joinAcrossLines': '', 'cgpnTransformationCssName': '', 'cdpnTransformationCssName': '', 'localRouteGroupName': '', 'geoLocationName': '', 'geoLocationFilterName': '', 'callingPartyNationalPrefix': '', 'callingPartyInternationalPrefix': '', 'callingPartyUnknownPrefix': '', 'callingPartySubscriberPrefix': '', 'adjunctCallingSearchSpace': '', 'callingPartyNationalStripDigits': '', 'callingPartyInternationalStripDigits': '', 'callingPartyUnknownStripDigits': '', 'callingPartySubscriberStripDigits': '', 'callingPartyNationalTransformationCssName': '', 'callingPartyInternationalTransformationCssName': '', 'callingPartyUnknownTransformationCssName': '', 'callingPartySubscriberTransformationCssName': '', 'calledPartyNationalPrefix': '', 'calledPartyInternationalPrefix': '', 'calledPartyUnknownPrefix': '', 'calledPartySubscriberPrefix': '', 'calledPartyNationalStripDigits': '', 'calledPartyInternationalStripDigits': '', 'calledPartyUnknownStripDigits': '', 'calledPartySubscriberStripDigits': '', 'calledPartyNationalTransformationCssName': '', 'calledPartyInternationalTransformationCssName': '', 'calledPartyUnknownTransformationCssName': '', 'calledPartySubscriberTransformationCssName': '', 'imeEnrolledPatternGroupName': '', 'localRouteGroup': '', 'mraServiceDomain': '', 'devicePoolName': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['devicePool']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_device_mobility_group(self, name=''):
            """
            list_device_mobility_group parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listDeviceMobilityGroup(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['deviceMobilityGroup']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_location(self, name=''):
            """
            list_location parameters
            :param uuid: uuid
            :param name: name
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listLocation(
                    {'name': '%'+name}, returnedTags={'name': '', 'id': '', 'withinAudioBandwidth': '', 'withinVideoBandwidth': '', 'withinImmersiveKbits': '', 'locationName': '', 'rsvpSetting': '', 'weight': '', 'audioBandwidth': '', 'videoBandwidth': '', 'immersiveBandwidth': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['location']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_soft_key_template(self, name=''):
            """
            list_soft_key_template parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listSoftKeyTemplate(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'baseSoftkeyTemplateName': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['softKeyTemplate']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_transcoder(self, name=''):
            """
            list_transcoder parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listTranscoder(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'product': '', 'subUnit': '', 'devicePoolName': '', 'commonDeviceConfigName': '', 'loadInformation': '', 'isTrustedRelayPoint': '', 'maximumCapacity': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['transcoder']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_common_device_config(self, name=''):
            """
            list_common_device_config parameters
            :param uuid: uuid
            :param name: name
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listCommonDeviceConfig(
                    {'name': '%'+name}, returnedTags={'name': '', 'softkeyTemplateName': '', 'userLocale': '', 'networkHoldMohAudioSourceId': '', 'userHoldMohAudioSourceId': '', 'mlppIndicationStatus': '', 'useTrustedRelayPoint': '', 'preemption': '', 'ipAddressingMode': '', 'ipAddressingModePreferenceControl': '', 'allowAutoConfigurationForPhones': '', 'useImeForOutboundCalls': '', 'confidentialAccess': '', 'allowDuplicateAddressDetection': '', 'acceptRedirectMessages': '', 'replyMulticastEchoRequest': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['commonDeviceConfig']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_resource_priority_namespace(self, name=''):
            """
            list_resource_priority_namespace parameters
            :param uuid: uuid
            :param namespace: namespace
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listResourcePriorityNamespace(
                    {'name': '%'+name}, returnedTags={'namespace': '', 'description': '', 'name': '', 'resourcePriorityNamespaceName': '', 'index': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['None']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_resource_priority_namespace_list(self, name=''):
            """
            list_resource_priority_namespace_list parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listResourcePriorityNamespaceList(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'resourcePriorityNamespaceName': '', 'index': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['None']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_device_mobility(self, name=''):
            """
            list_device_mobility parameters
            :param uuid: uuid
            :param name: name
            :param subNet: subNet
            :param subNetMaskSz: subNetMaskSz
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listDeviceMobility(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'subNetDetails': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['deviceMobilityGroup']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_cmc_info(self, name=''):
            """
            list_cmc_info parameters
            :param uuid: uuid
            :param code: code
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listCmcInfo(
                    {'name': '%'+name}, returnedTags={'code': '', 'description': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['cmcInfo']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_credential_policy(self, name=''):
            """
            list_credential_policy parameters
            :param uuid: uuid
            :param name: name
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listCredentialPolicy(
                    {'name': '%'+name}, returnedTags={'name': '', 'failedLogon': '', 'resetFailedLogonAttempts': '', 'lockoutDuration': '', 'credChangeDuration': '', 'credExpiresAfter': '', 'minCredLength': '', 'prevCredStoredNum': '', 'inactiveDaysAllowed': '', 'expiryWarningDays': '', 'trivialCredCheck': '', 'minCharsToChange': '', 'credentialUser': '', 'credentialType': '', 'credPolicyName': '', 'credentials': '', 'confirmCredentials': '', 'credUserCantChange': '', 'credUserMustChange': '', 'credDoesNotExpire': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['credentialPolicy']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_fac_info(self, name=''):
            """
            list_fac_info parameters
            :param uuid: uuid
            :param name: name
            :param code: code
            :param authorizationLevel: authorizationLevel
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listFacInfo(
                    {'name': '%'+name}, returnedTags={'name': '', 'code': '', 'authorizationLevel': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['facInfo']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_hunt_list(self, name=''):
            """
            list_hunt_list parameters
            :param uuid: uuid
            :param description: description
            :param name: name
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listHuntList(
                    {'name': '%'+name}, returnedTags={'description': '', 'callManagerGroupName': '', 'routeListEnabled': '', 'voiceMailUsage': '', 'name': '', 'lineGroupName': '', 'selectionOrder': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['huntList']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_ivr_user_locale(self, name=''):
            """
            list_ivr_user_locale parameters
            :param uuid: uuid
            :param userLocale: userLocale
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listIvrUserLocale(
                    {'name': '%'+name}, returnedTags={'userLocale': '', 'orderIndex': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['ivrUserLocale']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_line_group(self, name=''):
            """
            list_line_group parameters
            :param uuid: uuid
            :param name: name
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listLineGroup(
                    {'name': '%'+name}, returnedTags={'distributionAlgorithm': '', 'rnaReversionTimeOut': '', 'huntAlgorithmNoAnswer': '', 'huntAlgorithmBusy': '', 'huntAlgorithmNotAvailable': '', 'name': '', 'autoLogOffHunt': '', 'lineSelectionOrder': '', 'directoryNumber': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['lineGroup']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_recording_profile(self, name=''):
            """
            list_recording_profile parameters
            :param uuid: uuid
            :param name: name
            :param recordingCssName: recordingCssName
            :param recorderDestination: recorderDestination
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listRecordingProfile(
                    {'name': '%'+name}, returnedTags={'name': '', 'recordingCssName': '', 'recorderDestination': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['recordingProfile']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_route_filter(self, name=''):
            """
            list_route_filter parameters
            :param uuid: uuid
            :param name: name
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listRouteFilter(
                    {'name': '%'+name}, returnedTags={'name': '', 'clause': '', 'dialPlanName': '', 'dialPlanWizardGenId': '', 'dialPlanTagName': '', 'digits': '', 'operator': '', 'priority': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['routeFilter']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_call_manager_group(self, name=''):
            """
            list_call_manager_group parameters
            :param uuid: uuid
            :param name: name
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listCallManagerGroup(
                    {'name': '%'+name}, returnedTags={'name': '', 'tftpDefault': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['callManagerGroup']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_user_group(self, name=''):
            """
            list_user_group parameters
            :param uuid: uuid
            :param name: name
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listUserGroup(
                    {'name': '%'+name}, returnedTags={'name': '', 'userId': '', 'roleName': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['userGroup']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_dial_plan(self, name=''):
            """
            list_dial_plan parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listDialPlan(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'dialPlanName': '', 'operator': '', 'suppressFromRouteFilter': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['dialPlan']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_dial_plan_tag(self, name=''):
            """
            list_dial_plan_tag parameters
            :param uuid: uuid
            :param name: name
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listDialPlanTag(
                    {'name': '%'+name}, returnedTags={'name': '', 'dialPlanName': '', 'operator': '', 'suppressFromRouteFilter': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['dialPlanTag']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_ddi(self, name=''):
            """
            list_ddi parameters
            :param uuid: uuid
            :param name: name
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listDdi(
                    {'name': '%'+name}, returnedTags={'name': '', 'clause': '', 'dialPlanName': '', 'digitAnalysisId': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['ddi']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_mobile_smart_client_profile(self, name=''):
            """
            list_mobile_smart_client_profile parameters
            :param uuid: uuid
            :param name: name
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listMobileSmartClientProfile(
                    {'name': '%'+name}, returnedTags={'name': '', 'mobileSmartClient': '', 'enableSnrUri': '', 'enableCFAUri': '', 'handOffUri': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['mobileSmartClientProfile']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_process_node_service(self, name=''):
            """
            list_process_node_service parameters
            :param uuid: uuid
            :param processNodeName: processNodeName
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listProcessNodeService(
                    {'name': '%'+name}, returnedTags={'processNodeName': '', 'service': '', 'traceLevel': '', 'userCategories': '', 'enable': '', 'numFiles': '', 'maxFileSize': '', 'isActive': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['processNodeService']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_moh_audio_source(self, name=''):
            """
            list_moh_audio_source parameters
            :param uuid: uuid
            :param sourceId: sourceId
            :param name: name
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listMohAudioSource(
                    {'name': '%'+name}, returnedTags={'sourceId': '', 'name': '', 'sourceFile': '', 'multicast': '', 'mohFileStatus': '', 'initialAnnouncement': '', 'periodicAnnouncement': '', 'periodicAnnouncementInterval': '', 'localeAnnouncement': '', 'initialAnnouncementPlayed': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['mohAudioSource']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_dhcp_server(self, name=''):
            """
            list_dhcp_server parameters
            :param uuid: uuid
            :param processNodeName: processNodeName
            :param primaryDnsIpAddress: primaryDnsIpAddress
            :param secondaryDnsIpAddress: secondaryDnsIpAddress
            :param domainName: domainName
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listDhcpServer(
                    {'name': '%'+name}, returnedTags={'processNodeName': '', 'primaryDnsIpAddress': '', 'secondaryDnsIpAddress': '', 'primaryTftpServerIpAddress': '', 'secondaryTftpServerIpAddress': '', 'bootstrapServerIpAddress': '', 'domainName': '', 'tftpServerName': '', 'arpCacheTimeout': '', 'ipAddressLeaseTime': '', 'renewalTime': '', 'rebindingTime': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['dhcpServer']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_dhcp_subnet(self, name=''):
            """
            list_dhcp_subnet parameters
            :param uuid: uuid
            :param dhcpServerName: dhcpServerName
            :param subnetIpAddress: subnetIpAddress
            :param primaryStartIpAddress: primaryStartIpAddress
            :param primaryEndIpAddress: primaryEndIpAddress
            :param secondaryStartIpAddress: secondaryStartIpAddress
            :param secondaryEndIpAddress: secondaryEndIpAddress
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listDhcpSubnet(
                    {'name': '%'+name}, returnedTags={'subnetIpAddress': '', 'primaryStartIpAddress': '', 'primaryEndIpAddress': '', 'secondaryStartIpAddress': '', 'secondaryEndIpAddress': '', 'primaryRouterIpAddress': '', 'secondaryRouterIpAddress': '', 'subnetMask': '', 'domainName': '', 'primaryDnsIpAddress': '', 'secondaryDnsIpAddress': '', 'tftpServerName': '', 'primaryTftpServerIpAddress': '', 'secondaryTftpServerIpAddress': '', 'bootstrapServerIpAddress': '', 'arpCacheTimeout': '', 'ipAddressLeaseTime': '', 'renewalTime': '', 'rebindingTime': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['dhcpSubnet']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_call_park(self, name=''):
            """
            list_call_park parameters
            :param uuid: uuid
            :param pattern: pattern
            :param description: description
            :param routePartitionName: routePartitionName
            :param callManagerName: callManagerName
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listCallPark(
                    {'name': '%'+name}, returnedTags={'pattern': '', 'description': '', 'usage': '', 'routePartitionName': '', 'callManagerName': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['callPark']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_directed_call_park(self, name=''):
            """
            list_directed_call_park parameters
            :param uuid: uuid
            :param pattern: pattern
            :param description: description
            :param routePartitionName: routePartitionName
            :param reversionPattern: reversionPattern
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listDirectedCallPark(
                    {'name': '%'+name}, returnedTags={'pattern': '', 'description': '', 'usage': '', 'routePartitionName': '', 'retrievalPrefix': '', 'reversionPattern': '', 'revertCssName': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['directedCallPark']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_meet_me(self, name=''):
            """
            list_meet_me parameters
            :param uuid: uuid
            :param pattern: pattern
            :param description: description
            :param routePartitionName: routePartitionName
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listMeetMe(
                    {'name': '%'+name}, returnedTags={'pattern': '', 'description': '', 'usage': '', 'routePartitionName': '', 'minimumSecurityLevel': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['meetMe']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_conference_now(self, name=''):
            """
            list_conference_now parameters
            :param uuid: uuid
            :param conferenceNowNumber: conferenceNowNumber
            :param routePartitionName: routePartitionName
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listConferenceNow(
                    {'name': '%'+name}, returnedTags={'conferenceNowNumber': '', 'routePartitionName': '', 'description': '', 'maxWaitTimeForHost': '', 'MohAudioSourceId': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['conferenceNow']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_route_list(self, name=''):
            """
            list_route_list parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listRouteList(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'callManagerGroupName': '', 'routeListEnabled': '', 'runOnEveryNode': '', 'routeGroupName': '', 'selectionOrder': '', 'calledPartyTransformationMask': '', 'callingPartyTransformationMask': '', 'dialPlanWizardGenId': '', 'digitDiscardInstructionName': '', 'callingPartyPrefixDigits': '', 'prefixDigitsOut': '', 'useFullyQualifiedCallingPartyNumber': '', 'callingPartyNumberingPlan': '', 'callingPartyNumberType': '', 'calledPartyNumberingPlan': '', 'calledPartyNumberType': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['routeList']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_user(self, name=''):
            """
            list_user parameters
            :param uuid: uuid
            :param firstName: firstName
            :param lastName: lastName
            :param userid: userid
            :param department: department
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listUser(
                    {'name': '%'+name}, returnedTags={'name': '', 'firstName': '', 'middleName': '', 'lastName': '', 'emMaxLoginTime': '', 'userid': '', 'mailid': '', 'department': '', 'manager': '', 'userLocale': '', 'primaryExtension': '', 'associatedPc': '', 'enableCti': '', 'subscribeCallingSearchSpaceName': '', 'enableMobility': '', 'enableMobileVoiceAccess': '', 'maxDeskPickupWaitTime': '', 'remoteDestinationLimit': '', 'status': '', 'enableEmcc': '', 'patternPrecedence': '', 'numericUserId': '', 'mlppPassword': '', 'homeCluster': '', 'imAndPresenceEnable': '', 'serviceProfile': '', 'directoryUri': '', 'telephoneNumber': '', 'title': '', 'mobileNumber': '', 'homeNumber': '', 'pagerNumber': '', 'calendarPresence': '', 'userIdentity': '', 'userId': '', 'password': '', 'pin': '', 'productType': '', 'dnCssName': '', 'phoneCssName': '', 'e164Mask': '', 'extension': '', 'routePartitionName': '', 'voiceMailProfileName': '', 'enableExtensionMobility': '', 'DirectoryURI': '', 'DirectoryNumberURIPartition': '', 'description': '', 'allowProvision': '', 'limitProvision': '', 'defaultUserProfile': '', 'allowProvisionEMMaxLoginTime': '', 'roleName': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['userGroup']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_app_user(self, name=''):
            """
            list_app_user parameters
            :param uuid: uuid
            :param userid: userid
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listAppUser(
                    {'name': '%'+name}, returnedTags={'userid': '', 'presenceGroupName': '', 'acceptPresenceSubscription': '', 'acceptOutOfDialogRefer': '', 'acceptUnsolicitedNotification': '', 'allowReplaceHeader': '', 'isStandard': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['appUser']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_sip_realm(self, name=''):
            """
            list_sip_realm parameters
            :param uuid: uuid
            :param realm: realm
            :param userid: userid
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listSipRealm(
                    {'name': '%'+name}, returnedTags={'realm': '', 'userid': '', 'digestCredentials': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['sipRealm']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_phone_ntp(self, name=''):
            """
            list_phone_ntp parameters
            :param uuid: uuid
            :param ipAddress: ipAddress
            :param ipv6Address: ipv6Address
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listPhoneNtp(
                    {'name': '%'+name}, returnedTags={'ipAddress': '', 'ipv6Address': '', 'description': '', 'mode': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['phoneNtp']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_date_time_group(self, name=''):
            """
            list_date_time_group parameters
            :param uuid: uuid
            :param name: name
            :param timeZone: timeZone
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listDateTimeGroup(
                    {'name': '%'+name}, returnedTags={'name': '', 'timeZone': '', 'dateformat': '', 'phoneNtpName': '', 'selectionOrder': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['dateTimeGroup']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_presence_group(self, name=''):
            """
            list_presence_group parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listPresenceGroup(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'presenceGroupName': '', 'subscriptionPermission': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['presenceGroup']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_geo_location(self, name=''):
            """
            list_geo_location parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listGeoLocation(
                    {'name': '%'+name}, returnedTags={'name': '', 'country': '', 'description': '', 'nationalSubDivision': '', 'district': '', 'communityName': '', 'cityDivision': '', 'neighbourhood': '', 'street': '', 'leadingStreetDirection': '', 'trailingStreetSuffix': '', 'streetSuffix': '', 'houseNumber': '', 'houseNumberSuffix': '', 'landmark': '', 'location': '', 'floor': '', 'occupantName': '', 'postalCode': '', 'useCountry': '', 'useNationalSubDivision': '', 'useDistrict': '', 'useCommunityName': '', 'useCityDivision': '', 'useNeighbourhood': '', 'useStreet': '', 'useLeadingStreetDirection': '', 'useTrailingStreetSuffix': '', 'useStreetSuffix': '', 'useHouseNumber': '', 'useHouseNumberSuffix': '', 'useLandmark': '', 'useLocation': '', 'useFloor': '', 'useOccupantName': '', 'usePostalCode': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['geoLocation']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_srst(self, name=''):
            """
            list_srst parameters
            :param uuid: uuid
            :param name: name
            :param ipAddress: ipAddress
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listSrst(
                    {'name': '%'+name}, returnedTags={'name': '', 'port': '', 'ipAddress': '', 'ipv6Address': '', 'SipNetwork': '', 'SipPort': '', 'srstCertificatePort': '', 'isSecure': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['srst']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_mlpp_domain(self, name=''):
            """
            list_mlpp_domain parameters
            :param uuid: uuid
            :param domainName: domainName
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listMlppDomain(
                    {'name': '%'+name}, returnedTags={'domainName': '', 'domainId': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['mlppDomain']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_cuma_server_security_profile(self, name=''):
            """
            list_cuma_server_security_profile parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listCumaServerSecurityProfile(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'securityMode': '', 'transportType': '', 'x509SubjectName': '', 'serverIpHostName': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['cumaServerSecurityProfile']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_application_server(self, name=''):
            """
            list_application_server parameters
            :param uuid: uuid
            :param name: name
            :param ipAddress: ipAddress
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listApplicationServer(
                    {'name': '%'+name}, returnedTags={'appServerType': '', 'name': '', 'ipAddress': '', 'url': '', 'endUserUrl': '', 'processNodeName': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['applicationServer']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_application_user_capf_profile(self, name=''):
            """
            list_application_user_capf_profile parameters
            :param uuid: uuid
            :param applicationUser: applicationUser
            :param instanceId: instanceId
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listApplicationUserCapfProfile(
                    {'name': '%'+name}, returnedTags={'applicationUser': '', 'instanceId': '', 'certificateOperation': '', 'authenticationMode': '', 'authenticationString': '', 'keySize': '', 'keyOrder': '', 'ecKeySize': '', 'operationCompletion': '', 'certificationOperationStatus': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['applicationUserCapfProfile']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_end_user_capf_profile(self, name=''):
            """
            list_end_user_capf_profile parameters
            :param uuid: uuid
            :param endUserId: endUserId
            :param instanceId: instanceId
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listEndUserCapfProfile(
                    {'name': '%'+name}, returnedTags={'endUserId': '', 'instanceId': '', 'certificationOperation': '', 'authenticationMode': '', 'authenticationString': '', 'keySize': '', 'keyOrder': '', 'ecKeySize': '', 'operationCompletion': '', 'certificationOperationStatus': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['endUserCapfProfile']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_service_parameter(self, name=''):
            """
            list_service_parameter parameters
            :param uuid: uuid
            :param processNodeName: processNodeName
            :param service: service
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listServiceParameter(
                    {'name': '%'+name}, returnedTags={'processNodeName': '', 'name': '', 'service': '', 'value': '', 'valueType': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['serviceParameter']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_geo_location_filter(self, name=''):
            """
            list_geo_location_filter parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listGeoLocationFilter(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'useCountry': '', 'useNationalSubDivision': '', 'useDistrict': '', 'useCommunityName': '', 'useCityDivision': '', 'useNeighbourhood': '', 'useStreet': '', 'useLeadingStreetDirection': '', 'useTrailingStreetSuffix': '', 'useStreetSuffix': '', 'useHouseNumber': '', 'useHouseNumberSuffix': '', 'useLandmark': '', 'useLocation': '', 'useFloor': '', 'useOccupantName': '', 'usePostalCode': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['geoLocationFilter']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_voice_mail_profile(self, name=''):
            """
            list_voice_mail_profile parameters
            :param uuid: uuid
            :param name: name
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listVoiceMailProfile(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'isDefault': '', 'voiceMailboxMask': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['voiceMailProfile']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_voice_mail_port(self, name=''):
            """
            list_voice_mail_port parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            :param callingSearchSpaceName: callingSearchSpaceName
            :param devicePoolName: devicePoolName
            :param securityProfileName: securityProfileName
            :param dnPattern: dnPattern
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listVoiceMailPort(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'product': '', 'model': '', 'class': '', 'protocol': '', 'protocolSide': '', 'callingSearchSpaceName': '', 'devicePoolName': '', 'commonDeviceConfigName': '', 'locationName': '', 'preemption': '', 'useTrustedRelayPoint': '', 'securityProfileName': '', 'geoLocationName': '', 'automatedAlternateRoutingCssName': '', 'dnPattern': '', 'callerIdDisplay': '', 'callerIdDisplayAscii': '', 'externalMask': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['voiceMailPort']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_gatekeeper(self, name=''):
            """
            list_gatekeeper parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listGatekeeper(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'rrqTimeToLive': '', 'retryTimeout': '', 'enableDevice': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['gatekeeper']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_phone_button_template(self, name=''):
            """
            list_phone_button_template parameters
            :param uuid: uuid
            :param name: name
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listPhoneButtonTemplate(
                    {'name': '%'+name}, returnedTags={'name': '', 'isUserModifiable': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['phoneButtonTemplate']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_common_phone_config(self, name=''):
            """
            list_common_phone_config parameters
            :param uuid: uuid
            :param name: name
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listCommonPhoneConfig(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'dndOption': '', 'dndAlertingType': '', 'backgroundImage': '', 'phonePersonalization': '', 'phoneServiceDisplay': '', 'sshUserId': '', 'alwaysUsePrimeLine': '', 'alwaysUsePrimeLineForVoiceMessage': '', 'vpnGroupName': '', 'vpnProfileName': '', 'featureControlPolicy': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['commonPhoneConfig']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_message_waiting(self, name=''):
            """
            list_message_waiting parameters
            :param uuid: uuid
            :param pattern: pattern
            :param routePartitionName: routePartitionName
            :param description: description
            :param callingSearchSpaceName: callingSearchSpaceName
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listMessageWaiting(
                    {'name': '%'+name}, returnedTags={'pattern': '', 'routePartitionName': '', 'description': '', 'messageWaitingIndicator': '', 'callingSearchSpaceName': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['messageWaiting']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_ip_phone_services(self, name=''):
            """
            list_ip_phone_services parameters
            :param uuid: uuid
            :param serviceName: serviceName
            :param serviceDescription: serviceDescription
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listIpPhoneServices(
                    {'name': '%'+name}, returnedTags={'serviceName': '', 'asciiServiceName': '', 'serviceDescription': '', 'serviceUrl': '', 'secureServiceUrl': '', 'serviceCategory': '', 'serviceType': '', 'serviceVendor': '', 'serviceVersion': '', 'enabled': '', 'enterpriseSubscription': '', 'name': '', 'displayName': '', 'default': '', 'description': '', 'paramRequired': '', 'paramPassword': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['ipPhoneServices']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_cti_route_point(self, name=''):
            """
            list_cti_route_point parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            :param callingSearchSpaceName: callingSearchSpaceName
            :param devicePoolName: devicePoolName
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listCtiRoutePoint(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'product': '', 'model': '', 'class': '', 'protocol': '', 'protocolSide': '', 'callingSearchSpaceName': '', 'devicePoolName': '', 'commonDeviceConfigName': '', 'locationName': '', 'mediaResourceListName': '', 'networkHoldMohAudioSourceId': '', 'userHoldMohAudioSourceId': '', 'useTrustedRelayPoint': '', 'cgpnTransformationCssName': '', 'useDevicePoolCgpnTransformCss': '', 'geoLocationName': '', 'userLocale': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['ctiRoutePoint']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_trans_pattern(self, name=''):
            """
            list_trans_pattern parameters
            :param uuid: uuid
            :param pattern: pattern
            :param description: description
            :param routePartitionName: routePartitionName
            :param isEmergencyServiceNumber: isEmergencyServiceNumber
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listTransPattern(
                    {'name': '%'+name}, returnedTags={'pattern': '', 'description': '', 'usage': '', 'routePartitionName': '', 'blockEnable': '', 'calledPartyTransformationMask': '', 'callingPartyTransformationMask': '', 'useCallingPartyPhoneMask': '', 'callingPartyPrefixDigits': '', 'dialPlanName': '', 'digitDiscardInstructionName': '', 'patternUrgency': '', 'prefixDigitsOut': '', 'routeFilterName': '', 'callingLinePresentationBit': '', 'callingNamePresentationBit': '', 'connectedLinePresentationBit': '', 'connectedNamePresentationBit': '', 'patternPrecedence': '', 'provideOutsideDialtone': '', 'callingPartyNumberingPlan': '', 'callingPartyNumberType': '', 'calledPartyNumberingPlan': '', 'calledPartyNumberType': '', 'callingSearchSpaceName': '', 'resourcePriorityNamespaceName': '', 'routeNextHopByCgpn': '', 'routeClass': '', 'callInterceptProfileName': '', 'releaseClause': '', 'useOriginatorCss': '', 'dontWaitForIDTOnSubsequentHops': '', 'isEmergencyServiceNumber': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['transPattern']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_calling_party_transformation_pattern(self, name=''):
            """
            list_calling_party_transformation_pattern parameters
            :param uuid: uuid
            :param pattern: pattern
            :param description: description
            :param routePartitionName: routePartitionName
            :param dialPlanName: dialPlanName
            :param routeFilterName: routeFilterName
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listCallingPartyTransformationPattern(
                    {'name': '%'+name}, returnedTags={'pattern': '', 'description': '', 'usage': '', 'routePartitionName': '', 'callingPartyTransformationMask': '', 'useCallingPartyPhoneMask': '', 'dialPlanName': '', 'digitDiscardInstructionName': '', 'patternUrgency': '', 'callingPartyPrefixDigits': '', 'routeFilterName': '', 'callingLinePresentationBit': '', 'callingPartyNumberingPlan': '', 'callingPartyNumberType': '', 'mlppPreemptionDisabled': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['callingPartyTransformationPattern']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_sip_route_pattern(self, name=''):
            """
            list_sip_route_pattern parameters
            :param uuid: uuid
            :param pattern: pattern
            :param description: description
            :param routePartitionName: routePartitionName
            :param dnOrPatternIpv6: dnOrPatternIpv6
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listSipRoutePattern(
                    {'name': '%'+name}, returnedTags={'pattern': '', 'description': '', 'usage': '', 'routePartitionName': '', 'blockEnable': '', 'callingPartyTransformationMask': '', 'useCallingPartyPhoneMask': '', 'callingPartyPrefixDigits': '', 'callingLinePresentationBit': '', 'callingNamePresentationBit': '', 'connectedLinePresentationBit': '', 'connectedNamePresentationBit': '', 'sipTrunkName': '', 'dnOrPatternIpv6': '', 'routeOnUserPart': '', 'useCallerCss': '', 'domainRoutingCssName': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['sipRoutePattern']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_hunt_pilot(self, name=''):
            """
            list_hunt_pilot parameters
            :param uuid: uuid
            :param pattern: pattern
            :param description: description
            :param routePartitionName: routePartitionName
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listHuntPilot(
                    {'name': '%'+name}, returnedTags={'pattern': '', 'description': '', 'usage': '', 'routePartitionName': '', 'blockEnable': '', 'calledPartyTransformationMask': '', 'callingPartyTransformationMask': '', 'useCallingPartyPhoneMask': '', 'callingPartyPrefixDigits': '', 'dialPlanName': '', 'digitDiscardInstructionName': '', 'patternUrgency': '', 'prefixDigitsOut': '', 'routeFilterName': '', 'callingLinePresentationBit': '', 'callingNamePresentationBit': '', 'connectedLinePresentationBit': '', 'connectedNamePresentationBit': '', 'patternPrecedence': '', 'provideOutsideDialtone': '', 'callingPartyNumberingPlan': '', 'callingPartyNumberType': '', 'calledPartyNumberingPlan': '', 'calledPartyNumberType': '', 'huntListName': '', 'parkMonForwardNoRetrieve': '', 'alertingName': '', 'asciiAlertingName': '', 'aarNeighborhoodName': '', 'forwardHuntNoAnswer': '', 'forwardHuntBusy': '', 'callPickupGroupName': '', 'maxHuntduration': '', 'releaseClause': '', 'displayConnectedNumber': '', 'queueCalls': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['huntPilot']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_route_pattern(self, name=''):
            """
            list_route_pattern parameters
            :param uuid: uuid
            :param pattern: pattern
            :param description: description
            :param routePartitionName: routePartitionName
            :param isEmergencyServiceNumber: isEmergencyServiceNumber
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listRoutePattern(
                    {'name': '%'+name}, returnedTags={'pattern': '', 'description': '', 'usage': '', 'routePartitionName': '', 'blockEnable': '', 'calledPartyTransformationMask': '', 'callingPartyTransformationMask': '', 'useCallingPartyPhoneMask': '', 'callingPartyPrefixDigits': '', 'dialPlanName': '', 'dialPlanWizardGenId': '', 'digitDiscardInstructionName': '', 'networkLocation': '', 'patternUrgency': '', 'prefixDigitsOut': '', 'routeFilterName': '', 'callingLinePresentationBit': '', 'callingNamePresentationBit': '', 'connectedLinePresentationBit': '', 'connectedNamePresentationBit': '', 'supportOverlapSending': '', 'patternPrecedence': '', 'releaseClause': '', 'allowDeviceOverride': '', 'provideOutsideDialtone': '', 'callingPartyNumberingPlan': '', 'callingPartyNumberType': '', 'calledPartyNumberingPlan': '', 'calledPartyNumberType': '', 'authorizationCodeRequired': '', 'authorizationLevelRequired': '', 'clientCodeRequired': '', 'withTag': '', 'withValueClause': '', 'resourcePriorityNamespaceName': '', 'routeClass': '', 'externalCallControl': '', 'isEmergencyServiceNumber': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['routePattern']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_application_dial_rules(self, name=''):
            """
            list_application_dial_rules parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            :param numberBeginWith: numberBeginWith
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listApplicationDialRules(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'numberBeginWith': '', 'numberOfDigits': '', 'digitsToBeRemoved': '', 'prefixPattern': '', 'priority': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['applicationDialRules']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_directory_lookup_dial_rules(self, name=''):
            """
            list_directory_lookup_dial_rules parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            :param numberBeginWith: numberBeginWith
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listDirectoryLookupDialRules(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'numberBeginWith': '', 'numberOfDigits': '', 'digitsToBeRemoved': '', 'prefixPattern': '', 'priority': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['directoryLookupDialRules']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_phone_security_profile(self, name=''):
            """
            list_phone_security_profile parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listPhoneSecurityProfile(
                    {'name': '%'+name}, returnedTags={'phoneType': '', 'protocol': '', 'name': '', 'description': '', 'deviceSecurityMode': '', 'authenticationMode': '', 'keySize': '', 'keyOrder': '', 'ecKeySize': '', 'tftpEncryptedConfig': '', 'EnableOAuthAuthentication': '', 'nonceValidityTime': '', 'transportType': '', 'sipPhonePort': '', 'enableDigestAuthentication': '', 'excludeDigestCredentials': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['phoneSecurityProfile']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_sip_dial_rules(self, name=''):
            """
            list_sip_dial_rules parameters
            :param uuid: uuid
            :param dialPattern: dialPattern
            :param name: name
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listSipDialRules(
                    {'name': '%'+name}, returnedTags={'dialPattern': '', 'name': '', 'description': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['sipDialRules']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_conference_bridge(self, name=''):
            """
            list_conference_bridge parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            :param devicePoolName: devicePoolName
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listConferenceBridge(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'product': '', 'devicePoolName': '', 'commonDeviceConfigName': '', 'locationName': '', 'subUnit': '', 'loadInformation': '', 'maximumCapacity': '', 'useTrustedRelayPoint': '', 'securityProfileName': '', 'destinationAddress': '', 'mcuConferenceBridgeSipPort': '', 'sipProfile': '', 'srtpAllowed': '', 'normalizationScript': '', 'enableTrace': '', 'userName': '', 'password': '', 'httpPort': '', 'useHttps': '', 'conferenceBridgePrefix': '', 'allowCFBControlOfCallSecurityIcon': '', 'overrideSIPTrunkAddress': '', 'sipTrunkName': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['conferenceBridge']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_annunciator(self, name=''):
            """
            list_annunciator parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            :param devicePoolName: devicePoolName
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listAnnunciator(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'devicePoolName': '', 'locationName': '', 'useTrustedRelayPoint': '', 'serverName': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['annunciator']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_interactive_voice_response(self, name=''):
            """
            list_interactive_voice_response parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            :param devicePoolName: devicePoolName
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listInteractiveVoiceResponse(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'devicePoolName': '', 'locationName': '', 'useTrustedRelayPoint': '', 'serverName': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['None']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_mtp(self, name=''):
            """
            list_mtp parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            :param devicePoolName: devicePoolName
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listMtp(
                    {'name': '%'+name}, returnedTags={'mtpType': '', 'name': '', 'description': '', 'devicePoolName': '', 'trustedRelayPoint': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['mtp']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_remote_destination_profile(self, name=''):
            """
            list_remote_destination_profile parameters
            :param uuid: uuid
            :param name: name
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listRemoteDestinationProfile(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'product': '', 'model': '', 'class': '', 'protocol': '', 'protocolSide': '', 'callingSearchSpaceName': '', 'devicePoolName': '', 'networkHoldMohAudioSourceId': '', 'userHoldMohAudioSourceId': '', 'callInfoPrivacyStatus': '', 'userId': '', 'ignorePresentationIndicators': '', 'rerouteCallingSearchSpaceName': '', 'cgpnTransformationCssName': '', 'automatedAlternateRoutingCssName': '', 'useDevicePoolCgpnTransformCss': '', 'userLocale': '', 'networkLocale': '', 'primaryPhoneName': '', 'dndOption': '', 'dndStatus': '', 'mobileSmartClientProfileName': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['remoteDestinationProfile']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_line(self, name=''):
            """
            list_line parameters
            :param uuid: uuid
            :param pattern: pattern
            :param description: description
            :param usage: usage
            :param routePartitionName: routePartitionName
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listLine(
                    {'name': '%'+name}, returnedTags={'distributionAlgorithm': '', 'rnaReversionTimeOut': '', 'huntAlgorithmNoAnswer': '', 'huntAlgorithmBusy': '', 'huntAlgorithmNotAvailable': '', 'name': '', 'autoLogOffHunt': '', 'pattern': '', 'description': '', 'usage': '', 'routePartitionName': '', 'aarNeighborhoodName': '', 'aarDestinationMask': '', 'aarKeepCallHistory': '', 'aarVoiceMailEnabled': '', 'callPickupGroupName': '', 'autoAnswer': '', 'networkHoldMohAudioSourceId': '', 'userHoldMohAudioSourceId': '', 'callingIdPresentationWhenDiverted': '', 'alertingName': '', 'asciiAlertingName': '', 'presenceGroupName': '', 'shareLineAppearanceCssName': '', 'voiceMailProfileName': '', 'patternPrecedence': '', 'releaseClause': '', 'hrDuration': '', 'hrInterval': '', 'cfaCssPolicy': '', 'defaultActivatedDeviceName': '', 'parkMonForwardNoRetrieveDn': '', 'parkMonForwardNoRetrieveIntDn': '', 'parkMonForwardNoRetrieveVmEnabled': '', 'parkMonForwardNoRetrieveIntVmEnabled': '', 'parkMonForwardNoRetrieveCssName': '', 'parkMonForwardNoRetrieveIntCssName': '', 'parkMonReversionTimer': '', 'partyEntranceTone': '', 'allowCtiControlFlag': '', 'rejectAnonymousCall': '', 'confidentialAccess': '', 'externalCallControlProfile': '', 'enterpriseAltNum': '', 'e164AltNum': '', 'pstnFailover': '', 'lineSelectionOrder': '', 'directoryNumber': '', 'index': '', 'laapAssociate': '', 'laapProductType': '', 'laapDeviceName': '', 'laapDirectory': '', 'laapPartition': '', 'laapDescription': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['lineGroup']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_default_device_profile(self, name=''):
            """
            list_default_device_profile parameters
            :param uuid: uuid
            :param name: name
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listDefaultDeviceProfile(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'product': '', 'model': '', 'class': '', 'protocol': '', 'protocolSide': '', 'userHoldMohAudioSourceId': '', 'userLocale': '', 'phoneButtonTemplate': '', 'softkeyTemplate': '', 'privacy': '', 'singleButtonBarge': '', 'joinAcrossLines': '', 'ignorePi': '', 'dndStatus': '', 'dndRingSetting': '', 'dndOption': '', 'mlppIndication': '', 'preemption': '', 'alwaysUsePrimeLine': '', 'alwaysUsePrimeLineForVoiceMessage': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['defaultDeviceProfile']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_h323_phone(self, name=''):
            """
            list_h323_phone parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            :param callingSearchSpaceName: callingSearchSpaceName
            :param devicePoolName: devicePoolName
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listH323Phone(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'product': '', 'model': '', 'class': '', 'protocol': '', 'protocolSide': '', 'callingSearchSpaceName': '', 'devicePoolName': '', 'commonDeviceConfigName': '', 'commonPhoneConfigName': '', 'locationName': '', 'mediaResourceListName': '', 'automatedAlternateRoutingCssName': '', 'aarNeighborhoodName': '', 'traceFlag': '', 'useTrustedRelayPoint': '', 'retryVideoCallAsAudio': '', 'remoteDevice': '', 'cgpnTransformationCssName': '', 'useDevicePoolCgpnTransformCss': '', 'geoLocationName': '', 'alwaysUsePrimeLine': '', 'alwaysUsePrimeLineForVoiceMessage': '', 'srtpAllowed': '', 'unattendedPort': '', 'subscribeCallingSearchSpaceName': '', 'mtpRequired': '', 'mtpPreferredCodec': '', 'callerIdDn': '', 'callingPartySelection': '', 'callingLineIdPresentation': '', 'displayIEDelivery': '', 'redirectOutboundNumberIe': '', 'redirectInboundNumberIe': '', 'presenceGroupName': '', 'hlogStatus': '', 'ownerUserName': '', 'signalingPort': '', 'ignorePresentationIndicators': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['h323Phone']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_moh_server(self, name=''):
            """
            list_moh_server parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            :param devicePoolName: devicePoolName
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listMohServer(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'processNodeName': '', 'devicePoolName': '', 'locationName': '', 'maxUnicastConnections': '', 'maxMulticastConnections': '', 'fixedAudioSourceDevice': '', 'runFlag': '', 'useTrustedRelayPoint': '', 'isMultiCastEnabled': '', 'baseMulticastIpaddress': '', 'baseMulticastPort': '', 'multicastIncrementOnIp': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['mohServer']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_h323_trunk(self, name=''):
            """
            list_h323_trunk parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            :param callingSearchSpaceName: callingSearchSpaceName
            :param devicePoolName: devicePoolName
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listH323Trunk(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'product': '', 'model': '', 'class': '', 'protocol': '', 'protocolSide': '', 'callingSearchSpaceName': '', 'devicePoolName': '', 'commonDeviceConfigName': '', 'networkLocation': '', 'locationName': '', 'mediaResourceListName': '', 'aarNeighborhoodName': '', 'traceFlag': '', 'mlppIndicationStatus': '', 'preemption': '', 'useTrustedRelayPoint': '', 'retryVideoCallAsAudio': '', 'cgpnTransformationCssName': '', 'useDevicePoolCgpnTransformCss': '', 'geoLocationName': '', 'geoLocationFilterName': '', 'sendGeoLocation': '', 'cdpnTransformationCssName': '', 'useDevicePoolCdpnTransformCss': '', 'packetCaptureMode': '', 'packetCaptureDuration': '', 'srtpAllowed': '', 'unattendedPort': '', 'mtpRequired': '', 'callerIdDn': '', 'callingPartySelection': '', 'callingLineIdPresentation': '', 'displayIEDelivery': '', 'redirectOutboundNumberIe': '', 'redirectInboundNumberIe': '', 'enableInboundFaststart': '', 'enableOutboundFaststart': '', 'codecForOutboundFaststart': '', 'allowH235PassThrough': '', 'tunneledProtocol': '', 'asn1RoseOidEncoding': '', 'qsigVariant': '', 'transmitUtf8': '', 'signalingPort': '', 'nationalPrefix': '', 'internationalPrefix': '', 'unknownPrefix': '', 'subscriberPrefix': '', 'sigDigits': '', 'prefixDn': '', 'calledPartyIeNumberType': '', 'callingPartyIeNumberType': '', 'calledNumberingPlan': '', 'callingNumberingPlan': '', 'pathReplacementSupport': '', 'ictPassingPrecedenceLevelThroughUuie': '', 'ictSecurityAccessLevel': '', 'isSafEnabled': '', 'callingPartyNationalStripDigits': '', 'callingPartyInternationalStripDigits': '', 'callingPartyUnknownStripDigits': '', 'callingPartySubscriberStripDigits': '', 'callingPartyNationalTransformationCssName': '', 'callingPartyInternationalTransformationCssName': '', 'callingPartyUnknownTransformationCssName': '', 'callingPartySubscriberTransformationCssName': '', 'calledPartyNationalPrefix': '', 'calledPartyInternationalPrefix': '', 'calledPartyUnknownPrefix': '', 'calledPartySubscriberPrefix': '', 'pstnAccess': '', 'imeE164TransformationName': '', 'automatedAlternateRoutingCssName': '', 'useDevicePoolCgpnTransformCssNatl': '', 'useDevicePoolCgpnTransformCssIntl': '', 'useDevicePoolCgpnTransformCssUnkn': '', 'useDevicePoolCgpnTransformCssSubs': '', 'useDevicePoolCalledCssNatl': '', 'useDevicePoolCalledCssIntl': '', 'useDevicePoolCalledCssUnkn': '', 'useDevicePoolCalledCssSubs': '', 'calledPartyNationalStripDigits': '', 'calledPartyInternationalStripDigits': '', 'calledPartyUnknownStripDigits': '', 'calledPartySubscriberStripDigits': '', 'calledPartyNationalTransformationCssName': '', 'calledPartyInternationalTransformationCssName': '', 'calledPartyUnknownTransformationCssName': '', 'calledPartySubscriberTransformationCssName': '', 'runOnEveryNode': '', 'useDevicePoolCntdPnTransformationCss': '', 'confidentialAccess': '', 'addressIpv4': '', 'sortOrder': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['h323Trunk']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_phone(self, name=''):
            """
            list_phone parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            :param protocol: protocol
            :param callingSearchSpaceName: callingSearchSpaceName
            :param devicePoolName: devicePoolName
            :param securityProfileName: securityProfileName
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listPhone(
                    {'name': '%'+name}, returnedTags={'ipAddress': '', 'ipv6Address': '', 'description': '', 'mode': '', 'name': '', 'isUserModifiable': '', 'phoneType': '', 'protocol': '', 'deviceSecurityMode': '', 'authenticationMode': '', 'keySize': '', 'keyOrder': '', 'ecKeySize': '', 'tftpEncryptedConfig': '', 'EnableOAuthAuthentication': '', 'nonceValidityTime': '', 'transportType': '', 'sipPhonePort': '', 'enableDigestAuthentication': '', 'excludeDigestCredentials': '', 'product': '', 'model': '', 'class': '', 'protocolSide': '', 'callingSearchSpaceName': '', 'devicePoolName': '', 'commonDeviceConfigName': '', 'commonPhoneConfigName': '', 'networkLocation': '', 'locationName': '', 'mediaResourceListName': '', 'networkHoldMohAudioSourceId': '', 'userHoldMohAudioSourceId': '', 'automatedAlternateRoutingCssName': '', 'aarNeighborhoodName': '', 'loadInformation': '', 'traceFlag': '', 'mlppIndicationStatus': '', 'preemption': '', 'useTrustedRelayPoint': '', 'retryVideoCallAsAudio': '', 'securityProfileName': '', 'sipProfileName': '', 'cgpnTransformationCssName': '', 'useDevicePoolCgpnTransformCss': '', 'geoLocationName': '', 'geoLocationFilterName': '', 'sendGeoLocation': '', 'numberOfButtons': '', 'phoneTemplateName': '', 'primaryPhoneName': '', 'ringSettingIdleBlfAudibleAlert': '', 'ringSettingBusyBlfAudibleAlert': '', 'userLocale': '', 'networkLocale': '', 'idleTimeout': '', 'authenticationUrl': '', 'directoryUrl': '', 'idleUrl': '', 'informationUrl': '', 'messagesUrl': '', 'proxyServerUrl': '', 'servicesUrl': '', 'softkeyTemplateName': '', 'loginUserId': '', 'defaultProfileName': '', 'enableExtensionMobility': '', 'currentProfileName': '', 'loginTime': '', 'loginDuration': '', 'currentConfig': '', 'singleButtonBarge': '', 'joinAcrossLines': '', 'builtInBridgeStatus': '', 'callInfoPrivacyStatus': '', 'hlogStatus': '', 'ownerUserName': '', 'ignorePresentationIndicators': '', 'packetCaptureMode': '', 'packetCaptureDuration': '', 'subscribeCallingSearchSpaceName': '', 'rerouteCallingSearchSpaceName': '', 'allowCtiControlFlag': '', 'presenceGroupName': '', 'unattendedPort': '', 'requireDtmfReception': '', 'rfc2833Disabled': '', 'certificateOperation': '', 'authenticationString': '', 'certificateStatus': '', 'upgradeFinishTime': '', 'deviceMobilityMode': '', 'roamingDevicePoolName': '', 'remoteDevice': '', 'dndOption': '', 'dndRingSetting': '', 'dndStatus': '', 'isActive': '', 'isDualMode': '', 'mobilityUserIdName': '', 'phoneSuite': '', 'phoneServiceDisplay': '', 'isProtected': '', 'mtpRequired': '', 'mtpPreferedCodec': '', 'dialRulesName': '', 'sshUserId': '', 'digestUser': '', 'outboundCallRollover': '', 'hotlineDevice': '', 'secureInformationUrl': '', 'secureDirectoryUrl': '', 'secureMessageUrl': '', 'secureServicesUrl': '', 'secureAuthenticationUrl': '', 'secureIdleUrl': '', 'alwaysUsePrimeLine': '', 'alwaysUsePrimeLineForVoiceMessage': '', 'featureControlPolicy': '', 'deviceTrustMode': '', 'earlyOfferSupportForVoiceCall': '', 'requireThirdPartyRegistration': '', 'blockIncomingCallsWhenRoaming': '', 'homeNetworkId': '', 'AllowPresentationSharingUsingBfcp': '', 'confidentialAccess': '', 'requireOffPremiseLocation': '', 'allowiXApplicableMedia': '', 'enableCallRoutingToRdWhenNoneIsActive': '', 'enableActivationID': '', 'mraServiceDomain': '', 'allowMraMode': '', 'activationCode': '', 'activationCodeExpiry': '', 'phoneName': '', 'phoneDescription': '', 'phoneModel': '', 'enableActivationId': '', 'userId': '', 'index': '', 'label': '', 'display': '', 'dirn': '', 'ringSetting': '', 'consecutiveRingSetting': '', 'ringSettingIdlePickupAlert': '', 'ringSettingActivePickupAlert': '', 'displayAscii': '', 'e164Mask': '', 'dialPlanWizardId': '', 'mwlPolicy': '', 'maxNumCalls': '', 'busyTrigger': '', 'callInfoDisplay': '', 'recordingProfileName': '', 'monitoringCssName': '', 'recordingFlag': '', 'audibleMwi': '', 'speedDial': '', 'partitionUsage': '', 'associatedEndusers': '', 'missedCallLogging': '', 'recordingMediaSource': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['phoneNtp']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_h323_gateway(self, name=''):
            """
            list_h323_gateway parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            :param protocol: protocol
            :param callingSearchSpaceName: callingSearchSpaceName
            :param devicePoolName: devicePoolName
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listH323Gateway(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'product': '', 'model': '', 'class': '', 'protocol': '', 'protocolSide': '', 'callingSearchSpaceName': '', 'devicePoolName': '', 'commonDeviceConfigName': '', 'networkLocation': '', 'locationName': '', 'mediaResourceListName': '', 'automatedAlternateRoutingCssName': '', 'aarNeighborhoodName': '', 'loadInformation': '', 'tunneledProtocol': '', 'asn1RoseOidEncoding': '', 'qsigVariant': '', 'pathReplacementSupport': '', 'traceFlag': '', 'useTrustedRelayPoint': '', 'retryVideoCallAsAudio': '', 'cgpnTransformationCssName': '', 'useDevicePoolCgpnTransformCss': '', 'geoLocationName': '', 'geoLocationFilterName': '', 'cdpnTransformationCssName': '', 'useDevicePoolCdpnTransformCss': '', 'packetCaptureMode': '', 'packetCaptureDuration': '', 'srtpAllowed': '', 'mtpRequired': '', 'callerIdDn': '', 'callingPartySelection': '', 'callingLineIdPresentation': '', 'enableInboundFaststart': '', 'enableOutboundFaststart': '', 'codecForOutboundFaststart': '', 'transmitUtf8': '', 'signalingPort': '', 'allowH235PassThrough': '', 'sigDigits': '', 'prefixDn': '', 'calledPartyIeNumberType': '', 'callingPartyIeNumberType': '', 'calledNumberingPlan': '', 'callingNumberingPlan': '', 'callingPartyNationalPrefix': '', 'callingPartyInternationalPrefix': '', 'callingPartyUnknownPrefix': '', 'callingPartySubscriberPrefix': '', 'callingPartyNationalStripDigits': '', 'callingPartyInternationalStripDigits': '', 'callingPartyUnknownStripDigits': '', 'callingPartySubscriberStripDigits': '', 'callingPartyNationalTransformationCssName': '', 'callingPartyInternationalTransformationCssName': '', 'callingPartyUnknownTransformationCssName': '', 'callingPartySubscriberTransformationCssName': '', 'calledPartyNationalPrefix': '', 'calledPartyInternationalPrefix': '', 'calledPartyUnknownPrefix': '', 'calledPartySubscriberPrefix': '', 'calledPartyNationalStripDigits': '', 'calledPartyInternationalStripDigits': '', 'calledPartyUnknownStripDigits': '', 'calledPartySubscriberStripDigits': '', 'calledPartyNationalTransformationCssName': '', 'calledPartyInternationalTransformationCssName': '', 'calledPartyUnknownTransformationCssName': '', 'calledPartySubscriberTransformationCssName': '', 'pstnAccess': '', 'imeE164TransformationName': '', 'displayIeDelivery': '', 'redirectOutboundNumberIe': '', 'redirectInboundNumberIe': '', 'useDevicePoolCgpnTransformCssNatl': '', 'useDevicePoolCgpnTransformCssIntl': '', 'useDevicePoolCgpnTransformCssUnkn': '', 'useDevicePoolCgpnTransformCssSubs': '', 'useDevicePoolCalledCssNatl': '', 'useDevicePoolCalledCssIntl': '', 'useDevicePoolCalledCssUnkn': '', 'useDevicePoolCalledCssSubs': '', 'useDevicePoolCntdPnTransformationCss': '', 'confidentialAccess': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['h323Gateway']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_device_profile(self, name=''):
            """
            list_device_profile parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listDeviceProfile(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'product': '', 'model': '', 'class': '', 'protocol': '', 'protocolSide': '', 'userHoldMohAudioSourceId': '', 'traceFlag': '', 'mlppIndicationStatus': '', 'preemption': '', 'phoneTemplateName': '', 'userLocale': '', 'defaultProfileName': '', 'currentProfileName': '', 'loginTime': '', 'loginDuration': '', 'singleButtonBarge': '', 'joinAcrossLines': '', 'loginUserId': '', 'ignorePresentationIndicators': '', 'dndOption': '', 'dndRingSetting': '', 'dndStatus': '', 'emccCallingSearchSpace': '', 'alwaysUsePrimeLine': '', 'alwaysUsePrimeLineForVoiceMessage': '', 'softkeyTemplateName': '', 'callInfoPrivacyStatus': '', 'currentConfig': '', 'featureControlPolicy': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['deviceProfile']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_remote_destination(self, name=''):
            """
            list_remote_destination parameters
            :param uuid: uuid
            :param name: name
            :param remoteDestinationProfileName: remoteDestinationProfileName
            :param ctiRemoteDeviceName: ctiRemoteDeviceName
            :param dualModeDeviceName: dualModeDeviceName
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listRemoteDestination(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'product': '', 'model': '', 'class': '', 'protocol': '', 'protocolSide': '', 'callingSearchSpaceName': '', 'devicePoolName': '', 'networkHoldMohAudioSourceId': '', 'userHoldMohAudioSourceId': '', 'callInfoPrivacyStatus': '', 'userId': '', 'ignorePresentationIndicators': '', 'rerouteCallingSearchSpaceName': '', 'cgpnTransformationCssName': '', 'automatedAlternateRoutingCssName': '', 'useDevicePoolCgpnTransformCss': '', 'userLocale': '', 'networkLocale': '', 'primaryPhoneName': '', 'dndOption': '', 'dndStatus': '', 'mobileSmartClientProfileName': '', 'destination': '', 'answerTooSoonTimer': '', 'answerTooLateTimer': '', 'delayBeforeRingingCell': '', 'remoteDestinationProfileName': '', 'ctiRemoteDeviceName': '', 'dualModeDeviceName': '', 'isMobilePhone': '', 'enableMobileConnect': '', 'timeZone': '', 'todAccessName': '', 'mobileSmartClientName': '', 'mobilityProfileName': '', 'singleNumberReachVoicemail': '', 'dialViaOfficeReverseVoicemail': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['remoteDestinationProfile']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_gateway(self, name=''):
            """
            list_gateway parameters
            :param uuid: uuid
            :param domainName: domainName
            :param description: description
            :param product: product
            :param protocol: protocol
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listGateway(
                    {'name': '%'+name}, returnedTags={'domainName': '', 'description': '', 'product': '', 'protocol': '', 'callManagerGroupName': '', 'scratch': '', 'loadInformation': '', 'unit': '', 'subunit': '', 'endpoint': '', 'index': '', 'name': '', 'model': '', 'class': '', 'protocolSide': '', 'callingSearchSpaceName': '', 'devicePoolName': '', 'commonDeviceConfigName': '', 'networkLocale': '', 'locationName': '', 'mediaResourceListName': '', 'automatedAlternateRoutingCssName': '', 'aarNeighborhoodName': '', 'vendorConfig': '', 'mlppDomainId': '', 'useTrustedRelayPoint': '', 'retryVideoCallAsAudio': '', 'cgpnTransformationCssName': '', 'useDevicePoolCgpnTransformCss': '', 'geoLocationName': '', 'geoLocationFilterName': '', 'port': '', 'trunkSelectionOrder': '', 'transmitUtf8': '', 'cdpnTransformationCssName': '', 'useDevicePoolCdpnTransformCss': '', 'callingPartyNumberPrefix': '', 'callingPartyStripDigits': '', 'callingPartyUnknownTransformationCssName': '', 'useDevicePoolCgpnTransformCssUnknown': '', 'hotlineDevice': '', 'packetCaptureMode': '', 'packetCaptureDuration': '', 'pstnAccess': '', 'imeE164TransformationName': '', 'imeE164DirectoryNumber': '', 'confidentialAccess': '', 'networkLocation': '', 'mlppIndicationStatus': '', 'mlppPreemption': '', 'redirectInboundNumberIe': '', 'calledPlan': '', 'calledPri': '', 'callerIdDn': '', 'callingPartySelection': '', 'callingPlan': '', 'callingPri': '', 'chanIE': '', 'clockReference': '', 'dChannelEnable': '', 'channelSelectionOrder': '', 'displayIe': '', 'pcmType': '', 'csuParam': '', 'firstDelay': '', 'interfaceIdPresent': '', 'interfaceId': '', 'intraDelay': '', 'mcdnEnable': '', 'redirectOutboundNumberIe': '', 'numDigitsToStrip': '', 'passingPrecedenceLevelThrough': '', 'prefix': '', 'callingLinePresentationBit': '', 'connectedLineIdPresentation': '', 'priProtocol': '', 'securityAccessLevel': '', 'sendCallingNameInFacilityIe': '', 'sendExLeadingCharInDispIe': '', 'sendRestart': '', 'setupNonIsdnPi': '', 'sigDigits': '', 'span': '', 'statusPoll': '', 'smdiBasePort': '', 'GClearEnable': '', 'v150': '', 'asn1RoseOidEncoding': '', 'qsigVariant': '', 'unattendedPort': '', 'nationalPrefix': '', 'internationalPrefix': '', 'unknownPrefix': '', 'subscriberPrefix': '', 'routeClassSignalling': '', 'nationalStripDigits': '', 'internationalStripDigits': '', 'unknownStripDigits': '', 'subscriberStripDigits': '', 'nationalTransformationCssName': '', 'internationalTransformationCssName': '', 'unknownTransformationCssName': '', 'subscriberTransformationCssName': '', 'useDevicePoolCgpnTransformCssNatl': '', 'useDevicePoolCgpnTransformCssIntl': '', 'useDevicePoolCgpnTransformCssUnkn': '', 'useDevicePoolCgpnTransformCssSubs': '', 'calledPartyNationalPrefix': '', 'calledPartyInternationalPrefix': '', 'calledPartyUnknownPrefix': '', 'calledPartySubscriberPrefix': '', 'calledPartyNationalStripDigits': '', 'calledPartyInternationalStripDigits': '', 'calledPartyUnknownStripDigits': '', 'calledPartySubscriberStripDigits': '', 'calledPartyNationalTransformationCssName': '', 'calledPartyInternationalTransformationCssName': '', 'calledPartyUnknownTransformationCssName': '', 'calledPartySubscriberTransformationCssName': '', 'useDevicePoolCalledCssNatl': '', 'useDevicePoolCalledCssIntl': '', 'useDevicePoolCalledCssUnkn': '', 'useDevicePoolCalledCssSubs': '', 'useDevicePoolCntdPartyTransformationCss': '', 'cntdPartyTransformationCssName': '', 'briProtocol': '', 'presentationBit': '', 'enableDatalinkOnFirstCall': '', 'traceFlag': '', 'preemption': '', 'sendGeoLocation': '', 'ports': '', 'digitSending': '', 'fdlChannel': '', 'yellowAlarm': '', 'zeroSupression': '', 'handleDtmfPrecedenceSignals': '', 'encodeOutboundVoiceRouteClass': '', 'phoneTemplateName': '', 'securityProfileName': '', 'userLocale': '', 'deviceMobilityMode': '', 'ownerUserId': '', 'commonPhoneConfigName': '', 'alwaysUsePrimeLine': '', 'alwaysUsePrimeLineForVM': '', 'allowCtiControlFlag': '', 'remoteDevice': '', 'subscribeCallingSearchSpaceName': '', 'presenceGroupName': '', 'hlogStatus': '', 'ignorePresentationIndicators': '', 'lines': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['gateway']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_cisco_catalyst600024_port_fxs_gateway(self, name=''):
            """
            list_cisco_catalyst600024_port_fxs_gateway parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            :param callingSearchSpaceName: callingSearchSpaceName
            :param devicePoolName: devicePoolName
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listCiscoCatalyst600024PortFXSGateway(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'product': '', 'model': '', 'class': '', 'protocol': '', 'protocolSide': '', 'callingSearchSpaceName': '', 'devicePoolName': '', 'commonDeviceConfigName': '', 'networkLocale': '', 'locationName': '', 'mediaResourceListName': '', 'automatedAlternateRoutingCssName': '', 'aarNeighborhoodName': '', 'loadInformation': '', 'traceFlag': '', 'useTrustedRelayPoint': '', 'cgpnTransformationCssName': '', 'useDevicePoolCgpnTransformCss': '', 'geoLocationName': '', 'portSelectionOrder': '', 'transmitUtf8': '', 'geoLocationFilterName': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['ciscoCatalyst600024PortFXSGateway']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_cisco_catalyst6000_e1_vo_ip_gateway(self, name=''):
            """
            list_cisco_catalyst6000_e1_vo_ip_gateway parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            :param callingSearchSpaceName: callingSearchSpaceName
            :param devicePoolName: devicePoolName
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listCiscoCatalyst6000E1VoIPGateway(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'product': '', 'model': '', 'class': '', 'protocol': '', 'protocolSide': '', 'callingSearchSpaceName': '', 'devicePoolName': '', 'commonDeviceConfigName': '', 'networkLocation': '', 'locationName': '', 'networkLocale': '', 'mediaResourceListName': '', 'automatedAlternateRoutingCssName': '', 'aarNeighborhoodName': '', 'loadInformation': '', 'useTrustedRelayPoint': '', 'cgpnTransformationCssName': '', 'useDevicePoolCgpnTransformCss': '', 'geoLocationName': '', 'redirectInboundNumberIe': '', 'calledPlan': '', 'calledPri': '', 'callerIdDn': '', 'callingPartySelection': '', 'callingPlan': '', 'callingPri': '', 'chanIe': '', 'clockReference': '', 'dChannelEnable': '', 'channelSelectionOrder': '', 'displayIE': '', 'pcmType': '', 'csuParam': '', 'firstDelay': '', 'interfaceIdPresent': '', 'interfaceId': '', 'intraDelay': '', 'mcdnEnable': '', 'redirectOutboundNumberIe': '', 'numDigitsToStrip': '', 'passingPrecedenceLevelThrough': '', 'prefix': '', 'callingLinePresentationBit': '', 'connectedLineIdPresentation': '', 'priProtocol': '', 'securityAccessLevel': '', 'sendCallingNameInFacilityIe': '', 'sendExLeadingCharInDispIe': '', 'sendRestart': '', 'setupNonIsdnPi': '', 'sigDigits': '', 'span': '', 'statusPoll': '', 'smdiBasePort': '', 'packetCaptureMode': '', 'packetCaptureDuration': '', 'transmitUtf8': '', 'v150': '', 'asn1RoseOidEncoding': '', 'QSIGVariant': '', 'unattendedPort': '', 'cdpnTransformationCssName': '', 'useDevicePoolCdpnTransformCss': '', 'nationalPrefix': '', 'internationalPrefix': '', 'unknownPrefix': '', 'subscriberPrefix': '', 'geoLocationFilterName': '', 'nationalStripDigits': '', 'internationalStripDigits': '', 'unknownStripDigits': '', 'subscriberStripDigits': '', 'nationalTransformationCssName': '', 'internationalTransformationCssName': '', 'unknownTransformationCssName': '', 'subscriberTransformationCssName': '', 'useDevicePoolCgpnTransformCssNatl': '', 'useDevicePoolCgpnTransformCssIntl': '', 'useDevicePoolCgpnTransformCssUnkn': '', 'useDevicePoolCgpnTransformCssSubs': '', 'pstnAccess': '', 'imeE164TransformationName': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['ciscoCatalyst6000E1VoIPGateway']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_cisco_catalyst6000_t1_vo_ip_gateway_pri(self, name=''):
            """
            list_cisco_catalyst6000_t1_vo_ip_gateway_pri parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            :param callingSearchSpaceName: callingSearchSpaceName
            :param devicePoolName: devicePoolName
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listCiscoCatalyst6000T1VoIPGatewayPri(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'product': '', 'model': '', 'class': '', 'protocol': '', 'protocolSide': '', 'callingSearchSpaceName': '', 'devicePoolName': '', 'commonDeviceConfigName': '', 'networkLocation': '', 'locationName': '', 'networkLocale': '', 'mediaResourceListName': '', 'automatedAlternateRoutingCssName': '', 'aarNeighborhoodName': '', 'loadInformation': '', 'mlppIndicationStatus': '', 'mlppPreemption': '', 'useTrustedRelayPoint': '', 'cgpnTransformationCssName': '', 'useDevicePoolCgpnTransformCss': '', 'geoLocationName': '', 'redirectInboundNumberIe': '', 'calledPlan': '', 'calledPri': '', 'callerIdDn': '', 'callingPartySelection': '', 'callingPlan': '', 'callingPri': '', 'chanIe': '', 'clockReference': '', 'dChannelEnable': '', 'channelSelectionOrder': '', 'displayIE': '', 'pcmType': '', 'csuParam': '', 'firstDelay': '', 'interfaceIdPresent': '', 'interfaceId': '', 'intraDelay': '', 'mcdnEnable': '', 'redirectOutboundNumberIe': '', 'numDigitsToStrip': '', 'passingPrecedenceLevelThrough': '', 'prefix': '', 'callingLinePresentationBit': '', 'connectedLineIdPresentation': '', 'priProtocol': '', 'securityAccessLevel': '', 'sendCallingNameInFacilityIe': '', 'sendExLeadingCharInDispIe': '', 'sendRestart': '', 'setupNonIsdnPi': '', 'sigDigits': '', 'span': '', 'statusPoll': '', 'smdiBasePort': '', 'packetCaptureMode': '', 'packetCaptureDuration': '', 'transmitUtf8': '', 'v150': '', 'asn1RoseOidEncoding': '', 'QSIGVariant': '', 'unattendedPort': '', 'cdpnTransformationCssName': '', 'useDevicePoolCdpnTransformCss': '', 'nationalPrefix': '', 'internationalPrefix': '', 'unknownPrefix': '', 'subscriberPrefix': '', 'geoLocationFilterName': '', 'nationalStripDigits': '', 'internationalStripDigits': '', 'unknownStripDigits': '', 'subscriberStripDigits': '', 'nationalTransformationCssName': '', 'internationalTransformationCssName': '', 'unknownTransformationCssName': '', 'subscriberTransformationCssName': '', 'useDevicePoolCgpnTransformCssNatl': '', 'useDevicePoolCgpnTransformCssIntl': '', 'useDevicePoolCgpnTransformCssUnkn': '', 'useDevicePoolCgpnTransformCssSubs': '', 'pstnAccess': '', 'imeE164TransformationName': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['ciscoCatalyst6000T1VoIPGatewayPri']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_cisco_catalyst6000_t1_vo_ip_gateway_t1(self, name=''):
            """
            list_cisco_catalyst6000_t1_vo_ip_gateway_t1 parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            :param callingSearchSpaceName: callingSearchSpaceName
            :param devicePoolName: devicePoolName
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listCiscoCatalyst6000T1VoIPGatewayT1(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'product': '', 'model': '', 'class': '', 'protocol': '', 'protocolSide': '', 'callingSearchSpaceName': '', 'devicePoolName': '', 'commonDeviceConfigName': '', 'networkLocation': '', 'locationName': '', 'mediaResourceListName': '', 'automatedAlternateRoutingCssName': '', 'aarNeighborhoodName': '', 'loadInformation': '', 'traceFlag': '', 'mlppIndicationStatus': '', 'preemption': '', 'useTrustedRelayPoint': '', 'retryVideoCallAsAudio': '', 'cgpnTransformationCssName': '', 'useDevicePoolCgpnTransformCss': '', 'geoLocationName': '', 'sendGeoLocation': '', 'trunkSelectionOrder': '', 'clockReference': '', 'csuParam': '', 'digitSending': '', 'pcmType': '', 'fdlChannel': '', 'yellowAlarm': '', 'zeroSupression': '', 'smdiBasePort': '', 'handleDtmfPrecedenceSignals': '', 'cdpnTransformationCssName': '', 'useDevicePoolCdpnTransformCss': '', 'geoLocationFilterName': '', 'pstnAccess': '', 'imeE164TransformationName': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['ciscoCatalyst6000T1VoIPGatewayT1']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_call_pickup_group(self, name=''):
            """
            list_call_pickup_group parameters
            :param uuid: uuid
            :param pattern: pattern
            :param description: description
            :param routePartitionName: routePartitionName
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listCallPickupGroup(
                    {'name': '%'+name}, returnedTags={'pattern': '', 'description': '', 'usage': '', 'routePartitionName': '', 'pickupNotification': '', 'pickupNotificationTimer': '', 'callInfoForPickupNotification': '', 'name': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['callPickupGroup']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_route_plan(self, name=''):
            """
            list_route_plan parameters
            :param uuid: uuid
            :param dnOrPattern: dnOrPattern
            :param partition: partition
            :param type: type
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listRoutePlan(
                    {'name': '%'+name}, returnedTags={'dnOrPattern': '', 'partition': '', 'type': '', 'routeDetail': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['routePlan']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_geo_location_policy(self, name=''):
            """
            list_geo_location_policy parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listGeoLocationPolicy(
                    {'name': '%'+name}, returnedTags={'name': '', 'country': '', 'description': '', 'nationalSubDivision': '', 'district': '', 'communityName': '', 'cityDivision': '', 'neighbourhood': '', 'street': '', 'leadingStreetDirection': '', 'trailingStreetSuffix': '', 'streetSuffix': '', 'houseNumber': '', 'houseNumberSuffix': '', 'landmark': '', 'location': '', 'floor': '', 'occupantName': '', 'postalCode': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['geoLocationPolicy']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_sip_trunk(self, name=''):
            """
            list_sip_trunk parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            :param callingSearchSpaceName: callingSearchSpaceName
            :param devicePoolName: devicePoolName
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listSipTrunk(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'securityMode': '', 'incomingTransport': '', 'outgoingTransport': '', 'digestAuthentication': '', 'noncePolicyTime': '', 'x509SubjectName': '', 'incomingPort': '', 'applLevelAuthentication': '', 'acceptPresenceSubscription': '', 'acceptOutOfDialogRefer': '', 'acceptUnsolicitedNotification': '', 'allowReplaceHeader': '', 'transmitSecurityStatus': '', 'sipV150OutboundSdpOfferFiltering': '', 'allowChargingHeader': '', 'product': '', 'model': '', 'class': '', 'protocol': '', 'protocolSide': '', 'callingSearchSpaceName': '', 'devicePoolName': '', 'commonDeviceConfigName': '', 'networkLocation': '', 'locationName': '', 'mediaResourceListName': '', 'networkHoldMohAudioSourceId': '', 'userHoldMohAudioSourceId': '', 'automatedAlternateRoutingCssName': '', 'aarNeighborhoodName': '', 'packetCaptureMode': '', 'packetCaptureDuration': '', 'loadInformation': '', 'traceFlag': '', 'mlppIndicationStatus': '', 'preemption': '', 'useTrustedRelayPoint': '', 'retryVideoCallAsAudio': '', 'securityProfileName': '', 'sipProfileName': '', 'cgpnTransformationCssName': '', 'useDevicePoolCgpnTransformCss': '', 'geoLocationName': '', 'geoLocationFilterName': '', 'sendGeoLocation': '', 'cdpnTransformationCssName': '', 'useDevicePoolCdpnTransformCss': '', 'unattendedPort': '', 'transmitUtf8': '', 'subscribeCallingSearchSpaceName': '', 'rerouteCallingSearchSpaceName': '', 'referCallingSearchSpaceName': '', 'mtpRequired': '', 'presenceGroupName': '', 'unknownPrefix': '', 'destAddrIsSrv': '', 'tkSipCodec': '', 'sigDigits': '', 'connectedNamePresentation': '', 'connectedPartyIdPresentation': '', 'callingPartySelection': '', 'callingname': '', 'callingLineIdPresentation': '', 'prefixDn': '', 'acceptInboundRdnis': '', 'acceptOutboundRdnis': '', 'srtpAllowed': '', 'srtpFallbackAllowed': '', 'isPaiEnabled': '', 'sipPrivacy': '', 'isRpidEnabled': '', 'sipAssertedType': '', 'trustReceivedIdentity': '', 'dtmfSignalingMethod': '', 'routeClassSignalling': '', 'sipTrunkType': '', 'pstnAccess': '', 'imeE164TransformationName': '', 'useImePublicIpPort': '', 'useDevicePoolCntdPnTransformationCss': '', 'useDevicePoolCgpnTransformCssUnkn': '', 'rdnTransformationCssName': '', 'useDevicePoolRdnTransformCss': '', 'useOrigCallingPartyPresOnDivert': '', 'sipNormalizationScriptName': '', 'runOnEveryNode': '', 'unknownStripDigits': '', 'cgpnTransformationUnknownCssName': '', 'tunneledProtocol': '', 'asn1RoseOidEncoding': '', 'qsigVariant': '', 'pathReplacementSupport': '', 'enableQsigUtf8': '', 'scriptParameters': '', 'scriptTraceEnabled': '', 'trunkTrafficSecure': '', 'callingAndCalledPartyInfoFormat': '', 'useCallerIdCallerNameinUriOutgoingRequest': '', 'requestUriDomainName': '', 'enableCiscoRecordingQsigTunneling': '', 'calledPartyUnknownTransformationCssName': '', 'calledPartyUnknownPrefix': '', 'calledPartyUnknownStripDigits': '', 'useDevicePoolCalledCssUnkn': '', 'confidentialAccess': '', 'addressIpv4': '', 'addressIpv6': '', 'port': '', 'sortOrder': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['sipTrunkSecurityProfile']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_called_party_transformation_pattern(self, name=''):
            """
            list_called_party_transformation_pattern parameters
            :param uuid: uuid
            :param pattern: pattern
            :param description: description
            :param routePartitionName: routePartitionName
            :param dialPlanName: dialPlanName
            :param routeFilterName: routeFilterName
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listCalledPartyTransformationPattern(
                    {'name': '%'+name}, returnedTags={'pattern': '', 'description': '', 'usage': '', 'routePartitionName': '', 'calledPartyTransformationMask': '', 'dialPlanName': '', 'digitDiscardInstructionName': '', 'patternUrgency': '', 'routeFilterName': '', 'calledPartyPrefixDigits': '', 'calledPartyNumberingPlan': '', 'calledPartyNumberType': '', 'mlppPreemptionDisabled': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['calledPartyTransformationPattern']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_external_call_control_profile(self, name=''):
            """
            list_external_call_control_profile parameters
            :param uuid: uuid
            :param name: name
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listExternalCallControlProfile(
                    {'name': '%'+name}, returnedTags={'name': '', 'primaryUri': '', 'secondaryUri': '', 'enableLoadBalancing': '', 'routingRequestTimer': '', 'diversionReroutingCssName': '', 'callTreatmentOnFailure': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['externalCallControlProfile']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_saf_security_profile(self, name=''):
            """
            list_saf_security_profile parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            :param userid: userid
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listSafSecurityProfile(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'userid': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['safSecurityProfile']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_saf_forwarder(self, name=''):
            """
            list_saf_forwarder parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listSafForwarder(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'clientLabel': '', 'safSecurityProfile': '', 'ipAddress': '', 'port': '', 'enableTcpKeepAlive': '', 'safReconnectInterval': '', 'safNotificationsWindowSize': '', 'callManagerName': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['safForwarder']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_ccd_hosted_dn(self, name=''):
            """
            list_ccd_hosted_dn parameters
            :param uuid: uuid
            :param hostedPattern: hostedPattern
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listCcdHostedDN(
                    {'name': '%'+name}, returnedTags={'hostedPattern': '', 'description': '', 'CcdHostedDnGroup': '', 'pstnFailoverStripDigits': '', 'pstnFailoverPrependDigits': '', 'usePstnFailover': '', 'name': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['ccdHostedDN']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_ccd_hosted_dn_group(self, name=''):
            """
            list_ccd_hosted_dn_group parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listCcdHostedDNGroup(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'pstnFailoverStripDigits': '', 'pstnFailoverPrependDigits': '', 'usePstnFailover': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['ccdHostedDNGroup']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_remote_cluster(self, name=''):
            """
            list_remote_cluster parameters
            :param uuid: uuid
            :param clusterId: clusterId
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listRemoteCluster(
                    {'name': '%'+name}, returnedTags={'clusterId': '', 'description': '', 'fullyQualifiedName': '', 'emcc': '', 'pstnAccess': '', 'rsvpAgent': '', 'tftp': '', 'lbm': '', 'uds': '', 'enabled': '', 'remoteIpAddress1': '', 'remoteIpAddress2': '', 'remoteIpAddress3': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['remoteCluster']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_ccd_advertising_service(self, name=''):
            """
            list_ccd_advertising_service parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listCcdAdvertisingService(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'isActivated': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['ccdAdvertisingService']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_ldap_directory(self, name=''):
            """
            list_ldap_directory parameters
            :param uuid: uuid
            :param name: name
            :param ldapDn: ldapDn
            :param userSearchBase: userSearchBase
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listLdapDirectory(
                    {'name': '%'+name}, returnedTags={'name': '', 'ldapDn': '', 'userSearchBase': '', 'repeatable': '', 'intervalValue': '', 'scheduleUnit': '', 'nextExecTime': '', 'accessControlGroupInfo': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['ldapDirectory']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_saf_ccd_purge_block_learned_routes(self, name=''):
            """
            list_saf_ccd_purge_block_learned_routes parameters
            :param uuid: uuid
            :param learnedPattern: learnedPattern
            :param learnedPatternPrefix: learnedPatternPrefix
            :param callControlIdentity: callControlIdentity
            :param ipAddress: ipAddress
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listSafCcdPurgeBlockLearnedRoutes(
                    {'name': '%'+name}, returnedTags={'learnedPattern': '', 'learnedPatternPrefix': '', 'callControlIdentity': '', 'ipAddress': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['safCcdPurgeBlockLearnedRoutes']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_vpn_gateway(self, name=''):
            """
            list_vpn_gateway parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listVpnGateway(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'url': '', 'issuerName': '', 'serialNumber': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['vpnGateway']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_vpn_group(self, name=''):
            """
            list_vpn_group parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listVpnGroup(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'vpnGatewayName': '', 'priority': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['vpnGroup']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_vpn_profile(self, name=''):
            """
            list_vpn_profile parameters
            :param uuid: uuid
            :param name: name
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listVpnProfile(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'autoNetworkDetection': '', 'mtu': '', 'failToConnect': '', 'clientAuthentication': '', 'pwdPersistant': '', 'enableHostIdCheck': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['vpnProfile']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_ime_server(self, name=''):
            """
            list_ime_server parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listImeServer(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'ipAddress': '', 'port': '', 'deviceSecurityMode': '', 'applicationUser': '', 'reconnectInterval': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['imeServer']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_ime_route_filter_group(self, name=''):
            """
            list_ime_route_filter_group parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listImeRouteFilterGroup(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'groupTrustSetting': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['imeRouteFilterGroup']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_ime_route_filter_element(self, name=''):
            """
            list_ime_route_filter_element parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listImeRouteFilterElement(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'elementType': '', 'imeRouteFilterGroupName': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['imeRouteFilterElement']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_ime_client(self, name=''):
            """
            list_ime_client parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            :param domain: domain
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listImeClient(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'domain': '', 'isActivated': '', 'sipTrunkName': '', 'primaryImeServerName': '', 'secondaryImeServerName': '', 'learnedRouteFilterGroupName': '', 'exclusionNumberGroupName': '', 'firewallName': '', 'enrolledPatternGroupName': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['imeClient']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_ime_enrolled_pattern(self, name=''):
            """
            list_ime_enrolled_pattern parameters
            :param uuid: uuid
            :param pattern: pattern
            :param description: description
            :param imeEnrolledPatternGroupName: imeEnrolledPatternGroupName
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listImeEnrolledPattern(
                    {'name': '%'+name}, returnedTags={'pattern': '', 'description': '', 'imeEnrolledPatternGroupName': '', 'name': '', 'fallbackProfileName': '', 'isPatternAllAlias': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['imeEnrolledPattern']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_ime_enrolled_pattern_group(self, name=''):
            """
            list_ime_enrolled_pattern_group parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listImeEnrolledPatternGroup(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'fallbackProfileName': '', 'isPatternAllAlias': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['imeEnrolledPatternGroup']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_ime_exclusion_number(self, name=''):
            """
            list_ime_exclusion_number parameters
            :param uuid: uuid
            :param pattern: pattern
            :param description: description
            :param imeExclusionNumberGroupName: imeExclusionNumberGroupName
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listImeExclusionNumber(
                    {'name': '%'+name}, returnedTags={'pattern': '', 'description': '', 'imeExclusionNumberGroupName': '', 'name': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['imeExclusionNumber']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_ime_exclusion_number_group(self, name=''):
            """
            list_ime_exclusion_number_group parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listImeExclusionNumberGroup(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['imeExclusionNumberGroup']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_ime_firewall(self, name=''):
            """
            list_ime_firewall parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            :param ipAddress: ipAddress
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listImeFirewall(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'ipAddress': '', 'port': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['imeFirewall']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_ime_e164_transformation(self, name=''):
            """
            list_ime_e164_transformation parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listImeE164Transformation(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'cgpnTransformationCssName': '', 'isCgpnPreTransformation': '', 'cdpnTransformationCssName': '', 'isCdpnPreTransformation': '', 'incomingCgpnTransformationProfileName': '', 'incomingCdpnTransformationProfileName': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['imeE164Transformation']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_transformation_profile(self, name=''):
            """
            list_transformation_profile parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listTransformationProfile(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'nationalStripDigits': '', 'internationalStripDigits': '', 'unknownStripDigits': '', 'subscriberStripDigits': '', 'nationalPrefix': '', 'internationalPrefix': '', 'unknownPrefix': '', 'subscriberPrefix': '', 'nationalCssName': '', 'internationalCssName': '', 'unknownCssName': '', 'subscriberCssName': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['transformationProfile']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_fallback_profile(self, name=''):
            """
            list_fallback_profile parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listFallbackProfile(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'advertisedFallbackDirectoryE164Number': '', 'qosSensistivityLevel': '', 'callCss': '', 'callAnswerTimer': '', 'directoryNumberPartition': '', 'directoryNumber': '', 'numberOfDigitsForCallerIDPartialMatch': '', 'numberOfCorrelationDtmfDigits': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['fallbackProfile']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_ldap_filter(self, name=''):
            """
            list_ldap_filter parameters
            :param uuid: uuid
            :param name: name
            :param filter: filter
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listLdapFilter(
                    {'name': '%'+name}, returnedTags={'name': '', 'filter': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['ldapFilter']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_tvs_certificate(self, name=''):
            """
            list_tvs_certificate parameters
            :param uuid: uuid
            :param subjectName: subjectName
            :param issuerName: issuerName
            :param serialNumber: serialNumber
            :param timeToLive: timeToLive
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listTvsCertificate(
                    {'name': '%'+name}, returnedTags={'subjectName': '', 'issuerName': '', 'serialNumber': '', 'timeToLive': '', 'ipv4Address': '', 'ipv6Address': '', 'serviceName': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['tvsCertificate']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_feature_control_policy(self, name=''):
            """
            list_feature_control_policy parameters
            :param uuid: uuid
            :param name: name
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listFeatureControlPolicy(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['featureControlPolicy']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_mobility_profile(self, name=''):
            """
            list_mobility_profile parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listMobilityProfile(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'mobileClientCallingOption': '', 'dvofServiceAccessNumber': '', 'dvorCallerId': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['mobilityProfile']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_enterprise_feature_access_configuration(self, name=''):
            """
            list_enterprise_feature_access_configuration parameters
            :param uuid: uuid
            :param pattern: pattern
            :param routePartitionName: routePartitionName
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listEnterpriseFeatureAccessConfiguration(
                    {'name': '%'+name}, returnedTags={'pattern': '', 'routePartitionName': '', 'description': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['enterpriseFeatureAccessConfiguration']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_called_party_tracing(self, name=''):
            """
            list_called_party_tracing parameters
            :param uuid: uuid
            :param directorynumber: directorynumber
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listCalledPartyTracing(
                    {'name': '%'+name}, returnedTags={'directorynumber': '', 'description': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['calledPartyTracing']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_sip_normalization_script(self, name=''):
            """
            list_sip_normalization_script parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listSIPNormalizationScript(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'scriptExecutionErrorRecoveryAction': '', 'systemResourceErrorRecoveryAction': '', 'maxMemoryThreshold': '', 'maxLuaInstructionsThreshold': '', 'isStandard': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['sIPNormalizationScript']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_custom_user_field(self, name=''):
            """
            list_custom_user_field parameters
            :param uuid: uuid
            :param field: field
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listCustomUserField(
                    {'name': '%'+name}, returnedTags={'field': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['customUserField']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_billing_server(self, name=''):
            """
            list_billing_server parameters
            :param uuid: uuid
            :param hostName: hostName
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listBillingServer(
                    {'name': '%'+name}, returnedTags={'hostName': '', 'userId': '', 'password': '', 'directory': '', 'resendOnFailure': '', 'billingServerProtocol': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['billingServer']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_lbm_group(self, name=''):
            """
            list_lbm_group parameters
            :param uuid: uuid
            :param name: name
            :param Description: Description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listLbmGroup(
                    {'name': '%'+name}, returnedTags={'name': '', 'Description': '', 'ProcessnodeActive': '', 'ProcessnodeStandby': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['lbmGroup']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_announcement(self, name=''):
            """
            list_announcement parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listAnnouncement(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'announcementFile': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['announcement']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_service_profile(self, name=''):
            """
            list_service_profile parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listServiceProfile(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'isDefault': '', 'profileName': '', 'primary': '', 'secondary': '', 'tertiary': '', 'serverCertificateVerification': '', 'serviceProfileXml': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['serviceProfile']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_audio_codec_preference_list(self, name=''):
            """
            list_audio_codec_preference_list parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listAudioCodecPreferenceList(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['audioCodecPreferenceList']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_uc_service(self, name=''):
            """
            list_uc_service parameters
            :param uuid: uuid
            :param name: name
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listUcService(
                    {'name': '%'+name}, returnedTags={'serviceType': '', 'productType': '', 'name': '', 'description': '', 'hostnameorip': '', 'port': '', 'protocol': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['ucService']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_lbm_hub_group(self, name=''):
            """
            list_lbm_hub_group parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listLbmHubGroup(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'member1': '', 'member2': '', 'member3': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['lbmHubGroup']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_imported_directory_uri_catalogs(self, name=''):
            """
            list_imported_directory_uri_catalogs parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            :param routeString: routeString
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listImportedDirectoryUriCatalogs(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'routeString': '', 'lastLoadedFileName': '', 'fileLoadDateTime': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['importedDirectoryUriCatalogs']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_voh_server(self, name=''):
            """
            list_voh_server parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            :param defaultVideoStreamId: defaultVideoStreamId
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listVohServer(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'sipTrunkName': '', 'defaultVideoStreamId': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['vohServer']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_sdp_transparency_profile(self, name=''):
            """
            list_sdp_transparency_profile parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listSdpTransparencyProfile(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['sdpTransparencyProfile']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_feature_group_template(self, name=''):
            """
            list_feature_group_template parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listFeatureGroupTemplate(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'homeCluster': '', 'imAndUcPresenceEnable': '', 'serviceProfile': '', 'enableUserToHostConferenceNow': '', 'allowCTIControl': '', 'enableEMCC': '', 'enableMobility': '', 'enableMobileVoiceAccess': '', 'maxDeskPickupWait': '', 'remoteDestinationLimit': '', 'BLFPresenceGp': '', 'subscribeCallingSearch': '', 'userLocale': '', 'userProfile': '', 'meetingInformation': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['featureGroupTemplate']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_dir_number_alias_lookupand_sync(self, name=''):
            """
            list_dir_number_alias_lookupand_sync parameters
            :param uuid: uuid
            :param ldapConfigName: ldapConfigName
            :param ldapManagerDisgName: ldapManagerDisgName
            :param ldapUserSearch: ldapUserSearch
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listDirNumberAliasLookupandSync(
                    {'name': '%'+name}, returnedTags={'ldapConfigName': '', 'ldapManagerDisgName': '', 'ldapPassword': '', 'ldapUserSearch': '', 'ldapDirectoryServerUsage': '', 'keepAliveSearch': '', 'keepAliveTime': '', 'sipAliasSuffix': '', 'enableCachingofRecords': '', 'cacheSizeforAliasLookup': '', 'cacheAgeforAliasLookup': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['dirNumberAliasLookupandSync']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_local_route_group(self, name=''):
            """
            list_local_route_group parameters
            :param uuid: uuid
            :param name: name
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listLocalRouteGroup(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['localRouteGroup']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_advertised_patterns(self, name=''):
            """
            list_advertised_patterns parameters
            :param uuid: uuid
            :param description: description
            :param pattern: pattern
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listAdvertisedPatterns(
                    {'name': '%'+name}, returnedTags={'description': '', 'pattern': '', 'patternType': '', 'hostedRoutePSTNRule': '', 'pstnFailStrip': '', 'pstnFailPrepend': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['advertisedPatterns']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_blocked_learned_patterns(self, name=''):
            """
            list_blocked_learned_patterns parameters
            :param uuid: uuid
            :param description: description
            :param pattern: pattern
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listBlockedLearnedPatterns(
                    {'name': '%'+name}, returnedTags={'description': '', 'pattern': '', 'prefix': '', 'clusterId': '', 'patternType': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['blockedLearnedPatterns']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_cca_profiles(self, name=''):
            """
            list_cca_profiles parameters
            :param uuid: uuid
            :param ccaId: ccaId
            :param primarySoftSwitchId: primarySoftSwitchId
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listCCAProfiles(
                    {'name': '%'+name}, returnedTags={'ccaId': '', 'primarySoftSwitchId': '', 'secondarySoftSwitchId': '', 'objectClass': '', 'subscriberType': '', 'sipAliasSuffix': '', 'sipUserNameSuffix': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['cCAProfiles']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_universal_device_template(self, name=''):
            """
            list_universal_device_template parameters
            :param uuid: uuid
            :param name: name
            :param deviceDescription: deviceDescription
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listUniversalDeviceTemplate(
                    {'name': '%'+name}, returnedTags={'name': '', 'deviceDescription': '', 'devicePool': '', 'deviceSecurityProfile': '', 'sipProfile': '', 'phoneButtonTemplate': '', 'sipDialRules': '', 'callingSearchSpace': '', 'callingPartyTransformationCSSForInboundCalls': '', 'callingPartyTransformationCSSForOutboundCalls': '', 'reroutingCallingSearchSpace': '', 'subscribeCallingSearchSpaceName': '', 'useDevicePoolCallingPartyTransformationCSSforInboundCalls': '', 'useDevicePoolCallingPartyTransformationCSSforOutboundCalls': '', 'commonPhoneProfile': '', 'commonDeviceConfiguration': '', 'softkeyTemplate': '', 'featureControlPolicy': '', 'phonePersonalization': '', 'mtpPreferredOriginatingCodec': '', 'outboundCallRollover': '', 'mediaTerminationPointRequired': '', 'unattendedPort': '', 'requiredDtmfReception': '', 'rfc2833Disabled': '', 'useTrustedRelayPoint': '', 'protectedDevice': '', 'certificateOperation': '', 'authenticationMode': '', 'authenticationString': '', 'keySize': '', 'keyOrder': '', 'ecKeySize': '', 'servicesProvisioning': '', 'packetCaptureMode': '', 'packetCaptureDuration': '', 'secureShellUser': '', 'secureShellPassword': '', 'userLocale': '', 'networkLocale': '', 'mlppDomain': '', 'mlppIndication': '', 'mlppPreemption': '', 'doNotDisturb': '', 'dndOption': '', 'dndIncomingCallAlert': '', 'aarGroup': '', 'aarCallingSearchSpace': '', 'blfPresenceGroup': '', 'blfAudibleAlertSettingPhoneBusy': '', 'blfAudibleAlertSettingPhoneIdle': '', 'userHoldMohAudioSource': '', 'networkHoldMohAudioSource': '', 'location': '', 'geoLocation': '', 'deviceMobilityMode': '', 'mediaResourceGroupList': '', 'remoteDevice': '', 'hotlineDevice': '', 'retryVideoCallAsAudio': '', 'requireOffPremiseLocation': '', 'ownerUserId': '', 'mobilityUserId': '', 'joinAcrossLines': '', 'alwaysUsePrimeLine': '', 'alwaysUsePrimeLineForVoiceMessage': '', 'singleButtonBarge': '', 'builtInBridge': '', 'allowControlOfDeviceFromCti': '', 'ignorePresentationIndicators': '', 'enableExtensionMobility': '', 'privacy': '', 'loggedIntoHuntGroup': '', 'proxyServer': '', 'servicesUrl': '', 'idle': '', 'idleTimer': '', 'secureDirUrl': '', 'messages': '', 'secureIdleUrl': '', 'authenticationServer': '', 'directory': '', 'secureServicesUrl': '', 'information': '', 'secureMessagesUrl': '', 'secureInformationUrl': '', 'secureAuthenticationUrl': '', 'confidentialAccess': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['universalDeviceTemplate']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_user_profile_provision(self, name=''):
            """
            list_user_profile_provision parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listUserProfileProvision(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'allowProvision': '', 'limitProvision': '', 'defaultUserProfile': '', 'allowProvisionEMMaxLoginTime': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['userProfileProvision']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_presence_redundancy_group(self, name=''):
            """
            list_presence_redundancy_group parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listPresenceRedundancyGroup(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'server1': '', 'server2': '', 'haEnabled': '', 'numUsers': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['presenceRedundancyGroup']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_assigned_presence_servers(self, name=''):
            """
            list_assigned_presence_servers parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listAssignedPresenceServers(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'nodeUsage': '', 'numUsers': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['assignedPresenceServers']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_unassigned_presence_servers(self, name=''):
            """
            list_unassigned_presence_servers parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listUnassignedPresenceServers(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'nodeUsage': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['unassignedPresenceServers']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_assigned_presence_users(self, name=''):
            """
            list_assigned_presence_users parameters
            :param uuid: uuid
            :param userid: userid
            :param server: server
            :param presenceRedundancyGroup: presenceRedundancyGroup
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listAssignedPresenceUsers(
                    {'name': '%'+name}, returnedTags={'userid': '', 'server': '', 'presenceRedundancyGroup': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['assignedPresenceUsers']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_unassigned_presence_users(self, name=''):
            """
            list_unassigned_presence_users parameters
            :param uuid: uuid
            :param userid: userid
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listUnassignedPresenceUsers(
                    {'name': '%'+name}, returnedTags={'userid': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['unassignedPresenceUsers']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_wifi_hotspot(self, name=''):
            """
            list_wifi_hotspot parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            :param ssidPrefix: ssidPrefix
            :param authenticationMethod: authenticationMethod
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listWifiHotspot(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'ssidPrefix': '', 'authenticationMethod': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['wifiHotspot']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_wlan_profile_group(self, name=''):
            """
            list_wlan_profile_group parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listWlanProfileGroup(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['wlanProfileGroup']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_wlan_profile(self, name=''):
            """
            list_wlan_profile parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            :param ssid: ssid
            :param networkAccessProfile: networkAccessProfile
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listWLANProfile(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'ssid': '', 'frequencyBand': '', 'userModifiable': '', 'authMethod': '', 'userName': '', 'password': '', 'pskPassphrase': '', 'wepKey': '', 'passwordDescription': '', 'networkAccessProfile': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['wLANProfile']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_universal_line_template(self, name=''):
            """
            list_universal_line_template parameters
            :param uuid: uuid
            :param name: name
            :param lineDescription: lineDescription
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listUniversalLineTemplate(
                    {'name': '%'+name}, returnedTags={'name': '', 'urgentPriority': '', 'lineDescription': '', 'routePartition': '', 'voiceMailProfile': '', 'callingSearchSpace': '', 'alertingName': '', 'extCallControlProfile': '', 'blfPresenceGroup': '', 'callPickupGroup': '', 'partyEntranceTone': '', 'autoAnswer': '', 'rejectAnonymousCall': '', 'userHoldMohAudioSource': '', 'networkHoldMohAudioSource': '', 'aarDestinationMask': '', 'aarGroup': '', 'retainDestInCallFwdHistory': '', 'forwardDestAllCalls': '', 'primaryCssForwardingAllCalls': '', 'secondaryCssForwardingAllCalls': '', 'CssActivationPolicy': '', 'fwdDestExtCallsWhenNotRetrieved': '', 'cssFwdExtCallsWhenNotRetrieved': '', 'fwdDestInternalCallsWhenNotRetrieved': '', 'cssFwdInternalCallsWhenNotRetrieved': '', 'parkMonitorReversionTime': '', 'target': '', 'mlppCss': '', 'mlppNoAnsRingDuration': '', 'confidentialAccess': '', 'holdReversionRingDuration': '', 'holdReversionNotificationInterval': '', 'busyIntCallsDestination': '', 'busyIntCallsCss': '', 'busyExtCallsDestination': '', 'busyExtCallsCss': '', 'noAnsIntCallsDestination': '', 'noAnsIntCallsCss': '', 'noAnsExtCallsDestination': '', 'noAnsExtCallsCss': '', 'noCoverageIntCallsDestination': '', 'noCoverageIntCallsCss': '', 'noCoverageExtCallsDestination': '', 'noCoverageExtCallsCss': '', 'unregisteredIntCallsDestination': '', 'unregisteredIntCallsCss': '', 'unregisteredExtCallsDestination': '', 'unregisteredExtCallsCss': '', 'ctiFailureDestination': '', 'ctiFailureCss': '', 'callControlAgentProfile': '', 'enterpriseAltNum': '', 'e164AltNum': '', 'advertisedFailoverNumber': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['universalLineTemplate']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_network_access_profile(self, name=''):
            """
            list_network_access_profile parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listNetworkAccessProfile(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['networkAccessProfile']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_licensed_user(self, name=''):
            """
            list_licensed_user parameters
            :param uuid: uuid
            :param userId: userId
            :param firstName: firstName
            :param lastName: lastName
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listLicensedUser(
                    {'name': '%'+name}, returnedTags={'userId': '', 'firstName': '', 'lastName': '', 'snrEnabled': '', 'emEnabled': '', 'deviceCount': '', 'licenseType': '', 'licenseUsed': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['licensedUser']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_elin_group(self, name=''):
            """
            list_elin_group parameters
            :param uuid: uuid
            :param name: name
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listElinGroup(
                    {'name': '%'+name}, returnedTags={'name': '', 'elinNumbers': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['elinGroup']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_unassigned_device(self, name=''):
            """
            list_unassigned_device parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listUnassignedDevice(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'deviceType': '', 'licenseType': '', 'extension': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['unassignedDevice']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_registration_dynamic(self, name=''):
            """
            list_registration_dynamic parameters
            :param uuid: uuid
            :param device: device
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listRegistrationDynamic(
                    {'name': '%'+name}, returnedTags={'device': '', 'lastKnownIpAddress': '', 'lastKnownUcm': '', 'lastKnownConfigVersion': '', 'locationDetails': '', 'endpointConnection': '', 'portOrSsid': '', 'lastSeen': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['registrationDynamic']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_infrastructure_device(self, name=''):
            """
            list_infrastructure_device parameters
            :param uuid: uuid
            :param name: name
            :param isActive: isActive
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listInfrastructureDevice(
                    {'name': '%'+name}, returnedTags={'name': '', 'ipv4Address': '', 'ipv6Address': '', 'bssidWithMask': '', 'wapLocation': '', 'isActive': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['infrastructureDevice']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_ldap_search(self, name=''):
            """
            list_ldap_search parameters
            :param uuid: uuid
            :param distinguishedName: distinguishedName
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listLdapSearch(
                    {'name': '%'+name}, returnedTags={'enableDirectorySearch': '', 'distinguishedName': '', 'userSearchBase1': '', 'userSearchBase2': '', 'userSearchBase3': '', 'enableRecursiveSearch': '', 'primary': '', 'secondary': '', 'tertiary': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['ldapSearch']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_wireless_access_point_controllers(self, name=''):
            """
            list_wireless_access_point_controllers parameters
            :param uuid: uuid
            :param name: name
            :param description: description
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listWirelessAccessPointControllers(
                    {'name': '%'+name}, returnedTags={'name': '', 'description': '', 'snmpVersion': '', 'snmpUserIdOrCommunityString': '', 'snmpAuthenticationProtocol': '', 'snmpAuthenticationPassword': '', 'snmpPrivacyProtocol': '', 'snmpPrivacyPassword': '', 'syncNow': '', 'syncStatus': '', 'resyncInterval': '', 'nextSyncTime': '', 'scheduleUnit': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['wirelessAccessPointControllers']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_phone_activation_code(self, name=''):
            """
            list_phone_activation_code parameters
            :param uuid: uuid
            :param phoneName: phoneName
            :param userId: userId
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listPhoneActivationCode(
                    {'name': '%'+name}, returnedTags={'activationCode': '', 'activationCodeExpiry': '', 'phoneName': '', 'phoneDescription': '', 'phoneModel': '', 'enableActivationId': '', 'userId': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['phoneActivationCode']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_device_defaults(self, name=''):
            """
            list_device_defaults parameters
            :param uuid: uuid
            :param Model: Model
            :param Protocol: Protocol
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listDeviceDefaults(
                    {'name': '%'+name}, returnedTags={'Model': '', 'Protocol': '', 'LoadInformation': '', 'InactiveLoadInformation': '', 'DevicePoolName': '', 'PhoneButtonTemplate': '', 'PreferActCodeOverAutoReg': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['deviceDefaults']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_mra_service_domain(self, name=''):
            """
            list_mra_service_domain parameters
            :param uuid: uuid
            :param name: name
            :param isDefault: isDefault
            :param serviceDomains: serviceDomains
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listMraServiceDomain(
                    {'name': '%'+name}, returnedTags={'name': '', 'isDefault': '', 'serviceDomains': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['mraServiceDomain']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_cisco_cloud_onboarding(self, name=''):
            """
            list_cisco_cloud_onboarding parameters
            :param uuid: uuid
            
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listCiscoCloudOnboarding(
                    {'name': '%'+name}, returnedTags={'voucherExists': '', 'enablePushNotifications': '', 'enableHttpProxy': '', 'httpProxyAddress': '', 'proxyUsername': '', 'proxyPassword': '', 'enableTrustCACertificate': '', 'allowAnalyticsCollection': '', 'enableTroubleshooting': '', 'alarmSendEncryptedData': '', 'orgId': '', 'alarmPushIntervalSecs': '', 'alarmEncryptKey': '', 'serviceAddress': '', 'onboardingRegistrationStatus': '', 'email': '', 'partnerEmail': '', 'orgName': '', 'customerOneTimePassword': '', 'alarmSeverity': '', 'alarmPushNowToggle': '', 'enableGDSCommunication': '', 'mraActivationDomain': '', 'errorStatus': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['ciscoCloudOnboarding']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_ldap_sync_custom_field(self, name=''):
            """
            list_ldap_sync_custom_field parameters
            :param uuid: uuid
            :param ldapConfigurationName: ldapConfigurationName
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listLdapSyncCustomField(
                    {'name': '%'+name}, returnedTags={'ldapConfigurationName': '', 'customUserField': '', 'ldapUserField': ''}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['ldapSyncCustomField']
                return result

            except Fault as error:
                result['error'] = error
                return result
            
    def list_change(self, name=''):
            """
            list_change parameters
            :param uuid: uuid
            
            """
            result = {
                'success': False,
                'response': '',
                'error': '',
            }
            try:
                resp = self.client.listChange(
                    {'name': '%'+name}, returnedTags={}
                )

                if resp['return']:
                    result['success'] = True
                    result['response'] = resp['return']['change']
                return result

            except Fault as error:
                result['error'] = error
                return result