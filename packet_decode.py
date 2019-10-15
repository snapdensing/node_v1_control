from misc_func import byte_sum
from misc_func import byte_diff0xff

# Receive XBee API frame
def rxpacket(ser):

  payload = b'\x00'

  # Header: 0x7e
  header = ser.read(1)
  if header != b'\x7e':
    print('Error receiving packet: Header')
    return 0, payload 

  # Length: 2 bytes
  lengthb = ser.read(2)
  length = int.from_bytes(lengthb,'big')
  if length == 0:
    print('Error receiving packet: Zero length')
    return 0, payload

  # Payload
  checksum = b'\x00'
  payload = b''
  for i in range(length):
    currbyte = ser.read(1)
    payload = payload + currbyte
    checksum = byte_sum(checksum,currbyte) 

  # Checksum
  currbyte = ser.read(1)
  checksum = byte_diff0xff(checksum)
  if checksum != currbyte:
    print('Error receiving packet: Invalid checksum')
    return 0, payload

  print('Received XBee API frame w/ length {}'.format(length))
  return 1, payload

