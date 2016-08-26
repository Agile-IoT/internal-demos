
#########################################################
#            AGILE DBus Protocol Base                   #
#                                                       #
#    Description: Base class of the Protocol defined    #
#       in the AGILE API with all the operations. Other #
#       classes can inherit and extend this class to    #
#       implmenet the different protocols.              #
#    Author: David Palomares <d.palomares@libelium.com> #
#    Version: 0.1                                       #
#    Date: June 2016                                    #
#########################################################

# --- Imports -----------
import dbus
import dbus.service
# -----------------------


# --- Variables ---------
BUS_NAME = "iot.agile.Protocol.ZB"
OBJ_PATH = "/iot/agile/Protocol/ZB"
SOCKET0 = "socket0"
SOCKET1 = "socket1"

try:
  import RPi.GPIO as GPIO
  if GPIO.RPI_INFO["TYPE"] == "Pi 3 Model B":
     SOCKET0DEV = "/dev/ttyS0"
     SOCKET1DEV = "/dev/ttyS0"
  else:
     SOCKET0DEV = "/dev/ttyAMA0"
     SOCKET1DEV = "/dev/ttyAMA0"
except (ImportError, RuntimeError):
  SOCKET0DEV = "/dev/ttyUSB0"
  SOCKET1DEV = "/dev/ttyUSB0"
SOCKETDEV = {SOCKET0: SOCKET0DEV, SOCKET1: SOCKET1DEV} 
# -----------------------


# --- Classes -----------
class ProtocolException(dbus.DBusException):

   def __init__(self, protocol_name, msg=""):
      if msg == "":         
         super().__init__(protocol_name)
      else:
         super().__init__(protocol_name + ": " + msg)
      self._dbus_error_name = BUS_NAME
      
        
class ProtocolObj(dbus.service.Object):
   
   def __init__(self, protocol_name, socket):
      self._bus_name = BUS_NAME
      self._obj_path = OBJ_PATH
      self._socket = socket
      self._protocol_name = protocol_name   
      self._connected = False
      super().__init__(dbus.SessionBus(), self._obj_path + "/" + protocol_name + "/" + socket)
      
   def _getConnected(self):
      return self._connected
      
   def _setConnected(self, status):
      if status:
         self._connected = True
      else:
         self._connected = False 
      
   def _getSocketDev(self, socket):
      return SOCKETDEV[socket]
         
   # AGILE API Methods  
      
   @dbus.service.method(BUS_NAME, in_signature="", out_signature="b")
   def Connected(self):
      return _getConnected()

   @dbus.service.method(BUS_NAME, in_signature="", out_signature="s")
   def Driver(self):
      return "No driver."

   @dbus.service.method(BUS_NAME, in_signature="", out_signature="s")
   def Name(self):
      return self._protocol_name

   @dbus.service.method(BUS_NAME, in_signature="", out_signature="")
   def Connect(self):
      raise Protocol_Exception(self._protocol_name, "Function not supported.")

   @dbus.service.method(BUS_NAME, in_signature="", out_signature="")
   def Disconnect(self):
      raise Protocol_Exception(self._protocol_name, "Function not supported.")

   @dbus.service.method(BUS_NAME, in_signature="a{sv}", out_signature="") 
   def Discover(self, args):
      raise Protocol_Exception(self._protocol_name, "Function not supported.")

   @dbus.service.method(BUS_NAME, in_signature="sa{sv}", out_signature="")
   def Exec(self, op, args):
      raise Protocol_Exception(self._protocol_name, "Function not supported.")

   @dbus.service.method(BUS_NAME, in_signature="a{sv}", out_signature="")
   def Setup(self, args):
      raise Protocol_Exception(self._protocol_name, "Function not supported.")

   @dbus.service.method(BUS_NAME, in_signature="a{sv}", out_signature="")
   def Send(self, args):
      raise Protocol_Exception(self._protocol_name, "Function not supported.")

   @dbus.service.method(BUS_NAME, in_signature="", out_signature="a{sv}")
   def Receive(self):
      raise Protocol_Exception(self._protocol_name, "Function not supported.")

   @dbus.service.method(BUS_NAME, in_signature="a{sv}", out_signature="")
   def Subscribe(self, args):
      raise Protocol_Exception(self._protocol_name, "Function not supported.")


class Protocol():

   def __init__(self):
      self._socket0 = SOCKET0
      self._socket1 = SOCKET1
      self._name = dbus.service.BusName(BUS_NAME, dbus.SessionBus())
# -----------------------


