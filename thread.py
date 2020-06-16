import _thread
import time

def th_func(delay, id):
    ct = 0
    while True:
        time.sleep(delay)
        print('Running thread id=%d, ct=%d' % (id, ct) )
        ct += 1

for i in range(5):
    _thread.start_new_thread(th_func, (i + 1, i))
