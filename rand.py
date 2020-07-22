import machine
max = 0xffffff

# FYI: there is also os.urandom() which gives pseudo random numbers
def prand():
    return machine.rng() / max

def prandi(low, high):
    delta = high - low
    return int(low + rand()*delta)

def rng():
    rng_max = 0xffffff
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



def rand():
    r0 = rng()
    r1 = r0 / ( rng_max + 1 )
    # print("rand:", r0, r1)
    if r1 < 0:
        raise Exception("rand(): r1=({}) < 0".format(r1))
    if r1 >= 1.0:
        raise Exception("rand(): r1=({}) >= 0".format(r1))
    return r1

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


# if __name__ == "__main__":
    # import time
    # ct = dict()
    # l = 4
    # h = 9
    # n = 100
    # for i in range(l,h):
    #     ct[i] = 0
    #
    # t = time.ticks_ms()
    # for x in range(0,n):
    #     r = randi(l,h)
    #     ct[r] += 1
    # print("took", (time.ticks_ms() - t)/ 1000, "sec for", n)
    #
    # print("distribution", ct)

for i in range(0,10):
    r = rngboot()
    print(r, hex(r))
