import time
import machine
from network import LTE
import socket
import sys
import os
import binascii
import pycom

# from sleep import sleep
try: from http_get import http_get
except: pass
try: import sqnsupgrade
except: pass
try: from sdcard import sd
except: pass
try: from whoami import whoami
except: pass
try: from ntp import *
except: pass
try: from shell import *
except: pass


use_edrx = False
use_psm = False
lte_debug = False
# lte_debug = True

attach_timeout_s = 1800

# if you run this script multiple times via Play button
# the following try/except avoids unnecesary re-initialization
# todo: what does this mean for import & run from another, e.g., main.py
try:
    l
    # print("l exists, no initialization needed")
except:
    # print("initialize l=None")
    l = None

band_to_earfcn = [ # (low, mid, high) # band
    (	   0	,	 300	,	 599	), # band 	1
    (	 600	,	 900	,	1199	), # band 	2
    (	1200	,	1575	,	1949	), # band 	3
    (	1950	,	2175	,	2399	), # band 	4
    (	2400	,	2525	,	2649	), # band 	5
    (	2650	,	2700	,	2749	), # band 	6
    (	2750	,	3100	,	3449	), # band 	7
    (	3450	,	3625	,	3799	), # band 	8
    (	3800	,	3975	,	4149	), # band 	9
    (	4150	,	4450	,	4749	), # band 	10
    (	4750	,	4850	,	4949	), # band 	11
    (	5010	,	5090	,	5179	), # band 	12
    (	5180	,	5230	,	5279	), # band 	13
    (	5280	,	5330	,	5379	), # band 	14
    (	5730	,	5790	,	5849	), # band 	17
    (	5850	,	5925	,	5999	), # band 	18
    (	6000	,	6075	,	6149	), # band 	19
    (	6150	,	6300	,	6449	), # band 	20
    (	6450	,	7125	,	6599	), # band 	21
]

earfcn_to_band = {}
for band in range(1, len(band_to_earfcn)):
    earfcn_to_band[band_to_earfcn[band]] = band

def sleep(s, verbose=False):
    if verbose:
        print("sleep(", s, ") ", end="")
    while s > 0:
        if verbose:
            print(s, end=" ")
        time.sleep(1)
        s -= 1
    if verbose:
        print("")

def lte_cb_handler(arg):
    print("CB: LTE Coverage lost")
    pycom.rgbled(0x220000)

def lte_init_psm_on():
    global l
    print("lte_init_psm_on")
    l = LTE(psm_period_value=12, psm_period_unit=LTE.PSM_PERIOD_1H,
          psm_active_value=5, psm_active_unit=LTE.PSM_ACTIVE_2S, debug=lte_debug)

def lte_init_psm_off():
    global l
    print("lte_init_psm_off")
    try:
        l = LTE(psm_period_value=1, psm_period_unit=LTE.PSM_PERIOD_DISABLED,
                  psm_active_value=5, psm_active_unit=LTE.PSM_ACTIVE_DISABLED, debug=lte_debug)
    except Exception as e:
        print("Exception:", e)
        print("try without psm args")
        try:
            l = LTE(debug=lte_debug)
        except Exception as e:
            print("Exception:", e)
            print("try without debug")
            l = LTE()

def lte_init(use_psm=use_psm):
    if l is not None:
        return
    if use_psm:
        lte_init_psm_on()
    else:
        lte_init_psm_off()

def at(cmd='', verbose=False, quiet=True, do_return=False, raise_on_error=True):
    if l is None:
        lte_init()
    if cmd == '':
        cmd='AT'
        quiet=False
    if verbose:
        print(cmd)
    response = l.send_at_cmd(cmd)
    lines = response.split('\r\n')
    retval = ""
    for line in lines:
        if ( len(line) == 0 ):
            continue
        elif quiet and line == 'OK':
            continue
        else:
            if do_return:
                if line == 'ERROR' and raise_on_error:
                    raise Exception('AT cmd "' + cmd + '" returned ERROR: "' + response + '"')
                retval += line + '\n'
            else:
                print(line)
    if do_return:
        return retval

def at_log(cmd):
    resp = ""
    last_resp = ""
    while True:
        resp = at(cmd, do_return=True, raise_on_error=False).strip()
        if resp != last_resp:
            print(time.time(), resp)
            last_resp = resp
        sleep(1)

