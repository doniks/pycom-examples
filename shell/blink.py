import pycom
import time
import os
import machine
import binascii

def_color=0x330033 # nicely recognisable at daylight
def_color=0x220022 # not too bright, still ok-ish at daylight

# def_color=0x090009 # night


def blink(repetitions=5, color=def_color, on_ms=100, off_ms=100 ):
    print(os.uname().sysname.lower() + '-' + binascii.hexlify(machine.unique_id()).decode("utf-8")[-4:], "blink.py")
    print(os.uname())
    hb = pycom.heartbeat()
    pycom.heartbeat(False)


    ct = repetitions
    while repetitions == 0 or ct >= 0 :
        if ct % 100 == 0:
            print(time.time(), 'blink', ct)
        # print(ct, end=' ')
        if repetitions:
            ct -= 1
        else:
            ct += 1
        pycom.rgbled(color)
        time.sleep_ms(on_ms)
        pycom.rgbled(0x000000)
        time.sleep_ms(off_ms)
    #print()
    pycom.heartbeat(hb)

if __name__ == "__main__":
    import os
    import binascii
    import machine
    blink()
    # blink(repetitions=0, on_ms=1500, off_ms=500)
    # 0xffff00 # yellow
    # blink(3, 0x333300, 500, 100)
    #blink(10, 0x330033, 500)
