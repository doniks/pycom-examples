import sqnsupgrade
from machine import SD
import os
import time
import pycom
import binascii
import machine


###########
# Sequans modem firmware update per SDCARD
# 1. copy the sequans firmware you want to use onto an sd card:
#    folder structure should look like this:
#      /sd
#      /sd/NB1-41019
#      /sd/NB1-41019/updater.elf
#      /sd/NB1-41019/NB1-41019.dup
# 2. adjust the CONFIG variables below
# 3. insert SD card into expansion board
# 4. run this script on the device (e.g., via Atom Pymakr)
# 5. wait

print("sqnsup_sdcard.py")

print("sqnsupgrade.info:")
sqnsupgrade.info(debug=True)

try:
    sd = SD()
    os.mount(sd, '/sd')
except:
    # assume it is mounted already
    pass

dir='/sd'

########### CONFIG
# choose whether you want recovery update method, or normal update method
use_recovery = False
# choose whether you want to use full image or diff image
use_full = True
# choose target version
ver = 'NB1-41019'
# ver = 'CATM1-41065'
# run upgrade in debug mode or not
dbg = True
###########
dv = dir + "/" + ver + "/"
full = dv + ver + ".dup"
diff = dv + "upgdiff_33080-to-41019.dup"
updater = dv + "updater.elf"


############ main
# list and let it raise an exception if it doesn't exist
if use_recovery:
    print("updater", updater)
    print("updater", updater, os.stat(updater)[6]/1024, "KB")
else:
    print("full", full)
    print("full", full, os.stat(full)[6]/1024, "KB")


print("sys", os.uname().sysname)
print("unique_id", binascii.hexlify(machine.unique_id()))
print("release", os.uname().release)



x = time.time()
if use_full:
    if use_recovery:
        print("full, recovery", full, updater)
        sqnsupgrade.run(full, updater)
    else:
        print("full, normal", full)
        sqnsupgrade.run(full)
else:
    # diff
    print("diff", diff, os.stat(diff)[6]/1024, "KB")
    if use_recovery:
        print("NOT SUPPORTED (I think)")
    else:
        print("diff, normal", diff)
        sqnsupgrade.run(diff, debug=dbg)

print("upgrade finished after", time.time() - x , "seconds")
# full, normal: ~ 380 seconds

sqnsupgrade.info(debug=True)
