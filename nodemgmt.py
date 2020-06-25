#!/usr/bin/python3
import command_api as c
from datetime import datetime
import misc_func as mf

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

  def __init__(self, name, addr, **kwargs):
    self.name = name
    self.addr = addr
    self.channel = 12
    self.aggre = None
    self.txperiod = None 
    self.loc = 'noloc'
    self.lastping = None
    self.lastcommit = None
    self.status = None
    self.ver = None
    
    self.logfile = kwargs.get('log',None)

    if self.logfile != None:
      logAction(self.logfile,'Node {} (0x{}) created'.format(self.name,
        self.addr))
    

  def ping(self,ser):
    if self.status == 'Sensing':
      print('Cannot send ping. Node is sensing')
    else:
      data = c.remote_query(ser,self.addr,'A')
      try:
        #print('Aggregator: {}'.format(parseAggre(data)))
        response = 'Aggregator: {}'.format(parseAggre(data))
        print(response)
        self.lastping = datetime.now()
        self.status = 'Idle'
        if self.logfile != None:
          logAction(self.logfile,'Node {} ping()'.format(self.name))
          logAction(self.logfile,'Response: {}'.format(response))
      except:
        #print('Error pinging node')
        response = 'Error pinging node'
        print(response)
        
      if self.logfile != None:
        logAction(self.logfile,'Node {} ping()'.format(self.name))
        logAction(self.logfile,'Response: {}'.format(response))
 

  def getAggre(self,ser):
    if self.status == 'Sensing':
      print('Cannot send query. Node is sensing')
      return None
    else:
      payload = c.remote_query(ser,self.addr,'A')
      try:
        self.lastping = datetime.now()
        self.status = 'Idle'
        self.aggre = parseAggre(payload)
        return self.aggre
      except:
        print('Error getting aggregator address')
        return None

  def getPeriod(self,ser):
    if self.status == 'Sensing':
      print('Cannot send query. Node is sensing')
      return None
    else:
      payload = c.remote_query(ser,self.addr,'T')
      try:
        self.lastping = datetime.now()
        self.status = 'Idle'
        self.txperiod = parsePeriod(payload)
        return self.txperiod
      except:
        print('Error getting transmit period')
        return None

  def getVersion(self,ser):
    if self.status == 'Sensing':
      print('Cannot send query. Node is sensing')
      return None
    else:
      payload = c.remote_query(ser,self.addr,'V')
      try:
        self.lastping = datetime.now()
        self.status = 'Idle'
        self.ver = parseVersion(payload)
        return self.ver
      except:
        print('Error getting transmit period')
        return None


  def start(self,ser,**kwargs):
    period = kwargs.get('period',0)

    if self.status == 'Sensing':
      print('Node already sensing')
    else:
      success = c.remote_start(ser,self.addr,period)
      if success == 1:
        self.status = 'Sensing'
        self.lastping = datetime.now()
        if period != 0:
          self.txperiod = period
      else:
        print('Error sending START command')

  def stop(self,ser):
    if self.status == 'Idle':
      print('Node already idle')
    else:
      success = c.remote_stop(ser,self.addr)
      if success == 1:
        self.status = 'Idle'
        self.lastping = datetime.now()
      else:
        print('Error sending STOP command')         
          
  def setAggre(self,ser,aggre):
    if self.status == 'Sensing':
      print('Cannot send command. Node is sensing')
    else:
      success = c.remote_aggre(ser,self.addr,aggre)
      if success == 1:
        self.lastping = datetime.now()
        self.aggre = aggre
      else:
        print('Error setting node {}''s aggregator'.format(self.name))

# Parse Aggregator address from Query reply
def parseAggre(payload):

  if len(payload) != 20:
    print('Invalid payload: length')
    return 'Error'
  elif payload[0:4] != '5141':
    print('Invalid payload: header')
    return 'Error'
  else:
    return payload[4:]

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

# Parse Version from Query reply
def parseVersion(payload):

  if payload[0:4] != '5156':
    print('Invalid payload: header')
    return 'Error'
  else:
    bytestr = mf.hexstr2byte(payload[4:])
    return bytestr.decode('utf-8')

# Log action to file
def logAction(logfile,msg):
  now = datetime.now()
  fp = open(logfile,'a+')
  line = str(now) + ': ' + msg + '\n'
  fp.write(line)
  fp.close()
