from network import LTE
import time

def at(cmd):
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

_mcc_region = {
    '0':"Test network",
    '2':"Europe",
    '3':"North Americ and Carribean",
    '4':"Asia and Middle East",
    '5':"Australia and Oceania",
    '6':"Africa",
    '7':"South and Central America",
    '9':"Worldwide",
}
def mcc_region(r):
    try:
        return _mcc_region[r]
    except:
        return "unknown"

# https://en.wikipedia.org/wiki/List_of_country_calling_codes
_country = {
    "882": "XV - International Networks",
    "883": "XV - International Networks",
    "31":"NL - Netherlands",
    "44":"UK - UK, Guernsy, Isle of Man, Jersey",
    "86":"CN - China",
}
def country(cc):
    try:
        return _country[cc]
    except:
        return "unknown"

# https://en.wikipedia.org/wiki/Mobile_country_code
_mcc = {
    "001":"Test networks",
    "204":"NL",
    "234":"GB, GG, IM, JE",
    "901":"International operators",
}
def mcc(c):
    try:
        return _mcc[c]
    except:
        return "unknown"

# https://en.wikipedia.org/wiki/Mobile_country_code
# An "MCC/MNC tuple" uniquely identifies a mobile network operator (carrier)
# MCC is three digits, MNC is two or three digits
_operator = {
    "00101":"Test Network",
    "20404":"Vodafone NL",
    "20408":"KPN",
    "20416":"T-Mobile",
    "23450":"Jersey Telecom",
    "90128":"Vodafone Int",
}
def find_operator(mcc_mnc_tuple=None, mcc=None, mnc=None):
    if mcc_mnc_tuple is None:
        if mcc is None:
            return "(no mcc)",None
        elif mnc is None:
            return "(mcc={}, no mnc)".format(mcc),None
        else:
            mcc_mnc_tuple = mcc + mnc
    mnc_len = len(mcc_mnc_tuple) - 3
    try:
        # firstly try to find as is
        return (_operator[mcc_mnc_tuple],mnc_len)
    except:
        if mnc_len == 3:
            # secondly, try whether there is a 2 digit mnc
            try:
                return _operator[mcc_mnc_tuple[:-1]],2
            except:
                pass
    # lastly, we just don't know
    return "unknown({})".format(mcc_mnc_tuple),None

# https://en.wikipedia.org/wiki/Mobile_Network_Codes_in_ITU_region_2xx_(Europe)#N
_operator_bands = {
    "20408":"GSM 900 / GSM 1800 / UMTS 900 / UMTS 2100 / LTE 800 / LTE 1800 / LTE 2100 / LTE 2600",
    "23450":"GSM 1800 / UMTS 2100 / LTE 800 / LTE 1800 / LTE 2600"
}

def imei():
    _imei = lte.imei()
    # print("imei", _imei)
    print("# IMEI (International Mobile Equipment Identity) TAC+Serial+Check len=", len(_imei))
    print("# device identifier")
    print("IMEI", _imei)
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
    tac=_imei[0:8]
    print("  TAC (Type Allocation Code): ", tac[0:2], "-", tac[2:], sep='')
    print("  Serial:", _imei[8:-1])
    print("  Check:", _imei[-1])

def iccid():
    _iccid = lte.iccid()
    if _iccid == None:
        time.sleep(3)
        _iccid = lte.iccid()
    # print("iccid", _iccid)

    print("# ICCID (Integrated Circuit Card Identifier) IIN(MII+CC+II)+Indiv.Account+Check Digit")
    print("# SIM identifier")
    print("ICCID", _iccid)
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
    mii = _iccid[0:mii_len]
    print("  MII (Major Industry Identifier):", mii, end=" - ")
    if mii == "89":
        print("telecommunication purposes")
    else:
        print("unknown")

    cc_len = 3
    i1 = int(_iccid[mii_len])
    i2 = int(_iccid[mii_len+1])
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

    cc = _iccid[2:2 + cc_len]
    print("  CC (Country calling code):", cc, end=" ") # ITU-T E.164
    print(country(cc))

    rest = _iccid[mii_len + cc_len:]
    print("  II (Issue Identifier 1-4 digits, often equal to MNC):", rest[0:4])

def imsi():
    try:
        _imsi = at("AT+CIMI")
    except:
        # print("imsi failed, retry ... ")
        time.sleep(6)
        _imsi = at("AT+CIMI")
    return _imsi

def imsi_decode(_imsi, verbose=False):
    if verbose:
        # print("imsi", _imsi)
        print("# IMSI (International Mobile Subscriber Identity) MCC+MNC+MSIN")
        print("# subscriber identification") # stored on SIM
        print("IMSI", _imsi)
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
    _mcc = _imsi[0:3]
    if verbose:
        print("  MCC region:", _mcc[0], '-', mcc_region(_mcc[0]))
        print("  MCC (Mobile Country Code):", _mcc, '-', mcc(_mcc))
    op,mnc_len = find_operator(_imsi[0:6])
    if mnc_len is None:
        if verbose:
            print("  Can't find operator")
            return (_mcc,None,None)
    _mnc=_imsi[3:3+mnc_len]
    _msin=_imsi[3+mnc_len:]
    if verbose:
        print("  Operator: ", _mcc, _mnc, " - ", op, sep='')
        print("  MNC (Mobile Network Code):", _mnc )
        print("  MSIN (Mobile Subsciption Identification Number):", _msin)
    return (_mcc,_mnc,_msin)


if __name__ == '__main__':
    lte = LTE()
    imei()
    print()
    iccid()
    print()
    imsi_decode(imsi(),verbose=True)
