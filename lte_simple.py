import socket
import ssl
import time
from network import LTE
import binascii
import machine
import os

uid = binascii.hexlify(machine.unique_id())
name = os.uname().sysname.lower() + '-' + uid.decode("utf-8")[-4:]
print(name, "lte_simple.py")

print("init")
t = time.time()
lte = LTE(debug=True)

# lte.send_at_cmd('AT+COPS=?')
# '\r\n+COPS: (2,"Vodafone@","VF","20404",9),,(0,1,2,3,4),(0,1,2)\r\n\r\nOK\r\n'

print("attach")
#### amarisoft (the "anritsu" or the "blank" sim)
# lte.attach()
# lte.attach(band=20)
# lte.attach(band=20)
# lte.attach(apn="Internet")
#### pycom vodafone
# lte.attach(apn="pycom.io", band=20)
# lte.attach(apn="pycom.io")
#### vodafone
# lte.attach()
# lte.attach(cid=1, band=20, apn="spe.inetd.vodafone.nbiot", type=LTE.IP)
# lte.attach(band=20, apn="spe.inetd.vodafone.nbiot")
#### Jersey Telecom
lte.attach(band=8)

time.sleep(10)
while not lte.isattached():
    print(".", end="")
    time.sleep(10)
print("\nattached")

print("connect")
lte.connect() # legacy=True)
while not lte.isconnected():
    print(".", end="")
    time.sleep(2)
print("\nconnected")

host = "pycom.io"
print(host, socket.getaddrinfo(host, 443)[0][-1][0])

if False:
    # print("disconnect")
    # lte.disconnect()

    print("detach")
    lte.detach()
else:
    print("deinit")
    lte.deinit()
