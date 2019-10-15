# Functions for testing XBee using the interactive python terminal

import serial

# Configure remote node address
def cmdtest_remoteaddr():
  return b'\x00\x13\xa2\x00\x40\xbf\x1f\x4a'

# Configure serial
def cmdtest_uartsetup():
  ser = serial.Serial('/dev/ttyUSB0')
  print(ser.name)
  return ser

# Debug Unicast
def cmdtest_unicast(ser,n,dest):
  from packet_encode import debug_unicast
  from packet_decode import rxpacket
  tx_packet = debug_unicast(n,dest)
  print('Tx Packet: {}'.format(tx_packet))
  print('-----')
  ser.write(tx_packet)
  for i in range(n+1):
    status, payload = rxpacket(ser)
    print('Payload: {}'.format(payload))
    print('-----')
  
