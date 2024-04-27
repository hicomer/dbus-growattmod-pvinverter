import logging
import time

from . import registers
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException, ConnectionException

from . import datatypes

logging.basicConfig(level=logging.INFO)

class GroMOD:
    def __init__(self, host, port=502, timeout=5, wait=2, modbus_unit=1):
        self.wait = wait
        self.modbus_unit = modbus_unit
        self.inverter = ModbusTcpClient(host, port, timeout=timeout)

    def connect(self):
        if not self.isConnected():
            self.inverter.connect()
            time.sleep(self.wait)
            if self.isConnected():
                logging.info('Successfully connected to inverter')
                return True
            else:
                logging.error('Connection to inverter failed')
                return False
        else:
            return True

    def disconnect(self):
        """Close the underlying tcp socket"""
        self.inverter.close()

    def isConnected(self):
        """Check if underlying tcp socket is open"""
        return self.inverter.is_socket_open()

    def read_raw_value(self, register):
        if not self.isConnected():
            raise ValueError('Inverter is not connected')

        try:
            #logging.info("To read register: %s" % (register.value.address))
			
            if register.value.register_type == registers.RegisterType.InputRegister:
               register_value = self.inverter.read_input_registers(register.value.address, register.value.quantity, unit=self.modbus_unit)
            else:
               register_value = self.inverter.read_holding_registers(register.value.address, register.value.quantity, unit=self.modbus_unit)
            
            if type(register_value) == ModbusIOException:
                logging.error("Inverter modbus unit did not respond")
                raise register_value
        except ConnectionException:
            logging.error("A connection error occurred")
            raise

        return datatypes.decode(register_value.encode()[1:], register.value.data_type)

    def read(self, register):
        raw_value = self.read_raw_value(register)

        if register.value.gain is None:
            return raw_value
        else:
            return raw_value / register.value.gain

    def read_formatted(self, register):
        value = self.read(register)

        if register.value.unit is not None:
            return f'{value} {register.value.unit}'
        elif register.value.mapping is not None:
            return register.value.mapping.get(value, 'undefined')
        else:
            return value

    def read_range(self, start_address, quantity=0, end_address=0):
        if quantity == 0 and end_address == 0:
            raise ValueError("Either parameter quantity or end_address is required and must be greater than 0")
        if quantity != 0 and end_address != 0:
            raise ValueError("Only one parameter quantity or end_address should be defined")
        if end_address != 0 and end_address <= start_address:
            raise ValueError("end_address must be greater than start_address")

        if not self.isConnected():
            raise ValueError('Inverter is not connected')

        if end_address != 0:
            quantity = end_address - start_address + 1
        try:
            register_range_value = self.inverter.read_input_registers(start_address, quantity, unit=self.modbus_unit)
            if type(register_range_value) == ModbusIOException:
                logging.error("Inverter modbus unit did not respond")
                raise register_range_value
        except ConnectionException:
            logging.error("A connection error occurred")
            raise

        return datatypes.decode(register_range_value.encode()[1:], datatypes.DataType.MULTIDATA)
