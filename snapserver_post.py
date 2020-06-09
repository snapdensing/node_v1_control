import argparse
from datetime import datetime
from misc_func import hexstr2byte

# Function for getting last N lines
# from: https://www.geeksforgeeks.org/python-reading-last-n-lines-of-a-file/
def LastNlines(fname,N):
  assert N >= 0
  pos = N + 1
  lines = []
  with open(fname) as f:
    while len(lines) <= N:
      try:
        f.seek(-pos, 2)
      except IOError:
        f.seek(0) 
        break
      finally:
        lines = list(f)
      pos *= 2

  return lines[-N:]

# Function for processing fields
def processFields(entry):

   # DHT22 temperature 
   if 'temp_dht22' in entry:
     temp_raw = entry['temp_dht22']
     temp_parsed = temp_raw.split('x')
     temp_int = int.from_bytes(hexstr2byte(temp_parsed[1]),byteorder='big')
     # extract sign
     if temp_int > 32767:
       sign = -1.0
       temp_int = temp_int & 32767
     else:
       sign = 1.0
     temp = temp_int/10.0
     temp = temp*sign
     entry['temp_dht22'] = temp

   # DHT22 RH 
   if 'rh_dht22' in entry:
     rh_raw = entry['rh_dht22']
     rh_parsed = rh_raw.split('x')
     rh_int = int.from_bytes(hexstr2byte(rh_parsed[1]),byteorder='big')
     rh = rh_int/10.0
     entry['rh_dht22'] = rh 


# Parser
parser = argparse.ArgumentParser()

#parser.add_argument("srclog", help="source logfile")
parser.add_argument("-s", "--srclog", help="source logfile")

args = parser.parse_args()

# Default source log file
if args.srclog:
  srclog = args.srclog
else:
  srclog = '/var/log/aggregator.log'

# Get tail of srclog
lines = LastNlines(srclog,1)
tail = lines[0][:-1]
fields = tail.split(', ')

# Dictionary of last entry
entry = {} 

# Extract timestamp
entry['ts'] = datetime.strptime(fields[0],'%Y-%m-%d %H:%M:%S')
fields = fields[1:]

# Extract remaining fields
while len(fields) != 0:

  entry[fields[0]] = fields[1]
  fields = fields[2:]

print(entry)
processFields(entry)
print(entry)
