import machine
import binascii
import os

print(os.uname().sysname, binascii.hexlify(machine.unique_id()), "boot.py")

print("importing shell tools")
from cat import cat
from cd import cd
from cp import cp
from df import df
from ls import ls
from mkdir import mkdir
from mv import mv
from pwd import pwd
from rm import rm

from blink import blink
from dns import dns
from whoami import whoami
