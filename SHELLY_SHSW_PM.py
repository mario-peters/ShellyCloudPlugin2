import DomoticzEx as Domoticz
import SHELLY_SHSW

ID = "SHSW-PM"

def create(self, mac, ipaddress, username, password, dev,type):
    SHELLY_SHSW.create(self, mac, ipaddress, username, password, dev,type)

def onCommand(self, device_id, unit, command, Level, Color, Devices):
    Domoticz.Debug("SHELLY_SHSW_PM onCommand()")
    SHELLY_SHSW.onCommand(self, device_id, unit, command, Level, Color, Devices)

def onHeartbeat(self, device):
    Domoticz.Debug("SHELLY_SHSW_PM onHeartbeat()")
    SHELLY_SHSW.onHeartbeat(self, device)
