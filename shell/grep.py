import re

def grep(regex, str, line_numbers=False, do_return=False):
    lines = str.split('\n')
    ct = 0
    retval = ""
    for line in lines:
        if re.search(regex, line):
            if do_return:
                if line_numbers:
                    retval += str(ct)
                retval += line + '\n'
            else:
                if line_numbers:
                    print(ct, end=' ')
                print(line)
        # else:
        #     print(ct, line, "NO")
        ct += 1
    if do_return:
        return retval


if __name__ == "__main__":
    str="""asdf foo
bar stuff
things
p y c o m
123foo890
dc
"""
    grep('foo|bar', str)
