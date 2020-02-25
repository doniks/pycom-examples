import pycom
import time

pycom.heartbeat(False)

I = 10
for i in range(0, I):
    print(I-i, end=" ")
    pycom.rgbled(0x330033)
    time.sleep_ms(100)
    pycom.rgbled(0x000000)
    time.sleep_ms(100)
print()
