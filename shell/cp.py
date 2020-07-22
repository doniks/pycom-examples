def cp(src, dst, force=False, _buf_size=1000):
    import os
    try:
        src_size = os.stat(src)[6]
    except Exception as e:
        raise Exception("src", src, "does not exist:" + str(e))
    dst_exists = False
    if dst != '/' and dst[-1] == '/':
        # strip the trailing /
        dst = dst[:-1]
    print("cp", src, dst)
    try:
        os.listdir(dst)
        # dst is a directory
        src_name = src.split('/')[-1]
        dst = dst + '/' + src_name
    except:
        pass

    try:
        os.stat(dst)
        dst_exists = True
    except:
        pass
    if dst_exists and not force:
        raise Exception("Destination", dst, "exists")

    #raise Exception("hold on!", src, dst)
    s = open(src, 'r')
    d = open(dst, 'w')

    # _buf_size = 100000 # how much to copy at once
    progress_steps = 0.1 # how often to report progress
    if src_size > 1000000:
        progress_steps = 0.01
    progress = progress_steps
    dst_size = 0
    buf = b''
    print('copy', src, '[', src_size, '] to', dst, 'with _buf_size', _buf_size)
    while True:
        buf = s.read(_buf_size)
        if buf:
            d.write(buf)
            dst_size += len(buf)
            # print(dst_size, end=' ')
            if dst_size / src_size >= progress:
                print(int(progress * 100), '%', sep='', end=' ')
                progress += progress_steps
            else:
                #print('.', end='')
                pass
        else:
            break

    print()

    # d.write(s.read())

    d.close()
    s.close()
    dst_size = os.stat(dst)[6]
    if src_size != dst_size:
        raise Exception("Failed to copy. src_size=", src_size, "dst_size=", dst_size)

if __name__ == "__main__":
    #cp('test.txt', 'dst.txt')
    # cp('/sd/NB1-41019/updater.elf', 'upnb41019.elf')
    src='/sd/NB1-41019/upgdiff_41065-to-41019.dup'
    # src='/sd/NB1-41019/updater.elf'
    dst='/flash'
    t = time.ticks_ms()
    cp(src, dst, force=True)
    s = os.stat(src)[6]
    t = (time.ticks_ms() -1)/1000
    print(src, s, "B to", dst, "took", t, "s :", s/t, 'B/s')


    # for x in range(2,6):
    #     t = time.ticks_ms()
    #     b = 10**x
    #     print(x, b)
    #     cp(src, dst, force=True, _buf_size=b )
    #     s = os.stat(src)[6]
    #     t = (time.ticks_ms() -1)/1000
    #     print(src, s, "B to", dst, "with", b, "took", t, "s :", s/t, 'B/s')
    # /sd/NB1-41019/updater.elf 371307 B to /flash with 100 took 1276.867 s : 290.7954 B/s
    # /sd/NB1-41019/updater.elf 371307 B to /flash with 1000 took 1285.05 s : 288.9436 B/s
    # /sd/NB1-41019/updater.elf 371307 B to /flash with 10000 took 1292.45 s : 287.2893 B/s
    # /sd/NB1-41019/updater.elf 371307 B to /flash with 100000 took 1299.854 s : 285.6528 B/s
    # 1000000 MemoryError: memory allocation failed, allocating 1136112 bytes
    # import rm
    # rm.rm('/flash/test.txt')
    # cp('/flash/main.py', '/flash/test.txt')
    # if False:
    #     import hexdump
    #     hexdump.hexdump('/flash/test.txt')