def lte_version(debug=False):
    if not l:
        lte_init()
    if debug:
        at('AT!="showver"')
        at('AT!="get_sw_version"')
    else:
        # at('AT+CGMR')
        # UE5.2.0.3
        at('ATI1', quiet=True)

def smod():
    at('AT+SMOD?')

def bmod():
    at('AT+BMOD?')

def bands():
    if l is None:
        lte_init()
    import re
    # <vendor>GM01Q-REV4 configuration SQN3330 A1A3 SKY68001-31 17 bands R03</vendor>  1 2 3 4 5 8 12 13 14 17 18 19 20 25 26 28 66
    # <vendor>EVK41-A configuration SQN3330 A1A3 SKY68001-31 R01</vendor>                  3 4     12 13             20       28
    # grep('band ', at('AT+SMDD', do_return=True))
    # todo: how to detect missing SMDD? line==ERROR? or try/except?
    for line in at('AT+SMDD', do_return=True).split('\n'):
        if re.search('vendor', line):
            # print(line)
            # hexdump(buf=line)
            line = line.strip()
            if line == '<vendor>EVK41-A configuration SQN3330 A1A3 SKY68001-31 R01</vendor>':
                print('6 bands, I guess')
            elif line == '<vendor>GM01Q-REV4 configuration SQN3330 A1A3 SKY68001-31 17 bands R03</vendor>':
                print('17 bands, I guess')
            else:
                print('not sure which band set we have ... ')

def imsi():
    at('AT+CIMI')

def cfun(fun=None):
    if fun is not None:
        a = 'AT+CFUN='+str(fun)
        print(a)
        f = at(a, do_return=True).strip()
    else:
        f = at('AT+CFUN?', do_return=True).strip()
        import re
        return int(re.search('[0-9]$', f).group(0))

def cgatt(state=None):
    if state is not None:
        a = 'AT+CGATT=' + str(state)
        at(a)
    else:
        r = at('AT+CGATT?', do_return=True).strip()
        print(r)

def cereg():
    r = at('AT+CEREG?', do_return=True).strip()
    print(r)
    r = r.split('+CEREG: ')[1]
    #print('_', r ,'_', sep='')
    v = r.split(',')
    n = int(v[0])
    print('+CEREG: n=', n, sep='', end='')
    if n == 0: print('=no urc', end='')
    elif n == 2: print('=reg+loc urc', end='')
    s = int(v[1])
    print(', stat:', s, end='')
    if s == 0: print('=not registered, not searching', end='')
    elif s == 1: print('=registered', end='')
    elif s == 2: print('=searching', end='')
    if len(v) > 2:
        tac = v[2].strip('"')
        ci = v[3].strip('"')
        act = v[4]
        print(' tac=', tac, ' ci=', ci, ' act=', act, sep='', end='')
    print()

def psm():
    if not l:
        lte_init()
    p = l.psm()
    if p[0]:
        print("psm enabled: period=", p[1], end='*')
        P = int(p[1])
        if p[2] == LTE.PSM_PERIOD_2S:
            P *= 2
            print("2s = ", P, "s" , sep='', end=', ')
        elif p[2] == LTE.PSM_PERIOD_30S:
            P *= 30
            print("30s = ", P, "s", sep='', end=', ')
        elif p[2] == LTE.PSM_PERIOD_1M:
            print("1m", sep='', end=', ')
        elif p[2] == LTE.PSM_PERIOD_1H:
            print("1h", end=', ')
        else:
            # PSM_PERIOD_10M
            # PSM_PERIOD_10H
            # PSM_PERIOD_320H
            # PSM_PERIOD_DISABLED
            print("FIXME", p[2])

        print('active=', p[3], end='*' )
        if p[4] == LTE.PSM_ACTIVE_2S:
            print("2s = ", p[3]*2, 's', sep='', end=' ')
        else:
            print('FIXME', p[4], end=' ')
            # PSM_ACTIVE_1M
            # PSM_ACTIVE_6M
            # PSM_ACTIVE_DISABLED
    else:
        print("psm disabled", end=' ')
    print(p)

