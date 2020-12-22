import machine
import binascii
import os
import time

print(os.uname().sysname.lower() + '-' + binascii.hexlify(machine.unique_id()).decode("utf-8")[-4:], "boot.py")

import pycom
pycom.heartbeat(False)
pycom.rgbled(0x000005)

t = time.ticks_ms()
print("boot.py:importing shell tools ", end='')

# posix/linux like commands
try:
    print('s', end='')
    from shell import *
except:
    print('S', end='')

# custom pycom dev board commands
try:
    print('w', end='')
    import wlan
except:
    print('W', end='')
# print('e', end='')
# try: import eth
# except:pass
# try:
#     print('l', end='')
#     from lte import *
# except:
#     print('x', end='')

# print('n', end='')
# try: from net import *
# except:pass
try:
    print('d', end='')
    from dns import *
except:
    print('D', end='')
# print('h', end='')
# try: from http_get import *
# except: pass
try:
    print('n', end='')
    import ntp
except:
    print('N', end='')
    pass

print(' ...', (time.ticks_ms()-t)/1000)

print("boot.py:done")
