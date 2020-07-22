import ubinascii
import machine
import os

def int_to_bytes(i, len):
    return i.to_bytes(len, "big")


if __name__ == "__main__":

    r = machine.rng()
    b = int_to_bytes(r,3)
    print("int to bytes:", hex(r), "=", r, "->", end="")
    # print(b[0])
    # print(ubinascii.hexlify(b))
    for i in range(0, len(b)):
        print(ubinascii.hexlify(b[i:i+1]), end=" ")
    print()

    b = os.urandom(3)
    i = int.from_bytes(b, "big")
    print("bytes to int:", binascii.hexlify(b), "->", hex(i), "=", i)
