# Functions for testing XBee using the interactive python terminal

import serial
import packet_decode as pd
import packet_encode as pe
import misc_func as mf

# Configure remote node address
def cmdtest_remoteaddr(sel):
  addr_dict = {
    0 : b'\x00\x13\xa2\x00\x40\xbf\x1f\x4a',
    1 : b'\x00\x13\xa2\x00\x40\x9a\x0a\x81',
    2 : b'\x00\x13\xa2\x00\x40\xbf\x1f\x4b'
  }
  return addr_dict[sel]

# Configure serial
def cmdtest_uartsetup():
  ser = serial.Serial('/dev/ttyUSB0')
  print(ser.name)
  return ser

# Debug Unicast
def cmdtest_remote_unicast(ser,n,dest):
  from packet_encode import debug_unicast
  from packet_decode import rxpacket
  tx_packet = debug_unicast(n,dest)
  print('Tx Packet: {}'.format(mf.hexstr(tx_packet)))
  print('-----')
  ser.write(tx_packet)
  for i in range(n+1):
    status, payload = rxpacket(ser)
    print('Payload: {}'.format(mf.hexstr(payload)))
    status = pd.decode_payload(payload)
    if status != 0:
      print('Aborting listen')
      return 1
    print('-----')
  
# Debug Unicast 2
def cmdtest_remote_unicast2(ser,n,dest):
  from packet_encode import debug_unicast2
  from packet_decode import rxpacket
  tx_packet = debug_unicast2(n,dest)
  print('Tx Packet: {}'.format(mf.hexstr(tx_packet)))
  print('-----')
  ser.write(tx_packet)
  for i in range(n+1):
    status, payload = rxpacket(ser)
    print('Payload: {}'.format(mf.hexstr(payload)))
    pd.decode_payload(payload)
    print('-----')
 

# Local AT Command Set
#   at - AT parameter to set (in string)
#   val - AT parameter value (in bytes)
def cmdtest_local_atset(ser,at,val):
  from packet_encode import atcom_set
  from packet_decode import rxpacket
  tx_packet = atcom_set(at,val) 
  print('Tx Packet: {}'.format(mf.hexstr(tx_packet)))
  print('-----')
  ser.write(tx_packet)
  status, payload = rxpacket(ser)
  print('Payload: {}'.format(mf.hexstr(payload))) 
  pd.decode_payload(payload)
  print('-----')

# Local AT Command Query
#   at - AT parameter to query (in string)
def cmdtest_local_atquery(ser,at):
  from packet_encode import atcom_query
  from packet_decode import rxpacket
  tx_packet = atcom_query(at) 
  print('Tx Packet: {}'.format(mf.hexstr(tx_packet)))
  print('-----')
  ser.write(tx_packet)
  status, payload = rxpacket(ser)
  print('Payload: {}'.format(mf.hexstr(payload))) 
  pd.decode_payload(payload)
  print('-----')

# Remote change channel
#   ch - new channel (in bytes)
#   dest - destination (in bytes)
def cmdtest_remote_setchannel(ser,ch,dest):
  tx_packet = pe.debug_channel(ch,dest)
  print('Tx Packet: {}'.format(mf.hexstr(tx_packet)))
  print('-----')
  ser.write(tx_packet)
  status, payload = pd.rxpacket(ser)
  pd.decode_payload(payload)
  print('-----')

# Remote change power level 
#   pow - new power level (in bytes)
#   dest - destination (in bytes)
def cmdtest_remote_setpower(ser,pow,dest):
  tx_packet = pe.debug_power(pow,dest)
  print('Tx Packet: {}'.format(mf.hexstr(tx_packet)))
  print('-----')
  ser.write(tx_packet)
  status, payload = pd.rxpacket(ser)
  pd.decode_payload(payload)
  print('-----')
  
# Remote start signal
#  period - sampling period (in int)
def cmdtest_remote_start(ser,period,dest):
  tx_packet = pe.start_sensing(period,dest)
  print('Sending start signal')
  print('Tx Packet: {}'.format(mf.hexstr(tx_packet)))
  print('-----')
  ser.write(tx_packet)
  status, payload = pd.rxpacket(ser)
  pd.decode_payload(payload)
  print('-----')

# Listen to transmissions
def cmdtest_listen(ser):
  print('Listening to transmissions')
  print('-----')
  while 1:
    status, payload = pd.rxpacket(ser)
    print('Payload: {}'.format(mf.hexstr(payload)))
    status = pd.decode_payload(payload)
    print('-----')
 
# Remote stop signal
def cmdtest_remote_stop(ser,dest):
  tx_packet = pe.stop_sensing(dest)
  print('Sending stop signal')
  print('Tx Packet: {}'.format(mf.hexstr(tx_packet)))
  print('-----')
  ser.write(tx_packet)
  status, payload = pd.rxpacket(ser)
  pd.decode_payload(payload)
  print('-----')

# Remote change aggregator address
def cmdtest_remote_setaddr(ser,newaddr,dest):
  tx_packet = pe.debug_setaddr(newaddr,dest)
  print('Sending Change aggregator address')
  print('Tx Packet: {}'.format(mf.hexstr(tx_packet)))
  print('-----')
  ser.write(tx_packet)
  status, payload = pd.rxpacket(ser)
  pd.decode_payload(payload)
  print('-----')
