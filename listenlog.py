# Configure XBee to listen for transmissions
# Arguments:
# - output log file
# - channel

import argparse
import misc_func as mf
import cmdtest as c
import packet_decode as pd
import packet_encode as pe
from datetime import datetime

## Parse arguments
parser = argparse.ArgumentParser()

parser.add_argument("logfile", help="Log file")
parser.add_argument("-c", "--channel", help="Channel (1 byte hex str)")

args = parser.parse_args()

logfile = args.logfile

if args.channel:
  ch = mf.hexstr2byte(args.channel)
else:
  ch = mf.hexstr2byte('1a')

print('Listening to channel 0x{}'.format(ch))

## Configure UART
print('** Step 1. Configuring local UART **')
ser = c.cmdtest_uartsetup(0)

## Set local channel 
print('** Step 2. Setting local channel to 0x{} **'.format(args.channel))
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
newdir_flag = 0
now = datetime.now()
filename = logfile + '-' + str(now.year) + '-' + str(now.month) + '-' + str(now.day) + '-' + str(now.hour) + '-' + str(now.minute) + '.log'

while 1:

  now = datetime.now()
  if newdir_flag == 0:
    if (now.hour==0) & (now.minute==0):
      newdir_flag = 1
      #filename = logfile + '-' + str(now.year) + '-' + str(now.month) + '-' + str(now.day) + '-' + str(now.hour) + '-' + str(now.minute) + '.log'
      filename = logfile + '-' + str(now.year) + '-' + str(now.month) + '-' + str(now.day) + '-' + str(now.hour) + '-' + '00' + '.log'
  else: 
    if (now.hour==0) & (now.minute==1):
      newdir_flag = 0

  fp = open(filename,"a")
  status, payload = pd.rxpacket(ser)
  pd.decodelog_payload(fp,payload)
  fp.close()
