def cd(dir="/flash"):
    import pwd
    import os
    pwd.pwd() # print old pwd
    if dir[-1] == '*':
        print("wildcard")
        import ls
        hits = ls.find(name=dir, type='d', do_return=True)
        if len(hits) == 1:
            dir=hits[0]
        else:
            raise Exception("Cannot uniquely identify", dir, len(hits))
    if dir != '/' and dir[-1] == '/':
        # strip the trailing /
        dir = dir[:-1]
    try:
        #os.stat(dir)
        os.listdir(dir)
        # NB: seems chdir would throw an exception, but change the internal string anyway
        # hence subsequent calls to os.getcwd() aka pwd() would fail also :-P
    except Exception as e:
        print("Cannot change to", dir, e)
        return
    if len(dir) > 1 and dir[-1] == '/':
        # strip trailing /
        os.chdir(dir[:-1])
    else:
        os.chdir(dir)
    pwd.pwd() # print new pwd

if __name__ == "__main__":
    #cd('/flash/test/')
    #cd('NB1*')
    cd('CAT*')
