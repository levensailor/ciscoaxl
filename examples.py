import os
from ciscoaxl import axl
from py_dotenv import read_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
read_dotenv(dotenv_path)

cucm = os.getenv('cucm')
username = os.getenv('username')
password = os.getenv('password')
version = os.getenv('version')


ucm = axl(username=username,password=password,cucm=cucm,cucm_version=version)

"""
Users
"""
# print(ucm.get_ldap_dirs())
'''Get All Users'''
# for user in ucm.get_users():
#     try:
#         print(user)
#     except Exception as e:
#         print(e)

''''Get Specific User'''
# user = ucm.get_user(user_id='mscott')
# print(user)

''''Add User'''
#print(ucm.add_user(userid='jlevensailor', lastName='Levensailor', firstName='Jeff'))


''''Update User'''
#print(ucm.update_user(userid='jlevensailor', password='Lagavulin16', pin='5432'))

''''Delete User'''
#print(ucm.delete_user(userid='jlevensailor'))





"""
Phones
"""

#---Get Phones

# for phone in ucm.get_phones():
#     print(phone.name)

#---Get Specific Phone

# phone = ucm.get_phone(name='SEP001122445566')
# print(phone.name)

#---Add Phone

# dev = ucm.add_phone(
#     name='SEP0023AF482340',
#     description='Robert - 1102',
#     product='Cisco 8861',
#     device_pool='RTP_DP',
#     location='RTP_LOC',
#     phone_template='Standard 8861 SIP',
#     protocol='SIP',
#     css='AVST-CSS',
#     subscribe_css='AVST-CSS',
#     lines=[
#         ('1102', 'ABQ_PT', 'Robert Smith', 'Robert Smith', 'Robert Smith - 1102', '+1408202XXXX')
#     ]
# )

# dev = ucm.add_phone(
#             name='SEP001122334455',
#             product='Cisco 8861',
#             device_pool='Default',
#             location='Hub_None',
#             protocol='SIP',
#             lines=[
#                 ('1102', '', 'Robert Smith', 'Robert Smith', 'Robert Smith - 1102', '+1408202XXXX')
#             ])
# print(dev)

#---Delete Phone

# ucm.delete_phone('SEP004433220043')


"""
Translations and Transformations
"""

#---Get Translation Patterns

# for trans in ucm.get_translations():
#     detailed = ucm.get_translation(uuid=trans.uuid)
#     print(detailed.description)

#---Get Specific Translation Pattern

# trans = ucm.get_translation(pattern='2XXX', partition='xlates-pt')
# print(trans.description)

#---Add Translation Pattern

# ported = ['12324625544', '12324625545', '12324625546']

# for num in ported:
#     ucm.add_translation(pattern=num, partition='pstn_pt',calledPartyTransformationMask='1102', callingSearchSpaceName='GW_CSS')

#---Delete Translation Pattern

# ucm.delete_translation(pattern='34567', partition='xlates-pt')


#---Update Translation Pattern

# ucm.update_translation(pattern='1234', partition='xlates-pt', newPattern='4567')


"""
Device Pools
"""

#---Get Device Pools

# for dp in ucm.get_device_pools():
#     print(dp.name)

#---Get Specific Device Pool

# dp = ucm.get_device_pool(name='RTP_DP')
# print(dp.name)

#---Add Device Pool

# dp = ucm.add_device_pool(name='Hollywood_DP')
# print(dp)

#---Delete Device Pool

# ucm.delete_device_pool(device_pool='Hollywood_DP')


#---Update Device Pool

# ucm.update_device_pool(name='RTP_DP', regionName='G711_RGN')


"""
CSS and Partitions
"""

#---Get Calling Search Spaces

# for css in ucm.get_calling_search_spaces():
#     print(css.name)

#---Get Specific Calling Search Space

# css = ucm.get_calling_search_space(calling_search_space='pstn-css')
# print(css.name)

#---Add Calling Search Space

# ucm.add_calling_search_space(
#     calling_search_space='VIP_CSS',
#     description='Very Important Stuff'
#     members=['losfeliz-pt','silverlake-pt','pstn-pt']
#     )

#---Delete Calling Search Space

# ucm.update_calling_search_space(calling_search_space='VIP_CSS')


