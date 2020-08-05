import socket
import time
import binascii
from network import LTE
import os
import machine

print("sys", os.uname().sysname)
print("unique_id", binascii.hexlify(machine.unique_id()))
print("release", os.uname().release)


APN="spe.inetd.vodafone.nbiot"
APN=""
BAND=20
BAND=""
disconnect_detach = True

def sleep(s):
    print("sleep(", s, ")", end="")
    while s > 0:
        print(".", end="")
        time.sleep(1)
        s -= 1
    print("")

def disconnect(lte):
    if ( lte.isconnected() ):
        print("disconnect ", end="")
        t = time.time()
        lte.disconnect()
        print(" disconnected after", time.time() - t, "seconds")

def connect(lte):
    disconnect(lte)
    print("connect ", end="")
    t = time.time()
    lte.connect()
    while not lte.isconnected():
        print(".", end="")
        time.sleep(0.25)
    print(" connected after", time.time() - t, "seconds")
    try:
        # older sqns fw does not support pppsuspend
        ifconfig_suspend(lte)
    except:
        pass


def detach(lte):
    disconnect(lte)
    if ( lte.isattached() ):
        print("detach")
        # try:
        lte.detach()
        #except Exception as ex:
        #    print("detach failed:", ex)

def ifconfig(lte):
    for attempt in range(0,3):
        try:
            print(lte.send_at_cmd('AT+CGCONTRDP=1'))
            # '\r\n+CGCONTRDP: 1,5,"spe.inetd.vodafone.nbiot.mnc028.mcc901.gprs","10.175.213.177.255.255.255.255","","10.105.16.254","10.105.144.254","","",,,1430\r\n\r\nOK\r\n'
            # lte.send_at_cmd('AT+CGDCONT?')
            # '\r\n+CGDCONT: 1,"IP","spe.inetd.vodafone.nbiot",,,,0,0,0,0,0,0,1,,0\r\n\r\nOK\r\n'
            print(lte.send_at_cmd('AT!="ifconfig"'))
            return
        except Exception as ex:
            print("ifconfig Exception:", ex)
    raise Exception("Could not ifconfig")

def ifconfig_suspend(lte):
    lte.pppsuspend()
    ifconfig(lte)
    lte.pppresume()

def attach(lte):
    detach(lte)
    print("attach ", end="")
    t = time.time()
    if BAND:
        lte.attach(band=BAND, apn=APN) #, type=LTE.IP)
    else:
        lte.attach()
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

def lte_connect():
    print("init")
    t = time.time()
    try:
        # try to detach, in case the script was Ctrl-C-ed and is rerun
        detach(lte)
        print("detached")
    except:
        pass

    lte = LTE() # debug=True) # carrier=None, cid=1)
    # print("imei", lte.imei())
    attach(lte)
    # lte.init(debug=True)
    connect(lte)
    # host = 'google.com'
    # print(host, socket.getaddrinfo(host,80))
    return True


############################# main ##########################
if __name__ == "__main__":
    lte_connect()

    if False:
        disconnect(lte)
        detach(lte)
