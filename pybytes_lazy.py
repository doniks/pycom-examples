# ensure your pybytes_config says: "pybytes_autostart": false
import time
start = time.time()

def msg(m):
    print(time.time() - start, m)

def start_pybytes():
    global pybytes
    import json
    # print(pybytes_config) # this should be the full json file, somehow I just had that without doing the file read ... oh well

    msg("read config")
    f = open("/flash/pybytes_config.json", 'r')
    pybytes_cfg = json.load(f)
    f.close()


    msg("start pybytes")
    pybytes = Pybytes(pybytes_cfg) #, autoconnect=True)
    pybytes.start() #

    msg("send signal")
    pybytes.send_signal(1, time.time())

    msg("done")


if __name__ == "__main__":
    import _pybytes
    import time
    import pycom
    pycom.get_free_heap()

    if True:
        start_pybytes()
    else:
        import _thread
        _thread.start_new_thread(start_pybytes, ())
