import socket
import ssl
import time
from network import LTE

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
    lte.attach(band=BAND, apn=APN)
    while not lte.isattached():
        print(".", end="")
        time.sleep(0.25)
    print(" attached after", time.time() - t, "seconds")

def ping():
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
    # needed if we Ctrl-C the script and want to rerun
    detach()
except:
    pass
lte = LTE()
print("imei", lte.imei())
attach()
connect()

ct = 0
#while True:
for i in range(0, 1):
    print(ct)
    ping()
    ct += 1
    sleep(60)

if disconnect_detach:
    detach()
