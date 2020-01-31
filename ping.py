import socket
import time

def sleep(s):
    #print("sleep(", s, ")", end="")
    while s > 0:
        #print(".", end="")
        time.sleep(1)
        s -= 1
    #print("")

host = "detectportal.firefox.com"
ct = 0

while True:
    t = time.time()
    ip = socket.getaddrinfo(host, 80)[0][4][0]
    print(time.time(), ct, host, ip, "(", time.time() - t, "seconds )")
    ct += 1
    sleep(2)
