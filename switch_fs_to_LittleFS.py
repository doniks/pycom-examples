import pycom
import machine

fs_type = pycom.bootmgr()[1]
print("fs_type=", fs_type)

if fs_type != "LittleFS":
    print("Switch from", fs_type, "to LittleFS")
    pycom.bootmgr(fs_type=pycom.LittleFS)
    machine.reset()
else:
    print("Nothing to do, already on", fs_type)
