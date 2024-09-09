import DomoticzEx as Domoticz
from gen1 import SHELLY_SHSW
import requests
import json


ID = "SHSW-25"

def create(self, mac, ipaddress, username, password, dev,type):
    Domoticz.Log("SHELLY_SHSW25.onCommand()")
    SHELLY_SHSW.create(self, mac, ipaddress, username, password, dev,type)
    headers = {'content-type':'application/json'}
    try:
        response_shelly = requests.get("http://"+ipaddress+"/settings", headers=headers, auth=(username, password), timeout=(10,10))
        json_items = json.loads(response_shelly.text)
        response_shelly.close()

        rollers = None
        mode = ""
        name = ""
        for key, value in json_items.items():
            if key == "rollers":
                rollers = value
            if key == "mode":
                mode = value
            if key == "name":
                name = value
        deviceid = type+":"+mac+":"+ipaddress
        count = 2
        if mode == "roller":
            for roller in rollers:
                createRoller(deviceid,name, count, dev)
                count = count + 1
        if len(dev[deviceid].Units.items()) > 0:
            unitCheck = False
            for unit in dev[deviceid].Units.items():
                if unit[0] == 1:
                    if unit[1].Type != 80:
                        unit[1].Update(TypeName="Temperature")
                    unitCheck = True
            if unitCheck == False:
                Domoticz.Unit(name+" Temperature", DeviceID=deviceid, Unit=1, TypeName="Temperature", Used=1).Create()
        else:
            Domoticz.Unit(name+" Temperature", DeviceID=deviceid, Unit=1, TypeName="Temperature", Used=1).Create()
    except requests.exceptions.Timeout as e:
        Domoticz.Error(str(e))

def onCommand(self, device_id, unit, command, Level, Color, Devices):
    Domoticz.Log("SHELLY_SHSW25.onCommand()")
    SHELLY_SHSW.onCommand(self, device_id, unit, command, Level, Color, Devices)
    url = "http://"+device_id.rpartition(":")[-1]
    headers = {'content-type':'application/json'}
    if Devices[device_id].Units[unit].SwitchType == 21:
        #roller
        url = url + "/roller/" + str(unit-2)
        if str(command) == "Open":
            url = url + "?go=open"
        elif str(command) == "Close":
            url = url + "?go=close"
        elif str(command) == "Stop":
            url = url + "?go=stop"
        else:
            Domoticz.Log("Unknown command: "+str(command))
            return None
    Domoticz.Log("url: "+url)
    try:
        response = requests.get(url,headers=headers, auth=(self.username, self.password), timeout=(10,10))
        Domoticz.Debug(response.text)
        response.close()
    except requests.exceptions.Timeout as e:
        Domoticz.Error(str(e))

def onHeartbeat(self, device):
    Domoticz.Log("SHELLY_SHSW25.onHeartbeat()")
    SHELLY_SHSW.onHeartbeat(self, device)
    headers = {'content-type':'application/json'}
    try:
        request_shelly_status = requests.get("http://"+device.DeviceID.rpartition(":")[-1]+"/status",headers=headers, auth=(self.username, self.password), timeout=(10,10))
        #Domoticz.Log(request_shelly_status.text)
        json_request = json.loads(request_shelly_status.text)
        rollers = None
        for key, value in json_request.items():
            if key == "rollers":
                rollers = value
        if rollers is not None:
            #roller
            for roller in rollers:
                for roller_key, roller_value in roller.items():
                    if roller_key == "state":
                        #state
                        Domoticz.Debug("State")
                    if roller_key == "current_pos":
                        #currentpos
                        Domoticz.Debug("currentpos")
                        #check if roller is available
                        if len(device.Units) > 1:
                            if device.Units[2].Type == 244 and device.Units[2].SubType==73 and device.Units[2].SwitchType == 21:
                                device.Units[2].nValue=2
                                device.Units[2].sValue=str(roller_value)
                                device.Units[2].Update(Log=True)
        request_shelly_status.close()
    except requests.exceptions.Timeout as e:
        Domoticz.Error(str(e))

def createRoller(deviceid,name, count,dev):
    if name == "" or name is None:
        name = "Roller"
    if len(dev[deviceid].Units.items()) > 0:
        unitCheck = False
        for unit in dev[deviceid].Units.items():
            if unit[0] == count:
                if unit[1].Type != 244 and unit[1].SubType != 73 and unit[1].SwitchType != 21 and unit[1].Name != name:
                    unit[1].Type = 244
                    unit[1].SubType = 73
                    unit[1].SwitchType = 21
                    unit[1].Name = name
                    unit[1].Update(Log=True)
                unitCheck = True
        if unitCheck == False:
            Domoticz.Unit(Name=name,DeviceID=deviceid, Unit=count, Used=1, Type=244, Subtype=73, Switchtype=21).Create()
    else:
        Domoticz.Unit(Name=name,DeviceID=deviceid, Unit=count, Used=1, Type=244, Subtype=73, Switchtype=21).Create()
