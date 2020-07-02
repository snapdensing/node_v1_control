import serial

import packet_encode as pe
import packet_decode as pd
import misc_func as mf

# UART and XBee Configuration
# Arguments:
#   device - (string) serial device (e.g. /dev/ttyUSB0)
#   power - (int) XBee transmit power (0 to 4)
#   channel - (int) XBee channel (11 to 26) 
# Returns:
#   ser - (serial class) serial
def config(device,power,channel):
  ser = serial.Serial(port=device, timeout=5)

  # Set power
  if (power > 4) | (power < 0):
    print('Invalid power')
    return ser
  bytestr = pe.atcom_set('PL',(power).to_bytes(1,'big'))
  ser.write(bytestr)
  payload = b'\x00'
  while payload[0] != 0x88:
    success, payload = pd.rxpacket_buffered(ser)
    if payload == b'':
      print('Serial timeout')
      return ser
    if success == 0:
      print('Error receiving response from AT set PL')
      return ser
    if payload[0] == 0x88:
      error = pd.decode_atcomres(payload)
      if error == 1:
        print('Error reported by AT command response') 
        return success

  print('Set power {}: success'.format(power))  

  # Set channel
  if (channel > 26) | (channel < 11):
    print('Invalid channel')
    return ser
  bytestr = pe.atcom_set('CH',(channel).to_bytes(1,'big'))
  ser.write(bytestr)
  payload = b'\x00'
  while payload[0] != 0x88:
    success, payload = pd.rxpacket_buffered(ser)
    if payload == b'':
      print('Serial timeout')
      return ser
    if success == 0:
      print('Error receiving response from AT set CH')
      return ser
    if payload[0] == 0x88:
      error = pd.decode_atcomres(payload)
      if error == 1:
        print('Error reported by AT command response') 
        return success

  print('Set channel {}: success'.format(channel))

  # Write to NVM 
  bytestr = pe.atcom_query('WR')
  ser.write(bytestr)
  payload = b'\x00'
  while payload[0] != 0x88:
    success, payload = pd.rxpacket_buffered(ser)
    if payload == b'':
      print('Serial timeout')
      return ser
    if success == 0:
      print('Error receiving response from AT query WR')
      return ser
    if payload[0] == 0x88:
      error = pd.decode_atcomres(payload)
      if error == 1:
        print('Error reported by AT command response') 
        return success

  print('Configuration saved to NVM')

  return ser

# Config, No timeout version
def config_notimeout(device,power,channel):
  ser = serial.Serial(port=device)

  # Set power
  if (power > 4) | (power < 0):
    print('Invalid power')
    return ser
  bytestr = pe.atcom_set('PL',(power).to_bytes(1,'big'))
  ser.write(bytestr)
  payload = b'\x00'
  while payload[0] != 0x88:
    success, payload = pd.rxpacket_buffered(ser)
    if payload == b'':
      print('Serial timeout')
      return ser
    if success == 0:
      print('Error receiving response from AT set PL')
      return ser
    if payload[0] == 0x88:
      error = pd.decode_atcomres(payload)
      if error == 1:
        print('Error reported by AT command response') 
        return success

  print('Set power {}: success'.format(power))  

  # Set channel
  if (channel > 26) | (channel < 11):
    print('Invalid channel')
    return ser
  bytestr = pe.atcom_set('CH',(channel).to_bytes(1,'big'))
  ser.write(bytestr)
  payload = b'\x00'
  while payload[0] != 0x88:
    success, payload = pd.rxpacket_buffered(ser)
    if payload == b'':
      print('Serial timeout')
      return ser
    if success == 0:
      print('Error receiving response from AT set CH')
      return ser
    if payload[0] == 0x88:
      error = pd.decode_atcomres(payload)
      if error == 1:
        print('Error reported by AT command response') 
        return success

  print('Set channel {}: success'.format(channel))

  # Write to NVM 
  bytestr = pe.atcom_query('WR')
  ser.write(bytestr)
  payload = b'\x00'
  while payload[0] != 0x88:
    success, payload = pd.rxpacket_buffered(ser)
    if payload == b'':
      print('Serial timeout')
      return ser
    if success == 0:
      print('Error receiving response from AT query WR')
      return ser
    if payload[0] == 0x88:
      error = pd.decode_atcomres(payload)
      if error == 1:
        print('Error reported by AT command response') 
        return success

  print('Configuration saved to NVM')

  return ser



