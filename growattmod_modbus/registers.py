from enum import Enum

from . import datatypes
from . import mappings


class RegisterType(Enum):
    HoldingRegister = 3
    InputRegister = 4
	
	
class AccessType(Enum):
    RO = "ro"
    RW = "rw"
    WO = "wo"


class Register:
    register_tpye: RegisterType
    address: int
    quantity: int
    data_type: datatypes.DataType
    gain: float
    unit: str
    access_type: AccessType
    mapping: dict

    def __init__(self, register_type, address, quantity, data_type, gain, unit, access_type, mapping):
        self.register_type = register_type
        self.address = address
        self.quantity = quantity
        self.data_type = data_type
        self.gain = gain
        self.unit = unit
        self.access_type = access_type
        self.mapping = mapping


class InverterEquipmentRegister(Enum):

   # TL3-X(MAX、MID、MAC Type)：
   #   03 register range：0~124,125~249；
   #   04 register range：0~124,125~249
   #
   bAfciStatus = Register(RegisterType.InputRegister, 238, 1, datatypes.DataType.INT16_BE, 10, None, AccessType.RO, mappings.bAfciStatus)
   SN = Register(RegisterType.HoldingRegister, 23, 10, datatypes.DataType.STRING, None, None, AccessType.RO, None)
   TP = Register(RegisterType.HoldingRegister, 44, 1, datatypes.DataType.INT16_BE, None, None, AccessType.RO, None)
     # Input tracker num and output phase num
     # Eg:0x020: 3 is two MPPT and 3ph output
   NumberOfPVStrings = Register(RegisterType.HoldingRegister, 183, 1, datatypes.DataType.UINT16_BE, 1, None, AccessType.RO, None)
   OPFullwatt = Register(RegisterType.InputRegister, 102, 2, datatypes.DataType.UINT32_BE, 1, "W", AccessType.RO, None)  
   InverterStatus = Register(RegisterType.InputRegister, 0, 1, datatypes.DataType.INT16_BE, None, None, AccessType.RO, mappings.InverterStatus)
   InputPower = Register(RegisterType.InputRegister, 1, 2, datatypes.DataType.INT32_BE, 10, "W", AccessType.RO, None)
   PV1Voltage = Register(RegisterType.InputRegister, 3, 1, datatypes.DataType.INT16_BE, 10, "V", AccessType.RO, None)
   PV1Current = Register(RegisterType.InputRegister, 4, 1, datatypes.DataType.INT16_BE, 10, "A", AccessType.RO, None)
   PV1Power = Register(RegisterType.InputRegister, 5, 2, datatypes.DataType.INT32_BE, 10, "W", AccessType.RO, None)
   PV2Voltage = Register(RegisterType.InputRegister, 7, 1, datatypes.DataType.INT16_BE, 10, "V", AccessType.RO, None)
   PV2Current = Register(RegisterType.InputRegister, 8, 1, datatypes.DataType.INT16_BE, 10, "A", AccessType.RO, None)
   PV2Power = Register(RegisterType.InputRegister, 9, 2, datatypes.DataType.INT32_BE, 10, "W", AccessType.RO, None)
   OutputPower = Register(RegisterType.InputRegister, 35, 2, datatypes.DataType.INT32_BE, 10, "W", AccessType.RO, None)
   GridFrequency = Register(RegisterType.InputRegister, 37, 1, datatypes.DataType.UINT16_BE, 100, "Hz", AccessType.RO, None)
   PhaseAVoltage = Register(RegisterType.InputRegister, 38, 1, datatypes.DataType.UINT16_BE, 10, "V", AccessType.RO, None)
   PhaseBVoltage = Register(RegisterType.InputRegister, 42, 1, datatypes.DataType.UINT16_BE, 10, "V", AccessType.RO, None)
   PhaseCVoltage = Register(RegisterType.InputRegister, 46, 1, datatypes.DataType.UINT16_BE, 10, "V", AccessType.RO, None)
   PhaseACurrent = Register(RegisterType.InputRegister, 39, 1, datatypes.DataType.INT16_BE, 10, "A", AccessType.RO, None)
   PhaseBCurrent = Register(RegisterType.InputRegister, 43, 1, datatypes.DataType.INT16_BE, 10, "A", AccessType.RO, None)
   PhaseCCurrent = Register(RegisterType.InputRegister, 47, 1, datatypes.DataType.INT16_BE, 10, "A", AccessType.RO, None)
   PhaseAPower = Register(RegisterType.InputRegister, 40, 2, datatypes.DataType.INT32_BE, 10, "VA", AccessType.RO, None)
   PhaseBPower = Register(RegisterType.InputRegister, 44, 2, datatypes.DataType.INT32_BE, 10, "VA", AccessType.RO, None)
   PhaseCPower = Register(RegisterType.InputRegister, 48, 2, datatypes.DataType.INT32_BE, 10, "VA", AccessType.RO, None)
   Eactotal = Register(RegisterType.InputRegister, 55, 2, datatypes.DataType.UINT32_BE, 10, "kWh", AccessType.RO, None)
