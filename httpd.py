import usocket as socket
from network import WLAN

CONTENT = """HTTP/1.0 200 OK
Content-Type: text/html
Hello #{} from MicroPython!"""

wlan = WLAN()
print(wlan.ifconfig())
ai = socket.getaddrinfo("192.168.4.1",80)
addr = ai[0][4]
print("addr", addr)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(addr)
s.listen(5)
# s.settimeout(5)
counter=0

while True:
    print("accept", counter)
    res = s.accept()
    if res:
        client_s = res[0]
        client_addr = res[1]
        print("Client address:", client_addr)
        print("Client socket:", client_s)
        req = client_s.recv(4096)
        print("Request:", req)
        resp = bytes(CONTENT.format(counter), "ascii")
        print("Response:", resp)
        client_s.send(resp)
        client_s.close()
        parts = req.decode('ascii').split(' ')
        if parts[1] == '/exit':
            break
    counter += 1
