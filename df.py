
def df():
    import os
    print("/flash", os.getfree('/flash'), "KiB free")
    try:
        print("/sd", os.getfree('/sd'), "KiB free")
    except:
        pass

if __name__ == "__main__":
    df()
