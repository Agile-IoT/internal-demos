# GE Link Bulb Demo

This program allows to control a GE Link Bulb via a ZigBee module with the Cooking Hacks Raspberry Pi to Arduino Shields Connection Bridge. Functions allow to turn on, of, toggle dim or blink the bulb.                  

### Setting up the Xbee ZigBee module

In order to connect the bulb to the module, it must be configured as a ZigBee Coordinator API  with the latest firmware (21A7).

The following parameters must be set in the module:
- ZigBee Stack Profile (ZS) = 0x02
- Node Join Time (NJ) = 0xFF
- Encryption Enable (EE) = 0x01
- Encryption Options (EO) = 0x01

### Setting up the GE Link Bulb

Once the module is configured, a bulb can be connected to the network by just turning it on. If the bulb successfuly joins a network, it will blink three times. The configuration of the network will remain in the bulb. 

To reset the bulb configuration, the bulb must be turned on and off at a three-second intervals until the bulb dims and goes back to full brightness.

### Sending commands to the bulb

The bulb uses explicit addressing command frames (frame type 0x11) to accept commands. The profile ID is 0104 and the cluster ID is 0006 for the turn on, turn off and toggle commands and 0008 for the dim command.

The data of each command is:
- DATA_ON = [0x01, 0x00, 0x01, 0x00, 0x10]
- DATA_OFF = [0x01, 0x00, 0x00, 0x00, 0x10]
- DATA_TOGGLE = [0x01, 0x00, 0x02, 0x00, 0x10]
- DATA_DIM = [0x01, 0x00, 0x04, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x10]
   
A full frame example:
```
Turn Off (broadcast):
   7E 00 19 11 04 00 00 00 00 00 00 FF FF FF FE 00 01 00 06 01 04 00 00 01 00 00 00 10 D2
  
Turn On (broadcast):
   7E 00 19 11 04 00 00 00 00 00 00 FF FF FF FE 00 01 00 06 01 04 00 00 01 00 01 00 10 D1
```
