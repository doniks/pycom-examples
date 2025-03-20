from network import LTE

def send_at_cmd_pretty(cmd, verbose=True):
    if verbose:
        print(cmd)
    response = lte.send_at_cmd(cmd).split('\r\n')
    returnOk = False
    returnVector = []
    for line in response:
        if ( len(line) == 0 ):
            continue
        elif ( line == "OK" ):
            returnOk = True
        elif line == "ERROR":
            returnOk = False
        else:
            # try:
            #     returnVector += [line.split(" ")[1]]
            # except:
            returnVector += [line]
        if verbose:
            print(line)
    return (returnOk, returnVector)

lte = LTE()
try:
    print("imei", lte.imei())
except:
    lte.pppsuspend()
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


Requested_Periodic-TAU
string type;
one byte in an 8 bit format.
Requested extended periodic TAU value (T3412) to be allocated to the UE in E-UTRAN. The requested extended periodic TAU value is coded as one byte (octet 3) of the GPRS Timer 3 information element coded as bit format
(e.g. "01000111" equals 70 hours).
For the coding and the value range, see the GPRS Timer 3 IE in
3GPP TS 24.008 [8] Table 10.5.163a/3GPP TS 24.008.
See also 3GPP TS 23.682 [149] and 3GPP TS 23.401 [82].
The default value is set to 180 s.

Requested_Active-Timestring type; one byte in an 8 bit format. Requested Active Time value (T3324) to be allocated to the UE. The requested Active Time value is coded as one byte (octet 3) of the GPRS Timer 2 information element coded as bit format (e.g. "00100100" equals 4 minutes). For the coding and the value range, see the GPRS Timer 2 IE in 3GPP TS 24.008 [8] Table 10.5.163/3GPP TS 24.008. See also 3GPP TS 23.682 [149], 3GPP TS 23.060 [47] and 3GPP TS 23.401 [82]. The default value is set to 60 s.


send_at_cmd_pretty("AT+CPSMS?")
# +CPSMS: 0,,,"10100011","00100001"

send_at_cmd_pretty("AT+CREG=?")
# # supported n's: (0,1,2)
# # Set command controls the presentation of an
# # * unsolicited result code
# #   +CREG: <stat>
# #   when <n>=1 and
# #   there is a change in the MT's circuit mode network registration status in GERAN/UTRAN/E-UTRAN, or
# # * unsolicited result code
# #   +CREG: <stat>[,[<lac>],[<ci>],[<AcT>]]
# #   when <n>=2 and
# #   there is a change of the network cell in GERAN/UTRAN/E-UTRAN. The parameters <AcT>, <lac> and <ci> are sent only if available.
# # * The value <n>=3 further extends the unsolicited result code with
# #   [,<cause_type>,<reject_cause>], when available, when the value of <stat> changes.
# send_at_cmd_pretty("AT+CREG?")

def get_access_technology(act):
    if act == 0:
        return "GSM"
    elif act == 1:
        return "GSM Compact"
    elif act == 2:
        return "UTRAN"
    elif act == 3:
        return "GSM w/EGPRS"
    elif act == 4:
        return "UTRAN w/HSDPA"
    elif act == 5:
        return "UTRAN w/HSUPA"
    elif act == 6:
        return "UTRAN w/HSDPA and HSUPA"
    elif act == 7:
        return "E-UTRAN"
    else:
        return "dunno"
        # I keep getting act == 9 ... no clue what that means, docs only go up until 7
        # raise Exception("get_access_technology failed {}".format(act))

def get_creg_stat(stat):
    if stat == 0:
        return "not registered"
    elif stat == 1:
        return "registered, home"
    elif stat == 2:
        return "searching"
    elif stat == 3:
        return "denied"
    elif stat == 4:
        return "unknown"
    elif stat == 5:
        return "registered, roaming"
    elif stat == 9:
        return "registered, CSFB not preferred"
    else:
        raise Exception("get_creg_stat failed {}".format(stat))

# for n in range(0,4):
n = 2
# Possible values for access technology are,
(ok, val) = send_at_cmd_pretty("AT+CREG=" + str(n))
if not ok:
    print(n, "CREG failed")
    # continue
(ok, creg) = send_at_cmd_pretty("AT+CREG?", False)
# print(ok, creg)
ret = creg[0].split(" ")[1].split(",")
if (n != int(ret[0])):
    raise Exception("CREG error ({}!={})".format(n, ret[0]))
s = int(ret[1])
print(s,"='", get_creg_stat(s), "'", end=" ")
if len(ret) > 2:
    print("lac=", ret[2], "ci=", ret[3], "AcT=", ret[4], end="=")
    print("'", get_access_technology(ret[4]), "'", end=" ")
if len(ret) > 5:
    print("FIXME: <cause_type>,<reject_cause>", end=" ")
print()



send_at_cmd_pretty("AT+CEREG=5")
(ok, resp) = send_at_cmd_pretty("AT+CEREG?", True)
respv = resp[0].split(" ")[1].split(",")
print(len(respv), ":", respv)

print("Sequans modem version:", send_at_cmd_pretty("AT+CGMR", False)[1][0])
print("Sequans modem version:", send_at_cmd_pretty("ATI1", False)[1][0])

print(send_at_cmd_pretty("AT+CPSI?", True)) # Get Network Info
(ok, vec) = send_at_cmd_pretty("AT+COPS?", False)  # Check Network Name
cops = vec[0].split(" ")[1].split(",")
print("COPS:", len(cops), "mode", cops[0], end=" ")
if len(cops) > 1:
    print("format", cops[1], "oper", cops[2], "act", cops[3], end=" ")
print()
print(send_at_cmd_pretty("AT+CNMP?", True)) # GSM/LTE Preference
print(send_at_cmd_pretty("AT+CMNB?", True)) # CAT-M/NB-IoT Preference
print(send_at_cmd_pretty("AT+CBANDCFG?", True)) # CAT-M or NB-IoT Band
print(send_at_cmd_pretty("AT+CNSMOD?", True)) # Check Network System Mode

# 0 -> 0, 5
# 1 -> 1, 5
# 2 -> ['2', '5', '"2B5F"', '"0186B966"', '9']
#       n,   stat, tac,     ci,           AcT


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


send_at_cmd_pretty("AT+SQNHWCFG?")

send_at_cmd_pretty("AT+CPSMS?")
