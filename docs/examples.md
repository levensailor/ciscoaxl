# Examples

All examples assume a connected `ucm` object:

```python
from ciscoaxl import axl

ucm = axl(
    username='axlaccess',
    password='axlpassword',
    cucm='10.10.20.1',
    cucm_version='12.5'
)
```

---

## Users

```python
# List all users
for user in ucm.get_users():
    print(user.firstName, user.lastName)

# Get a specific user
user = ucm.get_user(user_id='mscott')
print(user.email)

# Add a user
ucm.add_user(user_id='jlevensailor', last_name='Levensailor', first_name='Jeff')

# Update a user's password
ucm.update_user(user_id='jlevensailor', password='Lagavulin16', pin='5432')

# Delete a user
ucm.delete_user(user_id='jlevensailor')
```

---

## Phones

```python
# List all phones
for phone in ucm.get_phones():
    print(phone.name)

# Add a phone with a line
ucm.add_phone(
    name='SEP0023AF482340',
    description='Robert - 1102',
    product='Cisco 8861',
    device_pool='RTP_DP',
    location='RTP_LOC',
    phone_template='Standard 8861 SIP',
    protocol='SIP',
    css='AVST-CSS',
    lines=[
        ('1102', 'ABQ_PT', 'Robert Smith', 'Robert Smith', 'Robert Smith - 1102', '+1408202XXXX')
    ]
)

# Delete a phone
ucm.delete_phone(name='SEP004433220043')
```

---

## Route Patterns

```python
# Add a route pattern
ucm.add_route_pattern(
    pattern='999',
    partition='losfeliz-pt',
    description='Movie Times',
    route_list='stdloc-rl'
)

# List the route plan for a DID
for route in ucm.list_route_plan('19197016707'):
    print(route.dnOrPattern)

# Delete a route pattern
ucm.delete_route_pattern(pattern='999', partition='losfeliz-pt')
```

---

## SQL

```python
# Run a read-only SQL query (never raises)
result = ucm.run_sql_query(
    "select name, description from device where description like 'Lab%'"
)
for row in result.get('rows', []):
    print(row['name'], row['description'])

# Run a SQL update
ucm.sql_update("update device set description='Updated' where name='SEP001122334455'")
```

---

## Hunt Groups

```python
# Add a line group
ucm.add_line_group(name='SupportLineGroup', distributionAlgorithm='Top Down')

# Add a hunt list referencing the line group
ucm.add_hunt_list(name='SupportHL', callManagerGroupName='Default')

# Add a hunt pilot
ucm.add_hunt_pilot(pattern='2000', partition='losfeliz-pt', huntListName='SupportHL')
```

---

## Extension Mobility

```python
# Log in a device
ucm.do_device_login(
    device='SEP001100220033',
    userId='bsimpson',
    profileName='UDP_bsimpson',
    loginDuration=0
)

# Log out a device
ucm.do_device_logout(device='SEP001100220033')
```

---

## LDAP Sync

```python
for ldap in ucm.get_ldap_dir():
    ucm.do_ldap_sync(uuid=ldap.uuid)
```

---

## Tagfilter (return extra fields)

By default, list methods return a minimal field set for performance.
Pass `tagfilter={}` to get everything:

```python
phones = ucm.get_phones(tagfilter={
    "name": "",
    "product": "",
    "description": "",
    "protocol": "",
    "locationName": "",
    "callingSearchSpaceName": "",
    "devicePoolName": ""
})
```
