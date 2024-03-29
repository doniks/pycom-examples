from machine import Pin
import time

# works on GPy, Fipy, Wipy

led = Pin('P9', mode=Pin.OUT) # G 16
led_off = 1
led_on = 0
led(led_off)

button = Pin('P10', mode=Pin.IN, pull=Pin.PULL_UP) # G17

while True:
    if button():
        # print("not pressed")
        led(led_off)
    else:
        print("pressed")
        led(led_on)
        # for b in range(3):
        #     led.value(led_on)
        #     time.sleep(0.1)
        #     led.value(led_off)
        #     time.sleep(0.1)

    time.sleep(0.1)



# from machine import Pin
# p_led = Pin('P9', mode=Pin.OUT)
# p_led.value(1)
# p_button = Pin('P10', mode=Pin.IN, pull=Pin.PULL_UP)
# p_button.callback(Pin.IRQ_FALLING, lambda x: p_led.toggle())
