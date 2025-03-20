from network import LTE
print('init')
lte = LTE(debug=True)
print('at')
lte.send_at_cmd('AT')
print('version')
lte.send_at_cmd('ATI1')
