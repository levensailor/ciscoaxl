# API Reference

ciscoaxl wraps the Cisco AXL SOAP API, providing Pythonic methods for every major CUCM object type.

## Class

::: ciscoaxl.axl.axl
    options:
      members:
        - __init__
      show_root_heading: true
      show_source: false
      heading_level: 3

## Coverage

| Resource | Methods |
|----------|---------|
| Users | get_users, get_user, add_user, update_user, update_user_em, update_user_credentials, delete_user |
| Phones | get_phones, get_phone, add_phone, update_phone, delete_phone |
| Device Profiles | get_device_profiles, get_device_profile, add_device_profile, update_device_profile, delete_device_profile |
| Directory Numbers | get_directory_numbers, get_directory_number, add_directory_number, update_directory_number, delete_directory_number |
| Device Pools | get_device_pools, get_device_pool, add_device_pool, update_device_pool, delete_device_pool |
| Calling Search Spaces | get_calling_search_spaces, get_calling_search_space, add_calling_search_space, update_calling_search_space, delete_calling_search_space |
| Partitions | get_partitions, get_partition, add_partition, update_partition, delete_partition |
| Route Patterns | get_route_patterns, get_route_pattern, add_route_pattern, update_route_pattern, delete_route_pattern |
| Route Groups | get_route_groups, get_route_group, add_route_group, update_route_group, delete_route_group |
| Route Lists | get_route_lists, get_route_list, add_route_list, update_route_list, delete_route_list |
| Translations | get_translations, get_translation, add_translation, update_translation, delete_translation |
| Transformations | get_called_party_xforms, get_called_party_xform, add_called_party_xform, update_called_party_xform, delete_called_party_xform |
| CTI Route Points | get_cti_route_points, get_cti_route_point, add_cti_route_point, update_cti_route_point, delete_cti_route_point |
| Media Resources | get_media_resource_groups, get_media_resource_group, ... |
| Regions | get_regions, get_region, add_region, update_region, delete_region |
| Locations | get_locations, get_location, add_location, update_location, delete_location |
| Trunks | get_sip_trunks, get_sip_trunk, add_sip_trunk, update_sip_trunk, delete_sip_trunk |
| Call Manager Groups | get_call_manager_groups, get_call_manager_group, add_call_manager_group, update_call_manager_group, delete_call_manager_group |
| Hunt Pilots | get_hunt_pilots, get_hunt_pilot, add_hunt_pilot, update_hunt_pilot, delete_hunt_pilot |
| Hunt Lists | get_hunt_lists, get_hunt_list, add_hunt_list, update_hunt_list, delete_hunt_list |
| Line Groups | get_line_groups, get_line_group, add_line_group, update_line_group, delete_line_group |
| Call Pickup | get_call_pickup_groups, get_call_pickup_group, add_call_pickup_group, update_call_pickup_group, delete_call_pickup_group |
| [Remote Destinations](rd.md) | get_remote_destinations, get_remote_destination, add_remote_destination, update_remote_destination, delete_remote_destination |
| [Remote Destination Profiles](rd.md) | get_remote_destination_profiles, get_remote_destination_profile, add_remote_destination_profile, update_remote_destination_profile, delete_remote_destination_profile |
| [UC Services](ucservice.md) | get_uc_services, get_uc_service, add_uc_service, update_uc_service, delete_uc_service, apply_uc_service, reset_uc_service, restart_uc_service |
| [Service Profiles](ucservice.md) | get_service_profiles, get_service_profile, add_service_profile, update_service_profile, delete_service_profile |
| [Voicemail Pilots](vm.md) | get_voice_mail_pilots, get_voice_mail_pilot, add_voice_mail_pilot, update_voice_mail_pilot, delete_voice_mail_pilot |
| [Voicemail Profiles](vm.md) | get_voice_mail_profiles, get_voice_mail_profile, add_voice_mail_profile, update_voice_mail_profile, delete_voice_mail_profile, apply_voice_mail_profile, reset_voice_mail_profile, restart_voice_mail_profile |
| SQL | run_sql_query, sql_query, sql_update |
| LDAP | get_ldap_dir, do_ldap_sync |
| Actions | do_device_login, do_device_logout, do_device_reset, reset_sip_trunk, do_change_dnd_status |
