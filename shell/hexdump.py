import binascii
def hexdump(filename, print_ascii=True, head=None):
    f = open(filename, 'r')
    content = f.read()
    f.close()
    ct = 0
    ascii_buffer = ""
    for c in content:
        # pretty print one byte
        print("{:02x} ".format(ord(c)), end="")
        if (0 <= ord(c) and ord(c) <= 0x1f) or ord(c) in [0x23, 0x7f, 0x81, 0x8d, 0x8f, 0x90, 0x9d, 0xa0, 0xad]: # c == '\n' or c == '\r' or (): #ord(c) in [0, 1, 2, 3, 4, 0x7f]:
            # non-printable characters
            # there are probably many more ... you find one, you fix it
            ascii_buffer += '.'
        elif ord(c) == 0x5c:
            ascii_buffer += '\\'
        elif ord(c) == 0x20:
            ascii_buffer += ' '
        else:
            ascii_buffer += c # str(c)
        ct += 1
        if ct % 8 == 0:
            print(" ", end="")
        if ct % 16 == 0:
            # wrap the line after 16 bytes
            if print_ascii:
                print(" |{:s}|".format(ascii_buffer))
            else:
                print()
            ascii_buffer = ""
        if head is not None and ct >= head:
            break
    if ascii_buffer:
        l = ct % 16
        for x in range(0, 16-l):
            # leave space as much as we have left in this line
            print('   ', end='')
        if l < 8:
            # print one space for ending off both blocks of 8
            print('  ', end='')
        else:
            # print one space for ending off the second block of 8
            print(' ', end='')
        # last partially filled ascii_buffer
        if print_ascii:
            print(" |{:s}|".format(ascii_buffer))
        else:
            print()

def hexdumptest(print_ascii=False):
    hexdump("/flash/test/test.bin.up", print_ascii)


if __name__ == "__main__":
    # hexdump("/flash/test/test.bin.up")
    # hexdump("/flash/test/http_get.recv")
    # cat("/flash/log_GPy_240ac4c7b250.log")
    hexdump("/flash/up41065.elf", head=2000)
