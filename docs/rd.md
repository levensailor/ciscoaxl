# Remote Destinations

!!! note "Not yet wrapped"
    Remote Destination (Mobile Connect) methods are not yet implemented in this SDK.
    This feature is tracked as a **P0 item** on the project roadmap.

    Follow progress or contribute at:
    [https://github.com/users/levensailor/projects/6](https://github.com/users/levensailor/projects/6)

Remote Destinations allow CUCM to ring a mobile number when a desk phone receives a call.
They are associated with a Remote Destination Profile, which is configured on the user.

Once implemented, the API will follow the same pattern as other resources:

```python
# Future usage (not yet available)
rds = ucm.get_remote_destinations()
ucm.add_remote_destination(name='...')
ucm.delete_remote_destination(name='...')
```
