import unittest
from axl import *
unittest.TestLoader.sortTestMethodsUsing = None
ucm = axl(username='administrator',password='Dev@1998',cucm='ucm1.presidio.cloud',cucm_version=12.5)

class TestCreate(unittest.TestCase):

	def _directory_number(self):
		self.assertIsInstance(ucm.add_directory_number(
			pattern='1234',
			partition='mypartition'
		)['return'], str, "Should return a str")

	def _partition(self):
		self.assertIsInstance(ucm.add_partition(
			name='testpt'
		)['return'], str, "Should return a str")

	def _calling_search_space(self):
		self.assertIsInstance(ucm.add_calling_search_space(
			name='testcss',
			members=['mypartition']
		)['return'], str, "Should return a str")

	def _location(self):
		self.assertIsInstance(ucm.add_location(
            name='testlocation'
        )['return'], str, "Should return a str")

	def _region(self):
		self.assertIsInstance(ucm.add_region(
            name='testregion'
        )['return'], str, "Should return a str")

	def _srst(self):
		self.assertIsInstance(ucm.add_srst(
            name='testsrst', 
            ip_address='1.1.1.1')['return'], str, "Should return a str")

	def _device_pool(self):
		self.assertIsInstance(ucm.add_device_pool(
            name='testdevicepool'
        )['return'], str, "Should return a str")

	def _call_manager_group(self):
		self.assertIsInstance(ucm.add_call_manager_group(
            name='testcallmanagergroup',
            members=[
                {
                    "member":
                    {"callManagerName": "Default",
                    "priority": "1"}
                }
            ]
        ), dict, "Should return a dict")

	def _cti_route_point(self):
		self.assertIsInstance(ucm.add_cti_route_point(
            name='testcti',
            lines=[
                ('1234', '')
            ]
        )['return'], str, "Should return a str")

	def _phone(self):
		self.assertIsInstance(ucm.add_phone(
            name='SEP001122334455',
            product='Cisco 8861',
            device_pool='Default',
            location='Hub_None',
            protocol='SIP',
            lines=[
                ('1102', '', 'Robert Smith', 'Robert Smith', 'Robert Smith - 1102', '+1408202XXXX')
            ])['return']
        , str, "Should return a str")

	def _device_profile(self):
		self.assertIsInstance(ucm.add_device_profile(
            name='testudp',
            product='Cisco 8861',
            protocol="SIP",
            phone_template='Standard 8861 SIP',
            lines=[
                ('1102', '', 'Robert Smith', 'Robert Smith', 'Robert Smith - 1102', '+1408202XXXX')
            ])['return']
        , str, "Should return a str")

	def _route_group(self):
		self.assertIsInstance(ucm.add_route_group(
            name='testrg',
            members=['trunk']
        )['return'], str, "Should return a str")

	def _route_list(self):
		self.assertIsInstance(ucm.add_route_list(
			name='testrl',
			members=['myrg']
		)['return'], str, "Should return a str")

	def _route_pattern(self):
		self.assertIsInstance(ucm.add_route_pattern(
			pattern='5555',
			partition='mypartition',
			route_list='myrl'
		)['return'], str, "Should return a str")

	def _translation(self):
		self.assertIsInstance(ucm.add_translation(
			pattern='6666',
			partition='mypartition',
			calledPartyTransformationMask='7777'
		)['return'], str, "Should return a str")

	def _called_party_xform(self):
		self.assertIsInstance(ucm.add_called_party_xform(
			pattern='5656',
			partition='mypartition'
		)['return'], str, "Should return a str")

	def _calling_party_xform(self):
		self.assertIsInstance(ucm.add_calling_party_xform(
			pattern='6565',
			partition='mypartition'
		)['return'], str, "Should return a str")

	def _user(self):
		self.assertIsInstance(ucm.add_user(
			userid='testuser',
			firstName='test',
			lastName='user'
		)['return'], str, "Should be str")

	def _sip_trunk(self):
		trunk_info = {
		"name": "testtrunk",
		"product": "SIP Trunk",
		"class": "Trunk",
		"protocol": "SIP",
		'locationName': "Hub_None",
		"protocolSide": "Network",
		"description": "my new sip trunk",
		"presenceGroupName": "Standard Presence group",
		"devicePoolName": "Default",
		"securityProfileName": "Non Secure SIP Trunk Profile",
		"sipProfileName": "Standard SIP Profile",
		"runOnEveryNode": "t",
		"destinations": {"destination": {
			"addressIpv4": "5.1.2.3",
			"port": "5060",
			"sortOrder": "1"
		}}
		}
		sipTrunk = {}
		sipTrunk['sipTrunk'] = trunk_info

		self.assertIsInstance(ucm.add_sip_trunk(**sipTrunk)['return'], str, "Should return a str")

	def _h323_gateway(self):
		gateway_info = {
		"name": "001100110011",
		"description": "",
		"product": "H.323 Gateway",
		"class": "Gateway",
		"protocol": "H.225",
		"protocolSide": "Network",
		"callingSearchSpaceName": "",
		"automatedAlternateRoutingCssName": "",
		"devicePoolName": "Default",
		"locationName": "Hub_None",
		"mediaResourceListName": "",
		"aarNeighborhoodName": "",
		"pstnAccess": "true",
		"sigDigits": "99",
		"prefixDn": "",
		"redirectInboundNumberIe": "false",
		"redirectOutboundNumberIe": "false",
		"calledPartyIeNumberType": "Unknown",
		"callingPartyIeNumberType": "Unknown",
		"callingPartyNationalPrefix": "",
		"callingPartyInternationalPrefix": "",
		"callingPartyUnknownPrefix": "",
		"callingPartySubscriberPrefix": "",
		"callingPartyNationalStripDigits": "",
		"callingPartyInternationalStripDigits": "",
		"callingPartyUnknownStripDigits": "",
		"callingPartySubscriberStripDigits": "",
		"callingPartyNationalTransformationCssName": "",
		"callingPartyInternationalTransformationCssName": "",
		"callingPartyUnknownTransformationCssName": "",
		"callingPartySubscriberTransformationCssName": "",
		}
		h323Gateway = {}
		h323Gateway['h323Gateway'] = gateway_info
		self.assertIsInstance(ucm.add_h323_gateway(**h323Gateway)['return'], str, "Should return a str")

	def _transcoder(self):
		self.assertIsInstance(ucm.add_transcoder(
			name='testxcode'
		)['return'], str, "Should return a str")

	def _conference_bridge(self):
		self.assertIsInstance(ucm.add_conference_bridge(
			name='testconf'
		)['return'], str, "Should return a str")

	def _mtp(self):
		self.assertIsInstance(ucm.add_mtp(
			name='testmtp'
		)['return'], str, "Should return a str")

	def _media_resource_group(self):
		self.assertIsInstance(ucm.add_media_resource_group(
			name='testmrg',
			members=['mymtp']
		)['return'], str, "Should return a str")

	def _media_resource_group_list(self):
		self.assertIsInstance(ucm.add_media_resource_group_list(
			name='testmrgl',
			members=['mymrg']
		)['return'], str, "Should return a str")

