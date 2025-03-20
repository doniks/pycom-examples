
def get():
    if pybytes.get_config('pybytes_autostart'):
        print("pybytes_autostart is enabled")
        return True
    else:
        print("pybytes_autostart is disabled")
        return False

def set(b):
    if b:
        print("enabling it")
    else:
        print("disabling it")
    pybytes.set_config('pybytes_autostart', b)

def toggle():
    if get():
        set(False)
    else:
        set(True)

if __name__ == "__main__":
    get()
    if False:
        toggle()
