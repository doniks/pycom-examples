import os
import binascii
import machine
import pycom
from network import WLAN
uid = binascii.hexlify(machine.unique_id())
name = os.uname().sysname.lower() + '-' + uid.decode("utf-8")[-4:]
print(os.uname().sysname, uid, name, "wlan_ap.py")

wlan = WLAN(mode=WLAN.AP, ssid=name, auth=(WLAN.WPA2, "8letters"))
print(wlan.ifconfig(id=1)) #id =1 signifies the AP interface

if False:
    print('wifi_on_boot', pycom.wifi_on_boot())
    print('wifi_mode_on_boot', pycom.wifi_mode_on_boot())
    print('AP', WLAN.AP)
    print('wifi_ssid_ap', pycom.wifi_ssid_ap())
    pycom.wifi_on_boot(True)
    pycom.wifi_mode_on_boot(WLAN.AP)
    pycom.wifi_ssid_ap('peter2-test')
    machine.reset()
