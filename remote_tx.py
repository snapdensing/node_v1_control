# Send arbitrary message to remote
# Arguments
# - node address
# - message
# - channel

import argparse
import misc_func as mf
import cmdtest as c
import packet_decode as pd
import packet_encode as pe
#from datetime import datetime
#from datetime import timedelta
import time

## Parse arguments
parser = argparse.ArgumentParser()

parser.add_argument("nodeaddr", help="Node address (8 byte hex str)")
parser.add_argument("-c", "--channel", help="Channel (1 byte hex str)")
parser.add_argument("-m", "--message", help="Message (hex str)")
parser.add_argument("-n", "--numtx", help="Number of transmissions")
parser.add_argument("-d", "--delay", help="Delay in seconds")

args = parser.parse_args()

if args.channel:
  ch = mf.hexstr2byte(args.channel)
else:
  ch = b'\x1a'

if args.message: 
  if (len(args.message)%2) != 0:
    print('Invalid message')
    quit()
  message = args.message
else:
  message = mf.hexstr(b'DefaultMessage')

if args.numtx:
  n = int(args.numtx)
else:
  n = 1

if args.delay:
  d = int(args.delay)
else:
  d = 1

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

# Send message
print('** Step 3. Sending message to 0x{} **'.format(args.nodeaddr))
for i in range(n):
  #time_stop = datetime.now() + timedelta(seconds=5)
  #print('time stop {}'.format(time_stop))
  tx_packet = pe.msgformer(message,remote)
  ser.write(tx_packet)
  status, payload = pd.rxpacket(ser)
  pd.decode_payload(payload)
  #while (time_stop > datetime.now()):
  #  print('now {}'.format(datetime.now()))
  time.sleep(d)

