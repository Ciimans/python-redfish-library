# Copyright Notice:
# Copyright 2016-2021 DMTF. All rights reserved.
# License: BSD 3-Clause License. For full text see link:
# https://github.com/DMTF/python-redfish-library/blob/master/LICENSE.md

import sys
import json
import redfish

# When running remotely connect using the address, account name, 
# and password to send https requests
login_host = "https://10.194.78.206"
login_account = "Administrator"
login_password = "superuser"

## Create a REDFISH object
REDFISH_OBJ = redfish.redfish_client(base_url=login_host, username=login_account,
                          password=login_password, default_prefix='/redfish/v1')

# Login into the server and create a session
REDFISH_OBJ.login(auth="basec")

# Format parts of the Update
headers = {'Content-Type': 'multipart/form-data'}
body = {}
body['image_file'] = ('rom.ima', open('rom.ima', 'rb'), 'application/octet-stream')

# Perform the POST operation, upload image
response = REDFISH_OBJ.post('/redfish/v1/UpdateService/Actions/Oem/UpdateService.UploadFirmwareImage', body=body, headers=headers)

# Print out the response
sys.stdout.write("%s\n" % response)

# Perform the update operation
headers = {'Content-Type': 'application/json'}
body = {"FlashType":"DUALIMAGEFwUpdate", "UploadSelector":"Image2"}
response = REDFISH_OBJ.post('/redfish/v1/UpdateService/Actions/Oem/UpdateService.BMCFwUpdate', body=body, headers=headers)
# Print out the response
sys.stdout.write("%s\n" % response)

# Logout of the current session
REDFISH_OBJ.logout()
