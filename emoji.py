print(' ', end='')
b = 1
for e in "😶😐😯😮😨😰😱🤢🤮😵🤯🥵💥":
    for i in range(b):
        print('\b', end='')
    print(e, end=' ')
    b = len(e)+1
    time.sleep(0.5)
sys.exit()
