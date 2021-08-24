import time
from network import MDNS
# As a first step connection to network should be estbalished, e.g. via WLAN

# Initialize the MDNS module
try:
  MDNS.init()
except Exception as e:
  print(e)

# Perform a query for 2000 ms
service_type = '_http'
# service_type = '_ftp'
# service_type = 'telnet'
proto = MDNS.PROTO_UDP
proto = MDNS.PROTO_TCP
q = MDNS.query(2000, service_type, proto)

# Print out the query's result
if q is not None:
    for elem in q:
        print(elem.instance_name())
        print(elem.hostname())
        print(elem.addr())
        print(elem.port())
        print(elem.txt())
