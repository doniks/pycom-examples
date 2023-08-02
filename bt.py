from network import Bluetooth
import time
from binascii import hexlify
import machine

# Address type
AT = {
    Bluetooth.PUBLIC_ADDR     : "PUBLIC",
    Bluetooth.RANDOM_ADDR     : "RANDOM",
    Bluetooth.PUBLIC_RPA_ADDR : "PUBLIC_RPA",
    Bluetooth.RANDOM_RPA_ADDR : "RANDOM_RPA"
}

# Advertisement type
ADT = {
    Bluetooth.CONN_ADV     : "CONN",
    Bluetooth.CONN_DIR_ADV : "CONN_DIR",
    Bluetooth.DISC_ADV     : "DISC",
    Bluetooth.NON_CONN_ADV : "NON_CONN",
    Bluetooth.SCAN_RSP     : "SCAN_RSP",
}

# Advertisement data type
ADDT = {
    Bluetooth.ADV_FLAG : "ADV_FLAG",
    Bluetooth.ADV_16SRV_PART : "ADV_16SRV_PART",
    Bluetooth.ADV_T16SRV_CMPL : "ADV_T16SRV_CMPL",
    Bluetooth.ADV_32SRV_PART : "ADV_32SRV_PART",
    Bluetooth.ADV_32SRV_CMPL : "ADV_32SRV_CMPL",
    Bluetooth.ADV_128SRV_PART : "ADV_128SRV_PART",
    Bluetooth.ADV_128SRV_CMPL : "ADV_128SRV_CMPL",
    Bluetooth.ADV_NAME_SHORT : "ADV_NAME_SHORT",
    Bluetooth.ADV_NAME_CMPL : "ADV_NAME_CMPL",
    Bluetooth.ADV_TX_PWR : "ADV_TX_PWR",
    Bluetooth.ADV_DEV_CLASS : "ADV_DEV_CLASS",
    Bluetooth.ADV_SERVICE_DATA : "ADV_SERVICE_DATA",
    Bluetooth.ADV_APPEARANCE : "ADV_APPEARANCE",
    Bluetooth.ADV_ADV_INT : "ADV_ADV_INT",
    Bluetooth.ADV_32SERVICE_DATA : "ADV_32SERVICE_DATA",
    Bluetooth.ADV_128SERVICE_DATA : "ADV_128SERVICE_DATA",
    Bluetooth.ADV_MANUFACTURER_DATA : "ADV_MANUFACTURER_DATA",
}

# Advertisement data type list used for printing
ADDTL = [
    Bluetooth.ADV_FLAG,
    Bluetooth.ADV_TX_PWR,

    Bluetooth.ADV_NAME_SHORT,
    Bluetooth.ADV_NAME_CMPL,

    Bluetooth.ADV_DEV_CLASS,
    Bluetooth.ADV_SERVICE_DATA,
    Bluetooth.ADV_APPEARANCE,
    Bluetooth.ADV_ADV_INT,

    Bluetooth.ADV_16SRV_PART,
    Bluetooth.ADV_T16SRV_CMPL,

    Bluetooth.ADV_32SRV_PART,
    Bluetooth.ADV_32SRV_CMPL,
    Bluetooth.ADV_32SERVICE_DATA,

    Bluetooth.ADV_128SRV_PART,
    Bluetooth.ADV_128SRV_CMPL,
    Bluetooth.ADV_128SERVICE_DATA,

    Bluetooth.ADV_MANUFACTURER_DATA,
]

# ADDT2 = dict(ADDT)
# ADDT2.pop(Bluetooth.ADV_FLAG)
# ADDT2.pop(Bluetooth.ADV_NAME_CMPL)
# ADDT2.pop(Bluetooth.ADV_NAME_SHORT)

def bt_event_cb(bt_o):
    #print("c", end='')
    events = bt_o.events()   # this method returns the flags and clears the internal registry
    #print("XX[", hex(events), "]", sep='', end=' ')
    if events & Bluetooth.CLIENT_CONNECTED:
        #print("event CLIENT_CONNECTED")
        print("CC", end=' ')
    elif events & Bluetooth.CLIENT_DISCONNECTED:
        #print("event CLIENT_DISCONNECTED")
        print("CD", end=' ')
    elif events & Bluetooth.CHAR_READ_EVENT:
        #print("event READ", end=' ')
        print("RD", end=' ')
    elif events & Bluetooth.CHAR_WRITE_EVENT:
        #print("event WRITE", end=' ')
        print("WR", end=' ')
    elif events & Bluetooth.CHAR_NOTIFY_EVENT:
        #print("event NOTIFY", end=' ')
        print("NT", end=' ')
    elif events & Bluetooth.NEW_ADV_EVENT:
        #print("AD", end=' ')
        #print('.', end='')
        process_adv()
    elif events == 0:
        # I don't knwo why this happens ... but it happens
        pass
    else:
        print("XX[", hex(events), "]", sep='', end=' ')
    #print()

def twoscmp(value):
    if value > 128:
        value = value - 256
    return value

