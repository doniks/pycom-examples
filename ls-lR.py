import os
import pycom

def ls(dir):
    contents = os.listdir(dir)
    for c in contents:
        d = dir + "/" + c
        if dir == "/":
            d = dir + c
        try:
            print(d, "[", len(os.listdir(d)), "]" )
            ls(d)
        except:
            print(d)


print("fs_type:", pycom.bootmgr()[1])
ls("/")
