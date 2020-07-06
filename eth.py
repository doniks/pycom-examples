from network import ETH
import time

def eth_connect(ip_mask_gw_dns=None):
    eth = ETH(hostname=binascii.hexlify(machine.unique_id()))
    eth.hostname(binascii.hexlify(machine.unique_id()) + "." + os.uname().sysname + "." + "eth")
    print("mac", binascii.hexlify(eth.mac()))
    # (ip, subnet_mask, gateway, DNS_server)
    # eth.ifconfig(config=('192.168.0.107', '255.255.255.0', '192.168.0.1', '192.168.0.1')) # use this!
    # eth.ifconfig(config=('192.168.0.107', '255.255.255.0', '192.168.0.1', '8.8.8.8')) # doesn't work?
    #### eth.ifconfig(config=('10.107.107.107', '255.0.0.0', '10.0.103.1', '10.0.103.1'))
    if ip_mask_gw_dns:
        eth.ifconfig(config=ip_mask_gw_dns)
    if eth.isconnected():
        print("already connected, deinit first")
        eth.deinit()
        while eth.isconnected():
            # wait for connection to go down
            pass
            # print(eth.isconnected())
        print("eth re-init")
        eth.init()
    print("connecting eth ...")
    i = 0
    for i in range(0,50):
        if eth.isconnected():
            print("... eth connected")
            break
        else:
            print(i, "waiting for connection", eth.ifconfig()) #, end=" ")
            time.sleep(0.5)
        i+=1

    if eth.isconnected():
        print("hostname", eth.hostname())
        print("isconnected", eth.isconnected())
        print("ifconfig", eth.ifconfig()) # (ip, subnet_mask, gateway, DNS_server)
        return True
    else:
        print("FAILED to connect eth")
        return False

def eth_ifconfig():
    from network import ETH
    eth = ETH()
    print("ifconfig", eth.ifconfig()) # (ip, subnet_mask, gateway, DNS_server)

def eth_disconnect():
    from network import ETH
    eth = ETH()
    eth.deinit()

if True: # __name__ == "__main__":
    import os
    import machine
    import binascii
    import pycom
    id = binascii.hexlify(machine.unique_id())
    print(os.uname().sysname, id, "eth.py")
    pycom.heartbeat(False)
    pycom.rgbled(0xffcc00) # yellow
    # config=('192.168.0.1', '255.255.255.0', '192.168.0.1', '192.168.0.1')
    # if id == b'840d8e120b30':
    #     print("I'm the other guy")
    config = ('192.168.0.107', '255.255.255.0', '192.168.0.1', '192.168.0.1')
    if not eth_connect(config):
        import machine
        machine.reset()
    pycom.rgbled(0x00001a) # faint blue
