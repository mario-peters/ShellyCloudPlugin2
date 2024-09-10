import DomoticzEx as Domoticz
import requests
import json
import SHELLY_Relay
import SHELLY_Meter
import random
from gen23 import SHELLY_Gen23_Auth

def create(mac, ipaddress, username, password, dev, type):
    Domoticz.Log("SHELLY_Gen23_SingleSwitch onCreate()")
    URL_SHELLY = f"http://"+ipaddress+"/rpc"
    method = "Switch.GetConfig"

    try:
        data_401:dict[str, str] = {}
        data_401 = SHELLY_Gen23_Auth.getData_401(URL_SHELLY, username, password, method)

        # cnonce = str(int(time.time()))
        cnonce = str(random.randint(1000000, 9999999))  # noqa: S311

        resp = SHELLY_Gen23_Auth.getResponse(data_401, username, password, cnonce)

        d = {
            "id": 1,
            "method": method,
            "params": {"id": 0},  # 0 = first switch/meter
            "auth": {
                "realm": data_401["realm"],
                "username": username,
                "nonce": data_401["nonce"],
                "cnonce": cnonce,
                "response": resp,
                "algorithm": "SHA-256",
            },
        }
        response = requests.post(URL_SHELLY, json=d, timeout=3)
        #Domoticz.Log(str(response))
        #res = json.loads(response.text)

        if response.status_code == 200:  # noqa: PLR2004
            data = json.loads(response.text)
            data = data["result"]
            #Domoticz.Log(str(data))

            name = data["name"]
            deviceid = type+":"+mac+":"+ipaddress
            count = 2
            relay = {"name":name}
            name = SHELLY_Relay.create(deviceid,relay, count, dev, type)
            meter = {"power":0,"total":0}
            SHELLY_Meter.create(deviceid,name, meter, count, dev)
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

        response.close()
    except requests.exceptions.Timeout as e:
        Domoticz.Error(str(e))

def onCommand(device_id, unit, command, Level, Hue, username, password, Devices):
    Domoticz.Log("SHELLY_Gen23_SingleSwitch onCommand()")
    URL_SHELLY = f"http://"+device_id.rsplit(":",1)[1]+"/rpc"
    method = "Switch.Set"

    try:
        data_401:dict[str, str] = {}
        data_401 = SHELLY_Gen23_Auth.getData_401(URL_SHELLY, username, password, method)

        # cnonce = str(int(time.time()))
        cnonce = str(random.randint(1000000, 9999999))  # noqa: S311

        resp = SHELLY_Gen23_Auth.getResponse(data_401, username, password, cnonce)

        comm = False
        if command == "On":
            comm = True

        d = {
            "id": 1,
            "method": method,
            "params": {"id": 0, "on": comm},  # 0 = first switch/meter
            "auth": {
                "realm": data_401["realm"],
                "username": username,
                "nonce": data_401["nonce"],
                "cnonce": cnonce,
                "response": resp,
                "algorithm": "SHA-256",
            },
        }
        response = requests.post(URL_SHELLY, json=d, timeout=3)
        #Domoticz.Log(str(response))
        if response.status_code == 200:
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
        response.close()
    except requests.exceptions.Timeout as e:
        Domoticz.Error(str(e))

def onHeartbeat(device, username, password):
    Domoticz.Log("SHELLY_Gen23_SingleSwitch onHeartbeat()")
    URL_SHELLY = f"http://"+device.DeviceID.rsplit(":",1)[1]+"/rpc"
    method = "Switch.GetStatus"

    try:
        data_401:dict[str, str] = {}
        data_401 = SHELLY_Gen23_Auth.getData_401(URL_SHELLY, username, password, method)

        # cnonce = str(int(time.time()))
        cnonce = str(random.randint(1000000, 9999999))  # noqa: S311

        resp = SHELLY_Gen23_Auth.getResponse(data_401, username, password, cnonce)

        d = {
            "id": 1,
            "method": method,
            "params": {"id": 0},  # 0 = first switch/meter
            "auth": {
                "realm": data_401["realm"],
                "username": username,
                "nonce": data_401["nonce"],
                "cnonce": cnonce,
                "response": resp,
                "algorithm": "SHA-256",
            },
        }
        response = requests.post(URL_SHELLY, json=d, timeout=3)
        #Domoticz.Log(str(response.text))
        if response.status_code == 200:
            data = json.loads(response.text)
            for unit in device.Units.items():
                if unit[0] == 1:
                    unit[1].sValue = str(data["result"]["temperature"]["tC"])
                    unit[1].Update(Log=True)
                if unit[0] == 2:
                    if data["result"]["output"] == True:
                        unit[1].nValue = 1
                        unit[1].sValue = "On"
                    else:
                        unit[1].nValue = 0
                        unit[1].sValue = "Off"
                    unit[1].Update(Log=True)
                elif unit[0] == 12:
                    unit[1].nValue = 0
                    unit[1].sValue = str(data["result"]["apower"])
                    unit[1].Update(Log=True)
                elif unit[0] == 22:
                    total = int(data["result"]["aenergy"]["total"])
                    total = total/60
                    unit[1].nValue = 0
                    unit[1].sValue = str(data["result"]["apower"])+";"+str(total)
                    unit[1].Update(Log=True)
        response.close()
    except requests.exceptions.Timeout as e:
        Domoticz.Error(str(e))
