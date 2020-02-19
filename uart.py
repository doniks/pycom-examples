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
#
import pycom
import time
from machine import UART
import machine

r = str(machine.rng())

# reinitializing uart0 in this way, breaks the REPL in pymakr
# however you can connect, e.g., with minicom -b 9600
# it will receive stdout, e.g. print() AND uart0.write()
# uart0 = UART(0, baudrate=9600)
# uart0.write("Hello UART 0 (")
# uart0.write(r)
# uart0.write(")\n\r")

uart1 = UART(1, baudrate=9600, timeout_chars=10)
uart1.write("Hello UART 1 (")
uart1.write(r)
uart1.write(")\n\r")

uart2 = UART(2, baudrate=9600, pins=('P8', 'P9'))
uart2.write("Hello UART 2 (")
uart2.write(r)
uart2.write(")\n\r")

while True:
    line = uart1.readline()
    if line == None:
        time.sleep(1)
        print(".", end="")
        # uart0.write("0")
        uart1.write("1")
        uart2.write("2")
    else:
        color = line.strip()
        if color == b'red' or color == b'r':
            print("red")
            pycom.heartbeat(False)
            pycom.rgbled(0x330000)
        if color == b'blue' or color == b'b':
            print("blue")
            pycom.heartbeat(False)
            pycom.rgbled(0x000033)
        else:
            pycom.heartbeat(True)
            print("Don't understand \"", color, "\"", sep="")
