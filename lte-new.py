import time
import machine
from network import LTE
# from sleep import sleep
from http_get import http_get
import sys
import binascii
import sqnsupgrade
from sdcard import sd
import pycom

try:
    from ntp import *
except:
    pass

print(os.uname().sysname.lower() + '-' + binascii.hexlify(machine.unique_id()).decode("utf-8")[-4:], "main.py")

use_edrx = False
use_psm = False
lte_debug = False

settle_s = 0 # 4
measure_s = 0 # 10

try:
    lte
except:
    lte = None

def sleep(s):
    if not s:
        return
    print("sleep", s)
    while s > 0:
        time.sleep(1)
        s -= 1
    print("sleep done")

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

def at(cmd='', quiet=True, do_return=False):
    if cmd == '':
        cmd='AT'
        quiet=False
    response = lte.send_at_cmd(cmd).split('\r\n')
    retval = ""
    for line in response:
        if ( len(line) == 0 ):
            continue
        elif quiet and line == 'OK':
            continue
        else:
            if do_return:
                retval += line + '\n'
            else:
                print(line)
    if do_return:
        return retval

def version(debug=False):
    if debug:
        at('AT!="showver"')
        at('AT!="get_sw_version"')
    else:
        # at('AT+CGMR')
        # UE5.2.0.3
        at('ATI1', quiet=True)

def fsm():
    at('AT!="fsm"')

def showphy():
    at('AT!="showphy"')

def imsi():
    at('AT+CIMI')

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
    #print('# lpm 60:')
    at('AT!="cat /fs/sqn/etc/scripts/60-lpm-enable.cli"')

    # print('# lpm 61:')
    at('AT!="cat /fs/sqn/etc/scripts/61-lpm-enable.cli"')

def provider():
    imsi = None
    for retry in range(10):
        try:
            imsi = at("AT+CIMI", do_return=True)
            if imsi:
                break
        except:
            print("imsi failed, retry ... ")
            time.sleep(1)
    if not imsi:
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
        print("bands: GSM 900 / GSM 1800 / UMTS 900 / UMTS 2100 / LTE 800 / LTE 1800 / LTE 2100 / LTE 2600")
    elif mcc == "234" and mnc2 == "50":
        print("50 Jersey Telecom Ltd.")
        print("bands: GSM 1800 / UMTS 2100 / LTE 800 / LTE 1800 / LTE 2600")
    elif mcc == "901" and mnc2 == "28":
        print("28 Vodafone")
    else:
        mnc_len = None
        print(mnc2, "/", mnc3, "unknown")

def attach(apn=None, timeout_s = 60, verbose=False):
    if lte.isattached():
        print("already attached")
    else:
        version()
        provider()
        lpm()
        lte.lte_callback(LTE.EVENT_COVERAGE_LOSS, cb_handler)
        if not apn:
            # print("guess apn")
            apn = guess_apn()
        print("attach(apn=", apn, ")", sep='')
        t = time.ticks_ms()
        if apn:
            lte.attach(apn=apn)
        else:
            lte.attach()
        print("attach took", (time.ticks_ms() - t ) / 1000 )
        isattached(timeout_s, verbose)
        print("attaching took", (time.ticks_ms() - t ) / 1000 )
        psm()
        edrx()
        ifconfig()
        # after attaching there's a longer period with higher consumption, so we measure it twice
        measure("attached")
        measure("attached2")
        measure("attached3")
        measure("attached4")

def isattached(timeout_s = 60, verbose=False):
    if timeout_s is not None:
        timeout_ms = timeout_s * 1000
    t = time.ticks_ms()
    while not lte.isattached():
        if verbose:
            fsm()
        time.sleep(0.5)
        if timeout_s is not None and time.ticks_ms() - t > timeout_ms:
            raise Exception("Could not attach in {} s".format(timeout_s))
    print("isattached", lte.isattached(), "after {} s".format(( time.ticks_ms()-t )  / 1000 ))

def ping(num=1, do_fsm=False, quiet=False):
    init()
    if not lte.isattached():
        attach()
    if lte.isconnected():
        lte.pppsuspend()
    ct = 0
    succ = 0
    fail = 0
    while ct < num:
        resp = at('AT!="IP::ping 8.8.8.8"', do_return=True)
        ct += 1
        if not quiet:
            print(resp)
        if do_fsm:
            fsm()
        if "from" in resp:
            succ += 1
        else:
            fail += 1
    print("pings:", num, " failed:", fail, " succeeded:", succ, " -- ", round(succ/num*100.0,1), "%", sep="")

def connect():
    if not lte.isattached():
        attach()
    if lte.isconnected():
        print("already connected")
        return
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

def _dl():
    print("download")
    t = time.ticks_ms()
    r = http_get()
    print(r)
    print("http_get took", (time.ticks_ms() - t)/1000)
    if not r[0]:
        raise Exception("http_get returned false")

