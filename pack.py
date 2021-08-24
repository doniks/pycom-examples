import struct


# b signed char     # 1
# B unsigned char   # 1
# h short           # 2
# H unsigned short  # 2
# l long            # 4
# i int             #
# f float
# q long long int
# Q

payload = 0xaf
payload = -99
for f in ['b', 'B', 'h', 'l', 'i', 'f', 'q', 'Q']:
    p = struct.pack(f,payload)
    print(payload, f, len(p), p, struct.unpack(f,p))


fmt = 'hhl'
p = struct.pack(fmt, 5 , 10, 15)
print(p)
print(struct.unpack(fmt, p))

fmt = 'iii'
p = struct.pack(fmt, 10, 20, 30)
print(var, struct.unpack(fmt, p))


r = machine.rng() # 3 bytes
p = struct.pack('L', r)
u = struct.unpack('BBB', p)
print(r, binascii.hexlify(p), u)
print(r, binascii.hexlify(p), [hex(x) for x in u])
