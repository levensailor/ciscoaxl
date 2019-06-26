# Python SDK for Cisco CUCM AXL API

## AXL API Documentation
 - https://developer.cisco.com/docs/axl-schema-reference/

## Installation
```bash
pip install ciscoaxl
```

## Example Usage
```python
from ciscoaxl import axl

cucm = os.getenv('cucm', '10.10.20.1')
username = os.getenv('cucm_username', 'administrator')
password = os.getenv('cucm_password', 'ciscopsdt')
version = os.getenv('version', '12.5')
ucm = axl(username=cucm_username,password=cucm_password,cucm=cucm,cucm_version=version)
```

## Users

#### Get All Users
```python
for user in ucm.get_users():
    print(user.firstName)
```

#### Get Specific User
```python
this_user = ucm.get_user(user_id='mscott')
if this_user['success']:
    print(this_user['response'])
```

#### Add User
```python
this_add_user = ucm.add_user(user_id='jlevensailor', last_name='Levensailor', first_name='Jeff')
if this_add_user['success']:
    print(this_add_user['response'])
```

#### Delete User
```python
this_delete_user = ucm.delete_user(user_id='jlevensailor')
if this_delete_user['success']:
    print(this_delete_user['response'])
```

#### Update User
```python
this_update_user = ucm.update_user(user_id='jlevensailor', password='Lagavulin16', pin='5432')
if this_update_user['success']:
    print(this_update_user['response'])
```

## Phones

#### Get Phones

```python
for phone in ucm.get_phones():
    print(phone.name)
```

#### Get Specific Phone

```python
this_phone = ucm.get_user(user_id='lsimpson')
if this_phone['success']:
    print(this_phone['response'])
```

#### Add Phone

```python
this_add_phone = ucm.add_phone(
    name='SEP0023AF482340',
    description='Robert - 1102',
    product='Cisco 8861',
    device_pool='RTP_DP',
    location='RTP_LOC',
    phone_template='Standard 8861 SIP',
    protocol='SIP',
    css='AVST-CSS',
    subscribe_css='AVST-CSS',
    lines=[
        ('1102', 'ABQ_PT', 'Robert Smith', 'Robert Smith', 'Robert Smith - 1102', '+1408202XXXX')
    ]
)
if this_add_phone['success']:
    print(this_add_phone['response'])
```

#### Delete Phone

```python
this_delete_phone = ucm.delete_phone('SEP004433220043')
if this_delete_phone['success']:
    print(this_delete_phone['response'])
```

## Translations and Transformations


#### Get Translation Patterns

```python
for trans in ucm.get_translations():
        this_trans = ucm.get_translation(uuid=trans._uuid)
        if this_trans['success']:
            mask = this_trans['response'].calledPartyTransformationMask
            if mask == "3001":
                print(this_trans['response'].pattern)
```

#### Get Specific Translation Pattern

```python
this_trans = ucm.get_translation(pattern='2XXX', partition='xlates-pt')
if this_trans['success']:
    print(this_trans['response'].description)
```

#### Add Translation Pattern

```python
ported = ['12324625544', '12324625545', '12324625546']

for num in ported:
    this_add_trans = ucm.add_translation(pattern=num, partition='pstn_pt',calledPartyTransformationMask='1102', callingSearchSpaceName='GW_CSS')
    if this_add_trans['success']:
        print(this_add_trans['response'])
```

#### Delete Translation Pattern

```python
this_delete_trans = ucm.delete_translation(pattern='34567', partition='xlates-pt')
if this_delete_trans['success']:
    print(this_delete_trans['response'])
```

#### Update Translation Pattern

```python
this_update_trans = ucm.update_translation(pattern='1234', partition='xlates-pt', newPattern='4567')
if this_update_trans['success']:
    print(this_update_trans['response'])
```

## Device Pools


#### Get Device Pools

```python
for dp in ucm.get_device_pools():
    print(dp)
```

#### Get Specific Device Pool

```python
this_dp = ucm.get_device_pool(name='RTP_DP')
if this_dp['success']:
    print(this_dp['response'])
```

#### Add Device Pool

```python
this_add_dp = ucm.add_device_pool(device_pool='Hollywood_DP')
if this_add_dp['success']:
    print(this_add_dp['response'])
```

#### Delete Device Pool

```python
this_delete_dp = ucm.delete_device_pool(device_pool='Hollywood_DP')
if this_delete_dp['success']:
    print(this_delete_dp['response'])
```

#### Update Device Pool

```python
this_update_dp = ucm.update_device_pool(name='RTP_DP', regionName='G711_RGN')
if this_update_dp['success']:
    print(this_update_dp['response'])
```

## CSS and Partitions


