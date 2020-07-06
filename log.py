import os
import binascii
import machine
import time

logfile = "/flash/log_" + os.uname().sysname + "_" + binascii.hexlify(machine.unique_id()).decode() + ".log"

def log(m):
    f = open(logfile, 'a')
    t = "[" + str(time.time()) + "] "
    f.write(t)
    f.write(m)
    f.write('\n')
    f.close()
    print(t, m, sep="")

def cat():
    f = open(logfile, 'r')
    print(f.read())
    f.close()

def rm():
    try:
        print("remove", logfile )
        os.remove(logfile)
        print("done")
    except Exception as e:
        print("couldn't remove {}: {}".format(logfile,e))
        pass