def print_adv(adv):
    #print("mac", mac, adv)
    # s=";"
    s=" "
    print(hexlify(adv.mac), end=s)
    print(adv.rssi, end=s)
    if adv.addr_type in AT:
        print(AT[adv.addr_type], end=s)
        #print("{:>20}".format(AT[adv.addr_type]), end=s)
    else:
        print(adv.addr_type, end=s)
    if adv.adv_type in ADT:
        #print(ADT[adv.adv_type], end=s)
        print("{:<8}".format(ADT[adv.adv_type]), end=s)
    else:
        print(adv.adv_type, end=s)
    name = _bt.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL)
    if name:
        print(name, end=s)
    else:
        name = _bt.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_SHORT)
        if name:
            print(name, end=s)
        else:
            print(end=s)
    #print(adv.data) # hexlify(strip(adv.data)))
    for addt in ADDTL:
        rd = _bt.resolve_adv_data(adv.data, addt)
        if rd:
            if addt == Bluetooth.ADV_FLAG:
                print('{:08b}'.format(rd), end=s)
            elif type(rd) == bytes:
                # print(ADDT[addt], "=", hexlify(rd), sep="", end=s)
                print(hexlify(rd), sep="", end=s)
            else:
                # print(ADDT[addt], "=", rd, sep="", end=s)
                print(rd, sep="", end=s)
        else:
            print(end=s)
    manuf_data = _bt.resolve_adv_data(adv.data, Bluetooth.ADV_MANUFACTURER_DATA)
    if manuf_data:
        # try decoding according to iBeacon encoding
        manuf4 = hexlify(manuf_data[0:4])
        uuid = hexlify(manuf_data[4:20])
        major = hexlify(manuf_data[20:22])
        minor = hexlify(manuf_data[22:24])
        tx_power = hexlify(manuf_data[24:25])
        print(len(manuf_data), manuf4, uuid, major, minor, tx_power, sep=s, end=s)
        try:
            print(int(major, 16), end=s)
        except:
            print(end=s)
        try:
            print(int(minor, 16), end=s)
        except:
            print(end=s)
        try:
            print(twoscmp(int(tx_power, 16)), end=s)
        except:
            print(end=s)
    print()

def process_adv():
    global _bt, _bt_total_adv_ct, _bt_advertisements, _bt_track_timeout_s
    debug = True
    adv = _bt.get_adv()
    if adv:
        _bt_total_adv_ct += 1
        t = time.ticks_ms() / 1000
        mac = hexlify(adv.mac)
        if mac in _bt_advertisement_periods:
            # we've seen mac before
            if t - _bt_advertisement_periods[mac][-1][1] < _bt_track_timeout_s:
                # we're still continuously seeing mac -> update last seen period
                if not debug:
                    print('-', end='')
                _bt_advertisement_periods[mac][-1][1] = t
                _bt_advertisement_periods[mac][-1][2] = adv.rssi
            else:
                # we've rediscovered it -> make a new period
                if not debug:
                    print('+', end='')
                _bt_advertisement_periods[mac] += [ [t, t, adv.rssi] ]
        else:
            # seeing mac for the first time
            _bt_advertisements[mac] = adv
            _bt_advertisement_periods[mac] = [ [t, t, adv.rssi] ]
            if debug:
                print_adv(adv)
            else:
                print('X', end='')

def _bt_init():
    global _bt, _bt_total_adv_ct, _bt_advertisements, _bt_advertisement_periods, _bt_track_timeout_s
    print("init")


    _bt_total_adv_ct = 0

    # _bt_advertisements is a dict of advertisements, ie list of scan results
    # _bt_advertisements[mac] = advertisment
    _bt_advertisements = {}

    _bt_track_timeout_s = 20

    # _bt_advertisement_periods is a dictionary of a list of _bt_advertisement_periods
    # _bt_advertisement_periods[mac] = [ [start,end,rssi], [], ... ]
    # for each mac (device) we have ever seen we record the _bt_advertisement_periods (start, end, rssi)
    _bt_advertisement_periods = {}

    _bt = Bluetooth() # antenna=Bluetooth.EXT_ANT)
    _bt.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED | Bluetooth.CHAR_READ_EVENT | Bluetooth.CHAR_WRITE_EVENT | Bluetooth.NEW_ADV_EVENT | Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED | Bluetooth.CHAR_NOTIFY_EVENT, handler=bt_event_cb)

def _bt_start_scan(scan_timeout_s):
    try:
        print("start_scan", scan_timeout_s)
        _bt.start_scan(scan_timeout_s)
    except Exception as e:
        print("cannot start_scan", e, 'trying to restart')
        print("stop_scan")
        _bt.stop_scan()
        print("start_scan again")
        _bt.start_scan(scan_timeout_s)

def bt_scan(timeout_s=5):
    _bt_init()

    time.sleep(1)
    _bt_start_scan(timeout_s)

    while _bt.isscanning():
        time.sleep(1)
    print("scanning stopped")

    # print scanning results, ie, advertisment details per device
    print("mac;rssi;AT;ADT;Name;", end='')
    for addt in ADDTL:
        print(ADDT[addt], end=';')
    print('len;manuf4?;uuid;major;minor;tx_pwr;major;minor;tx_pwr')
    print()

    # for a in _bt_advertisements:
    #     print_adv(_bt_advertisements[a])

    adv_sorted = sorted(_bt_advertisements.items(), key=lambda x: x[1][3])
    for a in adv_sorted:
        #print(a[0], a[1][3])
        print_adv(a[1])

    # print("devices", len(_bt_advertisement_periods))
    print("advertisements", _bt_total_adv_ct)


def bt_track(timeout_s=120):
    _bt_init()
    time.sleep(1)
    _bt_start_scan(timeout_s)

    while _bt.isscanning():
        time.sleep(1)
    print("scanning stopped")

    # print tracking results, ie _bt_advertisement_periods of visibility per device
    for k in _bt_advertisement_periods:
        print(hexlify(k), end=":")
        last_end = None
        for period in _bt_advertisement_periods[k]:
            if last_end is not None:
                print('[', period[0] - last_end, ']', sep='', end=' ')
            print(period[0], '+', period[1]-period[0], '@', period[2], sep='', end=' ')
            last_end = period[1]
        print()

def bt_stuffs():
    if False:
        from network import Bluetooth
        _bt = Bluetooth()
        _bt.nvram_erase()
        import machine
        machine.reset()
