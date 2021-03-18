# puts pin 12 high and reads pin 13
# if 13 is high, the led goes green
# 12 is bottom left, 13 is bottom right

from machine import Pin
import pycom
import time

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

def sleep(s):
    for x in range(s * 10):
        spin(x)
    print('\b.')


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

def blink(pin):
    for i in range(3):
        pin(1)
        time.sleep_ms(10)
        pin(0)
        time.sleep_ms(10)

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

pycom.heartbeat(False)
print(dir(Pin.module))
print(dir(Pin.exp_board))

# for property, value in vars(Pin.module).items():
#     print(property, ":", value)
#
# for p in dir(Pin.module):
#     print(p) # , ':', Pin.module.__dict__[p])
#     print(Pin.module.p)

# for p in Pin.module.__dict__:
#     print(p, ':', Pin.module.__dict__[p])

# for gp in Pin.exp_board.__dict__:
#     print('{:>3s}:'.format(gp), Pin.exp_board.__dict__[gp])

# out_p = Pin("P11", mode=Pin.OUT)
# out_p.value(1)
#
# in_p = Pin("P13", mode=Pin.IN, pull=Pin.PULL_UP)

# pycom.heartbeat(False)
# while True:
#     if in_p():
#         high()
#     else:
#         low()
#         high()
#     time.sleep_ms(100)

# print('outputs')
# # sleep(2)
# for p in range(0,23+1):
#     print('Pin', p)
#     if p == 0:
#         print('RX0')
#         continue
#     elif p == 1:
#         print('TX0')
#         continue
#     if p in [13, 14, 15, 16, 17, 18]:
#         print('input only!')
#     pin = Pin('P' + str(p), mode=Pin.OUT)
#     # sleep(2)
#     blink(pin)

def wait_low(pin):
    ct = 0
    while pin():
        spin(ct)
        ct += 1
    print('\n.')

def wait_high(pin):
    ct = 0
    while not pin():
        spin(ct)
        ct += 1
    print('\n.')

print('inputs')
for p in range(0,23+1):
    pycom.rgbled(0x001100)
    print('\nPin', p)
    time.sleep(1)
    pycom.rgbled(0x070700)
    if p == 0:
        print('RX0')
        continue
    elif p == 1:
        print('TX0')
        continue

    if p = 9:
        print('Expb LED')
    pin = Pin('P' + str(p), mode=Pin.IN)

    for i in range(3):
        wait_low(pin)
        print('low')
        wait_high(pin)
        print('high')
