![Ciscoaxl](ciscoaxl.png)

- Documentation: [ciscoaxl.readthedocs.io/en/latest](https://ciscoaxl.readthedocs.io/en/latest)
- Repository: [github.com/levensailor/ciscoaxl](https://github.com/levensailor/ciscoaxl)
- PyPi: [pypi.org/project/ciscoaxl/](https://pypi.org/project/ciscoaxl/)
- AXL Schema: [developer.cisco.com/docs/axl-schema-reference](https://developer.cisco.com/docs/axl-schema-reference/)

ciscoaxl is a simple to use python sdk for Cisco Unified Communications Manager AXL API. 


### Installation

```bash
pip install ciscoaxl
```

#### SDK Usage 

```python
from ciscoaxl import axl

cucm = '10.10.20.1'
username = 'axlaccess'
password = 'axlpassword'
version = '12.5'
ucm = axl(username=username,password=password,cucm=cucm,cucm_version=version)

users = ucm.get_users()
```
