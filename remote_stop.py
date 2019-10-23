# Send stop signal
# Arguments
# - node address
# - channel

import argparse
import misc_func as mf
import cmdtest as c
import packet_decode as pd
import packet_encode as pe

## Parse arguments
parser = argparse.ArgumentParser()

parser.add_argument("nodeaddr", help="Node address (8 byte hex str)")
parser.add_argument("-c", "--channel", help="Channel (1 byte hex str)")

args = parser.parse_args()

if args.channel:
  ch = mf.hexstr2byte(args.channel)
else:
  ch = b'\x1a'

## Configure UART
print('** Step 1. Configuring local UART **')
ser = c.cmdtest_uartsetup()
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
print('** Step 3. Sending stop command **')
tx_packet = pe.stop_sensing(remote)
ser.write(tx_packet)
status, payload = pd.rxpacket(ser)
pd.decode_payload(payload)
