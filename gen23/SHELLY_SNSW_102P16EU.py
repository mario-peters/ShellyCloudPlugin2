import DomoticzEx as Domoticz
from gen23 import SHELLY_SNSW_X02P16EU

ID = "SNSW-102P16EU"

def create(mac, ipaddress, username, password, dev,type):
    Domoticz.Log("SHELLY_SNSW_102P16EU onCreate()")
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
            if data["profile"] == "switch":
                SHELLY_SNSW_X02P16EU.create(mac, ipaddress, username, password, dev,type)
            elif data["profile"] == "cover":
                Domoticz.Unit(name+" Temperature", DeviceID=deviceid, Unit=1, TypeName="Temperature", Used=1).Create()
                Domoticz.Unit(Name=name,DeviceID=deviceid, Unit=count, Used=1, Type=244, Subtype=73, Switchtype=21, Description=type).Create()
        response.close()
    except requests.exceptions.Timeout as e:
        Domoticz.Error(str(e))
    SHELLY_SNSW_X02P16EU.create(mac, ipaddress, username, password, dev,type)

def onCommand(self, device_id, unit, command, Level, Color, Devices):
    Domoticz.Debug("SHELLY_SNSW_102P16EU onCommand()")
    SHELLY_SNSW_X02P16EU.onCommand(self, device_id, unit, command, Level, Color, Devices)

def onHeartbeat(self, device):
    Domoticz.Debug("SHELLY_SNSW_102P16EU onHeartbeat()")
    SHELLY_SNSW_X02P16EU.onHeartbeat(self, device)
