import DomoticzEx as Domoticz
import requests
import json
import SHELLY_Relay
import SHELLY_Meter

def create(self, mac, ipaddress, username, password, dev,type):
    Domoticz.Log("SHELLY_SHSW onCreate()")
    headers = {'content-type':'application/json'}
    try:
        response_shelly = requests.get("http://"+ipaddress+"/settings", headers=headers, auth=(username, password), timeout=(10,10))
        json_items = json.loads(response_shelly.text)
        response_shelly.close()

        relays = None
        num_meters = None
        hostname = ""
        mode = ""
        name = ""
        for key, value in json_items.items():
            if key == "relays":
                relays = value
            if key == "mode":
                mode = value
            if key == "device":
                for q, v in value.items():
                    if q == "hostname":
                        hostname = v
            if key == "name":
                name = value
        deviceid = type+":"+mac+":"+ipaddress
        count = 2
        if mode == "relay":
           for relay in relays:
               name = SHELLY_Relay.create(deviceid,relay, count, dev,type)
               meter = {"power":0,"total":0}
               SHELLY_Meter.create(deviceid,name, meter, count, dev)
               count = count + 1
        aDevice = dev.get(deviceid)
        if aDevice is not None and len(aDevice.Units.items()) > 0:
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
    Domoticz.Log("SHELLY_SHSW.onCommand()")
    url = "http://"+device_id.rpartition(":")[-1]
    headers = {'content-type':'application/json'}
    #relay
    url = url + "/relay/" + str(unit-2)
    if str(command) == "On":
        url = url + "?turn=on"
    elif str(command) == "Off":
        url = url + "?turn=off"
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
    if Devices[device_id].Units[unit].SwitchType != 21:
        if str(command) == "On":
            Devices[device_id].Units[unit].nValue = 1
            Devices[device_id].Units[unit].sValue = "On"
            Devices[device_id].Units[unit].Update(Log=True)
        elif str(command) == "Off":
            Devices[device_id].Units[unit].nValue = 0
            Devices[device_id].Units[unit].sValue = "Off"
            Devices[device_id].Units[unit].Update(Log=True)
        else:
            Domoticz.Log("Update "+Devices[device_id].Units[unit].Name+": Unknown command: "+str(command))

def onHeartbeat(self, device):
    Domoticz.Log("SHELLY_SHSW.onHeartbeat()")
    headers = {'content-type':'application/json'}
    try:
        request_shelly_status = requests.get("http://"+device.DeviceID.rpartition(":")[-1]+"/status",headers=headers, auth=(self.username, self.password), timeout=(10,10))
        #Domoticz.Log(request_shelly_status.text)
        json_request = json.loads(request_shelly_status.text)
        relays = None
        meters = None
        for key, value in json_request.items():
            if key == "relays":
                relays = value
            if key == "meters":
                meters = value
            if key == "temperature":
                #Devices[1].Update(nValue=Devices[1].nValue, sValue=str(value))
                #if len(device.Units) > 0:
                for unit in device.Units.items():
                    #Domoticz.Log(device.DeviceID.rpartition(":")[-1]+" --> "+str(unit[0]))
                    if unit[0] == 1:
                        if unit[1].Type == 80:
                            unit[1].sValue = str(value)
                            unit[1].Update(Log=True)
                    #if unit.Unit == 1:
                    #if device.Units[1].Type == 80:
                        #device.Units[1].sValue = str(value)
                        #device.Units[1].Update(Log=True)
        if relays is not None:
            #check if all relays and meters are there for SHSW25
            if len(device.Units) > 3:
                count = 1
                for relay in relays:
                    SHELLY_Relay.updateRelay(relay, count, device)
                    SHELLY_Meter.updateMeter(meters[count-1], count, self, device)
                    count = count + 1
        request_shelly_status.close()
    except requests.exceptions.Timeout as e:
        Domoticz.Error(str(e))
