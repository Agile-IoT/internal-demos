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
#    Version: 1.0                                       #
#    Date: May 2016                                     #
#########################################################

# --- Imports -----------
import sys
import signal
import serial
import time
import RPi.GPIO as GPIO
import tkinter as tk
# -----------------------


# --- Variables ---------
# GE Link Bulb
GE_LINK_BULB_MAC = [0xF0, 0xFE, 0x6B, 0x00, 0x14, 0x00, 0xBF, 0x26]
#GPIOs
PINPOWER = 16 # Must be HIGH for shield to work
# Serial
ser = serial.Serial()
device = ""
baudrates = [0, 50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400, 4800, 
             9600, 19200, 38400, 57600, 115200, 230400, 460800, 576000, 921600]
bytesizes = [serial.FIVEBITS, serial.SIXBITS, 
             serial.SEVENBITS, serial.EIGHTBITS]
parities =  [serial.PARITY_NONE, serial.PARITY_EVEN, serial.PARITY_ODD,
             serial.PARITY_MARK, serial.PARITY_SPACE]
stopbitss = [serial.STOPBITS_ONE, serial.STOPBITS_ONE_POINT_FIVE, 
             serial.STOPBITS_TWO]
if GPIO.RPI_INFO["TYPE"] == "Pi 3 Model B":
   defDevice = "/dev/ttyS0"
else:
   defDevice = "/dev/ttyAMA0"
defBaudrate = 9600
defBytesize = serial.EIGHTBITS
defParity = serial.PARITY_NONE
defStopbits = serial.STOPBITS_ONE
defTimeout = 0.5
# Frame = start delimiter, length (2), frame type,
#    frame id, 64-bit dest (8), 16-bit dest (2), 
#    source endpoint, dest endpoint, cluster ID (2), 
#    profile ID (2), broadcast radius, options, 
#    payload (N), checksum
START_DELIMITER = [0x7E]
TYPE_EXPLICIT = [0x11]
FRAME_ID = [0x04]
DST64 = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF] # Broadcast
DST16 = [0xFF, 0xFE]
SRC_ENDP = [0x00]
DST_ENDP = [0x01]
CLUSTER_A = [0x00, 0x06]
CLUSTER_B = [0x00, 0x08]
PROFILE = [0x01, 0x04]
BROAD_RAD = [0x00]
OPTIONS = [0x00]
dst_64_addr = GE_LINK_BULB_MAC
dst_16_addr = DST16
# Payloads
DATA_ON = [0x01, 0x00, 0x01, 0x00, 0x10]
DATA_OFF = [0x01, 0x00, 0x00, 0x00, 0x10]
DATA_TOGGLE = [0x01, 0x00, 0x02, 0x00, 0x10]
DATA_DIM = [0x01, 0x00, 0x04, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x10]
DATA_DIM_PARAM = 3
# -----------------------


# --- Functions ---------
def initXbee(port, baudrate = defBaudrate, bytesize = defBytesize, 
          parity = defParity, stopbits = defStopbits, timeout = defTimeout): 
      """
      Opens a serial port with the desired settings.
      """
      ser.port = port
      if baudrate in baudrates:
         ser.baudrate = baudrate
      else:
         ser.baudrate = defBaudrate
      if bytesize in bytesizes:
         ser.bytesyze = bytesize
      else:
         ser.bytesize = defBytesize
      if parity in parities:
         ser.parity = parity
      else:
         ser.bytesize = defBytesize
      if stopbits in stopbitss:
         ser.stopbits = stopbits
      else:
         ser.stopbits = defStopbits
      if timeout >= 0:
         ser.timeout = timeout
      else:
         ser.timeout = defTimeout
      try:
         ser.open()
      except:
         print("Serial exception.")
         endProgram(-1)

def makeFrame(cluster, data):
   """
   Creates a explicit frame with the parameters specified.
   """
   frame = []
   frame.extend(START_DELIMITER) # start delimiter
   frame.extend([0x00, 0x00])    # length
   frame.extend(TYPE_EXPLICIT)   # frame type
   frame.extend(FRAME_ID)        # frame ID
   frame.extend(dst_64_addr)     # 64-bit dest
   frame.extend(dst_16_addr)     # 16-bit dest
   frame.extend(SRC_ENDP)        # source endpoint
   frame.extend(DST_ENDP)        # dest endpoint
   frame.extend(cluster)         # cluster ID
   frame.extend(PROFILE)         # profile ID
   frame.extend(BROAD_RAD)       # broadcast radius
   frame.extend(OPTIONS)         # options
   frame.extend(data)            # payload
   length = len(frame[3:])
   lengthH = (length >> 8) & 0xFF
   lengthL = length & 0xFF
   frame[1] = lengthH
   frame[2] = lengthL
   checksum = 0x00
   for byte in frame[3:]:
      checksum = checksum + byte
   checksum = 0xFF - (checksum & 0xFF)
   frame.append(checksum)
   return bytes(frame)

