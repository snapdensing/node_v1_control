def byte_xor(ba1, ba2):
  return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

# Get sum of 2 bytes
def byte_sum(ba1, ba2):
  sum = int.from_bytes(ba1,'big') + int.from_bytes(ba2,'big')
  if sum > 255:
    sum = sum - 256
  return (sum).to_bytes(1,'big')

# Get difference of 0xFF and a specified byte
def byte_diff0xff(x):
  diff = int.from_bytes(b'\xff','big') - int.from_bytes(x,'big')
  return (diff).to_bytes(1,'big')

# Convert byte stream to hex string
def hexstr(bytestream):
  hexstream = ''
  for i in range(len(bytestream)):
    hexchar = hex(bytestream[i])
    if len(hexchar) == 3:
      hexchar = hexchar[0:2] + '0' + hexchar[2]
    hexstream = hexstream + hexchar[2:]
  return hexstream

# Convert hex string to byte stream
def hexstr2byte(hexstream):

  if (len(hexstream)%2) != 0:
    print('Error converting hex string to bytes: odd number of chars')
    return b'' 

  bytestream = b''
  for i in range(len(hexstream)):
    if (i%2)==0:
      curr_int = int(hexstream[i:(i+2)],16)
      bytestream = bytestream + (curr_int).to_bytes(1,'big')

  return bytestream
