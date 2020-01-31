import socket
import ssl
import time
from network import LTE

# choose nbiot or catm1
use_nbiot = True
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

def dettach():
    disconnect()
    if ( lte.isattached() ):
        print("dettach")
        # try:
        lte.dettach()
        #except Exception as ex:
        #    print("dettach failed:", ex)

def attach():
    dettach()
    print("attach ", end="")
    t = time.time()
    if use_nbiot:
        lte.attach(band=20, apn="spe.inetd.vodafone.nbiot")
    else:
        lte.attach()
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
    dettach()
except:
    pass
lte = LTE()
print("imei", lte.imei())

ct = 0
while True:
    print(ct)
    attach()
    connect()
    ping()
    ct += 1
    sleep(60)

if disconnect_detach:
    dettach()
