import ubinascii
import machine

r = machine.rng()
b = r.to_bytes(3, "big")
print(r, "->", end="")
# print(b[0])
# print(ubinascii.hexlify(b))
for i in range(0, len(b)):
    print(ubinascii.hexlify(b[i:i+1]), end=" ")
