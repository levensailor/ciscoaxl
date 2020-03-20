import unittest

'''
execute_sql_query
update_sql_query
do_ldap_sync
do_change_dnd_status
do_device_login
do_device_logout
do_device_reset
reset_sip_trunk
update_dhcp_subnet
list_process_nodes
'''

class TestDosAndSQL(unittest.TestCase):



    def test_sum(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

if __name__ == '__main__':
    unittest.main()