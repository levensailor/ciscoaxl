"""
get singular = returns dict
get plural = returns list of dicts
update = returns dict with return item
add = returns dict with return item
delete = returns dict with return item
do = returns dict with return item
sqlquery = returns dict with row list of lists
sqlupdate = returns dict with return item with rowsUpdated item
reset = returns dict with return item
list = returns list of dicts

"""

base = [
    "get_ldap_dir",
    "add_location",
    "get_location",
    "get_locations",
    "update_location",
    "delete_location",
    "add_region",
    "get_region",
    "get_regions",
    "update_region",
    "delete_region",
    "add_srst",
    "get_srst",
    "delete_srst",
    "add_device_pool",
    "get_device_pool",
    "get_device_pools",
    "update_device_pool",
    "delete_device_pool",
    "add_call_manager_group",
]


devices = [
    "add_cti_route_point",
    "get_cti_route_point",
    "get_cti_route_points",
    "update_cti_route_point",
    "delete_cti_route_point",
    "add_phone",
    "get_phone",
    "get_phones",
    "update_phone",
    "delete_phone",
    "add_device_profile",
    "get_device_profile",
    "get_device_profiles",
    "update_device_profile",
    "delete_device_profile",
]

dialplan = [
    "add_route_group",
    "get_route_group",
    "get_route_groups",
    "update_route_group",
    "delete_route_group",
    "add_route_list",
    "get_route_list",
    "get_route_lists",
    "update_route_list",
    "delete_route_list",
    "add_partition",
    "get_partition",
    "get_partitions",
    "update_partition",
    "delete_partition",
    "add_calling_search_space",
    "get_calling_search_space",
    "get_calling_search_spaces",
    "update_calling_search_space",
    "delete_calling_search_space",
    "add_route_pattern",
    "get_route_pattern",
    "get_route_patterns",
    "update_route_pattern",
    "delete_route_pattern",
    "add_directory_number",
    "get_directory_number",
    "get_directory_numbers",
    "update_directory_number",
    "delete_directory_number",
    "add_translation",
    "get_translation",
    "get_translations",
    "update_translation",
    "delete_translation",
    "list_route_plan",
    "add_called_party_xform",
    "get_called_party_xform",
    "get_called_party_xforms",
    "update_called_party_xform",
    "delete_called_party_xform",
    "add_calling_party_xform",
    "get_calling_party_xform",
    "get_calling_party_xforms",
    "update_calling_party_xform",
    "delete_calling_party_xform",
]

dos_and_sql = [
    "sql_query",
    "sql_update",
    "do_ldap_sync",
    "do_change_dnd_status",
    "do_device_login",
    "do_device_logout",
    "do_device_reset",
    "reset_sip_trunk",
    "update_dhcp_subnet",
    "list_process_nodes",
]

users = [
    "add_user",
    "get_user",
    "get_users",
    "update_user",
    "delete_user",
    "update_user_credentials",
]

media = [
    "add_conference_bridge",
    "get_conference_bridge",
    "get_conference_bridges",
    "delete_conference_bridge",
    "add_transcoder",
    "get_transcoder",
    "get_transcoders",
    "delete_transcoder",
    "add_media_resource_group",
    "get_media_resource_group",
    "get_media_resource_groups",
    "delete_media_resource_group",
    "add_media_resource_group_list",
    "get_media_resource_group_lists",
    "get_media_resource_group_list",
    "delete_media_resource_group_list",
]

gateways = [
    "add_h323_gateway",
    "get_h323_gateway",
    "get_h323_gateways",
    "update_h323_gateway",
    "delete_h323_gateway",
    "add_sip_trunk",
    "get_sip_trunk",
    "get_sip_trunks",
    "update_sip_trunk",
]


def find_assert(function):
    if function.startswith("add"):
        return (
            f"""self.assertIsInstance(ucm.{function}(), dict, "Should return a dict")"""
        )
    elif function.startswith("delete"):
        return (
            f"""self.assertIsInstance(ucm.{function}(), dict, "Should return a dict")"""
        )
    elif function.startswith("update"):
        return (
            f"""self.assertIsInstance(ucm.{function}(), dict, "Should return a dict")"""
        )
    elif function.startswith("get_ldap"):
        return (
            f"""self.assertIsInstance(ucm.{function}(), list, "Should return a list")"""
        )
    elif function.startswith("get") and not function.endswith("s"):
        return (
            f"""self.assertIsInstance(ucm.{function}(), dict, "Should return a dict")"""
        )
    elif function.startswith("get") and function.endswith("s"):
        return (
            f"""self.assertIsInstance(ucm.{function}(), list, "Should return a list")"""
        )
    elif function.startswith("do"):
        return (
            f"""self.assertIsInstance(ucm.{function}(), dict, "Should return a dict")"""
        )
    elif function.startswith("sql_query"):
        return (
            f"""self.assertIsInstance(ucm.{function}(), dict, "Should return a dict")"""
        )
    elif function.startswith("sql_update"):
        return (
            f"""self.assertIsInstance(ucm.{function}(), dict, "Should return a dict")"""
        )
    elif function.startswith("reset"):
        return (
            f"""self.assertIsInstance(ucm.{function}(), dict, "Should return a dict")"""
        )
    elif function.startswith("list"):
        return (
            f"""self.assertIsInstance(ucm.{function}(), list, "Should return a list")"""
        )


def generate_tests():
    t = open("tests.py", "w")
    t.write("")
    t.close()
    t = open("tests.py", "a+")
    t.flush()
    t.write(f"""import unittest\n""")
    t.write(f"""from axl import *\n""")
    t.write(
        f"""ucm = axl(username='administrator',password='Dev@1998',cucm='ucm1.presidio.cloud',cucm_version=12.5)\n"""
    )
    t.write("\n")
    t.write(f"""class Tests(unittest.TestCase):\n""")
    for test in base:
        t.write(f"""\tdef test_{test}(self):\n""")
        t.write(f"""\t\t{find_assert(test)}\n\n""")
    for test in devices:
        t.write(f"""\tdef test_{test}(self):\n""")
        t.write(f"""\t\t{find_assert(test)}\n\n""")
    for test in dialplan:
        t.write(f"""\tdef test_{test}(self):\n""")
        t.write(f"""\t\t{find_assert(test)}\n\n""")
    for test in dos_and_sql:
        t.write(f"""\tdef test_{test}(self):\n""")
        t.write(f"""\t\t{find_assert(test)}\n\n""")
    for test in gateways:
        t.write(f"""\tdef test_{test}(self):\n""")
        t.write(f"""\t\t{find_assert(test)}\n\n""")
    for test in media:
        t.write(f"""\tdef test_{test}(self):\n""")
        t.write(f"""\t\t{find_assert(test)}\n\n""")
    for test in users:
        t.write(f"""\tdef test_{test}(self):\n""")
        t.write(f"""\t\t{find_assert(test)}\n\n""")
    t.write("\n")
    t.write("if __name__ == '__main__':\n")
    t.write("\tunittest.main()\n")


def main():
    generate_tests()


if __name__ == "__main__":
    main()
