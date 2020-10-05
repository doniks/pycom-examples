lte.version(True)
# gpy-d1ac
# this is a 6 band module
# Sequans FW LR5.4.1.0-50523 CAT-M1

# Test command reports the list of supported <rat> and <operator> as well as list of 4G LTE bands supported by the device (Hardware capabilities).
lte.at('AT+SQNBANDSEL=?')
# AT+SQNBANDSEL=? +SQNBANDSEL:(list of supported <rat>s),(list of supported <operator>s),(list of hardware supported bands)
# +SQNBANDSEL:
# (0,1),
# ("3gpp-conformance","ais","aptg","att","bell","cht","cta","dialog","dish","docomo","dtag","etisalat","kddi","kpn","kt","lgu","mci","mtn","orange","pod","ptcrb","singtel","skt","softbank","soracom","spark","sprint","standard","swisscom","telenor","telstra","telus","tim","tmo","truphone","turkcell","verizon","vodafone"),
# (1,2,3,4,5,8,12,13,14,17,18,19,20,25,26,28,66)

# Read command reports the list of authorized band configuration per <rat> and <operator>.
lte.at('AT+SQNBANDSEL?')
# +SQNBANDSEL: 0,3gpp-conformance,"1,2,3,4,5,8,12,13,14,17,18,19,20,25,26,28,66"
# +SQNBANDSEL: 0,ais,"1,3,8"
# +SQNBANDSEL: 0,aptg,"1,8"
# +SQNBANDSEL: 0,att,"2,4,12"
# +SQNBANDSEL: 0,bell,"4"
# +SQNBANDSEL: 0,cht,"8"
# +SQNBANDSEL: 0,cta,"5,8"
# +SQNBANDSEL: 0,dialog,"3,8"
# +SQNBANDSEL: 0,dish,"111,222"
# +SQNBANDSEL: 0,docomo,"1,19"
# +SQNBANDSEL: 0,dtag,"3,8,20"
# +SQNBANDSEL: 0,etisalat,"20"
# +SQNBANDSEL: 0,kddi,"18,26"
# +SQNBANDSEL: 0,kpn,"3,20"
# +SQNBANDSEL: 0,kt,"3"
# +SQNBANDSEL: 0,lgu,"5"
# +SQNBANDSEL: 0,mci,"8,3"
# +SQNBANDSEL: 0,mtn,"8,3"
# +SQNBANDSEL: 0,orange,"20,3"
# +SQNBANDSEL: 0,pod,"2,4,12,13,20,3"
# +SQNBANDSEL: 0,ptcrb,"1,2,3,4,5,8,12,13,14,17,18,19,20,25,26,28,66"
# +SQNBANDSEL: 0,singtel,"3,8"
# +SQNBANDSEL: 0,skt,"3,5,26"
# +SQNBANDSEL: 0,softbank,"1,8"
# +SQNBANDSEL: 0,soracom,"2,4,12"
# +SQNBANDSEL: 0,spark,"1,3,28"
# +SQNBANDSEL: 0,sprint,"2,4,5,12,25"
# +SQNBANDSEL: 0,standard,"1,2,3,4,5,8,12,13,14,17,18,19,20,25,26,28,66"
# +SQNBANDSEL: 0,swisscom,"20,3"
# +SQNBANDSEL: 0,telenor,"1,3,8,20"
# +SQNBANDSEL: 0,telstra,"3,28"
# +SQNBANDSEL: 0,telus,"12,4,5"
# +SQNBANDSEL: 0,tim,"3,20"
# +SQNBANDSEL: 0,tmo,"2,4,5,12,66"
# +SQNBANDSEL: 0,truphone,"1,2,4,8,12,20"
# +SQNBANDSEL: 0,turkcell,"20,1,3,8"
# +SQNBANDSEL: 0,verizon,"13,4"
# +SQNBANDSEL: 0,vodafone,"20,8"

# -> cbe "showCaps"
# No permission to use the RRC private debug CLI
# value = -1 = 0xffffffff

# AT+SQNBANDSEL=<rat>,<operator>,<bandList> OK
#
# Write command enables the user to specify list of 4G LTE bands the modem is allowed to use for different Radio Access Technologies (RATs) for all cell search operations (initial scanning, cell drop scanning, cell reselection, handover, etc.) for identified <rat> and <operator>. New configuration can will be saved in non-volatile memory and is applied at next device registration to network. For a given pair of <rat> and <operator>, the list of enabled bands is given by the <bandList> parameter containing comma-separated list of LTE band numbers as defined by 3GPP standard TS 36.101 (4G). Any LTE band not part of <bandList> is considered as deactivated.
lte.at('AT+SQNBANDSEL=0,"tim","1,2,3"') # set new value
lte.at('AT+SQNBANDSEL=0,"tim","3,20"') # reset to original value
grep("tim", lte.at('AT+SQNBANDSEL?', do_return=True)) # get current value
# after a factory reset, the bands are back to original values, but BANDSEL seems to have duplicated the whole list
# setting value again, changes both values
# second factory reset brings it back to single entries ...

