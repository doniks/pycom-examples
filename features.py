import time
from machine import RTC
import machine
import binascii
import pycom

def features(on=None):
    if on is None:
        print("heartbeat   ", pycom.heartbeat_on_boot())
        print("lte         ", pycom.lte_modem_en_on_boot())
        try:
            print("pybytes     ", pycom.pybytes_on_boot())
        except:
            pass
        try:
            print("smart_config", pycom.smart_config_on_boot())
        except:
            pass
        print("wdt         ", pycom.wdt_on_boot())
        print("wifi        ", pycom.wifi_on_boot())
    else:
        print("configure all features as", on)
        pycom.heartbeat_on_boot(on)
        pycom.lte_modem_en_on_boot(on)
        try:
            pycom.pybytes_on_boot(on)
        except:
            pass
        try:
            pycom.smart_config_on_boot(on)
        except:
            pass
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
        # print
        print(pycom.heartbeat_on_boot())
        print(pycom.lte_modem_en_on_boot())
        print(pycom.pybytes_on_boot())
        print(pycom.smart_config_on_boot())
        print(pycom.wdt_on_boot())
        print(pycom.wifi_on_boot())
        # off
        pycom.heartbeat_on_boot(False)
        import pycom
        pycom.lte_modem_en_on_boot(False)
        pycom.wdt_on_boot(False)
        pycom.wifi_on_boot(False)
        pycom.smart_config_on_boot(False)
        pycom.pybytes_on_boot(False)
        # on
        pycom.heartbeat_on_boot(True)
        pycom.lte_modem_en_on_boot(True)
        pycom.pybytes_on_boot(True)
        pycom.smart_config_on_boot(True)
        pycom.wdt_on_boot(True)
        pycom.wifi_on_boot(True)
