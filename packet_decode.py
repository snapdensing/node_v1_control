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

# Decode AT Command Response frame 0x88
def decode_atcomres(payload):

  fid = payload[1]
  athi = (payload[2]).to_bytes(1,'big')
  atlo = (payload[3]).to_bytes(1,'big')
  status = payload[4]
  status_dict = {
    0 : 'OK',
    1 : 'ERROR',
    2 : 'Invalid command',
    3 : 'Invalid parameter'
  }

  # Presence of Command Data
#  if len(payload) > 5:
#    datalen = len(payload) - 5
#    for i in range(datalen):
      
  
  print('AT Command Response frame (0x88)')
  print('  Frame ID: {}'.format(hex(fid)))
  print('  AT command: {}{}'.format(athi.decode(),atlo.decode()))
  print('  Command status: {}({})'.format(status,status_dict[status]))
  
# Decode generic payload
def decode_payload(payload):

  if payload[0] == 0x88:
    decode_atcomres(payload)
  else:
    print('Error: Unknown XBee API frame type')
