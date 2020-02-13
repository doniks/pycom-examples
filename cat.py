filename = "/flash/pybytes_config.json"

f = open(filename, 'r')
content = f.read()
f.close()
print(content, sep="")