# def edrx():
#     at('AT+SQNEDRX?') # "0010"')
#     # +SQNEDRX: 2,4,"0101","0000"
#     # AT+CEDRXS=[<mode>,[,<AcTtype>[,<Requested_eDRX_value>]]
#     # mode:
#     #   0: Disable the use of eDRX
#     #   1: Enable the use of eDRX
#     #   2 Enable the use of eDRX and enable the URC
#     #     +CEDRXP: [,[,<NW- provided_eDRX_value>[,<Paging_time_window>]]]
#     # AcTtype: 4 for E-UTRAN (WB-S1 mode)
#     # Requested_eDRX_value, e.g. 0101 = 81.92s
#
# def edrx_on():
#     print("turn edrx ON")
#     at('AT+SQNEDRX=2,4,"0101","0000"') # 81.92s
#
# def edrx_off():
#     print("turn edrx OFF"),
#     at('AT+SQNEDRX=3')

def lpmc():
    L = 'disablelog 1\nsetlpm airplane=1 enable=1\n'
    #print('# lpm 60:')
    try:
        l = at('AT!="cat /fs/sqn/etc/scripts/60-lpm-enable.cli"', do_return=True)
        if l == L:
            print("lpm is configured (60)")
            return True
        else:
            print("lpm: 60-lpm-enable.cli:", l)
    except Exception as e:
        pass
        print("Exception while reading lpm 60:", e)

    # print('# lpm 61:')
    try:
        l = at('AT!="cat /fs/sqn/etc/scripts/61-lpm-enable.cli"', do_return=True)
        if l == L:
            print("lpm is configured (61)")
            return True
        else:
            print("lpm: 61-lpm-enable.cli:", l)
    except Exception as e:
        pass
        print("Exception while reading lpm 61:", e)

    print("lpm is not configured")
    return False

def lpmc_unconfigure():
    try:
        at('AT!="rm /fs/sqn/etc/scripts/60-lpm-enable.cli"')
    except Exception as e:
        print("lpm rm 60", e)
    try:
        at('AT!="rm /fs/sqn/etc/scripts/61-lpm-enable.cli"')
    except Exception as e:
        print("lpm rm 61", e)
    lpm()

def lpmc_configure():
    try:
        at('AT!="echo setlpm 1 0 0 1 > /fs/sqn/etc/scripts/60-lpm-enable.cli"')
        time.sleep(.1)
        at('AT!="echo disablelog 1 >> /fs/sqn/etc/scripts/60-lpm-enable.cli"')
    except Exception as e:
        print("lpm enable 60", e)
    lpm()

def provider(imsi=None):
    apn = None
    if imsi is None:
        for retry in range(5):
            try:
                imsi = at("AT+CIMI", do_return=True)
                if imsi:
                    break
            except Exception as e:
                if retry > 2:
                    print("imsi failed, retry [", retry, "]... ", e)
                # it doesn't work in CFUN=0
                if cfun() == 0:
                    # maybe we shouldn't mess with it ... but it's just more convenient that way :)
                    print('cfun 4')
                    cfun(4)
                time.sleep(1)
    if imsi is None:
        print("Can't get IMSI")
        return
        raise Exception("Can't get IMSI", imsi)

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
    elif mcc == "204" and mnc2 == "04":
        print("04 Vodafone")
    elif mcc == "204" and mnc2 == "08":
        print("08 KPN")
        apn = 'simpoint.m2m'
        print("bands: GSM 900 / GSM 1800 / UMTS 900 / UMTS 2100 / LTE 800 / LTE 1800 / LTE 2100 / LTE 2600")
    elif mcc == "204" and mnc2 == "16":
        print("16 T-Mobile")
    elif mcc == "234" and mnc2 == "50":
        print("50 Jersey Telecom Ltd.")
        print("bands: GSM 1800 / UMTS 2100 / LTE 800 / LTE 1800 / LTE 2600")
    elif mcc == "901" and mnc2 == "28":
        print("28 Vodafone")
        apn = "pycom.io" # this is for test cards, maybe we need iccid to distinguish
    else:
        mnc_len = None
        print(mnc2, "/", mnc3, "unknown")
    print("provider: APN=", apn, sep='')
    return apn

def fsm(write_file=False, do_return=False):
    if write_file:
        log = at('AT!="fsm"', do_return=True)
        f = open('/flash/fsm.log', 'w')
        f.write("time ")
        f.write(str(time.time()))
        f.write(", isattached:")
        f.write(str(l.isattached()))
        f.write('\n')

        f.write(log)
        f.close()
    elif do_return:
        return at('AT!="fsm"', do_return=do_return)
    else:
        at('AT!="fsm"')

def cat_fsm():
    cat('/flash/fsm.log')

