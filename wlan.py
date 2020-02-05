from network import WLAN
import machine
import socket
import ssl
import time

wlan = WLAN(mode=WLAN.STA)

# fill in !!!
ssid = 'XXX'
passwd = 'XXX'

if wlan.isconnected():
    print("Already connected")
else:
    print("Scanning ...")
    nets = wlan.scan()
    for net in nets:
        if net.ssid == ssid:
            print('Network', ssid, 'found. Connecting ...')
            wlan.connect(net.ssid, auth=(net.sec, passwd), timeout=5000)
            while not wlan.isconnected():
                #machine.idle() # save power while waiting
                time.sleep_ms(200)
                print(".", end="")
            print('WLAN connection succeeded!')
            break

print("WLAN connected:", wlan.ssid(), wlan.ifconfig() )
print(wlan.ifconfig()[0] )

# s = socket.socket()
# ss = ssl.wrap_socket(s)
# ss.connect(socket.getaddrinfo('www.google.com', 443)[0][-1])
host = "detectportal.firefox.com"
ip = socket.getaddrinfo(host, 80)[0][4][0]
print(host, ip) # 185.27.16.8
