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

print(os.uname().sysname.lower() + '-' + binascii.hexlify(machine.unique_id()).decode("utf-8")[-4:], "lte.py")

use_edrx = False
use_psm = False
lte_debug = False

settle_s = 0 # 4
measure_s = 0 # 10
attach_timeout_s = 1800

try:
    lte
except:
    lte = None

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

def msg(*m):
    print(time.time(), m)

def measure(m, s=measure_s):
    if not s:
        return
    sleep(settle_s)
    pretty_time()
    msg(m, "start")
    sleep(s)
    msg(m, "end")

def m(s=10):
    print(time.time(), "begin ({})".format(s))
    sleep(s)
    print(time.time(), "end ({})".format(s))

def cb_handler(arg):
    print("CB: LTE Coverage lost")
    pycom.rgbled(0x220000)

def init_psm_on():
    print("init and turn psm on")
    return LTE(psm_period_value=1, psm_period_unit=LTE.PSM_PERIOD_1H,
          psm_active_value=5, psm_active_unit=LTE.PSM_ACTIVE_2S, debug=lte_debug)

def init_psm_off():
    print("init and turn psm off")
    try:
        return LTE(psm_period_value=1, psm_period_unit=LTE.PSM_PERIOD_DISABLED,
                  psm_active_value=5, psm_active_unit=LTE.PSM_ACTIVE_DISABLED, debug=lte_debug)
    except Exception as e:
        print("Exception:", e)
        print("try without psm")
        try:
            return LTE(debug=lte_debug)
        except Exception as e:
            print("Exception:", e)
            print("try without debug")
            return LTE()

def init():
    global lte
    if lte is None:
        if use_psm:
            lte=init_psm_on()
        else:
            lte=init_psm_off()

def at(cmd='', quiet=True, do_return=False, raise_on_error=True):
    if lte is None:
        init()
    if cmd == '':
        cmd='AT'
        quiet=False
    response = lte.send_at_cmd(cmd)
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

def version(debug=False):
    if not lte:
        init()
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

def fsm(write_file=False, do_return=False):
    if write_file:
        log = at('AT!="fsm"', do_return=True)
        f = open('/flash/fsm.log', 'w')
        f.write("time ")
        f.write(str(time.time()))
        f.write(", isattached:")
        f.write(str(lte.isattached()))
        f.write('\n')

        f.write(log)
        f.close()
    elif do_return:
        return at('AT!="fsm"', do_return=do_return)
    else:
        at('AT!="fsm"')

def cat_fsm():
    cat('/flash/fsm.log')

def stat_log():
    if lte is None:
        init()
    # import hashlib
    # m = hashlib.md5()
    f = at('AT!="fsm"', do_return=True)
    s = at('AT!="showphy"', do_return=True)
    r = at('AT+CSQ', do_return=True)
    a = lte.isattached()
    #h = m.update(f)
    print(time.time(), a, f, s, r)
    while True:
        f2 = at('AT!="fsm"', do_return=True)
        a2 = lte.isattached()
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
    # rssi - Received signal strength indication.
    #     0 -113 dBm or less
    #     1 -111 dBm
    #     2 .. 30 -109 .. -53 dBm
    #     31 -51 dBm or greater
    #     99 not known or not detectable
    # ber - Channel bit error rate (in percent).
    #     0 .. 7 as RXQUAL values in the table in 3GPP TS 45.008 [20]
    #     99 not known or not detectable
    at('AT+CSQ')

    # Reference Signal Receive Power [dBm]
    # +VZWRSRP Verizon Wireles RSRP values for all cells which the UE is measuring
    # <cellID>1, <EARFCN>1, <RSRP>1,
    # <cellID>2,<EARFCN>2, <RSRP>2,
    # ...,
    # <cellID>n, <EARFCN>n, <RSRP>n
    at('AT+VZWRSRP')
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
    at('AT+VZWRSRQ')
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

def bands():
    if lte is None:
        init()
    grep('vendor', at('AT+SMDD', do_return=True))

def rssi(log=False):
    if lte is None:
        init()
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
    a = lte.isattached()
    print(time.time(), a, csq, rsrp, rsrq)
    while log:
        a2 = lte.isattached()
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