def showphy():
    at('AT!="showphy"')

def stat_log():
    if l is None:
        lte_init()
    # import hashlib
    # m = hashlib.md5()
    f = at('AT!="fsm"', do_return=True)
    s = at('AT!="showphy"', do_return=True)
    r = at('AT+CSQ', do_return=True)
    a = l.isattached()
    #h = m.update(f)
    print(time.time(), a, f, s, r)
    while True:
        f2 = at('AT!="fsm"', do_return=True)
        a2 = l.isattached()
        s2 = at('AT!="showphy"', do_return=True)
        r2 = at('AT+CSQ', do_return=True)
        #h2 = m.update(f2)
        if a != a2:
            f = f2
            s = s2
            a = a2
            r = r2
            print(time.time(), a, f, s, r)
        else:
            if f != f2:
                f = f2
                s = s2
                print(time.time(), a, f, s)
            # if s != s2:
            #     s = s2
            #     print(time.time(), s)
            if r != r2:
                r = r2
                print(time.time(), a, r)

def rssi_old():
    at('AT+CSQ')
    at('AT+VZWRSRP')
    at('AT+VZWRSRQ')
    # fipy-4624 41019
    # time att       rssi                   rsrp                     rsrq
    # 120 False +CSQ: 18,99 +VZWRSRP: 1,6309,-95.60 +VZWRSRQ: 1,6309,-12.10
    # 121 False +CSQ: 20,99 +VZWRSRP: 1,6309,-91.70 +VZWRSRQ: 1,6309,-11.40
    # 122 True +CSQ: 19,99 +VZWRSRP: 1,6309,-92.00 +VZWRSRQ: 1,6309,-11.50
    # 124 True +CSQ: 20,99 +VZWRSRP: 1,6309,-91.90 +VZWRSRQ: 1,6309,-11.20
    # 127 True +CSQ: 18,99 +VZWRSRP: 1,6309,-104.40 +VZWRSRQ: 1,6309,-21.60
    # 137 True +CSQ: 18,99 +VZWRSRP: 1,6309,-91.80 +VZWRSRQ: 1,6309,-11.10
    # 145 True +CSQ: 15,99 +VZWRSRP: 1,6309,-104.90 +VZWRSRQ: 1,6309,-15.70
    # 149 True +CSQ: 17,99 +VZWRSRP: 1,6309,-99.70 +VZWRSRQ: 1,6309,-13.80

    # gpy-b678
    # LR6.0.0.0-41019
    # time att       rssi                   rsrp                     rsrq
    # 58 False +CSQ: 20,99 +VZWRSRP: 1,6309,-90.70  +VZWRSRQ: 1,6309,-11.20
    # 73 False +CSQ: 13,99 +VZWRSRP: 1,6309,-180.10 +VZWRSRQ: 1,6309,-87.20
    # 81 False +CSQ: 20,99 +VZWRSRP: 1,6309,-92.20  +VZWRSRQ: 1,6309,-12.80
    # 84 False +CSQ: 20,99 +VZWRSRP: 1,6309,-91.00  +VZWRSRQ: 1,6309,-11.80
    # 84 True  +CSQ: 20,99 +VZWRSRP: 1,6309,-91.00  +VZWRSRQ: 1,6309,-11.80
    # 85 True  +CSQ: 20,99 +VZWRSRP: 1,6309,-91.60  +VZWRSRQ: 1,6309,-12.60
    # 97 True  +CSQ: 21,99 +VZWRSRP: 1,6309,-90.10  +VZWRSRQ: 1,6309,-11.40
    pass

def rssi(log=False):
    if l is None:
        lte_init()
    csq = at('AT+CSQ', do_return=True).strip()
    rsrp = ""
    rsrq = ""
    rsrp2 = ""
    rsrq2 = ""
    try:
        rsrp = at('AT+VZWRSRP', do_return=True).strip()
        rsrq = at('AT+VZWRSRQ', do_return=True).strip()
    except:
        pass
    a = l.isattached()
    print(time.time(), a, csq, rsrp, rsrq)
    while log:
        a2 = l.isattached()
        csq2 = at('AT+CSQ', do_return=True).strip()
        try:
            rsrp2 = at('AT+VZWRSRP', do_return=True).strip()
            rsrq2 = at('AT+VZWRSRQ', do_return=True).strip()
        except:
            pass
        if a != a2 or csq != csq2 or rsrp != rsrp2 or rsrq != rsrq2:
            a = a2
            csq = csq2
            rsrp = rsrp2
            rsrq = rsrq2
            print(time.time(), a, csq, rsrp, rsrq)

