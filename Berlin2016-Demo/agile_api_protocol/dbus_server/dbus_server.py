#!/usr/bin/env python3

#########################################################
#            AGILE DBus Protocol Server                 #
#                                                       #
#    Description: Runs the AGILE DBus Protocol defined  #
#       in the AGILE API for the XBee 802.15.4 and XBee #
#       ZigBee protocols.                               #
#    Author: David Palomares <d.palomares@libelium.com> #
#    Version: 0.1                                       #
#    Date: June 2016                                    #
#########################################################

# --- Imports -----------
import sys
from gi.repository import GLib
import dbus
import dbus.service
import dbus.mainloop.glib
from dbus_protocols import dbus_protocol as dbP
from dbus_protocols import dbus_xbee_802_15_4 as xb_802
from dbus_protocols import dbus_xbee_zigbee as xb_zb
# -----------------------


# --- Variables ---------
mainloop = GLib.MainLoop()
# -----------------------


# --- Classes -----------
class DBusExit(dbus.service.Object):
    
   def __init__(self):
      super().__init__(dbus.SessionBus(), dbP.OBJ_PATH) 
    
   @dbus.service.method(dbP.BUS_NAME, in_signature="", out_signature="")
   def Exit(self):
      mainloop.quit() 
# -----------------------


# --- Functions ---------
def dbusService():
   dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
   dbe = DBusExit()
   xb1 = xb_802.XBee_802_15_4()
   xb2 = xb_zb.XBee_ZigBee()
   print("Running DBus service.")
   try:
      mainloop.run()
   except KeyboardInterrupt:
      mainloop.quit()
      print()
      endProgram(0)
   
def endProgram(status):
   print("DBus service stopped.")
   sys.exit(status)
# -----------------------
   

# --- Main program ------
if __name__ == "__main__":
   dbusService()   
   endProgram(0)
# -----------------------

