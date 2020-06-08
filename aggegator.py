import argparse
import misc_func as mf
import packet_decode as pd
import packet_encode as pe
import command_api as c
from datetime import datetime

# Parser
parser = argparse.ArgumentParser()

parser.add_argument("channel", help="Channel (integer)")
parser.add_argument("-d", "--device", help="Serial device")
parser.add_argument("-o", "--outputfile", help="Output log file")

args = parser.parse_args()

if args.device:
  dev = args.device
else:
  dev = '/dev/ttyUSB0'

if args.outputfile:
  outputfile = args.outputfile
else:
  outputfile = '/var/log/aggregator.log'

ch = int(args.channel)

# Configure UART
try:
  ser = c.config_notimeout(dev, 4, ch)
  print('\nConfiguring XBee in {} to channel {}'.format(dev,ch))
except:
  print('\nUART XBee configuration error')
  quit()

# Display XBee address
try:
  c.local_addr(ser)
  print('\n')
except:
  print('Error getting XBee address')
  quit()

# Listen

while 1:

  success, payload = pd.rxpacket(ser)
  print(mf.hexstr(payload))
  src, data = pd.decode_payload(payload,suppress=1)
  fields = pd.parse_data(data)
  parsed = 'src, 0x' + src
  for item in fields:
    parsed = parsed + ', {}, {}'.format(item,fields[item]) 
  print(parsed)
  print('***')
