hex_string_prefixed = "\xde\xad\xbe\xef"
print(" ".join(hex(ord(n)) for n in hex_string_prefixed))
# 0xde 0xad 0xbe 0xef

hex_bytes = b'\xde\xad\xbe\xef'
print(" ".join(hex(n) for n in hex_bytes))

hex_string = "deadbeef"
print(hex(int(hex_string, 16)))
# 0xdeadbeef

a=12
b=0xf
print("0x{0:02x} {1:02x}".format(a,b))
# 0x0c 0f

print("'12345'_12345678_")
print("'12345'_     .12_")
for x in range(998, 1111, 11):
    print("'{:>5s}'_{:8.2f}_".format(str(x), x/11))

# new_str = ""
# str_value = "rojbasr"
# for i in str_value:
#     new_str += "0x%s " % (i.encode('hex'))
# print new_str

0.123
print("{}")
