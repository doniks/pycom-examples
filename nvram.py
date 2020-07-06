import pycom

key = "nvram_test_key0" # max 15 characters long
key = "nvram6789abcdefs" # max 15 characters long
# print(len(key))
newvalue = 42

try:
    oldvalue = pycom.nvs_get(key)
    print("get", key, oldvalue)
    newvalue = oldvalue + 1
except Exception as e:
    print("Couldn't read", key, e)

print("set", key, newvalue)
pycom.nvs_set(key, newvalue)


x = pycom.nvs_get(key)
print("get", key, x)

# print("erase")
# pycom.nvs_erase(key)

print("OK")
