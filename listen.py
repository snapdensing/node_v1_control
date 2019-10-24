# Configure XBee to listen for transmissions
# Arguments:
# - channel

import argparse
import misc_func as mf
import cmdtest as c
import packet_decode as pd
import packet_encode as pe
from datetime import datetime

## Parse arguments
parser = argparse.ArgumentParser()

parser.add_argument("channel", help="Channel (1 byte hex str)")

args = parser.parse_args()

print('Listening to channel 0x{}'.format(args.channel))

## Configure UART
print('** Step 1. Configuring local UART **')
ser = c.cmdtest_uartsetup(0)

## Set local channel channel
print('** Step 2. Setting local channel to 0x{} **'.format(args.channel))
ch = mf.hexstr2byte(args.channel)
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

## Listen
#c.cmdtest_listen(ser)
while 1:
  status, payload = pd.rxpacket(ser)
  print(datetime.now())
  print('Payload: {}'.format(mf.hexstr(payload))) 
  status = pd.decode_payload(payload)
  print('-----')