# Set Aggregator
# Arguments:
#   ser - Serial interface
#   remote - (hex string) 64-bit remote node address
#   aggre - (hex string) 64-bit aggregator address
def remote_aggre(ser,remote,addr):
  success = 0

  # Arguments check
  if len(remote) != 16:
    print('Invalid remote node address')
    return success
  if len(addr) != 16:
    print('Invalid aggregator address')
    return success

  addr_b = mf.hexstr2byte(addr)
  remote_b = mf.hexstr2byte(remote)

  bytestr = pe.debug_setaddr(addr_b,remote_b) 
  ser.write(bytestr)

  payload = b'\x00'
  while payload[0] != 0x8b:
    success, payload = pd.rxpacket_buffered(ser)
    if payload == b'':
      print('Serial timeout')
      return 0
    if success == 0:
      print('Error receiving response from Transmit request')
      return success
    if payload[0] == 0x8b:
      error = pd.decode_txstat(payload)
      if error == 1:
        print('Error reported by Transmit status')
        return 0

  print('Remote {} aggregator now set to {}'.format(remote,addr))
  success = 1
  return success

# Stop node from sensing
# Returns 1 if success, 0 otherwise
def remote_stop(ser,remote):
  timeout_max = 5
  remote_b = mf.hexstr2byte(remote)

  bytestr = pe.stop_sensing(remote_b)
  ser.write(bytestr)

  timeouts = 0
  while 1:
    success, payload = pd.rxpacket_buffered(ser)
    if payload == b'':
      print('Serial timeout, Sending stop again')
      timeouts = timeouts + 1
      ser.write(bytestr)
    else:
      if success == 1:
        success = pd.decode_stopack(payload,remote_b) 
        if success == 1:
          print('Remote node {} stopped'.format(remote))
          return success

    if timeouts == timeout_max:
      return 0

# Start node sensing
# Returns 1 if success, 0 otherwise
# period = 0 means retain previous period
def remote_start(ser,remote,period):
  timeout_max = 5

  #if period > 255:
  if (period > 65535) | (period < 0):
    print('Invalid period')
    return 0
  remote_b = mf.hexstr2byte(remote)

  if period != 0:
    bytestr = pe.start_sensing(period,remote_b)
  else:
    bytestr = pe.start_sensing_ret(remote_b)

  ser.write(bytestr)

  timeouts = 0
  while 1:
    success, payload = pd.rxpacket_buffered(ser)

    if payload == b'':
      print('Serial timeout, Sending start again')
      timeouts = timeouts + 1
      ser.write(bytestr)

    else:
      if success == 1:
        success = pd.decode_startack(payload,remote_b)
        if success == 1:
          print('Remote node {} started'.format(remote))
          return success

    if timeouts == timeout_max:
      return 0

# Set node ID
def remote_nodeid(ser,remote,id):
  success = 0
  maxlen = 20

  length = len(id)
  if length > maxlen:
    print('Exceeded maximum node ID length')
    #return 0
  length_b = (length).to_bytes(1,'big')

  data = b'DI' + length_b + bytes(id,'ascii')
  payload = pe.gen_txreq('01',remote,'00','00',mf.hexstr(data))
  bytestr = pe.gen_headtail(payload)
  ser.write(bytestr)

  while success == 0:
    success, payload = pd.rxpacket_buffered(ser)
    if payload == b'':
      print('Serial timeout')
      return 0
    else:
      if success == 1:
        if payload[0] == 0x8b:
          error = pd.decode_txstat(payload)
          if error == 0:
            print('Remote node {} node ID set'.format(remote)) 
            return 1

      success = 0

# Set node loc 
def remote_nodeloc(ser,remote,loc):
  success = 0
  maxlen = 20

  length = len(loc)
  if length > maxlen:
    print('Exceeded maximum node loc length')
    #return 0
  length_b = (length).to_bytes(1,'big')

  data = b'DL' + length_b + bytes(loc,'ascii')
  payload = pe.gen_txreq('01',remote,'00','00',mf.hexstr(data))
  bytestr = pe.gen_headtail(payload)
  ser.write(bytestr)

  while success == 0:
    success, payload = pd.rxpacket_buffered(ser)
    if payload == b'':
      print('Serial timeout')
      return 0
    else:
      if success == 1:
        if payload[0] == 0x8b:
          error = pd.decode_txstat(payload)
          if error == 0:
            print('Remote node {} node loc set'.format(remote)) 
            return 1

      success = 0

