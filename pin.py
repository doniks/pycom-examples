# puts pin 12 high and reads pin 13
# if 13 is high, the led goes green
# 12 is bottom left, 13 is bottom right

from machine import Pin
import pycom
import time

out_p = Pin("P11", mode=Pin.OUT)
out_p.value(1)

in_p = Pin("P13", mode=Pin.IN, pull=Pin.PULL_UP)

pycom.heartbeat(False)


def low():
    print("_", end="")
    out_p(0)
    pycom.rgbled(0x0a000a)
    time.sleep_ms(1000)

def high():
    print("-", end="")
    out_p(1)
    pycom.rgbled(0x220022)
    time.sleep_ms(1000)

while True:
    if in_p():
        high()
    else:
        low()
        high()
    time.sleep_ms(100)
