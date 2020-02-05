import sqnsupgrade
from machine import SD
import os
import time

sqnsupgrade.info(debug=True)

try:
    sd = SD()
    os.mount(sd, '/sd')
except:
    # assume it is mounted already
    pass

name = "CATM1-41065"
# name = "NB1-41019"

# list the dir and let it raise an exception if it doesn't exist (maybe SD card isn't present?)
print(os.listdir('/sd/' + name))


fw = "/sd/" + name + "/" + name + ".dup"
up = "/sd/" + name + "/updater.elf"

print("upgrading", fw, up)
x = time.time()
sqnsupgrade.run(fw, up)
#sqnsupgrade.run(‘/sd/nb/NB1-41019.dup’,‘/sd/nb/updater.elf’)
print("upgrade finished after", time.time() - x , "seconds") # ~ 380 seconds

sqnsupgrade.info(debug=True)
