from machine import Pin
import pycom
import time

out_p = Pin("P12", mode=Pin.OUT)
out_p.value(1)

in_p = Pin("P13", mode=Pin.IN, pull=Pin.PULL_UP)

pycom.heartbeat(False)

while True:
    if in_p():
        print("X", end="")
        pycom.rgbled(0x002200)
    else:
        print("_", end="")
        pycom.rgbled(0x111100)
    time.sleep_ms(300)
