import time
import machine
from machine import Timer

secs = 3
ct = 0
max_ct = 5

def handler(alarm):
    global ct
    ct += 1
    print(time.time(), ct, 'now')
    if ct >= max_ct:
        print('done')
        alarm.cancel()

def rst(alarm):
    print('\n\n\n\nreset\n\n\n')
    time.sleep(1)
    machine.reset()

print('setup timer', secs)
# alarm = Timer.Alarm(handler, secs, periodic=True)
alarm = Timer.Alarm(rst, secs, periodic=True)
