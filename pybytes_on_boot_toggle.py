import pycom
import machine

if pycom.pybytes_on_boot():
    print("Pybytes is turned on ... turning it off")
    pycom.pybytes_on_boot(False)
else:
    print("Pybytes is turned off ... turning it on")
    pycom.pybytes_on_boot(True)

# machine.reset()