class TestRead(unittest.TestCase):

	def _directory_number(self):
		self.assertIsInstance(ucm.get_directory_number(
			pattern='1234',
			routePartitionName='mypartition'
		)['return']['line']['uuid'], str, "Should return a str")

	def _partition(self):
		self.assertIsInstance(ucm.get_partition(
			name='testpt'
		)['return']['routePartition']['name'], str, "Should return a str")

	def _calling_search_space(self):
		self.assertIsInstance(ucm.get_calling_search_space(
			name='testcss'
		)['return']['css']['uuid'], str, "Should return a str")

	def _location(self):
		self.assertIsInstance(ucm.get_location(
            name='testlocation'
        )['return']['location']['uuid'], str, "Should return a str")

	def _region(self):
		self.assertIsInstance(ucm.get_region(
            name='testregion'
        )['return']['region']['name'], str, "Should return a dict")

	def _srst(self):
		self.assertIsInstance(ucm.get_srst(
            name='testsrst')['return']['srst']['name'], str, "Should return a str")

	def _device_pool(self):
		self.assertIsInstance(ucm.get_device_pool(
            name='testdevicepool'
        )['return']['devicePool']['name'], str, "Should return a str")

	def _call_manager_group(self):
		self.assertIsInstance(ucm.get_call_manager_group(
            name='testcallmanagergroup',
        )['return'], dict, "Should return a dict")

	def _cti_route_point(self):
		self.assertIsInstance(ucm.get_cti_route_point(
            name='testcti'
        )['return']['ctiRoutePoint']['name'], str, "Should return a str")

	def _phone(self):
		self.assertIsInstance(ucm.get_phone(
            name='SEP001122334455'
        )['name'], str, "Should return a str")

	def _device_profile(self):
		self.assertIsInstance(ucm.get_device_profile(
            name='testudp')['return']['deviceProfile']['name']
        , str, "Should return a str")

	def _route_group(self):
		self.assertIsInstance(ucm.get_route_group(
            name='testrg',
        )['return']['routeGroup']['uuid'], str, "Should return a str")

	def _route_list(self):
		self.assertIsInstance(ucm.get_route_list(
			name='testrl',
		)['return']['routeList']['uuid'], str, "Should return a str")

	def _route_pattern(self):
		self.assertIsInstance(ucm.get_route_pattern(
			pattern='5555',
		)['return']['routePattern']['uuid'], str, "Should return a str")

	def _translation(self):
		self.assertIsInstance(ucm.get_translation(
			pattern='6666',
			partition='mypartition'
		)['return']['transPattern']['uuid'], str, "Should return a str")

	def _called_party_xform(self):
		self.assertIsInstance(ucm.get_called_party_xform(
			pattern='5656',
			routePartitionName='mypartition',
		)['return']['calledPartyTransformationPattern']['uuid'], str, "Should return a str")

	def _calling_party_xform(self):
		self.assertIsInstance(ucm.get_calling_party_xform(
			pattern='6565',
			routePartitionName='mypartition',
		)['return']['callingPartyTransformationPattern']['uuid'], str, "Should return a str")

	def _user(self):
		self.assertIsInstance(ucm.get_user(
			userid='testuser',
		)['userid'], str, "Should be str")

	def _sip_trunk(self):
		self.assertIsInstance(ucm.get_sip_trunk(
			name='testtrunk',
		)['return']['sipTrunk']['uuid'], str, "Should be str")

	def _h323_gateway(self):
		self.assertIsInstance(ucm.get_h323_gateway(
			name='001100110011'
		)['return']['h323Gateway']['uuid'], str, "Should return a str")

	def _transcoder(self):
		self.assertIsInstance(ucm.get_transcoder(
			name='testxcode'
		)['return']["transcoder"]['uuid'], str, "Should return a str")

	def _conference_bridge(self):
		self.assertIsInstance(ucm.get_conference_bridge(
			name='testconf'
		)['return']["conferenceBridge"]['uuid'], str, "Should return a str")

	def _mtp(self):
		self.assertIsInstance(ucm.get_mtp(
			name='testmtp'
		)['return']["mtp"]['uuid'], str, "Should return a str")

	def _media_resource_group(self):
		self.assertIsInstance(ucm.get_media_resource_group(
			name='testmrg',
		)['return']['mediaResourceGroup']['uuid'], str, "Should return a str")

	def _media_resource_group_list(self):
		self.assertIsInstance(ucm.get_media_resource_group_list(
			name='testmrgl'
		)['return']['mediaResourceList']['uuid'], str, "Should return a str")

