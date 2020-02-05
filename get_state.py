import os
import ubinascii
import machine
print("===== machine ====================================")
print("unique_id", ubinascii.hexlify(machine.unique_id()))
print("temperature", machine.temperature())
# print("rng", machine.rng())

print("===== os =========================================")
print("sysname", os.uname().sysname) # e.g., GPy
print("release", os.uname().release) # e.g., 1.20.1.r1
print("uname", os.uname())

import pycom
print("===== pycom ======================================")
# print("bootmgr", pycom.bootmgr())
print("partition", pycom.bootmgr()[0])
print("fs_type", pycom.bootmgr()[1])
print("safeboot", pycom.bootmgr()[2])
print("status", pycom.bootmgr()[3])
print("ota_slot", hex(pycom.ota_slot()))
if (pycom.ota_slot() == 0x210000):
    print("ota_slot is", "'ota_0' in 'new' 8MB layout")
elif (pycom.ota_slot() == 0x1A0000):
    print("ota_slot is", "'ota_0' in 'old' 4MB layout")
elif (pycom.ota_slot() == 0x10000):
    print("ota_slot is", "'Factory'")
else:
    raise Exception("Unkown ota_slot"+ str(pycom.ota_slot()))

print("wifi_on_boot", pycom.wifi_on_boot())
try:
    print("wifi_ssid", pycom.wifi_ssid())
    print("wifi_pwd", pycom.wifi_pwd())
except:
    pass
try:
    # v1.20.1.r1
    print("wifi_ssid_sta", pycom.wifi_ssid_sta())
    print("wifi_pwd_sta", pycom.wifi_pwd_sta())
    print("wifi_ssid_ap", pycom.wifi_ssid_ap())
    print("wifi_pwd_ap", pycom.wifi_pwd_ap())
except:
    pass


print("===== wlan =======================================")
from network import WLAN
wlan = WLAN()
print("is_connected", wlan.isconnected())
print("bssid", ubinascii.hexlify(wlan.bssid()))
print("country", wlan.country())
print("ifconfig", wlan.ifconfig())
print('IP:', wlan.ifconfig()[0])
print("mode", wlan.mode(), "(STA=", WLAN.STA, "AP=", WLAN.AP, ")")


print("===== lora =======================================")
from network import LoRa
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
print("mac", ubinascii.hexlify(lora.mac()))
print(lora.frequency())
print(lora.has_joined())
print(lora.tx_power())
print(lora.power_mode())
#print(lora.stats())


print("===== sigfox =====================================")
from network import Sigfox
sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1)
print("id", ubinascii.hexlify(sigfox.id()))
print("mac", ubinascii.hexlify(sigfox.mac()))
print("pac", ubinascii.hexlify(sigfox.pac()))
print("frequencies", sigfox.frequencies())

try:
    print("===== lte ========================================")
    from network import LTE
    lte = LTE()
    print("imei", lte.imei())
    print("is_connected", lte.isconnected())
    print("ue_coverage", lte.ue_coverage())
    print("iccid", lte.iccid())
    print("time", lte.time())
except:
    pass
