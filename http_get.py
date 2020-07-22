import socket
import time
def_url = 'http://detectportal.firefox.com/'

def http_get(url = def_url):
    time_start = time.time()
    dur_send = 0
    dur_recv = 0
    dur_total = 0
    bps_send = 0
    bps_recv = 0
    len_recv = 0
    cnt_recv = 0
    success = False
    try:
        print("http_get(", url, ")")
        _, _, host, path = url.split('/', 3)
        print('getaddrinfo')
        ip_port = socket.getaddrinfo(host, 80)[0][-1]
        print('socket')
        s = socket.socket()
        print('connect')
        s.connect(ip_port)
        request = bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8')
        time_send = time.time()
        print('send')
        s.send(request)
        dur_send = time.time() - time_send
        if dur_send:
            bps_send = len(request) / dur_send

        print('recv')
        time_recv = time.time()
        s.settimeout(60)
        while True:
            data = s.recv(100)
            if data:
                cnt_recv += 1
                len_recv += len(data)
                dur_recv = time.time() - time_recv
                if dur_recv:
                    bps_recv = len_recv / dur_recv
                if cnt_recv % 1000 == 0:
                    print("received[", time.time(), "]:", len_recv, bps_recv)
                success = True
                # print(str(data, 'utf8'), end='')
                pass
            else:
                break
        print("recv: done")
        print("close")
        s.close()
    except Exception as e:
        print("http_get failed:", e)
    dur_total = time.time() - time_start
    return (success, dur_send, dur_recv, dur_total, len_recv, bps_send, bps_recv)

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
    # http_get('http://micropython.org/ks/test.html')
    http_gets('http://detectportal.firefox.com/')
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
