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
        <param field="Mode1" label="IP-range" width="200px" required="true"/>
        <param field="Mode2" label="Heartbeat In Seconds" width="50px" required="true" default="30"/>
    </params>
</plugin>
"""
import DomoticzEx as Domoticz
import requests
import json
from gen23 import *
from gen1 import *

SHELLY_DEVICES = {SHELLY_SHDM_2.ID, SHELLY_SHSW25.ID, SHELLY_SHSW_PM.ID, SHELLY_SNSW_002P16EU.ID, SHELLY_SNSW_102P16EU.ID, SHELLY_SNSW_001P16EU.ID, SHELLY_SNPL_00112EU.ID, SHELLY_S3SW_001P8EU.ID}

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

    #SHELLY_DEVICES = {SHELLY_SHSW25.ID, SHELLY_SHSW_PM.ID, SHELLY_SNSW_002P16EU.ID, SHELLY_SNSW_102P16EU.ID}

    HeartbeatInSeconds = 30

    def __init__(self):
        return

    def onStart(self):
        Domoticz.Log("onStart called")
        self.HeartbeatInSeconds = int(Parameters["Mode2"])
        if self.HeartbeatInSeconds < 0:
            Domoticz.Error("HeartbeatInSeconds size out of boundary error (HeartbeatInSeconds>0). Default value 30 is being used")

        Domoticz.Heartbeat(self.HeartbeatInSeconds)

        createDevices(self)

    def onStop(self):
        Domoticz.Log("onStop called")
        
    def onConnect(self, Connection, Status, Description):
        Domoticz.Log("onConnect called")

    def onMessage(self, Connection, Data):
        Domoticz.Log("onMessage called")

    def onCommand(self, DeviceID, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called for Device " + str(DeviceID) + " Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))
        if DeviceID.startswith(SHELLY_SNSW_001P16EU.ID):
            SHELLY_SNSW_001P16EU.onCommand(DeviceID, Unit, Command, Level, Hue, Parameters["Username"], Parameters["Password"], Devices)
        elif DeviceID.startswith(SHELLY_SNPL_00112EU.ID):
            SHELLY_SNPL_00112EU.onCommand(DeviceID, Unit, Command, Level, Hue, Parameters["Username"], Parameters["Password"], Devices)
        elif DeviceID.startswith(SHELLY_S3SW_001P8EU.ID):
            SHELLY_S3SW_001P8EU.onCommand(DeviceID, Unit, Command, Level, Hue, Parameters["Username"], Parameters["Password"], Devices)
        elif DeviceID.startswith(SHELLY_SHDM_2.ID):
            SHELLY_SHDM_2.onCommand(DeviceID, Unit, Command, Level, Hue, Parameters["Username"], Parameters["Password"], Devices)

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called")

    def onHeartbeat(self):
        Domoticz.Log("onHeartbeat called")
        for device in Devices:
            if device.startswith(SHELLY_SNSW_001P16EU.ID):
                SHELLY_SNSW_001P16EU.onHeartbeat(Devices[device], Parameters["Username"], Parameters["Password"])
            elif device.startswith(SHELLY_SNPL_00112EU.ID):
                SHELLY_SNPL_00112EU.onHeartbeat(Devices[device], Parameters["Username"], Parameters["Password"])
            elif device.startswith(SHELLY_S3SW_001P8EU.ID):
                SHELLY_S3SW_001P8EU.onHeartbeat(Devices[device], Parameters["Username"], Parameters["Password"])
            elif device.startswith(SHELLY_SHDM_2.ID):
                SHELLY_SHDM_2.onHeartbeat(Devices[device], Parameters["Username"], Parameters["Password"])

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

def onCommand(DeviceID, Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(DeviceID, Unit, Command, Level, Hue)

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

def createDevices(self):
    Domoticz.Log("CreateDevices")
    headers = {'content-type':'application/json'}
    count = 50
    while count < 255:
        ipaddress = "192.168.1."+str(count)
        url = "http://"+ipaddress+"/shelly"
        #Domoticz.Log(url)
        count = count + 1
        response_shelly = None
        try:
            response_shelly = requests.get(url, headers=headers, auth=(Parameters["Username"], Parameters["Password"]), timeout=1)
        except requests.exceptions.Timeout as e:
            Domoticz.Debug(str(e))
        except requests.exceptions.ConnectionError as e:
            Domoticz.Debug(str(e))
        if response_shelly is not None and response_shelly.status_code == 200 and response_shelly.headers.get('content-type') == 'application/json':
            Domoticz.Debug(ipaddress+" --> "+str(response_shelly.text))
            json_items = json.loads(response_shelly.text)
            response_shelly.close()
            type = ""
            mac = ""
            for key, value in json_items.items():
                if key == "type" or key == "model":
                    type = value
                if key == "mac":
                    mac = value
            deviceid = type+":"+mac+":"+ipaddress
            if deviceid not in Devices:
                deviceFound = False
                for shelly_dev in SHELLY_DEVICES:
                    if deviceFound == False:
                        #if shelly_dev == type:
                        if type == SHELLY_SHSW25.ID:
                            Domoticz.Log(type+" found with IP: "+ipaddress)
                            SHELLY_SHSW25.create(self, mac, ipaddress, Parameters["Username"], Parameters["Password"], Devices,type)
                            deviceFound = True
                        elif type == SHELLY_SHSW_PM.ID:
                            Domoticz.Log(type+" found with IP: "+ipaddress)
                            SHELLY_SHSW_PM.create(self, mac, ipaddress, Parameters["Username"], Parameters["Password"], Devices, type)
                            deviceFound = True
                        elif type == SHELLY_SNSW_001P16EU.ID:
                            Domoticz.Log(type+" found with IP: "+ipaddress)
                            SHELLY_SNSW_001P16EU.create(mac, ipaddress, Parameters["Username"], Parameters["Password"], Devices, type)
                            deviceFound = True
                        elif type == SHELLY_SNPL_00112EU.ID:
                            Domoticz.Log(type+" found with IP: "+ipaddress)
                            SHELLY_SNPL_00112EU.create(mac, ipaddress, Parameters["Username"], Parameters["Password"], Devices, type)
                            deviceFound = True
                        elif type == SHELLY_S3SW_001P8EU.ID:
                            Domoticz.Log(type+" found with IP: "+ipaddress)
                            SHELLY_S3SW_001P8EU.create(mac, ipaddress, Parameters["Username"], Parameters["Password"], Devices, type)
                            deviceFound = True
                        elif type == SHELLY_SHDM_2.ID:
                            Domoticz.Log(type+" found with IP: "+ipaddress)
                            SHELLY_SHDM_2.create(mac, ipaddress, Parameters["Username"], Parameters["Password"], Devices, type)
                            deviceFound = True
                        else:
                            deviceFound = False
                if deviceFound == False:
                    Domoticz.Log("Unknown device found for ip "+ipaddress+" and type "+type)
