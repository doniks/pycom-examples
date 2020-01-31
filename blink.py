import pycom
import time

pycom.heartbeat(False)

I = 10
for i in range(0, I):
    print(i, "/", I)
    pycom.rgbled(0x330033)
    time.sleep_ms(200)
    pycom.rgbled(0x000000)
    time.sleep_ms(200)
