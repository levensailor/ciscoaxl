from ciscoaxl import axl
from decouple import config

cucm = config("CUCM_PUBLISHER")
username = config("CUCM_AXL_USERNAME")
password = config("CUCM_AXL_PASSWORD")
version = config("CUCM_VERSION")

ucm = axl(username=username, password=password, cucm=cucm, cucm_version=version)


class TestPhoneMethods:
    def test_add_phone(self):
        add_phone = ucm.add_phone(
            name="SEP0023AF482340",
            description="Robert - 1102",
            product="Cisco 8861",
            device_pool="boston",
            location="Hub_None",
            phone_template="Standard 8861 SIP",
            protocol="SIP",
            css="Device_CSS",
            subscribe_css="Device_CSS",
            lines=[
                (
                    "1102",
                    "Internal_PT",
                    "Robert Smith",
                    "Robert Smith",
                    "Robert Smith - 1102",
                    "+1408202XXXX",
                )
            ],
        )

        assert type(add_phone["return"]) == str

    def test_update_phone(self):
        add_phone = ucm.update_phone(
            name="SEP0023AF482340",
            description="Robert - 1102 changed",
        )

        get_phone = ucm.get_phone(name="SEP0023AF482340")
        assert type(add_phone["return"]) == str
        assert get_phone.description == "Robert - 1102 changed"

    def test_delete_phone(self):
        add_phone = ucm.delete_phone(
            name="SEP0023AF482340",
        )

        get_phone = ucm.get_phone(name="SEP0023AF482340")
        assert type(add_phone["return"]) == str
        assert (
            get_phone.message
            == "Item not valid: The specified SEP0023AF482340 was not found"
        )

    def test_add_phone_bogus_macaddr(self):
        add_phone = ucm.add_phone(
            name="SEP0023AF482340Z",
            description="Robert - 1102",
            product="Cisco 8861",
            device_pool="boston",
            location="Hub_None",
            phone_template="Standard 8861 SIP",
            protocol="SIP",
            css="Device_CSS",
            subscribe_css="Device_CSS",
            lines=[
                (
                    "1102",
                    "Internal_PT",
                    "Robert Smith",
                    "Robert Smith",
                    "Robert Smith - 1102",
                    "+1408202XXXX",
                )
            ],
        )

        assert (
            add_phone.message
            == "The specified name has invalid characters or is not formatted correctly for this device type."
        )


# TODO: add below methods for testing
# # return a list of phones with the following fields populated
# phone_list = ucm.get_phones(
#     tagfilter={
#         "name": "",
#         "description": "",
#         "product": "",
#         "model": "",
#         "class": "",
#         "protocol": "",
#         "protocolSide": "",
#         "callingSearchSpaceName": "",
#         "devicePoolName": "",
#         "commonDeviceConfigName": "",
#         "commonPhoneConfigName": "",
#         "networkLocation": "",
#         "locationName": "",
#         "mediaResourceListName": "",
#         "networkHoldMohAudioSourceId": "",
#         "userHoldMohAudioSourceId": "",
#         "loadInformation": "",
#         "securityProfileName": "",
#         "sipProfileName": "",
#         "cgpnTransformationCssName": "",
#         "useDevicePoolCgpnTransformCss": "",
#         "numberOfButtons": "",
#         "phoneTemplateName": "",
#         "primaryPhoneName": "",
#         "loginUserId": "",
#         "defaultProfileName": "",
#         "enableExtensionMobility": "",
#         "currentProfileName": "",
#         "loginTime": "",
#         "loginDuration": "",
#         # "currentConfig": "",
#         "ownerUserName": "",
#         "subscribeCallingSearchSpaceName": "",
#         "rerouteCallingSearchSpaceName": "",
#         "allowCtiControlFlag": "",
#         "alwaysUsePrimeLine": "",
#         "alwaysUsePrimeLineForVoiceMessage": "",
#     }
# )

# get_phone = ucm.get_phone(name="SEP0023AF482340")
# print(get_phone)

# user_list = ucm.get_users(
#     tagfilter={
#         "userid": "",
#         "firstName": "",
#         "lastName": "",
#         "directoryUri": "",
#         "telephoneNumber": "",
#         "enableCti": "",
#         "mailid": "",
#         "primaryExtension": {"pattern": "", "routePartitionName": ""},
#         "enableMobility": "",
#         "homeCluster": "",
#         "associatedPc": "",
#         "enableEmcc": "",
#         "imAndPresenceEnable": "",
#         "serviceProfile": {"_value_1": ""},
#         "status": "",
#         "userLocale": "",
#         "title": "",
#         "subscribeCallingSearchSpaceName": "",
#     }
# )

