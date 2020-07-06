# https://docs.pycom.io/gettingstarted/registration/lora/
from network import LoRa
import socket
import time
import binascii
import os
import machine

uid = binascii.hexlify(machine.unique_id())
id = int(uid,16)
print(os.uname().sysname, uid, id, "lora_wan_otaa.py")

# 1. get the device eui (below)
# 2. register device on TTN website https://console.thethingsnetwork.org with this device eui
# 3. create a config block below
# 4. fill with app_eui and app_key from TTN
# 5. run this script and check on TTN website that the device shows up



# https://docs.pycom.io/gettingstarted/registration/lora/ttn/
# https://console.thethingsnetwork.org/applications/hello13245/devices


# Initialise LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
#   Asia           = LoRa.AS923
#   Australia      = LoRa.AU915
#   Europe         = LoRa.EU868
#   United States  = LoRa.US915
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

# for dr/sf see here
# https://forum.pycom.io/topic/6103/set-spreading-factor/16

device_eui = binascii.hexlify(lora.mac()).upper().decode('utf-8')
print("device_eui", device_eui)


config = dict()

c = config[id]
print("app_eui:" + binascii.hexlify(c["app_eui"]).decode())
print("app_key:" + binascii.hexlify(c["app_key"]).decode())


# join a network using OTAA (Over the Air Activation)
print("Joining...")
lora.join(activation=LoRa.OTAA, auth=(c["app_eui"], c["app_key"]), timeout=0)

# wait until the module has joined the network
start_join = time.time()
while not lora.has_joined():
    time.sleep(1)
    print('.', end="")
print('Joined after', time.time() - start_join)

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)



m = 0
while m < 1:
    # make the socket blocking
    # (waits for the data to be sent and for the 2 receive windows to expire)
    s.setblocking(True)
    b = bytes([0xaa, 0xaa, m % 256])
    print("sending:", binascii.hexlify(b))
    # send some data
    s.send(b)

    time.sleep(1)

    s.setblocking(False)
    data = s.recv(64)
    if data:
        print("received:", binascii.hexlify(data))

    time.sleep(5)
    m += 1
