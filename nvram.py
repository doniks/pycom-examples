import pycom

key = "nvram_test_key0" # max 15 characters long
# print(len(key))
value = 42
pycom.nvs_set(key, value)
x = 0
x = pycom.nvs_get(key)
print(x)
if not x == value:
    raise "hell"
pycom.nvs_erase(key)
print("OK")
