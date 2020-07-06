import os
import binascii
import machine

def print_wifi_mode(m):
    if m == WLAN.AP:
        print("AP", end='')
    elif m == WLAN.STA:
        print("STA", end='')
    elif m == WLAN.STA_AP:
        print("STA_AP", end='')


print("===== machine ====================================")
print("unique_id", binascii.hexlify(machine.unique_id()))
try:
    print("temperature", machine.temperature())
except:
    pass
# print("rng", machine.rng())

print("===== os =========================================")
print("sysname", os.uname().sysname) # e.g., GPy
print("release", os.uname().release) # e.g., 1.20.1.r1
print("release", os.uname().version)
print("uname", os.uname())

import pycom
print("===== pycom ======================================")
try:
    print("free_heap", pycom.get_free_heap())
    # print("bootmgr", pycom.bootmgr())
    print("partition", pycom.bootmgr()[0])
    print("fs_type", pycom.bootmgr()[1])
    print("free", os.getfree('/flash'))
    print(pycom.bootmgr()[2]) # safeboot
    print(pycom.bootmgr()[3]) # status
    print("ota_slot", hex(pycom.ota_slot()))
    if (pycom.ota_slot() == 0x210000):
        print("ota_slot is", "'ota_0' in 'new' 8MB layout")
    elif (pycom.ota_slot() == 0x1A0000):
        print("ota_slot is", "'ota_0' in 'old' 4MB layout")
    elif (pycom.ota_slot() == 0x10000):
        print("ota_slot is", "'Factory'")
    else:
        raise Exception("Unkown ota_slot"+ str(pycom.ota_slot()))
except:
    pass

try:
    print("smart_config_on_boot", pycom.smart_config_on_boot())
except:
    pass
try:
    print("pybytes_on_boot", pycom.pybytes_on_boot())
except:
    pass

try:
    print("wifi_on_boot", pycom.wifi_on_boot())
except:
    pass
from network import WLAN
try:
    m = pycom.wifi_mode_on_boot()
    print("wifi_mode_on_boot", m, end=" ")
    print_wifi_mode(m)
    print()
except:
    pass
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
wlan = WLAN()
try:
    print("sta_mac", binascii.hexlify(wlan.mac().sta_mac))
    print("ap_mac", binascii.hexlify(wlan.mac().ap_mac))
except:
    print("mac", binascii.hexlify(wlan.mac()))
print("is_connected", wlan.isconnected())
print("ssid", wlan.ssid())
print("bssid", binascii.hexlify(wlan.bssid()))
try:
    print("country", wlan.country())
except:
    pass
print("ifconfig", wlan.ifconfig())
print('IP:', wlan.ifconfig()[0])
print("mode", wlan.mode(), end=' ')
print_wifi_mode(wlan.mode())
print()

try:
    print("===== lora =======================================")
    from network import LoRa
    lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
    print("mac", binascii.hexlify(lora.mac()))
    print(lora.frequency())
    print(lora.has_joined())
    print(lora.tx_power())
    print(lora.power_mode())
    #print(lora.stats())
except:
    pass

try:
    print("===== sigfox =====================================")
    from network import Sigfox
    sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1)
    print("id", binascii.hexlify(sigfox.id()))
    print("mac", binascii.hexlify(sigfox.mac()))
    print("pac", binascii.hexlify(sigfox.pac()))
    print("frequencies", sigfox.frequencies())
except:
    pass

try:
    print("===== lte ========================================")
    from network import LTE
    lte = LTE()
    print("imei", lte.imei())
    print("iccid", lte.iccid())
    print("is_connected", lte.isconnected())
    print("ue_coverage", lte.ue_coverage())
    def send_at_cmd_pretty(cmd):
        return lte.send_at_cmd(cmd).replace('\r', '').strip().replace('\n\n','\n')
    print('AT+CGCONTRDP=1', send_at_cmd_pretty('AT+CGCONTRDP=1'))
    print('AT!="config"', send_at_cmd_pretty('AT!="ifconfig"'))
    print("time", lte.time())
except:
    pass

try:
    print("===== eth ========================================")
    from network import ETH
    eth = ETH()
    print("mac", binascii.hexlify(eth.mac()))
except:
    pass
