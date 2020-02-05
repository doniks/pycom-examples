from network import LTE

def send_at_cmd_pretty(cmd):
    response = lte.send_at_cmd(cmd).split('\r\n')
    for line in response:
        if ( len(line) > 0 ):
            print(line)

lte = LTE()
print("imei", lte.imei())
print("is_connected", lte.isconnected())
print("ue_coverage", lte.ue_coverage())
print("iccid", lte.iccid())
print("time", lte.time())


send_at_cmd_pretty('AT+CGMI')
# PYCOM
send_at_cmd_pretty('AT+CGMM')
# FiPy
send_at_cmd_pretty('AT+CGMR')
# UE5.0.0.0d
send_at_cmd_pretty('AT+CGSN=0')

send_at_cmd_pretty('AT+CGSN=1')

send_at_cmd_pretty('AT+CGSN=2')

send_at_cmd_pretty('AT+CGSN=3')
# +CGSN: "00"
send_at_cmd_pretty('AT+CIMI')

send_at_cmd_pretty('AT+CPINR')
# +CPINR: SIM PIN,3,3
# +CPINR: SIM PUK,10,10
# +CPINR: SIM PIN2,3,3
# +CPINR: SIM PUK2,10,10
send_at_cmd_pretty('AT+CSQ')
# +CSQ: 99,99
send_at_cmd_pretty('AT+CFUN?')
# +CFUN: 4

send_at_cmd_pretty("AT+CEREG?")
send_at_cmd_pretty('AT!="fsm"')

send_at_cmd_pretty('AT!="showphy"')

send_at_cmd_pretty('AT+SQNLED=?')
send_at_cmd_pretty('AT+SQNLED?')

send_at_cmd_pretty('AT+SQNOMAHDEV=?')
send_at_cmd_pretty('AT+SQNOMAHDEV?')

send_at_cmd_pretty('AT+GSN')

