import machine
import socket
import pycom

def http_get(url):
    print("get(", url, ")")
    _, _, host, path = url.split('/', 3)
    print("host", host)
    print("path", path)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    print("addr", addr)
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    # s.settimeout(5)
    # while True:
    #     data = s.recv(100)
    #     if data:
    #         print(str(data, 'utf8'), end='')
    #     else:
    #         break
    s.close()

# http_get('http://micropython.org/ks/test.html')
# 'http://detectportal.firefox.com/',

ct = 0
try:
    ct = pycom.nvs_get("hgwct")
    ct += 1
except:
    pass
pycom.nvs_set("hgwct", ct)

url = 'http://webhook.site/d393c709-9736-4ef1-8c61-0806fd22e858'
data = str(machine.rng())
http_get(url + "?data=" + data + "&ct=" + str(ct))

# go to
# https://webhook.site/#!/d393c709-9736-4ef1-8c61-0806fd22e858/fee74dde-c8e8-4cd3-9ad1-e286d1169ea5/1
# to see the results
