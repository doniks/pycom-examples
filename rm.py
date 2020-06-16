
def rm(file):
    print("rm", file)
    import os
    os.unlink(file)

if __name__ == "__main__":
    rm('/flash/main.py')
