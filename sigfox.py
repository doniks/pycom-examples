from network import Sigfox
import socket

downlink = True

​print("init")
sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1) # rcz1 Europe
print("id", ubinascii.hexlify(sigfox.id()))
print("pac", ubinascii.hexlify(sigfox.pac()))
​
print("socket")
s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)
s.setblocking(True)
​
if downlink:
    s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, True)
    print("send")
    s.send(bytes([1, 4, 12]))
    x = s.recv(64)
    print("received", ubinascii.hexlify(x))
else:
    s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)
    print("send")
    s.send(bytes([1, 4, 3]))
