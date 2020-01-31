import pycom
import machine

fs_type = pycom.bootmgr()[1]
print("fs_type=", fs_type)

if fs_type != "FAT":
    print("Switch from", fs_type, "to FAT")
    pycom.bootmgr(fs_type=pycom.FAT)
    machine.reset()
else:
    print("Nothing to do, already on", fs_type)
