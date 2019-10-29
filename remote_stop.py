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
parser.add_argument("-p", "--portusb", help="USB Serial port number")

args = parser.parse_args()

if args.channel:
  ch = mf.hexstr2byte(args.channel)
else:
  ch = b'\x1a'

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
print('** Step 3. Sending stop command **')
tx_packet = pe.stop_sensing(remote)
ser.write(tx_packet)

# Number of packets to receive and decode before sending another stop signal
timeout = 10
timer = 0
while(1):
  status, payload = pd.rxpacket(ser)
  success = pd.decode_stopack(payload,remote)
  print('Success {}'.format(success))
  if success == 1:
    quit()
  timer = timer + 1
  if timer > timeout:
    ser.write(tx_packet)
