#!/usr/bin/env python3
import socket
import binascii
import time
import struct

port = 6661
#use = "TCP"
use = "UDP"
size = 2000 # how many bytes to send in one packet
count = 3 # how many packets to send

# configure IP of remote host
try:
    # script is running on the device
    import machine
    import os
    uid = binascii.hexlify(machine.unique_id())
    print(os.uname().sysname, uid, "send.py")
    host = '10.0.103.1'
except:
    # script is running on the laptop
    print("Laptop", "send.py")
    host = "10.0.33.143"

#####################
print(host, port)

payload = bytes([])
for x in range(size):
    payload += bytes([x % 256])
print(binascii.hexlify(payload))

try:
    s.close()
except:
    pass

def send(s, c=0):
    C = c % 256
    # M = bytes([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, C])
    M = bytes([C]) + payload
    print("send", binascii.hexlify(M))
    s.send(M)
    print("sent")
    S = 0.1 # sufficient for pyeth board to keep up over eth
    #S = 0.01 # too fast
    # S = 0.2
    time.sleep(S)


def udp():
    print("UDP")
    # don't send size > 75 over wifi
    # size=29 seems to be the max that gets through over eth
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # , socket.IPPROTO_UDP)
    s.connect((host, port))
    print("connected")
    try:
        for c in range(count):
            send(s, c)
    except Exception as e:
        # maybe other side closed the socket
        print("could not send", e)
    s.close()


# else:
#     #FIXME
#     print("TCP")
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     print("connect socket")
#     s.connect(ap)
#     print("connected")
#     M = bytes([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
#     print(M)
#     s.send(M)
#     time.sleep(0.0001)
#     s.close()
#     t = (time.time() - start) / 1000
#     print("up(", packets, size, proto, ") -- done", l, t, l/t)
#
# print("end")

if __name__ == "__main__":
    udp()
