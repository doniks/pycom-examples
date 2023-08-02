import machine
import binascii
import gc
import micropython
import pycom

def mem(verbose=False):
    if verbose:
        print("{:18} {:9}".format("GC total ", gc.mem_alloc() + gc.mem_free()))
        micropython.mem_info()
        print("{:18} {:9}".format("mp stack use", micropython.stack_use()))
    print("{:18} {:9}".format("GC free", gc.mem_free()))
    print("{:18} {:9}".format("heap internal free", pycom.get_free_heap()[0]))
    print("{:18} {:9}".format("heap external free", pycom.get_free_heap()[1]))

def mem_stress():
    bufs = []
    ct = 0
    size = 1024 * 10
    print("stress", size)
    while True:
        i = ct % 0xff
        bufs.append(bytearray([i] * size))
        print(ct, (ct * size)/1024, gc.mem_alloc(), gc.mem_free())
        ct+=1

if __name__ == '__main__':
    import binascii
    import machine
    uid = binascii.hexlify(machine.unique_id())
    name = os.uname().sysname.lower() + '-' + uid.decode("utf-8")[-4:]
    print(name)

    mem()
    # mem_stress()