def rsrpq(log=False, do_return=False):
    msg = ""
    last_msg = ""
    while True:
        r = at('AT+CESQ', do_return=True).strip()
        rr = r.split(' ')[1].split(',')
        # RSRP Reference Signal Receive Power [dBm]
        try:
            rsrp = int(rr[5])
        except Exception as e:
            print('Exception', e, rr)
            raise(e)
        msg = 'RSRP=' + str(rsrp) + ':'
        if rsrp == 0:
            msg += ' < -140 dBm (poor)'
        elif rsrp == 255:
            msg += ' unknown'
        else:
            dBm = -140 + rsrp
            msg += ' ' + str(dBm) + 'dBm'
            if dBm < - 100:
                msg += ' (poor)'
            elif dBm < -90:
                msg += ' (fair)'
            elif dBm < -80:
                msg += ' (good)'
            else:
                msg += ' (excellent)'
        # RSRQ Reference Signal Receive Quality [dB]
        rsrq = int(rr[4])
        msg += ', RSRQ=' + str(rsrq) + ':'
        if rsrq == 0:
            msg += ' < -19.5dB (poor)'
        elif rsrq == 255:
            msg += ' unknown'
        else:
            dB = -19.5 + 0.5 * rsrq
            msg += ' ' + str(dB) + 'dB'
            if dB < -20:
                msg += ' (poor)'
            elif dB < -15:
                msg += ' (fair)'
            elif dB < -10:
                msg += ' (good)'
            else:
                msg += ' (excellent)'
        if msg != last_msg:
            if do_return:
                return msg
            print(time.time(), msg)
            last_msg = msg
        if not log:
            break
    # rssi - Received signal strength indication.
    #     0 -113 dBm or less
    #     1 -111 dBm
    #     2 .. 30 -109 .. -53 dBm
    #     31 -51 dBm or greater
    #     99 not known or not detectable
    # ber - Channel bit error rate (in percent).
    #     0 .. 7 as RXQUAL values in the table in 3GPP TS 45.008 [20]
    #     99 not known or not detectable
    # at('AT+CSQ')

    # Reference Signal Receive Power [dBm]
    # +VZWRSRP Verizon Wireles RSRP values for all cells which the UE is measuring
    # <cellID>1, <EARFCN>1, <RSRP>1,
    # <cellID>2,<EARFCN>2, <RSRP>2,
    # ...,
    # <cellID>n, <EARFCN>n, <RSRP>n
    # at('AT+VZWRSRP')
    # +VZWRSRP: 1,6309,-86.00
    # +VZWRSRP: 1,6309,-86.70

    # Reference Signal Receive Quality
    # +VZWRSRQ Verizon Wireless RSRQ [dB]
    # values for all cells which the UE is measuring
    # up to 8 cells. in both RRC_IDLE and RRC_CONNECTED modes
    # <cellID>1, <EARFCN>1, <RSRQ>1,
    # <cellID>2, <EARFCN>2, <RSRQ>2,
    # ...,
    # <cellID>n, <EARFCN>n, <RSRQ>n
    # at('AT+VZWRSRQ')
    # +VZWRSRQ: 1,6309,-12.20
    # +VZWRSRQ: 1,6309,-12.10

    # at('AT+SQNINS=0')
    # # +SQNINS: 0,4,7,,,,,,,,
    # # +SQNINS: 0,13,7,,,,,,,,
    #
    # at('AT+SQNINS=1')
    # # +SQNINS: 1,4,7,,,,,,,,
    # # +SQNINS: 1,13,7,,,,,,,,

    #                RSSI         RSRP          RSRQ         SNR
    # ----------+-----------+-------------+-------------+-----------
    # Excellent |            >-80          > -10
    # Good      |            -80 to -90    -10 to -15
    # Fair      |            -90 to -100   -15 to -20
    # Poor      |            < -100        < -20
    pass

def moni(m=9, do_return=False):
    mn = at('AT+SQNMONI=' + str(m), do_return=True, raise_on_error=False).strip()
    if do_return:
        return mn
    else:
        print(mn)