# Set remote node channel
# Arguments:
#   ser - Serial interface
#   remote - (hex string) 64-bit remote node address
#   channel - (int) channel
def remote_channel(ser,remote,channel):
  success = 0

  # Arguments check
  if len(remote) != 16:
    print('Invalid remote node address')
    return success
  if (channel > 26) | (channel < 11):
    print('Invalid XBee channel')
    return success

  remote_b = mf.hexstr2byte(remote)
  channel_b = (channel).to_bytes(1,'big') 

  bytestr = pe.debug_channel(channel_b,remote_b) 
  ser.write(bytestr)

  payload = b'\x00'
  while payload[0] != 0x8b:
    success, payload = pd.rxpacket_buffered(ser)
    if payload == b'':
      print('Serial timeout')
      return 0
    if success == 0:
      print('Error receiving response from Transmit request')
      return success
    if payload[0] == 0x8b:
      error = pd.decode_txstat(payload)
      if error == 1:
        print('Error reported by Transmit status')
        return 0

  print('Remote {} channel now set to {}'.format(remote,channel))
  success = 1
  return success

# Set remote node power
# Arguments:
#   ser - Serial interface
#   remote - (hex string) 64-bit remote node address
#   power- (int) power 
def remote_power(ser,remote,power):
  success = 0

  # Arguments check
  if len(remote) != 16:
    print('Invalid remote node address')
    return success
  if (power > 4) | (power < 0):
    print('Invalid XBee power')
    return success

  remote_b = mf.hexstr2byte(remote)
  power_b = (power).to_bytes(1,'big') 

  bytestr = pe.debug_power(power_b,remote_b) 
  ser.write(bytestr)

  payload = b'\x00'
  while payload[0] != 0x8b:
    success, payload = pd.rxpacket_buffered(ser)
    if payload == b'':
      print('Serial timeout')
      return 0
    if success == 0:
      print('Error receiving response from Transmit request')
      return success
    if payload[0] == 0x8b:
      error = pd.decode_txstat(payload)
      if error == 1:
        print('Error reported by Transmit status')
        return 0

  print('Remote {} power now set to {}'.format(remote,power))
  success = 1
  return success

# Remote Query
# Arguments:
#   ser - Serial interface
#   remote - (hex string) 64-bit remote node address
#   param - (string) parameter
def remote_query(ser,remote,param,**kwargs):

  # Supress option
  suppress = kwargs.get('suppress',0)

  success = 0

  command_dict = {
    'PL' : b'QPL',
    'P'  : b'QP',
    'CH' : b'QCH',
    'A'  : b'QA',
    'T'  : b'QT',
    'WR' : b'DW',
    'S'  : b'QS',
    'F'  : b'QF',
    'V'  : b'QV',
    'MR' : b'QMR',
    'NH' : b'QNH'
  }

  data = command_dict[param]
  payload = pe.gen_txreq('01',remote,'00','00',mf.hexstr(data))
  bytestr = pe.gen_headtail(payload)
  ser.write(bytestr)

  while success == 0:

    success, payload = pd.rxpacket_buffered(ser)
    if payload == b'':
      print('Serial timeout')
      return 0
    if success == 0:
      print('Error receiving response from Transmit request')
      return success
    if payload[0] == 0x8b:
      error = pd.decode_txstat(payload)
      if error == 1:
        print('Error reported by transmit status')
        return 0
      else:
        success = 1
    else:
      success = 0

  # Read Transmitted values
  success = 0

  print('Remote node response:')

  while success == 0:

    success, payload = pd.rxpacket_buffered(ser)
    #print('payload: {}'.format(payload))

    if payload == b'':
      print('Serial timeout')
      return 0

    if payload[0] == 0x90:
      #print('-- received packet')
      src, data = pd.decode_rxpacket(payload,suppress=1)
      success = 1
      return data
    else:
      success = 0 

# Commit node settings to NVRAM
def remote_wr(ser,remote):

  remote_query(ser,remote,'WR')

# Set control flag
# Arguments:
#   ser - Serial interface
#   remote - (hex string) 64-bit remote node address
#   flag - (hex string) 8-bit control flag value
def remote_flag(ser,remote,flag):
  success = 0

  # Arguments check
  if len(remote) != 16:
    print('Invalid remote node address')
    return success
  if len(flag) != 2:
    print('Invalid flag')
    return success

  remote_b = mf.hexstr2byte(remote)
  flag_b = mf.hexstr2byte(flag)

  bytestr = pe.debug_flag(flag_b,remote_b)
  ser.write(bytestr)
    
  payload = b'\x00'
  while payload[0] != 0x8b:
    success, payload = pd.rxpacket_buffered(ser)
    if payload == b'':
      print('Serial timeout')
      return 0
    if success == 0:
      print('Error receiving response from Transmit request')
      return success
    if payload[0] == 0x8b:
      error = pd.decode_txstat(payload)
      if error == 1:
        print('Error reported by Transmit status')
        return 0

  print('Remote {} flag now set to {}'.format(remote,flag))
  success = 1
  return success

