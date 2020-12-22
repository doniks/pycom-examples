from machine import Pin
import pycom
import time

def pin_blink(b):
    preamble=50
    high=2
    low=25
    debug_pin(1)
    time.sleep_ms(preamble)
    debug_pin(0)
    time.sleep_ms(low)
    for i in range(b):
        debug_pin(1)
        time.sleep_ms(high)
        debug_pin(0)
        time.sleep_ms(low)

debug_pin = Pin("P11", mode=Pin.OUT) # second one bottom left
# debug_pin = Pin("P12", mode=Pin.OUT) # bottom left
if __name__ == "__main__":
    pin_blink(3)
