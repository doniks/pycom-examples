import pycom

key = "pybytes_debug" # max 15 characters long

try:
    print("previous", pycom.nvs_get(key))
except:
    print("not set")
    pass
pycom.nvs_set(key, 6) # 99 
print("new", pycom.nvs_get(key))
