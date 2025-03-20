
import binascii
import machine
uid = binascii.hexlify(machine.unique_id())
name = os.uname().sysname.lower() + '-' + uid.decode("utf-8")[-4:]
print(name)

import sqnsupgrade
sqnsupgrade.info()
