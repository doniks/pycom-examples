from network import Bluetooth
import time
import binascii
import machine
import pycom

#server_name = "Pycom BT test server5"
server_name = "Zephyr Heartrate Sensor"
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

    # Bluetooth.ADV_DEV_CLASS,
    Bluetooth.ADV_SERVICE_DATA,
    # Bluetooth.ADV_APPEARANCE,
    # Bluetooth.ADV_ADV_INT,

    Bluetooth.ADV_16SRV_PART,
    Bluetooth.ADV_T16SRV_CMPL,

    Bluetooth.ADV_32SRV_PART,
    Bluetooth.ADV_32SRV_CMPL,

    Bluetooth.ADV_128SRV_PART,
    Bluetooth.ADV_128SRV_CMPL,

    # Bluetooth.ADV_32SERVICE_DATA,
    # Bluetooth.ADV_128SERVICE_DATA,

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
        print("event CLIENT_CONNECTED")
        #print("CC", end=' ')
    elif events & Bluetooth.CLIENT_DISCONNECTED:
        print("event CLIENT_DISCONNECTED")
        #print("CD", end=' ')
    elif events & Bluetooth.CHAR_READ_EVENT:
        print("event READ")
        #print("RD", end=' ')
    elif events & Bluetooth.CHAR_WRITE_EVENT:
        print("event WRITE")
        #print("WR", end=' ')
    elif events & Bluetooth.CHAR_NOTIFY_EVENT:
        print("event NOTIFY")
        #print("NT", end=' ')
    elif events & Bluetooth.NEW_ADV_EVENT:
        process_adv()
        #print("AD", end=' ')
    elif events == 0:
        # I don't knwo why this happens ... but it happens
        pass
    else:
        print("XX[", hex(events), "]", sep='', end=' ')
    #print()

def print_adv(adv):
    #print("mac", mac, adv)
    s=";"
    # s=" "
    print(binascii.hexlify(adv.mac), end=s)
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
            # we've seen this mac already -> ignore it
            pass
        else:
            # new mac discovered -> check it
            print('.', end='')
            Adv[mac] = adv
            #print_adv(adv)
            name = bt.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL)
            if name is None or not name:
                name = bt.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_SHORT)
            if name == server_name:
                print("found", server_name, adv.rssi, "stop scan")
                print_adv(adv)
                server_mac = adv.mac
                bt.stop_scan()

def list_characteristics(s):
    for c in s.characteristics():
        print("        C:", end="")
        uuid = c.uuid()
        #print(type(c), end="")
        if type(uuid) == int:
            #print(uuid, "/", hex(uuid), end=" ")
            print(hex(uuid), end=" ")
            if uuid == 0x2A00:
                print("Device Name", end=' ')
            elif uuid == 0x2A01:
                print("Appearance", end=' ')
            elif uuid == 0x2A04:
                print("Peripheral Preferred Connection Parameters", end=' ')
            elif uuid == 0x2A05:
                print("Service Changed", end=' ')
            elif uuid == 0x2A19:
                print("Battery Level", end=' ')
            elif uuid == 0x2a24:
                print("Model Number String", end=' ')
            elif uuid == 0x2a29:
                print("Manufacturer Name String", end=' ')
            elif uuid == 0x2A37:
                print("Heart Rate Measurement", end=' ')
            elif uuid == 0x2A38:
                print("Body Sensor Location", end=' ')
            elif uuid == 0x2A39:
                print("Heart Rate Control Point", end=' ')
            elif uuid == 0x2b29:
                print("Client Supported Features", end=' ')
            elif uuid == 0x2b2a:
                print("Database Hash", end=' ')
        else:
            print(binascii.hexlify(uuid), end=" ")

        p = c.properties()
        print(" i=", c.instance(), " p=", p, end=' ', sep='')
        if p & Bluetooth.PROP_AUTH:
            print(" auth", end='')
        if p & Bluetooth.PROP_BROADCAST:
            print(" bc", end='')
        if p & Bluetooth.PROP_EXT_PROP:
            print(" ext", end='')
        if p & Bluetooth.PROP_INDICATE:
            print(" ind", end='')
        if p & Bluetooth.PROP_NOTIFY:
            print(" ntf", end='')
        if p & Bluetooth.PROP_READ:
            print(" rd", end='')
        if p & Bluetooth.PROP_WRITE:
            print(" wr", end='')
        if p & Bluetooth.PROP_WRITE_NR:
            print(" nr", end='')
        v = c.value()
        #print(" v=", v, '/', binascii.hexlify(v), end=" ", sep=' ')
        print(" v=", binascii.hexlify(v), end=" ", sep=' ')
        try:
            r = c.read()
            print(" r=", r, '/', binascii.hexlify(r) )
        except Exception as e:
            print(e)
        # c.read_descriptor(uuid)

