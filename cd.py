def cd(dir="/flash"):
    import pwd
    import os
    pwd.pwd()
    if dir[-1] == '/':
        # strip trailing /
        os.chdir(dir[:-1])
    else:
        os.chdir(dir)
    pwd.pwd()

if __name__ == "__main__":
    cd('/flash/test/')
