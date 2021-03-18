
Expansion board 3.2 with
Firmware with "P3 high to reboot" feature
exp_board_32_0561b03.dfu

https://pycomiot.atlassian.net/wiki/spaces/FIR/pages/1657241601/Power+cycle+on+Expansion+board+3.2

Pull P3 high to power cycle the module.
When removing the RUN jumper, P3 is free to be used for other purposes.

from machine import Pin
P3 = Pin('P3', mode=Pin.OUT)
