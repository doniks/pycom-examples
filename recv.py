#!/usr/bin/env python3
import socket
import struct
import time
import binascii

port = 5555
use = "TCP"
use = "UDP"
count = 10000000 # how many packets to receive

# configure IP of local host
try:
    # script is running on the device
    import machine
    import os
    uid = binascii.hexlify(machine.unique_id())
    print(os.uname().sysname, uid, "recv.py")
    host = '192.168.0.107' # board via eth
    # host = '10.0.91.181'
    #host = '192.168.0.1' # board as wifi AP
    #host = '192.168.178.74' # board via peter's wlan router
except:
    # script is running on the laptop
    print("Laptop", "recv.py")
    # host = '127.0.0.1'
    # host = '10.0.103.1'
    host = '192.168.178.81' # dell laptop in peter's apartment

print(host, port)

try:
    s.close()
except:
    pass

seq = None

def recv(s):
    global seq
    try:
        # print("recv", t)
        M = s.recv(4000)
        print("recieved", len(M), binascii.hexlify(M), end=' ')
        newseq = M[0]
        if newseq == seq + 1:
            print("next", end=' ')
        else:
            print("start", end=' ')
        print(newseq)
        seq = newseq
        time.sleep(0.001)
        return True;
    except Exception as e:
        # maybe there was nothing sent, and recv timed out
        print("could not recv:", e)
        seq = None
    return False



if use == "UDP":
    print("UDP")
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("bind socket")
    s.bind((host, port))
    print("bound")
    t = 5
    s.settimeout(t)
    ok = 0
    notok = 0
    for c in range(count):
        if recv(s):
            ok += 1
        else:
            notok += 1
        # if ok % 100 == 0:
        #     print("received", ok, "so far")
        # if notok >= 5:
        #     print("stop after", notok, "failed attempts")
        #     break
    print("received", ok, "in total. had", notok, "failed attempts")
    s.close()
else:
    #FIXME
    print("TCP")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    while True:
        # now our endpoint knows about the OTHER endpoint.
        print("accept")
        clientsocket, address = s.accept()
        print(address)
        recv(clientsocket)
        # for x in range(0,10):
        # while True:
        #     # s.settimeout(20)
        #     r = clientsocket.recv(256)
        #     if len(r):
        #         print(r)
        #         print("\n")
        #     #     P = r[:10]
        #     #     print(P)
        #     #     p = int.from_bytes(P, "big")
        #     #     # p = struct.unpack('<10i',P)[0]
        #     #     print(p, len(r), r[10:])
        #     # except Exception as e:
        #     #     print(e)
        #     #     clientsocket.close()
        #     #     break
        # clientsocket.close()

print("end")
