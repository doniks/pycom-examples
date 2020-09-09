import ubinascii
import machine
import os

def int_to_bytes(i, len):
    return i.to_bytes(len, "big")

def bytes_to_int(b):
    return int.from_bytes(b, "big")

def str_to_bytes(s):
    return bytes(s, "utf-8")

def bytes_to_str(b):
    return b.decode('utf-8')


# An easy way that I was able to do a variable length when packing a string is:
# pack('{}s'.format(len(string)), string)
# when unpacking it is kind of the same way
# unpack('{}s'.format(len(data)), data)

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
    #i = int.from_bytes(b, "big")
    i = bytes_to_int(b)
    print("bytes to int:", binascii.hexlify(b), "->", hex(i), "=", i)
