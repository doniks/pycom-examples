# µPing (MicroPing) for MicroPython
# copyright (c) 2018 Shawwwn <shawwwn1@gmail.com>
# License: MIT

# Internet Checksum Algorithm
# Author: Olav Morken
# https://github.com/olavmrk/python-ping/blob/master/ping.py
# @data: bytes
def _checksum(data):
    if len(data) & 0x1: # Odd number of bytes
        data += b'\0'
    cs = 0
    for pos in range(0, len(data), 2):
        b1 = data[pos]
        b2 = data[pos + 1]
        cs += (b1 << 8) + b2
    while cs >= 0x10000:
        cs = (cs & 0xffff) + (cs >> 16)
    cs = ~cs & 0xffff
    return cs

def ping(host, count=4, timeout=5000, interval=1000, quiet=False, size=64):
    raise Exception('Unsupported! Leaks memory!')
    # print('ping')
    import utime
    import uselect
    import uctypes
    import usocket
    import ustruct
    import machine

    # round up fractional values
    interval=max(1,int(interval))

    # avoid count==0
    count = max(count, 1)

    # prepare packet
    assert size >= 16, "pkt size too small"
    pkt = b'Q'*size
    pkt_desc = {
        "type": uctypes.UINT8 | 0,
        "code": uctypes.UINT8 | 1,
        "checksum": uctypes.UINT16 | 2,
        "id": uctypes.UINT16 | 4,
        "seq": uctypes.INT16 | 6,
        "timestamp": uctypes.UINT64 | 8,
    } # packet header descriptor
    h = uctypes.struct(uctypes.addressof(pkt), pkt_desc, uctypes.BIG_ENDIAN)
    h.type = 8 # ICMP_ECHO_REQUEST
    h.code = 0
    h.checksum = 0
    h.id = machine.rng()
    h.seq = 1

    # init socket
    sock = usocket.socket(usocket.AF_INET, 3, 1) # usocket.SOCK_RAW, 1)
    sock.setblocking(0)
    sock.settimeout(timeout/1000)
    addr = usocket.getaddrinfo(host, 1)[0][-1][0] # ip address
    sock.connect((addr, 1))
    not quiet and print("PING %s (%s): %u data bytes" % (host, addr, len(pkt)))

    seqs = list(range(1, count+1)) # [1,2,...,count]
    c = 1
    t = 0
    n_trans = 0
    n_recv = 0
    time_s = 0
    finish = False
    # print('ping2')
    while t < timeout:
        if t==interval and c<=count:
            # send packet
            h.checksum = 0
            h.seq = c
            h.timestamp = utime.ticks_us()
            h.checksum = _checksum(pkt)
            if sock.send(pkt) == size:
                n_trans += 1
                t = 0 # reset timeout
            else:
                seqs.remove(c)
            c += 1

        # recv packet
        while 1:
            socks, _, _ = uselect.select([sock], [], [], 0)
            if socks:
                resp = socks[0].recv(4096)
                resp_mv = memoryview(resp)
                h2 = uctypes.struct(uctypes.addressof(resp_mv[20:]), pkt_desc, uctypes.BIG_ENDIAN)
                # TODO: validate checksum (optional)
                seq = h2.seq
                if h2.type==0 and h2.id==h.id and (seq in seqs): # 0: ICMP_ECHO_REPLY
                    t_elasped = (utime.ticks_us()-h2.timestamp) / 1000
                    ttl = ustruct.unpack('!B', resp_mv[8:9])[0] # time-to-live
                    n_recv += 1
                    not quiet and print("%u bytes from %s: icmp_seq=%u, ttl=%u, time=%.2f ms" % (len(resp), addr, seq, ttl, t_elasped))
                    time_s += t_elasped
                    seqs.remove(seq)
                    if len(seqs) == 0:
                        finish = True
                        break
            else:
                break

        if finish:
            break

        #utime.sleep_ms(1)
        t += 1

    sock.close()
    loss = 0
    try:
        loss = (n_trans - n_recv) / n_trans * 100
    except:
        pass
    avg_ms = 0;
    try:
        avg_ms = time_s / n_recv
    except:
        pass
    ret = (n_trans, n_recv, loss, avg_ms)
    not quiet and print("%u packets transmitted, %u packets received, %.2f%% packet loss, %.2f ms avg" % ret)
    return ret

def pings(host, repetitions=None, count=10, quiet=True):
    print('pings', host, 'repetitions:', repetitions, 'count:', count)
    ct = 0
    while True:
        s = ping(host, count=count, quiet=quiet)
        #print('ct:', ct, ' time:', time.time(), ' sent:', s[0], ' recv:', s[1], ' loss:', s[2], '% avg:', s[3], ' ms', sep='')
        print('ct:%u time:%u sent:%u recv:%u loss:%.2f%% avg:%.2f ms' % (ct, time.time(), s[0], s[1], s[2], s[3]) )
        time.sleep(1)
        ct += 1
        if repetitions and cd >= repetitions:
            break

if __name__ == "__main__":
    # ping('192.168.0.1')
    # ping('8.8.8.8', count=10)
    ping('8.8.8.8')
    #ping(gw())
    # pings(gw())
