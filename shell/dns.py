import time

def dns(host="mqtt.pybytes.pycom.io", attempts=1):
    import socket
    import os

    connected = False
    for attempt in range(0,attempts):
        try:
            print(time.time(), "dns[{}] success:".format(attempt), host, socket.getaddrinfo(host, 80))
            connected = True
            break
        except Exception as e:
            print(time.time(), "dns[{}] failure:".format(attempt), host, e)
            time.sleep(2)
    if not connected:
        raise Exception(time.time(), "dns lookup failed")



def _dns_test(hostname, attempts=3):
    t = time.ticks_ms()
    dns(hostname, attempts=attempts)
    print('hostname', hostname, 'seconds:', (time.ticks_ms() - t) / 1000 )

def dns_test(index=None, attempts=3):
    if index is not None:
        name = ord('a') + index
        _dns_test(chr(name)+'.root-servers.net', attempts)
    else:
        for name in range(ord('a'), ord('n')):
            _dns_test(chr(name)+'.root-servers.net', attempts)

if __name__ == "__main__":
    import binascii
    import machine
    print(os.uname().sysname, binascii.hexlify(machine.unique_id()), "dns.py")
    # dns('www.pycom.io')
    dns('pybytes.pycom.io')
    # dns_test(attempts=100)
