import pycom
safeboot = pycom.bootmgr()[2]
if safeboot == "SafeBoot: False":
    print("Safeboot mode is already off")
elif safeboot == "SafeBoot: True":
    print("Switching safeboot mode off")
    pycom.bootmgr(safeboot=False, reset=True)
else:
    raise Exception("Script error")
