import time
from machine import RTC
import machine
import pycom
import os

rtc = RTC()
rtc.ntp_sync('nl.pool.ntp.org')
time.sleep_ms(750)
time.timezone(3600)


for i in range(0, 100):
    if rtc.synced():
        print("rtc is synced")
        break
    print(".", end="")
    time.sleep(1)

now = time.localtime()
print("now", now)
# formatted_time = "{year}-{month}-{day} {hours}:{minutes}:{seconds}".format(hours=now[3], minutes=now[4], seconds=now[5], day=now[2], month=now[1], year=now[0])
#
