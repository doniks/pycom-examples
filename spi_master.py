from machine import SPI
from machine import Pin
import os
import sys
import time

def log(fct):
    last = None
    while True:
        v = fct()
        if v != last:
            print(time.time(), v)
            last = v
        time.sleep(1)

p_mosi = 'P11'
p_miso = 'P14'
# p_miso = 'P16' # ... doesn't work ... why? on a gpy
p_clk  = 'P10'
# p_cs   =  'P3'

# KSZ8851
p_mosi = 'P23'
p_miso = 'P17'
p_clk  = 'P21'

# esp32 HSPI
p_mosi = 'P10' # gpio013
p_miso =  'P9' # gpio012
p_clk  = 'P23' # gpio014



# cs   = Pin(p_cs,  mode=Pin.OUT, value=1)
# clk  = Pin(p_clk, mode=Pin.OUT, value=0)
# mosi = Pin(p_mosi, mode=Pin.OUT)
# miso = Pin(p_miso, mode=Pin.IN, pull=Pin.PULL_UP)

#            CLK,   MOSI   MISO
# spi_pins = ('P22', "P11", "P16")
spi_pins = (p_clk, p_mosi, p_miso)

speeds = [ 10_000, 100_000, 1_000_000, 10_000_000, 11_000_000, 12_000_000, 13_000_000, 15_000_000, 20_000_000, 40_000_000 ]
speeds = [ 10_000_000, 11_000_000, 11_250_000, 11_375_000, 11_500_000, 12_000_000, 13_000_000]
ok   = [0] * len(speeds)
fail = [0] * len(speeds)
# br = 20_000_000 #  20 M
# br = 10_000_000 #  10 M
# br =  2_000_000 #   2 M
# br =  1_000_000 #   1 M
br =    200_000 # 200 K
# br =    100_000 # 100 K
# br =     10_000 #  10 K
buffer_w = bytearray([0x1, 0x2, 0x3, 0x1,0x2,0x3, 0x1,0x2,0x3, 0x66])
# buffer_w = bytearray([0xa,0xa,0xa, 0xa,0xa,0xa, 0xa,0xa,0xa, 0])
#buffer_w = bytearray([0xa,0xe,0xa, 0xe,0xa,0xe, 0xa,0xe,0xa, 0])
buffer_r = bytearray(len(buffer_w))
while True:
    for s in range(len(speeds)):
        spi = SPI(0, SPI.MASTER, baudrate=speeds[s], polarity=0, phase=0, pins=spi_pins)
        for i in range(10):
            # cs(0)
            l = spi.write_readinto(buffer_w, buffer_r)
            # cs(1)
            # print(buffer_r)
            # print(buffer_r == buffer_w)
            if buffer_r == buffer_w:
                ok[s] += 1
            else:
                fail[s] += 1
            time.sleep(0.01)
    for s in range(len(speeds)):
        print("{}:{}/{}".format(speeds[s],ok[s],fail[s]), end=' ')
    print()

sys.exit()
log(miso)