class TestList(unittest.TestCase):

	def _directory_number(self):
		self.assertIsInstance(ucm.get_directory_numbers(), list, "Should return a list")

	def _partition(self):
		self.assertIsInstance(ucm.get_partitions(), list, "Should return a list")

	def _calling_search_space(self):
		self.assertIsInstance(ucm.get_calling_search_spaces(
		), list, "Should return a list")

	def _location(self):
		self.assertIsInstance(ucm.get_locations(), list, "Should return a list")

	def _region(self):
		self.assertIsInstance(ucm.get_regions(), list, "Should return a list")

	def _srst(self):
		self.assertIsInstance(ucm.get_srsts(), list, "Should return a list")

	def _device_pool(self):
		self.assertIsInstance(ucm.get_device_pools(), list, "Should return a list")

	def _call_manager_group(self):
		self.assertIsInstance(ucm.get_call_manager_groups(), list, "Should return a list")

	def _cti_route_point(self):
		self.assertIsInstance(ucm.get_cti_route_points(), list, "Should return a dict")

	def _phone(self):
		self.assertIsInstance(ucm.get_phones(), list, "Should return a list")

	def _device_profile(self):
		self.assertIsInstance(ucm.get_device_profiles(), list, "Should return a list")

	def _route_group(self):
		self.assertIsInstance(ucm.get_route_groups(), list, "Should return a list")

	def _route_list(self):
		self.assertIsInstance(ucm.get_route_lists(), list, "Should return a list")

	def _route_pattern(self):
		self.assertIsInstance(ucm.get_route_patterns(), list, "Should return a list")

	def _translation(self):
		self.assertIsInstance(ucm.get_translations(), list, "Should return a list")

	def _called_party_xform(self):
		self.assertIsInstance(ucm.get_called_party_xforms(), list, "Should return a list")

	def _calling_party_xform(self):
		self.assertIsInstance(ucm.get_calling_party_xforms(), list, "Should return a list")

	def _route_plan(self):
		self.assertIsInstance(ucm.list_route_plan(), list, "Should return a list")

	def _process_nodes(self):
		self.assertIsInstance(ucm.list_process_nodes(), list, "Should return a list")

	def _user(self):
		self.assertIsInstance(ucm.get_users(), list, "Should be a list")

	def _sip_trunk(self):
		self.assertIsInstance(ucm.get_sip_trunks(
		), list, "Should be list")

	def _h323_gateway(self):
		self.assertIsInstance(ucm.get_h323_gateways(), list, "Should return a list")

	def _transcoder(self):
		self.assertIsInstance(ucm.get_transcoders(), list, "Should return a list")

	def _conference_bridge(self):
		self.assertIsInstance(ucm.get_conference_bridges(), list, "Should return a list")

	def _mtp(self):
		self.assertIsInstance(ucm.get_mtps(), list, "Should return a list")

	def _media_resource_group(self):
		self.assertIsInstance(ucm.get_media_resource_groups(), list, "Should return a list")

	def _media_resource_group_list(self):
		self.assertIsInstance(ucm.get_media_resource_group_lists(), list, "Should return a list")

