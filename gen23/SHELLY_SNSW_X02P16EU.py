import DomoticzEx as Domoticz
from gen23 import SHELLY_Gen23_Auth
import requests
import random
import json
import SHELLY_Relay
import SHELLY_Meter

def create(mac, ipaddress, username, password, dev,type):
    Domoticz.Debug("SHELLY_SNSW_X02P16EU onCreate()")
    URL_SHELLY = f"http://"+ipaddress+"/rpc"
    method = "Sys.GetConfig"

    try:
        data_401:dict[str, str] = {}
        data_401 = SHELLY_Gen23_Auth.getData_401(URL_SHELLY, method)

        cnonce = str(random.randint(1000000, 9999999))  # noqa: S311

        resp = SHELLY_Gen23_Auth.getResponse(data_401, username, password, cnonce)

        d = {
            "id": 1,
            "method": method,
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
            data = data["result"]["device"]
            name = data["name"]
            deviceid = type+":"+mac+":"+ipaddress
            Domoticz.Unit(name+" Temperature", DeviceID=deviceid, Unit=1, TypeName="Temperature", Used=1).Create()
            if data["profile"] == "switch":
                methodSwitch = "Switch.GetConfig"
                data_401 = SHELLY_Gen23_Auth.getData_401(URL_SHELLY, methodSwitch)
                cnonce = str(random.randint(1000000, 9999999))
                resp = SHELLY_Gen23_Auth.getResponse(data_401, username, password, cnonce)
                d = {
                    "id":1,
                    "method": methodSwitch,
                    "params": {"id": 0},
                    "auth": {
                        "realm": data_401["realm"],
                        "username": username,
                        "nonce": data_401["nonce"],
                        "cnonce": cnonce,
                        "response": resp,
                        "algorithm": "SHA-256",
                    },
                }
                responseSwitch0 = requests.post(URL_SHELLY, json=d, timeout=3)
                Domoticz.Log(str(responseSwitch0.text))
                meter = {"power":0,"total":0}
                if responseSwitch0.status_code == 200:
                    dataSwitch0 = json.loads(responseSwitch0.text)
                    dataSwitch0 = dataSwitch0["result"]
                    relay = {"name": name+" - "+dataSwitch0["name"]}
                    name = SHELLY_Relay.create(deviceid, relay, 2, dev, type)
                    SHELLY_Meter.create(deviceid, name, meter, 2, dev)
                responseSwitch0.close()

                d = {
                    "id":1,
                    "method": methodSwitch,
                    "params": {"id": 1},
                    "auth": {
                        "realm": data_401["realm"],
                        "username": username,
                        "nonce": data_401["nonce"],
                        "cnonce": cnonce,
                        "response": resp,
                        "algorithm": "SHA-256",
                    },
                }
                responseSwitch1 = requests.post(URL_SHELLY, json=d, timeout=3)
                Domoticz.Log(str(responseSwitch1.text))
                if responseSwitch1.status_code == 200:
                    dataSwitch1 = json.loads(responseSwitch1.text)
                    dataSwitch1 = dataSwitch1["result"]
                    relay = {"name": data["name"]+" - "+dataSwitch1["name"]}
                    name = SHELLY_Relay.create(deviceid, relay, 3, dev, type)
                    SHELLY_Meter.create(deviceid, name, meter, 3, dev)
                responseSwitch1.close()
            elif data["profile"] == "cover":
                Domoticz.Log("TODO profile=cover")
        response.close()
    except requests.exceptions.Timeout as e:
        Domoticz.Error(str(e))

def onCommand(self, device_id, unit, command, Level, Color, Devices):
    Domoticz.Debug("SHELLY_SNSW_X02P16EU onCommand()")

def onHeartbeat(self, device):
    Domoticz.Debug("SHELLY_SNSW_X02P16EU onHeartbeat()")
