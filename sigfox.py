import machine
import os
from binascii import hexlify
uid = hexlify(machine.unique_id())
name = os.uname().sysname.lower() + '-' + uid.decode("utf-8")[-4:]
print(name, "sigfox.py")

from network import Sigfox
import socket
import pycom
import time


# FIRST TIME:
# if you haven't set up your device follow these steps:
# * go here https://backend.sigfox.com/activate
# * login
#   (country will be autoselected once you are logged in)
# * get device ID and PAC (see below) and add them on the website
# -> if it fails with "We could not find a DevKit matching your ID/PAC"
#    This (usually? always?) means someone has already registered this device
#    It might be you! So double check with link below
# -> if it is ok it will say "Pycom Go Invent DevKit available for activation"
# * select a purpose, fill in a description and click on next
# -> if it is successful it will say
#    Congratulations ! Your device .. has been successfully registered on Sigfox Cloud.
#    To finalize its activation your device must send a first frame. After this first message, your device will be able to send a maximum of 140 messages per day during 1 year
# * go to https://backend.sigfox.com/device/list
# * find the device based on the ID
# * left click on the Name of the device
# * Edit
# * Change the name to something useful, like fipy-4HEX as printed above
# * configure downlink:
#   * go to Device - List
#   * click on Device type
#   * Edit
#   * Change the name to something useful, like "fipy-beef direct DL"
#   * Downlink mode: DIRECT
#   * Downlink data in hex: {time}0000{rssi}
# ( see also: https://docs.pycom.io/gettingstarted/registration/sigfox )

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
# downlink = False
count = 100
sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1)
print("ID", hexlify(sigfox.id()))
if False:
    # one time PAC to be used when initially registering device
    print("PAC", hexlify(sigfox.pac()))


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
    pycom.rgbled(0x111100)
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
            print("send", hexlify(m), "and wait for reception")
            s.send(m)
            pycom.rgbled(0x000011)
            ct_send += 1
            print("receive ...")
            x = s.recv(64)
            pycom.rgbled(0x001100)
            # {time}0000{rssi} 4,2,2 bytes
            t = x[0:4]
            z = x[4:6]
            rssi = x[6:8]
            # b'5f59ebe4' b'0000' b'ff75'
            # b'5f59ec42' b'0000' b'ff72'
            # TODO: how to convert
            print("received=", hexlify(x), " time=", hexlify(t), " zero=", hexlify(z), " rssi=", hexlify(rssi), sep='')
            print("rssi", sigfox.rssi())
            ct_recv += 1
        else:
            s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False) # uplink only
            m = i + bytes([0x01]) + g + r
            print("send", hexlify(m))
            s.send(m)
            pycom.rgbled(0x000011)
            ct_send += 1
    except Exception as e:
        pycom.rgbled(0x110000)
        print("failed", e)
        ct_fail += 1
    time.sleep(2)
    print("ct=", ct, "(send,recv,fail)=", ct_send, ct_recv, ct_fail)



print("done (send,recv,fail)=", ct_send, ct_recv, ct_fail)

# for downlink
# a simple test is to configure the DEVICE TYPE on the sigfox website for
# Downlink mode: DIRECT
# Downlink data: {tapId}0000{rssi}

# a more meaningful test would involve an actual web call back .... tbd
