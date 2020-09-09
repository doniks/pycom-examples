
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

    # cd
    os.chdir('/sd')

    # check the content
    #print('/sd :', os.listdir('/sd'))
    print('/sd :', os.listdir())



    # # try some standard file operations
    # f = open('/sd/test.txt', 'w')
    # f.write('Testing SD card write operations')
    # f.close()
    # f = open('/sd/test.txt', 'r')
    # f.readall()
    # f.close()

if __name__ == "__main__":
    sd()
