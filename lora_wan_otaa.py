# https://docs.pycom.io/gettingstarted/registration/lora/
from network import LoRa
import socket
import time
import ubinascii

# Initialise LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

device_eui = ubinascii.hexlify(lora.mac()).upper().decode('utf-8')
print(device_eui)


# Application EUI and identifies what application your device is connecting to
app_eui = ubinascii.unhexlify('XXX') # fill in
# Application Key is a shared secret key unique to your device to generate the session keys that prove its identity to the network.
app_key = ubinascii.unhexlify('XXX') # fill in

# join a network using OTAA (Over the Air Activation)
print("Joining...")
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(2.5)
    print('Not yet joined...')
print('Joined!')

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

# make the socket blocking
# (waits for the data to be sent and for the 2 receive windows to expire)
s.setblocking(True)

# send some data
print("sending ...")
s.send(bytes([0x01, 0x02, 0x03]))

# make the socket non-blocking
# (because if there's no data received it will block forever...)
s.setblocking(False)

# get any data received (if any...)
data = s.recv(64)
print("received:(", data, ")")