#### Get Calling Search Spaces

```python
for css in ucm.get_calling_search_spaces():
    print(css.name)
```

#### Get Specific Calling Search Space

```python
this_css = ucm.get_calling_search_space(calling_search_space='pstn-css')
if this_css['success']:
    print(this_css['response']._uuid)
```

#### Add Calling Search Space

```python
this_add_css = ucm.add_calling_search_space(
    calling_search_space='VIP_CSS',
    description='Very Important Stuff'
    members=['losfeliz-pt','silverlake-pt','pstn-pt']
    )
if this_add_css['success']:
    print(this_add_css['response'])
```

#### Delete Calling Search Space

```python
this_update_css = ucm.update_calling_search_space(calling_search_space='VIP_CSS')
if this_update_css['success']:
    print(this_update_css['response'])
```

#### Delete Calling Search Space

```python
this_delete_css = ucm.delete_calling_search_space(calling_search_space='VIP_CSS')
if this_delete_css['success']:
    print(this_delete_css['response'])
```

#### Get Partitions

```python
for pt in ucm.get_partitions():
    print(pt.name)
```

#### Get Specific Partition

```python
this_pt = ucm.get_partition(partition='pstn-pt')
if this_pt['success']:
    print(this_pt['response']._uuid)
```

#### Add Partition

```python
this_add_pt = ucm.add_partition(partition='VIP_PT', description='Very Important Peep')
if this_add_pt['success']:
    print(this_add_pt['response'])
```

#### Delete Partition

```python
this_delete_pt = ucm.delete_partition(name='VIP_PT')
if this_delete_pt['success']:
    print(this_delete_pt['response'])
```

## Regions and Locations

#### Get Regions

```python
for reg in ucm.get_regions():
    print(reg._uuid)
```

#### Get Specific Region

```python
this_reg = ucm.get_region(region='losfeliz_reg')
if this_reg['success']:
    print(this_reg['response']._uuid)
```

#### Add Region

```python
this_add_reg = ucm.add_region(region='Hollywood-REG')
if this_add_reg['success']:
    print(this_add_reg['response'])
```

#### Delete Region

```python
this_delete_reg = ucm.delete_region(region='Hollywood-REG')
if this_delete_reg['success']:
    print(this_delete_reg['response'])
```

#### Get Locations

```python
for loc in ucm.get_locations():
    print(loc.name)
```

#### Get Specific Location

```python
this_loc = ucm.get_location(name='Shadow')
if this_loc['success']:
    print(this_loc['response'])
```

#### Add Location

```python
this_add_location = ucm.add_location(location='Hollywood-LOC')
if this_add_location['success']:
    print(this_add_location['response'])
```

#### Delete Location

```python
this_delete_location = ucm.delete_location(location='Hollywood-LOC')
if this_delete_location['success']:
    print(this_delete_location['response'])
```

## Directory Numbers

#### Get Directory Numbers

```python
for dn in ucm.get_directory_numbers():
    print(dn)
```

#### Get Specific Directory Number

```python
this_dn = ucm.get_directory_number(directory_number='2888',partition='losfeliz-pt')
if this_dn['success']:
    print(this_dn['response']._uuid)
```

#### Add Directory Number

```python
this_add_dn = ucm.add_directory_number(
    pattern='1102',
    partition='ABQ_PT'
    )
if this_add_dn['success']:
    print(this_add_dn['response'])
```

#### Delete Directory Number

```python
this_delete_dn = ucm.delete_directory_number(uuid='{0B0CDC93-EC9C-7255-1B09-40A3CE727D5A}')
if this_delete_dn['success']:
    print(this_delete_dn['response'])
```

## Device Profiles

#### Get User Device Profiles

```python
for udp in ucm.get_device_profiles():
    print(udp.name)
```

#### Get Specific User Device Profile

```python
this_udp = ucm.get_device_profile(profile='udp-bsimpson')
if this_udp['success']:
    print(this_udp['response']._uuid)
```

#### Add User Device Profile

```python
this_add_udp = ucm.add_device_profile(
    profile='UDP_MScott',
    description='Michael Scott - 2901',
    product='Cisco 8861',
    phone_template='Standard 8861 SIP',
    protocol='SIP',
    lines=[
        ('2901', 'losfeliz-pt', 'Michael Scott', 'Michael Scott', 'Michael Scott - 2901', '+1408202XXXX'),
        ('2902', 'losfeliz-pt', 'Pam Beesley', 'Pam Beesley', 'Pam Beesley - 2902', '+1408202XXXX')
    ]
)
if this_add_udp['success']:
    print(this_add_udp['response'])
```

#### Delete User Device Profile

