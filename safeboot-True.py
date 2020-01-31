import pycom
print(pycom.bootmgr())
pycom.bootmgr(safeboot=True, reset=True)
