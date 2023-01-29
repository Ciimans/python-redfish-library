# Copyright Notice:
# Copyright 2016-2021 DMTF. All rights reserved.
# License: BSD 3-Clause License. For full text see link:
# https://github.com/DMTF/python-redfish-library/blob/master/LICENSE.md

import sys
import json
import redfish

# When running remotely connect using the address, account name, 
# and password to send https requests
login_host = "https://10.194.78.17"
login_account = "Administrator"
login_password = "superuser"

error_code = 0

## Create a REDFISH object
REDFISH_OBJ = redfish.redfish_client(base_url=login_host, username=login_account,
                          password=login_password, default_prefix='/redfish/v1')

# Login into the server and create a session
REDFISH_OBJ.login(auth="basic")

###############################################
# First time password change of default account
###############################################
sys.stdout.write("%s\n" % "Change password ...")
headers = {'Content-Type': 'application/json', "If-None-Match": "sdggfgvdfgdgfdgdfgd"}
body = {"Password":"superuser1"}
response = REDFISH_OBJ.patch('/redfish/v1/AccountService/Accounts/1', body=body, headers=headers)
if response.status != 204:
    sys.stdout.write("%s\n" % response)
    error_code = 1
REDFISH_OBJ.logout()
if error_code == 1:
    sys.exit(error_code)

REDFISH_OBJ = redfish.redfish_client(base_url=login_host, username=login_account,
                          password="superuser1", default_prefix='/redfish/v1')


REDFISH_OBJ.login(auth="basic")
body = {"Password": login_password}
response = REDFISH_OBJ.patch('/redfish/v1/AccountService/Accounts/1', body=body, headers=headers)
if response.status != 204:
    sys.stdout.write("%s\n" % response)
    error_code = 1
REDFISH_OBJ.logout()
if error_code == 1:
    sys.exit(error_code)

###############################################
# Login again
###############################################

## Create a REDFISH object
REDFISH_OBJ = redfish.redfish_client(base_url=login_host, username=login_account,
                          password=login_password, default_prefix='/redfish/v1')

# Login into the server and create a session
REDFISH_OBJ.login(auth="basic")


###############################################
# Firmware update
###############################################

# Format parts of the Update
sys.stdout.write("%s\n" % "Uploading image ...")
headers = {'Content-Type': 'multipart/form-data'}
body = {}
body['image_file'] = ('rom.ima', open(str(sys.argv[1]), 'rb'), 'application/octet-stream')
response = REDFISH_OBJ.post('/redfish/v1/UpdateService/Actions/Oem/UpdateService.UploadFirmwareImage', body=body, headers=headers)
if response.status != 204:
    sys.stdout.write("%s\n" % response)
    sys.exit(1)

sys.stdout.write("%s\n" % "Updating firmware ...")
headers2 = {'Content-Type': 'application/json'}
body2 = {"FlashType":"DUALIMAGEFwUpdate","UploadSelector":"Image2"}
response = REDFISH_OBJ.post('/redfish/v1/UpdateService/Actions/Oem/UpdateService.BMCFwUpdate', body=body2, headers=headers2)
if response.status != 202:
    sys.stdout.write("%s\n" % response)
    sys.exit(1)
REDFISH_OBJ.logout()
sys.stdout.write("%s\n" % "Firmware update complete ...")
sys.exit(0)