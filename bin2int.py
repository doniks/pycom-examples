
def binstring2int(s):
    return int(s,2)

def hexstring2int(s):
    return int(s,16)

def int2hexstring(i):
    #return "%x"%i # 10 -> a
    return hex(i) # 10 -> 0xa



print(2)
print(0x9)
print(0xa)
print(binstring2int("0101"))
print(int("0xa"))
print(hexstring2int("a"))
print(int2hexstring(10))
