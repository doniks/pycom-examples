import time
import os
import binascii

u = None

pins = {
    # pins = ( TXD,   RXD,   RTS,   CTS )
    'GPy'  : ( 'P5', 'P98',  'P7', 'P99'),
    'FiPy' : ('P20', 'P18', 'P19', 'P17')
}

def init(br=None):
    global u
    if not br:
        if u:
            # already initialized
            return True
        else:
            # not initialized and no br specified, so, we guess
            return init(921600) or init(115200)
    else:
        s = os.uname().sysname
        p=pins[s]
        print('init(', br, ')', s, p)
        u = UART(1, baudrate=br, pins=p, timeout_chars=10)
        try:
            at()
            print('init(', br, ') succeeded')
            return True
        except Exception as e:
            print('init(', br, ') failed', e)
            try:
                at()
                print('init(', br, ') succeeded')
                return True
            except:
                print('init(', br, ') failed', e)
                return False

def help(verbose=False):
    init()
    r = at('AT+CLAC', do_return=True)
    if verbose:
        for cmd in r:
            at(cmd + '=?')
    else:
        for cmd in r:
            print(cmd, end=' ')

def at(cmd='', pretty=True, verbose=False, do_return=False):
    init()
    if do_return:
        retval = []
    else:
        retval = False
    if not cmd:
        cmd='AT'
        verbose = True
    if verbose:
        print('[', cmd, ']', sep='', end=':')

    u.write((cmd + '\r\n').encode())
    time.sleep_ms(1000)
    r = u.read()
    # print("[", len(r), "]<", binascii.hexlify(r), ">", sep='', end='')
    try:
        for line in r.decode().split('\r\n'):
            if len(line) == 0:
                continue
            else:
                if do_return:
                    retval += [line]
                    if verbose:
                        print(line)
                else:
                    if line == 'OK':
                        retval = True
                        if verbose:
                            print(line)
                    elif line == 'ERROR':
                        retval = False
                        if verbose:
                            print(line)
                    else:
                        print(line)
        return retval
    except:
        print("[", len(r), "]<", binascii.hexlify(r), ">", sep='', end='')
        print()

def smod():
    init()
    r = at('AT+SMOD?', do_return=True)
    print(r, end=' ')
    m = int(r[0])
    if m == 0:
        print('FFH (bootloader)')
    elif m == 1:
        print('mTools')
    elif m == 2:
        print('FFF (application)')
    elif m == 3:
        print('dunno')
    elif m == 4:
        print('upgrade???')
    else:
        print('?')



if __name__ == '__main__':
    # init(921600) or init(115200)
    init()
    at('AT', verbose=True)
    smod()
    if False:
        # which mode are we in right now
        at('AT+SMOD?') # 2
        at('AT+BMOD?') # FFF
        # which mode is configured for next boot
        at('AT+SMSWBOOT?')
        # change mode for next boot
        at('AT+SMSWBOOT=?', verbose=True)
        # +SMSWBOOT: mode[,reboot]
        #   mode: 0=FFH, 1=FFF, 2=UPDATER, 3=RECOVERY
        #   reboot: 0=Do not reboot, 1=reboot
        at('AT+SMSWBOOT=0', verbose=True) # FFH
        at('AT+SMSWBOOT=1', verbose=True) # FFF
        at('AT+SMSWBOOT=2', verbose=True) # UPDATER
        at('AT+SMSWBOOT=3', verbose=True) # RECOVERY
        at('AT^RESET', verbose=True)
        at()
        help(True)
        help(verbose=True)
    at("ATI1")
    # UE:5.0.0.0d;att:5.1.0.0d
    # LR5.1.1.0-39529
