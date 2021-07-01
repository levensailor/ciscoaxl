from ciscoaxl import axl
from lxml import etree
cucm = '10.129.225.201'
username = 'administrator'
password = 'Pr3sid10!'
version = '11.5'
ucm = axl(username=username,password=password,cucm=cucm,cucm_version=version)

# query = {"product": "Cisco Unified Client Services Framework"}
# phones = ucm.get_phones(query=query)
# for phone in phones:
#     print(phone.name)

css = ucm.update_calling_search_space(
name="WOB-HQ-CSS",
addMembers=[
    {
        "member": {
        "routePartitionName": "DUBLIN_PT",
        "index": "0"
        },
        "member": {
            "routePartitionName": "IPMA-PT",
            "index": "1"
        }
    }
])