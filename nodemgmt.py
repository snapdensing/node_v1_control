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
    self.loc = None
    self.lastping = None
    self.lastcommit = None
    self.txpower = None
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
        parsed = parseAggre(payload)
        if parsed == 'Error':
          raise Exception('Error parsing payload')

        self.aggre = parsed
        self.lastping = datetime.now()
        self.status = 'Idle'
 
        if self.logfile != None:
          logAction(self.logfile,'Node {} getAggre()'.format(self.name))
          logAction(self.logfile,'Response: {}'.format(self.aggre))

        return self.aggre

      except:
        #print('Error getting aggregator address')
        response = 'Error getting aggregator address'
        print(response)

        if self.logfile != None:
          logAction(self.logfile,'Node {} getAggre()'.format(self.name))
          logAction(self.logfile,'Response: {}'.format(response))

        return None

  def getPeriod(self,ser):
    if self.status == 'Sensing':
      print('Cannot send query. Node is sensing')
      return None
    else:
      payload = c.remote_query(ser,self.addr,'T')

      try:
        parsed = parsePeriod(payload)
        if parsed == 'Error':
          raise Exception('Error parsing payload')

        self.txperiod = parsed
        self.lastping = datetime.now()
        self.status = 'Idle'

        if self.logfile != None:
          logAction(self.logfile,'Node {} getPeriod()'.format(self.name))
          logAction(self.logfile,'Response: {}'.format(self.txperiod))

        return self.txperiod

      except:
        #print('Error getting transmit period')
        response = 'Error getting transmit period'
        print(response)
        if self.logfile != None:
          logAction(self.logfile,'Node {} getPeriod()'.format(self.name))
          logAction(self.logfile,'Response: {}'.format(response))

        return None

  # Class function for querying remote node's power
  # Nodes with firmware version 1.7.2 should set old parameter to True
  # - i.e. node0.getPower(ser,old=True)
  def getPower(self,ser,**kwargs):

    # Backwards compatibility for firmware 1.7.2 and prior
    oldquery = kwargs.get('old',False)

    if self.status == 'Sensing':
      print('Cannot send query. Node is sensing')
      return None
    else:
      if oldquery == False:
        payload = c.remote_query(ser,self.addr,'PL')
      else:
        payload = c.remote_query(ser,self.addr,'P')

      try:
        parsed = parsePower(payload)
        if parsed == 'Error':
          raise Exception('Error parsing payload')

        self.lastping = datetime.now()
        self.status = 'Idle'
        self.txpower = parsed

        if self.logfile != None:
          logAction(self.logfile,'Node {} getPower()'.format(self.name))
          logAction(self.logfile,'Response: {}'.format(self.txpower))

        return self.txpower

      except:
        response = 'Error getting transmit power'
        print(response)
        if self.logfile != None:
          logAction(self.logfile,'Node {} getPower()'.format(self.name))
          logAction(self.logfile,'Response: {}'.format(response))

        return None

  def getVersion(self,ser):
    if self.status == 'Sensing':
      print('Cannot send query. Node is sensing')
      return None
    else:
      payload = c.remote_query(ser,self.addr,'V')

      try:
        parsed = parseVersion(payload)
        if parsed == 'Error':
          raise Exception('Error parsing payload')

        self.lastping = datetime.now()
        self.status = 'Idle'
        self.ver = parsed

        if self.logfile != None:
          logAction(self.logfile,'Node {} getVersion()'.format(self.name))
          logAction(self.logfile,'Response: {}'.format(self.ver))

        return self.ver

      except:
        #print('Error getting transmit period')
        response = 'Error getting firmware version'
        if self.logfile != None:
          logAction(self.logfile,'Node {} getVersion()'.format(self.name))
          logAction(self.logfile,'Response: {}'.format(response))

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

        if self.logfile != None:
          logAction(self.logfile,'Node {} started'.format(self.name))

      else:
        print('Error sending START command')

        if self.logfile != None:
          logAction(self.logfile,'Error starting Node {}'.format(self.name))

  def stop(self,ser):
    if self.status == 'Idle':
      print('Node already idle')
    else:
      success = c.remote_stop(ser,self.addr)
      if success == 1:
        self.status = 'Idle'
        self.lastping = datetime.now()

        if self.logfile != None:
          logAction(self.logfile,'Node {} stopped'.format(self.name))

      else:
        print('Error sending STOP command')         

        if self.logfile != None:
          logAction(self.logfile,'Error stopping Node {}'.format(self.name))
          
  def setAggre(self,ser,aggre):
    if self.status == 'Sensing':
      print('Cannot send command. Node is sensing')
    else:
      success = c.remote_aggre(ser,self.addr,aggre)
      if success == 1:
        self.lastping = datetime.now()
        self.aggre = aggre

        if self.logfile != None:
          logAction(self.logfile,'Node {} aggregator set to 0x{}'.format(
            self.name,self.aggre))

      else:
        print('Error setting node {}\'s aggregator'.format(self.name))

        if self.logfile != None:
          logAction(self.logfile,'Error setting node {}\'s aggregator'.
              format(self.name))

  def setPeriod(self,ser,period):
    pass

  def setPower(self,ser,power):
    if self.status == 'Sensing':
      print('Cannot send command. Node is sensing')
    else:
      success = c.remote_power(ser,self.addr,power)
      if success == 1:
        self.lastping = datetime.now()
        self.txpower = power

        if self.logfile != None:
          logAction(self.logfile,'Node {} power set to 0x{}'.format(
            self.name,self.txpower))

      else:
        msg = 'Error setting node {}\'s power'.format(self.name)
        print(msg)

        if self.logfile != None:
          logAction(self.logfile,msg)

  def commitSetting(self,ser):
    if self.status == 'Sensing':
      print('Cannot send command. Node is sensing')
    else:
      payload = c.remote_query(ser,self.addr,'WR')

      try:
        success = parseCommit(payload)

        if success == True:
          self.lastping = datetime.now()
          self.status = 'Idle'
      
          if self.logfile != None:
            logAction(self.logfile,'Node {} settings committed to flash'.format(
              self.name))

        else:
          msg = 'Error committing node {}\'s settings to flash'.format(
              self.name)
          print(msg)

          if self.logfile != None:
            logAction(self.logfile,msg)

      except:
        msg = 'Error commiting node {}\'s settings to flash'.format(self.name)
        print(msg)

        if self.logfile != None:
          logAction(self.logfile,msg)


  def getIDLoc(self,ser):
    pass

  def setIDLoc(self,ser,name,loc):
    if self.status == 'Sensing':
      print('Cannot send command. Node is sensing')
    else:

      # Set ID/Name
      success = c.remote_nodeid(ser,self.addr,name)
      if success == 1:
        self.lastping = datetime.now()
        self.name = name

        if self.logfile != None:
          logAction(self.logfile,'Node 0x{}\'s ID changed to {}'.format(
            self.addr,self.name))

        # Set Loc
        success = c.remote_nodeloc(ser,self.addr,loc)
        if success == 1:
          self.lastping = datetime.now()
          self.loc = loc

          if self.logfile != None:
            logAction(self.logfile,'Node {}\'s loc changed to {}'.format(
              self.name,self.loc))

        else:
          msg = 'Error change node {}\'s loc'.format(self.name)
          print(msg)

          if self.logfile != None:
            logAction(self.logfile,msg)

      else:
        msg = 'Error changing node 0x{}\'s ID'.format(self.addr)
        print(msg)

        if self.logfile != None:
          logAction(self.logfile,msg)


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
  
# Parse Power from Query reply
def parsePower(payload):

  if len(payload) != 8:
    print('Invalid payload: length')
    return 'Error'
  elif payload[0:6] != '51504c':
    print('Invalid payload: header')
    return 'Error'
  else:
    return int('0x'+payload[6:],0)

# Parse Version from Query reply
def parseVersion(payload):

  if payload[0:4] != '5156':
    print('Invalid payload: header')
    return 'Error'
  else:
    bytestr = mf.hexstr2byte(payload[4:])
    return bytestr.decode('utf-8')

# Parse commit from Query reply
def parseCommit(payload):

  if payload[0:6] != '515752':
    print('Invalid payload: header')
    return False
  else:
    return True

# Log action to file
def logAction(logfile,msg):
  now = datetime.now()
  fp = open(logfile,'a+')
  line = str(now) + ': ' + msg + '\n'
  fp.write(line)
  fp.close()
