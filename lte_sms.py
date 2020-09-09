from network import LTE
import time
import socket
import machine
import pycom

def at(cmd):
    response = lte.send_at_cmd(cmd).split('\r\n')
    for line in response:
        if ( len(line) == 0 ):
            continue
        else:
            print(line)

def atv(cmd):
    response = lte.send_at_cmd(cmd).split('\r\n')
    for line in response:
        if ( len(line) == 0 ):
            continue
        elif line == "OK":
            continue
        elif line == "ERROR":
            continue
        else:
            print(line)
            return line


def sleep(timeout):
    while timeout:
        print(timeout, end=" ")
        time.sleep(1)
        timeout -= 1
    print("X")


def attach():
    if lte.isattached():
        print("already attached")
    else:
        print("attach")
        start = time.time()
        lte.attach(band=20, apn="spe.inetd.vodafone.nbiot")
        print("attach() finished after", time.time() - start, "seconds")

        # lte.init(debug=False)
        while not lte.isattached():
            # AT        OK
            # AT+CGATT? :0
            # AT+CEREG? :2,2
            # AT+CFUN?  :1
            # ....
            # AT
            # +CEREG: 5,"2E1D","01905667",9
            # +CREG:  5,"2E1D","01905667",9
            # AT+CGATT?
            # +CGATT: 1
            print('.', end='')
            time.sleep(1)
        print()

        # lte.init(debug=True)
        print("isattached() after", time.time() - start, "seconds")

    p = lte.psm()
    pretty_print_psm(p)

def connect():
    print("connect")
    start = time.time()
    lte.connect()
    print("connect() finished after", time.time() - start, "seconds")
    while not lte.isconnected():
        print('.', end='')
        time.sleep(0.5)
    print()
    print("isconnected() after", time.time() - start, "seconds")



############################################
pycom.heartbeat(False)
pycom.rgbled(0x000003)
sleep(1)

from network import LTE
print("new")
lte = LTE(debug=True)

# at('AT+CEDRX?')
# [AT] AT+CEDRX?
# [AT-OK]
# ERROR
# at('AT+SQNEDRX=?')
# +SQNEDRX: (0-3),(5),("0000"-"1111"),("0000"-"1111")
at('AT+SQNEDRX?')
# [AT] AT+SQNEDRX?
# [AT-OK]
# +SQNEDRX: 0,5,"1111","0000"
# <mode>[,<Requested_eDRX_value>,<Requested_ptw_value>]

attach()


# at('AT+COPS=?')
at('AT+CPIN?')
at('AT+CREG?') # registered? 2,5,"2E1D","01905667",9
at('AT+COPS?') # network 0,2,"20404",9
at('AT+CSQ')

at('AT+CGEREP=2,0')

at('AT+CMGF=1')
at('AT+CMGF?')
at('AT+CMGS="+<<<PHONENR>>>"\rHullo'+chr(26))
r = lte.send_at_cmd('AT+CMGS="+<<<PHONENR>>>",145\rHullo'+chr(26))
print(r)
r = lte.send_at_cmd('AT+CMGS="<<<PHONENR>>>"\rHullo'+chr(26))
print(r)
r = lte.send_at_cmd('AT+CMGS="<<<PHONENR>>>",129\rHullo'+chr(26))
print(r)

at('AT+CNMI?') # how newly arrived SMS messages should be handled
# connect()
lte.send_at_cmd('AT+CGPADDR')
'\r\n+CGPADDR: 1,"10.175.211.94"\r\n\r\nOK\r\n'
>>> lte.send_at_cmd('AT+CGCONTRDP=1')
'\r\n+CGCONTRDP: 1,5,"spe.inetd.vodafone.nbiot.mnc028.mcc901.gprs","10.175.211.94.255.255.255.255","","10.105.16.254","10.105.144.254","",""\r\n\r\nOK\r\n'
