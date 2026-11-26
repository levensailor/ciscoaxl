# UC Services

!!! note "Not yet wrapped"
    UC Service methods (Unified Messaging, Conferencing, Directory, etc.) are not yet
    implemented in this SDK.

    Follow progress or contribute at:
    [https://github.com/users/levensailor/projects/6](https://github.com/users/levensailor/projects/6)

UC Services are configured in CUCM under **User Management → User Settings → UC Service**
and assigned to users via Service Profiles.

Once implemented, the API will follow the same pattern as other resources:

```python
# Future usage (not yet available)
services = ucm.get_uc_services()
ucm.add_uc_service(name='...', product='Unity Connection', hostnameOrIP='10.0.0.1')
ucm.delete_uc_service(name='...')
```
