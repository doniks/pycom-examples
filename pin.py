# puts pin 12 high and reads pin 13
# if 13 is high, the led goes green
# 12 is bottom left, 13 is bottom right

from machine import Pin
import pycom
import time

def low():
    print("_", end="")
    out_p(0)
    pycom.rgbled(0x0a000a)
    time.sleep_ms(1000)

def high():
    print("-", end="")
    out_p(1)
    pycom.rgbled(0x220022)
    time.sleep_ms(1000)

def state(pin):
    print(pin.id(), end=': ')
    print("mode", pin.mode(), end=' ')
    if pin.mode() == Pin.OUT:
        print('OUT', end='')
    elif pin.mode() == Pin.IN:
        print('IN', end='')
    elif pin.mode() == Pin.OPEN_DRAIN:
        print('OD', end='')
    if pin.pull() is None:
        print(", pull None", end='')
    elif pin.pull() == Pin.PULL_UP:
        print(", pull UP", end='')
    elif pin.pull() == Pin.PULL_DOWN:
        print(", pull DOWN", end='')
    print(", value", pin.value())
p5 = Pin('P5')
state(p5)
p8 = Pin('P8')
state(p8)

for p in Pin.module.__dict__:
    print(p, ':', Pin.module.__dict__[p])

for gp in Pin.exp_board.__dict__:
    print('{:>3s}:'.format(gp), Pin.exp_board.__dict__[gp])

out_p = Pin("P11", mode=Pin.OUT)
out_p.value(1)

in_p = Pin("P13", mode=Pin.IN, pull=Pin.PULL_UP)

pycom.heartbeat(False)
while True:
    if in_p():
        high()
    else:
        low()
        high()
    time.sleep_ms(100)
