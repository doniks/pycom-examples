import sqnsupgrade

from network import LTE
def send_at_cmd_pretty(cmd, verbose=True):
    return lte.send_at_cmd(cmd).replace('\r', '').strip().replace('\n\n','\n')

# def send_at_cmd_pretty_return(cmd, verbose=True):
#     response = lte.send_at_cmd(cmd).split('\r\n')
#     retval =
#     for line in response:
#         if ( len(line) == 0 ):
#             continue
#         elif ( line == "OK" ):
#             retval = True
#             continue
#         elif line == "ERROR":
#             retval = False
#         else:
#             if verbose:
#                 print(len(line), line)
#                 retval = line
#     return retval

lte = LTE()


print("############ ATI1")
a = send_at_cmd_pretty('ATI1')
print(a)
if "LR5.1.1.0-33080" in a:
    print("legacy")

print("############ info")
sqnsupgrade.info()
print("state", sqnsupgrade.state())
print("imei", sqnsupgrade.imei())
# load
# reconnect_uart
print("release", sqnsupgrade.release)
print("VERSION", sqnsupgrade.VERSION)
# crc
# stp
# run
# uart

#print("############ info debug")
#info = sqnsupgrade.info(debug=True)
