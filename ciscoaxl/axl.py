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


    ## GET Commands

    def get_user(self, **args):
        """
        Get user parameters
        :param userid: userid
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

    def get_phone(self, **args):
        """
        Get phone parameters
        :param name: name
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

    def get_partition(self, **args):
        """
        Get partition parameters
        :param name: name
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
        Get css parameters
        :param name: name
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

    def get_mrg(self, **args):
        """
        Get mrg parameters
        :param name: name
        :param uuid: uuid 
        :return: result dictionary
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }
        try:
            resp = self.client.getMediaResourceGroup(**args)

            if resp['return']:
                result['success'] = True
                result['response'] = resp['return']['mediaResourceGroup']
            return result

        except Fault as error:
            result['error'] = error
            return result

    def get_mrgl(self, **args):
        """
        Get mrgl parameters
        :param name: name
        :param uuid: uuid 
        :return: result dictionary
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }
        try:
            resp = self.client.getMediaResourceGroupList(**args)

            if resp['return']:
                result['success'] = True
                result['response'] = resp['return']['mediaResourceGroupList']
            return result

        except Fault as error:
            result['error'] = error
            return result

    def get_region(self, **args):
        """
        Get region parameters
        :param name: name
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

    def get_physical_location(self, **args):
        """
        Get physical location parameters
        :param name: name
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

    def get_route_group(self, **args):
        """
        Get route group parameters
        :param name: name
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
        Get device pool parameters
        :param name: name
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
        Get device mobility group parameters
        :param name: name
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
        Get location parameters
        :param name: name
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

    def get_softkey_template(self, **args):
        """
        Get softkey template parameters
        :param name: name
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
        Get transcoder parameters
        :param name: name
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
        Get common device config parameters
        :param name: name
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

    def get_device_mobility(self, **args):
        """
        Get device mobility parameters
        :param name: name
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

    def get_credential_policy(self, **args):
        """
        Get credential policy parameters
        :param name: name
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

    def get_hunt_list(self, **args):
        """
        Get hunt list parameters
        :param name: name
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

    def get_line_group(self, **args):
        """
        Get line group parameters
        :param name: name
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
        Get recording profile parameters
        :param name: name
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
        Get route filter parameters
        :param name: name
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