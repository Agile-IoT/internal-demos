
#########################################################
#            AGILE DBus Protocol XBee ZigBee            #
#                                                       #
#    Description: Class of the Protocol defined in the  #
#       in the AGILE API with the implementation of the #
#       XBee ZigBee protocol.                           #
#    Author: David Palomares <d.palomares@libelium.com> #
#    Version: 0.2                                       #
#    Date: August 2016                                  #
#########################################################

# --- Imports -----------
import dbus
import dbus.service
from dbus_protocols import dbus_protocol as dbP
import serial
import xbee
# -----------------------


# --- Variables ---------
PROTOCOL_NAME = "XBee_ZigBee"
BAUDRATE = "baudrate"
DEF_BAUDRATE = 9600
APIMODE2 = "apiMode2"
DEF_APIMODE2 = False
ATCMDS = "atCmds"
APITXCMDS = ["at", "queued_at", "remote_at", "tx_long_addr", "tx", "tx_explicit"]
CMDWRITE = b"WR"
# -----------------------


# --- Classes -----------
class XBee_ZigBee(dbP.Protocol):
   
   def __init__(self):     
      super().__init__()
      self._protocol_name = PROTOCOL_NAME
      self._objS0 = XBee_ZigBee_Obj(self._socket0)
      self._objS1 = XBee_ZigBee_Obj(self._socket1)
       

class XBee_ZigBee_Exception(dbP.ProtocolException):
   
   def __init__(self, msg=""):
      super().__init__(PROTOCOL_NAME, msg)
      
    
class XBee_ZigBee_Obj(dbP.ProtocolObj):

   def __init__(self, socket):
      super().__init__(PROTOCOL_NAME, socket)
      self._setup = {
         BAUDRATE: DEF_BAUDRATE,
         APIMODE2: DEF_APIMODE2,
         ATCMDS: []
      }

   # Override DBus object methods
   @dbus.service.method(dbP.BUS_NAME, in_signature="", out_signature="")
   def Connect(self):
      if self._getConnected():
         raise XBee_ZigBee_Exception("Module is already connected.")
      self._serial = serial.Serial(self._getSocketDev(self._socket), self._setup[BAUDRATE])
      self._module = xbee.ZigBee(self._serial, escaped=self._setup[APIMODE2])
      writeChanges = False
      for option in self._setup[ATCMDS]:
         cmd = list(option.keys())[0]
         param = list(option.values())[0]
         cmdEnc = cmd.encode("UTF-8")
         if (cmdEnc == CMDWRITE):
            writeChanges = True
            break
         paramEnc = b"\x00"
         blen = (param.bit_length() + 7) // 8
         if blen != 0:
            paramEnc = param.to_bytes(blen, byteorder="big")
         self._module.send("at", frame_id=b"R", command=cmdEnc, parameter=paramEnc)
         rx = self._module.wait_read_frame()
         if not rx["status"]:
            raise XBee_ZigBee_Exception("Did not receive response from AT command")
         if rx["status"] != b"\x00":
            raise XBee_ZigBee_Exception("Wrong AT command/parameter ({}/{})".format(cmd, param))
      if writeChanges:
         self._module.send("at", frame_id=b"R", command=CMDWRITE)
         rx = self._module.wait_read_frame()
         if not rx["status"]:
            raise XBee_ZigBee_Exception("Did not receive response from AT command")
      self._setConnected(True)

   @dbus.service.method(dbP.BUS_NAME, in_signature="", out_signature="")
   def Disconnect(self):
      if not self._getConnected():
         raise XBee_ZigBee_Exception("Module is already disconnected.")
      self._setConnected(False)
      self._module.halt()
      self._serial.close()

   @dbus.service.method(dbP.BUS_NAME, in_signature="a{sv}", out_signature="")
   def Setup(self, args):
      self._setup.clear()
      self._setup = {
         BAUDRATE: DEF_BAUDRATE,
         APIMODE2: DEF_APIMODE2,
         ATCMDS: []
      }
      for key in args.keys():
         if key == BAUDRATE:
            self._setup[BAUDRATE] = int(args[BAUDRATE])
         elif key == APIMODE2:
            self._setup[APIMODE2] = bool(args[APIMODE2])
         else:
            try:
               param = int(args[key], 16)              
            except ValueError:
               param = 0x00
            finally:
               self._setup[ATCMDS].append({str(key): param})
         
   @dbus.service.method(dbP.BUS_NAME, in_signature="a{sv}", out_signature="")
   def Send(self, args):
      if not self._getConnected():
         raise XBee_ZigBee_Exception("Module is not connected.")
      cmd = args.pop("api_command", "")
      if not cmd in APITXCMDS:
         raise XBee_ZigBee_Exception("A valid API command must be provided {}.".format(APITXCMDS))
      params = {}
      for key in args.keys():
         if type(args[key]) == dbus.Array:
            params[key] = bytes(args[key])
      self._module.send(cmd, **params)

   @dbus.service.method(dbP.BUS_NAME, in_signature="", out_signature="a{sv}")
   def Receive(self):
      if not self._getConnected():
         raise XBee_ZigBee_Exception("Module is not connected.")
      rx = self._module.wait_read_frame()
      result = {}
      for key in rx.keys():
         result[key] = []
         for byte in rx[key]:
            result[key].append(byte)
      return dbus.Dictionary(result, signature="sv")
# -----------------------