def dl():
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
    _dl()

def test_dl():
    connect()
    repetitions = 3
    delays = [10, 60, 300, 600]
    for d in delays:
        for r in range(repetitions):
            print("\ntest_dl", d, r)
            pretty_time()
            _dl()
            sleep(d)

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

try:
    # sqnsupgrade.info(True)
    msg("start")
    raise Exception("stop")
    measure("booted")

    msg("instantiate")
    lte = init()
    # lte = LTE() # debug=True)
    measure("instantiated")

    attach()

    connect()

    if False:
        ntp_sync()
        test_dl()
        raise Exception("stop")
    elif False:
        msg("download", "start")
        _dl()
        msg("download", "end")
        measure("downloaded")
    else:
        msg("ping", "start")
        ping()
        msg("ping", "end")
        measure("pinged")
        measure("pinged2")
        measure("pinged3")
        measure("pinged4")


    if use_psm:
        msg("deinit detach=False")
        lte.deinit(detach=False)
    else:
        msg("deinit")
        lte.deinit()
    measure("deinited")
    measure("deinited2")

    ds = 10 # 10s - you probably want more if you want to replug the current shunts
    msg("deepsleep", ds)
    machine.deepsleep(ds * 1000)
except Exception as e:
    # sleep(1)
    # try:
    #     msg("deinit")
    #     lte.deinit()
    #     msg("deinit done")
    # except:
    #     msg("deinit failed")
    # # print("reset")
    # # machine.reset()
    msg("Exception", e)

if False:

    lte.init(psm_period_value=1, psm_period_unit=LTE.PSM_PERIOD_1H,
          psm_active_value=5, psm_active_unit=LTE.PSM_ACTIVE_2S)

    at('AT+CFUN?') # is it on?
    # 0 minimum functionality
    # 1 full functionality
    # 2 disable phone transmit RF circuits only
    # 3 disable phone receive RF circuits only
    # 4 disable phone both transmit and receive RF circuits

    at('AT+CFUN=1') # turn it on
    at('AT+CFUN=4') # turn it off
    at('AT+CFUN=0') # turn it completely off

    at('AT+CEREG=5')
    at('AT+CEREG?')
    # +CEREG: 2,1,"0001","01A2D001",7  -> attached
    # CREG: <n>,<stat>[,[<lac>],[<ci>],[<AcT>][,<cause_type>,<reject_cause>]]
    # CREG result codes ... I think CEREG is same ..
    # 0 not registered, MT is not currently searching a new operator to register to
    # 1 registered, home network
    # 2 not registered, but MT is currently searching a new operator to register to
    # 3 registration denied
    # 4 unknown (e.g. out of GERAN/UTRAN/E-UTRAN coverage)
    # 5 registered, roaming
    # 6 registered for "SMS only", home network (applicable only when indicates E-UTRAN)
    # 7 registered for "SMS only", roaming (applicable only when indicates E-UTRAN)
    # 8 attached for emergency bearer services only (see NOTE 2) (not applicable)
    # 9 registered for "CSFB not preferred", home network (applicable only when indicates E-UTRAN)
    # 10 registered for "CSFB not preferred", roaming (applicable only when indicates E-UTRAN)

    at('AT+CGATT?') # is it attached? -> 0 = no, 1 = yes
    print(lte.isattached())

    at('AT+CGATT=1') # attach

    at('AT+CGATT=0') # detach

    print("edrx get")
    at('AT+SQNEDRX?')
    # 0,4,"1101","0000" ->
    # 2,4,"0101","0000"
    at('AT+CEDRXS?') # setting
    # mode,ActType,ReqVal
    # Act,ReqVal
    # mode: 0 disable, 1 enable, 2 en+unsolicitedResC, 3 disable+discard
    # ActType: 4 = E-UTRAN (WB-S1 mode)
    # ReqVal:
    # 1101 2621,44s
    # +CEDRXS: 4,"1101"
    at('AT+CEDRXRDP?') # read dynamic parameters
    # AcT-type>[,<Requested_eDRX_value>[,<NW-provided_eDRX_value>[,<Paging_time_window>
    # ERROR
    at('AT+CEDRXP?')
    # ERROR
    print("edrx set OFF")
    at('AT+SQNEDRX=3')
    print("edrx set ON")
    # at('AT+SQNEDRX=2,,"1111"') # "0010"')
    # ERROR
    at('AT+SQNEDRX=2,4,"0101","0000"') # "0010"')



    import time
    print("start");time.sleep(10);print("stop")

    sqnsupgrade.uart(True, 'upcm41065.elf')
    sd()
    ls('/flash')
    try:
        rm('/flash/upgdiff_41019-to-41065.dup')
    except:
        pass
    cd('/sd/CATM1-41065')
    ls()
    cp('upgdiff_41019-to-41065.dup', '/flash')
