from machine import Timer

def alarm_handler(alarm):
    print("X", alarm, end=' ')

alarm = Timer.Alarm(alarm_handler, 1, periodic=True)

if False:
    alarm.cancel()
