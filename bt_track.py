from network import Bluetooth
import time
import binascii
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
    Bluetooth.CONN_ADV     : "CONN_ADV",
    Bluetooth.CONN_DIR_ADV : "CONN_DIR_ADV",
    Bluetooth.DISC_ADV     : "DISC_ADV",
    Bluetooth.NON_CONN_ADV : "NON_CONN_ADV",
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

ADDTL = [
    Bluetooth.ADV_NAME_SHORT,
    Bluetooth.ADV_NAME_CMPL,
    Bluetooth.ADV_FLAG,

    Bluetooth.ADV_DEV_CLASS,
    Bluetooth.ADV_SERVICE_DATA,
    Bluetooth.ADV_APPEARANCE,
    Bluetooth.ADV_ADV_INT,
    Bluetooth.ADV_TX_PWR,

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


ADDT2 = dict(ADDT)
ADDT2.pop(Bluetooth.ADV_FLAG)
ADDT2.pop(Bluetooth.ADV_NAME_CMPL)
ADDT2.pop(Bluetooth.ADV_NAME_SHORT)

print("init")
bt = Bluetooth() # antenna=Bluetooth.EXT_ANT)
time.sleep(1)
scan_timeout_s = 10
track_timeout_s = 10
total_adv_ct = 0
last_adv_time = None
try:
    print("start_scan")
    bt.start_scan(scan_timeout_s)
except Exception as e:
    print("cannot start_scan", e)
    print("stop_scan")
    bt.stop_scan()
    print("start_scan again")
    bt.start_scan(scan_timeout_s)

# Adv[mac] = [ [start,end,rssi], [], ... ]
Adv = {}



def bt_event_cb(bt_o):
    #print("c", end='')
    events = bt_o.events()   # this method returns the flags and clears the internal registry
    if events & Bluetooth.CLIENT_CONNECTED:
        print("CC", end=' ')
    elif events & Bluetooth.CLIENT_DISCONNECTED:
        print("CD", end=' ')
    elif events & Bluetooth.CHAR_READ_EVENT:
        print("RD", end=' ')
    elif events & Bluetooth.CHAR_WRITE_EVENT:
        print("WR", end=' ')
    elif events & Bluetooth.CHAR_NOTIFY_EVENT:
        print("NT", end=' ')
    elif events & Bluetooth.NEW_ADV_EVENT:
        #print("AD", end=' ')
        process_adv()
    elif events == 0:
        # I don't knwo why this happens ... but it happens
        pass
    else:
        print("XX[", hex(events), "]", sep='', end=' ')
    #print()


def print_adv(adv):
    #print("mac", mac, adv)
    s=";"
    print(binascii.hexlify(adv.mac), end=s)
    print(adv.rssi, end=s)
    if adv.addr_type in AT:
        print(AT[adv.addr_type], end=s)
    else:
        print(adv.addr_type, end=s)
    if adv.adv_type in ADT:
        print(ADT[adv.adv_type], end=s)
    else:
        print(adv.adv_type, end=s)
    #print(adv.data) # binascii.hexlify(strip(adv.data)))
    for addt in ADDTL:
        rd = bt.resolve_adv_data(adv.data, addt)
        if rd:
            if type(rd) == bytes:
                # print(ADDT[addt], "=", binascii.hexlify(rd), sep="", end=s)
                print(binascii.hexlify(rd), sep="", end=s)
            else:
                # print(ADDT[addt], "=", rd, sep="", end=s)
                print(rd, sep="", end=s)
        else:
            print(end=s)
    # if adv.data is not None:
    #     print(bt.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL), end=" ")
    #     manuf = bt.resolve_adv_data(adv.data, Bluetooth.ADV_MANUFACTURER_DATA)
    #     if manuf:
    #         # try to get the manufacturer data (Apple's iBeacon data is sent here)
    #         print(binascii.hexlify(manuf), end=" ")
    print()

def process_adv():
    global total_adv_ct
    debug = False
    adv = bt.get_adv()
    if adv:
        total_adv_ct += 1
        t = time.ticks_ms() / 1000
        mac = binascii.hexlify(adv.mac)
        if mac in Adv:
            if t - Adv[mac][-1][1] < track_timeout_s:
                # still present, update last seen
                if debug:
                    print('-', end='')
                Adv[mac][-1][1] = t
                Adv[mac][-1][2] = adv.rssi
            else:
                # present again, make a new period
                if debug:
                    print('+', end='')
                Adv[mac] += [ [t, t, adv.rssi] ]
        else:
            # seen for the first time
            if debug:
                print()
            print_adv(adv)
            #print('X', end='')
            Adv[mac] = [ [t, t, adv.rssi] ]



bt.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED | Bluetooth.CHAR_READ_EVENT | Bluetooth.CHAR_WRITE_EVENT | Bluetooth.NEW_ADV_EVENT | Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED | Bluetooth.CHAR_NOTIFY_EVENT, handler=bt_event_cb)

while bt.isscanning():
    # process_adv()
    # pass
    # print("sleep")
    # machine.sleep(5000, True)
    # print("sleep done")
    time.sleep(1)
print()
print("stopped scanning")

if False:
    Adv_list = list(Adv)
    for k in Adv:
        print(binascii.hexlify(k), end=":")
        last_end = None
        for period in Adv[k]:
            if last_end is not None:
                print('[', period[0] - last_end, ']', sep='', end=' ')
            print(period[0], '+', period[1]-period[0], '@', period[2], sep='', end=' ')
            last_end = period[1]
        print()
print("total advertisements", total_adv_ct)
print("unique advertisements", len(Adv))
