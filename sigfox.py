from network import Sigfox
import socket
import machine
import binascii
import pycom
import time
import os

uid = binascii.hexlify(machine.unique_id())
name = os.uname().sysname.lower() + '-' + uid.decode("utf-8")[-4:]
print(name, "sigfox.py")

# FIRST TIME:
# if you haven't set up your device follow these steps:
# * go here https://backend.sigfox.com/activate
# * login
#   (country will be autoselected when you are logged in)
# * paste device ID and PAC (see below)
# -> if it is ok it will say "DevKit available for activation"
# -> if it fails with "We could not find a DevKit matching your ID/PAC", then I think someone has already registered this device, it might be you! so double check with link below
# * click blabla continue ...
# -> if it is successful ... Congratulations ! Your device .. has been successfully registered on Sigfox Cloud. To finalize its activation your device must send a first frame. After this first message, your device will be able to send a maximum of 140 messages per day during 1 year
# * go to https://backend.sigfox.com/device/list
# * find the device based on Id
# * click on the Name of the device
# * Edit and change it to something useful, like fipy-4HEX as printed above
# ( background: https://docs.pycom.io/gettingstarted/registration/sigfox )

# EVERY TIME:
# * go here https://backend.sigfox.com/device/list
# * click on your device Id in the list
# * click on Messages
# * run this script
# -> see a message show up in the list
# -> see a "received .... " line in the REPL



##################################################
# init

downlink = True
count = 10
sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1)
print("ID", binascii.hexlify(sigfox.id()))
print("PAC", binascii.hexlify(sigfox.pac()))


s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)
s.setblocking(True)

##################################################
# blink
if pycom.heartbeat():
    pycom.heartbeat(False)
for i in range(0, 5):
    pycom.rgbled(0x220022)
    time.sleep_ms(100)
    pycom.rgbled(0x000000)
    time.sleep_ms(100)

##################################################
# message format:
# [i][u][r][c][g]
# i ... last byte of sigfox id
# u ... uplink=1, downlink=2
# r ... random byte
# c ... counter
# g ... global counter based on nvs variable

i = sigfox.id()[-1].to_bytes(1, "big")
ct_send = 0
ct_recv = 0
ct_fail = 0

for ct in range(count):
    c = (ct % 256).to_bytes(1, "big")
    key = "sfx_ct"
    gct = 0
    try:
        gct = pycom.nvs_get(key)
        gct += 1
    except:
        pass
    gct = gct % 256
    pycom.nvs_set(key, gct)
    g = gct.to_bytes(1, "big")
    r = machine.rng().to_bytes(1, "big")

    try:
        if downlink:
            s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, True) # up and downlink
            m = i + bytes([0x02]) + c + g + r
            print("send", binascii.hexlify(m), "and wait for reception")
            s.send(m)
            ct_send += 1
            x = s.recv(64)
            print("received", binascii.hexlify(x))
            print("rssi", sigfox.rssi())
            ct_recv += 1
        else:
            s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False) # uplink only
            m = i + bytes([0x01]) + g + r
            print("send", binascii.hexlify(m))
            s.send(m)
            ct_send += 1
    except Exception as e:
        print("failed", e)
        ct_fail += 1


print("done (send,recv,fail)=", ct_send, ct_recv, ct_fail)

# for downlink
# a simple test is to configure the DEVICE TYPE on the sigfox website for
# Downlink mode: DIRECT
# Downlink data: {tapId}0000{rssi}

# a more meaningful test would involve an actual web call back .... tbd
