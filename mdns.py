import time
from network import MDNS
# As a first step connection to network should be estbalished, e.g. via WLAN

def mdns(name=None, txt=None, instance=None):
    devname = os.uname().sysname.lower() + '-' + binascii.hexlify(machine.unique_id()).decode("utf-8")[-4:]
    if name is None:
        name = devname
    print(devname, 'mdns', name)

    # Initialize the MDNS module
    try:
        MDNS.init()
    except:
        MDNS.deinit()
        time.sleep(1)
        MDNS.init()
    # Set the hostname and instance name of this device
    MDNS.set_name(hostname = name, instance_name = name + '-instance')
    MDNS.add_service("telnet", MDNS.PROTO_TCP, 23)
    # MDNS.add_service("ftp", MDNS.PROTO_TCP, 21)

    # todo, maybe turn off after a timeout. timeout should be with a thread

    # # Add a TCP service to advertise
    # MDNS.add_service("_http", MDNS.PROTO_TCP, 80)
    # # Add an UDP service to advertise
    # MDNS.add_service("_myservice", MDNS.PROTO_UDP, 1234, txt= (("board","esp32"),("u","user"),("p","password")))
    #
    # # Give the other devices time to discover the services offered
    # time.sleep(60)
    #
    # # Remove a service, it will no longer be advertised
    # MDNS.remove_service("_http", MDNS.PROTO_TCP)

if __name__ == "__main__":
    mdns()
