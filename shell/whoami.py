def whoami(verbose=False):
    import machine
    import binascii
    import os
    uid = binascii.hexlify(machine.unique_id())
    name = os.uname().sysname.lower() + '-' + uid.decode("utf-8")[-4:]
    print(name)
    if verbose:
        for attr in dir(os.uname()):
            if attr[0] != '_':
                print(attr, getattr(os.uname(),attr))
        if os.uname().nodename == 'GPy' or os.uname().nodename == 'FiPy':
            from network import LTE
            lte = LTE()
            print('Sequans FW', lte.send_at_cmd('ATI1').split('\r\n')[2])

if __name__ == "__main__":
    whoami(True)
