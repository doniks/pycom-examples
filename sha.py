import hashlib, time


sha_stress_running = None
sha_stress_verbose = None

def sha_test(lenght=100):
    import machine
    import hashlib

    buf = bytearray()
    for x in range(lenght//3):
        buf += machine.rng().to_bytes(3, 'big')
    # print(buf)

    h = hashlib.sha256(buf)
    # print(hex(buf[0]), hex(buf[-1]), h.digest())
    return h.digest()

def sha_stress(verbose=True):
    global sha_stress_running, sha_stress_verbose
    import machine
    l = 20_000
    sha_stress_running = True
    sha_stress_verbose = verbose
    print('sha_stress start', l)
    while sha_stress_running:
        t_ms = time.ticks_ms()
        d = sha_test(l)
        temp = (machine.temperature()-32)/1.8
        t_s = (time.ticks_ms()-t_ms)/1000
        sha_stress_verbose and print(time.time(), t_s, temp, len(d))
        pybytes.send_signal(1,time.time())
        pybytes.send_signal(2, temp)
        pybytes.send_signal(3, t_s)
    print('sha_stress end')

def sha_hello():

    t = time.time()
    if t % 2:
      msg = 'asdf'
    else:
      msg = 'jkl'
    h = hashlib.sha256(msg)
    print(msg, h.digest())

    if t % 2:
        msg = 'jkl'
    else:
        msg = 'asdf'
    h = hashlib.sha256(msg)
    # h.update(msg)
    print(msg, h.digest())

if __name__ == "__main__":
    if False:
        sha_stress()
    else:
        import _thread
        _thread.start_new_thread(sha_stress, (False,))

    if False:
        sha_stress_running = False
        sha_stress_verbose = False
        sha_stress_verbose = True
        pybytes.send_signal(1,time.time())
