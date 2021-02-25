class RingBuffer:
    def __init__(self, size=100):
        self.size = size
        self.buf = [0] * size
        self.fill = 0
        self.total = 0
        self.next = 0
    def push(self, val):
        # update buf and total
        self.total -= self.buf[self.next]
        self.buf[self.next] = val
        self.total += val
        # update curr and fill
        self.next += 1
        if self.next > self.fill:
            # print('f', self.fill)
            self.fill = self.next
        if self.next >= self.size:
            # print('x')
            self.next = 0
        # print(self.size, self.fill, self.next, self.total, self.avg()) # self.buf)
    def avg(self):
        if self.fill == 0:
            return 0
        return self.total / self.fill
    def full(self):
        return self.fill >= self.size

class NoiseFilter:
    def __init__(self, precision=0, values=10, averages=3):
        self.vals = RingBuffer(values)
        self.avgs = RingBuffer(averages)
        self.prec = precision
    def push(self, val):
        self.avgs.push( round(self.vals.avg(), self.prec) )
        self.vals.push(val)
        print(self.avgs.buf)



if __name__ == "__main__":
    from random import *
    import time

    b = RingBuffer(1000)
    r = 2
    r_range = 0.3
    last = None
    for x in range(100000):
        v = round(random() * r_range,r)
        b.push(v)
        a = round(b.avg(),r)
        if a != last:
            print('\n', x, a, end=' ')
            last = a
        else:
            print('.', end='')
        time.sleep(0.1)

    # nf = NoiseFilter(averages=10, precision=1)
    # for x in range(20):
    #     nf.push(random())