class TestUpdate(unittest.TestCase):

	def _directory_number(self):
		self.assertIsInstance(ucm.update_directory_number(
			pattern='1234',
			routePartitionName='mypartition',
			newPattern='5678'
		)['return'], str, "Should return a str")

	def _partition(self):
		self.assertIsInstance(ucm.update_partition(
			name='testpt',
			newName='newpt'
		)['return'], str, "Should return a str")

	def _calling_search_space(self):
		self.assertIsInstance(ucm.update_calling_search_space(
			name='testcss',
			newName='newcss'
		)['return'], str, "Should return a str")

	def _location(self):
		self.assertIsInstance(ucm.update_location(
            name='testlocation',
            newName='newlocation'
        )['return'], str, "Should return a str")

	def _region(self):
		self.assertIsInstance(ucm.update_region(
            name='testregion',
            newName='newregion'
        ), str, "Should return a str")

	def _srst(self):
		self.assertIsInstance(ucm.update_srst(
            name='testsrst',
            newName='newsrst'
        )['return'], str, "Should return a str")

	def _device_pool(self):
		self.assertIsInstance(ucm.update_device_pool(
            name='testdevicepool',
            newName='newdevicepool'
        )['return'], str, "Should return a str")

	def _call_manager_group(self):
		self.assertIsInstance(ucm.update_call_manager_group(
            name='testcallmanagergroup',
            newName='newcallmanagergroup'
        )['return'], str, "Should return a str")

	def _cti_route_point(self):
		self.assertIsInstance(ucm.update_cti_route_point(
            name='testcti',
            newName='newcti'
        )['return'], str, "Should return a str")

	def _phone(self):
		self.assertIsInstance(ucm.update_phone(
            name='SEP001122334455',
            newName='SEP554433221100'
        )['return'], str, "Should return a str")

	def _device_profile(self):
		self.assertIsInstance(ucm.update_device_profile(
            name='testudp',
            description='teatudp'
        )['return'], str, "Should return a str")

	def _route_group(self):
		self.assertIsInstance(ucm.update_route_group(
            name='testrg',
			newName='newrg'
        )['return'], str, "Should return a str")

	def _route_list(self):
		self.assertIsInstance(ucm.update_route_list(
			name='testrl',
			newName='newrl'
		)['return'], str, "Should return a str")

	def _route_pattern(self):
		self.assertIsInstance(ucm.update_route_pattern(
			pattern='5555',
			routePartitionName='mypartition',
			newPattern='6666'
		)['return'], str, "Should return a str")

	def _translation(self):
		self.assertIsInstance(ucm.update_translation(
			pattern='6666',
			partition='mypartition',
			newPattern='6667'
		)['return'], str, "Should return a str")

	def _called_party_xform(self):
		self.assertIsInstance(ucm.update_called_party_xform(
			pattern='5656',
			routePartitionName='mypartition',
			newPattern='4646'
		)['return'], str, "Should return a str")

	def _calling_party_xform(self):
		self.assertIsInstance(ucm.update_calling_party_xform(
			pattern='6565',
			routePartitionName='mypartition',
			newPattern='6464'
		)['return'], str, "Should return a str")

	def _user(self):
		self.assertIsInstance(ucm.update_user(
			userid='testuser',
			lastName='newuser'
		)['return'], str, "Should be str")

	def _sip_trunk(self):
		self.assertIsInstance(ucm.update_sip_trunk(
			name='testtrunk',
			newName='newtrunk'
		)['return'], str, "Should be str")

	def _h323_gateway(self):
		self.assertIsInstance(ucm.update_h323_gateway(
			name='001100110011',
			newName='020202030303'
		)['return'], str, "Should return a str")

	def _transcoder(self):
		self.assertIsInstance(ucm.update_transcoder(
			name='testxcode',
			newName='newxcode'
		)['return'], str, "Should return a str")

	def _conference_bridge(self):
		self.assertIsInstance(ucm.update_conference_bridge(
			name='testconf',
			newName='newconf'
		)['return'], str, "Should return a str")

	def _mtp(self):
		self.assertIsInstance(ucm.update_mtp(
			name='testmtp',
			newName='newmtp'
		)['return'], str, "Should return a str")

	def _media_resource_group(self):
		self.assertIsInstance(ucm.update_media_resource_group(
			name='testmrg',
			newName='newmrg'
		)['return'], str, "Should return a str")

	def _media_resource_group_list(self):
		self.assertIsInstance(ucm.update_media_resource_group_list(
			name='testmrgl',
			newName='newmrgl'
		)['return'], str, "Should return a str")

