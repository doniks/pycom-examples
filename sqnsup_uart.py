import sqnsupgrade
import os
import time

###########
# Sequans modem firmware update per UART
# 1. adjust the CONFIG variables below
# 2. run this script on the device (e.g., via Atom Pymakr)
# 3. close Pymakr as instructed
# 4. run this script on the laptop:
# ```
#   cd ~/docs/sqnsupgrade/flash
#   PYTHONPATH=. python3 ~/docs/pycom-examples/sqnsup_uart.py
# ```
# 5. wait

print("sqnsup_uart.py")

########### CONFIG
# choose whether you want recovery update method, or normal update method
use_recovery = False
# choose whether you want to use full image or diff image
use_full = True
# target version
# ver = 'NB1-41019'
ver = 'CATM1-41065'
# run upgrade in debug mode or not
dbg = True
# serial port
serial_port = '/dev/ttyACM0'
serial_port = '/dev/ttyUSB2'
# where are the FW images stored
dir='/home/peter/docs/FirmwareReleases/sequans'

dv = dir + "/" + ver + "/"
full = dv + ver + ".dup"
# choose diff file
diff = dv + "upgdiff_33080-to-41019.dup"
updater = dv + "updater.elf"





########### MAIN
print("dbg", dbg)
try:
    import pycom
    print("sqnsup_uart.py is running on device")

    import pycom
    import binascii
    import machine

    print("sys", os.uname().sysname)
    print("unique_id", binascii.hexlify(machine.unique_id()))
    print("release", os.uname().release)

    sqnsupgrade.info(debug=True)
    # state 2 .. Application mode

    if use_recovery:
        import sqnsupgrade
        sqnsupgrade.uart(True, debug=dbg)
    else:
        import sqnsupgrade
        sqnsupgrade.uart(debug=dbg)
except:
    print("sqnsup_uart.py is running on desktop")

    # list and let it raise an exception if it doesn't exist
    if use_recovery:
        print("updater", updater, os.stat(updater)[6]/1024, "KB")
    if use_full:
        print("full", full, os.stat(full)[6]/1024, "KB")
    else:
        print("diff", diff, os.stat(diff)[6]/1024, "KB")

    x = time.time()
    if use_full:
        if use_recovery:
            print("full, recovery", serial_port, full, updater)
            sqnsupgrade.run(serial_port, full, updater, debug=dbg)
        else:
            print("full, normal", serial_port, full)
            sqnsupgrade.run(serial_port, full, debug=dbg)
    else:
        if use_recovery:
            print("diff update with recovery is NOT SUPPORTED (I think :-P)")
        else:
            print("diff, normal", serial_port, diff)
            sqnsupgrade.run(serial_port, diff, debug=dbg)
    print("upgrade finished after", time.time() - x , "seconds")
