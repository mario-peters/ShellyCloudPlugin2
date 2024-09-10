import DomoticzEx as Domoticz

SHELLY_EM="SHEM"
SHELLY_3EM="SHEM-3"

def create(deviceid,name, meter, count, dev):
    power = 0.0
    for key, value in meter.items():
        if key == "power":
            power = value
            createPower(deviceid,name, power, count, dev)
    for key, value in meter.items():
        if key == "total":
            createTotal(deviceid,name, power, value, count, dev)

def createPower(deviceid,name, power, count, dev):
    if len(dev[deviceid].Units.items()) > 0:
        unitCheck = False
        for unit in dev[deviceid].Units.items():
            if unit[0] == 10+count:
                if unit[1].Type != 248 and unit[1].SubType != 1 and unit[1].Name != name+"_power":
                    unit[1].Type = 248
                    unit[1].SubType = 1
                    unit[1].Name = name+"_power"
                    unit[1].Update(Log=True)
                unitCheck = True
        if unitCheck == False:
            Domoticz.Unit(DeviceID=deviceid,Name=name+"_power", Unit=10+count, Used=1, Type=248, Subtype=1).Create()
    else:
        Domoticz.Unit(DeviceID=deviceid,Name=name+"_power", Unit=10+count, Used=1, Type=248, Subtype=1).Create()

    #dev[deviceid].Units[10+count].nValue=0
    #dev[deviceid].Units[10+count].sValue=str(power)
    #dev[deviceid].Units[10+count].Update(Log=True)

def createTotal(deviceid,name, power, value, count, dev):
    if len(dev[deviceid].Units.items()) > 0:
        unitCheck = False
        for unit in dev[deviceid].Units.items():
            if unit[0] == 20+count:
                if unit[1].Type != 243 and unit[1].SubType != 29 and unit[1].Name != name+"_kWh":
                    unit[1].Type = 243
                    unit[1].SubType = 29 
                    unit[1].Name = name+"_kWh"
                    unit[1].Update(Log=True)
                unitCheck = True
        if unitCheck == False:
            Domoticz.Unit(DeviceID=deviceid,Name=name+"_kWh", Unit=20+count, Used=1, Type=243, Subtype=29).Create()
    else:
        Domoticz.Unit(DeviceID=deviceid,Name=name+"_kWh", Unit=20+count, Used=1, Type=243, Subtype=29).Create()

    total = int(value)
    total = total/60
    total = int(total)
    #dev[deviceid].Units[20+count].nValue=0
    #dev[deviceid].Units[20+count].sValue=str(power)+";"+str(total)
    #dev[deviceid].Units[20+count].Update(Log=True)

def updateMeter(meter, count, device):
    power = ""
    for key, value in meter.items():
        if key == "power":
            power = str(value)
            if device.Units[11+count].Type == 248 and device.Units[11+count].SubType == 1:
                device.Units[11+count].nValue = 0
                device.Units[11+count].sValue = power
                device.Units[11+count].Update(Log=True)
    for key, value in meter.items():
        if key == "total":
            total=int(value)
            if device.DeviceID.startswith(SHELLY_EM) == False and device.DeviceID.startswith(SHELLY_3EM) == False:
                total = total/60
            total=int(total)
            if device.Units[21+count].Type==243 and device.Units[21+count].SubType==29:
                device.Units[21+count].nValue = 0
                device.Units[21+count].sValue = power+";"+str(total)
                device.Units[21+count].Update(Log=True)
        if key == "total_returned":
            total = int(value)
            total = total/60
            total = int(total)
            if device.Units[31+count].Type==243 and device.Units[31+count].SubType==29:
                device.Units[31+count].nValue = 0
                device.Units[31+count].sValue = power+";"+str(total)
                device.Units[31+count].Update(Log=True)
