import socket
# import ssl
import time
import binascii
from network import LTE
import os
import machine

print("sys", os.uname().sysname)
print("unique_id", binascii.hexlify(machine.unique_id()))
print("release", os.uname().release)


APN="spe.inetd.vodafone.nbiot"
BAND=20
disconnect_detach = True

def sleep(s):
    print("sleep(", s, ")", end="")
    while s > 0:
        print(".", end="")
        time.sleep(1)
        s -= 1
    print("")

def disconnect():
    if ( lte.isconnected() ):
        print("disconnect ", end="")
        t = time.time()
        lte.disconnect()
        print(" disconnected after", time.time() - t, "seconds")

def connect():
    disconnect()
    print("connect ", end="")
    t = time.time()
    lte.connect()
    while not lte.isconnected():
        print(".", end="")
        time.sleep(0.25)
    print(" connected after", time.time() - t, "seconds")

def detach():
    disconnect()
    if ( lte.isattached() ):
        print("detach")
        # try:
        lte.detach()
        #except Exception as ex:
        #    print("detach failed:", ex)

def attach():
    detach()
    print("attach ", end="")
    t = time.time()
    lte.attach(band=BAND, apn=APN, type=LTE.IP)
    while not lte.isattached():
        print(".", end="")
        time.sleep(0.25)
    print(" attached after", time.time() - t, "seconds")

def http_get(url="http://detectportal.firefox.com/"):
    print("http_get(", url, ")")
    _, _, host, path = url.split('/', 3)
    #print("host", host)
    #print("path", path)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    #print("addr", addr)
    s = socket.socket()
    #print("connect")
    s.connect(addr)
    #print("send")
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    s.settimeout(15)
    while True:
        data = s.recv(100)
        if data:
            # print("http_get: data")
            # print(str(data, 'utf8'), end='')
            pass
        else:
            break
    # print("close")
    s.close()
    # print("done")


def dns():
    print("accessing internet ", end="")
    host = "detectportal.firefox.com"
    t = time.time()
    ip = socket.getaddrinfo(host, 80)[0][4][0]
    print(" completed after", time.time() - t, "seconds")
    print(host, ip)

############################# main ##########################
print("init")
t = time.time()
try:
    # try to detach, in case the script was Ctrl-C-ed and is rerun
    detach()
    print("detached")
except:
    pass

lte = LTE(debug=False) # carrier=None, cid=1)
# print("imei", lte.imei())
attach()
lte.init(debug=False)
connect()

ct = 0
#while True:
for i in range(0, 3):
    print(ct)
    dns()
    http_get()
    ct += 1
    #sleep(60)

if disconnect_detach:
    disconnect()
    detach()
