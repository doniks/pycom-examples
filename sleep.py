import socket
import time

def sleep(s, verbose=False):
    if verbose:
        print("sleep(", s, ") ", end="")
    while s > 0:
        if verbose:
            print(s, end=" ")
        time.sleep(1)
        s -= 1
    if verbose:
        print("")


if __name__ == "__main__":
    sleep(3, True)
