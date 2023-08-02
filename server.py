from network import Server

_server = None

def _is_allocated():
    try:
        _server
        print('allocated')
        return True
    except Exception as e:
        print('not allocated', e)
        return False

def _is_init():
    v = False
    if _is_allocated():
        v = _server is not None
        if v:
            print('initialized')
        else:
            print('not initialized')
    return v

def is_running():
    v = False
    if _is_init():
        v = _server.isrunning()
        if v:
            print('running')
        else:
            print('not running')
    else:
        print('dont know')
        # there is no instance initialized locally. Which means I cannot test wheter the server is running. it might be running, or it might not. Once we initiate the object we also automatically start is, so I'm not doing this here automatically
        return None
    return v

def _init():
    print('initializing')
    global _server
    _server = Server()

def stop():
    global _server
    if not _is_init():
        _init()
        print('stopping')
        _server.deinit()
    else:
        if is_running():
            print('stopping')
            _server.deinit()
        else:
            print('not running')

def start():
    global _server
    if not _is_init():
        print('starting')
        _init()
    else:
        if not is_running():
            print('starting')
            _server.init()

def restart():
    global _server
    print('restart')
    stop()
    start()
