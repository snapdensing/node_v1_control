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
