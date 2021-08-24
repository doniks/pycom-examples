# import machine
# import binascii
# import os
# import time
# print(os.uname().sysname.lower() + '-' + binascii.hexlify(machine.unique_id()).decode("utf-8")[-4:], "boot.py")
# import pycom
# pycom.heartbeat(False)
# pycom.rgbled(0x000005)
# t = time.ticks_ms()
# print("boot.py:importing shell tools ", end='')
# # posix/linux like shell commands
# try:
#     print('s', end='')
#     from shell import *
# except:
#     print('S', end='')
# # custom pycom dev board commands
# try:
#     print('b', end='')
#     from blink import *
# except:
#     print('B', end='')
# # try:
# #     print('w', end='')
# #     from wlan import *
# # except:
# #     print('W', end='')
# # print('e', end='')
# # try: import eth
# # except:pass
# # try:
# #     print('l', end='')
# #     from lte import *
# # except:
# #     print('L', end='')
# try:
#     print('n', end='')
#     from net import *
# except:
#     print('N', end='')
# print(' ...', (time.ticks_ms()-t)/1000)
# print("boot.py:done")
