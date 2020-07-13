import argparse
import status_func as s

# Configuration variables
refresh_interval = '5m'
gspread_creds = './gsheets/gspread_credentials.json'
gspread_key = '1CyLKDCl3noYfy95CFcEfl-R1kQ_MnxuK1gpcpCrXyVU'
gspread_worksheet = 'Monitor'

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("nodelist", help="File containing list of nodes and addresses")
args = parser.parse_args()

# Read file
try:
  init_list = {}
  fp = open(args.nodelist,'r')
  for line in fp:
    # remove newline
    x = line.split() 
    # separate fields
    y = x[0].split(',')

    # init_list dictionary
    # key - address
    # value - name/ID
    init_list[y[1].upper()] = y[0]

  fp.close()

except:
  print('Error reading file')
  quit()

# Initialize spreadsheet
worksheet = s.openWorksheet(gspread_key,gspread_creds,gspread_worksheet)
data = [None for item in init_list]
header = ['Name', 'Address', 'Status']
worksheet.update('A2',[header])

i = 0
for item in init_list:
  data[i] = [init_list[item], item]
  i = i + 1
worksheet.update('A3',data)

# Get Sensing nodes from REST API
try:
  nodes_sensing = s.getSensingRest(refresh_interval)
except:
  print('Error getting data from REST API')

print(nodes_sensing)

# Update spreadsheet with REST API results
for item in nodes_sensing:
  if item in init_list:
    s.findUpdate(worksheet, nodes_sensing[item], item, 'Sensing')
  else:
    print('Node found sensing is not in initial list 0x{}'.format(
      item))
