import time


def _pretty_time(t, do_return=False):
    buf=""
    d = t[6]
    if d == 0:
        buf += "Mon"
    elif d == 1:
        buf += "Tue"
    elif d == 2:
        buf += "Wed"
    elif d == 3:
        buf += "Thu"
    elif d == 4:
        buf += "Fri"
    elif d == 5:
        buf += "Sat"
    elif d == 6:
        buf += "Sun"
    # according to docs, h, m and s are 0 based, but that doesn't seem to be the case in 1.20.2.rc10
    # buf += "{:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(t[0], t[1], t[2], t[3]+1, t[4]+1, t[5]+1))
    buf += ", {:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(t[0], t[1], t[2], t[3], t[4], t[5])
    if do_return:
        return buf
    else:
        print(buf)

def pretty_gmt(do_return=False):
    if do_return:
        return _pretty_time(time.gmtime(), do_return=do_return)
    else:
        _pretty_time(time.gmtime(), do_return=do_return)

def pretty_local(do_return=False):
    if do_return:
        return _pretty_time(time.localtime(), do_return=do_return)
    else:
        _pretty_time(time.localtime(), do_return=do_return)

def sync(TZ=0, timeout_s = 30):
    from machine import RTC
    print("sync rtc via ntp, TZ=", TZ)
    rtc = RTC()
    print("synced?", rtc.synced())
    rtc.ntp_sync('nl.pool.ntp.org')
    print("synced?", rtc.synced())
    #time.sleep_ms(750)
    time.timezone(TZ * 3600)

    timeout_ms = 1000 * timeout_s
    for i in range(0, timeout_ms):
        if rtc.synced():
            print("rtc is synced after", i/1000, "s")
            # if rtc.now()[0] == 1970:
            #     print()
            break
        if i % 100 == 0:
            print(".", end="")
        time.sleep_ms(1)
    if not rtc.synced():
        raise Exception("RTC did not sync in", timeout_ms/1000, "s")

    print("rtc.now", rtc.now())
    print("time.gmtime", time.gmtime())
    print("time.localtime", time.localtime())
    print("gmt  ", end=" ")
    pretty_gmt()
    print("local", end=" ")
    pretty_local()


if __name__ == "__main__":
    print(time.time())
    # sync(TZ=2) # 2 = EU daylight savings
    sync(TZ=1) # 1 = EU regular time
    t = time.time()
    print("s", t)
    t /= 60
    print("m", int(t))
    t /= 60
    print("h", int(t))
    t /= 24
    print("d", int(t))
    t /= 365
    print("y", int(t))
