# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import math
import os
import random
from azure.iot.device import ProvisioningDeviceClient
from azure.iot.device import IoTHubDeviceClient, Message
import uuid
import time
# 
def randomSpeed():
    count = random.randint(100,200)
    duration = random.randint(50,70)
    return str({"ProduceSpeed":{"count":count,"duration":duration,"speed":count/(duration/60),"product":"aa"}})


provisioning_host = "global.azure-devices-provisioning.net"
id_scope = "0ne0051ACE9"
registration_id = "249bnk59bus"
symmetric_key = "ULDVEXKOU400oMEB/iSfFtcEPvosgCn8UJu0bcFibeg="

provisioning_device_client = ProvisioningDeviceClient.create_from_symmetric_key(
    provisioning_host=provisioning_host,
    registration_id=registration_id,
    id_scope=id_scope,
    symmetric_key=symmetric_key,
)

provisioning_device_client.provisioning_payload = {"modelId": "dtmi:cryIotCentral:Hackathon_1g4;1"}
registration_result = provisioning_device_client.register()
# The result can be directly printed to view the important details.
print(registration_result)

# Individual attributes can be seen as well
print("The status was :-")
print(registration_result.status)
print("The etag is :-")
print(registration_result.registration_state.etag)
print(registration_result.registration_state.assigned_hub)


if registration_result.status == "assigned":
    print("Will send telemetry from the provisioned device")
    # Create device client from the above result
    device_client = IoTHubDeviceClient.create_from_symmetric_key(
        symmetric_key=symmetric_key,
        hostname=registration_result.registration_state.assigned_hub,
        device_id=registration_result.registration_state.device_id,
    )

    # Connect the client.
    device_client.connect()

    for i in range(1, 999):
        print("sending message #" + str(i))
        device_client.send_message(randomSpeed())
        time.sleep(5)
    time.sleep(20)
    device_client.disconnect()
else:
    print("Can not send telemetry from the provisioned device")

 
