import machine
rng_max = 0xffffff

# FYI: there is also os.urandom() which gives pseudo random numbers

# def prand():
#     return machine.rng() / rng_max
#
# def prandi(low, high):
#     delta = high - low
#     return int(low + rand()*delta)

def rng():
    r0 = machine.rng()
    if r0 > rng_max:
        # raise Exception("rand(): r0=({}) > rng_max=({})".format(hex(r0), hex(rng_max)))
        print("ERROR: rand(): r0=({}) > rng_max=({}), retrying".format(hex(r0), hex(rng_max)))
        return rng()
    else:
        return r0

def rngboot():
    r0 = rng()
    if r0 == 0x021611:
        print("skip 0x021611")
        return rngboot()
    elif r0 == 0x271611:
        print("skip 0x021611")
        return rngboot()
    else:
        return r0


# returns a random floating point number from [low to high]
# that is inclusive low and inclusive high
def rand(low=0.0, high=1.0):
    if high < low:
        raise Exception("high value is lower than low value")
    if high == low:
        return low

    r0 = rng()
    r01 = r0 / ( rng_max  ) # why+1? # + 1 )
    # print("rand:", r0, r1)
    if r01 < 0:
        raise Exception("rand(): r1=({}) < 0".format(r1))
    if r01 >= 1.0:
        raise Exception("rand(): r1=({}) >= 0".format(r1))
    delta = high - low   # e.g. low=1, high=4, delta=3
    return low + delta * r01

# returns a random integer from [low, high)
# that is inclusive low, but exclusive high
def randi(low, high):
    if low != int(low):
        raise Exception("low value is not an int")
    if high != int(high):
        raise Exception("high value is not an int")
    if high < low:
        raise Exception("high value is lower than low value")
    if high == low:
        return low

    delta = high - low   # e.g. low=1, high=4, delta=3
    r0 = rand()          # [0  , 1  )
    r1 = r0 * delta      # [0  , 3  )
    r2 = low + r1        # [1  , 4  )
    r3 = r2 - 0.49999    # (0.5, 3.5)
    r4 = round(r3)       # {1,2,3}
    r5 = int(r4)
    # print("randi:", low, high, r0, r1, r2, r3, r4, r5)
    return r5

def randb():
    return bool(randi(0,2))

def rand_test(low=4, high=9, num=10000):
    import time
    ct = dict()
    # for i in range(low, high):
    #     ct[i] = 0

    t = time.ticks_ms()
    for x in range(0, num):
        if False:
            # test ints
            r = randi(low, high)
        elif False:
            # test floats
            r = rand(low, high)
            r = round(r)
        else:
            # test bools
            r = randb()
        try:
            ct[r] += 1
        except:
            ct[r] = 1
    #print("took", (time.ticks_ms() - t)/ 1000, "sec for", num, "random numbers in ", low, ", ", high)

    # print("distribution", ct)
    # print({key: value for key, value in sorted(my_dict.items(), key=lambda item: item[1])})
    # print("distribution", dict(sorted(ct.items(), key=lambda item: item[0])))
    print("distribution", end=" ")
    for k in sorted(ct.keys()):
        print(k, ": ", ct[k], sep="", end=", ")
    print()

if __name__ == "__main__":
    print(rand(), randi(1,180))
    # for i in range(0,10):
    #     r = rngboot()
    #     print(r, hex(r))
    # rand_test()
