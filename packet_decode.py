from misc_func import byte_sum
from misc_func import byte_diff0xff
from misc_func import hexstr

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

  print('AT Command Response frame (0x88)')
  print('  Frame ID: {}'.format(hex(fid)))
  print('  AT command: {}{}'.format(athi.decode(),atlo.decode()))
  print('  Command status: {} ({})'.format(status,status_dict[status]))

  # Presence of Command Data
  if len(payload) > 5:
    print('  Command data: 0x{}'.format(hexstr(payload[5:])))

# Decode Transmit Status frame 0x8b
def decode_txstat(payload):

  fid = payload[1]
  dest16 = hexstr(payload[2:4])
  txretry = payload[4]
  delivery = payload[5]
  delivery_dict = {
    0x00 : 'Success',
    0x01 : 'MAC ACK failure',
    0x02 : 'Collision avoidance failure',
    0x21 : 'Network ACK failure',
    0x25 : 'Route not found',
    0x31 : 'Internal resource error',
    0x32 : 'Internal error'
  }
  discovery = payload[6]
  discovery_dict = {
    0x00 : 'No discovery overhead',
    0x02 : 'Route discovery'
  }

  print('Transmit Status frame (0x8b)')
  print('  Frame ID: {}'.format(hex(fid)))
  print('  16-bit dest addr: {}'.format(dest16))
  print('  Tx retry count: {}'.format(txretry))
  print('  Delivery status: {} ({})'.format(delivery,delivery_dict[delivery]))
  print('  Discovery status: {} ({})'.format(discovery,discovery_dict[discovery]))

# Decode Receive Packet frame 0x90
def decode_rxpacket(payload):

  src = hexstr(payload[1:9])
  res = hexstr(payload[9:11])
  rxopt = payload[11]
  rxopt_dict = {
    0x01 : 'Packet acknowledged',
    0x02 : 'Packet was a broadcast packet'
  }
  data = hexstr(payload[12:])

  print('Receive Packet frame (0x90)')
  print('  64-bit source addr: {}'.format(src))
  print('  Reserved: {}'.format(res))
  if rxopt in rxopt_dict:
    print('  Rx options: {} ({})'.format(rxopt,rxopt_dict[rxopt]))
  else:
    print('  Rx options: ({})'.format(hex(rxopt)))
  print('  Rx data: 0x{} ({})'.format(data,payload[12:]))

# Decode generic payload
def decode_payload(payload):

  if payload[0] == 0x88:
    decode_atcomres(payload)
  elif payload[0] == 0x8b:
    decode_txstat(payload)
  elif payload[0] == 0x90:
    decode_rxpacket(payload)
  else:
    print('Error: Unknown XBee API frame type')
