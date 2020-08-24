from network import LTE
import time




def get_at_cmd_response(cmd):
    response = lte.send_at_cmd(cmd).split('\r\n')
    retval = ""
    for line in response:
        if len(line) == 0:
            pass
        elif line == "OK":
            pass
        elif line == "ERROR":
            print(response)
            raise Exception("AT error")
        elif retval != "":
            raise Exception("Ambiguous return value (" + retval + "," + line + ")")
        else:
            retval = line
    return retval

def print_cc(cc):
    if cc == "882" or cc == "883":
        print("XV = International Networks")
    elif cc == "31":
        print("NL = Netherlands")
    elif cc == "44":
        print("UK = UK, Guernsy, Isle of Man, Jersey")
    elif cc == "86":
        print("CN = China")
    else:
        print("unknown")

print("#################################### reading ids ....")
lte = LTE()
print("LTE")
imei = lte.imei()
print("imei", imei)
iccid = lte.iccid()
if iccid == None:
    time.sleep(3)
    iccid = lte.iccid()
print("iccid", iccid)
try:
    imsi = get_at_cmd_response("AT+CIMI")
except:
    print("imsi failed, retry ... ")
    time.sleep(6)
    imsi = get_at_cmd_response("AT+CIMI")
print("imsi", imsi)



print("\n#################################### decoding ids ....")

print()
print("IMEI (International Mobile Equipment Identity) - identifies the device")
print("IMEI", imei, "TAC+Serial+Check len=", len(imei))
#
# IMEI (International Mobile Equipment Identity)
# number of a mobile phone is a 15 digit number unique to a mobile handset.
# The IMEI number is used by a GSM network to identify valid devices
#
# https://www.quora.com/What-is-the-difference-between-ICCID-IMSI-and-IMEI-numbers?share=1

# The IMEI (15 decimal digits: 14 digits plus a check digit)
# or IMEISV (16 decimal digits: 14 digits plus two software version digits)
# includes information on
# - the origin,
# - model,
# - and serial number of the device.
# The model and origin comprise the initial 8-digit portion of the IMEI/SV, known as the Type Allocation Code (TAC).
# The remainder of the IMEI is manufacturer-defined, with a Luhn check digit at the end.
# As of 2004,
# the format of the IMEI is AA-BBBBBB-CCCCCC-D
# The IMEISV does not have the Luhn check digit but instead has two digits for the Software Version Number (SVN), making the format
# AA-BBBBBB-CCCCCC-EE
tac=imei[0:8]
print("TAC (Type Allocation Code) ", tac[0:2], "-", tac[2:], sep='')
print("Serial", imei[8:-1])
print("Check", imei[-1])


print()
print("ICCID (Integrated Circuit Card Identifier) - identifies the SIM")
print("ICCID", iccid, "IIN(MII+CC+II) + Indiv. Account + Check Digit")
# ICCID (Integrated Circuit Card Identifier)
# identifies each SIM internationally. A full ICCID is 19 or 20 characters.
# ICCID can be thought of as the serial number of the SIM Card. It is also
# considered as Issuers Identification Number. In layman's terms, it is sim
# cards ID number.
#
# The format of the ICCID is:
# MMCC IINNNNNN NNNN NN C x
# 1234 56789012 3456 78 9 0
# MM = Major industry identifier (MII), 2 fixed digits, 89 for telecommunication purposes. (ISO 7812 Major industry identifier)
# CC = Country Code 1 to 3 digits, as defined by ITU-T recommendation E.164.
# II = Issuer Identifier 1-4 digigs. Often identical to the Mobile Network Code (MNC).
# N{12} = Account ID ( "SIM numb
# C = Checksum calculated from Luhn algorithm
# X = An extra 20 th digit is re

mii_len = 2 # FIXME, can be 1-3
mii = iccid[0:mii_len]
print("MII (Major Industry Identifier)", mii, end=" ")
if mii == "89":
    print("telecommunication purposes")
else:
    print("unknown")

cc_len = 3
i1 = int(iccid[mii_len])
i2 = int(iccid[mii_len+1])
if i1 == 1:
    cc_len = 2
elif i1 == 2 and i1 in (0,                   7):
    cc_len = 2