class TestDelete(unittest.TestCase):

	def _directory_number(self):
		self.assertIsInstance(ucm.delete_directory_number(
			pattern='5678',
			routePartitionName='mypartition'
		)['return'], str, "Should return a str")

	def _partition(self):
		self.assertIsInstance(ucm.delete_partition(
			name='newpt'
		)['return'], str, "Should return a str")

	def _calling_search_space(self):
		self.assertIsInstance(ucm.delete_calling_search_space(
			name='newcss',
		)['return'], str, "Should return a str")

	def _location(self):
		self.assertIsInstance(ucm.delete_location(
            name='newlocation'
        )['return'], str, "Should return a str")

	def _region(self):
		self.assertIsInstance(ucm.delete_region(
            name='testregion'
        )['return'], str, "Should return a str")

	def _srst(self):
		self.assertIsInstance(ucm.delete_srst(
            name='newsrst')['return'], str, "Should return a str")

	def _device_pool(self):
		self.assertIsInstance(ucm.delete_device_pool(
            name='newdevicepool'
        )['return'], str, "Should return a str")

	def _call_manager_group(self):
		self.assertIsInstance(ucm.delete_call_manager_group(
            name='newcallmanagergroup',
        )['return'], str, "Should return a str")

	def _cti_route_point(self):
		self.assertIsInstance(ucm.delete_cti_route_point(
            name='newcti'
        )['return'], str, "Should return a str")

	def _phone(self):
		self.assertIsInstance(ucm.delete_phone(
            name='SEP554433221100'
        )['return'], str, "Should return a str")

	def _device_profile(self):
		self.assertIsInstance(ucm.delete_device_profile(
            name='testudp'
        )['return'], str, "Should return a str")

	def _route_group(self):
		self.assertIsInstance(ucm.delete_route_group(
            name='newrg',
        )['return'], str, "Should return a str")

	def _route_list(self):
		self.assertIsInstance(ucm.delete_route_list(
			name='newrl'
		)['return'], str, "Should return a str")

	def _route_pattern(self):
		self.assertIsInstance(ucm.delete_route_pattern(
			pattern='6666',
			routePartitionName='mypartition'
		)['return'], str, "Should return a str")

	def _translation(self):
		self.assertIsInstance(ucm.delete_translation(
			pattern='6667',
			partition='mypartition'
		)['return'], str, "Should return a str")

	def _called_party_xform(self):
		self.assertIsInstance(ucm.delete_called_party_xform(
			pattern='4646',
			routePartitionName='mypartition'
		)['return'], str, "Should return a str")

	def _calling_party_xform(self):
		self.assertIsInstance(ucm.delete_calling_party_xform(
			pattern='6464',
			routePartitionName='mypartition'
		)['return'], str, "Should return a str")

	def _user(self):
		self.assertIsInstance(ucm.delete_user(
			userid='testuser',
		)['return'], str, "Should be str")

	def _sip_trunk(self):
		self.assertIsInstance(ucm.delete_sip_trunk(
			name='newtrunk',
		)['return'], str, "Should be str")

	def _h323_gateway(self):
		self.assertIsInstance(ucm.delete_h323_gateway(
			name='020202030303'
		)['return'], str, "Should return a str")

	def _transcoder(self):
		self.assertIsInstance(ucm.delete_transcoder(
			name='newxcode'
		)['return'], str, "Should return a str")

	def _conference_bridge(self):
		self.assertIsInstance(ucm.delete_conference_bridge(
			name='newconf'
		)['return'], str, "Should return a str")

	def _mtp(self):
		self.assertIsInstance(ucm.delete_mtp(
			name='newmtp'
		)['return'], str, "Should return a str")

	def _media_resource_group(self):
		self.assertIsInstance(ucm.delete_media_resource_group(
			name='newmrg',
		)['return'], str, "Should return a str")

	def _media_resource_group_list(self):
		self.assertIsInstance(ucm.delete_media_resource_group_list(
			name='newmrgl',
		)['return'], str, "Should return a str")

