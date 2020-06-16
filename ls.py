
def ls(dir=""):
    import os
    #import pycom
    #print("fs_type:", pycom.bootmgr()[1])
    #print("cwd:", os.getcwd())
    if dir == "":
        dir = os.getcwd()
    #print("dir:", dir)
    contents = os.listdir(dir)
    for c in contents:
        d = dir + "/" + c
        if dir == "/":
            d = dir + c
        try:
            # try to treat as a directory
            print(d, '\t', "[", len(os.listdir(d)), "]" )
            ls(d)
        except:
            # not a directory, ie a file
            s = os.stat(d)
            mode = s[0]
            ## the following values seem to always be 0
            # inode
            # device
            # num_links
            # uid
            # gid
            ## in bytes
            size = s[6]
            ## times are in seconds since reset (like time.time()), hence the values don't make too much sense. Might be usefull for determining how long ago a file was written IFF it was written since the last reset
            atime = s[7]
            mtime = s[8]
            ctime = s[9]
            if mode != 0x8000:
                # seems to be the only value we ever see
                print(d, '\t', hex(mode), size, 'B') # , atime, mtime, ctime)
            else:
                print(d, '\t', size, 'B')




if __name__ == "__main__":
    ls()
