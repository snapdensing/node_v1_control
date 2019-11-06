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
def remote_start(ser,remote,period):
  success = 0

  if period > 255:
    print('Invalid period')
    return 0
  remote_b = mf.hexstr2byte(remote)

  bytestr = pe.start_sensing(period,remote_b)
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
            print('Remote node {} started'.format(remote)) 
            return 1

      success = 0

# Set channel

# Set node ID
def remote_nodeid(ser,remote,id):
  success = 0
  maxlen = 20

  length = len(id)
  if length > maxlen:
    print('Exceeded maximum node ID length')
    return 0
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
    return 0
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


