import pycom
import machine

#########################################################
##### SWITCHING FILESYSTEM MEANS LOSING ALL FILES ! #####
#########################################################

def switch_to(name, type):
    current_name = pycom.bootmgr()[1]
    if current_name != name:
        print("Switch from", current_name, "to", name)
        pycom.bootmgr(fs_type=type)
        machine.reset()
    else:
        print("Nothing to do, already on", name)

def switch_to_FAT():
    switch_to("FAT", pycom.FAT)

def switch_to_LittleFS():
    switch_to("LittleFS", pycom.LittleFS)

def switch_to_other():
    current_name = pycom.bootmgr()[1]
    if current_name == "FAT":
        switch_to_LittleFS()
    else:
        switch_to_FAT()

def get():
    fs = pycom.bootmgr()[1]
    print('FS:', fs)

if __name__ == "__main__":
    get()
    if False:
        switch_to_other()
