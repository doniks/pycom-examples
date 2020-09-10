import os

# COMMANDS: ls() ll() find() du()
#
# EXAMPLES:
# ls('/flash/lib')
# ls() # lists the current working directory, see pwd()
# ll('/sd')

# TODO:
# implement wildcards
# move cd() pwd() df() here
# probably rm() cat() mv() as well? they all kinda belong together and they all should support wildcards
# fix/implement find(/flash/foo*/bar.*', do_return=True) and cat(find('thingy.txt', do_return=True)) mv(find('*.py'), '/flash/backup/')

# add a trailing /
def _add_slash(dir):
    if dir[-1] == '/':
        return dir
    else:
        return dir + '/'

# strip the trailing /
def _strip_slash(dir):
    if dir == '/' or dir[-1] != '/':
        return dir
    else:
        return dir[:-1]

def _concat_path(d1, d2):
    return _add_slash(d1) + d2

def _is_dir(obj):
    try:
        os.listdir(obj)
        return True
    except:
        return False

def _ll(d):
    try:
        contents = os.listdir(d)
        for c in contents:
            _ll(_concat_path(d,c))
    except:
        ##print("_ll", d)
        s = os.stat(d)
        mode = s[0]
        ## the following values seem to always be 0
        # inode = s[1]
        # device = s[2]
        # num_links = s[3]
        # uid = s[4]
        # gid = s[5]
        ## in bytes
        size = s[6]
        ## times are in seconds since reset (like time.time()), hence the values don't make too much sense. Might be usefull for determining how long ago a file was written IFF it was written since the last reset
        atime = s[7]
        mtime = s[8]
        ctime = s[9]
        if mode != 0x8000:
            # seems to be the only values we ever see are
            # 0x8000 for files and
            # 0x4000 for directories
            print(d, '\t\t', hex(mode), size, 'B', end='') # , atime, mtime, ctime)
        else:
            print(d, '\t\t', size, 'B', end='')
        if size > 1024:
            print(' (', round(size/1024,2), ' KiB', sep='', end='')
            if size > 1024 * 1204:
                print(', ', round(size / 1024 / 1024,2), ' MiB)', sep='')
            else:
                print(')')
        else:
            print()

def _wildcard_obj(dir, obj):
    pass

def _wildcard(path):
    # FIXME
    objects = path.split('/')
    dir = '/'
    objects = objects.reverse()
    if objects[-1] != '':
        # path is not an absolute path starting at /
        dir = os.getcwd()
        objects.pop()
    print(dir, objects)

def _find(obj, name=None, type=None, do_return=False):
    import re
    obj = _strip_slash(obj)
    if type is not None and type != 'f' and type != 'd':
        raise Exception("Invalid type:", type)
    do_list = True
    if name and not re.search(name, obj):
        do_list = False
    return_list = []
    #print("obj=", obj, name, type, do_return )

    try:
        # try to treat it as a directory
        contents = os.listdir(obj)
        # jep, it's a directory
        obj = _add_slash(obj)
        if type != 'f' and do_list:
            if do_return:
                return_list += [obj]
            else:
                # print(obj, '\t\t', hex(os.stat(obj)[0]), "[", len(contents), "]" )
                print(_add_slash(obj), '\t\t', "[", len(contents), "]" )

        for c in contents:
            obj2 = _concat_path(obj, c)
            if do_return:
                return_list += _find(obj2, name, type, do_return)
                #print("coming up", obj, obj2, r)
            else:
                _find(obj2, name, type, do_return)
            # print("c=",c, "d=",d, return_list)
    except Exception as e:
        # not a directory, ie a file
        #print("not a dir", e)
        if type != 'd' and do_list:
            if do_return:
                return_list += [obj]
            else:
                _ll(obj)
    if do_return:
        #print("end", obj, return_list)
        return return_list

def ls(x=''):
    if x == '':
        x = os.getcwd()
    try:
        print(x, ":", os.listdir(x) )
    except:
        try:
            os.stat(x)
            print(x, ":", x)
        except Exception as e:
            print(x, ":", e)

def ll(dir=''):
    if dir == '':
        dir = os.getcwd()
    _ll(dir)

def find(dir='', name=None, type=None, do_return=False):
    if dir == '':
        dir = os.getcwd()

    msg = ""
    if do_return:
        msg += "return "
        if name:
            msg += "matching '" + name + "' "
    elif name:
        msg += "find matching '" + name + "' "
    else:
        msg += "list all "
    if type == 'f':
        msg += "files "
    elif type == 'd':
        msg += "directories "
    msg += "in " + dir + ":"
    print(msg)
    if do_return:
        return _find(dir, name, type, do_return)
    else:
        _find(dir, name, type, do_return)

def du(dir='', do_return=False):
    if dir == '':
        dir = os.getcwd()
    if dir != '/' and dir[-1] == '/':
        # strip the trailing /
        dir = dir[:-1]
    total_b = _du(dir)
    if do_return:
        return total_b
    else:
        print("du", dir, total_b, 'B used', end='')
        if total_b > 1024:
            print(' (', round(total_b / 1024,2), ' KiB', sep='', end='')
            if total_b > 1024 * 1024:
                print(', ', round(total_b / 1024 / 1024,2), ' MiB)', sep='')
            else:
                print(')')
        else:
            print()

def _du(dir):
    total = 0 # sum up the bytes of diskusage
    contents = []
    try:
        contents = os.listdir(dir)
        for c in contents:
            d = dir + "/" + c
            if dir == "/":
                d = dir + c
            # print("c=",c, "d=",d, return_list)
            total += _du(d)
        return total
    except:
        return os.stat(dir)[6]

if __name__ == "__main__":
    # ls()
    find()
    # print(find('/', name='sy', do_return=True))
    # du('/flash')
    # ll('/sd')

    #_wildcard('/sd/CAT*/mtool*')
    # ls('/sd')
    # ls('/flash')
    # find('/sd/CATM1-41065', 'updater')
    #find('/', 'updater')
    #find(name='update')
    # ll("/flash/up41065.elf")
    # print(find(name='.*33080.*', type='f', do_return=True))
    #print(find(name='.*NB1.*', type='d', do_return=True))
    # print(find(name='.*41065.*', type=None, do_return=True))
    pass
