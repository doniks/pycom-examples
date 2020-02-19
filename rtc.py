import time
from machine import RTC


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
