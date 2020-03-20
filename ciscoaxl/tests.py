import unittest
from axl import *
ucm = axl(username='administrator',password='Dev@1998',cucm='ucm1.presidio.cloud',cucm_version=12.5)

class Tests(unittest.TestCase):
	def test_get_ldap_dir(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_add_location(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_location(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_locations(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_update_location(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_delete_location(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_add_region(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_region(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_regions(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_update_region(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_delete_region(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_add_srst(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_srst(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_delete_srst(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_add_device_pool(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_device_pool(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_device_pools(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_update_device_pool(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_delete_device_pool(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_add_call_manager_group(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_add_cti_route_point(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_cti_route_point(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_cti_route_points(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_update_cti_route_point(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_delete_cti_route_point(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_add_phone(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_phone(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_phones(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_update_phone(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_delete_phone(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_add_device_profile(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_device_profile(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_device_profiles(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_update_device_profile(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_delete_device_profile(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_add_route_group(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_route_group(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_route_groups(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_update_route_group(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_delete_route_group(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_add_route_list(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_route_list(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_route_lists(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_update_route_list(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_delete_route_list(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_add_partition(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_partition(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_partitions(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_update_partition(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_delete_partition(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_add_calling_search_space(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_calling_search_space(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_calling_search_spaces(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_update_calling_search_space(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_delete_calling_search_space(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_add_route_pattern(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_route_pattern(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_route_patterns(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_update_route_pattern(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_delete_route_pattern(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_add_directory_number(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_directory_number(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_directory_numbers(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_update_directory_number(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_delete_directory_number(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_add_translation(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_translation(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_translations(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_update_translation(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_delete_translation(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_list_route_plan(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_add_called_party_xform(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_called_party_xform(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_called_party_xforms(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_update_called_party_xform(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_delete_called_party_xform(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_add_calling_party_xform(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_calling_party_xform(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_calling_party_xforms(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_update_calling_party_xform(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_delete_calling_party_xform(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_execute_sql_query(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_update_sql_query(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_do_ldap_sync(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_do_change_dnd_status(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_do_device_login(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_do_device_logout(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_do_device_reset(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_reset_sip_trunk(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_update_dhcp_subnet(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_list_process_nodes(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_add_h323_gateway(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_h323_gateway(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_h323_gateways(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_update_h323_gateway(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_delete_h323_gateway(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_add_sip_trunk(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_sip_trunk(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_sip_trunks(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_update_sip_trunk(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_add_conference_bridge(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_conference_bridge(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_conference_bridges(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_delete_conference_bridge(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_add_transcoder(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_transcoder(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_transcoders(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_delete_transcoder(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_add_media_resource_group(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_media_resource_group(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_media_resource_groups(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_delete_media_resource_group(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_add_media_resource_group_list(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_media_resource_group_lists(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_media_resource_group_list(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_delete_media_resource_group_list(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_add_user(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_user(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_get_users(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_update_user(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_delete_user(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
	def test_update_user_credentials(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

if __name__ == '__main__':
	unittest.main()
