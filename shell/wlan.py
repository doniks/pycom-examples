import machine
import time
import os
from network import WLAN
import socket
import binascii

wlan_mode_names = {
    WLAN.AP     : 'AP',
    WLAN.STA    : 'STA',
    WLAN.STA_AP : 'STA_AP',
}

known_nets_dict = {
    # 'ssid2': {'pwd': 'password2', 'wlan_config':  ('10.0.0.114', '255.255.0.0', '10.0.0.1', '10.0.0.1')}, # (ip, subnet_mask, gateway, DNS_server)
    'openwireless.org' : {'pwd': '', 'sec': 0},
    'wipy-wlan-349c'   : {'pwd': 'www.pycom.io', 'sec': None}
}

# w = None
connection = ""
IP = ""

ant_name = {
    WLAN.EXT_ANT : 'EXT',
    WLAN.INT_ANT : 'INT',
    # WLAN.MAN_ANT : 'MAN',
    2            : 'MAN',
}

mode_name = {
    WLAN.STA    : 'STA',
    WLAN.STA_AP : 'STA_AP',
    WLAN.AP     : 'AP',
}

bw_name = dict()
try:
    bw_name = {
        WLAN.HT20 : '20MHz',
        WLAN.HT40 : '40MHz',
    }
except:
    # fw 1.18
    pass

def wlan_init(antenna=None):
    global w
    try:
        if w is not None:
            # print('already initialized')
            if antenna is not None and w.antenna() != antenna:
                print('set antenna', antenna)
                w.antenna(antenna)
            return w
    except:
        pass
    if antenna is None:
        print("Initialise WiFi")
        w = WLAN()
    else:
        print("Initialise WiFi", ant_name[antenna])
        w = WLAN(antenna=antenna)
    try:
        w.hostname(binascii.hexlify(machine.unique_id()) + "." + os.uname().sysname + "." + "w")
        # hostname is not available in 1.18.2
    except:
        pass
    # print("ap_mac", binascii.hexlify(w.mac().ap_mac))
    # print("sta_mac", binascii.hexlify(w.mac().sta_mac))
    # original_ssid = w.ssid()
    # original_auth = w.auth()
    return w

def wlan_add_sta():
    if ( w.mode() == WLAN.AP ):
        print("switch from AP to STA_AP")
        w.mode(WLAN.STA_AP)

def wlan_isconnected():
    wlan_init()
    # try:
    #     return w.isconnected()
    # except NameError as e:
    #     print('Not initialized', e)
    #     return None
    return w.isconnected()

def wlan_waitconnected(timeout_s = 10):
    global connection
    wlan_init()
    # try:
    #     w
    # except NameError as e:
    #     print('Not initialized', e)
    #     return None

    t = time.ticks_ms()
    ct = 0;
    # while not w.isconnected():
    #     ct += 1
    #     print(".", end="")
    #     machine.idle()  # save power while waiting
    #     time.sleep_ms(200)
    print('Connecting: -', end='')
    while True:
        if w.isconnected():
            print()
            break
        if timeout_s is not None and time.ticks_ms() - t > (timeout_s * 1000):
            print("\nTimeout")
            return False
        ct += 1
        x = ct % 3
        if x == 0:
            print('\b\\', end='')
        elif x == 1:
            print('\b/', end='')
        elif x == 2:
            print('\b-', end='')
        time.sleep_ms(100)
    print("Connected in", round((time.ticks_ms() - t) /1000,1), "seconds") # , "(", w.ifconfig(), ")")
    connection = "WLAN"
    ct = 0
    IP = w.ifconfig()[0]
    while IP == "0.0.0.0":
        ct += 1
        machine.idle()
        IP = w.ifconfig()[0]
        time.sleep_ms(100)
    print("Connected to", w.ssid(), #net_to_use,
          binascii.hexlify(w.bssid()),
          "with IP address:", IP, ct)
    host = "detectportal.firefox.com"
    print(host, socket.getaddrinfo(host, 80)[0][4][0])
    return True

def wlan_quick(net = ''):
    wlan_init()
    if not net:
        return wlan_quick('TP') or wlan_connect()
    else:
        # perform a quick connect, ie no scan
        wlan_add_sta()
        if w.isconnected():
            print('already connected ({})'.format(w.ssid()))
            return True
        print("Quick connect", net)
        k = known_nets_dict[net]
        sec = k['sec']
        pwd = k['pwd']
        w.connect(net, ( sec, pwd ) )
        return wlan_waitconnected(timeout_s=10)

