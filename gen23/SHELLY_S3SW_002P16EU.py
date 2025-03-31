import DomoticzEx as Domoticz
from gen23 import SHELLY_SNSW_102P16EU

ID = "S3SW-002P16EU"

def create(mac, ipaddress, username, password, dev,type):
    Domoticz.Debug("SHELLY_S3SW_002P16EU onCreate()")
    SHELLY_SNSW_102P16EU.create(mac, ipaddress, username, password, dev,type)

def onCommand(device_id, unit, command, Level, Color, username, password, Devices):
    Domoticz.Debug("SHELLY_S3SW_002P16EU onCommand()")
    SHELLY_SNSW_102P16EU.onCommand(device_id, unit, command, Level, Color, username, password, Devices)

def onHeartbeat(device, username, password):
    Domoticz.Debug("SHELLY_S3SW_002P16EU onHeartbeat()")
    SHELLY_SNSW_102P16EU.onHeartbeat(device, username, password)
