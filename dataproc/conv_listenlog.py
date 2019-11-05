import argparse
import sys

# User-made modules
sys.path.insert(1,'/home/snap/Work/xbee_serial')
import misc_func as mf

# Parser
parser = argparse.ArgumentParser()
parser.add_argument("inputlogfile", help="Input log file")
parser.add_argument("-o", "--outputlogfile", help="Output log file")
args = parser.parse_args()

inputlogfile = args.inputlogfile

if args.outputlogfile:
  outputlogfile = args.outputlogfile
else:
  outputlogfile = 'output.txt'

print('Input file: {}'.format(inputlogfile))
print('Output file: {}'.format(outputlogfile))
