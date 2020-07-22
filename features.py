import time
from machine import RTC
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

def features():
    print("heartbeat", pycom.heartbeat_on_boot())
    print("lte", pycom.lte_modem_en_on_boot())
    print("pybytes", pycom.pybytes_on_boot())
    print("smart_config", pycom.smart_config_on_boot())
    print("wdt", pycom.wdt_on_boot())
    print("wifi", pycom.wifi_on_boot())

def on():
    pycom.heartbeat_on_boot(True)
    pycom.lte_modem_en_on_boot(True)
    pycom.pybytes_on_boot(True)
    pycom.smart_config_on_boot(True)
    pycom.wdt_on_boot(True)
    pycom.wifi_on_boot(True)

def off():
    pycom.heartbeat_on_boot(False)
    pycom.lte_modem_en_on_boot(False)
    pycom.pybytes_on_boot(False)
    pycom.smart_config_on_boot(False)
    pycom.wdt_on_boot(False)
    pycom.wifi_on_boot(False)

import binascii
import machine
uid = binascii.hexlify(machine.unique_id())
name = os.uname().sysname.lower() + '-' + uid.decode("utf-8")[-4:]
print(name)

mem()
features()
