import time
from machine import PWM
pwm = PWM(0, frequency=5000)  # use PWM timer 0, with a frequency of 5KHz
# create pwm channel on pin P12 with a duty cycle of 50%
pwm_c = pwm.channel(0, pin='P23', duty_cycle=0.5)



pwm_c.duty_cycle(0.1)
time.sleep(1)
pwm_c.duty_cycle(0.3)
time.sleep(1)
pwm_c.duty_cycle(0.6)
time.sleep(1)
pwm_c.duty_cycle(0.9)
time.sleep(1)
pwm_c.duty_cycle(0)
