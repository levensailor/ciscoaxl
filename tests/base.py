import unittest
'''
get_ldap_dir
add_location
get_location
get_locations
update_location
delete_location
add_region
get_region
get_regions
update_region
delete_region
add_srst
get_srst
delete_srst
add_device_pool
get_device_pool
get_device_pools
update_device_pool
delete_device_pool
add_call_manager_group
'''

class TestBase(unittest.TestCase):



    def test_sum(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

if __name__ == '__main__':
    unittest.main()