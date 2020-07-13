import requests
import gspread
from datetime import datetime
import nodemgmt as n

# Use RestAPI to get list of sensing nodes
# Arguments:
# - interval - (string) Interval for Rest API (ex. '5m', '1h')
# Return:
# - nodes_dict - dictionary of node names/ID keyed by node address
def getSensingRest(interval):

  base_url = 'http://122.53.116.119/api-v0_5/aggregator/2/nodes/'
  url = base_url + interval
  print(url)

  # Request
  r = requests.get(url)
  x = r.json()

  # Node list
  nodes_list = x['results']

  # Node dictionary
  # key: name
  # value: address
  nodes_dict = {}
  for item in nodes_list:
    nodes_dict[item['node_mac']] = item['node_id']

  return nodes_dict

# Open google sheet worksheet
# Arguments:
# - key - Google sheet URL id
# - creds - JSON file for credentials
# - worksheet - (String) Worksheet name
# Returns:
# - wkst - gspread worksheet object
def openWorksheet(key,creds,worksheet):

  gc = gspread.service_account(filename=creds)
  sh = gc.open_by_key(key)
  wkst = sh.worksheet(worksheet)

  return wkst

# Find node in worksheet and update status
# Arguments:
# - wkst - gspread worksheet object
# - name - (String) node name (ID)
# - addr - (String) Node address in hexadecimal
# - status - (String) Status value to be used 
def findUpdate(wkst,name,addr,status):

  addr_cell = wkst.find(addr)
  #print(addr_cell)
  row = addr_cell.row
  col = addr_cell.col
  #print(addr_cell.value)

  # Read adjacent cell (addr field)
  name_cell = wkst.cell(row, col-1)
  print(name_cell.value)

  # Update status
  # Check if name in spreadsheet corresponds to supplied name
  if name_cell.value == name:
    wkst.update_cell(row, col+1, status)
    print('Node {} status updated to {}'.format(name_cell.value,
      status))
