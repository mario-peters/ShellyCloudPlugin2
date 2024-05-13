# ShellyCloudPlugin
#
# Author: Mario Peters
#
"""
<plugin key="ShellyCloudPlugin2" name="Shelly Cloud Plugin V2" author="Mario Peters" version="1.0.0" wikilink="https://github.com/mario-peters/ShellyCloudPlugin2/wiki" externallink="https://github.com/mario-peters/ShellyCloudPlugin2">
    <description>
        <h2>Shelly Cloud Plugin V2</h2><br/>
        Plugin for controlling Shelly devices.
        <h3>Configuration</h3>
        <ul style="list-style-type:square">
            <li>IP Address is the IP Address of the Shelly device. Default value is 127.0.0.1</li>
            <li>Username</li>
            <li>Password</li>
            <li>Type is the type of Shelly device you want to add. Shelly 1, Shelly PM, Shelly 2.5 (relay and roller), Shelly Dimmer, Shelly RGBW2 (color and white), Shelly Bulb, Shelly Door/Window 2 and Shelly Plug-S are currently supported</li>
        </ul>
        <br/><br/>
    </description>
    <params>
        <param field="Address" label="IP Address" width="200px" required="true" default="127.0.0.1"/>
        <param field="Username" label="Username" width="200px" required="true"/>
        <param field="Password" label="Password" width="200px" required="true" password="true"/>
        <param field="Mode1" label="Type" width="200px" required="true">
            <options>
               <option label="Shelly 1" value="SHSW-1"/>
               <option label="Shelly IX3" value="SHIX3-1"/>
               <option label="Shelly PM" value="SHSW-PM"/>
               <option label="Shelly 1L" value="SHSW-L"/>
               <option label="Shelly 2.5" value="SHSW-25"/>
               <option label="Shelly Motion" value="SHMOS-01"/>
               <option label="Shelly TRV" value="SHTRV-01"/>
               <option label="Shelly Plug" value="SHPLG-S"/>
               <option label="Shelly Bulb" value="SHBLB-1"/>
               <option label="Shelly RGBW2" value="SHRGBW2"/>
               <option label="Shelly Dimmer" value="SHDM-1"/>
               <option label="Shelly H&T" value="SHHT-1"/>
               <option label="Shelly Smoke" value="SHSM-01"/>
               <option label="Shelly Flood" value="SHWT-1"/>
               <option label="Shelly Door/Window 2" value="SHDW-2"/>
               <option label="Shelly Gas" value="SHGS-1"/>
               <option label="Shelly 3EM" value="SHEM-3"/>
               <option label="Shelly EM" value="SHEM"/>
            </options> 
        </param>
       <param field="Mode2" label="Heartbeat In Seconds" width="50px" required="true" default="30"/>
    </params>
</plugin>
"""
import Domoticz
import requests
import json

class BasePlugin:
 
    #mode = None
    mode = "color"
    SHELLY_1 = "SHSW-1"
    SHELLY_IX3 = "SHIX3-1"
    SHELLY_1PM = "SHSW-PM"
    SHELLY_1L="SHSW-L"
    SHELLY_25 = "SHSW-25"
    SHELLY_MOTION = "SHMOS-01"
    SHELLY_TRV="SHTRV-01"
    SHELLY_PLUG = "SHPLG-S"
    SHELLY_BULB = "SHBLB-1"    
    SHELLY_RGBW2 = "SHRGBW2"
    SHELLY_DIMMER = "SHDM-1"
    SHELLY_HT = "SHHT-1"
    SHELLY_SMOKE = "SHSM-01"
    SHELLY_FLOOD = "SHWT-1"
    SHELLY_DW = "SHDW-2"
    SHELLY_GAS="SHGS-1"
    SHELLY_EM="SHEM"
    SHELLY_3EM="SHEM-3"

    HeartbeatInSeconds = 30

    def __init__(self):
        return

    def onStart(self):
        Domoticz.Log("onStart called")
        self.HeartbeatInSeconds = int(Parameters["Mode2"])
        if self.HeartbeatInSeconds < 0:
            Domoticz.Error("HeartbeatInSeconds size out of boundary error (HeartbeatInSeconds>0). Default value 30 is being used")

        Domoticz.Heartbeat(self.HeartbeatInSeconds)

        createDevices()

    def onStop(self):
        Domoticz.Log("onStop called")
        
    def onConnect(self, Connection, Status, Description):
        Domoticz.Log("onConnect called")

    def onMessage(self, Connection, Data):
        Domoticz.Log("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called")

    def onHeartbeat(self):
        Domoticz.Log("onHeartbeat called")

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

    # Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return