elif i1 == 3 and i2 in (0, 1, 2, 3, 4,    6,       9):
    cc_len = 2
elif i1 == 4 and i2 in (0, 1,    3, 4, 5, 6, 7, 8, 9):
    cc_len = 2
elif i1 == 5 and i2 in (   1, 2, 3, 4, 5, 6, 7, 8):
    cc_len = 2
elif i1 == 6 and i2 in (0, 1, 2, 3, 4, 5, 6):
    cc_len = 2
elif i1 == 7:
    cc_len = 2
elif i1 == 8 and i2 in (   1, 2,    4,    6):
    cc_len = 2
elif i1 == 9 and i2 in (0, 1, 2, 3, 4, 5,       8):
    cc_len = 2

cc = iccid[2:2 + cc_len]
print("CC (Country calling code ITU-T E.164)", cc, end=" ")
print_cc(cc)

rest = iccid[mii_len + cc_len:]
print("II (Issue Identifier 1-4 digits, often equal to MNC)", rest[0:4])




print()
print("IMSI (International Mobile Subscriber Identity) - identifies the subscriber (stored on SIM)")
print("IMSI", imsi, "MCC+MNC+MSIN")
# IMSI (International Mobile Subscriber Identity)
# It is stored inside the SIM.  It consists of three part.
#
#     Mobile Country Code (MCC) : First 3 digits of IMSI gives you MCC.
#                                 e.g. 310 for USA
#     Mobile Network Code (MNC) : Next 2 or 3 digits give you this info.
#                                 e.g. 410 for AT&T
#     Mobile Station ID (MSID)  : Rest of the digits. Gives away the network you
#                                 are using like IS-95, TDMA , GSM etc.
#
#     Mobile network code (MNC) is used in combination with a mobile country
#     code (MCC) (also known as a "MCC / MNC tuple") to uniquely identify a
#     mobile phone operator/carrier.
mcc = imsi[0:3]
print("MCC (Mobile Country Code)", mcc, end=": ")
print("region(", mcc[0], ")=", sep='', end='')
if mcc[0] == '0':
    print("Test network", end=", ")
elif mcc[0] == '2':
    print("Europe", end=", ")
elif mcc[0] == '3':
    print("North Americ and Carribean", end=", ")
elif mcc[0] == '4':
    print("Asia and Middle East", end=", ")
elif mcc[0] == '5':
    print("Australia and Oceania", end=", ")
elif mcc[0] == '6':
    print("Africa", end=", ")
elif mcc[0] == '7':
    print("South and Central America", end=", ")
elif mcc[0] == '9':
    print("Worldwide", end=", ")
else :
    print("unknown", end=", ")

print("country=", sep='', end='')
if mcc == "001":
    print("Test networks")
elif mcc == "204":
    print("NL")
elif mcc == "234":
    print("GB, GG, IM, JE")
elif mcc == "901":
    print("International operators")
else:
    print("unknown")

mnc2=imsi[3:5] # europe 2 digits
mnc3=imsi[3:6] # north america 3 digits
mnc_len = 2
print("MNC (Mobile Network Code)", end=" ")
if mcc == "001" and mnc2 == "01":
    print("01 Test Network")
elif mcc == "204" and mnc2 == "08":
    print("08 KPN")
    print("bands: GSM 900 / GSM 1800 / UMTS 900 / UMTS 2100 / LTE 800 / LTE 1800 / LTE 2100 / LTE 2600")
elif mcc == "234" and mnc2 == "50":
    print("50 Jersey Telecom Ltd.")
    print("bands: GSM 1800 / UMTS 2100 / LTE 800 / LTE 1800 / LTE 2600")
elif mcc == "901" and mnc2 == "28":
    print("28 Vodafone")
else:
    mnc_len = None
    print(mnc2, "/", mnc3, "unknown")
print("MSIN (Mobile Subsciption Identification Number) ", end='')
if mnc_len is None:
    print("2/3? ({}){}".format(imsi[5], imsi[6:]))
elif mnc_len == 2:
    print("2:{}".format(imsi[5:]))
elif mnc_len == 3:
    print("3:{}".format(imsi[6:]))
