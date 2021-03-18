import machine
import os
import binascii
uid = binascii.hexlify(machine.unique_id())
name = os.uname().sysname.lower() + '-' + uid.decode("utf-8")[-4:]
print(os.uname().sysname, uid, name, "wlan_ap.py")

from network import WLAN
wlan = WLAN(mode=WLAN.AP, ssid=name, auth=(WLAN.WPA2, "8letters"))
print(wlan.ifconfig(id=1)) #id =1 signifies the AP interface
