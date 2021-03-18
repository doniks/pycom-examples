import time
import socket
import time

from machine import RTC
TZ = 0
print("sync rtc via ntp, TZ=", TZ)
rtc = RTC()
print("synced?", rtc.synced())
rtc.ntp_sync('nl.pool.ntp.org')
print("synced?", rtc.synced())
#time.sleep_ms(750)
time.timezone(TZ * 3600)
i = 0
while True:
    if rtc.synced():
        print("rtc is synced after", i/1000, "s")
        # if rtc.now()[0] == 1970:
        #     print()
        break
    if i % 100 == 0:
        print(".", end="")
    time.sleep_ms(1)
print("rtc.now", rtc.now())
print("time.gmtime", time.gmtime())
print("time.localtime", time.localtime())
print("gmt  ", end=" ")
print("local", end=" ")
