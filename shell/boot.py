import machine
import binascii
import os

print(os.uname().sysname.lower() + '-' + binascii.hexlify(machine.unique_id()).decode("utf-8")[-4:], "boot.py")

import pycom
pycom.heartbeat(False)
pycom.rgbled(0x000005)

print("boot.py:importing shell tools")

# posix like commands
try: from cat import cat
except: pass
try: from cd import cd
except: pass
try: from cp import cp
except: pass
try: from df import df
except: pass
try: from grep import grep
except: pass
try: from ls import *
except: pass
try: from mkdir import mkdir, rmdir
except: pass
try: from mv import mv
except: pass
try: from pwd import pwd
except: pass
try: from rm import rm
except: pass

# custom pycom dev board commands
try: from sleep import sleep
except: pass
try: from blink import blink
except: pass
try: from sdcard import sd
except: pass
try: from uping import ping
except: pass
try: from dns import dns
except: pass
try: from http_get import *
except: pass
try: from whoami import whoami
except: pass
try: from hexdump import hexdump
except:pass
try: import ntp
except:pass
try: import wlan
except:pass
try: import eth
except:pass

print("boot.py:done")
