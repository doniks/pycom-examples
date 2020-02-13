import pycom
#print(pycom.bootmgr())
safeboot = pycom.bootmgr()[2]
#print(safeboot)
if safeboot == "SafeBoot: True":
    print("Already in safeboot mode")
elif safeboot == "SafeBoot: False":
    print("Switching to safeboot mode")
    pycom.bootmgr(safeboot=True, reset=True)
else:
    raise Exception("Script error")
