#### Enable AXL SOAP Service on CUCM:

Enable the AXL SOAP interface
Browse to the CUCM Serviceability page on https://<IP_CUCM>/ccmservice
Tools > Service Activation:
Enable the "Cisco AXL Web Service"

![Axl Service](2020-06-01-11-13-59.png)

---

#### Create an AXL Service Account

> Step 1 - Create an AXL User Group
CUCM > User Management > User Group > Add.

> Step 2 - Assign the AXL role to the group
On the top right drop down list "Related Links". 
Select "Assign Role to User Group" and select "Standard AXL API Access"

![Axl role](2020-06-01-11-29-06.png)


> Step 3 - Create a new Application User

CUCM > User Management > Application User > Add.
![Application User](2020-06-01-11-33-25.png)

Add the User Group "AXL Group" to this user so that after saving the roles of the new Application User appear as in the following screen:
![AXL Group](2020-06-01-11-43-34.png)
