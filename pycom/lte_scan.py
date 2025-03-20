

lte.at('AT+SQNMONI=?')
# +SQNMONI: (0,1,2,7,9)


lte.attach()

# 0 Report information for the serving cell only
lte.at('AT+SQNMONI=0')
# +SQNMONI: Amarisoft Network Cc:001 Nc:01 RSRP:-86.80 RSRQ:-6.00 TAC:2 Id:1 EARFCN:5104 PWR:-73.02 PAGING:128

# 9 Report information for the serving cell only with RSRP/CINR measurements
lte.at('AT+SQNMONI=9')
# +SQNMONI: Amarisoft Network Cc:001 Nc:01 RSRP:-85.90 CINR:26.60 RSRQ:-5.90 TAC:2 Id:1 EARFCN:5104 PWR:-72.22 PAGING:128

# run AT+CGATT=0 in uart1
lte.at_log('AT+SQNMONI=9')
# run AT+CGATT=1 in uart1
# now SQNMONI will print measurements for a little bit, I think while attaching and briefly after

# 8 Report information for the serving cell only with RSRP/CINR measurements per antenna.
# Applicable to Calliope-based and Cassiopeia-based products only.
# lte.at('AT+SQNMONI=8')
# ERROR

# 7 Report information for all cells
lte.at('AT+SQNMONI=7')
lte.at_log('AT+SQNMONI=7')
# same as at_log('AT+SQNMONI=9')
# netmame           country Operator                              cell
# Amarisoft Network Cc:001  Nc:01    RSRP:-90.70 RSRQ:-4.50 TAC:1 Id:1 EARFCN:6300 PWR:-78.42 PAGING:128


# 1 Report information for the intra-frequency cells only
lte.at('AT+SQNMONI=1', quiet=False)

# 2 Report information for the inter-frequency cells only
lte.at('AT+SQNMONI=2', quiet=False)


lte.at('AT+SQNINS=?')
# 0 full informal network scanning.
# This scanning enable a full reporting of information extracted from MIB (Master information Block) and SIB1 (System Information Block 1).
#
# 1 fast informal network scanning.
# This scanning enable a reporting of information extracted from MIB (Master information Block) only.

lte.at('AT+SQNINS=0')

# if attached:
# +SQNINS: 0,4,9,,,,,,,,
# +SQNINS: 0,13,9,,,,,,,,
# or
# +SQNINS: 0,4,7,,,,,,,,
# +SQNINS: 0,13,7,,,,,,,,


lte.detach()

# if detached, crashes

lte.at_log('AT+SQNINS=0')

lte.at('AT+SQNINS=1', quiet=False)
# if detached, crashes

# catm 5.4 times out, but via uart1:
# when not attached, ie either cfun=0, or cfun=1 and cgatt=0
+SQNINS: 1,1,7,"0","0000","000000",75,298,1.4,-98.90,-8.10
+SQNINS: 1,4,7,"0","0000","000000",2025,298,1.4,-98.30,-8.90
+SQNINS: 1,8,7,"415A15","001A","20416",3700,131,10,-96.10,-10.30
+SQNINS: 1,3,7,"0","0000","000000",1500,328,1.4,-95.90,-8.20
+SQNINS: 1,3,7,"0","0000","000000",1300,176,1.4,-101.00,-8.80
+SQNINS: 1,3,7,"0","0000","000000",1800,131,1.4,-115.70,-12.20








5.4:
CFUN=0
AT+SQNMONI=0-7 all return ERROR
CFUN=1 (automatically attaches)
+CEREG: 1,"0001","01A2D001",7
AT+SQNMONI=0 7 or 9 all report one line:
+SQNMONI: Amarisoft Network Cc:001 Nc:01 RSRP:-92.70 CINR:-1.10 RSRQ:-12.40 TAC:1 Id:1 E8
1 and 2 return just OK
CGATT=0
AT+SQNMONI same

AT+SQNINS=0 (37s )
AT+SQNINS=1 (33s, 37s) # same result basically