#---Delete Calling Search Space

# ucm.delete_calling_search_space(calling_search_space='VIP_CSS')


#---Get Partitions

# for pt in ucm.get_partitions():
#     print(pt.name)

#---Get Specific Partition

# pt = ucm.get_partition(partition='pstn-pt')
# print(pt.name)

#---Add Partition

# sites = ['ABQ', 'PHX', 'FGS']

# for site in sites:
#     ucm.add_partition(name=site+'_PT', description='Site Specific PT')

#---Delete Partition

# ucm.delete_partition(name='VIP_PT')

"""
Regions and Locations
"""

#---Get Regions

# for reg in ucm.get_regions():
#     print(reg._uuid)

#---Get Specific Region

# reg = ucm.get_region(region='losfeliz_reg')
# print(reg.name)

#---Add Region

# ucm.add_region(region='Hollywood-REG')

#---Delete Region

# ucm.delete_region(region='Hollywood-REG')

#---Get Locations

# for loc in ucm.get_locations():
#     print(loc.name)

#---Get Specific Location

# loc = ucm.get_location(name='Shadow')
# print(loc.name)

#---Add Location

# print(type(ucm.add_location(name='testlocation')))

# print(type(ucm.update_location(name='testlocation', newName='newlocation')['return']))

#---Delete Location

# ucm.delete_location(location='Hollywood-LOC')


"""
Directory Numbers
"""

#---Get Directory Numbers

# for dn in ucm.get_directory_numbers():
#     print(dn)

#---Get Specific Directory Number

# dn = ucm.get_directory_number(directory_number='2888',partition='losfeliz-pt')
# print(dn.uuid)

#---Add Directory Number

# ucm.add_directory_number(
#     pattern='1102',
#     partition='ABQ_PT'
#     )

#---Delete Directory Number

# ucm.delete_directory_number(uuid='{0B0CDC93-EC9C-7255-1B09-40A3CE727D5A}')


"""
Device Profiles
"""

#---Get User Device Profiles

# for udp in ucm.get_device_profiles():
#     print(udp.name)

#---Get Specific User Device Profile

# udp = ucm.get_device_profile(profile='udp-bsimpson')
# print(udp.name)

#---Add User Device Profile

# ucm.add_device_profile(
#     profile='UDP_MScott',
#     description='Michael Scott - 2901',
#     product='Cisco 8861',
#     phone_template='Standard 8861 SIP',
#     protocol='SIP',
#     lines=[
#         ('2901', 'losfeliz-pt', 'Michael Scott', 'Michael Scott', 'Michael Scott - 2901', '+1408202XXXX'),
#         ('2902', 'losfeliz-pt', 'Pam Beesley', 'Pam Beesley', 'Pam Beesley - 2902', '+1408202XXXX')
#     ]
# )

#---Delete User Device Profile

# ucm.delete_device_profile('UDP_Mscott')


"""
CTI Route Points
"""

#---Get CTI Route Points

# for cti in ucm.get_cti_route_points():
#     print(cti.name)

#---Get Specific CTI Route Point

# cti = ucm.get_cti_route_point(cti_route_point='AutoAttendant')
# print(cti.name)

#---Add CTI Route Point

# ucm.add_cti_route_point(
#     cti_route_point='aa-pilot',
#     description='pilot to unity',
#     device_pool='LosFeliz_DP',
#     css='allphone-css',
#     lines=[
#         ('2908', 'losfeliz-pt'), 
#         ('2909', 'losfeliz-pt')
#     ]
# )

#---Delete CTI Route Point

# ucm.delete_cti_route_point(name='OneArch')

"""
CTI Route Points
"""

#---List Sip Trunks

# for trunk in ucm.get_sip_trunks():
#     print(trunk.name)

#---Get Specific Sip Trunk

# trunk = ucm.get_sip_trunk(name='LosFeliz-Trunks')
# print(trunk.name)

#---Add a Sip Trunk

