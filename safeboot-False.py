import pycom
print(pycom.bootmgr())
pycom.bootmgr(safeboot=False, reset=True)
