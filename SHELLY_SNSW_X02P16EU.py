import DomoticzEx as Domoticz

def create(self, mac, ipaddress, username, password, dev,type):
    Domoticz.Debug("SHELLY_SNSW_X02P16EU onCreate()")

def onCommand(self, device_id, unit, command, Level, Color, Devices):
    Domoticz.Debug("SHELLY_SNSW_X02P16EU onCommand()")

def onHeartbeat(self, device):
    Domoticz.Debug("SHELLY_SNSW_X02P16EU onHeartbeat()")
