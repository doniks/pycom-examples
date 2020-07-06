from machine import SD
import os

sd = SD()
try:
    os.mount(sd, '/sd')
except Exception as e:
    print("Exception while trying to mount (maybe it's mounted already):", e)

# check the content
print(os.listdir('/sd'))

# # try some standard file operations
# f = open('/sd/test.txt', 'w')
# f.write('Testing SD card write operations')
# f.close()
# f = open('/sd/test.txt', 'r')
# f.readall()
# f.close()
