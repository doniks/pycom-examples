import pycom
import machine

if pycom.pybytes_on_boot():
    print("Pybytes is currently turned on ... turning it off now")
    pycom.pybytes_on_boot(False)
else:
    print("Pybytes is currently turned off ... turning it on now")
    pycom.pybytes_on_boot(True)

if False:
    machine.reset()

    import _thread
    _thread.start_new_thread(pybytes.start,)
