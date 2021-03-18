import framebuf
import math
import sys
from binascii import hexlify

def p():
    for y in range(height):
        for x in range(width):
            if fbuf.pixel(x,y):
                print('#', end='')
            else:
                print(' ', end='')
            # print(fbuf.pixel(x,y), end=' ')
        print('|')

def raw_1bit(w,h, buf, sep=''):
    for y in range(h):
        for x in range(w):
            print("{0:08b}".format(buf[y*w + x]), end=sep)
        print('|')

def raw_buf_1bit(buf, bytes_per_row=1, sep='', pretty=False):
    ct = 0
    for b in buf:
        binary = "{0:08b}".format(b)
        if pretty:
            display = ''
            for c in binary:
                if c == '0':
                    display += ' '
                else:
                    display += '1'
        else:
            display = binary
        print(display, end=sep)
        ct += 1
        if ct % bytes_per_row == 0:
            print()

# pixel dimensions (make it multiples of 8)
width = 80
height = 24
format = framebuf.MONO_HLSB
# format = framebuf.MONO_VLSB
bits_per_pixel = None
if format == framebuf.MONO_HLSB or format == framebuf.MONO_VLSB:
    bits_per_pixel = 8;
# format = None

# byte dimensions
# FrameBuffer needs
# - 2 bytes for every RGB565 pixel
# - 1 bit for every MONO_HLSB pixel

buf = bytearray(math.ceil(width * height / bits_per_pixel))
fbuf = framebuf.FrameBuffer(buf, width, height, format)
fbuf.fill(0)
fbuf.text("Hello", 0,0, 1)
fbuf.text("world", 12,8, 1)
fbuf.rect(      2, 17, 20, 7, 1)
fbuf.fill_rect( 5, 19, 14, 3, 1)
fbuf.fill_rect( 24, 17, 14, 6, 1)
fbuf.line(24,17,38,23,0)
print('-----------------')
p()
print('-----------------')
print(hexlify(buf))
if format == framebuf.MONO_HLSB:
    print("HLSB - landscape")
    raw_buf_1bit(math.ceil(width/8), pretty=True)
elif format == framebuf.MONO_VLSB:
    print("VLSB - portrait")
    raw_buf_1bit(pretty=True)
