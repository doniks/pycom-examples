from machine import SD
import os

sd = SD()
os.mount(sd, '/sd')

# check the content
print(os.listdir('/sd'))

# # try some standard file operations
# f = open('/sd/test.txt', 'w')
# f.write('Testing SD card write operations')
# f.close()
# f = open('/sd/test.txt', 'r')
# f.readall()
# f.close()
