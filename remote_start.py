# Send start signal
# Arguments
# - node address
# - channel
# - sampling rate

import argparse
import misc_func as mf
import cmdtest as c
import packet_decode as pd
import packet_encode as pe

## Parse arguments
parser = argparse.ArgumentParser()

parser.add_argument("nodeaddr", help="Node address (8 byte hex str)")
parser.add_argument("-c", "--channel", help="Channel (1 byte hex str)")
parser.add_argument("-t", "--period", help="Sampling period (integer)")
parser.add_argument("-p", "--portusb", help="USB Serial port number")

args = parser.parse_args()

if args.channel:
  ch = mf.hexstr2byte(args.channel)
else:
  ch = b'\x1a'

if args.period:
#  period = (int(args.period)).to_bytes(1,'big')
   period = int(args.period)
else:
#  period = b'\x0a'
   period = 10
   print('Running default period')

if args.portusb:
  dev = int(args.portusb)
else:
  dev = 0

## Configure UART
print('** Step 1. Configuring local UART **')
ser = c.cmdtest_uartsetup(0)
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

## Send start command
print('** Step 3. Sending start command **')
tx_packet = pe.start_sensing(period,remote)
ser.write(tx_packet)
status, payload = pd.rxpacket(ser)
pd.decode_payload(payload)
