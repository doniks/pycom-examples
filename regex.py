import re

str="pycom foo micro python foo-bar"

# def r(regex, str=str):
regex='foo.'
m = re.search(regex, str)
print('"', regex, '", "', str, '" -> "', m.group(0),'"', sep='')

# r('foo.')
