# Command API

Python functions for configuring and controlling RESE2NSE v1 nodes (XBee). Code an be found in [command_api.py](https://github.com/snapdensing/node_v1_control/blob/v1.1_dev/command_api.py).

## Contents:
- Local XBee (USB Shield Configuration
  - [config()](#config)
- Remote Node (XBee + MSP) Configuration
  - [remote_aggre()](#remote_aggre)
  - [remote_nodeid()](#remote_nodeid)
  - [remote_nodeloc()](#remote_nodeloc)
  - [remote_channel()](#remote_channel)
  - [remote_power()](#remote_power)
  - [remote_wr()](#remote_wr)
- Remote Node (XBee + MSP) Query and Control
  - [remote_query()](#remote_query)
  - [remote_start()](#remote_start)
  - [remote_stop()](#remote_stop)

## Local XBee (USB shield) Configuration

<a name="config"></a>
### `config(device, power, channel)`

- Configures a USB-connected XBee to a certain channel and power.

- Arguments:
  - `device` - (type: string) Serial device (e.g. `/dev/ttyUSB0` in linux)
  - `power` - (type: int) XBee transmit power. Allowed values: 0 to 4.
  - `channel` - (type: int)  XBee channel. Allowed values: 11 to 26.

- Return values:
  - `ser` - (type: serial object) Serial object for specified device. Used by other functions in Command API to refer to the USB-connected XBee.

- Example:
  ```
  import command_api as c
  ser = c.config('/dev/ttyUSB1', 4, 24)
  ```
  Configures device connected as `/dev/ttyUSB1` to transmit on channel 24 with maximum transmit power.

## Remote Node (XBee + MSP) Configuration

<a name="remote_aggre"></a>
### `remote_aggre(ser, remote, addr)`

- Changes the aggregator/sink node of a remote node.

- Arguments:
  - `ser` - (type: serial object) Serial object for local USB-connected XBee.
  - `remote` - (type: string) Hexadecimal value of 64-bit remote node address.
  - `aggre` - (type: string) Hexadecimal value of 64-bit (new) aggregator address.

- Return values:
  - `success` - (type: int) Returns a 1 on a successful change, 0 otherwise.

- Example:
  ```
  import command_api as c
  remote = '0013a200abcd1234'
  sink = '0013a20056785678'
  c.remote_aggre(ser, remote, sink)
  ```
  Sets the sink node of remote node `0x0013a200abcd1234` to `0x0013a20056785678`

<a name="remote_nodeid"></a>
### `remote_nodeid(ser, remote, id)`

- Changes the node ID of a remote node.

- Arguments:
  - `ser` - (type: serial object) Serial object for local USB-connected XBee.
  - `remote` - (type: string) Hexadecimal value of 64-bit remote node address.
  - `id` - (type: string) New node ID value.
 
- Return values:

- Example:
  - `success` - (type: int) Returns a 1 on a successful change, 0 otherwise.

<a name="remote_nodeloc"></a>
### `remote_nodeloc()`
<a name="remote_channel"></a>
### `remote_channel()`
<a name="remote_power"></a>
### `remote_power()`
<a name="remote_wr"></a>
### `remote_wr()`

## Remote Node (XBee + MSP) Query and Control
<a name="remote_query"></a>
### `remote_query()`
<a name="remote_start"></a>
### `remote_start()`
<a name="remote_stop"></a>
### `remote_stop()`

