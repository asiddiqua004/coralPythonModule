import os
import asyncio
import uuid
import time
import sys
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message

async def main():

    conn_str = "HostName=5G-IoT-System-For-Emergency-Responders.azure-devices.net;DeviceId=application_device1;SharedAccessKey=x84oYfc8Wm4lL7nfMzNm87X7YmFbC+TtHX4ny+bV8ck="
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    # Connect the device client.
    await device_client.connect()

    # Send a few messages
    count = 0
    tempFile = open("/sys/class/thermal/thermal_zone0/temp", "r")
    while count < 5:
        cpu_temp = tempFile.read()
        cpu_temp_float = float(cpu_temp)
        tempFile.seek(0)
        print("Sending message to Azure IoT...")
        msg = Message("Environment sensor")
        msg.message_id = uuid.uuid4()
        msg.custom_properties["Temperature"] = cpu_temp_float
        await device_client.send_message(msg)
        print("Message successfully sent:")
        print(msg.custom_properties)
        count = count + 1
        time.sleep(10)

    # finally, disconnect
    await device_client.disconnect()
    sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())
