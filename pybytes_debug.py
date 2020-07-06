import pycom

key = "pybytes_debug" # max 15 characters long

try:
    d = pycom.nvs_get(key)
    print("previous", d)
    if d:
        print("was enabled, disabling now ...")
        pycom.nvs_set(key, 0) # 1,2,3,4,5,6, 99
    else:
        print("was disabled, enabling now ...")
        pycom.nvs_set(key, 99) # 1,2,3,4,5,6, 99
except:
    print("not set yet, setting ...")
    pycom.nvs_set(key, 99) # 1,2,3,4,5,6, 99

print("new", pycom.nvs_get(key))
