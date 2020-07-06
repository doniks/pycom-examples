import machine
    import statistics

    NUM_ADC_READINGS = const(50)

    adc = machine.ADC()
    adc.vref(1126)  # put here ESP32 VRef measured in mV with a voltmeter
    # adcP16 = adc.channel(pin='P16', attn=machine.ADC.ATTN_6DB) # For Expansion Board v2.x
    adcP16 = adc.channel(pin='P16', attn=machine.ADC.ATTN_11DB) # For Expansion Board v3.x
    samples_voltage = [0]*NUM_ADC_READINGS
    for i in range(NUM_ADC_READINGS):
    #    samples_voltage[i] = (171*adcP16.voltage())//56     # Expansion Board v2.x has voltage divider (115K + 56K) converting to integer voltage, [0, 6702] mV
        samples_voltage[i] = (2*adcP16.voltage())//1   # Expansion Board v3.x has voltage divider (1M + 1M) converting to integer voltage, [0, 6600] mV
    batt_mV = round(statistics.mean(samples_voltage))
    batt_mV_error = round(statistics.stdev(samples_voltage))