def wlan_scan(verbose=True, antenna=None):
    wlan_init(antenna)
    wlan_add_sta()
    verbose and print('scan', end='')
    nets = w.scan()
    verbose and print("[{}]".format(len(nets)))

    min_rssi =  1000
    max_rssi = -1000
    for net in nets:
        # verbose and print('    {:25s} ({:4d}) {:2d} {:3d}'.format(net.ssid, net.rssi, net.channel, net.sec), ':', net)
        if net.rssi < min_rssi:
            min_rssi = net.rssi
        if net.rssi > max_rssi:
            max_rssi = net.rssi
    verbose and print('rssi range = [{},{}]'.format(min_rssi, max_rssi))
    print('ant={} mode={} bw={} ch={} pwr={} scan[{}] rssi=[{},{}]'.format(ant_name[w.antenna()], mode_name[w.mode()], bw_name[w.bandwidth()], w.channel(), w.max_tx_power(), len(nets), min_rssi, max_rssi))

    if verbose:
        nets_sorted = sorted(nets, key=lambda x: x.rssi)
        # print('sorted')
        print('    {:25s} ({:4s}) {:2s} {:3s}'.format('SSID', 'RSSI', 'CH', 'SEC'))
        for net in nets:
            print('    {:25s} ({:4d}) {:2d} {:3d}'.format(net.ssid, net.rssi, net.channel, net.sec), ':', net)

    return len(nets)

def wlan_connect(timeout_s = 20, antenna=None):
    global connection, IP, w
    wlan_init(antenna=antenna)
    wlan_add_sta()

    if w.isconnected():
        print("currently connected ... disconnecting")
        w.disconnect()
        while w.isconnected():
            time.sleep_ms(100)

    print("Scanning for wifi networks")
    available_nets_list = w.scan()
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
                w.ifconfig(config=net_properties['wlan_config'])
            #print("connect", net_to_use, sec) # , pwd)
            w.connect(net_to_use, (sec, pwd))
            return wlan_waitconnected(timeout_s)

        except Exception as e:
            print("Error while trying to connect to Wlan:", e)
            return False

def wlan_ip():
    wlan_init()
    return w.ifconfig()[0]

def wlan_gw():
    wlan_init()
    return w.ifconfig()[2]

def wlan_ifconfig():
    wlan_init()
    c = w.ifconfig()# (ip, subnet_mask, gateway, DNS_server)
    print("ifconfig", c)
    return c

def wlan_deinit():
    global w
    w.deinit()
    w = None

def wlan_info():
    # print('i')
    w = wlan_init()
    # print('d')
    def p(*m):
        print(*m, end='')

    p('mode={} '.format(mode_name[w.mode()]))
    try:
        p('hostname={} '.format(w.hostname()))
    except:
        pass
    p('conn={} '.format(w.isconnected()))
    # p('ant({})={} '.format(ant_name[w.antenna()]))
    p('ant={} '.format(ant_name[w.antenna()]))
    try:
        p('bw={} '.format(bw_name[w.bandwidth()]))
    except:
        pass
    p('ch={} '.format(w.channel()))
    try:
        p('TXPWR={} '.format(w.max_tx_power()))
    except:
        p('TXPWR=(fail)')
    try:
        p('country={} '.format(w.country()))
    except:
        pass

    p('protocol=')
    try:
        p('{} '.format(w.wifi_protocol()))
    except Exception as e:
        p('({}) '.format(e))

    p('ifconfig=')
    try:
        p(w.ifconfig(), '')
    except Exception as e:
        p(e, '')
    p('auth={} '.format(w.auth()))
    p('ssid={} '.format(w.ssid()))
    p('mac={} bssid={} '.format(w.mac(), w.bssid()))

    try:
        p('AP={} '.format(w.joined_ap_info()))
        if False:
            p('PW={} '.format(w.Connected_ap_pwd()))
    except:
        pass

    try:
        stations = w.ap_sta_list()
        p('ap_sta_list[{}] '.format(len(stations)))
        print()
        for sta in stations:
            print(sta)
    except:
        print()


if __name__ == "__main__":
    import binascii
    import os
    uid = binascii.hexlify(machine.unique_id())
    name = os.uname().sysname.lower() + '-' + uid.decode("utf-8")[-4:]
    print(os.uname().sysname, uid, name, "wlan.py")
    print("sys", os.uname().sysname)
    print("unique_id", binascii.hexlify(machine.unique_id()))
    wlan_info()
    # wlan_scan(False)
    # wlan_scan(False, WLAN.MAN_ANT)
    # wlan_scan(False, WLAN.EXT_ANT)
    # wlan_scan(False, WLAN.MAN_ANT)
    # wlan_scan(False, WLAN.INT_ANT)
    # wlan_scan(False, WLAN.MAN_ANT)

    import sys
    sys.exit()
    # ants = [WLAN.MAN_ANT, WLAN.INT_ANT, WLAN.EXT_ANT]
    # ants = [WLAN.EXT_ANT]
    ants = [WLAN.INT_ANT]

    for a in ants:
        wlan_init(antenna=a)
        ct = 0
        S = 10
        for s in range(S):
            try:
                ct += wlan_scan(False)
            except Exception as e:
                print(e)
        print(ant_name[a], ct, ct/S)
        wlan_deinit()
        time.sleep(10)

    # wlan_connect()
    if False:
        wlan_quick()
        machine.reset()
