# Command API

Python functions for configuring and controlling RESE2NSE v1 nodes (XBee). Code can be found in [command_api.py](https://github.com/snapdensing/node_v1_control/blob/v1.1_dev/command_api.py).

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
Remote nodes can only be configured when they are in the idle/debug state (not sensing).

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
  - `success` - (type: int) Returns a 1 on a successful change, 0 otherwise.

<a name="remote_nodeloc"></a>
### `remote_nodeloc(ser, remote, loc)`
- Changes the node location (ID) of a remote node.

- Arguments:
  - `ser` - (type: serial object) Serial object for local USB-connected XBee.
  - `remote` - (type: string) Hexadecimal value of 64-bit remote node address.
  - `loc` - (type: string) New node ID value.
 
- Return values:
  - `success` - (type: int) Returns a 1 on a successful change, 0 otherwise.

<a name="remote_channel"></a>
### `remote_channel(ser, remote, channel)`

- Sets the XBee channel of a remote node.

- Arguments:
  - `ser` - (type: serial object) Serial object for local USB-connected XBee.
  - `remote` - (type: string) Hexadecimal value of 64-bit remote node address.
  - `channel` - (type: int) New XBee channel for remote node (Values allowed: 11 to 26)

- Return value:
  - `success` - (type: int) Returns a 1 on a successful change, 0 otherwise.

<a name="remote_power"></a>
### `remote_power(ser, remote, power)`
- Sets the XBee transmit power of a remote node.

- Arguments:
  - `ser` - (type: serial object) Serial object for local USB-connected XBee.
  - `remote` - (type: string) Hexadecimal value of 64-bit remote node address.
  - `power` - (type: int) New XBee transmit power for remote node (Values allowed: 0 to 4)

- Return value:
  - `success` - (type: int) Returns a 1 on a successful change, 0 otherwise.

<a name="remote_wr"></a>
### `remote_wr(ser, remote)`

- Commits XBee internal parameters to XBee flash.

- Arguments:
  - `ser` - (type: serial object) Serial object for local USB-connected XBee.
  - `remote` - (type: string) Hexadecimal value of 64-bit remote node address.

## Remote Node (XBee + MSP) Query and Control
<a name="remote_query"></a>
### `remote_query(ser, remote, param)`

- Queries for MSP or XBee parameters of a remote node. Remote nodes can only be queried if they are in the idle/debug state.

- Arguments:
  - `ser` - (type: serial object) Serial object for local USB-connected XBee.
  - `remote` - (type: string) Hexadecimal value of 64-bit remote node address.
  - `param` - (type: string) Parameter to query. The list of parameters are shown below.
 
- Return value:
  - `success` - (type: int) Returns a 1 on a successful change, 0 otherwise.

- Parameters (`param`):
  - `'PL'` - XBee transmit power. Node returns `'QPL[power]'`, where `[power]` is 1-byte power value (0x00 to 0x04).
  - `'CH'` - XBee channel. Node returns `'QC[channel]'`, where `[channel]` is 1-byte channel value (0x0b to 0x1a).
  - `'A'` - Aggregator address. Node returns `'QA[address]'`, where `[address]` is an 8-byte value.
  - `'T'` - Node transmit/sensing period. Node returns `'QT[period]'`, where `[period]` is a 1 to 2 byte value.
  - `'S'` - Node transmit statistics. Node returns `'QS[txnum][txfail]'`, where `[txnum]` is the number of transmissions made (2-bytes) and `[txfail]` is the number of failed transmissions (2-bytes). 
  - `'F'` - Node MSP Control Flag register. Node returns `'QF[flag]'`, where `[flag]` is a 1-byte control flag register value.
    - Control Flag register fields:
      - bit 7 - Auto-start sensing flag. Auto-starts node into sensing state on boot when set to `0`.
  - `'V'` - Node firmware version. Node returns `'QV[version]'`, where `[version]` is an ASCII-encoded string.
  - `'WR'` - Performs an XBee parameter flash commit (same as [remote_wr()](#remote_wr). Node returns `QWR`.

<a name="remote_start"></a>
### `remote_start(ser, remote, period)`

- Commands a remote node from idle/debug state to start sensing.

- Arguments:
  - `ser` - (type: serial object) Serial object for local USB-connected XBee.
  - `remote` - (type: string) Hexadecimal value of 64-bit remote node address.
  - `period` - (type: int) Sense/transmit period of the remote node. Allowed values are `0 to 65535`. If the value set is `0`, the remote node will retain its previously set period.
 
- Return value:
  - `success` - (type: int) Returns a 1 on a successful change, 0 otherwise.

<a name="remote_stop"></a>
### `remote_stop(ser, remote)`

- Stops a remote node from sensing and transitions it to the idle/debug state.

- Arguments:
  - `ser` - (type: serial object) Serial object for local USB-connected XBee.
  - `remote` - (type: string) Hexadecimal value of 64-bit remote node address.
 
- Return value:
  - `success` - (type: int) Returns a 1 on a successful change, 0 otherwise.


