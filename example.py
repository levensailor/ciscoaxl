from ciscoaxl import axl
from lxml import etree

cucm = "10.10.20.1"
username = "administrator"
password = "ciscopsdt"
version = "12.5"
ucm = axl(username=username, password=password, cucm=cucm, cucm_version=version)

# return a list of phones with the following fields populated
phone_list = ucm.get_phones(
    tagfilter={
        "name": "",
        "description": "",
        "product": "",
        "model": "",
        "class": "",
        "protocol": "",
        "protocolSide": "",
        "callingSearchSpaceName": "",
        "devicePoolName": "",
        "commonDeviceConfigName": "",
        "commonPhoneConfigName": "",
        "networkLocation": "",
        "locationName": "",
        "mediaResourceListName": "",
        "networkHoldMohAudioSourceId": "",
        "userHoldMohAudioSourceId": "",
        "loadInformation": "",
        "securityProfileName": "",
        "sipProfileName": "",
        "cgpnTransformationCssName": "",
        "useDevicePoolCgpnTransformCss": "",
        "numberOfButtons": "",
        "phoneTemplateName": "",
        "primaryPhoneName": "",
        "loginUserId": "",
        "defaultProfileName": "",
        "enableExtensionMobility": "",
        "currentProfileName": "",
        "loginTime": "",
        "loginDuration": "",
        # "currentConfig": "",
        "ownerUserName": "",
        "subscribeCallingSearchSpaceName": "",
        "rerouteCallingSearchSpaceName": "",
        "allowCtiControlFlag": "",
        "alwaysUsePrimeLine": "",
        "alwaysUsePrimeLineForVoiceMessage": "",
    }
)

for phone in phone_list:
    print(phone.name)

user_list = ucm.get_users(
    tagfilter={
        "userid": "",
        "firstName": "",
        "lastName": "",
        "directoryUri": "",
        "telephoneNumber": "",
        "enableCti": "",
        "mailid": "",
        "primaryExtension": {"pattern": "", "routePartitionName": ""},
        "enableMobility": "",
        "homeCluster": "",
        "associatedPc": "",
        "enableEmcc": "",
        "imAndPresenceEnable": "",
        "serviceProfile": {"_value_1": ""},
        "status": "",
        "userLocale": "",
        "title": "",
        "subscribeCallingSearchSpaceName": "",
    }
)

for user in user_list:
    print(user.firstName, user.lastName, user.mailid, user.primaryExtension.pattern)

hunt_pilots = ucm.get_hunt_pilots(
    tagfilter={
        "pattern": "",
        "patternUrgency": "",
        "routePartitionName": "",
        "alertingName": "",
        "blockEnable": "",
        "description": "",
        "forwardHuntBusy": "",
        "forwardHuntNoAnswer": "",
        "queueCalls": "",
        "callingPartyTransformationMask": "",
        "callingPartyPrefixDigits": "",
        "callingLinePresentationBit": "",
        "callingNamePresentationBit": "",
        "calledPartyTransformationMask": "",
        "callPickupGroupName": "",
        "huntListName": "",
        "useCallingPartyPhoneMask": "",
        "maxHuntduration": "",
        "displayConnectedNumber": "",
        "aarNeighborhoodName": "",
    }
)

for hunt_pilot in hunt_pilots:
    print(hunt_pilot)

hp = ucm.get_hunt_pilot(pattern="5600")
print(hp)

new_pilot = ucm.add_hunt_pilot(
    pattern="2500",
    description="new pilot",
    blockEnable="false",
    useCallingPartyPhoneMask="Off",
    huntListName="VM_Hunt",
)
print(new_pilot)