def lte_attach(apn=None, band=None, timeout_s = attach_timeout_s, do_fsm_log=True, do_rssi_log=True):
    if not l:
        lte_init()
    if l.isattached():
        print("already attached")
    else:
        l.imei()
        lte_version()
        lpmc()
        try:
            whoami()
        except:
            pass
        l.lte_callback(LTE.EVENT_COVERAGE_LOSS, lte_cb_handler)
        if not apn:
            apn = provider()
        else:
            provider()
        print("attach(apn=", apn, ", band=", band, ")", sep='')
        t = time.ticks_ms()
        if apn:
            if band:
                l.attach(apn=apn, band=band)
            else:
                l.attach(apn=apn)
        else:
            if band:
                l.attach(band=band)
            else:
                l.attach()
        print("attach (", (time.ticks_ms() - t ) / 1000, ")" ) # e.g., 0.124 , I think this is usually fast
        lte_waitattached(timeout_s, do_fsm_log=do_fsm_log, do_rssi_log=do_rssi_log)
        print("attaching took", (time.ticks_ms() - t ) / 1000 )
        at('AT+CEREG?')
        # at('AT+SQNMONI=7')
        moni()
        psm()
        # edrx()
        lte_ifconfig()
        d = socket.dnsserver()
        if d[0] == '0.0.0.0':
            print("setting dns server 8.8.8.8")
            socket.dnsserver(0, '8.8.8.8')
        print("DNS:", socket.dnsserver())

def lte_attach_manual(apn=None, band=None, timeout_s = attach_timeout_s, do_fsm_log=True, do_rssi_log=True):
    if not l:
        lte_debug = True
        lte_init()
    if l.isattached():
        print("already attached")
    else:
        if band is None:
            raise Exception('specify band')
            band = 20
        l.lte_init(debug=True)
        t = time.ticks_ms()
        at()
        #at('AT')
        #at('AT+CGATT?')
        cgatt()
        #at('AT+CEREG?')
        cereg()
        #at('AT+CFUN?')
        cfun()
        at('AT+SQNCTM?')
        # SMDD
        at('AT!="showver"')
        at('AT!="clearscanconfig"')
        at('AT!="RRC::addScanBand band=' + str(band) + '"')
        at('AT!=disablelog 1')
        at('AT+CFUN=1')
        at('AT!=setlpm airplane=1 enable=1')
        # if apn:
        #     if band:
        #         l.attach(apn=apn, band=band)
        #     else:
        #         l.attach(apn=apn)
        # else:
        #     if band:
        #         l.attach(band=band)
        #     else:
        #         l.attach()
        print("attach took", (time.ticks_ms() - t ) / 1000 )
        waitattached(timeout_s, do_fsm_log=do_fsm_log, do_rssi_log=do_rssi_log)
        print("attaching took", (time.ticks_ms() - t ) / 1000 )
        at('AT+CEREG?')
        # at('AT+SQNMONI=7')
        moni()
        psm()
        edrx()
        ifconfig()
        d = socket.dnsserver()
        if d[0] == '0.0.0.0':
            print("setting dns server 8.8.8.8")
            socket.dnsserver(0, '8.8.8.8')
        print("DNS:", socket.dnsserver())

def lte_isattached_manual():
    cmds=['AT+CEREG?', 'AT+CGATT?', ]
    for cmd in cmds:
        print(at(cmd, do_return=True).strip(), end=', ')
    rsrpq()
    print()

def lte_isattached():
    try:
        rsrpq()
        moni()
    except:
        pass
    r = l.isattached()
    print('isattached', r)
    return r

def lte_waitattached(timeout_s = attach_timeout_s, do_fsm_log=True, do_rssi_log=True):
    if timeout_s is not None:
        timeout_ms = timeout_s * 1000
    t = time.ticks_ms()
    r = None
    f = None
    if l.isconnected():
        print("isconnected")
    elif l.isattached():
        print("isattached")
        rssi()
    else:
        while not l.isattached():
            if do_fsm_log:
                f2 = grep("TOP FSM|SEARCH FSM", fsm(do_return=True), do_return=True)
                if f != f2:
                    f = f2
                    print(time.time(), '\n', f, sep='')
                #cat_fsm()
            if do_rssi_log:
                # r2 = at('AT+CSQ', do_return=True).strip()
                # r2 = moni(do_return=True)
                r2 = rsrpq(do_return=True)
                if r != r2:
                    r = r2
                    print(time.time(), r)
                    # rssi()
            time.sleep(0.1)
            if timeout_s is not None and time.ticks_ms() - t > timeout_ms:
                raise Exception("Could not attach in {} s".format(timeout_s))
        print("isattached", l.isattached(), "turned true after {} s".format(( time.ticks_ms()-t )  / 1000 ))
        # rssi()
        moni(9)

