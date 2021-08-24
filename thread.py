import _thread
import time
import machine
import gc
import micropython
import pycom

keep_going = True

mpy_heap_free = gc.mem_free()
mpy_stack_used = micropython.stack_use()
internal_heap_free = pycom.get_free_heap()[0]
external_heap_free = pycom.get_free_heap()[1]

def mem():
    global mpy_heap_free, mpy_stack_used, internal_heap_free, external_heap_free

    # machine.info()

    #print("MPy heap free=", gc.mem_free(), "alloc=", gc.mem_alloc(), "total=", gc.mem_alloc() + gc.mem_free(), "diff=", mpy_heap_free - gc.mem_free())
    # micropython.mem_info()
    print("MPy heap free=     {:>8} diff={:>6}".format(gc.mem_free(),gc.mem_free() - mpy_heap_free))
    print("MPy stack used=    {:>8} diff={:>6}".format(micropython.stack_use(), micropython.stack_use() - mpy_stack_used))
    print("internal heap free={:>8} diff={:>6}".format(pycom.get_free_heap()[0], pycom.get_free_heap()[0] - internal_heap_free))
    print("external heap free={:>8} diff={:>6}".format(pycom.get_free_heap()[1], pycom.get_free_heap()[1] - external_heap_free))

    mpy_heap_free = gc.mem_free()
    mpy_stack_used = micropython.stack_use()
    internal_heap_free = pycom.get_free_heap()[0]
    external_heap_free = pycom.get_free_heap()[1]

def doit(id, ct, level):
    print(id, ct, level, micropython.stack_use())
    if level > 10:
        return
    else:
        doit(id, ct, level+1)
    time.sleep(0.5)


def th_func(delay, id):
    # if id == 0:
    #     print("Start thread in thread %d" %(id))
    #     _thread.start_new_thread(th_func, (delay+1,1000+id))
    ct = 0
    # for i in range(10):
    while True:
        time.sleep(delay)
        # print('id=%d\t ct=%d st=%d' % (id, ct, micropython.stack_use()) )
        # doit(id, ct, 0)
        ct += 1
    print('id=%d\t ct=%d --- end' % (id, ct) )


# create threads with increasing delays
def thread_test():
    mem()
    n = 24
    # n = 2
    # GPy base core dumps at 25 in safe boot mode
    # , or 21?
    _thread.stack_size(8*1024) # default is 5k
    print("Starting %d threads...." %(n))
    for i in range(n):
        print('Start thread', i)
        time.sleep(1)
        _thread.start_new_thread(th_func, (i + 1, i))
        time.sleep(1)
        mem()
        time.sleep(1)
        #achine.info()
        # mem()

    if False:
        keep_going = False

if __name__ == "__main__":
    # machine.info()
    print("start")
    _thread.stack_size(4 * 1024)
    try:
        pass
        thread_test()
        # while True:
        #     pass
    except Exception as e:
        print("Exception during thread_test:", type(e), e)
    # print("sleep")
    # for i in range(5):
    #     print("main stack_use=", micropython.stack_use())
    #     time.sleep(5)
    # print("end")
    # keep_going = False
