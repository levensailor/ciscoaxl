# Introduction

**ciscoaxl** is a Python SDK for the Cisco Unified Communications Manager (CUCM) AXL API.
It makes CUCM automation feel like a normal Python library — no WSDL wrangling, no raw XML.

## What it does

- Wraps the AXL SOAP API with clean, Pythonic methods
- Bundles AXL schema versions from 8.5 through 15.0
- Returns structured objects instead of raw XML
- Translates friendly names (e.g. `partition=`) to AXL element names automatically

## Quick start

```python
from ciscoaxl import axl

ucm = axl(
    username='axlaccess',
    password='axlpassword',
    cucm='10.10.20.1',
    cucm_version='12.5'
)

# List every phone
for phone in ucm.get_phones():
    print(phone.name, phone.description)

# Add a user
ucm.add_user(user_id='jsmith', last_name='Smith', first_name='Jane')

# Run an arbitrary SQL query
result = ucm.run_sql_query("select name from device where description like 'Lab%'")
for row in result.get('rows', []):
    print(row['name'])
```

## AXL schema versions

Bundled: `8.5`, `9.1`, `10.0`, `10.5`, `11.0`, `11.5`, `12.0`, `12.5`, `14.0`, `15.0` (plus `current`).

Set `cucm_version` to match your CUCM major release.

## Error handling

AXL errors surface as `zeep.exceptions.Fault`:

```python
from zeep.exceptions import Fault

try:
    phone = ucm.get_phone(name='SEP001122445566')
except Fault as err:
    print(f'AXL error: {err.message}')
```

`run_sql_query` never raises — on error it returns `num_rows: 0` and stores the exception
in `ucm.last_exception`. Use `ucm.sql_query()` when you want the `Fault` raised.

## DevNet Sandbox

No lab? Reserve a free [Cisco DevNet Collaboration Sandbox](https://developer.cisco.com/site/sandbox/)
to test against a real CUCM instance.
