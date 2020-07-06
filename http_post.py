def http_post(url, post_data):
    import socket
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    print("post:", path, host, len(post_data), post_data)
    s.send(bytes('POST /%s HTTP/1.0\r\nHost: %s\r\nContent-Length: %d\r\n%s\r\n\r\n\r\n\r\n' % (path, host, len(post_data), post_data), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break
    s.close()

# http_get('http://micropython.org/ks/test.html')
r = machine.rng()
print(r)
http_post('http://ptsv2.com/t/8gcmj-1581434758/post', str(r))
