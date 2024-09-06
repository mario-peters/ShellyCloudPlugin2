import DomoticzEx as Domoticz
from gen23 import SHELLY_Gen23_SingleSwitch

ID = "S3SW-001P8EU"

def create(mac, ipaddress, username, password, dev, type):
    Domoticz.Log("SHELLY_S3SW_001P8EU onCreate()")
    SHELLY_Gen23_SingleSwitch.create(mac, ipaddress, username, password, dev, type)

def onCommand(device_id, unit, command, Level, Hue, username, password, Devices):
    Domoticz.Log("SHELLY_S3SW_001P8EU onCommand()")
    SHELLY_Gen23_SingleSwitch.onCommand(device_id, unit, command, Level, Hue, username, password, Devices)

def onHeartbeat(device, username, password):
    Domoticz.Log("SHELLY_S3SW_001P8EU onHeartbeat()")
    SHELLY_Gen23_SingleSwitch.onHeartbeat(device, username, password)
