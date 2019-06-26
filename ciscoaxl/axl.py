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