from misc_func import byte_sum
from misc_func import byte_diff0xff

# AT Command Query
#   param - AT parameter (String format)
#   returns byte string to send to XBee UART
def atcom_query(param):

  # Header
  bytestr = b'\x7e'

  # Length
  length = 4
  bytestr = bytestr + (length).to_bytes(2,'big')

  # Frame type
  ftype = b'\x08'
  bytestr = bytestr + ftype

  # Frame ID
  fid = b'\x01'
  bytestr = bytestr + fid
  checksum = byte_sum(ftype,fid)

  # AT command
  athi = bytes(param[0],'ascii')
  atlo = bytes(param[1],'ascii')
  bytestr = bytestr + athi + atlo
  checksum = byte_sum(checksum,athi)
  checksum = byte_sum(checksum,atlo)

  # Checksum
  checksum = byte_diff0xff(checksum)
  bytestr = bytestr + checksum

  return bytestr
