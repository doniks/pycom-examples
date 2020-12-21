from network import Bluetooth

def conn_cb (bt_o):
    print("conn_cb")
    events = bt_o.events()
    if  events & Bluetooth.CLIENT_CONNECTED:
        print("Client connected")
    elif events & Bluetooth.CLIENT_DISCONNECTED:
        print("Client disconnected")
    else:
        print("Other event", events)

def char11_cb_handler(chr, data):
    #print("char1_cb_handler")
    # The data is a tuple containing the triggering event and the value if the event is a WRITE event.
    # We recommend fetching the event and value from the input parameter, and not via characteristic.event() and characteristic.value()
    events, value = data
    if  events & Bluetooth.CHAR_WRITE_EVENT:
        print("Write request on char 1 with value = {}".format(value))
    else:
        print("Read request on char 1")
        # print('Read request on char 1')
        # print('.', end='')

def char21_cb_handler(chr, data):
    print("char2_cb_handler")
    # The value is not used in this callback as the WRITE events are not processed.
    events, value = data
    if  events & Bluetooth.CHAR_READ_EVENT:
        print('Read request on char 2')

print("init")
bt = Bluetooth()
bt.set_advertisement(name='Pycom BT test server5', service_uuid=666, manufacturer_data=b'deadbeef', service_data=b'cafebabe') # bytes([0xC0, 0x01, 0xD0, 0x0D, 0xC0, 0x01, 0xD0, 0x0D, 0xC0, 0x01, 0xD0, 0x0D, 0xC0, 0x01, 0xD0, 0x0D, ])) # b'1234567890123456')
bt.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED, handler=conn_cb)

print("service 1")
srv1 = bt.service(isprimary=True, uuid=1) # bytes([0xCA, 0xFE, 0xBA, 0xBE, 0xCA, 0xFE, 0xBA, 0xBE, 0xCA, 0xFE, 0xBA, 0xBE, 0xCA, 0xFE, 0xBA, 0xBE, ]))
chr11 = srv1.characteristic(uuid=11, value=87)
chr11.callback(trigger=Bluetooth.CHAR_WRITE_EVENT | Bluetooth.CHAR_READ_EVENT, handler=char11_cb_handler)
chr12 = srv1.characteristic(uuid=12, value=99)
# chr13 = srv1.characteristic(uuid=13, value=33)

print("service 2")
srv2 = bt.service(isprimary=True, uuid=2, )
chr21 = srv2.characteristic(uuid=4567, value=9) # 0x1234)
chr21.callback(trigger=Bluetooth.CHAR_READ_EVENT, handler=char21_cb_handler)
# chr22 = srv2.characteristic(uuid=89, value=2) # 0x1234)

print("advertise")
bt.advertise(True)

if False:
    bt.start_scan(-1); time.sleep(1); bt.stop_scan()
    print("start"); bt.start_scan(10); print("stop")
    print("start"); bt.start_scan(-1); time.sleep(10); bt.stop_scan(); print("stop")
    print("start"); bt.advertise(True); time.sleep(10); print("stop")
    print("\nstart\n"); time.sleep(10); print("\nstop\n")

    bt.nvram_erase()
    machine.reset()
