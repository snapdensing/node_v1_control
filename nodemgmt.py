#!/usr/bin/python3
import command_api as c
from datetime import datetime

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
    self.lastping = None
    self.lastcommit = None

  def ping(self,ser):
    data = c.remote_query(ser,self.addr,'A')
    try:
      print('Aggregator: {}'.format(parseAggre(data)))
      self.lastping = datetime.now()
    except:
      print('Error pinging node')
      return None

  def getAggre(self,ser):
    payload = c.remote_query(ser,self.addr,'A')
    try:
      self.lastping = datetime.now()
      return parseAggre(payload)
    except:
      print('Error getting aggregator address')
      return None

  def getPeriod(self,ser):
    payload = c.remote_query(ser,self.addr,'T')
    try:
      self.lastping = datetime.now()
      return parsePeriod(payload)
    except:
      print('Error getting transmit period')
      return None

# Parse Aggregator address from Query reply
def parseAggre(payload):

  if len(payload) != 20:
    print('Invalid payload: length')
    return 'Error'
  elif payload[0:4] != '5141':
    print('Invalid payload: header')
    return 'Error'
  else:
    return payload[2:]

# Parse Period from Query reply
def parsePeriod(payload):

  if not ((len(payload) == 6) | (len(payload) == 8)):
    print('Invalid payload: length')
    return 'Error'
  elif payload[0:4] != '5154':
    print('Invalid payload: header')
    return 'Error'
  else:
    return int('0x'+payload[4:],0)
