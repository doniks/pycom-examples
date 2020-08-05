import time


def pretty_time(t=None):
    if not t:
        pretty_time(time.gmtime())
    else:
        d = t[6]
        if d == 0:
            print("Mon", end="")
        elif d == 1:
            print("Tue", end="")
        elif d == 2:
            print("Wed", end="")
        elif d == 3:
            print("Thu", end="")
        elif d == 4:
            print("Fri", end="")
        elif d == 5:
            print("Sat", end="")
        elif d == 6:
            print("Sun", end="")
        # according to docs, h, m and s are 0 based, but that doesn't seem to be the case in 1.20.2.rc10
        # print("{:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(t[0], t[1], t[2], t[3]+1, t[4]+1, t[5]+1))
        print(", {:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(t[0], t[1], t[2], t[3], t[4], t[5]))

def ntp_sync(TZ=0):
    from machine import RTC
    print("sync rtc, TZ=", TZ)
    rtc = RTC()
    print("synced?", rtc.synced())
    rtc.ntp_sync('nl.pool.ntp.org')
    print("synced?", rtc.synced())
    #time.sleep_ms(750)
    time.timezone(TZ * 3600)


    timeout_ms = 10000
    for i in range(0, timeout_ms):
        if rtc.synced():
            print("rtc is synced")
            # if rtc.now()[0] == 1970:
            #     print()
            break
        if i % 10 == 0:
            print(".", end="")
        time.sleep_ms(1)
    if not rtc.synced():
        raise Exception("RTC did not sync in", timeout_ms/1000, "s")

    print("now", rtc.now())
    print("gmtime", time.gmtime())
    print("localtime", time.localtime())
    print("gmt  ", end=" ")
    pretty_time(time.gmtime())
    print("local", end=" ")
    pretty_time(time.localtime())
    # formatted_time = "{year}-{month}-{day} {hours}:{minutes}:{seconds}".format(hours=now[3], minutes=now[4], seconds=now[5], day=now[2], month=now[1], year=now[0])
    #


if __name__ == "__main__":
    ntp_sync(TZ=2) # 2 EU daylight savings
    # ntp()
