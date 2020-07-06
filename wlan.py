import machine
import time
import os
from network import WLAN
import socket
import binascii

known_nets_dict = {
    # 'ssid2': {'pwd': 'password2', 'wlan_config':  ('10.0.0.114', '255.255.0.0', '10.0.0.1', '10.0.0.1')}, # (ip, subnet_mask, gateway, DNS_server)
    'MySSID': {'pwd': 'MyPASSWORD'},
}

connection = ""
IP = ""

def wlan_connect():
    global connection, IP
    print("Initialise WiFi")
    wlan = WLAN() # antenna=WLAN.EXT_ANT)
    wlan.hostname(binascii.hexlify(machine.unique_id()) + "." + os.uname().sysname + "." + "wlan")
    # print("ap_mac", binascii.hexlify(wlan.mac().ap_mac))
    # print("sta_mac", binascii.hexlify(wlan.mac().sta_mac))
    if ( wlan.mode() == WLAN.AP ):
        print("switch from AP to STA_AP")
        wlan.mode(WLAN.STA_AP)
    original_ssid = wlan.ssid()
    original_auth = wlan.auth()

    if wlan.isconnected():
        print("currently connected ... disconnecting")
        wlan.disconnect()
        while wlan.isconnected():
            time.sleep_ms(200)

    print("Scanning for wifi networks")
    available_nets_list = wlan.scan()
    available_ssids_set = frozenset([n.ssid for n in available_nets_list])
    known_ssids_set = frozenset([key for key in known_nets_dict])
    # make the intersection
    usable_ssids_set = available_ssids_set & known_ssids_set
    print("available:", len(available_ssids_set))
    print("known:", len(known_ssids_set))
    print("usable:", len(usable_ssids_set))
    if (len(usable_ssids_set) == 0):
        print("No usable network found")
        print("known", known_ssids_set)
        print("available", available_ssids_set)
    else:
        try:
            net_to_use = usable_ssids_set.pop()
            print("net_to_use", net_to_use)
            net_properties = known_nets_dict[net_to_use]
            pwd = net_properties['pwd']
            sec = [e.sec for e in available_nets_list if e.ssid == net_to_use][0]
            if 'wlan_config' in net_properties:
                wlan.ifconfig(config=net_properties['wlan_config'])
            print("connect", net_to_use, sec, pwd)
            wlan.connect(net_to_use, (sec, pwd))
            ct = 0;
            while not wlan.isconnected():
                ct += 1
                # print(".", end="")
                machine.idle()  # save power while waiting
                time.sleep_ms(200)
            print("Connected", ct) # , "(", wlan.ifconfig(), ")")
            connection = "WLAN"
            ct = 0
            IP = wlan.ifconfig()[0]
            while IP == "0.0.0.0":
                ct += 1
                machine.idle()
                IP = wlan.ifconfig()[0]
                time.sleep_ms(100)
            print("Connected to", net_to_use,
                  "with IP address:", IP, ct)
            host = "detectportal.firefox.com"
            print(host, socket.getaddrinfo(host, 80)[0][4][0])
            return True

        except Exception as e:
            print("Error while trying to connect to Wlan:", e)
            return False

def wlan_deinit():
    wlan.deinit()

if __name__ == "__main__":
    import binascii
    import os
    uid = binascii.hexlify(machine.unique_id())
    name = os.uname().sysname.lower() + '-' + uid.decode("utf-8")[-4:]
    print(os.uname().sysname, uid, name, "main.py")
    print("sys", os.uname().sysname)
    print("unique_id", binascii.hexlify(machine.unique_id()))
    wlan_connect()
