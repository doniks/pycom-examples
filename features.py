import time
from machine import RTC
import machine
import binascii
import pycom

def features(on=None):
    if on is None:
        print("heartbeat   ", pycom.heartbeat_on_boot())
        print("lte         ", pycom.lte_modem_en_on_boot())
        print("pybytes     ", pycom.pybytes_on_boot())
        print("smart_config", pycom.smart_config_on_boot())
        print("wdt         ", pycom.wdt_on_boot())
        print("wifi        ", pycom.wifi_on_boot())
    else:
        print("configure all features as", on)
        pycom.heartbeat_on_boot(on)
        pycom.lte_modem_en_on_boot(on)
        pycom.pybytes_on_boot(on)
        pycom.smart_config_on_boot(on)
        pycom.wdt_on_boot(on)
        pycom.wifi_on_boot(on)
        features(None)


if __name__ == '__main__':
    import binascii
    import machine
    uid = binascii.hexlify(machine.unique_id())
    name = os.uname().sysname.lower() + '-' + uid.decode("utf-8")[-4:]
    print(name)

    features()
    if False:
        features(True) # turn everything on
        features(False) # turn everything off