def rsrpq(log=False):
    msg = ""
    last_msg = ""
    while log:
        r = at('AT+CESQ', do_return=True).strip()
        rr = r.split(' ')[1].split(',')
        rsrq = int(rr[4])
        rsrp = int(rr[5])
        msg = 'RSRP=' + str(rsrp) + ':'
        if rsrp == 0:
            msg += ' <-140 dBm'
        elif rsrp == 255:
            msg += 'not known'
        else:
            dBm = -140 + rsrp
            msg += ' <' + str(dBm) + 'dBm'
        msg += ', RSRQ=' + str(rsrq) + ':'
        if rsrq == 0:
            msg += ' <-19.5dB'
        elif rsrq == 255:
            msg += 'not known'
        else:
            db = -19.5 + 0.5 * rsrq
            msg += ' <' + str(db) + 'dB'
        if msg != last_msg:
            print(time.time(), msg)
            last_msg = msg

def showphy():
    at('AT!="showphy"')

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

def psm():
    p = lte.psm()
    if p[0]:
        print("psm enabled:", end=' period:')
        print(p[1], end='*')
        if p[2] == LTE.PSM_PERIOD_2S:
            print("2s", end=', ')
        elif p[2] == LTE.PSM_PERIOD_30S:
            print("30s", end=', ')
        elif p[2] == LTE.PSM_PERIOD_1H:
            print("1h", end=', ')
        else:
            print("fixme", p[2])
            # PSM_PERIOD_30S
            # PSM_PERIOD_1M
            # PSM_PERIOD_10M
            # PSM_PERIOD_1H
            # PSM_PERIOD_10H
            # PSM_PERIOD_320H
            # PSM_PERIOD_DISABLED
        print('active:', p[3], end='*' )
        if p[4] == LTE.PSM_ACTIVE_2S:
            print("2s", end=' ')
        else:
            print('fixme', p[4], end=' ')
            # PSM_ACTIVE_1M
            # PSM_ACTIVE_6M
            # PSM_ACTIVE_DISABLED
    else:
        print("psm disabled", end=' ')
    print(p)

def edrx():
    at('AT+SQNEDRX?') # "0010"')

def edrx_on():
    print("turn edrx ON")
    at('AT+SQNEDRX=2,4,"0101","0000"') # 81.92s

def edrx_off():
    print("turn edrx OFF")
    at('AT+SQNEDRX=3')

def lpm():
    L = 'disablelog 1\nsetlpm airplane=1 enable=1\n'
    #print('# lpm 60:')
    try:
        l = at('AT!="cat /fs/sqn/etc/scripts/60-lpm-enable.cli"', do_return=True)
        if l == L:
            print("lpm is configured (60)")
            return True
    except Exception as e:
        print("Exception while reading lpm 60")

    # print('# lpm 61:')
    try:
        l = at('AT!="cat /fs/sqn/etc/scripts/61-lpm-enable.cli"', do_return=True)
        if l == L:
            print("lpm is configured (61)")
            return True
    except Exception as e:
        print("Exception while reading lpm 61")

    print("lpm is not configured")
    return False

def lpm_unconfigure():
    try:
        at('AT!="rm /fs/sqn/etc/scripts/60-lpm-enable.cli"')
    except Exception as e:
        print("lpm rm 60", e)
    try:
        at('AT!="rm /fs/sqn/etc/scripts/61-lpm-enable.cli"')
    except Exception as e:
        print("lpm rm 61", e)
    lpm()

def lpm_configure():
    try:
        at('AT!="echo setlpm 1 0 0 1 > /fs/sqn/etc/scripts/60-lpm-enable.cli"')
        time.sleep(.1)
        at('AT!="echo disablelog 1 >> /fs/sqn/etc/scripts/60-lpm-enable.cli"')
    except Exception as e:
        print("lpm enable 60", e)
    lpm()

def provider():
    imsi = None
    apn = None
    for retry in range(5):
        try:
            imsi = at("AT+CIMI", do_return=True)
            if imsi:
                break
        except Exception as e:
            print("imsi failed, retry ... ", e)
            # it doesn't work in CFUN=0
            if cfun() == 0:
                # maybe we shouldn't mess with it ... but it's just more convenient that way :)
                cfun(4)
            time.sleep(1)
    if not imsi:
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
    elif mcc == "204" and mnc2 == "08":
        print("08 KPN")
        apn = 'simpoint.m2m'
        print("bands: GSM 900 / GSM 1800 / UMTS 900 / UMTS 2100 / LTE 800 / LTE 1800 / LTE 2100 / LTE 2600")
    elif mcc == "234" and mnc2 == "50":
        print("50 Jersey Telecom Ltd.")
        print("bands: GSM 1800 / UMTS 2100 / LTE 800 / LTE 1800 / LTE 2600")
    elif mcc == "901" and mnc2 == "28":
        print("28 Vodafone")
        apn = "pycom.io" # this is for test cards, maybe we need iccid to distinguish
    else:
        mnc_len = None
        print(mnc2, "/", mnc3, "unknown")
    return apn

