import time
from machine import RTC
import machine
import pycom
import os

def d(m):
    print(time.time(), m)

def send():
    print(time.time(), "sending")
    m = 'first  {}'.format(time.time())
    pybytes.send_signal(1, m)
    m = 'second {}'.format(time.time())
    pybytes.send_signal(2, m)


d("start")
send()
machine.deepsleep(10)
