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

# 1. get the device eui and name (below)
# 2. register device on TTN website https://console.thethingsnetwork.org with this
#    * device eui and
#    * use name for Device ID
# 3. create a config block below using
#    * name
#    * application EUI
#    * App Key
# 4. run this script and check on TTN website that the device shows up



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

name = os.uname().sysname.lower() + '-' + uid.decode("utf-8")[-4:]
print("name", name)

config = dict()

config["lopy4-8454"] = {
    "app_eui": binascii.unhexlify('70B3D57ED00299F9'),
    "app_key": binascii.unhexlify('82B2BF49C69C4A599010200D813629F1'),
}

config["lopy4-6d34"] = {
    "app_eui": binascii.unhexlify('70B3D57ED00299F9'),
    "app_key": binascii.unhexlify('3FCB2D364750F3F9F4D757A63D0247A8'),
}

config["fipy-4624"] = {
    "app_eui": binascii.unhexlify('70B3D57ED00299F9'), # the second half of this is shown by the gateway as 'mote' during join, ie D00299F9. during sending 'mote' refers to the "Device Address", seemingly a new code after every join
    "app_key": binascii.unhexlify('2363DB43D11C47B442C55A4A55BEA878'),
}

config["fipy-2b40"] = {
    "app_eui": binascii.unhexlify('70B3D57ED00299F9'),
    "app_key": binascii.unhexlify('C63041521BE4AEB32760F4C985A0C6D4'),
}

config["lopy-32a8"] = {
    # doesn't work .... prototype lopy? not even sure it's 1 or 4 ...
    "app_eui": binascii.unhexlify('70B3D54999CAD88C'),
    "app_key": binascii.unhexlify('C5F8AD51FB6D6F528F37A2AF9B73B1EE'),
}

config["lopy4-835c"] = {
    "app_eui": binascii.unhexlify('70B3D57ED00299F9'),
    "app_key": binascii.unhexlify('B7B3CB9BE083C4A002F9DF97E8411333'),
}


c = config[name]
print("app_eui:" + binascii.hexlify(c["app_eui"]).decode())
print("app_key:" + binascii.hexlify(c["app_key"]).decode())


# join a network using OTAA (Over the Air Activation)
print("Joining...")
lora.join(activation=LoRa.OTAA, auth=(c["app_eui"], c["app_key"]), timeout=0)

# wait until the module has joined the network
start_join = time.time()
while not lora.has_joined():
    time.sleep(2.5)
    print('.', end="")
print('Joined after', time.time() - start_join)

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)


packets_to_send = 10
sleep_between_pkts = 30
n = 0
while n < packets_to_send:
    # make the socket blocking
    # (waits for the data to be sent and for the 2 receive windows to expire)
    s.setblocking(True)
    b = bytes([0xaa, 0xaa, n % 256])
    print("sending:", binascii.hexlify(b))
    # send some data
    s.send(b)

    time.sleep(1)

    s.setblocking(False)
    data = s.recv(64)
    if data:
        print("received:", binascii.hexlify(data))

    n += 1
    if n < packets_to_send:
        time.sleep(sleep_between_pkts)

deepsleep_s = 1800
print("deepsleep", deepsleep_s, "s")
machine.deepsleep(deepsleep_s * 1000)
