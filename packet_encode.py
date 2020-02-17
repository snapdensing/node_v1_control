# Functions for assembling XBee API frames

from misc_func import byte_sum
from misc_func import byte_diff0xff
from misc_func import hexstr2byte
from misc_func import hexstr

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

# AT Command Set
#   param - AT parameter (String format)
#   value - New AT parameter value (in bytes)
#   returns byte string to send to XBee UART
def atcom_set(param,value):

  # Header
  bytestr = b'\x7e'

  # Length
  length = 4 + len(value)
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

  # Parameter value
  bytestr = bytestr + value
  for i in range(len(value)):
    checksum = byte_sum(checksum,(value[i]).to_bytes(1,'big'))

  # Checksum
  checksum = byte_diff0xff(checksum)
  bytestr = bytestr + checksum

  return bytestr


# Debug command: Unicast
#   n - number of unicast transmissions
#   dest - 64-bit destination address (in bytes)
def debug_unicast(n,dest):

  # Header
  bytestr = b'\x7e'

  # Length
  length = 17
  bytestr = bytestr + (length).to_bytes(2,'big')

  # Frame type
  ftype = b'\x10'
  bytestr = bytestr + ftype

  # Frame ID
  fid = b'\x01'
  bytestr = bytestr + fid
  checksum = byte_sum(ftype,fid)

  # 64-bit dest addr
  bytestr = bytestr + dest
  for i in range(8):
    checksum = byte_sum(checksum,dest[i].to_bytes(1,'big'))
    
  # 16-bit dest addr
  dest16 = b'\xff\xfe' 
  bytestr = bytestr + dest16
  for i in range(2):
    checksum = byte_sum(checksum,dest16[i].to_bytes(1,'big'))

  # Broadcast radius
  brad = b'\x00'
  bytestr = bytestr + brad
  checksum = byte_sum(checksum,brad)

  # Options
  opt = b'\x00'
  bytestr = bytestr + opt
  checksum = byte_sum(checksum,opt)

  # Data
  data = b'DU'
  if n > 255:
    print('Error: number of transmissions exceeds limit')
    return bytestr
  data = data + (n).to_bytes(1,'big')
  bytestr = bytestr + data
  checksum = byte_sum(checksum,b'D')
  checksum = byte_sum(checksum,b'U')
  checksum = byte_sum(checksum,(n).to_bytes(1,'big'))

  # Checksum
  checksum = byte_diff0xff(checksum)
  bytestr = bytestr + checksum

  return bytestr  

# Generic Transmit request
#   fid - Frame ID (hex string, 1 byte)
#   dest - 64-bit dest address (hex string, 8 bytes)
#   brad - Broadcat radius (hex string, 1 byte)
#   opts - Transmit options (hex string, 1 byte)
#   data - RF data (hex string, variable length)
def gen_txreq(fid,dest,brad,opts,data):

  if len(fid) != 2:
    print('Error generating tx req: Frame ID')
    return b'' 
  bytestr = b'\x10' + hexstr2byte(fid)

  if len(dest) != 16:
    print('Error generating tx req: 64-bit dest addr') 
    return bytestr
  bytestr = bytestr + hexstr2byte(dest) + b'\xff\xfe'

  if len(brad) != 2:
    print('Error generating tx req: Broadcast radius')
    return bytestr
  bytestr = bytestr + hexstr2byte(brad)

  if len(opts) != 2:
    print('Error generating tx req: Transmit options') 
    return bytestr
  bytestr=  bytestr + hexstr2byte(opts)

  if (len(data)%2) != 0:
    print('Error generating tx req: RF data')
    return bytestr
  bytestr=  bytestr + hexstr2byte(data)

  return bytestr

# Attach header and checksum
#   bytestr - packet contents
def gen_headtail(bytestr):

  # Compute checksum
  checksum = b'\x00'
  for i in range(len(bytestr)):
    checksum = byte_sum(checksum,(bytestr[i]).to_bytes(1,'big'))
  checksum = byte_diff0xff(checksum)

  # Generate length
  length = (len(bytestr)).to_bytes(2,'big')

  # Append headers and checksum
  bytestr = b'\x7e' + length + bytestr + checksum

  return bytestr

