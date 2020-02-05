import socket
import ssl
import time
from network import LTE

print("init")
lte = LTE()
print("attach", end="")
lte.attach(apn="Internet")
while not lte.isattached():
    print(".", end="")
    time.sleep(1)
print("")


print("connect", end="")
lte.connect()       # start a data session and obtain an IP address
while not lte.isconnected():
    print(".", end="")
    time.sleep(1)
print()

print(socket.getaddrinfo('www.google.com', 443))

print("disconnect")
lte.disconnect()

print("dettach")
lte.dettach()
