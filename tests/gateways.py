import unittest

'''
add_h323_gateway
get_h323_gateway
get_h323_gateways
update_h323_gateway
delete_h323_gateway
add_sip_trunk
get_sip_trunk
get_sip_trunks
update_sip_trunk
delete_sip_trunk?
'''

class TestGateways(unittest.TestCase):



    def test_sum(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

if __name__ == '__main__':
    unittest.main()