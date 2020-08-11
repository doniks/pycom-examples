import socket
import time
def_url = 'http://detectportal.firefox.com/'

def http_get(url=None, kb=None, verbose=False, timeout_s=5, do_print=False):
    if not url:
        if kb is not None:
            if kb == 0:
                url = def_url # the smallest file I know
                print('smallest file:', url)
            elif kb == 1:
                url = 'http://ftp.snt.utwente.nl/pub/docs/rfc/rfc1498.json' # 1000 B
                print('1k file:', url)
            elif kb == 10:
                url = 'http://ftp.snt.utwente.nl/pub/docs/rfc/rfc1535.html'
                print('10k file:', url)
            elif kb == 100:
                url = 'http://ftp.snt.utwente.nl/pub/docs/rfc/rfc753.html'
                print('100k file:', url)
            elif kb == 1000:
                url = 'http://ftp.snt.utwente.nl/pub/test/1M'
                print('1M file', url)
            elif kb == 10000:
                url = 'http://ftp.snt.utwente.nl/pub/test/10M'
            else:
                raise Exception("Don't have a url that matches kb=", kb)
            # http_get('http://ftp.snt.utwente.nl/pub/test/100M')
        else:
            url = def_url

    time_start_ms = time.ticks_ms()
    dur_send_ms = 0
    dur_recv_ms = 0
    dur_total_s = 0
    bps_send = 0
    bps_recv = 0
    len_recv = 0
    cnt_recv = 0
    success = False
    try:
        # print("http_get(", url, ")")
        _, _, host, path = url.split('/', 3)
        # print('getaddrinfo')
        ip_port = socket.getaddrinfo(host, 80)[0][-1]
        # print('socket')
        s = socket.socket()
        # print('connect')
        s.connect(ip_port)
        request = bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8')
        time_send_ms = time.ticks_ms()
        # print('send request')
        s.send(request)
        dur_send_ms = time.ticks_ms() - time_send_ms
        if dur_send_ms:
            bps_send = len(request) / dur_send_ms / 1000

        # print('recv response')
        time_recv_ms = time.ticks_ms()
        s.settimeout(timeout_s) # 10)
        while True:
            data = s.recv(100)
            if data:
                cnt_recv += 1
                len_recv += len(data)
                dur_recv_ms = time.ticks_ms() - time_recv_ms
                if dur_recv_ms:
                    dur_recv_s = dur_recv_ms / 1000
                    bps_recv = len_recv / dur_recv_s
                    if verbose or dur_recv_s % 5 == 0:
                        print("received[", time.time(), "]: len=", len_recv, "bps=", bps_recv)
                    if do_print:
                        print(str(data, 'utf8'), end='')

                success = True
                pass
            else:
                break
        # print("recv: done")
        # print("close")
        s.close()
    except Exception as e:
        print("http_get Exception:", e)
        success = False
    dur_total_s = (time.ticks_ms() - time_start_ms ) / 1000
    dur_send_s = dur_send_ms / 1000
    dur_recv_s = dur_recv_ms / 1000
    if success:
        print("http_get succeeded:", end="")
    else:
        print("http_get failed:", end="")
    print(len_recv, "bytes received in", dur_recv_s, "s ->", bps_recv, "bps")
    return (success, dur_send_ms/ 1000, dur_recv_ms/1000, dur_total_s, len_recv, bps_send, bps_recv)


# def http_gets(url = def_url, count=1):
#     for c in range(0, count):
#         try:
#             http_get(url)
#             print("success[", c, "]")
#             # break
#         except Exception as e:
#             print("failure[", c, "]:", e)

def http_gets(url = def_url, count=1):
    for c in range(0, count):
        print(c, http_get(url))

if __name__ == "__main__":
    # http_get()
    http_get(kb=0)
    # http_get('http://micropython.org/ks/test.html')
    # http_gets('http://detectportal.firefox.com/')
    # http_gets('http://192.168.178.1/', 1) # router login page
    # http_get('http://ftp.snt.utwente.nl/pub/docs/rfc/rfc1498.json') # 1000 B
    # http_get.http_gets('http://ftp.snt.utwente.nl/pub/docs/rfc/rfc1535.html') #   10 KiB
    # http_get('http://ftp.snt.utwente.nl/pub/docs/rfc/rfc753.html')  #  100 KiB
    # http_get('http://ftp.snt.utwente.nl/pub/test/1M')               #  977 KiB
    # http_get('http://ftp.snt.utwente.nl/pub/test/100M')
    # http_get.http_gets('http://ftp.snt.utwente.nl/pub/test/10M')
    # http_get.http_gets("http://10.0.103.1/pycom-fwtool-1.16.1-bionic-amd64.deb") # peters laptop in the office
    # http_get.http_gets("http://192.168.178.81/pycom-fwtool-1.16.1-bionic-amd64.deb") # peters laptop at home via wifi
    # laptop when directly connected to the PyEthernet
    # http_gets("http://192.168.0.1/pycom-fwtool-1.16.1-bionic-amd64.deb")
    # http_gets("http://192.168.0.1/test.bin")