lte.at('AT+SQNBANDSEL=0,"standard","3,4,12,13,20,28"') # reduce to 6 bands
lte.at('AT+SQNBANDSEL=0,"standard","1,2,3,4,5,8,12,13,14,17,18,19,20,25,26,28,66"') # return to default
grep("standard", lte.at('AT+SQNBANDSEL?', do_return=True))

at('AT!="clearscanconfig"')
at('AT!="RRC::addScanBand band=' + str(3) + '"')
at('AT!="RRC::addScanBand band=' + str(18) + '"') # ERROR if not auth via BANDSEL

print(lte.l.send_at_cmd('AT+SQNINS=0',timeout=0))

lte.at('AT+CFUN?')
lte.at('AT+CGATT?')
lte.at('AT+CEREG?')

lte.at('AT+CFUN=0') # off
lte.at('AT+CFUN=1') # on
lte.at('AT+CFUN=4') # sim
lte.at('AT+CGATT=0') # detach
lte.at('AT+CGATT=1') # attach
lte.cgatt(1)




#######################################
# upgraded module gpy-b678
# 17 bands calibrated
[AT] 51519 AT!="showver"
[AT-OK] +47
SYSTEM VERSION
==============
  FIRMWARE VERSION
    Bootloader0  : 6.0.0.0 [44556]
    Bootloader1* : 5.4.1.0 [50523]
    Bootloader2  : 6.1.2.0 [46262]
    NV Info      : 1.1,0,0
    Software     : 5.4.1.0 [50523] by robot-soft at 2020-08-31 09:28:03
    UE           : 5.4.0.2
    Ecopaging    : 5.4.1.0 [50523] by robot-soft at 2020-08-31 09:28:03
    pxl          : 5.4.1.0-50523
  COMPONENTS
    ZSP0         : 1.0.0-16046
    ZSP1         : 1.0.99-15984

OK

SYSTEM VERSION
==============
  FIRMWARE VERSION
    Bootloader0  : 6.0.0.0 [44556]
    Bootloader1* : 5.4.1.0 [50523]
    Bootloader2  : 6.1.2.0 [46262]
    NV Info      : 1.1,0,0
    Software     : 5.4.1.0 [50523] by robot-soft at 2020-08-31 09:28:03
    UE           : 5.4.0.2
    Ecopaging    : 5.4.1.0 [50523] by robot-soft at 2020-08-31 09:28:03
    pxl          : 5.4.1.0-50523
  COMPONENTS
    ZSP0         : 1.0.0-16046
    ZSP1         : 1.0.99-15984
[AT] 51657 AT!="get_sw_version"
[AT-OK] +41
[BOOTROM0] 6.0.0.0 [44556]
[BOOTROM1*] 5.4.1.0 [50523]
[BOOTROM2] 6.1.2.0 [46262]
[FFF] 5.4.1.0 [50523] by robot-soft at 2020-08-31 09:28:03
[ECOPAGING] 5.4.1.0 [50523] by robot-soft at 2020-08-31 09:28:03
[UPDATER] 5.4.1.0 [50523] by robot-soft at 2020-08-31 09:28:03
[NVRAM] 1.1,0,0

OK

[BOOTROM0] 6.0.0.0 [44556]
[BOOTROM1*] 5.4.1.0 [50523]
[BOOTROM2] 6.1.2.0 [46262]
[FFF] 5.4.1.0 [50523] by robot-soft at 2020-08-31 09:28:03
[ECOPAGING] 5.4.1.0 [50523] by robot-soft at 2020-08-31 09:28:03
[UPDATER] 5.4.1.0 [50523] by robot-soft at 2020-08-31 09:28:03
[NVRAM] 1.1,0,0
>
Pycom MicroPython 1.20.2.rc9 [v1.11-c245dc2] on 2020-06-17; GPy with ESP32
Type "help()" for more information.
>>>
>>>


# empty!
[AT] 138009 AT+SQNBANDSEL?
[AT-OK] +32
OK

$ sfu upgrade -z 2 -b 921600 /dev/ttyUSB3 ../FIPY_BOOTROM_UART2-41802.dup
-> crash loop
