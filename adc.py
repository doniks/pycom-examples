from machine import ADC
import machine
import time
from binascii import hexlify
import os


name = os.uname().sysname.lower() + '-' + hexlify(machine.unique_id()).decode("utf-8")[-4:]
print(name, "adc.py")

# bits = 12 # produce values from [0,4096)
# bits = 10
bits =  9 # produce values from [0,512)
fmt = '={:0' + str(bits) + 'b}'
adc = ADC(bits=bits)

vref = {
    'lopy4-52e0': 1133,
    # does adc.vref() actually do anything? I see no effect :-P
}
if name not in vref:
    print('module', name, "has not been calibrated")
    import sys
    sys.exit()
    # calibration:
    # 1. output the internal reference voltage of 1100mV to P22
    adc.vref_to_pin('P22')
    # 2. measture the voltage at P22 with a voltmeter
    # 3. enter the actual value into vref above and then re-run
else:
    print('calibrate vref for', name)
    adc.vref(vref[name])

print("vref=", adc.vref(), "mV")

# create an analog pin
# Valid pins are P13 to P20.
# attenuation suggested range:
# (dB)   (mV)
#   0    100 ~  950
#   2.5  100 ~ 1250
#   6    150 ~ 1750
#  11    150 ~ 2450
apin = adc.channel(pin='P20', attn=ADC.ATTN_11DB)
# P20 seventh from top right


def log():
    # log adc value
    # using exponential moving average
    # and extra filtering of +/-1 increases/decreases
    alpha = 0.3
    inc_ct = 0
    dec_ct = 0
    id_ct_limit = 5
    update = True
    last = apin()
    print(last)
    while True:
        val = apin()
        val = val * alpha + last * (1 - alpha)
        val = int(round(val))
        if val == last:
            # print('.', end='')
            update = False
        elif val == last-1:
            dec_ct += 1
            inc_ct = 0
            if dec_ct > id_ct_limit:
                dec_ct = 0
            else:
                update = False
        elif val == last+1:
            inc_ct += 1
            dec_ct = 0
            if inc_ct > id_ct_limit:
                inc_ct = 0
            else:
                update = False
        else:
            # print('X', end='')
            update = True

        if update:
            # print("[", time.time(), "]", " val=", val, fmt.format(val), " voltage=", apin.value_to_voltage(val), "mV", sep='')
            print("[", time.time(), "]", " val=", val, " voltage=", apin.value_to_voltage(int(val)), "mV", sep='')
            last = val
        # else:
        #     print('.', end='')

log()
