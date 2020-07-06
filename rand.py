import machine
max = 0xffffff

# TODO: there is os.urandom() might be easier
def rand():
    return machine.rng() / max

def randi(low, high):
    delta = high - low
    return int(low + rand()*delta)

ct = dict()
l = 4
h = 9
for i in range(l,h):
    ct[i] = 0

for x in range(0,10000):
    r = randi(4,9)
    ct[r] += 1

print(ct)