def list_services(conn):
    for s in conn.services():
        print("    S:", end="")
        #print(type(s), end="")
        uuid = s.uuid()
        if type(uuid) == int:
            print(hex(uuid), end=" ")
            if uuid == 0x1800:
                print("Generic Access", end=" ")
            elif uuid == 0x1801:
                print("Generic Attribute", end=" ")
            elif uuid == 0x180a:
                print("Device Information", end=" ")
            elif uuid == 0x180d:
                print("Heart Rate", end=" ")
            elif uuid == 0x180f:
                print("Battery", end=" ")
        else:
            print(binascii.hexlify(uuid), end=" ")
        print(s.isprimary(), s.instance())
        list_characteristics(s)

#############################################################
print(os.uname().sysname.lower() + '-' + binascii.hexlify(machine.unique_id()).decode("utf-8")[-4:], "bt_client.py")
pycom.heartbeat(False)
pycom.rgbled(0x222200)
print("init")
bt = Bluetooth() # antenna=Bluetooth.EXT_ANT)
bt.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED | Bluetooth.CHAR_READ_EVENT | Bluetooth.CHAR_WRITE_EVENT | Bluetooth.NEW_ADV_EVENT | Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED | Bluetooth.CHAR_NOTIFY_EVENT, handler=bt_event_cb)

scan_timeout_s = 7 # 5 sometimes doesn't find it
total_adv_ct = 0
last_adv_time = None
try:
    print("start_scan for", server_name)
    bt.start_scan(scan_timeout_s)
except Exception as e:
    print("cannot start_scan", e)
    print("stop_scan")
    bt.stop_scan()
    print("start_scan again")
    bt.start_scan(scan_timeout_s)

# Adv is a dict of advertisements, ie list of scan results
# Adv[mac] = advertisment
Adv = {}


while bt.isscanning():
    time.sleep(1)
print("scanning stopped")

# Adv_list = list(Adv)
# for k in Adv:
#     print(Adv[k].rssi, binascii.hexlify(Adv[k].mac))
print("devices", len(Adv))
print("advertisements", total_adv_ct)

if server_mac is None:
    print(time.time(), "couldn not find", server_name)
    pycom.rgbled(0x220000)
    time.sleep(5)
    machine.reset()
else:
    #server_adv = Adv[server_mac]
    print(time.time(), "found", server_name, "at", binascii.hexlify(server_mac)) # , "with", server_adv.rssi)
    ct = 0
    while True:
        try:
            pycom.rgbled(0x000022)
            print(time.time(), ct, "connect to", server_name)
            conn = bt.connect(server_mac)
            print(time.time(), "connected successful", ct)
            break
        except Exception as e:
            print(time.time(), "failed", e)
            bt.disconnect_client()
            pycom.rgbled(0x220000)
            time.sleep(1)
            if ct >= 10:
                print("reset")
                machine.reset()
        ct += 1
    pycom.rgbled(0x002200)
    print(conn.isconnected())
    print(conn.get_mtu())
    print("Services", len(conn.services()), ":")
    list_services(conn)
    # print("Test:")
    # S = 1
    # C = 11
    # for s in conn.services():
    #     if s.uuid() == S:
    #         for c in s.characteristics():
    #             if c.uuid() == C:
    #                 print("found", S, C)
    #                 for ct in range(0,10):
    #                     c.read()
    #                     print('.', end='')
    #                     # if ct % 100 == 0:
    #                     #     print('[', time.time(),']:', ct, sep='')
    #                 print(time.time())


print("disconnect")
bt.disconnect_client()

print("end")

if False:
    from network import Bluetooth
    bt = Bluetooth()
    bt.nvram_erase()
    import machine
    machine.reset()
