from network import WLAN
import machine
import socket
import ssl
import time

start = time.time()

wlan = WLAN(mode=WLAN.STA)

# fill in !!!
ssid = 'XXX'
passwd = 'XXX'
sec    = 3

do_scan = False

def connect(ssid, auth):
    print("Connecting ...", end="")
    wlan.connect(ssid, auth, timeout=5000)
    while not wlan.isconnected():
        time.sleep_ms(200)
        print(".", end="")
    print('WLAN connection succeeded after', time.time() - start, "seconds")

if wlan.isconnected():
    print("Already connected")
else:
    if do_scan:
        print("Scanning ...")
        nets = wlan.scan()
        for net in nets:
            if net.ssid == ssid:
                print('Network', ssid, 'found after', time.time() - start, 'seconds')
                connect(net.ssid, auth=(net.sec, passwd))
                break
    else:
        connect(ssid, auth=(sec, passwd))
        pass

print("WLAN connected:", wlan.ssid(), wlan.ifconfig() )
print(wlan.ifconfig()[0] )

# s = socket.socket()
# ss = ssl.wrap_socket(s)
# ss.connect(socket.getaddrinfo('www.google.com', 443)[0][-1])
host = "detectportal.firefox.com"
ip = socket.getaddrinfo(host, 80)[0][4][0]
print(host, ip) # 185.27.16.8
