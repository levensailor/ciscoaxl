# Voicemail

!!! note "Not yet wrapped"
    Voicemail profile / Unity Connection methods are not yet implemented in this SDK.

    Follow progress or contribute at:
    [https://github.com/users/levensailor/projects/6](https://github.com/users/levensailor/projects/6)

Voicemail integration in CUCM is typically done via:

- **UC Service** pointing to a Unity Connection server (see [UC Services](ucservice.md))
- **Voice Mail Profile** attached to Directory Numbers
- **Voice Mail Pilot** that routes calls to the voicemail server

Once implemented, the API will follow the same pattern as other resources:

```python
# Future usage (not yet available)
ucm.get_voice_mail_pilots()
ucm.add_voice_mail_pilot(dirn='8000', css='allphone-css')
ucm.get_voice_mail_profiles()
```
