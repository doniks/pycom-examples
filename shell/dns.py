
def dns(host='pycom.io', attempts=1):
    import socket
    import time
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
        raise Exception(time.time(), "no connection")

if __name__ == "__main__":
    import binascii
    import machine
    print(os.uname().sysname, binascii.hexlify(machine.unique_id()), "dns.py")
    dns('www.pycom.io')
