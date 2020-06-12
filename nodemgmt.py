#!/usr/bin/python3
import command_api as c

# Initialize XBee command node
def initcmd(dev,channel):
  ser = c.config(dev,4,channel)
  return ser

def parseAggre(payload):

  if len(payload) != 20:
    print('Invalid payload')
    return 'Error'
  elif payload[0:2] != '5141':
    print('Invalid payload')
    return 'Error'
  else:
    return payload[2:]

# Sensor node object
# On creation, must declare:
# - name - string for unique identifier
# - addr - 64-bit hex string for XBee address
class node:

  def __init__(self, name, addr):
    self.name = name
    self.addr = addr
    self.channel = 12
    self.aggre = '0013a200409a0a81'
    self.txperiod = 10
    self.loc = 'noloc'

  def ping(self,ser):
    data = c.remote_query(ser,self.addr,'A')
    print('Aggregator: {}'.format(parseAggre(data)))

  def getAggre(self,ser):
    pass

  def getPeriod(self,ser):
    pass

def parseAggre(payload):

  if len(payload) != 20:
    print('Invalid payload: length')
    return 'Error'
  elif payload[0:4] != '5141':
    print('Invalid payload: header')
    return 'Error'
  else:
    return payload[2:]
