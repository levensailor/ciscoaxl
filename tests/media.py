import unittest

'''
add_conference_bridge
get_conference_bridge
get_conference_bridges
delete_conference_bridge
add_transcoder
get_transcoder
get_transcoders
delete_transcoder
add_media_resource_group
get_media_resource_group
get_media_resource_groups
delete_media_resource_group
add_media_resource_group_list
get_media_resource_group_lists
get_media_resource_group_list
delete_media_resource_group_list
'''

class TestMedia(unittest.TestCase):



    def test_sum(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

if __name__ == '__main__':
    unittest.main()