+SQNINS: a, b,r, cell_Id,   tac,    plmn,earf,pci, bwD,   rsrp,  rsrq
+SQNINS: 0, 1,7,     "0","0000","000000",  75,298, 1.4, -98.30, -6.70
+SQNINS: 0, 3,7,     "0","0000","000000",1500,328, 1.4,-104.30, -8.10
+SQNINS: 0, 3,7,     "0","0000","000000",1800,131, 1.4,-116.60,-14.90
+SQNINS: 0, 3,7,     "0","0000","000000",1300,176, 1.4,-105.40,-10.60
+SQNINS: 0, 4,7,     "0","0000","000000",2025,298, 1.4, -98.30, -8.10
+SQNINS: 0, 8,7,"415A15","001A", "20416",3700,131,10  , -98.30,-11.40
+SQNINS: 0, 8,7,"415A17","001A", "20416",3700,130,10  ,-101.70,-12.50
+SQNINS: 0, 8,7,     "0","0000","000000",3700,130, 1.4,-106.10,-19.40


lte.at('AT+SQNMONI=7')
netmame           country Operator                              cell
Amarisoft Network Cc:001  Nc:01    RSRP:-90.70 RSRQ:-4.50 TAC:1 Id:1 EARFCN:6300 PWR:-78.42 PAGING:128

+CEREG: <stat>,   tac,   cell id,AcT
+CEREG:      1,"0001","01A2D001",7

+COPS:<mode>[,<format>,<oper>[,<AcT>]]
+COPS: 0,2,"00101",7

OPS=

+COPS:
status, long,          short      ,operator,AcT
(2,"Amarisoft Network","Amarisoft","00101",7) # 2 .. current
(1,"NL KPN",           "NL KPN",   "20408",7) # 1 .. available
,,
(0,1,2,3,4), modes
(0,1,2)      formats


copn_db = None
def copn_init():
    global copn_db
    copn_db = {}
    copn_raw = lte.at('AT+COPN', do_return=True)
    for line in copn_raw.split('\n'):
        data = line.split('+COPN: ')
        # print(data)
        if len(data) > 1:
            # print(data[1])
            # print(data[1][0])
            id, name = data[1].split(',')
            id = id.strip('"')
            name = name.strip('"')
            copn_db[id] = name
    print('copn database initialized with', len(copn_db), 'entries')

def copn(operator = None):
    if copn_db is None:
        copn_init()
    try:
        print(operator, ':', copn_db[operator])
    except:
        print(operator, 'unknown')
copn()
copn('00101') # Amarisoft
copn('20408') # KPN
copn('20416') # vodafone I think


def sqnins(action=1, do_return=False, do_print=True):
    t = time.ticks_ms()
    r = lte.l.send_at_cmd('AT+SQNINS=' + str(action), timeout=0 ) # 120000)
    print('Scan took', (time.ticks_ms() - t)/1000)
    print(r)
    scan = [['scan', 'band', 'AcT', 'cell',   'tac',    'plmn','earfcn','pci', 'BWd',   'rsrp',  'rsrq']]
    for line in r.split('\r\n'):
        if len(line) > 3:
            scan += [line.split('SQNINS: ')[1].split(',')]
    print('Scan took', (time.ticks_ms() - t)/1000, 'found', len(scan)-1, 'entries')
    scan.sort()
    if do_print:
        for cell in scan:
            print(cell)
    if do_return:
        return scan
# sqnins(1)
def lte_scan(band):
    orig = grep("standard", lte.at('AT+SQNBANDSEL?', do_return=True), do_return=True)
    print(orig)
    orig = orig.split('+SQNBANDSEL: ')[1].strip()
    print(orig)
    lte.at('AT+SQNBANDSEL=0,"standard","' + str(band) + '"') # reduce to 6 bands
    last = None
    while True:
        scan = sqnins(do_return=True, do_print=False);
        #          band cell tac plmn earfcn pci
        cells = [ [s[1],s[3],s[4],s[5],s[6],s[7]] for s in scan ]
        cells.sort()
        if cells != last:
            for c in cells:
                print(c)
            last = cells
        time.sleep(1)
lte_scan(20)

On CAT-M1 with the 5.4 firmware, I can perform a SQNINS with out a crash. So that's good.


Both SQNINS=0 and =1 take approximately 35-40 seconds and always finds 6-8 cells. It is more or less the same set it finds. It's peculiar that it only finds cells in bands 1, 3, 4 and 8. Never any other band, even after letting it repeatedly scan for more than 1 hour. The scan never finds the Amarisoft at band 20 even though attaching to it works reliably and quickly. Only the one or two cells in band 8 are ever identified with their cell id, tac and plmn. The others are always 0. Seems the identified one is Vodafone 20416. But, e.g., KPN 20408 never shows up.

Looking at the PLMN id, only
