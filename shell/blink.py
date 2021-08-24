import pycom
import time
import os
import machine
import binascii

# intensity=0x05
# intensity=0x07 # at night: comfortable to look at, lowest value where there is still a decent color contrast
# intensity=0x08
# intensity=0x0a  # at night: comfortable
# intensity=0x11 # at daylight: bit dull. at night: quite bright, possible to look at
intensity=0x15
# intensity=0x19 # at dayligh: noticable. at night: bright
# intensity=0x22 # at daylight: noticable. at night: very bright
# intensity=0x33
# intensity=0x55 # at daylight: a tad too bright
# intensity=0x88 # at dayligh: bright, you don't want to look straight at it
# intensity=0xff # go blind :)

#######################################################
mask_red   = 0xff0000
mask_green = 0x00ff00
mask_blue  = 0x0000ff
color_red   = (intensity<<16)
color_green = (intensity<<8)
color_blue  = (intensity)
color_white      = (color_red | color_green | color_blue)
color_yellow     = (color_red | color_green)
color_light_blue = (color_green | color_blue)
color_purple     = (color_red | color_blue)
color_orange     = (color_red | int(intensity * 0.7)<<8 )

# def_color=0x330033 # nicely recognisable at daylight
# def_color=0x220022 # not too bright, still ok-ish at daylight
# def_color=0x090009 # night
def_color=color_purple

def spin(ct, ms=100):
    if ct == 0:
        print('-', end='')
        return
    x = ct % 3
    if x == 0:
        print('\b\\', end='')
    elif x == 1:
        print('\b/', end='')
    elif x == 2:
        print('\b-', end='')
    time.sleep_ms(ms)

def blink(repetitions=10, color=def_color, on_ms=100, off_ms=100, do_spin=False):
    # print(repetitions, hex(color), on_ms, off_ms)
    hb = pycom.heartbeat()
    if hb:
        pycom.heartbeat(False)

    ct = repetitions
    while repetitions == 0 or ct >= 0 :
        # if ct % 100 == 0:
        #     print(time.time(), 'blink', ct)
        if repetitions:
            # count down until zero
            ct -= 1
        else:
            # keep blinking forever, but count them
            ct += 1
        if do_spin:
            spin(ct,ms=0)
        pycom.rgbled(color)
        time.sleep_ms(on_ms)
        pycom.rgbled(0x000000)
        time.sleep_ms(off_ms)
    if hb:
        pycom.heartbeat(hb)

def led(color):
    pycom.heartbeat(False)
    pycom.rgbled(color)

def led_off():
    led(0)

def fw_type():
    u = os.uname()
    # fixme: pymesh
    if hasattr(u, 'pygate'):
        return 'pygate'
    elif hasattr(u, 'pybytes'):
        return 'pybytes'
    else:
        return 'base'

def color2rgb(color):
    r = color >> 16
    g = color >> 8 & 0x00ff
    b = color & 0x0000ff
    return r,g,b

def rgb2color(red, green, blue):
    red = round(red) & 0xff
    green = round(green) & 0xff
    blue = round(blue) & 0xff
    return red << 16 | green << 8 | blue

def fade(color=def_color, steps=100, step_ms=200):
    r,g,b = color2rgb(pycom.rgbled())
    r2,g2,b2 = color2rgb(color)
    rd = (r2 - r) / steps
    gd = (g2 - g) / steps
    bd = (b2 - b) / steps
    for s in range(steps):
        c = rgb2color(r + rd*s, g + gd*s, b + bd*s)
        print(s, hex(c))
        pycom.rgbled(c)

def shimmer(repetitions=10, color=def_color, on_ms=100, off_ms=100 ):
    print(repetitions, hex(color), on_ms, off_ms)
    hb = pycom.heartbeat()
    if hb:
        pycom.heartbeat(False)

    ct = repetitions
    while repetitions == 0 or ct >= 0 :
        if ct % 100 == 0:
            print(time.time(), 'blink', ct)
        if repetitions:
            # coun
            ct -= 1
        else:
            ct += 1
        fade(color)
        fade(0)
    if hb:
        pycom.heartbeat(hb)

def whoami(verbose=False, veryverbose=False):
    import machine
    import binascii
    import os
    uid = binascii.hexlify(machine.unique_id())
    name = os.uname().sysname.lower() + '-' + uid.decode("utf-8")[-4:]
    print(name)
    print(os.uname())
    if verbose:
        print("type", fw_type())
        for attr in dir(os.uname()):
            if attr[0] != '_':
                # filter out __class__
                print(attr, getattr(os.uname(),attr))
    if veryverbose:
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
        # pysense2 in gpy - power on from otii
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
        # pysense2 w gpy - wake from picsleep via mclr button
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
    print(os.uname().sysname.lower() + '-' + binascii.hexlify(machine.unique_id()).decode("utf-8")[-4:], "blink.py")
    import _thread
    blink()
    # _thread.start_new_thread(blink, () )
    # time.sleep(0.1)
    whoami(True, True)
    if False:
        pretty_reset_cause()
        pretty_wake_reason()
        blink(3, 0x333300, 500, 100)
        shimmer()
        print(color2rgb(0xaabbcc))
        print(hex(rgb2color(0x5, 0xa, 0xff)))
        print(hex(rgb2color(5.5, 5.4, 5.6)))
        fade(0)
        for i in range(3):
            fade(0x1a2b3c)
            fade(0)
        print("spin")
        for x in range(20):
            spin(x)
        print("\bspun")
    if False:
        # slow yellow blink with spin forever
        blink(0, 0x111100, on_ms=1000, off_ms=100, do_spin=True)