def bulb_on():
   """
   Turns the GE Link Bulb On.
   """
   frame = makeFrame(CLUSTER_A, DATA_ON)
   ser.write(frame)

def bulb_off():
   """
   Turns the GE Link Bulb On.
   """
   frame = makeFrame(CLUSTER_A, DATA_OFF)
   ser.write(frame)
   
def bulb_toggle():
   """
   Toggles the GE Link Bulb.
   """
   frame = makeFrame(CLUSTER_A, DATA_TOGGLE)
   ser.write(frame)
   
def bulb_dim(bright):
   """
   Sets the bright of the GE Link Bulb between 100% (0xFF) and 0% (0x00).
   """
   bright = bright & 0xFF
   data = DATA_DIM
   data[DATA_DIM_PARAM] = bright
   frame = makeFrame(CLUSTER_B, data)
   ser.write(frame)
   
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
   # Signal handler (Ctrl+C exit)
   signal.signal(signal.SIGINT, signal_handler) 
   # GPIOs
   GPIO.setmode(GPIO.BOARD)
   GPIO.setwarnings(False) 
   GPIO.setup(PINPOWER, GPIO.OUT)
   GPIO.output(PINPOWER, GPIO.HIGH)
   #TODO: Check params from args? (device, dst64, dst16, baudrate...)
   initXbee(defDevice)
   
def signal_handler(signal, frame):
   """
   Handles the SIGINT signal.
   """
   print()
   endProgram(0)
   
def endProgram(status):
   """
   Exists the program.
   """
   ser.close()
   GPIO.output(PINPOWER, GPIO.LOW)
   GPIO.cleanup()
   sys.exit(status)
# -----------------------
   

# --- Main program ------
if __name__ == "__main__":

   # Setup
   setup()
   
   # Root window
   root = tk.Tk()
   root.wm_title("GE Link Bulb Control")
   root.rowconfigure(1, weight=1)
   root.columnconfigure(0, weight=1)
   root.minsize(width=270, height=95)
   root.maxsize(width=270, height=95)
   root.resizable(width=tk.FALSE, height=tk.FALSE)
   
   # Frames
   frameOnOff = tk.Frame(root)
   frameOnOff.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)  
   frameOnOff.columnconfigure(0, weight=1)
   frameOnOff.columnconfigure(1, weight=1)
   frameOnOff.columnconfigure(2, weight=1)
   frameDimBlink = tk.Frame(root)
   frameDimBlink.grid(row=1, column=0, sticky=tk.N+tk.S+tk.E+tk.W) 
   frameDimBlink.rowconfigure(0, weight=1)
   frameDimBlink.columnconfigure(0, weight=1)
   frameDimBlink.columnconfigure(1, weight=1)
   frameSliders = tk.Frame(root)
   frameSliders.grid(row=2, column=0, sticky=tk.N+tk.S+tk.E+tk.W) 
   frameSliders.rowconfigure(0, weight=1)
   frameSliders.columnconfigure(0, weight=1)
   frameSliders.columnconfigure(1, weight=1)
   
   # On/Off/Toggle
   onButton = tk.Button(frameOnOff, text="Turn ON", command=bulb_on)
   onButton.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)  
   offButton = tk.Button(frameOnOff, text="Turn OFF", command=bulb_off)
   offButton.grid(row=0, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
   toggleButton = tk.Button(frameOnOff, text="Toggle", command=bulb_toggle)
   toggleButton.grid(row=0, column=2, sticky=tk.N+tk.S+tk.E+tk.W)
   
   # Dim/Blink
   dimButton = tk.Button(frameDimBlink, text="Dim", command=bulb_dim_call)
   dimButton.grid(row=1, column=0, sticky=tk.N+tk.S+tk.E+tk.W) 
   blinkButton = tk.Button(frameDimBlink, text="Blink", command=bulb_blink_call)
   blinkButton.grid(row=1, column=1, sticky=tk.N+tk.S+tk.E+tk.W) 
   
   # Sliders
   dimSlider = tk.Scale(frameSliders, from_=0, to=100, orient=tk.HORIZONTAL)
   dimSlider.set(100)
   dimSlider.grid(row=2, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
   blinkSlider = tk.Scale(frameSliders, from_=1, to=10, orient=tk.HORIZONTAL)
   blinkSlider.set(5)
   blinkSlider.grid(row=2, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
   
   root.mainloop()
   
   endProgram(0)
# -----------------------

