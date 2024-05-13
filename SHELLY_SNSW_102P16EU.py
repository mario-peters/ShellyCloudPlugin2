import DomoticzEx as Domoticz
import SHELLY_SNSW_X02P16EU

ID = "SNSW-102P16EU"

def create(self, mac, ipaddress, username, password, dev,type):
    Domoticz.Log("SHELLY_SNSW_102P16EU onCreate()")
    SHELLY_SNSW_X02P16EU.create(self, mac, ipaddress, username, password, dev,type)

def onCommand(self, device_id, unit, command, Level, Color, Devices):
    Domoticz.Debug("SHELLY_SNSW_102P16EU onCommand()")
    SHELLY_SNSW_X02P16EU.onCommand(self, device_id, unit, command, Level, Color, Devices)

def onHeartbeat(self, device):
    Domoticz.Debug("SHELLY_SNSW_102P16EU onHeartbeat()")
    SHELLY_SNSW_X02P16EU.onHeartbeat(self, device)
