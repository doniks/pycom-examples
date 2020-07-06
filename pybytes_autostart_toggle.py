
def toggle():
    if pybytes.get_config('pybytes_autostart'):
        print("pybytes_autostart is enabled, disabling it")
        pybytes.set_config('pybytes_autostart', False)
    else:
        print("pybytes_autostart is disabled, enabling it")
        pybytes.set_config('pybytes_autostart', True)



if __name__ == "__main__":
    toggle()
