def pybytes_init():
    global pybytes
    t = time.ticks_ms()
    from _pybytes_config import PybytesConfig
    print('import', time.ticks_ms()-t)
    conf = PybytesConfig().read_config()
    print('conf', time.ticks_ms()-t)
    pybytes = Pybytes(conf)
    print('init', time.ticks_ms()-t)

def pybytes_start():
    global pybytes_started
    if pybytes.isconnected():
        print('pybytes is already connnected')
    else:
        t = time.ticks_ms()
        pybytes.start()
        print("start", hex(id(pybytes)), pybytes.isconnected(), (time.ticks_ms()-1)/1000)
    pybytes_started = True

def temp():
    return (machine.temperature()-32)/1.8

if __name__ == '__main__':
    import machine
    t0 = temp()
    from _pybytes import Pybytes
    pybytes_started = False
    lazy = True
    try:
        pybytes # if the object exists there is nothing else to do
        pybytes_started = True
        lazy = False
        print('sync', time.ticks_ms())
    except:
        print('async', time.ticks_ms())

    if lazy:
        pybytes_init()
        import _thread
        _thread.start_new_thread(pybytes_start,())

    # start working, .... reading sensors, etc ...
    import time
    import rand
    # import pycom
    print('work', end=' ')
    for work in range(50):
        print('X', end='')
        time.sleep(0.1)
    print(" done working")

    # once we want to send_signal or otherwise expect connectivity we should
    # either check/wait for pybytes_started to signal the completion of the async connection (success or timeout)
    # or check/wait for pybytes.isconnected() directly
    print('wait', end=' ')
    while not pybytes_started:
        print('.', end='')
        time.sleep(0.1)
    print(" done waiting")
    t = time.ticks_ms()
    print('send', lazy, t, pybytes_started, pybytes.isconnected())
    pybytes.send_signal(6, t0)
    if lazy:
        pybytes.send_signal(2, t)
        pycom.pybytes_on_boot(True)
    else:
        pybytes.send_signal(4, t)
        # pycom.pybytes_on_boot(False)
    s = rand.randi(1,181)*10
    s =   30 #         t=56.6
    s =    0 # 17:58-  t=58.3
    s = 1800 # 18:17-
    pybytes.send_signal(5, s)
    t1 = temp()
    pybytes.send_signal(7, t1)
    print(s, t0, t1)
    # https://www.openstreetmap.org/#map=9/51.5087/5.0317
    time.sleep(10)
    print('sleep')
    time.sleep(1)
    pybytes.disconnect()
    machine.deepsleep(s * 1000)
    # import machine
    # machine.reset()
