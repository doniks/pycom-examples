import time
t = time.time()
print("send_signal(1,", t, ")")
pybytes.send_signal(1, t)


'''



pybytes.start()

connect()
print(pybytes.isconnected())
pybytes.reconnect()
pybytes.connect_wifi()
pybytes.connect_lte()
pybytes.connect_lora_abp()
pybytes.connect_lora_otaa()
pybytes.connect_sigfox()
pybytes.disconnect()

pybytes.send_signal()
pybytes.send_battery_level()
pybytes.send_custom_location()
pybytes.send_custom_message()
pybytes.send_ping_message()
pybytes.send_info_message()
pybytes.send_scan_info_message()
pybytes.send_digital_pin_value()
pybytes.send_analog_pin_value()
pybytes.send_node_signal()

# pybytes.activate()
pybytes.deepsleep(1000)
pybytes.enable_terminal()
pybytes.enable_ssl()
pybytes.enable_lte()
pybytes.dump_ca() # Successfully created /flash/cert/pycom-ca.pem
print(pybytes.smart_config())

pybytes.set_custom_message_callback()
pybytes.add_custom_method()
pybytes.register_periodical_digital_pin_publish()
pybytes.register_periodical_analog_pin_publish()

pybytes.read_config() # reads /flash/pybytes_config.json
pybytes.write_config() # Pybytes configuration written to /flash/pybytes_config.json
pybytes.print_config()
pybytes.update_config()
pybytes.export_config()
print(pybytes.get_config())
pybytes.set_config('yaddayadda', 666) # I think it sets it in memory AND writes to file
pybytes.set_config('yaddayadda', None)
pybytes.print_cfg_msg()
os.unlink('/flash/pybytes_config.json')

Pybytes.WAKEUP_ALL_LOW
Pybytes.WAKEUP_ANY_HIGH
'''