# trunk_info = {
#     "name": "test-sip-trunk",
#     "product": "SIP Trunk",
#     "protocol": "SIP",
#     "protocolSide": "Network",
#     "description": "my new sip trunk",
#     "callingSearchSpaceName": "WOB-HQ-GW-CSS",
#     "devicePoolName": "WOB-HQ-DP",
#     "securityProfileName": "Non Secure SIP Trunk Profile",
#     "sipProfileName": "Standard SIP Profile",
#     "runOnEveryNode": "t",
#     "destinations": {"destination": {
#         "addressIpv4": "4.1.2.3",
#         "port": 5060,
#         "sortOrder": "1"
#     }}
# }

# this_add_siptrunk = ucm.add_sip_trunk(**trunk_info)
# print(this_add_siptrunk)

#---Update Sip Trunk

# ucm.update_sip_trunk(name='oldname', newName='newname')

#---Delete Sip Trunk

# ucm.delete_sip_trunk(name='atlanta')

"""
Route Groups, Lists, and Patterns
"""

#---List Route Plan

# nums = ['19197016707', '19197016712', '19197016713', '19197016706', '191970167016']

# for num in nums:
#     for route in ucm.list_route_plan(num):
#         print(route.dnOrPattern)
# for route in ucm.list_route_plan('2901'):
#     print(route.uuid)

#---Get Route Groups

# for rg in ucm.get_route_groups():
#     print(rg.name)

#--Get Specific Route Group

# rg = ucm.get_route_group(route_group='losfeliz-rg')
# print(rg.uuid)

#---Add Route Group

# ucm.add_route_group(
#     route_group='hollywood-rg', 
#     distribution_algorithm='Circular', 
#     members=[('america-online-sip'), ('h323')])

#---Delete Route Group

# ucm.delete_route_group(route_group='hollywood-rg')


#---Get Route Lists

# for rl in ucm.get_route_lists():
#     print(rl.name)

#---Get Specific Route List

# rl = ucm.get_route_list(route_list='stdloc-rl')
# print(rl.description)

#---Add Route List

# ucm.add_route_list(
#     route_list='hollywood-rl', 
#     description='hollywood', 
#     run_on_all_nodes='true', 
#     cm_group_name='Default', 
#     members=[
#         ('losfeliz-rg'), 
#         ('silverlake-rg')
#     ])

#---Delete Route List

# ucm.delete_route_list(route_list='hollywood-rl')


#---Get Route Patterns

# for rp in ucm.get_route_patterns():
#     print(rp.pattern)

#---Get Specific Route Pattern

# rp = ucm.get_route_pattern(pattern='911')
# print(rp.description)

#---Add Route Pattern

# ucm.add_route_pattern(
#     pattern='999', 
#     partition='losfeliz-pt', 
#     description='Movie Times', 
#     route_list='stdloc-rl'
#     )

#---Delete Route Pattern

# ucm.delete_route_pattern(pattern='999', partition='losfeliz-pt')


"""
Runs and Dos
"""

#---Execute SQL Query

# for sql in ucm.execute_sql_update(query):
#     print(sql)
# def dothis(row):
#     print(row)

# def build_query():
#     with open("intercoms.txt") as intercoms:
#         for row in intercoms:
#             #print(row, end='')
#             query = f'''
#             UPDATE devicenumplanmap dnmp
#             SET dnmp.speeddial = '', dnmp.label = 'ICM:'
#             WHERE dnmp.speeddial = "{row[:10]}*"
#             '''
#             print(query)
#             sql = ucm.execute_sql_update(query)
#             print(sql)

# build_query()
#---Do LDAP Sync on all agreements

#print(ucm.execute_sql_update('''insert into routepartition (name,description) values ('Dodgers','World Series Champs')'''))

# for ldap in ucm.get_ldap_dir():
#     print(ldap.uuid)
#     print(ucm.do_ldap_sync(uuid='ldap.uuid'))

#---Reset Device

#print(ucm.do_device_reset(name='SEP001122337788'))


#---Extension Mobility Login

# ucm.do_device_login(device='SEP001100220033', userId='bsimpson')


#---Extension Mobility Logout

# ucm.do_device_logout(device='SEP001100220033', userId='bsimpson')


# pro = ucm.get_sip_security_profile(name='Non Secure SIP Trunk Profile')
# print(pro)

trunk_info = {
        "name": "trunk",
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
trunk = {}
trunk['sipTrunk'] = trunk_info

trk = ucm.add_sip_trunk(**trunk)
print(trk)