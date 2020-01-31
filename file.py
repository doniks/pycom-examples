
f = open('test.txt2', 'w')
f.write("bla\nblub")
f.close()
f = open('test.txt2', 'r')
content = f.read()
f.close()
print(content)
