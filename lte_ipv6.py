https://forum.pycom.io/topic/5777/using-gpy-with-ipv6

https://pycomiot.atlassian.net/browse/PYCSD-1971

from network import LTE
lte = LTE()
lte.init()
lte.send_at_cmd('AT+CFUN=0')
lte.send_at_cmd('AT+CGDCONT=1,"IPV6","iot"')
lte.send_at_cmd('AT+CFUN?')
lte.send_at_cmd('AT+CFUN=1')
lte.send_at_cmd('AT+CFUN?')
lte.send_at_cmd('AT+CREG?')
