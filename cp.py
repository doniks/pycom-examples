def cp(src, dst):
    print("cp", src, dst)
    import os
    s = open(src, 'r')
    d = open(dst, 'w')

    d.write(s.read())

    d.close()
    s.close()

if __name__ == "__main__":
    cp('test.txt', 'dst.txt')
