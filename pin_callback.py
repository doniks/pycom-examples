from machine import Pin

def pin_handler(arg):
    print("got an interrupt in pin %s" % (arg.id()))

p_in = Pin('P10', mode=Pin.IN, pull=Pin.PULL_UP)
p_in.callback(Pin.IRQ_FALLING | Pin.IRQ_RISING, pin_handler)
