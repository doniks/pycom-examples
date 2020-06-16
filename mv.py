
def mv(src, dst):
    import cp
    import rm
    cp.cp(src, dst)
    rm.rm(src)

if __name__ == "__main__":
    try:
        s = os.stat('/flash/main.py')
        mv('/flash/main.py', '/flash/main.py.bak')
    except:
        mv('/flash/main.py.bak', '/flash/main.py')
