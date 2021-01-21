print("""
Yes we can do funky colors such as
\x1b[93myellow \x1b[91mt\x1b[92me\x1b[94mx\x1b[96mt
\x1b[0mor \x1b[7mblack on white
\x1b[0mor \x1b[45;94mblue on purple
\x1b[4mwith underline
\x1b[3mor italics
\x1b[1mand bold!\x1b[0m""")
# https://en.wikipedia.org/wiki/ANSI_escape_code

print('And spinning wheel for progress: -', end='')
import time
for ct in range(30):
    x = ct % 3
    if x == 0:
        print('\b\\', end='')
    elif x == 1:
        print('\b/', end='')
    elif x == 2:
        print('\b-', end='')
    time.sleep_ms(100)
print()


print("Emojis as well! 😇 🙂 😊 😉 😀 😆 😁 😅 😂 🤣 🙃 ")
# but note:
# we cannot "Run" it in Atom, not even in comments. It works only via upload
# also add a space after every emoji, otherwise they overlap
# https://unicode.org/emoji/charts/full-emoji-list.html
