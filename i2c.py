from machine import I2C
import time

# known
addr = {
  0x08: 'PIC',
  0x10: 'GPS',
  0x1e: 'LIS2HH12 (ACC)',
  0x60: 'MPL3115A2',
  0x29: 'LTR329ALS01',
  0x40: 'SI7006A20',
}

def scan():
    s = i2c.scan()
    print("i2c[{}]:".format(len(s)))
    for i in s:
        if i in addr:
            print('  0x{:02x} /{:3d}: {}'.format(i,i,addr[i]))
        else:
            print('  0x{:02x} /{:3d}'.format(i, i))

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
# print('done')
