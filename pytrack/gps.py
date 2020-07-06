import time
import gc
from L76GNSS import L76GNSS
from pytrack import Pytrack

time.sleep(2)
gc.enable()

py = Pytrack()
print(py.read_fw_version())
l76 = L76GNSS(py, timeout=30)

while (True):
    coord = l76.coordinates()
    print("{} - {} - {}".format(coord, time.time(), gc.mem_free()))
