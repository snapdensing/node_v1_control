# Send stop signal
# Arguments
# - node address
# - channel

import serial
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
parser.add_argument("-to","--timeout", help="Max no of serial read timeouts")

args = parser.parse_args()

if args.channel:
  ch = mf.hexstr2byte(args.channel)
else:
  ch = b'\x1a'

if args.portusb:
  dev = int(args.portusb)
else:
  dev = 0

if args.timeout:
  timeout_max = int(args.timeout)
else:
  timeout_max = 5

## Configure UART
print('** Step 1. Configuring local UART **')
#ser = c.cmdtest_uartsetup(port=dev,timeout=5)
device = '/dev/ttyUSB' + str(dev)
ser = serial.Serial(port=device,timeout=5)
remote = c.cmdtest_addrconv(args.nodeaddr)

## Set channel
print('** Step 2. Setting local channel to 0x{} **'.format(mf.hexstr(ch)))
tx_packet = pe.atcom_query('CH')
ser.write(tx_packet)
status, payload = pd.rxpacket_buffered(ser)
if status != 1:
  print('-- Error receiving internal packet (atcom_query)')
  quit()
status = pd.decode_payload(payload)
if status != 0:
  print('-- Error decoding internal packet (atcom_query)')
  quit()

tx_packet = pe.atcom_set('CH',ch)
ser.write(tx_packet)
status, payload = pd.rxpacket_buffered(ser)
status = pd.decode_payload(payload)
if status != 0:
  print('-- Error setting AT parameter CH')
  quit()

tx_packet = pe.atcom_query('CH')
ser.write(tx_packet)
status, payload = pd.rxpacket_buffered(ser)
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

timeouts = 0

while(1):
  status, payload = pd.rxpacket_buffered(ser)
  # If received a packet
  if status == 1:
    success = pd.decode_stopack(payload,remote)
    print('Success {}'.format(success))
    if success == 1:
      quit()

  # Serial read timed out
  else: 
    if timeouts >= timeout_max:
      quit()
    else:
      timeouts = timeouts + 1
      print('Trying again')
      ser.write(tx_packet)
