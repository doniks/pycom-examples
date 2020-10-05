import pycom
import time
import os
import machine
import binascii
def_color=0x330033 # nicely recognisable at daylight
def_color=0x220022 # not too bright, still ok-ish at daylight
# def_color=0x090009 # night

def blink(repetitions=5, color=def_color, on_ms=100, off_ms=100 ):
    hb = pycom.heartbeat()
    if hb:
        pycom.heartbeat(False)

    ct = repetitions
    while repetitions == 0 or ct >= 0 :
        if ct % 100 == 0:
            print(time.time(), 'blink', ct)
        if repetitions:
            ct -= 1
        else:
            ct += 1
        pycom.rgbled(color)
        time.sleep_ms(on_ms)
        pycom.rgbled(0x000000)
        time.sleep_ms(off_ms)
    if hb:
        pycom.heartbeat(hb)

def whoami(verbose=False):
    import machine
    import binascii
    import os
    uid = binascii.hexlify(machine.unique_id())
    name = os.uname().sysname.lower() + '-' + uid.decode("utf-8")[-4:]
    print(name)
    if verbose:
        for attr in dir(os.uname()):
            if attr[0] != '_':
                # filter out __class__
                print(attr, getattr(os.uname(),attr))
        if os.uname().nodename == 'GPy' or os.uname().nodename == 'FiPy':
            from network import LTE
            lte = LTE()
            ver = lte.send_at_cmd('ATI1').split('\r\n')[2]
            prot = 'unknown'
            import re
            if re.search('^LR5', ver):
                prot = 'CAT-M1'
            elif re.search('^LR6', ver):
                prot = 'NB-IoT'
            print('Sequans FW', ver, prot)

def pretty_reset_cause():
    mrc = machine.reset_cause()
    print('reset_cause', mrc, end=' ')
    if mrc == machine.PWRON_RESET:
        print("PWRON_RESET")
        # plug in
        # press reset button on module
        # reset button on JTAG board
        # core dump
    elif mrc == machine.HARD_RESET:
        print("HARD_RESET")
    elif mrc == machine.WDT_RESET:
        print("WDT_RESET")
        # machine.reset()
        # machine.lte_reset()
    elif mrc == machine.DEEPSLEEP_RESET:
        print("DEEPSLEEP_RESET")
        # machine.deepsleep()
    elif mrc == machine.SOFT_RESET:
        print("SOFT_RESET")
        # Ctrl-D
    elif mrc == machine.BROWN_OUT_RESET:
        print("BROWN_OUT_RESET")

def pretty_wake_reason():
    mwr = machine.wake_reason()
    print("wake_reason", mwr, end=' ')
    if mwr[0] == machine.PWRON_WAKE:
        print("PWRON_WAKE")
        # reset button
    elif mwr[0] == machine.PIN_WAKE:
        print("PIN_WAKE")
    elif mwr[0] == machine.RTC_WAKE:
        print("RTC_WAKE")
        # from deepsleep
    elif mwr[0] == machine.ULP_WAKE:
        print("ULP_WAKE")

# on an Exp 3.1
# plugin                        PWRON_RESET, PWRON_WAKE
# reset button                  PWRON_RESET, PWRON_WAKE
# Atom -> More -> Reboot device WDT_RESET,   PWRON_WAKE
# Ctrl-D                        SOFT_RESET,  PWRON_WAKE
## on a pysense 1

## on a pysense 1               reset_cause      wake_reason  pysense.wr
# plugin                        PWRON_RESET      PWRON_WAKE
# reset button                  PWRON_RESET      PWRON_WAKE
# machine.deepsleep             DEEPSLEEP_RESET  RTC_WAKE
# Atom -> More -> Reboot device WDT_RESET        PWRON_WAKE
# Ctrl-D                        SOFT_RESET       PWRON_WAKE
# pysense sleep timeout         PWRON_RESET      PWRON_WAKE   4 Timer
# pysense sleep ext IO          PWRON_RESET      PWRON_WAKE   8 Int Pin
# pysense sleep accelerometer   PWRON_RESET      PWRON_WAKE   1 Accelerometer
# pysense sleep button          PWRON_RESET      PWRON_WAKE   2 Push button

if __name__ == "__main__":
    import os
    import binascii
    import machine
    # blink(repetitions=0, on_ms=1500, off_ms=500)
    # 0xffff00 # yellow
    # blink(3, 0x333300, 500, 100)
    #blink(10, 0x330033, 500)
    print(os.uname().sysname.lower() + '-' + binascii.hexlify(machine.unique_id()).decode("utf-8")[-4:], "blink.py")
    # print(os.uname())
    pretty_reset_cause()
    pretty_wake_reason()
    blink()
    whoami(True)
