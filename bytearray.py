from binascii import hexlify

def dostuffparam(b):
    b[0] = 0x99

def dostuff():
    buf[1] = 0xaa

def dostuffglobal():
    global buf
    buf[2] = 0xbb

buf = bytearray(10)
for i in range(len(buf)):
    buf[i] = i

print(hexlify(buf))
dostuff()
print(hexlify(buf))
dostuffparam(buf)
print(hexlify(buf))
dostuffglobal()
print(hexlify(buf))
