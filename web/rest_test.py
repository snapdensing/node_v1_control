import requests

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
  #nodes_dict[item['node_id']] = item['node_mac']
  nodes_dict[item['node_id']] = n.node(item['node_id'],item['node_mac'])

