# configure_remote.py
# Configuration script for nodes
# Arguments:
# - node address
# - old channel
# - new channel

import argparse
import misc_func as mf
import cmdtest as c
import packet_encode as pe
import packet_decode as pd

## Parse arguments
parser = argparse.ArgumentParser()

parser.add_argument("nodeaddr", help="Node address (64-bit)")
parser.add_argument("-oc", "--oldchannel", help="Old channel (1 byte hex str)")
parser.add_argument("-nc", "--newchannel", help="New channel (1 byte hex str)")

args = parser.parse_args()

print('Target node: 0x{}'.format(args.nodeaddr))

if args.oldchannel:
  ch_old = mf.hexstr2byte(args.oldchannel)
else:
  ch_old = b'\x0c'

if args.newchannel:
  ch_new = mf.hexstr2byte(args.newchannel)
else:
  ch_new = b'\x1a'

print('-- Switching channel from 0x{} to 0x{}'.format(mf.hexstr(ch_old),mf.hexstr(ch_new))) 
print(' ')

## Configure UART
print('** Step 1. Configuring local UART **')
ser = c.cmdtest_uartsetup(0)
remote = c.cmdtest_addrconv(args.nodeaddr)
print(' ')

## Set local channel to old channel
print('** Step 2. Setting local channel to 0x{} **'.format(mf.hexstr(ch_old)))
tx_packet = pe.atcom_query('CH')
ser.write(tx_packet)
status, payload = pd.rxpacket(ser)
if status != 1:
  print('-- Error receiving internal packet (atcom_query)')
  quit()
status = pd.decode_payload(payload)
if status != 0:
  print('-- Error decoding internal packet (atcom_query)')
  quit()

tx_packet = pe.atcom_set('CH',ch_old)
ser.write(tx_packet)
status, payload = pd.rxpacket(ser)
status = pd.decode_payload(payload)
if status != 0:
  print('-- Error setting AT parameter CH')
  quit()

tx_packet = pe.atcom_query('CH')
ser.write(tx_packet)
status, payload = pd.rxpacket(ser)
if status != 1:
  print('-- Error receiving internal packet (atcom_query)')
  quit()
status = pd.decode_payload(payload)
if status != 0:
  print('-- Error decoding internal packet (atcom_query)')
  quit()
print(' ')

## Query remote PL, terminate if not found
print('** Step 3. Query remote node to check if present **')
tx_packet = pe.debug_query('PL',remote)
ser.write(tx_packet)
status, payload = pd.rxpacket(ser)
status = pd.decode_payload(payload)
if status !=0:
  print('-- Error transmitting remote query')
  quit()
status, payload = pd.rxpacket(ser)
status = pd.decode_payload(payload)
print(' ')

# Set remote channel to new channel
print('** Step 4. Set remote node to new channel **')
tx_packet = pe.debug_channel(ch_new,remote)
print('tx_packet: {}'.format(mf.hexstr(tx_packet)))
ser.write(tx_packet)
status, payload = pd.rxpacket(ser)
status = pd.decode_payload(payload)
if status !=0:
  print('-- Error transmitting remote set channel')
  quit()
print(' ')

# Set local channel to new channel
print('** Step 5. Setting local channel to 0x{} (target)**'.format(mf.hexstr(ch_new)))
tx_packet = pe.atcom_query('CH')
ser.write(tx_packet)
status, payload = pd.rxpacket(ser)
if status != 1:
  print('-- Error receiving internal packet (atcom_query)')
  quit()
status = pd.decode_payload(payload)
if status != 0:
  print('-- Error decoding internal packet (atcom_query)')
  quit()

tx_packet = pe.atcom_set('CH',ch_new)
ser.write(tx_packet)
status, payload = pd.rxpacket(ser)
status = pd.decode_payload(payload)
if status != 0:
  print('-- Error setting AT parameter CH')
  quit()

tx_packet = pe.atcom_query('CH')
ser.write(tx_packet)
status, payload = pd.rxpacket(ser)
if status != 1:
  print('-- Error receiving internal packet (atcom_query)')
  quit()
status = pd.decode_payload(payload)
if status != 0:
  print('-- Error decoding internal packet (atcom_query)')
  quit()
print(' ')

# Query remote PL to confirm channel change
print('** Step 6. Query remote node to check if present (in target)**')
tx_packet = pe.debug_query('PL',remote)
ser.write(tx_packet)
status, payload = pd.rxpacket(ser)
status = pd.decode_payload(payload)
if status !=0:
  print('-- Error transmitting remote query')
  quit()
status, payload = pd.rxpacket(ser)
status = pd.decode_payload(payload)
print(' ')

print('Remote node 0x{} is now on channel 0x{}'.format(args.nodeaddr,args.newchannel))

ser.close()
