

def mkdir(dir):
    import os
    if dir[-1] == '/':
        # strip trailing /
        os.mkdir(dir[:-1])
    else:
        os.mkdir(dir)

def rmdir(dir):
    os.rmdir(dir)

if __name__ == "__main__":
    mkdir('/flash/test/')