def sqnsping(num=10, interval=0, do_fsm=False, quiet=False):
    lte_init()
    if not l.isattached():
        attach()
    # if l.isconnected():
    #     l.pppsuspend()
    ct = 0
    ct_succ = 0
    ct_fail = 0
    while num < 0 or ct < num:
        succ = False
        try:
            resp = at('AT!="IP::ping 8.8.8.8"', do_return=True)
            if not quiet:
                print(resp)
            succ = "from" in resp
        except Exception as e:
            print("Exception during ping", e)
        if succ:
            ct_succ += 1
        else:
            ct_fail += 1
        if do_fsm:
            fsm()
        ct += 1
        if (num < 0 or ct < num):
            # we're still going
            if interval < 0:
                sleep(-interval)
                if succ:
                    interval *= 2
                else:
                    interval /= 2
                    interval = min(-1, interval)
            elif interval:
                sleep(interval)
    print("pings:", num, " failed:", ct_fail, " succeeded:", ct_succ, " -- ", round(ct_succ/num*100.0,1), "%", sep="")

def lte_connect():
    if l.isconnected():
        print("already connected")
        return
    if not l.isattached():
        attach()
    print("connect")
    t = time.ticks_ms()
    l.connect()
    print("connect took", (time.ticks_ms() - t ) / 1000 )
    timeout_ms = 60000
    while not l.isconnected():
        time.sleep(0.1)
        if time.ticks_ms() - t > timeout_ms:
            raise Exception("Could not connect in {} s".format((time.ticks_ms() - t )/ 1000 ))
    print("connecting took", (time.ticks_ms() - t ) / 1000 )

def lte_isconnected():
    return l.isconnected()

def lte_ifconfig(verbose=False):
    for attempt in range(0,3):
        try:
            cgcontrdp = at('AT+CGCONTRDP=1', do_return=True)
            if cgcontrdp.strip() == 'ERROR':
                print('IP not set')
            else:
                if verbose:
                    print(cgcontrdp)
                    # '\r\n+CGCONTRDP: 1,5,"spe.inetd.vodafone.nbiot.mnc028.mcc901.gprs","10.175.213.177.255.255.255.255","","10.105.16.254","10.105.144.254","","",,,1430\r\n\r\nOK\r\n'
                    # l.send_at_cmd('AT+CGDCONT?')
                    # '\r\n+CGDCONT: 1,"IP","spe.inetd.vodafone.nbiot",,,,0,0,0,0,0,0,1,,0\r\n\r\nOK\r\n'
                    at('AT!="ifconfig"')
                else:
                    cgcontrdp_list = cgcontrdp.split(',')
                    ip_mask = cgcontrdp_list[3].split('.')
                    print('APN:', cgcontrdp_list[2])
                    print('IP:', '.'.join(ip_mask[0:4]))
                    print('mask:', '.'.join(ip_mask[4:8]))
            return
        except Exception as ex:
            print("ifconfig Exception:", ex)
    raise Exception("Could not ifconfig")

def lte_ifconfig_suspend():
    l.pppsuspend()
    ifconfig()
    l.pppresume()

def dl(kb=None):
    lte_init()
    if not l.isattached():
        attach()
    if not l.isconnected():
        try:
            print("resume")
            l.pppresume()
            if not l.isconnected():
                print("connect")
                connect()
        except Exception as e:
            print("couldn't resume, try to connect (", e, ")", sep='')
            try:
                connect()
            except Exception as e:
                print("connect failed, try second time (", e, ")")
                sleep(1)
                connect()
    print("download")
    t = time.ticks_ms()
    r = http_get(kb=kb)
    print(r)
    print("http_get took", (time.ticks_ms() - t)/1000)
    if not r[0]:
        raise Exception("http_get returned false")

