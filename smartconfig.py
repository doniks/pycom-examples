#https://forum.pycom.io/topic/6347/wlan-smartconfig/2
from network import WLAN

def conf(msg): print('smart config', msg)

wlan = WLAN(mode=WLAN.STA, antenna=WLAN.INT_ANT)
if wlan.isconnected(): print('connected')
wlan.callback(trigger=WLAN.SMART_CONF_DONE, handler=conf('done'))
wlan.callback(trigger=WLAN.SMART_CONF_TIMEOUT, handler=conf('timed out'))
print('try smartConfig'); wlan.smartConfig()
