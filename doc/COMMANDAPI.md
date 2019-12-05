# Command API

Python functions for configuring and controlling RESE2NSE v1 nodes (XBee). Code an be found in [command_api.py](https://github.com/snapdensing/node_v1_control/blob/v1.1_dev/command_api.py).

## Local XBee (USB shield) Configuration
- `config(device,power,channel)`
  - Configures a USB-connected XBee to a certain channel and power.
  - Arguments:
    - `device` - (type: string) Serial device (e.g. `/dev/ttyUSB0` in linux)
    - `power` - (type: int) XBee transmit power. Allowed values: 0 to 4.
    - `channel` - (type: int)  XBee channel. Allowed values: 11 to 26.
  - Return values:
    - `ser` - (type: pyserial object) Serial object for specified device. Used by other functions in Command API to refer to the USB-connected XBee.
  - Example:
    ```
    ser = config('/dev/ttyUSB1', 4, 24)
    ```
    Configures device connected as `/dev/ttyUSB1` to transmit on channel 24 with maximum transmit power.

## Remote Node (XBee + MSP) Configuration
- `remote_aggre()`
- `remote_nodeid()`
- `remote_nodeloc()`
- `remote_channel()`
- `remote_power()`
- `remote_wr()`

## Remote Node (XBee + MSP) Query and Control
- `remote_query()`
- `remote_start()`
- `remote_stop()`

