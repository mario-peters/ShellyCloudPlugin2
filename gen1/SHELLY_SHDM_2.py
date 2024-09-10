import DomoticzEx as Domoticz
import SHELLY_Meter
import requests
import json

ID = "SHDM-2"

def create(mac, ipaddress, username, password, dev, type):
    Domoticz.Log("SHELLY_SHDM_2 onCreate()")
    deviceid = type+":"+mac+":"+ipaddress
    headers = {'content-type':'application/json'}
    try:
        response_shelly = requests.get("http://"+ipaddress+"/settings", headers=headers, auth=(username, password), timeout=(10,10))
        json_items = json.loads(response_shelly.text)
        response_shelly.close()
        name = json_items["name"]

        Domoticz.Unit(Name=name,DeviceID=deviceid, Unit=2, Used=1, Type=244, Subtype=73, Switchtype=7, Description=ID).Create()
        if json_items["lights"][0]["ison"] == True:
            dev[deviceid].Units[2].nValue = 1
            dev[deviceid].Units[2].sValue = "On"
        else:
            dev[deviceid].Units[2].nValue = 0
            dev[deviceid].Units[2].sValue = "Off"
        dev[deviceid].Units[2].Update(Log=True)
        meter = {"power":0,"total":0}
        SHELLY_Meter.create(deviceid,name, meter, 2, dev)
        Domoticz.Unit(name+" Temperature", DeviceID=deviceid, Unit=1, TypeName="Temperature", Used=1).Create()
    except requests.exceptions.Timeout as e:
        Domoticz.Error(str(e))

def onCommand(device_id, unit, command, Level, Hue, username, password, Devices):
    Domoticz.Log("SHELLY_SHDM_2 onCommand()")
    url = "http://"+device_id.rpartition(":")[-1]+"/light/0"
    if str(command) == "On":
        url = url + "?turn=on"
    elif str(command) == "Off":
        url = url + "?turn=off"
    elif str(command) == "Set Level":
        url = url + "?turn=on&brightness=" + str(Level)
    Domoticz.Log(url)
    headers = {'content-type':'application/json'}
    try:
        response = requests.get(url,headers=headers, auth=(username, password), timeout=(10,10))
        Domoticz.Debug(response.text)
        if response.status_code == 200:
            for unit in Devices[device_id].Units.items():
                if unit[0] == 2:
                    unit[1].sValue = str(Level)
                    if str(command) == "On" or str(command) == "Set Level" :
                        unit[1].nValue = 1
                    else:
                        unit[1].nValue = 0
                    unit[1].Update(Log=True)
        response.close()
    except requests.exceptions.Timeout as e:
        Domoticz.Error(str(e))

def onHeartbeat(device, username, password):
    Domoticz.Log("SHELLY_SHDM_2 onHeartbeat()")
    headers = {'content-type':'application/json'}
    try:
        response = requests.get("http://"+device.DeviceID.rpartition(":")[-1]+"/status",headers=headers, auth=(username, password), timeout=(10,10))

        if response.status_code == 200:
            data = json.loads(response.text)
            for unit in device.Units.items():
                if unit[0] == 1:
                    unit[1].sValue = str(data["tmp"]["tC"])
                    unit[1].Update(Log=True)
                if unit[0] == 2:
                    unit[1].sValue = str(data["lights"][0]["brightness"])
                    if data["lights"][0]["ison"] == True:
                        unit[1].nValue = 1
                    else:
                        unit[1].nValue = 0
                    unit[1].Update(Log=True)
                elif unit[0] == 12:
                    unit[1].nValue = 0
                    unit[1].sValue = str(data["meters"][0]["power"])
                    unit[1].Update(Log=True)
                elif unit[0] == 22:
                    total = int(data["meters"][0]["total"])
                    total = total/60
                    unit[1].nValue = 0
                    unit[1].sValue = str(data["meters"][0]["power"])+";"+str(total)
                    unit[1].Update(Log=True)
        response.close()
    except requests.exceptions.Timeout as e:
        Domoticz.Error(str(e))
