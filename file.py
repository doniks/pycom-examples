import os
name = 'test.txt'
# name = '/test.txt'
# name = '/flash/test.txt'
name = '/flash/device_dev'

def write(name):
    f = open(name, 'w')
    # f.write("bla\nblubasdfasdfasdfasdfasdfadsf")
    f.write("2\n")
    f.close()

def read(name):
    try:
        f = open(name, 'r')
        print("##############", name)
        content = f.read()
        f.close()
        print("_", content, "_", sep="")
    except:
        print('Cannot read', name)

def remove(name):
    os.remove(name)

# write()
# print(os.listdir('/flash'))
print(os.listdir('/flash/logs'))
read('/flash/logs/log_0.log')
read('/flash/logs/log_1.log')
read('/flash/logs/log_2.log')
if False:
    remove('/flash/logs/log_0.log')
    remove('/flash/logs/log_1.log')
    remove('/flash/logs/log_2.log')
# remove()
