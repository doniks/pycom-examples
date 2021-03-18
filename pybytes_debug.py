import pycom

key = "pybytes_debug" # max 15 characters long

def dbg(v=None, verbose=True):
    if v is None:
        try:
            d = pycom.nvs_get(key)
            if verbose:
                print("current", d)
            return d
        except:
            if verbose:
                print("not set")
            return 0
    else:
        try:
            d = pycom.nvs_get(key)
            if verbose:
                print("previous", d)
        except:
            if verbose:
                print("not set yet, setting ...")
        pycom.nvs_set(key, v) # 1,2,3,4,5,6, 99
        if verbose:
            print("new", pycom.nvs_get(key))

def toggle():
    if dbg(verbose=False):
        dbg(0)
    else:
        dbg(99)

if __name__ == '__main__':
    # toggle()
    if False:
        pycom.nvs_set(key, 99) # 1,2,3,4,5,6, 99
        dbg(0) # off
        dbg(1) #
        dbg(2) #
        dbg(3) # not enough
        dbg(4) #
        dbg(5) #
        dbg(6) # okish
        dbg(99) # max
        import machine
        machine.reset()

'''
1:

WMAC: 2462ABF4E438
Firmware: 1.20.2.r4
Pybytes: 1.6.1
Initialized watchdog for WiFi and LTE connection with timeout 1260000 ms
WiFi connection established
MQTT Protocol
Connected to MQTT mqtt.pybytes.pycom.io
Pybytes connected successfully (using the built-in pybytes library)
MQTT Protocol
Pybytes configuration read from /flash/pybytes_config.json
'''
