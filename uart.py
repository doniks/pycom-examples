#

# Connect GND,RX,TX from FTDI USB Uart to GND,P3,P4 of the LoPy4
#             |----------------|            |----------------|
#             |             RX |------------| P3 (TX)        |
#             |      FTDI   TX |------------| P4 (RX)        |
#  Laptop ====| USB       3.3V |            |          LOPY4 |
#             |            GND |------------|GND             |
#             |----------------|            |                |
#                                           |----------------|
#
# minicom -oD /dev/ttyUSB0 -b 9600
import pycom
import time
from machine import UART
import machine
import binascii
import os
uid = binascii.hexlify(machine.unique_id())
name = os.uname().sysname.lower() + '-' + uid.decode("utf-8")[-4:]


def uprint(uart, *values):
    for v in values:
        uart.write(str(v))
        uart.write(' ')
    uart.write('\r\n')


#####################################################
m = hex(machine.rng())

# uart 0, repl
# reinitializing uart0 in the following way, breaks the REPL in pymakr
# however you can connect, e.g., with minicom -b 9600
# it will receive stdout, e.g. print() AND uart0.write()
# uart0 = UART(0, baudrate=9600)
# uart0.write("Hello UART 0 (")
# uart0.write(r)
# uart0.write(")\n\r")

print("uart1")
# uart1 = UART(1, baudrate=9600, timeout_chars=10)
# pins=(TXD, RXD, RTS, CTS)
uart1 = UART(1, baudrate=9600 ) # pins=('P23', 'P22'))

if name == "fipy-2b40":
    print(name, "recieve")
    while True:
        r = uart1.readline()
        if r is None:
            print(".", end="")
        else:
            print("recv(", len(r), "):[", binascii.hexlify(r), "]", sep='', end='->')
            try:
                print('"', r.decode('utf-8'), '"', sep='')
            except:
                print()
        time.sleep(0.1)


print(name, "send")


uart1.write("Hello UART 1 (")
uart1.write(m)
uart1.write(")\n\r")

while True:
    # uprint(uart1, time.time(), m, "jo")
    uprint(uart1, time.time())
    print('.', end='')
    time.sleep(1)

print("uart1 done")

print("uart2")
# On the GPy/FiPy UART2 is unavailable because it is used to communicate with the cellular radio.
# OSError: resource not available
uart2 = UART(2, baudrate=9600, pins=('P8', 'P9', 'P10', 'P11'), timeout_chars=10)
# uart2 = UART(2, baudrate=9600, pins=('P8', 'P9'), timeout_chars=10)
print("uart2 tx")
uart2.write("Hello UART 2")
uart2.write(m)
uart2.write('\n\r')
t = time.ticks_ms()
i = 0
while (time.ticks_ms() - t ) / 1000 < 5:
    m = i.to_
    uart2.write(m)
    uart2.write("\n\r")
    print(".")
    time.sleep(0.2)
print("uart2 tx done")
sleep(5)
print("uart2 rx")
for x in range(5):
    r = uart2.readline()
    if r is None:
        print(".")
    else:
        print("recv(", len(r), "):[", binascii.hexlify(r), "]", sep='', end='->')
        try:
            print(r.decode('utf-8'))
        except:
            pass
        print()
    time.sleep(1)
#print("recv:", str(r))
print("uart2 done")


#
# while True:
#     line = uart1.readline()
#     if line == None:
#         time.sleep(1)
#         print(".", end="")
#         # uart0.write("0")
#         uart1.write("1")
#         uart2.write("2")
#     else:
#         color = line.strip()
#         if color == b'red' or color == b'r':
#             print("red")
#             pycom.heartbeat(False)
#             pycom.rgbled(0x330000)
#         if color == b'blue' or color == b'b':
#             print("blue")
#             pycom.heartbeat(False)
#             pycom.rgbled(0x000033)
#         else:
#             pycom.heartbeat(True)
#             print("Don't understand \"", color, "\"", sep="")
