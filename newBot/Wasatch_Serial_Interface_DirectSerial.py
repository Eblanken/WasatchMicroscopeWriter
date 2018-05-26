# TODO Interface_Serial: everything.
#
# File: WasatchInterface_DirectSerial
# ------------------------------
# Author: Erick Blankenberg
# Date: 5/12/2018
#
# Description:
#
# This class enables communication with the Wasatch microscope
# by directly accessing serial communication.
#
# NOTES:
# * As of right now, requires NULL MODEM to work
# * Setup:
#   * Set up null modem
#   * Plug in the microscope
#   * Run the controller GUI, wait for confirmation that this program
#    has gained control of the microscope
#   * Run the SparkOCT application, wait for confirmation that the program
#     has established communications with the "microscope" (really this program)
#

import pyautogui
import io
import serial
from serial.tools import list_ports
from Wasatch_Serial_Interface_Abstract import Wasatch_Serial_Interface_Abstract
from Wasatch_Serial_Commands import *


#
class Wasatch_Serial_Interface_DirectSerial(Wasatch_Serial_Interface_Abstract):
    #-------------------- Public Members ---------------
    # Initializes communications over serial to the Wastach
    def __init__(self):
        self.reconnectToMicroscope()
        
    def connectedToMicroscope(self):
        return self._currentlyConnected

    # Attempts to reestablish connection with the microscope
    def reconnectToMicroscope(self):
        if self._findPort():
            self._currentlyConnected = True;
            return True
        return False

    # Sends a serial command to the Wasatch Microscope after 'time' milliseconds
    def sendCommand(self, command):
        self.serialPort.write(("%s\n" % command).encode('utf-8'))

    #------------------- Private Members ---------------

    # Functions
    def _findPort(self):
        portList = list_ports.comports()
        print('Looking for serial ports:')
        for index in range(0, self._RECONNECTIONATTEMPTS):
            for currentPort in portList:
                try:
                    self.serialPort = serial.Serial(currentPort.device)
                    self.serialPort.close()
                    self.serialPort.open()
                except:
                    continue
                self.serialPort.timeout = 1.0
                self.sendCommand(WCommand_Ping())
                val = self.serialPort.read();
                if(val == b'A'):
                    print('Found the port for the galvos.')
                    self.sendCommand(WCommand_ScanStop())
                    print('Galvo connection initialized.')
                    return True
        print('No serial ports found for the galvo.')
        return False

    # Variables
    _currentlyConnected = False
    _serialPort = None # Object for serial comms

    # Constants
    _RECONNECTIONATTEMPTS = 5
