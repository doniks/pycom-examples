from machine import I2C
sda='P21' # or sda='P22'
scl='P22'
i2c = I2C(0, mode=I2C.MASTER, pins=(sda, scl), baudrate=100000)
print(i2c.scan())
