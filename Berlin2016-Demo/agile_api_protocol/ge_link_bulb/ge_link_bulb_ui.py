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
import tkinter as tk
import dbus
# -----------------------


# --- Variables ---------
# DBus
BUS_NAME = "iot.agile.Device.ZB"
OBJ_PATH_BASE = "/iot/agile/Device/ZB/"
DEVICE_ID = "000000000000FFFF"
bulb = None

# --- Functions ---------
def bulb_on():
   """
   Turns the GE Link Bulb On.
   """
   bulb.Execute("on",dbus.Dictionary(signature="sv"))

def bulb_off():
   """
   Turns the GE Link Bulb On.
   """
   bulb.Execute("off",dbus.Dictionary(signature="sv"))

   
def bulb_toggle():
   """
   Toggles the GE Link Bulb.
   """
   bulb.Execute("toggle",dbus.Dictionary(signature="sv"))

   
def bulb_dim(bright, steps=30, speed=1):
   """
   Sets the bright of the GE Link Bulb between 100% (0xFF) and 0% (0x00).
   """
   bulb.Execute("dim",dbus.Dictionary({"brightness": bright},signature="sv"))
   
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
   global bulb
   # Signal handler (Ctrl+C exit)
   signal.signal(signal.SIGINT, signal_handler) 
   # DBus
   session_bus = dbus.SessionBus()
   objlamp = session_bus.get_object(BUS_NAME, OBJ_PATH_BASE + DEVICE_ID)
   bulb = dbus.Interface(objlamp, dbus_interface="iot.agile.Device.ZB")
   
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
   bulb.Disconnect()
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

