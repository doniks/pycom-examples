def cat(filename):
    f = open(filename, 'r')
    content = f.read()
    f.close()
    print(content, sep="")

if __name__ == "__main__":
    # cat("/flash/test/test.bin.up")
    # cat("/flash/test/http_get.recv")
    #cat("/flash/pybytes_config.json")
    # cat("/flash/main.py")
    # cat("/flash/log_GPy_240ac4c7b250.log")
    cat("/flash/OTA_VERSION.py")
