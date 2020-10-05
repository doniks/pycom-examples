import machine
from machine import Pin
import pycom
import time

pins = ["P2", "P3", "P4"]
#pins = ["P4"]
# P2, P3, P4, P6, P8 to P10 and P13 to P23

wake_on_pull_up = True

s = 60000

if wake_on_pull_up:
    print("Pull", pins, "down. Device will wake when any is pulled high")
    wake_pins = []
    for p in pins:
        wake_pins += [Pin(p, mode=Pin.IN, pull=Pin.PULL_DOWN)]
    machine.pin_sleep_wakeup(wake_pins, machine.WAKEUP_ANY_HIGH, True)
else:
    print("Pull", pins, "high. Device will wake when all are pulled low")
    wake_pins = []
    for p in pins:
        wake_pins += [Pin(p, mode=Pin.IN, pull=Pin.PULL_UP)]
    machine.pin_sleep_wakeup(wake_pins, machine.WAKEUP_ALL_LOW, True)

print("deepsleep for", s / 1000, "seconds")
pycom.heartbeat(False)
pycom.rgbled(0x222200)
time.sleep(0.5)
machine.deepsleep(s)
