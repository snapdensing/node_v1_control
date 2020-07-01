# Node Management

This file documents the functions that can be used for controlling the RESE2NSE node version 1 in nodemgmt.py. It uses an object-oriented approach, associating each node in the WSN with an object.

Contents:

- [Setting up serial connection to XBee](#serialsetup)
- [Node Object](#nodeobject)
- [Node Functions](#nodefunc)
- [Sample Code](#samplecode)

<a name="serialsetup"></a>
## Setting up serial connection to XBee
To setup the serial interface to the XBee that will be used for communicating with your remote nodes, you need to use the `initcmd()` function. 

`ser initcmd(dev,channel)`

Arguments:

- `dev` - (String) Path to serial device (i.e. /dev/ttyUSB0, COM1, etc.)
- `channel` - (Integer) XBee channel

Returns:

- `ser` - Serial object. Will be used by Node Management functions.

<a name="nodeobject"></a>
## Node Object

Each node will be instantiated a node object. This object will store all relevant parameters and settings for a particular node. To instantiate a node, you will need to supply an arbitrary name and its XBee address in hexadecimal. Both arguments are strings. The following code snippet shows an example:
```
import nodemgmt as n
X = n.node('nodeX','0013a20012345678')
```
In the example above, node object X was instantiated to have a name of `nodeX` and address of `0x0013a20012345678'.

### Node Object Properties

Important parameters and settings for each node object are stored as a object properties. The node object has the following properties. Unless specified, all properties have a value of `None` during initialization.

- `name` - (String) Node name. Set when inititalizing a node object.
- `addr` - (String) XBee address in hexadecimal. Set when initializing a node object.
- `channel` - (String) XBee channel.
- `aggre` - (String) XBee aggregator address in hexadecimal.
- `txperiod` - (Integer) Sampling period.
- `loc` - (String) Node location.
- `lastping` - (datetime object) Last successful communication with the node.
- `lastcommit` - (datetime object) Last successful settings commit (write to flash).
- `txpower` - (Integer) XBee transmit power.
- `status` - (String) Node status. Possible values are: 'Idle', 'Sensing'.
- `ver` - (String) Node firmware version.

Objects properties may be updated by issuing get or set commands to the node.

### Enabling logging

Object initialization and communication through get or set commands can be logged by setting the `logfile` property of a node object. This can be done during instantiation by using the `log` attribute to the target log file's path as shown:

```
import nodemgmt as n
X = n.node('nodeX','0013a20012345678',log='./logfile.log')
```

Log files may be shared between different node objects.

### The `status` property

Most of the functions in the node class automatically update the `status` property of a node object. Some functions use this property to automatically reject a command or query. For example, after sending a start command to a node, all further queries through the node management functions are automatically blocked until the node is sent a stopped command. The functions are able to do this because they check the `status` property before actually sending a command or query.

However, we don't actually have exclusive control of the remote node. Other sources may send commands/queries to the remote node, and these commands do not update the properties of our locally instantiated node objects. For example, a locally instantiated node might appear 'Idle', but another command source may have already sent it a start command. This in turn would bar us from sending a stop command, since the local object's status is still set to 'Idle'. To overcome this, you can simply manually set the property to `None` so that they check is bypassed the next time you issue the command/query.

```
>>> c6.status = None
```

<a name="nodefunc"></a>
## Node Functions

Commands and queries to remote nodes may be sent by using the following node functions.

- [getAggre()](#getAggre)
- [getPeriod()](#getPeriod)
- [getPower()](#getPower)
- [getVersion()](#getVersion)
- [setAggre()](#setAggre)
- [setIDLoc()](#setIDLoc)
- [setPeriod()](#setPeriod)
- [setPower()](#setPower)
- [start()](#start)
- [stop()](#stop)
- [commitSetting()](#commitSetting)

<a name="getAggre"></a>
### getAggre(ser)

Queries for a remote node's aggregator address. The reply is used to update the `aggre` property automatically. A successful reply updates the value of `lastping`, and sets the value of `status` to 'Idle'.

#### Required parameters:

- `ser` - Serial object.

#### Return value:

- `aggre` - (String) XBee aggregator address in hexadecimal.

#### Example:
```
>> x = c6.getAggre(ser)
>>> c6.aggre
'0013a20041249e0c'
>>> x
'0013a20041249e0c'
```

<a name="getPeriod"></a>
### getPeriod(ser)

Queries for a remote node's transmit period. The reply is used to update the `txperiod` property automatically. A value of 1 corresponds approximately to 0.25s. A successful reply updates the value of `lastping`, and sets the value of `status` to 'Idle'.

#### Required parameters:

- `ser` - Serial object.

#### Return value:

- `txperiod` - (Integer) XBee transmit period.

#### Example:
```
>> x = c6.getPeriod(ser)
>>> c6.txperiod
240
>>> x
240
```

<a name="getPower"></a>
### getPower(ser)

Queries for a remote node's transmit power. The reply is used to update the `txpower` property automatically. A successful reply updates the value of `lastping`, and sets the value of `status` to 'Idle'. Optional parameter `old` should be set to True for remote nodes with firmware version 1.7.2 or older.

#### Required parameters:

- `ser` - Serial object.

#### Return value:

- `txpower` - (Integer) XBee transmit power.

#### Optional parameters:

- `old` - (Boolean) Set this parameter to True when issuing this command to a node with firmware version 1.7.2 or older. 

#### Example 1: Firmware versions newer than 1.7.2
```
>>> x = c6.getPower(ser)
>>> c6.txpower
3
>>> x
3
```

#### Example 2 : Firmware versions 1.7.2 or older
```
>> x = c6.getPower(ser, old=True)
>>> c6.txpower
3
>>> x
3
```

<a name="getVersion"></a>
### getVersion(ser)

Queries for a remote node's firmware version. The reply is used to update the `ver` property automatically. A successful reply updates the value of `lastping`, and sets the value of `status` to 'Idle'.

#### Required parameters:

- `ser` - Serial object.

#### Return value:

- `ver` - (String) Node firmware version.

#### Example:
```
>>> x = c6.getVersion(ser)
>>> c6.aggre
'1.7.2'
>>> x
'1.7.2'
```

<a name=setAggre></a>
### setAggre(ser,aggre)

Sets a remote node's aggregator address. Updates the `aggre` property on success. Success also updates the value of `lastping`, and sets the value of `status` to 'Idle'.

#### Required parameters:

- `ser` - Serial object.
- `aggre` - (String) XBee aggregator address in hexadecimal.

#### Example:
```
>> c6.setAggre(ser,'0013a20041249e0c')
>>> c6.aggre
'0013a20041249e0c'
```

<a name="setIDLoc"></a>
### setIDLoc(ser,name,loc)
Sets a remote node's ID(name) and loc fields. Updates the `name` and `loc` properties on success. Success also updates the value of `lastping`, and sets the value of `status` to 'Idle'.

#### Required parameters:

- `ser` - Serial object.
- `name` - (String) Remote node ID.
- `loc` - (String) Remote node location.

#### Example:
```
>> c6.setIDLoc(ser,'testnode','somewhere')
>>> c6.name
'testnode'
>>> c6.loc
'somewhere'
```

<a name="setPeriod"></a>
### setPeriod(ser,period)

Sets a remote node's transmit period. Updates the `txperiod` property automatically. A value of 1 corresponds approximately to 0.25s. Success also updates the value of `lastping`, and sets the value of `status` to 'Idle'.

#### Required parameters:

- `ser` - Serial object.
- `period` - (Integer) XBee transmit period.

#### Example:
```
>>> x = c6.setPeriod(ser,240)
>>> c6.txperiod
240
```

<a name="setPower"></a>
### setPower(ser,power)

Sets a remote node's transmit power. Updates the `txpower` property automatically. Success also updates the value of `lastping`, and sets the value of `status` to 'Idle'.

#### Required parameters:

- `ser` - Serial object.
- `power` - (Integer) XBee transmit power.

#### Example:
```
>>> x = c6.setPower(ser,4)
>>> c6.txpower
4
```

<a name="start"></a>
### start(ser)

Sends a start command to a remote node. Success updates the value of `lastping` and sets the value of `status` to 'Sensing'.

#### Required parameters:

- `ser` - Serial object.

#### Optional parameters:

- `period` - (Integer) Transmit period. Automatically sets `txperiod` to this value. If not provided, node starts sensing using its current txperiod.

#### Example:
```
>>> c6.start(ser, period=120)
```

<a name="stop"></a>
### stop(ser)

Sends a stop command to a remote node. Success updates the value of `lastping` and sets the value of `status` to 'Idle'.

#### Required parameters:

- `ser` - Serial object.

#### Example:
```
>>> c6.stop(ser)
```

<a name="commitSetting"></a>
### commitSetting(ser)

Sends a "Write to Flash" command to a remote node. Success updates the value of `lastping` and sets the value of `status` to 'Idle'.

#### Required parameters:

- `ser` - Serial object.

#### Example:
```
>>> c6.commitSetting(ser)
```

<a name="samplecode"></a>
## Sample Code

```
import nodemgmt as n

# Configure local XBee serial interface, channel 20
ser = n.initcmd('/dev/ttyUSB0',20)

# Initialize node C6 with address 0x0013a20040e495a7
# Enable logging to logfile.log
c6 = n.node('C6','0013a20040e495a7',log='logfile.log')

# Initialize node A6 with address 0x0013a20040f436d7
# Enable logging to logfile.log
a6 = n.node('A6','0013a20040f436d7',log='logfile.log')

# Get C6's aggregator address and transmit period
aggre = c6.getAggre(ser)
c6.getPeriod(ser)

# Set A6's aggregator and period to be the same as C6
a6.setAggre(ser, aggre)
a6.setPeriod(ser, c6.txperiod)

# Start both nodes
c6.start(ser)
a6.start(ser)
```