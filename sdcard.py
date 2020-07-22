
def sd():
    from machine import SD
    import os

    sd = SD()
    try:
        os.mount(sd, '/sd')
    except Exception as e:
        if os.stat('/sd'):
            # should be ok, probably previously mounted
            pass
        else:
            print("Exception while trying to mount:", e)

    # check the content
    print('/sd :', os.listdir('/sd'))

    # # try some standard file operations
    # f = open('/sd/test.txt', 'w')
    # f.write('Testing SD card write operations')
    # f.close()
    # f = open('/sd/test.txt', 'r')
    # f.readall()
    # f.close()

if __name__ == "__main__":
    sd()
