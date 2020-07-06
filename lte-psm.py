from network import LTE
import time
import socket
import machine
import pycom

def attach():
    start = time.time()
    if lte.isattached():
        print("already attached")
    else:
        print("attach")
        # lte.attach(band=20, apn="the.apn.to.be.used.with.your.simcard")
        lte.attach()
        while not lte.isattached():
            time.sleep(1)
    print("attached after", time.time() - start, "seconds")
    print(lte.psm())

def connect():
    print("connect")
    start = time.time()
    lte.connect()
    while not lte.isconnected():
        time.sleep(0.5)
    print("connected after", time.time() - start, "seconds")

def http_get(url = 'http://detectportal.firefox.com/'):
    _, _, host, path = url.split('/', 3)
    for attempt in range(5):
        try:
            addr = socket.getaddrinfo(host, 80)[0][-1]
            print(time.time(), "dns[{}] success:".format(attempt), host, addr)
            connected = True
            break
        except Exception as e:
            print(time.time(), "dns[{}] failure:".format(attempt), host, e)
            time.sleep(0.5)
    if not connected:
        raise Exception(time.time(), "dns failed", attempt, "times")

    print(host, addr[0])
    s = socket.socket()
    s.connect(addr)
    print("sending")
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    s.close()

# main
lte = LTE(
 # period
 psm_period_value=1, psm_period_unit=LTE.PSM_PERIOD_1M, # 1 minute
 # psm_period_value=1, psm_period_unit=LTE.PSM_PERIOD_1H, # 1 hour

 # active
 psm_active_value=5, psm_active_unit=LTE.PSM_ACTIVE_2S # 10s
 )
print(lte.psm())
attach()
connect()
http_get()

print("deinit")
lte.deinit(detach=False, reset=False)

print("deepsleep")
machine.deepsleep(50 * 1000) # 50 seconds
# machine.deepsleep(55 * 60 * 1000) # 55m
