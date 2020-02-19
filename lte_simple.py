import socket
import ssl
import time
from network import LTE

print("init")
t = time.time()
lte = LTE()


print("attach", end="")
t = time.time()
#### amarisoft (the "anritsu" or the "blank" sim)
lte.attach(band=20)
# lte.attach(apn="Internet")
#### pycom vodafone
# lte.attach(apn="pycom.io", band=20)
#### vodafone
# lte.attach(band=20, apn="spe.inetd.vodafone.nbiot")
# lte.attach(cid=1, band=20, apn="spe.inetd.vodafone.nbiot", type=LTE.IP)

while not lte.isattached():
    print(".", end="")
    time.sleep(1)
print(time.time() - t, "seconds")


print("connect", end="")
t = time.time()
lte.connect()       # start a data session and obtain an IP address
while not lte.isconnected():
    print(".", end="")
    time.sleep(1)
print(time.time() - t , "seconds")

print(socket.getaddrinfo('www.google.com', 443))

print("disconnect")
lte.disconnect()

print("dettach")
lte.dettach()
