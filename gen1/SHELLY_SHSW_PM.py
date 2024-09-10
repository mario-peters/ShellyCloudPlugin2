import DomoticzEx as Domoticz
from gen1 import SHELLY_SHSW

ID = "SHSW-PM"

def create(self, mac, ipaddress, username, password, dev,type):
    Domoticz.Log("SHELLY_SHSW_PM onCreate()")
    SHELLY_SHSW.create(self, mac, ipaddress, username, password, dev,type)

def onCommand(self, device_id, unit, command, Level, Color, Devices):
    Domoticz.Log("SHELLY_SHSW_PM onCommand()")
    SHELLY_SHSW.onCommand(self, device_id, unit, command, Level, Color, Devices)

def onHeartbeat(device, username, password):
    Domoticz.Log("SHELLY_SHSW_PM onHeartbeat()")
    SHELLY_SHSW.onHeartbeat(device, username, password)
