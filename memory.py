import machine
import binascii
import gc
import micropython
import pycom



def mem():
    machine.info()
    print("GC free=", gc.mem_free(), "alloc=", gc.mem_alloc(), "total=", gc.mem_alloc() + gc.mem_free())
    # micropython.mem_info()
    print("mp stack", micropython.stack_use())
    print("heap internal", pycom.get_free_heap()[0])
    print("heap external", pycom.get_free_heap()[1])

def stress():
    bufs = []
    ct = 0
    size = 1024 * 10
    print("stress", size)
    while True:
        i = ct % 0xff
        bufs.append(bytearray([i] * size))
        print(ct, (ct * size)/1024, gc.mem_alloc(), gc.mem_free())
        ct+=1


import binascii
import machine
uid = binascii.hexlify(machine.unique_id())
name = os.uname().sysname.lower() + '-' + uid.decode("utf-8")[-4:]
print(name)

mem()
stress()
