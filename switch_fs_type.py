import pycom
import machine

fs_type = pycom.bootmgr()[1]
print("fs_type=", fs_type)

if fs_type == "LittleFS":
    print("Switch from", fs_type, "to FAT")
    pycom.bootmgr(fs_type=pycom.FAT)
elif fs_type == "FAT":
    print("Switch from", fs_type, "to LittleFS")
    pycom.bootmgr(fs_type=pycom.LittleFS)
else:
    raise "Oh no"

machine.reset()
