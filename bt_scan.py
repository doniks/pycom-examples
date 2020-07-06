from network import Bluetooth
import time
import binascii

server_name = "Pycom BT test server3"
server_mac = None

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

# print("mac;rssi;AT;ADT", sep=";", end=";")
# for addt in ADDTL:
#     print(ADDT[addt], sep=";", end=";")
# print()

bt = Bluetooth() # antenna=Bluetooth.EXT_ANT)
scan_timeout_s = 7 # 5 sometimes doesn't find it
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

Adv = {}



def bt_event_cb(bt_o):
    #print("c", end='')
    events = bt_o.events()   # this method returns the flags and clears the internal registry
    #print("XX[", hex(events), "]", sep='', end=' ')
    if events & Bluetooth.CLIENT_CONNECTED:
        print("CLIENT_CONNECTED")
    elif events & Bluetooth.CLIENT_DISCONNECTED:
        print("CLIENT_DISCONNECTED")
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
    global server_mac
    debug = False
    adv = bt.get_adv()
    if adv:
        # print(adv)
        total_adv_ct += 1
        t = time.ticks_ms() / 1000
        mac = binascii.hexlify(adv.mac)
        if mac in Adv:
            pass
        else:
            Adv[mac] = adv
            #print_adv(adv)
            name = bt.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL)
            if name is None or not name:
                name = bt.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_SHORT)
            if name == server_name:
                #print_adv(adv)
                print("found", server_name)
                server_mac = adv.mac
                bt.stop_scan()

def list_characteristics(s):
    for c in s.characteristics():
        print("        C:", end="")
        uuid = c.uuid()
        print(type(c), end="")
        if type(uuid) == int:
            print(uuid, end=" ")
        else:
            print(binascii.hexlify(uuid), end=" ")

        print(c.instance(), c.properties(), c.value(), end=" ")
        try:
            print(c.read())
        except Exception as e:
            print(e)
        # c.read_descriptor(uuid)

def list_services(conn):
    for s in conn.services():
        print("    S:", end="")
        print(type(s), end="")
        uuid = s.uuid()
        if type(uuid) == int:
            print(uuid, end=" ")
        else:
            print(binascii.hexlify(uuid), end=" ")
        print(s.isprimary(), s.instance())
        list_characteristics(s)


bt.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED | Bluetooth.CHAR_READ_EVENT | Bluetooth.CHAR_WRITE_EVENT | Bluetooth.NEW_ADV_EVENT | Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED | Bluetooth.CHAR_NOTIFY_EVENT, handler=bt_event_cb)

while bt.isscanning():
    time.sleep(1)
print("stopped scanning")

# Adv_list = list(Adv)
# for k in Adv:
#     print(Adv[k].rssi, binascii.hexlify(Adv[k].mac))
print("total advertisements", total_adv_ct)
print("unique advertisements", len(Adv))

if server_mac is None:
    print("couldn not find", server_name)
else:
    print("connect to", server_name, "at", binascii.hexlify(server_mac))
    try:
        conn = bt.connect(server_mac)
    except Exception as e:
        print(e)
        bt.disconnect_client()
        time.sleep(1)
        conn = bt.connect(server_mac)
    print(conn.isconnected())
    print(conn.get_mtu())
    #print(len(conn.services()))
    list_services(conn)
    for s in conn.services():
        if s.uuid() == 1:
            for c in s.characteristics():
                if c.uuid() == 11:
                    print("found")
                    for ct in range(0,10):
                        c.read()
                        print('.', end='')
                        if ct % 100 == 0:
                            print('[', time.time(),']:', ct, sep='')
                    print(time.time())


print("disconnect")
bt.disconnect_client()

print("end")
