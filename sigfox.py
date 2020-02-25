from network import Sigfox
import socket
import machine
import ubinascii
import pycom
import time
import os

downlink = True


print("sys", os.uname().sysname)

##################################################
# init
sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1)
print("id", ubinascii.hexlify(sigfox.id()))
print("pac", ubinascii.hexlify(sigfox.pac()))
s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)
s.setblocking(True)
##################################################
# blink
import pycom
pycom.heartbeat(False)
for i in range(0, 5):
    pycom.rgbled(0x220022)
    time.sleep_ms(100)
    pycom.rgbled(0x000000)
    time.sleep_ms(100)

##################################################
# message
i = sigfox.id()[3].to_bytes(1, "big")
key = "sfx_ct" # max 15 characters long
ct = 0
try:
    ct = pycom.nvs_get(key)
    ct += 1
except:
    pass
pycom.nvs_set(key, ct)
c = ct.to_bytes(1, "big")
r = machine.rng().to_bytes(1, "big")




##################################################
# transmit​
# [i][c][u][r]
# i ... last byte of sigfox id
# c ... counter
# u ... uplink=1, downlink=2
# r ... random byte
if downlink:
    s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, True) # up and downlink
    m = i + c + bytes([0x02]) + r
    print("send/receive", ubinascii.hexlify(m))
    s.send(m)
    x = s.recv(64)
    print("received", ubinascii.hexlify(x))
    print("rssi", sigfox.rssi())
else:
    s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False) # uplink only
    m = i + c + bytes([0x01]) + r
    print("send", ubinascii.hexlify(m))
    s.send(m)


# go to https://backend.sigfox.com
# DEVICE
# click on the Id of this device
# MESSAGES
# you should see the list of messages

# for downlink
# a simple test is to configure the DEVICE TYPE on the sigfox website for
# Downlink mode: DIRECT
# Downlink data: {tapId}0000{rssi}

# a more meaningful test would involve an actual web call back .... tbd