# for user in user_list:
#     print(user.firstName, user.lastName, user.mailid, user.primaryExtension.pattern)

# hunt_pilots = ucm.get_hunt_pilots(
#     tagfilter={
#         "pattern": "",
#         "patternUrgency": "",
#         "routePartitionName": "",
#         "alertingName": "",
#         "blockEnable": "",
#         "description": "",
#         "forwardHuntBusy": "",
#         "forwardHuntNoAnswer": "",
#         "queueCalls": "",
#         "callingPartyTransformationMask": "",
#         "callingPartyPrefixDigits": "",
#         "callingLinePresentationBit": "",
#         "callingNamePresentationBit": "",
#         "calledPartyTransformationMask": "",
#         "callPickupGroupName": "",
#         "huntListName": "",
#         "useCallingPartyPhoneMask": "",
#         "maxHuntduration": "",
#         "displayConnectedNumber": "",
#         "aarNeighborhoodName": "",
#     }
# )
# print(hunt_pilots)

# ###########################  Hunt List, Line Group, Hunt Pilot ############
# huntlists = ucm.get_hunt_lists()
# print(huntlists)

# new_huntlist = ucm.add_hunt_list(
#     name="My_Test_HL",
#     callManagerGroupName="Default",
#     description="new hunt list",
#     routeListEnabled=True,
# )
# print(new_huntlist)

# update_huntlist = ucm.update_hunt_list(name="My_Test_HL", description="modified HL")
# print(update_huntlist)

# hunt_pilots = ucm.get_hunt_pilots()
# print(hunt_pilots)

# new_pilot = ucm.add_hunt_pilot(
#     pattern="2500",
#     routePartitionName="Internal_PT",
#     description="new pilot",
#     blockEnable="false",
#     useCallingPartyPhoneMask="Off",
#     huntListName="My_Test_HL",
# )
# print(new_pilot)

# hunt_pilots = ucm.get_hunt_pilots()
# print(hunt_pilots)

# update_pilot = ucm.update_hunt_pilot(
#     pattern=2500, description="modified pilot", routePartitionName="Internal_PT"
# )
# print(update_pilot)

# get_hunt_pilot = ucm.get_hunt_pilot(pattern="2500", routePartitionName="Internal_PT")
# print(get_hunt_pilot)

# line_groups = ucm.get_line_groups()
# print(line_groups)

# get_line_group = ucm.get_line_group(name="Test")
# print(get_line_group)

# new_line_group = ucm.add_line_group(
#     name="My_Test_LG",
#     distributionAlgorithm="Longest Idle Time",
#     rnaReversionTimeOut="10",
#     huntAlgorithmNoAnswer="Try next member; then, try next group in Hunt List",
#     huntAlgorithmBusy="Try next member; then, try next group in Hunt List",
#     huntAlgorithmNotAvailable="Try next member; then, try next group in Hunt List",
#     members={
#         "member": [
#             {
#                 "lineSelectionOrder": 0,
#                 "directoryNumber": {
#                     "pattern": "1102",
#                     "routePartitionName": "Internal_PT",
#                 },
#             }
#         ]
#     },
# )
# print(new_line_group)

# update_line_group = ucm.update_line_group(
#     name="My_Test_LG", distributionAlgorithm="Broadcast"
# )

# get_line_group = ucm.get_line_group(name="My_Test_LG")
# print(get_line_group)

# call_pickup_groups = ucm.get_call_pickup_groups()
# print(call_pickup_groups)

# new_cpug = ucm.add_call_pickup_group(name="My_Test_CPUG", pattern="2502")
# print(new_cpug)

# update_call_pickup_group = ucm.update_call_pickup_group(
#     name="My_Test_CPUG", description="changed description"
# )
# print(update_call_pickup_group)

# get_cpug = ucm.get_call_pickup_group(name="My_Test_CPUG")
# print(get_cpug)

# #####   CLEANUP   #####
# del_hp = ucm.delete_hunt_pilot(pattern="2500", routePartitionName="Internal_PT")
# print(del_hp)

# del_hp = ucm.delete_hunt_list(name="My_Test_HL")
# print(del_hp)

# del_lg = ucm.delete_line_group(name="My_Test_LG")
# print(del_hp)

# del_cpug = ucm.delete_call_pickup_group(name="My_Test_CPUG")
# print(del_cpug)

# del_phone = ucm.delete_phone(name="SEP0023AF482340")
# print(del_phone)

# del_dirnum = ucm.delete_directory_number(
#     pattern="1102", routePartitionName="Internal_PT"
# )
# print(del_dirnum)
