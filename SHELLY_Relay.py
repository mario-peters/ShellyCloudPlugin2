import DomoticzEx as Domoticz

def create(deviceid, relay, count, dev):
    name = ""
    ison = False
    for key, value in relay.items():
        if key == "name":
            name = value
        if key == "ison":
            ison = value
    if name == "" or name is None:
        name = "Relay"+str(count-1)
    #device = dev[deviceid]
    device = dev.get(deviceid)
    if device is not None:
        if len(dev[deviceid].Units.items()) > 0:
            unitCheck = False
            for unit in dev[deviceid].Units.items():
                if unit[0] == count:
                    if unit[1].Type != 244 and unit[1].SubType != 73 and unit[1].Name != name:
                        unit[1].Type = 244
                        unit[1].SubType = 73
                        unit[1].Name = name
                        unit[1].Update(Log=True)
                    unitCheck = True
            if unitCheck == False:
                Domoticz.Unit(Name=name,DeviceID=deviceid, Unit=count, Used=1, Type=244, Subtype=73).Create()
        else:
            Domoticz.Unit(Name=name,DeviceID=deviceid, Unit=count, Used=1, Type=244, Subtype=73).Create()
    else:
        Domoticz.Unit(Name=name,DeviceID=deviceid, Unit=count, Used=1, Type=244, Subtype=73).Create()
 
    #Domoticz.Unit(Name=name,DeviceID=deviceid, Unit=count, Used=1, Type=244, Subtype=73).Create()
    if ison == True:
        dev[deviceid].Units[count].nValue=1
        dev[deviceid].Units[count].sValue="On"
        dev[deviceid].Units[count].Update(Log=True)
    return name

def updateRelay(relay, count, device):
    if device.Units[1+count].Type == 244 and device.Units[1+count].SubType == 73:
        for key, value in relay.items():
            if key == "ison":
                if value:
                    if device.Units[1+count].nValue != 1:
                        device.Units[1+count].nValue = 1
                        device.Units[1+count].sValue = "On"
                        device.Units[1+count].Update(Log=True)
                else:
                    device.Units[1+count].nValue = 0
                    device.Units[1+count].sValue = "Off"
                    device.Units[1+count].Update(Log=True)
