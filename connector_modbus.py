from growattmod_modbus import inverter
from growattmod_modbus import registers

from dbus.mainloop.glib import DBusGMainLoop

from settings import GrowattMODSettings

state1Readable = {
    0: "waiting",
    1: "normal",
    3: "fault"
}


class ModbusDataCollector2000Delux:
    def __init__(self, host='192.168.178.56', port=502, modbus_unit=1): 
        self.invGroMOD = inverter.GroMOD(host=host, port=port, modbus_unit=modbus_unit)

    def getData(self):
        # the connect() method internally checks whether there's already a connection
        if not self.invGroMOD.connect():
            print("Connection error Modbus TCP")
            return None

        data = {}

        dbuspath = {
            '/Ac/Power': {'initial': 0, "groMOD": registers.InverterEquipmentRegister.OutputPower},
            '/Ac/L1/Current': {'initial': 0, "groMOD": registers.InverterEquipmentRegister.PhaseACurrent},
            '/Ac/L1/Voltage': {'initial': 0, "groMOD": registers.InverterEquipmentRegister.PhaseAVoltage},
            '/Ac/L1/Power': {'initial': 0, "groMOD": registers.InverterEquipmentRegister.PhaseAPower},
            '/Ac/L2/Current': {'initial': 0, "groMOD": registers.InverterEquipmentRegister.PhaseBCurrent},
            '/Ac/L2/Voltage': {'initial': 0, "groMOD": registers.InverterEquipmentRegister.PhaseBVoltage},
            '/Ac/L2/Power': {'initial': 0, "groMOD": registers.InverterEquipmentRegister.PhaseBPower},
            '/Ac/L3/Current': {'initial': 0, "groMOD": registers.InverterEquipmentRegister.PhaseCCurrent},
            '/Ac/L3/Voltage': {'initial': 0, "groMOD": registers.InverterEquipmentRegister.PhaseCVoltage},
            '/Ac/L3/Power': {'initial': 0, "groMOD": registers.InverterEquipmentRegister.PhaseCPower},
            '/Dc/Power': {'initial': 0, "groMOD": registers.InverterEquipmentRegister.InputPower},
            '/Ac/MaxPower': {'initial': 0, "groMOD": registers.InverterEquipmentRegister.OPFullwatt},
        }

        for k, v in dbuspath.items():
            s = v.get("groMOD")
            data[k] = self.invGroMOD.read(s)

        state1 = self.invGroMOD.read(registers.InverterEquipmentRegister.InverterStatus)
        state1_string = ";".join([val for key, val in state1Readable.items() if int(state1)&key>0])
        data['/Status'] = state1_string

        # data['/Ac/StatusCode'] = statuscode

        energy_forward = self.invGroMOD.read(registers.InverterEquipmentRegister.Eactotal)
        data['/Ac/Energy/Forward'] = energy_forward
        # There is no Modbus register for the phases
        data['/Ac/L1/Energy/Forward'] = round(energy_forward / 3.0, 2)
        data['/Ac/L2/Energy/Forward'] = round(energy_forward / 3.0, 2)
        data['/Ac/L3/Energy/Forward'] = round(energy_forward / 3.0, 2)

        freq = self.invGroMOD.read(registers.InverterEquipmentRegister.GridFrequency)
        data['/Ac/L1/Frequency'] = freq
        data['/Ac/L2/Frequency'] = freq
        data['/Ac/L3/Frequency'] = freq

        return data

    def getStaticData(self):
        # the connect() method internally checks whether there's already a connection
        if not self.invGroMOD.connect():
            print("Connection error Modbus TCP")
            return None

        try:
            data = {}
            data['bAfciStatus'] = self.invGroMOD.read(registers.InverterEquipmentRegister.bAfciStatus)
            data['SN'] = self.invGroMOD.read(registers.InverterEquipmentRegister.SN)
            data['TP'] = self.invGroMOD.read(registers.InverterEquipmentRegister.TP)
            #data['ModelID'] = "123"  #self.invGroMOD.read(registers.InverterEquipmentRegister.ModelID)
            data['Model'] = "TL3-X" #str(self.invGroMOD.read_formatted(registers.InverterEquipmentRegister.Model)).replace('\0','')
            data['NumberOfPVStrings'] = self.invGroMOD.read(registers.InverterEquipmentRegister.NumberOfPVStrings)
            data['NumberOfMPPTrackers'] = 2 #self.invGroMOD.read(registers.InverterEquipmentRegister.NumberOfMPPTrackers)
            return data

        except:
            print("Problem while getting static data modbus TCP")
            return None



## Just for testing ##
if __name__ == "__main__":
    DBusGMainLoop(set_as_default=True)
    settings = GrowattMODSettings()
    inverter = inverter.GroMOD(host=settings.get("modbus_host"), port=settings.get("modbus_port"), modbus_unit=settings.get("modbus_unit"))
    #inverter = inverter.GroMOD(host="192.168.178.56", port=settings.get("modbus_port"), modbus_unit=settings.get("modbus_unit"))
    inverter.connect()
    if inverter.isConnected():
       attrs = (getattr(registers.InverterEquipmentRegister, name) for name in
                dir(registers.InverterEquipmentRegister))
       datata = dict()
       for f in attrs:
	     
           if isinstance(f, registers.InverterEquipmentRegister):
               datata[f.name] = inverter.read_formatted(f)
   
       for k, v in datata.items():
           print(f"{k}: {v}")
