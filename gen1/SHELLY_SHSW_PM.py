import DomoticzEx as Domoticz
from gen1 import SHELLY_SHSW

ID = "SHSW-PM"

def create(mac, ipaddress, username, password, dev,type):
    Domoticz.Log("SHELLY_SHSW_PM onCreate()")
    SHELLY_SHSW.create(mac, ipaddress, username, password, dev,type)

def onCommand(device_id, unit, command, Level, Color, username, password, Devices):
    Domoticz.Log("SHELLY_SHSW_PM onCommand()")
    SHELLY_SHSW.onCommand(device_id, unit, command, Level, Color, username, password, Devices)

def onHeartbeat(device, username, password):
    Domoticz.Log("SHELLY_SHSW_PM onHeartbeat()")
    SHELLY_SHSW.onHeartbeat(device, username, password)
