import zlib
import os
# verify that the file has been uploaded
file = 'test.txt.z'
print('dir', os.listdir())
print(file, os.stat(file))
# read contents, decompress and print
with open(file, 'r') as f:
    z = f.read()
b = zlib.decompress(z)
s = b.decode('utf-8')
print('ratio', len(z)/len(s))
print(s)


file = 'test.txt.gz'
print('dir', os.listdir())
print(file, os.stat(file))
with open('test.txt.gz', 'r') as file:
    data = uzlib.DecompIO(file, 31)
    #use data.readline() to read a single line
    print(data.read())