```python
this_delete_udp = ucm.delete_device_profile('UDP_Mscott')
if this_delete_udp['success']:
    print(this_delete_udp['response'])
```

## CTI Route Points

#### Get CTI Route Points

```python
for cti in ucm.get_cti_route_points():
    print(cti.name)
```

#### Get Specific CTI Route Point

```python
this_cti = ucm.get_cti_route_point(cti_route_point='AutoAttendant')
if this_cti['success']:
    print(this_cti['response'])
```

#### Add CTI Route Point

```python
this_add_cti = ucm.add_cti_route_point(
    cti_route_point='aa-pilot',
    description='pilot to unity',
    device_pool='LosFeliz_DP',
    css='allphone-css',
    lines=[
        ('2908', 'losfeliz-pt'), 
        ('2909', 'losfeliz-pt')
    ]
)
if this_add_cti['success']:
    print(this_add_cti['response'])
```

#### Delete CTI Route Point

```python
this_delete_cti = ucm.delete_cti_route_point(name='OneArch')
if this_delete_cti['success']:
    print(this_delete_cti['response'])
```

## Route Groups, Lists, and Patterns

#### List Route Plan

```python
nums = ['19197016707', '19197016712', '19197016713', '19197016706', '191970167016']

for num in nums:
    for route in ucm.list_route_plan(num):
        print(route.dnOrPattern)
for route in ucm.list_route_plan('2901'):
    print(route._uuid)
```

#### Get Route Groups

```python
for rg in ucm.get_route_groups():
    print(rg.name)
```

#### Get Specific Route Group

```python
this_rg = ucm.get_route_group(route_group='losfeliz-rg')
if this_rg['success']:
    print(this_rg['response']._uuid)
```

#### Add Route Group

```python
this_add_rg = ucm.add_route_group(
    route_group='hollywood-rg', 
    distribution_algorithm='Circular', 
    members=[('america-online-sip'), ('h323')])
if this_add_rg['success']:
    print(this_add_rg['response'])
```

#### Delete Route Group

```python
this_delete_rg = ucm.delete_route_group(route_group='hollywood-rg')
if this_delete_rg['success']:
    print(this_delete_rg['response'])
```

#### Get Route Lists

```python
for rl in ucm.get_route_lists():
    print(rl.name)
```

#### Get Specific Route List

```python
this_rl = ucm.get_route_list(route_list='stdloc-rl')
if this_rl['success']:
    print(this_rl['response'].description)
```

#### Add Route List

```python
this_add_rl = ucm.add_route_list(
    route_list='hollywood-rl', 
    description='hollywood', 
    run_on_all_nodes='true', 
    cm_group_name='Default', 
    members=[
        ('losfeliz-rg'), 
        ('silverlake-rg')
    ])
if this_add_rl['success']:
    print(this_add_rl['response'])
```

#### Delete Route List

```python
this_delete_rl = ucm.delete_route_list(route_list='hollywood-rl')
if this_delete_rl['success']:
    print(this_delete_rl['response'])
```

#### Get Route Patterns

```python
for rp in ucm.get_route_patterns():
    print(rp.pattern)
```

#### Get Specific Route Pattern

```python
this_rp = ucm.get_route_pattern(pattern='911')
if this_rp['success']:
    print(this_rp['response'].description)
```

#### Add Route Pattern

```python
this_add_rp = ucm.add_route_pattern(
    pattern='999', 
    partition='losfeliz-pt', 
    description='Movie Times', 
    route_list='stdloc-rl'
    )
if this_add_rp['success']:
    print(this_add_rp['response'])
```

#### Delete Route Pattern

```python
this_delete_rp = ucm.delete_route_pattern(pattern='999', partition='losfeliz-pt')
if this_delete_rp['success']:
    print(this_delete_rp['response'])
```

## Runs and Dos

#### Execute SQL Query

```sh
for sql in ucm.execute_sql_query('select * from device where description like "Bart%"'):
    print(sql.name)
```

#### Do LDAP Sync on all agreements

```sh
for ldap in ucm.get_ldap_dir():
    this_sync = ucm.do_ldap_sync(uuid=ldap._uuid)
    if this_sync['success']:
            print(this_sync['response'])
```

#### Reset Device

```python
this_reset = ucm.do_device_reset(device='SEP001100220033')
if this_reset['success']:
    print(this_reset['response'])
```

#### Extension Mobility Login

```python
this_device_login = ucm.do_device_login(device='SEP001100220033', userId='bsimpson')
if this_device_login['success']:
    print(this_device_login['response'])
```

#### Extension Mobility Logout

```python
this_device_logout = ucm.do_device_logout(device='SEP001100220033', userId='bsimpson')
if this_device_logout['success']:
    print(this_device_logout['response'])
```