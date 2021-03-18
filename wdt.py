from machine import WDT
import time

# This demonstrates the WDT
# theoretically, it should keep running and feed it just in time, but
# practically, you will see it randomly be just late to feed and the module will reset

def spin(ct, ms=100):
    if ct == 0:
        print('-', end='')
        return
    x = ct % 3
    if x == 0:
        print('\b\\', end='')
    elif x == 1:
        print('\b/', end='')
    elif x == 2:
        print('\b-', end='')
    time.sleep_ms(ms)

wdt_to_s = 15
print('WDT with', wdt_to_s, 's')
wdt = WDT(id=0, timeout=wdt_to_s * 1000)


# how many deci-seconds before wdt timeout
early_ds = 10
early_ds = 1
# early_ds = 0
feed_ds = 15 * 10 - early_ds
print('feeding the wdt every', feed_ds / 10, 's')
for x_ds in range(10_000):
    spin(x_ds) # 100 ms each
    if x_ds % feed_ds == 0:
        print('\b', time.time(), ' feed', sep='')
        wdt.feed()
