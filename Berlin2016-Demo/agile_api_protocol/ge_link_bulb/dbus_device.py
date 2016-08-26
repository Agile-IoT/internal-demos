
#########################################################
#            AGILE DBus Device Base                     #
#                                                       #
#    Description: Base class of the Device defined      #
#       in the AGILE API with all the operations. Other #
#       classes can inherit and extend this class to    #
#       implmenet the different devices.                #
#    Author: David Palomares <d.palomares@libelium.com> #
#    Author: Csaba Kiraly <kiraly@fbk.eu>               #
#    Version: 0.1                                       #
#    Date: August 2016                                  #
#########################################################

# --- Imports -----------
import dbus
import dbus.service
# -----------------------


# --- Variables ---------
BUS_NAME = "iot.agile.Device.ZB"
IFACE_NAME = "iot.agile.Device"
OBJ_PATH = "/iot/agile/Device/ZB"

# --- Classes -----------
class DeviceException(dbus.DBusException):

   def __init__(self, device_name, msg=""):
      if msg == "":         
         super().__init__(device_name)
      else:
         super().__init__(device_name + ": " + msg)
      self._dbus_error_name = BUS_NAME
      
        
class DeviceObj(dbus.service.Object):
   
   def __init__(self, device_name):
      self._bus_name = BUS_NAME
      self._obj_path = OBJ_PATH
      self._device_name = device_name
      self._connected = False
      super().__init__(dbus.SessionBus(), self._obj_path + "/" + device_name)
      
   def _getConnected(self):
      return self._connected
      
   def _setConnected(self, status):
      if status:
         self._connected = True
      else:
         self._connected = False 
      
   # AGILE API Methods  
      
   @dbus.service.method(IFACE_NAME, in_signature="", out_signature="b")
   def Connected(self):
      return _getConnected()

   @dbus.service.method(IFACE_NAME, in_signature="", out_signature="s")
   def Name(self):
      return self._device_name

   @dbus.service.method(IFACE_NAME, in_signature="", out_signature="")
   def Connect(self):
      raise Device_Exception(self._device_name, "Function not supported.")

   @dbus.service.method(IFACE_NAME, in_signature="", out_signature="")
   def Disconnect(self):
      raise Device_Exception(self._device_name, "Function not supported.")

   @dbus.service.method(IFACE_NAME, in_signature="sa{sv}", out_signature="")
   def Execute(self, op, args):
      raise Device_Exception(self._device_name, "Function not supported.")

class Device():

   def __init__(self):
      self._name = dbus.service.BusName(BUS_NAME, dbus.SessionBus())
# -----------------------


