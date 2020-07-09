import requests
import gspread
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import nodemgmt as n

# Request Rest API for all nodes in the last 10 minutes
r = requests.get('http://122.53.116.119/api-v0_5/aggregator/2/nodes/10m')

print(r.status_code)
print(r.headers['content-type'])
print(r.encoding)

x = r.json()

# Aggregator ID
print('Aggregator ID: {}'.format(x['aggregator_id']))

# length
print('Length: {}'.format(x['length']))

# Results
res_list = x['results']

# Dictionary for Nodes
nodes_dict = {}

# Parse initial results to populate nodes_dict
# node_id is key, value is node object
for item in res_list:
  nodes_dict[item['node_id']] = n.node(item['node_id'],item['node_mac'])

# Set all parsed nodes to sensing
for item in nodes_dict:
  nodes_dict[item].status = 'Sensing'

# Display initial
print('Initialization Results')
for item in nodes_dict:
  print('Node {}, Addr {}, Status {}'.format(item,nodes_dict[item].addr,
    nodes_dict[item].status))
print('')

# Scheduler Job
def job_function(nodes_dict):

  now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  r = requests.get('http://122.53.116.119/api-v0_5/aggregator/2/nodes/5m')
  x = r.json()
  res_list = x['results']

  # Reset status to 'Unknown'
  for item in nodes_dict:
    nodes_dict[item].status = 'Unknown'

  # Update status based on new request
  for item in res_list:
    nodes_dict[item['node_id']].status = 'Sensing'

  print('Updated {}'.format(now))
  print_nodes(nodes_dict)
  update_sheets(nodes_dict,now)

# Function for printing status
def print_nodes(nodes_dict):
  for item in nodes_dict:
    print('Node {}, Addr {}, Status {}'.format(item,nodes_dict[item].addr,
      nodes_dict[item].status))
  print('')

# Function for updating gsheets
def update_sheets(nodes_dict,now):

  gc = gspread.service_account(filename='./gsheets/gspread_credentials.json')
  sh = gc.open_by_key('1CyLKDCl3noYfy95CFcEfl-R1kQ_MnxuK1gpcpCrXyVU')
  worksheet = sh.worksheet('Status(testing)')

  values_list = [None for item in nodes_dict]
  row = 0
  for item in nodes_dict:
    values = [item, nodes_dict[item].addr, nodes_dict[item].status]
    values_list[row] = values
    row = row + 1

  worksheet.update('A1',[['Updated', now]])
  worksheet.update('A2',values_list)

# Scheduler Run
sched = BlockingScheduler()
#sched.add_job(job_function, 'cron', second='0,10,20,30,40,50', 
sched.add_job(job_function, 'cron', minute='5,10,15,20,25,30,35,40,45,50,55', 
  args=[nodes_dict])
sched.start()
