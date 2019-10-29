# Send Change Aggregator address 
# Arguments
# - node address
# - channel
# - new aggregator address

import argparse
import misc_func as mf
import cmdtest as c
import packet_decode as pd
import packet_encode as pe

## Parse arguments
parser = argparse.ArgumentParser()

parser.add_argument("nodeaddr", help="Node address (8 byte hex str)")
parser.add_argument("-c", "--channel", help="Channel (1 byte hex str)")
parser.add_argument("-a", "--aggre", help="New aggregator (8 byte hex str)")
parser.add_argument("-p", "--portusb", help="USB serial port")

args = parser.parse_args()

if args.channel:
  ch = mf.hexstr2byte(args.channel)
else:
  ch = b'\x1a'

if args.aggre:
  aggre_addr = args.aggre
else:
  aggre_addr = '0013a200409a0a81'

if args.portusb:
  dev = int(args.portusb)
else:
  dev = 0

## Configure UART
print('** Step 1. Configuring local UART **')
ser = c.cmdtest_uartsetup(dev)
remote = c.cmdtest_addrconv(args.nodeaddr)

## Set channel
print('** Step 2. Setting local channel to 0x{} **'.format(mf.hexstr(ch)))
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

tx_packet = pe.atcom_set('CH',ch)
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

## Send stop command
print('** Step 3. Sending Set Address (DA): 0x{} **'.format(aggre_addr))
msg = mf.hexstr(b'DA') + aggre_addr 
tx_packet = pe.msgformer(msg,remote)
ser.write(tx_packet)
status, payload = pd.rxpacket(ser)
pd.decode_payload(payload)
