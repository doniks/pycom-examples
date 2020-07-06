from network import LTE

def send_at_cmd_pretty(cmd, verbose=True):
    response = lte.send_at_cmd(cmd).split('\r\n')
    retval = ""
    for line in response:
        if ( len(line) == 0 ):
            continue
        # elif ( line == "OK" ):
        #     continue
        elif line == "ERROR":
            return None
        else:
            if verbose:
                print(len(line), line)
                retval = line
    return retval

lte = LTE()
print("imei", lte.imei())

send_at_cmd_pretty("AT+CPSMS=?")
# +CPSMS: (0-2), , ,("00000000"-"11111111"),("00000000"-"11111111")
#         modes 0-2
#               ^no Periodic-RAU values
#                 ^no GPRS READY timer values
#                   ^Periodic TAU values : 0000 0000 - 1111 1111
#                                            ^Active Time values
# +CPSMS:
# (list of supported <mode>s),
# (list of supported <Requested_Periodic-RAU>s),
# (list of supported <Requested_GPRS-READY-timer>s) in GERAN/UTRAN,
# (list of supported <Requested_Periodic-TAU>s), in E-UTRAN
# (list of supported <Requested_Active-Time>s)
# modes:
#  0 disable PSM
#  1 enable PSM
#  2 ?

send_at_cmd_pretty("AT+CPSMS?")
# +CPSMS: 0,,,"10100011","00100001"

send_at_cmd_pretty("AT+CREG=?")
# supported n's: (0,1,2)
# Set command controls the presentation of an
# * unsolicited result code
#   +CREG: <stat>
#   when <n>=1 and
#   there is a change in the MT's circuit mode network registration status in GERAN/UTRAN/E-UTRAN, or
# * unsolicited result code
#   +CREG: <stat>[,[<lac>],[<ci>],[<AcT>]]
#   when <n>=2 and
#   there is a change of the network cell in GERAN/UTRAN/E-UTRAN. The parameters <AcT>, <lac> and <ci> are sent only if available.
# * The value <n>=3 further extends the unsolicited result code with
#   [,<cause_type>,<reject_cause>], when available, when the value of <stat> changes.
send_at_cmd_pretty("AT+CREG?")


for n in range(0,8):
    # print(n)
    # Possible values for access technology are,
    # 0 GSM
    # 1 GSM Compact
    # 2 UTRAN
    # 3 GSM w/EGPRS
    # 4 UTRAN w/HSDPA
    # 5 UTRAN w/HSUPA
    # 6 UTRAN w/HSDPA and HSUPA
    # 7 E-UTRAN
    x = send_at_cmd_pretty("AT+CREG=" + str(n))
    print(x)
    creg = send_at_cmd_pretty("AT+CREG?", True)
    creg.split(" ")
    (cregn, stat) = creg.split(" ")[1].split(",")
    if (int(cregn) != n):
        raise Exception("CREG error")
    if n == 0:
        N="GSM"
    elif n == 1:
        N="GSM Compact"
    elif n == 2:
        N="UTRAN"
    elif n == 3:
        N="GSM w/EGPRS"
    elif n == 4:
        N="UTRAN w/HSDPA"
    elif n == 5:
        N="UTRAN w/HSUPA"
    elif n == 6:
        N="UTRAN w/HSDPA and HSUPA"
    elif n == 7:
        N="E-UTRAN"
    else:
        N="dunno"
    s = int(stat)
    if s == 0:
        S="not registered"
    elif s == 1:
        S="registered, home"
    elif s == 2:
        S="searching"
    elif s == 3:
        S="denied"
    elif s == 4:
        S="unknown"
    else:
        S="dunno"
    print(n, N, s, S)


send_at_cmd_pretty("AT+CEREG=?") # in E-UTRAN:      i) Active Time value and ii) the extended periodic TAU value that are allocated to the UE by the network
send_at_cmd_pretty("AT+CEREG?")

send_at_cmd_pretty("AT+CGREG=?") # in GERAN/UTRAN : i) Active Time value, ii) the extended periodic RAU value and iii) the GPRS READY timer value that are allocated to the UE by the network
send_at_cmd_pretty("AT+CGREG?")

send_at_cmd_pretty("AT")

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
# +CEREG:
# n=2 ... enable network registration and location information unsolicited result code
# stat=5 ... registered, roaming
# tac="B7B6" ... two byte tracking area code in hexadecimal format
# ci="0010581F" ... four byte E-UTRAN cell ID in hexadecimal format
# AcT=9 ... 9 undefined ???




send_at_cmd_pretty('AT!="fsm"')

send_at_cmd_pretty('AT!="showphy"')

send_at_cmd_pretty('AT+SQNLED=?')
send_at_cmd_pretty('AT+SQNLED?')

send_at_cmd_pretty('AT+SQNOMAHDEV=?')
send_at_cmd_pretty('AT+SQNOMAHDEV?')

send_at_cmd_pretty('AT+GSN')

send_at_cmd_pretty('AT+CGPADDR')
# '\r\n+CGPADDR: 1,"10.0.1.197"\r\n\r\nOK\r\n'