def test_dl(delays = [10, 60, 300], repetitions=3):
    lte_init()
    if not l.isattached():
        attach()
    if not l.isconnected():
        try:
            print("resume")
            l.pppresume()
            if not l.isconnected():
                print('connect')
                connect()
        except Exception as e:
            print("couldn't resume, try to connect (", e, ")", sep='')
            try:
                connect()
            except:
                print("failed, try second time")
                sleep(1)
                connect()
    # repetitions = 3
    # delays = [10, 60, 300 ] # , 600]
    results = []
    for d in delays:
        results_for_delay = []
        for r in range(repetitions):
            success = False
            results_for_delay_rep = (False, 0, 0)
            for a in range(3):
                print("\ntest_dl (delay# after:", d, " repetition:", r, "attempt:", a, ")")
                pretty_gmt()
                try:
                    #dl()
                    r = http_get()
                    if r[0]:
                        results_for_delay_rep = (True, a, r[6])
                        success=True
                        break
                except Exception as e:
                    print("Exception during download:", e)
            results_for_delay += [results_for_delay_rep]
            # if not success:
            #     raise Exception("test_dl failed (delay after:", d, " repetition:", r, "attempt:", a, ")")
            sleep(d, verbose=True)
        results += [ (d, results_for_delay) ]
    print("test_dl results:")
    for d_reps in results:
        #print('X', d_reps, 'Y')
        print("% 3d     " %(d_reps[0]), end='')
        for rep in d_reps[1]:
            if rep[0]:
                print("succ:", rep[1], "@", round(rep[2],1), sep='', end='   ')
            else:
                print("fail", end='          ')
            #print('x', rep, 'y', end='')
        print()

def long_at():
    if not l.isattached():
        attach()
    # from network import LTE
    # l = LTE(debug=True)
    #
    # attach()

    # set the socket option to expect the TX bytes to be provided in the form of HEX values.
    l.send_at_cmd('AT+SQNSCFGEXT=1,1,0,0,0,1')

    l.send_at_cmd('AT+SQNSD=1,1,5555,"80.101.10.222",0,8888,1')
    sleep(1)

    # short
    l.send_at_cmd('AT+SQNSSENDEXT=1,10')
    l.send_at_cmd('0102030405060708090a')
    sleep(1)

    # Request the transmission of 70 bytes (which will be 140 long HEX string)
    l.send_at_cmd('AT+SQNSSENDEXT=1,70')
    # 140 characters -> 70 bytes. This messages could not be sent with the default implementation.
    l.send_at_cmd('A343164303A3730313A313130303A303A303A303A32303630886368A343164303A3730313A313130303A303A303A303A32303630886368A343164303A3730313A313130303A3')
    sleep(1)

    # two chunks + remaining
    l.send_at_cmd('AT+SQNSSENDEXT=1,140')
    l.send_at_cmd('A343164303A3730313A313130303A303A303A303A32303630886368A343164303A3730313A313130303A303A303A303A32303630886368A343164303A3730313A313130303A3A343164303A3730313A313130303A303A303A303A32303630886368A343164303A3730313A313130303A303A303A303A32303630886368A343164303A3730313A313130303A3')
    sleep(1)

    # corner case two chunks and no remaining
    l.send_at_cmd('AT+SQNSSENDEXT=1,124')
    l.send_at_cmd('0102030405060708090a0102030405060708090a0102030405060708090a0102030405060708090a0102030405060708090a0102030405060708090a0102030405060708090a0102030405060708090a0102030405060708090a0102030405060708090a0102030405060708090a0102030405060708090a01020304')
    sleep(1)

    # Shutdown socket
    l.send_at_cmd('AT+SQNSH=1')
    sleep(1)

def lte_reset():
    print('lte_reset')
    l.reset()

def lte_detach():
    l.detach()

def lte_disconnect():
    l.disconnect()

def lte_deinit(detach=True, reset=False):
    global l
    if l:
        print("lte_deinit(detach=", detach, "reset=", reset, ")")
        l.deinit(detach=detach, reset=reset)
        l = None
        return True
    else:
        print("Can't deinit")

if __name__ == "__main__":
    print(os.uname().sysname.lower() + '-' + binascii.hexlify(machine.unique_id()).decode("utf-8")[-4:], "lte.py")
    lte_version()
    lpmc()
    provider()
    # bands()
    lte_attach()
    # lte_init_psm_on()
    # attach()
    # connect()
    # ntp.sync()
    # dl()
    # test_dl()
    # machine.deepsleep(10000)
    # attach(band=20)
    # sqnsping(10)
    # connect()
    # dl()

    pass