def attach(apn=None, band=None, timeout_s = attach_timeout_s, do_fsm_log=True, do_rssi_log=True):
    if not lte:
        init()
    if lte.isattached():
        print("already attached")
    else:
        lte.imei()
        version()
        lpm()
        try:
            whoami()
        except:
            pass
        lte.lte_callback(LTE.EVENT_COVERAGE_LOSS, cb_handler)
        if not apn:
            apn = provider()
        else:
            provider()
        print("attach(apn=", apn, ", band=", band, ")", sep='')
        t = time.ticks_ms()
        if apn:
            if band:
                lte.attach(apn=apn, band=band)
            else:
                lte.attach(apn=apn)
        else:
            if band:
                lte.attach(band=band)
            else:
                lte.attach()
        print("attach took", (time.ticks_ms() - t ) / 1000 )
        isattached(timeout_s, do_fsm_log=do_fsm_log, do_rssi_log=do_rssi_log)
        print("attaching took", (time.ticks_ms() - t ) / 1000 )
        at('AT+CEREG?')
        at('AT+SQNMONI=7')
        psm()
        edrx()
        ifconfig()
        d = socket.dnsserver()
        if d[0] == '0.0.0.0':
            print("setting dns server 8.8.8.8")
            socket.dnsserver(0, '8.8.8.8')
        print("DNS:", socket.dnsserver())
        # after attaching there's a longer period with higher consumption, so we measure it twice
        measure("attached")
        measure("attached2")
        measure("attached3")
        measure("attached4")

def attach_manual(apn=None, band=None, timeout_s = attach_timeout_s, do_fsm_log=True, do_rssi_log=True):
    if not lte:
        lte_debug = True
        init()
    if lte.isattached():
        print("already attached")
    else:
        if band is None:
            band=20
        t = time.ticks_ms()
        at('AT')
        at('AT+CGATT?')
        at('AT+CEREG?')
        at('AT+CFUN?')
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
        #         lte.attach(apn=apn, band=band)
        #     else:
        #         lte.attach(apn=apn)
        # else:
        #     if band:
        #         lte.attach(band=band)
        #     else:
        #         lte.attach()
        print("attach took", (time.ticks_ms() - t ) / 1000 )
        isattached(timeout_s, do_fsm_log=do_fsm_log, do_rssi_log=do_rssi_log)
        print("attaching took", (time.ticks_ms() - t ) / 1000 )
        at('AT+CEREG?')
        at('AT+SQNMONI=7')
        psm()
        edrx()
        ifconfig()
        d = socket.dnsserver()
        if d[0] == '0.0.0.0':
            print("setting dns server 8.8.8.8")
            socket.dnsserver(0, '8.8.8.8')
        print("DNS:", socket.dnsserver())
        # after attaching there's a longer period with higher consumption, so we measure it twice
        measure("attached")
        measure("attached2")
        measure("attached3")
        measure("attached4")

def isattached_manual():
    cmds=['AT+CEREG?', 'AT+CGATT?', ]
    for cmd in cmds:
        print(at(cmd, do_return=True).strip(), end=', ')
    rsrpq()
    #print()

def isattached(timeout_s = attach_timeout_s, do_fsm_log=True, do_rssi_log=True):
    if timeout_s is not None:
        timeout_ms = timeout_s * 1000
    t = time.ticks_ms()
    r = None
    f = None
    if lte.isconnected():
        print("isconnected")
    elif lte.isattached():
        print("isattached")
        rssi()
    else:
        while not lte.isattached():
            if do_fsm_log:
                f2 = grep("TOP FSM|SEARCH FSM", fsm(do_return=True), do_return=True)
                if f != f2:
                    f = f2
                    print(time.time(), '\n', f, sep='')
                #cat_fsm()
            if do_rssi_log:
                r2 = at('AT+CSQ', do_return=True).strip()
                if r != r2:
                    r = r2
                    #print(time.time(), r)
                    rssi()
            time.sleep(0.1)
            if timeout_s is not None and time.ticks_ms() - t > timeout_ms:
                raise Exception("Could not attach in {} s".format(timeout_s))
        print("isattached", lte.isattached(), "turned true after {} s".format(( time.ticks_ms()-t )  / 1000 ))
        rssi()

def sqn_ping(num=1, interval=0, do_fsm=False, quiet=False):
    init()
    if not lte.isattached():
        attach()
    # if lte.isconnected():
    #     lte.pppsuspend()
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

