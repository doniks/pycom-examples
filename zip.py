#!/usr/bin/env python3

import zlib
import os
s = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n'
b = bytes(s, "utf-8")
z = zlib.compress(b)
with open('test.txt.z', 'wb') as f:
    f.write(z)
print('ratio', len(z)/len(s))
