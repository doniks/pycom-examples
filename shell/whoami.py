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

if __name__ == "__main__":
    whoami(True)
