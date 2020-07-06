import _thread
import time
import machine

keep_going = True

def th_func(delay, id):
    ct = 0
    while keep_going:
        time.sleep(delay)
        print('Running thread id=%d, ct=%d' % (id, ct) )
        ct += 1
    print('End thread id=%d' %(id))


def thread_test():
    n = 20
    print("Starting %d threads...." %(n))
    for i in range(n):
        _thread.start_new_thread(th_func, (i + 1, i))
        print(i)
        time.sleep(0.2)
        machine.info()

    if False:
        keep_going = False

if __name__ == "__main__":
    # machine.info()
    print("sd")
    thread_test()
    print("adf")
