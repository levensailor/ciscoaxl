import unittest

'''
add_user
get_user
get_users
update_user
delete_user
update_user_credentials


'''

class TestUsers(unittest.TestCase):



    def test_sum(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

if __name__ == '__main__':
    unittest.main()