# Debug command: Remote Unicast (version 2)
#   n - number of unicast transmissions
#   dest - 64-bit destination address (in bytes)
def debug_unicast2(n,dest):

  if n > 255:
    print('Error: number of transmissions exceeds limit')
    return b''

  data = b'DU' + (n).to_bytes(1,'big')
  payload = gen_txreq('01',hexstr(dest),'00','00',hexstr(data))

  bytestr = gen_headtail(payload)

  return bytestr

# Debug command: Remote Change channel
#   ch - channel (in bytes)
#   dest - 64-bit destination address (in bytes)
def debug_channel(ch,dest):
  data = b'DC' + ch
  payload = gen_txreq('01',hexstr(dest),'00','00',hexstr(data)) 
  bytestr = gen_headtail(payload)
  return bytestr

# Debug command: Remote Change power level
#   pow - power level (in bytes)
#   dest - 64-bit destination address (in bytes)
def debug_power(pow,dest):
  data = b'DP' + pow
  payload = gen_txreq('01',hexstr(dest),'00','00',hexstr(data)) 
  bytestr = gen_headtail(payload)
  return bytestr

# Command: Start
#   period - sampling period (in int)
#   dest - 64-bit destination address (in bytes)
def start_sensing(period,dest):

  if period < 256:
      period_b = (period).to_bytes(1,'big')
  else:
      period_b = (period).to_bytes(2,'big')

  #data = b'S' + (period).to_bytes(1,'big')
  data = b'S' + period_b
  payload = gen_txreq('01',hexstr(dest),'00','00',hexstr(data))
  bytestr = gen_headtail(payload)
  return bytestr

# Command: Start (retain previous period)
#   dest - 64-bit destination address (in bytes)
def start_sensing_ret(dest):

  data = b'S'
  payload = gen_txreq('01',hexstr(dest),'00','00',hexstr(data))
  bytestr = gen_headtail(payload)
  return bytestr

# Command: Stop
#   dest - 64-bit destination address (in bytes)
def stop_sensing(dest):
  data = b'X'
  payload = gen_txreq('01',hexstr(dest),'00','00',hexstr(data))
  bytestr = gen_headtail(payload)
  return bytestr 

# Command: Change aggregator address
#   dest - 64-bit destination (remote) address (in bytes)
#   newaddr - new 64-bit aggregator address (in bytes)
def debug_setaddr(newaddr,dest):
  data = b'DA' + newaddr
  payload = gen_txreq('01',hexstr(dest),'00','00',hexstr(data))
  bytestr = gen_headtail(payload)
  return bytestr

# Command: Remote Query parameter
#   atcom - 2-character string for AT parameter
#         - 1-character string for MSP parameter
def debug_query(atcom,dest):
  command_dict = {
    'PL' : b'QP',
    'CH' : b'QC',
    'A'  : b'QA',
    'T'  : b'QT'
  }
  data = command_dict[atcom]
  print('data: {}({})'.format(data,type(data)))
  payload = gen_txreq('01',hexstr(dest),'00','00',hexstr(data))
  bytestr = gen_headtail(payload)
  return bytestr

# Command: Remote form arbitrary message
#   msg - arbitrary message (hex str)
#   dest - 64-bit destination address (in bytes)
def msgformer(msg,dest):
  payload = gen_txreq('01',hexstr(dest),'00','00',msg)
  bytestr = gen_headtail(payload)
  return bytestr

# Debug command: Remote Change control flag
#   flag - flag value (in bytes)
#   dest - 64-bit destination address (in bytes)
def debug_flag(flag,dest):
  data = b'DF' + flag
  payload = gen_txreq('01',hexstr(dest),'00','00',hexstr(data)) 
  bytestr = gen_headtail(payload)
  return bytestr

# Debug command: Remote Change period
#   period - sampling period (integer)
#   dest - 64-bit destination address (in bytes)
def debug_period(period,dest):

  if period < 256:
      period_b = (period).to_bytes(1,'big')
  else:
      period_b = (period).to_bytes(2,'big')

  data = b'DT' + period_b
  payload = gen_txreq('01',hexstr(dest),'00','00',hexstr(data)) 
  bytestr = gen_headtail(payload)
  return bytestr