class TestSql(unittest.TestCase):

	def _query(self):
		self.assertIsInstance(ucm.sql_query(
			'select first 2 * from enduser'
		)['row'], list, "Should return a list")

	def _update(self):
		self.assertIsInstance(ucm.sql_update(
			f'''insert into routepartition (name,description) values ('test-sql-pt', 'inserted from unittest')'''
		)['rowsUpdated'], int, "Should return a int")
	
	def _delete(self):
		self.assertIsInstance(ucm.sql_update(
			f'''delete from routepartition where description like 'inserted from unittest' '''
		)['rowsUpdated'], int, "Should return a int")

class TestDo(unittest.TestCase):

	def _ldap_sync(self):
		ldap_uuid = ucm.get_ldap_dir()[0]['uuid']
		self.assertIsInstance(ucm.do_ldap_sync(
			uuid=ldap_uuid
		)['return'], str, "Should return a str")

	def _change_dnd_status(self):
		self.assertIsInstance(ucm.do_change_dnd_status(
			userID='myuser',
			dndStatus='true'
		)['return'], str, "Should return a str")

	def _device_login(self):
		self.assertIsInstance(ucm.do_device_login(
			deviceName='SEP101122334455',
			userId='myuser',
			profileName='myudp',
			loginDuration=90
		)['return'], str, "Should return a str")

	def _device_logout(self):
		self.assertIsInstance(ucm.do_device_logout(
			deviceName='SEP101122334455'
		)['return'], str, "Should return a str")

	def _device_reset(self):
		self.assertIsInstance(ucm.do_device_reset(
			name='SEP101122334455'
		)['return'], str, "Should return a str")

	def _sip_trunk_reset(self):
		self.assertIsInstance(ucm.reset_sip_trunk(
			name='trunk'
		)['return'], str, "Should return a str")	

partition = 'mypartition'
css = 'mycss'
dn = '1001'
location = 'mylocation'
region = 'myregion'
name = 'SEP001100220033'
trunk = 'trunk'

