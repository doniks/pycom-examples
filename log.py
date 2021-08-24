import os
import binascii
import machine
import time

name = os.uname().sysname.lower() + '-' + binascii.hexlify(machine.unique_id()).decode("utf-8")[-4:]
logbase = "/flash/log_" + name + "_"
logfile = logbase + "0.log"
logmax = 2

def log(*messages):
    # messages = ('eh', 'yo', 666, 'whazzzup!?')
    f = open(logfile, 'a')
    t = "[" + str(time.time()) + "]"
    f.write(t)
    f.write(' ')
    for m in messages:
        print(m)
        f.write(str(m))
        f.write(' ')
    f.write('\n')
    f.close()
    print(t, *messages)

def logcat():
    print("logcat", logfile )
    f = open(logfile, 'r')
    print(f.read())
    f.close()

def logrm():
    try:
        print("logrm", logfile )
        os.remove(logfile)
        print("done")
    except Exception as e:
        print("couldn't remove {}: {}".format(logfile,e))
        pass

def logrotate():
    print("logrotate", logbase, logmax)
    # from shell import *
    f = logbase + str(logmax) + ".log"
    try:
        os.remove(f)
        print("remove", f)
    except Exception as e:
        # print("doesn't exist:", f, e)
        pass
    for l in range(logmax,0,-1):
        old = logbase + str(l-1) + ".log"
        new = logbase + str(l) + ".log"
        try:
            mv(old, new)
            print("mv", l-1, l, old, new)
        except Exception as e:
            # print("doesn't exist:", old, e)
            pass



if __name__ == "__main__":
    # log('eh', 'yo', 666, 'whazzzup!?')
    # print('---')
    # catlog()
    logrotate()
    if False:
        rmlog()
