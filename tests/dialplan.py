import unittest

'''
add_route_group
get_route_group
get_route_groups
update_route_group
delete_route_group
add_route_list
get_route_list
get_route_lists
update_route_list
delete_route_list
add_partition
get_partition
get_partitions
update_partition
delete_partition
add_calling_search_space
get_calling_search_space
get_calling_search_spaces
update_calling_search_space
delete_calling_search_space
add_route_pattern
get_route_pattern
get_route_patterns
update_route_pattern
delete_route_pattern
add_directory_number
get_directory_number
get_directory_numbers
update_directory_number
delete_directory_number
add_translation
get_translation
get_translations
update_translation
delete_translation
list_route_plan
add_called_party_xform
get_called_party_xform
get_called_party_xforms
update_called_party_xform
delete_called_party_xform
add_calling_party_xform
get_calling_party_xform
get_calling_party_xforms
update_calling_party_xform
delete_calling_party_xform
'''

class TestDialPlan(unittest.TestCase):



    def test_sum(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

if __name__ == '__main__':
    unittest.main()