def prep():
    '''
    used for pre-requisites of other tests
    make sure names don't overlap with individual tests
    '''

    trunk_info = {
        "name": trunk,
        "product": "SIP Trunk",
        "class": "Trunk",
        "protocol": "SIP",
        'locationName': "Hub_None",
        "protocolSide": "Network",
        "description": "my new sip trunk",
        "presenceGroupName": "Standard Presence group",
        "devicePoolName": "Default",
        "securityProfileName": "Non Secure SIP Trunk Profile",
        "sipProfileName": "Standard SIP Profile",
        "runOnEveryNode": "t",
        "destinations": {"destination": {
            "addressIpv4": "4.1.2.3",
            "port": "5060",
            "sortOrder": "1"
        }}
    }
    sipTrunk = {}
    sipTrunk['sipTrunk'] = trunk_info

    ucm.add_partition(
        name=partition
        )
    ucm.add_calling_search_space(
        name=css,
        members=[partition]
        )
    ucm.add_location(
        name=location
        )
    ucm.add_region(
        name=region
    )
    ucm.add_directory_number(
        pattern=dn,
        partition=partition
    )

    ucm.add_sip_trunk(**sipTrunk)

    ucm.add_route_group(
        name='myrg',
        members=[trunk]
    )

    ucm.add_route_list(
        name='myrl',
        members=['myrg']
    )

    ucm.add_device_profile(
        name='myudp',
        product='Cisco 8861',
        protocol="SIP",
        phone_template='Standard 8861 SIP',
        lines=[
            ('1101', '', 'Robert Smith', 'Robert Smith', 'Robert Smith - 1102', '+1408202XXXX')
        ])

    pro = []
    profile = {}
    profile['profileName'] = 'myudp'
    pro.append(profile)
    ucm.add_user(
        userid='myuser',
        firstName='my',
        lastName='user',
        phoneProfiles=pro
    )

    ucm.add_phone(
        name='SEP101122334455',
        product='Cisco 8861',
        device_pool='Default',
        location='Hub_None',
        protocol='SIP',
        lines=[
        ('1101', '', 'Robert Smith', 'Robert Smith', 'Robert Smith - 1102', '+1408202XXXX')
    ])

    ucm.add_mtp(
        name='mymtp'
    )

    ucm.add_media_resource_group(
        name='mymrg',
        members=['mymtp']
    )

def cleanup():
    ucm.delete_partition(
        name=partition
        )
    ucm.delete_calling_search_space(
        name=css
        )
    ucm.delete_location(
        name=location
        )
    ucm.delete_region(
        name=region
    )
    dn_uuid = ucm.get_directory_number(
        pattern=dn,
        routePartitionName=partition
    )
    ucm.delete_directory_number(
        uuid=dn_uuid
    )
    ucm.delete_sip_trunk(
        name=trunk
    )

    ucm.delete_route_group(
    name='myrg'
    )
    ucm.delete_route_list(
        name='myrl'
    )
    ucm.delete_user(
        userid='myuser'
    )

    ucm.delete_device_profile(
        name='myudp'
	)

    ucm.delete_phone(
        name='SEP101122334455'
	)

    ucm.delete_mtp(
        name='mymtp'
    )

    ucm.delete_media_resource_group(
        name='mymrg'
    )

skipped = [
    'call_manager_group', 
    'region']

crud_endpoints = [
    'location', 
    'srst',
    'region',
    'device_pool', 
    'cti_route_point',
    'call_manager_group',
    'phone',
    'device_profile',
	'route_group',
	'partition',
	'calling_search_space',
	'directory_number',
	'route_list',
	'route_pattern',
	'translation',
	'called_party_xform',
	'calling_party_xform',
	'user',
	'sip_trunk',
	'h323_gateway',
	'transcoder',
	'conference_bridge',
	'mtp',
	'media_resource_group',
	'media_resource_group_list'
	]

list_endpoints = [
	'process_nodes',
	'route_plan'
]

sql_endpoints = [
	'query',
	'update',
	'delete'
]

do_endpoints = [
	'ldap_sync',
	'change_dnd_status',
	'device_login',
	'device_logout',
	'device_reset',
	'sip_trunk_reset'
]

def suite():
    suite = unittest.TestSuite()
    for endpoint in crud_endpoints:
        if endpoint not in skipped:
            suite.addTest(TestCreate(f'''_{endpoint}'''))
            suite.addTest(TestRead(f'''_{endpoint}'''))
            suite.addTest(TestList(f'''_{endpoint}'''))
            suite.addTest(TestUpdate(f'''_{endpoint}'''))
            suite.addTest(TestDelete(f'''_{endpoint}'''))
    for endpoint in list_endpoints:
        if endpoint not in skipped:
            suite.addTest(TestList(f'''_{endpoint}'''))
    for endpoint in sql_endpoints:
        if endpoint not in skipped:
            suite.addTest(TestSql(f'''_{endpoint}'''))
    for endpoint in do_endpoints:
        if endpoint not in skipped:
            suite.addTest(TestDo(f'''_{endpoint}'''))
    return suite

if __name__ == '__main__':
    prep()
    runner = unittest.TextTestRunner()
    runner.run(suite())
    cleanup()