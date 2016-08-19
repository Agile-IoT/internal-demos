
# AGILE DBus Protocol API (iot.agile.Protocol)

This repository contains a Python3 DBus server for the AGILE Protocol API. The server is in **alpha version**, as the AGILE API is being defined.

It also contains a demo program for controlling a GE Link Bulb with DBus, intended to be used with the Cooking Hacks shield and a XBee ZigBee module.


## Protocols and methods

The server implements the following protocols:
- XBee 802.15.4
- XBee ZigBee

Each protocol might implement the following methods:
- Connected () -> string
- Driver () -> string
- Name () -> string
- Connect () -> void
- Disconnect () -> void
- Discover (a{sv}) -> void
- Exec (sa{sv}) -> void
- Setup (a{sv}) -> void
- Send (a{sv}) -> void
- Receive () -> a{sv}
- Subscribe (a{sv}) -> void


## Installation

In order to run the application, some DBus libraries must be installed in the system.
```
sudo apt-get install libdbus-1-dev libdbus-glib-1-dev python3-gi
```

The python modules required are listed in the `requirements.txt` file, and can be installed from there.
```
sudo python3 -m pip install -r requirements.txt
```


## Usage

The order of execution is: 
- Setup
- Connect
- Send / Receive
- Disconnect. 

The Setup method only applies when the Connect method is called. If no setup parameters are defined, the Conect method will default to 9600 baudrate and XBee API Mode 1, the rest of the parameters being the ones saved in the XBee module.

#### Setup method

The Setup method will define the parameters that will be applied to the module. The method accepts the type a{sv} (array of string:variable pairs, ie. Python's Dictionary).

These string:variable pairs can be:
- "baudrate": int -> Defines a valid baudrate for the module (if omitted, defaults to 9600)
- "apiMode2": boolean -> Defines if the module is in API Mode 2 (if omitted, defaults to false)
- string atCommand1: string -> Two char string defining the AT command to send, the value must be the string representation of the hex parameter (example: {"ID": "A1B2"}).
- string atCommand2: string
- ...

#### Connect method

The Connect method opens the communication with the XBee module and applies the parameters stored in the setup.

#### Send method

The Send method accepts the type a{sv} in order to send information through the XBee module.

The string: variable pairs must be:
- "api_command": string -> One of the API Commands of the  API Commands table.
- string field: byte[] -> The fields required by the API Command, whose value must be an array of bytes
- string field2: byte[]
- ...

| API Command | Fields | XBee 802.15.4 | XBee ZigBee |
| ----------- | ------ | ------------- | ----------- |
| at | frame_id, command, parameter | **✔** | **✔** |
| queued_at | frame_id, command, parameter | **✔** | **✔** |
| remote_at | frame_id, dest_addr_long, dest_addr, options, command, parameter | **✔** | **✔** |
| tx_long_addr | frame_id, dest_addr, options, data | **✔** | **✗** |
| tx | frame_id, dest_addr, options, data | **✔** | **✔** |
| tx_explicit | frame_id, dest_addr_long, dest_addr, src_endpoint, cluster, profile, broadcast_radius, optios, data | **✗** | **✔** |

#### Receive method

The Receive method returns a frame received by the module in the format of a{sv}. The fields of the frame depend on the response and can be check in the API Responses table.

| API Responses | Fields | XBee 802.15.4 | XBee ZigBee |
| ------------- | ------ | ------------- | ----------- |
| (0x80) rx_long_addr | source_addr, rssi, options, rf_data | **✔** | **✗** |
| (0x81) rx | source_addr, rssi, options, rf_data | **✔** | **✗** |
| (0x82) rx_io_data_long_addr | source_addr_long, rssi, options, samples | **✔** | **✗** |
| (0x83) rx_io_data | source_addr, rssi, options, samples | **✔** | **✗** |
| (0x88) at_response | frame_id, command, status, parameter | **✔** | **✔** |
| (0x89) tx_status | frame_id, status | **✔** | **✗** |
| (0x8A) status | status | **✔** | **✔** |
| (0x8B) tx_status | frame_id, dest_addr, retries, deliver_status, discover_status | **✗** | **✔** |
| (0x90) rx | source_addr_long, source_addr, options, rf_data | **✗** | **✔** |
| (0x91) rx_explicit | source_addr_long, source_addr, source_endpoint, dest_endpoint, cluster, profile, options, rf_data | **✗** | **✔** |
| (0x92) rx_io_data_long_addr | source_addr_long, source_addr, options, samples | **✗** | **✔** |
| (0x95) node_id_indicator | sender_addr_long, sender_addr, options, source_addr, source_addr_long, node_id, parent_source_addr, device_type, source_event, digi_profile_id, manufacturer_id | **✗** | **✔** |
| (0x97) remote_at_response | frame_id, source_addr_long, source_addr, command, status, parameter | **✔** | **✔** |


#### Disconnect method

The Disconnect method closes the communication with the XBee module.


## Exiting the server

There are two ways of exiting the server, either by calling the Exit method (prefered) or by using `Control+C`.
```
dbus-send --session --type=method_call --dest='iot.agile.Protocol' '/iot/agile/Protocol' iot.agile.Protocol.Exit
```
