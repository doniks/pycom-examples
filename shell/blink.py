import pycom
import time

def blink(repetitions=5, color=0x330033, on_ms=100, off_ms=100 ):
    hb = pycom.heartbeat()
    pycom.heartbeat(False)

    for i in range(0, repetitions):
        print(repetitions-i, end=" ")
        pycom.rgbled(color)
        time.sleep_ms(on_ms)
        pycom.rgbled(0x000000)
        time.sleep_ms(off_ms)
    print()
    pycom.heartbeat(hb)

if __name__ == "__main__":
    import os
    import binascii
    import machine
    print(os.uname().sysname.lower() + '-' + binascii.hexlify(machine.unique_id()).decode("utf-8")[-4:], "blink.py")
    print(os.uname())
    blink()
    # 0xffff00 # yellow
    # blink(3, 0x333300, 500, 100)
    #blink(10, 0x330033, 500)
