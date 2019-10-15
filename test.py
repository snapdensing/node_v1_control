import serial
from packet_encode import atcom_query
from packet_decode import rxpacket
from packet_encode import debug_unicast

ser = serial.Serial('/dev/ttyUSB0')
print(ser.name)

#ser.write(atcom_query('PL'))
#status, payload = rxpacket(ser)
#print('Payload: {}'.format(payload))

#ser.write(atcom_query('CH'))
#status, payload = rxpacket(ser)
#print('Payload: {}'.format(payload))

dest = b'\x00\x13\xa2\x00\x40\xbf\x1f\x4a'
tx_packet = debug_unicast(10,dest)
print('Tx Packet: {}'.format(tx_packet))
ser.write(tx_packet)
for i in range(11):
  status, payload = rxpacket(ser)
  print('Payload: {}'.format(payload))
  print('---------')

ser.close()

print('End')
