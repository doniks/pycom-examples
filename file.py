import os
name = 'test.txt'
# name = '/test.txt'
# name = '/flash/test.txt'

def write():
    global name
    f = open(name, 'w')
    f.write("bla\nblubasdfasdfasdfasdfasdfadsf")
    f.close()

def read():
    global name
    f = open(name, 'r')
    content = f.read()
    f.close()
    print("_", content, "_", sep="")

def remove():
    global name
    os.remove(name)

write()
read()
# remove()