# Set period
# Arguments:
#   ser - Serial interface
#   remote - (hex string) 64-bit remote node address
#   period- (int) Sampling period 
def remote_period(ser,remote,period):
  success = 0

  # Arguments check
  if len(remote) != 16:
    print('Invalid remote node address')
    return success
  if (period > 65535) | (period < 0):
    print('Invalid period')
    return 0

  remote_b = mf.hexstr2byte(remote)

  if period != 0:
    bytestr = pe.start_sensing(period,remote_b)
  else:
    bytestr = pe.start_sensing_ret(remote_b)

  bytestr = pe.debug_period(period,remote_b)
  ser.write(bytestr)
    
  payload = b'\x00'
  while payload[0] != 0x8b:
    success, payload = pd.rxpacket_buffered(ser)
    if payload == b'':
      print('Serial timeout')
      return 0
    if success == 0:
      print('Error receiving response from Transmit request')
      return success
    if payload[0] == 0x8b:
      error = pd.decode_txstat(payload)
      if error == 1:
        print('Error reported by Transmit status')
        return 0

  print('Remote {} period now set to {}'.format(remote,period))
  success = 1
  return success

# Set AT parameter
def remote_at(ser,remote,atparam,valhex):
 
  success = 0;

  # Arguments check
  if len(remote) != 16:
    print('Invalid remote node address')
    return success
  if len(atparam) != 2:
    print('Invalid AT parameter')
    return success

  remote_b = mf.hexstr2byte(remote)
  val_b = mf.hexstr2byte(valhex)

  at_dict = {
    'PL' : b'DPL',
    'CH' : b'DCH',
    'MR' : b'DMR',
    'NH' : b'DNH'
  }

  data_b = at_dict[atparam] + val_b
  payload = pe.gen_txreq('01',mf.hexstr(remote_b),'00','00',mf.hexstr(data_b))
  bytestr = pe.gen_headtail(payload)
  ser.write(bytestr)

  payload = b'\x00'
  while payload[0] != 0x8b:
    success, payload = pd.rxpacket_buffered(ser)
    if payload == b'':
      print('Serial timeout')
      return 0
    if success == 0:
      print('Error receiving response from Transmit request')
      return success
    if payload[0] == 0x8b:
      error = pd.decode_txstat(payload)
      if error == 1:
        print('Error reported by Transmit status')
        return 0

  print('Remote {} AT parameter {} now set to {}'.format(remote,atparam,valhex))
  success = 1
  return success

# Change maximum retries
# Arguments:
#   ret - (int) Max retries
def remote_retries(ser,remote,ret):
  if (ret < 0) | (ret > 7):
    print('Invalid parameter value')
     return 0 

  ret_b = (ret).to_bytes(1,'big')
  rethex = mf.hexstr(ret_b)
  success = remote_at(ser,remote,'MR',rethex)
  return success

# Change maximum hops
# Arguments:
#   hops - (int) Max hops
def remote_hops(ser,remote,hops):
  if (hops < 1) | (hops > 32):
    print('Invalid parameter value')
    return 0 

  hops_b = (hops).to_bytes(1,'big')
  hopshex = mf.hexstr(hops_b)
  success = remote_at(ser,remote,'NH',hopshex)
  return success

# Check local XBee address
def local_addr(ser):
  bytestr = pe.atcom_query('SH')
  ser.write(bytestr)
  success, payload = pd.rxpacket(ser)
  addr_hi = payload[5:]

  bytestr = pe.atcom_query('SL')
  ser.write(bytestr)
  success, payload = pd.rxpacket(ser)
  addr_lo = payload[5:]

  addr = mf.hexstr(addr_hi) + mf.hexstr(addr_lo)

  print('Local address: 0x{}'.format(addr))

  return addr

# Check local XBee channel
def local_ch(ser):
  bytestr = pe.atcom_query('CH')
  ser.write(bytestr)
  success, payload = pd.rxpacket(ser)
  channel = int('0x'+payload[5:],0)

  print('Local channel: 0x{}'.format(channel))

  return(channel) 

