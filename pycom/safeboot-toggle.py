import pycom


def toggle_safeboot_on():
    safeboot = pycom.bootmgr()[2]
    if safeboot == "SafeBoot: False":
        print("Switching to safeboot mode")
        pycom.bootmgr(safeboot=True, reset=True)
    elif safeboot == "SafeBoot: True":
        print("Already in safeboot mode")

def toggle_safeboot_off():
    safeboot = pycom.bootmgr()[2]
    if safeboot == "SafeBoot: False":
        print("Already in normal mode")
    elif safeboot == "SafeBoot: True":
        print("Switching to normal mode")
        pycom.bootmgr(safeboot=False, reset=True)


def toggle_safeboot():
    safeboot = pycom.bootmgr()[2]
    if safeboot == "SafeBoot: False":
        toggle_safeboot_on()
    elif safeboot == "SafeBoot: True":
        toggle_safeboot_off()

if __name__ == "__main__":
    toggle_safeboot()
