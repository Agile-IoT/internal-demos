#!/usr/bin/env python3

#########################################################
#               GE Link Bulb Control                    #
#                                                       #
#    Description: Program to control a GE Link Bulb     #
#       via a ZigBee module with the Cooking Hacks      #
#       Raspberry Pi to Arduino Shields Connection      #
#       Bridge. Functions allow to turn on, of, toggle  #
#       dim or blink the bulb                           #
#    Author: David Palomares <d.palomares@libelium.com> #
#    Version: 2.0                                       #
#    Date: May 2016                                     #
#########################################################

# --- Imports -----------
import sys
import signal
import time
#import RPi.GPIO as GPIO
import tkinter as tk
import dbus
import dbus_device as dbD
from gi.repository import GLib
import dbus.mainloop.glib
# -----------------------


# --- Variables ---------
mainloop = GLib.MainLoop()

# GE Link Bulb
GE_LINK_BULB_MAC = [0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF] # TODO: Your bulb's MAC here
GE_LINK_BULB_MAC = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF]
DEVICE_NAME = "000000000000FFFF"
#GPIOs
PINPOWER = 16 # Must be HIGH for shield to work
#if GPIO.RPI_INFO["TYPE"] == "Pi 3 Model B":
#   defDevice = "/dev/ttyS0"
#else:
defDevice = "/dev/ttyUSB0"
# DBus
PROTOCOL_BUS_NAME = "iot.agile.Protocol"
PROTOCOL_OBJ_PATH = "/iot/agile/Protocol"
SOCKET0 = "socket0"
SOCKET1 = "socket1"
XBEE_ZB = "XBee_ZigBee"
zb = None
# ZigBee
setup_params = {
   "baudrate": 38400,
   "apiMode2": False,
   "NJ": "FF",
   "ZS": "00",
   "EE": "01",
   "SC": "0020"  # set bit 5 only, which means only the 5th channel, starting from 11, i.e. channel 16 (shown as ATCH=0x10)
}
zb_explicit_command = {
   "api_command": "tx_explicit",
   "frame_id": [0x04],
   "dest_addr_long": [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF],
   "dest_addr": [0xFF, 0xFE],
   "src_endpoint": [0x00],
   "dest_endpoint": [0x01],
   "cluster": [0x00, 0x00],
   "profile": [0x01, 0x04],
   "broadcast_radius": [0x00],
   "options": [0x00],
   "data": [0x00] 
}
CLUSTER_A = [0x00, 0x06]
CLUSTER_B = [0x00, 0x08]
DATA_ON = [0x01, 0x00, 0x01, 0x00, 0x10]
DATA_OFF = [0x01, 0x00, 0x00, 0x00, 0x10]
DATA_TOGGLE = [0x01, 0x00, 0x02, 0x00, 0x10]
DATA_DIM = [0x01, 0x00, 0x04, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x10]
DATA_DIM_PARAM = 3
# -----------------------

class Lamp(dbD.Device):

   def __init__(self):     
      super().__init__()
      self._obj = Lamp_Obj()

class Lamp_Exception(dbD.DeviceException):
   
   def __init__(self, msg=""):
      super().__init__(DEVICE_NAME, msg)

class Lamp_Obj(dbD.DeviceObj):

   def __init__(self):
      super().__init__(DEVICE_NAME)

   @dbus.service.method(dbD.IFACE_NAME, in_signature="sa{sv}", out_signature="")
   def Execute(self, op, args):
      if op == "on":
         bulb_on()
      elif op == "off":
         bulb_off()
      elif op == "toggle":
         bulb_toggle()


# --- Functions ---------
def bulb_on():
   """
   Turns the GE Link Bulb On.
   """
   tx = zb_explicit_command
   tx["dest_addr_long"] = GE_LINK_BULB_MAC
   tx["cluster"] = CLUSTER_A
   tx["data"] = DATA_ON
   response = zb.Send(tx)

def bulb_off():
   """
   Turns the GE Link Bulb On.
   """
   tx = zb_explicit_command
   tx["dest_addr_long"] = GE_LINK_BULB_MAC
   tx["cluster"] = CLUSTER_A
   tx["data"] = DATA_OFF
   response = zb.Send(tx)

   
def bulb_toggle():
   """
   Toggles the GE Link Bulb.
   """
   tx = zb_explicit_command
   tx["dest_addr_long"] = GE_LINK_BULB_MAC
   tx["cluster"] = CLUSTER_A
   tx["data"] = DATA_TOGGLE
   response = zb.Send(tx)

   
def bulb_dim(bright):
   """
   Sets the bright of the GE Link Bulb between 100% (0xFF) and 0% (0x00).
   """
   bright = bright & 0xFF
   data = DATA_DIM
   data[DATA_DIM_PARAM] = bright
   tx = zb_explicit_command
   tx["dest_addr_long"] = GE_LINK_BULB_MAC
   tx["cluster"] = CLUSTER_B
   tx["data"] = data
   response = zb.Send(tx)
   
def bulb_dim_call():
   """
   Calls to bulb_dim with the bright set in the slider.
   """
   bright = int((dimSlider.get() * 0xFF) / 100)
   bulb_dim(bright)
   
def bulb_blink(times=5, speed=0.25):
   """
   Blinks the GE Link Bulb the specified number of times.
   """
   for i in range(times):
      bulb_toggle()
      time.sleep(speed)
      bulb_toggle()
      time.sleep(speed)
      
def bulb_blink_call():
   """
   Calls to bulb_dim with the times and the speed set.
   """
   times = blinkSlider.get()
   bulb_blink(times)

def setup():
   """
   Sets the default parameters of the program.
   """
   global zb
   # Signal handler (Ctrl+C exit)
   signal.signal(signal.SIGINT, signal_handler) 
   # DBus
   session_bus = dbus.SessionBus()
   objXBZB = session_bus.get_object(PROTOCOL_BUS_NAME, PROTOCOL_OBJ_PATH + "/" + XBEE_ZB + "/" + SOCKET0)
   zb = dbus.Interface(objXBZB, dbus_interface=PROTOCOL_BUS_NAME)
   # ZigBee
   zb.Setup(dbus.Dictionary(setup_params, signature="sv"))
   zb.Connect()
   
def signal_handler(signal, frame):
   """
   Handles the SIGINT signal.
   """
   print()
   endProgram(0)
   

# --- Classes -----------
#class DBusExit(dbus.service.Object):
    
#   def __init__(self):
#      super().__init__(dbus.SessionBus(), dbD.OBJ_PATH) 
    
#   @dbus.service.method(dbD.BUS_NAME, in_signature="", out_signature="")
#   def Exit(self):
#      mainloop.quit() 
# -----------------------

# --- Functions ---------
def dbusService():
   dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
#   dbe = DBusExit()
   lamp = Lamp()
   setup()
   print("Running DBus service.")
   try:
      mainloop.run()
   except KeyboardInterrupt:
      mainloop.quit()
      print()
      endProgram(0)
   
def endProgram(status):
   print("DBus service stopped.")
   zb.Disconnect()
   sys.exit(status)
# -----------------------



# --- Main program ------
if __name__ == "__main__":

   # Setup
#   setup()
   dbusService()
   
   endProgram(0)
# -----------------------

