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
try: from shell import *
except: pass
print('.', end='')
try: from grep import grep
except: pass
print('.', end='')
# try: from hexdump import hexdump
# except:pass
# print('.', end='')

# custom pycom dev board commands
try: from sleep import sleep
except: pass
print('.', end='')
try: from blink import *
except: pass
print('.', end='')
# try: from rand import rand,randi
# except: pass
# print('.', end='')

try: import wlan
except:pass
print('.', end='')
# try: import eth
# except:pass
# print('.', end='')
#try:
from ltei import *
#except:pass
print('.', end='')

# try: from net import *
# except:pass
# print('.', end='')
try: from dns import dns
except: pass
print('.', end='')
try: from http_get import *
except: pass
print('.', end='')
try: import ntp
except:pass

print('.', (time.ticks_ms()-t)/1000)

print("boot.py:done")
