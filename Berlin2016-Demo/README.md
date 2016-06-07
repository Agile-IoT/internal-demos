# Berlin Demo (July 2016)

The is the first internal - generic AGILE demo that aims to showcase the following:
* Demonstrate the use of 2 different wireless technologies for device communication using the Libelium shield and a RaspberryPi2 (or 3)
* Basic AGILE software functionality in: a) discovering and connecting to IoT devices, b) retrieving data from sensors and visualizing them (potentially saving them locally), c) triggering some actuation

### Scenario
Plug the shield on the Rpi and add a ZigBee (XBee) module, plug a BLE dongle in a USB port

The devices to be connected will be the TI SensorTag (BLE) and a GE Link light bulb (ZigBee)

Drivers (xbee serial, BlueZ) will be preinstalled and configured. Their functionality (scan network, connect to device, etc.) will be exposed internally through the AGILE API.

Connect to the AGILE main UI using a browser and authenticate -  for now, IDM supports Oauth2 with github, so any github user could log in. 

Have a sample Device Manager UI to initiate a BLE scan and connect to the TI SensorTag. Show the status of the TI, e.g., displaying some information (querying) from the device. Be able to trigger on/off actions on the light bulb (already connected and configured).

Have a sample Data Management UI to visualise some of the TI sensor data (as they arrive live from the sensor), store them in the local DB and visualise subset of the stored data.

Use Node-RED to display data from the sensor and control the light bulb
Use the Recommender (Recommender API can be invoked through Node-RED) to get recommendations of e.g., devices that support BLE and ZigBee or Node-RED flows that support BLE and ZigBee communication.

### Types of connected devices:
* Connected Lights (actuator) over ZigBee
* TI SensorTag multisensor over BLE
* (Time allowing) a connected device in the same LAN (e.g., a WeMo device)
* (Time allowing) a connected RIOT devices (over 802.14.5)

### List of hardware
* Raspberry Pi ver 2.
* Libelium extension shield (with 1 or 2 XBee sockets)
* [XBee ZigBee Mesh module] 
* [BLE USB dongle] (since there is no BLE xbee module yet from Libelium)
* [ZigBee lightbulb] 

[XBee ZigBee Mesh module]:
<https://www.sparkfun.com/products/10414>
[BLE USB dongle]:
<https://www.amazon.co.uk/Plugable-Bluetooth-Adapter-Raspberry-Compatible/dp/B009ZIILLI/>
[ZigBee lightbulb]: <http://www.amazon.it/Wireless-Connected-Bulb-Equivalent-Quirky/dp/B018HETCVS/>


Available instructions/examples on device Xbee communication:
* https://www.youtube.com/watch?v=MPgN5I_nOoU
* http://www.instructables.com/id/ZigBee-Home-Automation-Lightbulb/?ALLSTEPS
* http://forum.linksprite.com/index.php?/topic/3606-my-diy-home-automation-box-with-pcduinoarduino/?p=7786