def connect():
    if lte.isconnected():
        print("already connected")
        return
    if not lte.isattached():
        attach()
    print("connect")
    t = time.ticks_ms()
    lte.connect()
    print("connect took", (time.ticks_ms() - t ) / 1000 )
    timeout_ms = 60000
    while not lte.isconnected():
        time.sleep(0.1)
        if time.ticks_ms() - t > timeout_ms:
            raise Exception("Could not connect in {} s".format((time.ticks_ms() - t )/ 1000 ))
    print("connecting took", (time.ticks_ms() - t ) / 1000 )
    measure("connected")

def ifconfig(verbose=False):
    for attempt in range(0,3):
        try:
            cgcontrdp = at('AT+CGCONTRDP=1', do_return=True)
            if cgcontrdp.strip() == 'ERROR':
                print('IP not set')
            else:
                if verbose:
                    print(cgcontrdp)
                    # '\r\n+CGCONTRDP: 1,5,"spe.inetd.vodafone.nbiot.mnc028.mcc901.gprs","10.175.213.177.255.255.255.255","","10.105.16.254","10.105.144.254","","",,,1430\r\n\r\nOK\r\n'
                    # lte.send_at_cmd('AT+CGDCONT?')
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

def ifconfig_suspend():
    lte.pppsuspend()
    ifconfig()
    lte.pppresume()

def dl(kb=None):
    init()
    if not lte.isattached():
        attach()
    if not lte.isconnected():
        try:
            print("resume")
            lte.pppresume()
            if not lte.isconnected():
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

def test_dl():
    init()
    if not lte.isattached():
        attach()
    if not lte.isconnected():
        try:
            print("resume")
            lte.pppresume()
            if not lte.isconnected():
                connect()
        except Exception as e:
            print("couldn't resume, try to connect (", e, ")", sep='')
            try:
                connect()
            except:
                print("failed, try second time")
                sleep(1)
                connect()
    repetitions = 3
    delays = [10, 60, 300 ] # , 600]
    for d in delays:
        for r in range(repetitions):
            success = False
            for a in range(3):
                print("\ntest_dl (delay after:", d, " repetition:", r, "attempt:", a, ")")
                pretty_time()
                try:
                    dl()
                    success=True
                    break
                except Exception as e:
                    print("Exception during download:", e)
            if not success:
                raise Exception("test_dl failed (delay after:", d, " repetition:", r, "attempt:", a, ")")
            sleep(d, verbose=True)

def long_at():
    if not lte.isattached():
        attach()
    # from network import LTE
    # lte = LTE(debug=True)
    #
    # attach()

    # set the socket option to expect the TX bytes to be provided in the form of HEX values.
    lte.send_at_cmd('AT+SQNSCFGEXT=1,1,0,0,0,1')

    lte.send_at_cmd('AT+SQNSD=1,1,5555,"80.101.10.222",0,8888,1')
    sleep(1)

    # short
    lte.send_at_cmd('AT+SQNSSENDEXT=1,10')
    lte.send_at_cmd('0102030405060708090a')
    sleep(1)

    # Request the transmission of 70 bytes (which will be 140 long HEX string)
    lte.send_at_cmd('AT+SQNSSENDEXT=1,70')
    # 140 characters -> 70 bytes. This messages could not be sent with the default implementation.
    lte.send_at_cmd('A343164303A3730313A313130303A303A303A303A32303630886368A343164303A3730313A313130303A303A303A303A32303630886368A343164303A3730313A313130303A3')
    sleep(1)

    # two chunks + remaining
    lte.send_at_cmd('AT+SQNSSENDEXT=1,140')
    lte.send_at_cmd('A343164303A3730313A313130303A303A303A303A32303630886368A343164303A3730313A313130303A303A303A303A32303630886368A343164303A3730313A313130303A3A343164303A3730313A313130303A303A303A303A32303630886368A343164303A3730313A313130303A303A303A303A32303630886368A343164303A3730313A313130303A3')
    sleep(1)

    # corner case two chunks and no remaining
    lte.send_at_cmd('AT+SQNSSENDEXT=1,124')
    lte.send_at_cmd('0102030405060708090a0102030405060708090a0102030405060708090a0102030405060708090a0102030405060708090a0102030405060708090a0102030405060708090a0102030405060708090a0102030405060708090a0102030405060708090a0102030405060708090a0102030405060708090a01020304')
    sleep(1)

    # Shutdown socket
    lte.send_at_cmd('AT+SQNSH=1')
    sleep(1)

def reset():
    print('lte.reset')
    lte.reset()
    print('machine.reset')
    sleep(1)
    machine.reset()

if __name__ == "__main__":
    attach(band=20)
    sqn_ping(10)
    connect()
    dl()
