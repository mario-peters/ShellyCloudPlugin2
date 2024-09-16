import DomoticzEx as Domoticz
from gen23 import SHELLY_SNSW_X02P16EU

ID = "SNSW-002P16EU"

def create(mac, ipaddress, username, password, dev,type):
    Domoticz.Debug("SHELLY_SNSW_002P16EU onCreate()")
    SHELLY_SNSW_X02P16EU.create(mac, ipaddress, username, password, dev,type)

def onCommand(device_id, unit, command, Level, Color, Devices):
    Domoticz.Debug("SHELLY_SNSW_002P16EU onCommand()")
    SHELLY_SNSW_X02P16EU.onCommand(device_id, unit, command, Level, Color, Devices)

def onHeartbeat(device):
    Domoticz.Debug("SHELLY_SNSW_002P16EU onHeartbeat()")
    SHELLY_SNSW_X02P16EU.onHeartbeat(device)
