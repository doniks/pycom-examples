from machine import I2C
import time

def scan():
    s = i2c.scan()
    print("i2c:", end='')
    for i in s:
        print(hex(i), end=', ')
    print()
# print(i2c.scan())
# while True:
#     print(i2c.scan())
#     time.sleep(0.5)
#
# i2c.writeto(0xaa,1,stop=False)


# sda='P21' # default P9
# scl='P22' # default P10

print(os.uname())
# pytrack:
sda='P22'
scl='P21'
i2c = I2C(2, mode=I2C.MASTER, pins=(sda, scl)) # , baudrate=100000)
# i2c = I2C(0, mode=I2C.MASTER)
# i2c = I2C()
# i2c = I2C(pins=(sda, scl), baudrate=400000 )
scan()
