import machine
import time
import os
from network import WLAN
import socket
import binascii

# default wlan configurations
# you can place a wlan_configs.py with your own configurations
_wlan_configs = {
    # 'ssid2': {'pwd': 'password2', 'wlan_config':  ('10.0.0.114', '255.255.0.0', '10.0.0.1', '10.0.0.1')}, # (ip, subnet_mask, gateway, DNS_server)
    'openwireless.org' : {'pwd': '', 'sec': 0},
    'wipy-wlan-349c'   : {'pwd': 'www.pycom.io', 'sec': None}
}
try:
    # print('default _wlan_configs', _wlan_configs)
    # print('attempting to import custom _wlan_configs ...')
    from wlan_configs import _wlan_configs
    # print('succeeded')
    # print('new _wlan_configs', _wlan_configs)
except Exception as e:
    # print(e)
    pass

# w = None
SCAN_RESULT_IDX_SSID = 0
SCAN_RESULT_IDX_BSSID = 1
SCAN_RESULT_IDX_CHANNEL = 2
SCAN_RESULT_IDX_RSSI = 3
SCAN_RESULT_IDX_SEC = 4
SCAN_RESULT_IDX_HIDDEN = 5
connection = ""
IP = ""

mode_name = {
    WLAN.IF_STA    : 'STA',
    WLAN.IF_AP     : 'AP',
}

def wlan_init():
    global w
    try:
        if w is not None:
            # print('already initialized')
            return w
    except:
        pass
    print("Initialise WiFi")
    w = WLAN(WLAN.IF_STA)
    w.config(hostname=(binascii.hexlify(machine.unique_id()) + "." + os.uname().sysname + "." + "w"))
    return w

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
            print(f"\nTimeout ({timeout_s}s)")
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
        print("-", end="")
        ct += 1
        machine.idle()
        IP = w.ifconfig()[0]
        time.sleep_ms(100)
    print('')
    print("Connected to", w.config('ssid'), "with IP address:", IP, ct)
    host = "detectportal.firefox.com"
    print(host, socket.getaddrinfo(host, 80)[0][4][0])
    return True

def wlan_quick(ssid = ''):
    wlan_init()
    if not ssid:
        return wlan_quick('TP') or wlan_connect()
    else:
        # perform a quick connect, ie no scan
        if w.isconnected():
            print('already connected ({})'.format(w.config('ssid')))
            return True
        print("Quick connect", ssid)
        k = _wlan_configs[ssid]
        sec = k['sec']
        pwd = k['pwd']
        w.connect(ssid, pwd )
        return wlan_waitconnected(timeout_s=10)

def wlan_scan(verbose=True):
    wlan_init()
    w.active(True)
    verbose and print('scan', end='')
    nets = w.scan()
    verbose and print("[{}]".format(len(nets)))

    min_rssi =  1000
    max_rssi = -1000
    for net in nets:
        # verbose and print('    {:25s} ({:4d}) {:2d} {:3d}'.format(net[SCAN_RESULT_IDX_SSID], net[SCAN_RESULT_IDX_RSSI], net.config('channel'), net.config('security')), ':', net)
        if net[SCAN_RESULT_IDX_RSSI] < min_rssi:
            min_rssi = net[SCAN_RESULT_IDX_RSSI]
        if net[SCAN_RESULT_IDX_RSSI] > max_rssi:
            max_rssi = net[SCAN_RESULT_IDX_RSSI]
    verbose and print('rssi range = [{},{}]'.format(min_rssi, max_rssi))
    print('ch={} pwr={} scan[{}] rssi=[{},{}]'.format(w.config('channel'), w.config('txpower'), len(nets), min_rssi, max_rssi))

    if verbose:
        nets_sorted = sorted(nets, key=lambda x: x[SCAN_RESULT_IDX_RSSI])
        # print('sorted')
        print('    {:25s} ({:4s}) {:2s} {:3s}'.format('SSID', 'RSSI', 'CH', 'SEC'))
        for net in nets:
            print('    {:25s} ({:4d}) {:2d} {:3d}'.format(net[SCAN_RESULT_IDX_SSID], net[SCAN_RESULT_IDX_RSSI], net[SCAN_RESULT_IDX_CHANNEL], net[SCAN_RESULT_IDX_SEC]), ':', net)

    return len(nets)

def wlan_connect(timeout_s = 20):
    global connection, IP, w
    wlan_init()

    if w.isconnected():
        print("currently connected ... disconnecting")
        w.disconnect()
        while w.isconnected():
            time.sleep_ms(100)

    print("Scanning for wifi networks")
    available_nets_list = w.scan()
    available_ssids_set = {net[SCAN_RESULT_IDX_SSID].decode() for net in available_nets_list}
    known_ssids_set = set(_wlan_configs.keys())
    # make the intersection
    usable_ssids_set = available_ssids_set & known_ssids_set
    print("available networks:", len(available_ssids_set))
    print("known networks:", len(known_ssids_set))
    print("-> available and known:", len(usable_ssids_set))
    if (len(usable_ssids_set) == 0):
        print("No usable network found")
        print("available", available_ssids_set)
        print("known", known_ssids_set)
    else:
        try:
            ssid_to_use = usable_ssids_set.pop()
            print("network found:", ssid_to_use)
            net_properties = _wlan_configs[ssid_to_use]
            pwd = net_properties['pwd']
            if 'network_config' in net_properties:
                w.ifconfig(net_properties['network_config'])
            #print("connect", net_to_use) # , pwd)
            w.connect(ssid_to_use, pwd)
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
    try:
        w.active(False)
    except NameError as e:
        print('Not initialized', e)
        return
    del w

def wlan_info():
    # print('i')
    w = wlan_init()
    # print('d')
    def p(*m):
        print(*m, end='')

    p('active={} '.format(w.active()))
    p('hostname={} '.format(w.config('hostname')))
    p('conn={} '.format(w.isconnected()))
    p('ch={} '.format(w.config('channel')))
    try:
        p('TXPWR={} '.format(w.config('txpower')))
    except:
        pass

    p('ifconfig=')
    p(w.ifconfig(), '')
    try:
        p('sec={} '.format(w.config('security')))
    except:
        pass
    p('ssid={} '.format(w.config('ssid')))
    p('mac={} '.format(binascii.hexlify(w.config('mac'))))
    try:
        p('rssi={} '.format(w.status('rssi')))
    except:
        pass
    try:
        p('status={} '.format(w.status('stations')))
        stations = w.status('stations')
        p('stations[{}] '.format(len(stations)))
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

    if False:
        wlan_scan(False)
        wlan_connect()
        wlan_quick()
        machine.reset()
