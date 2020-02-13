from network import WLAN
wlan = WLAN()
print("wlan.isconnected", wlan.isconnected())
if wlan.isconnected():
    print('IP:', wlan.ifconfig()[0])

try:
    from network import LTE
    lte = LTE()
    print("imei", lte.imei())
    print("lte.isconnected", lte.isconnected())
    # print("ue_coverage", lte.ue_coverage())
except:
    print("no LTE")
