import serial
from packet_encode import atcom_query
from packet_decode import rxpacket

ser = serial.Serial('/dev/ttyUSB0')
print(ser.name)

ser.write(atcom_query('PL'))
status, payload = rxpacket(ser)
print('Payload: {}'.format(payload))

ser.write(atcom_query('CH'))
status, payload = rxpacket(ser)
print('Payload: {}'.format(payload))

ser.close()
