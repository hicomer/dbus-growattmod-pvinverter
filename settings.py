#!/usr/bin/env python3

# flake8 --ignore E501,E402 settings.py

import dbus
import logging
import os
import sys

sys.path.insert(1, os.path.join(os.path.dirname(__file__), '/opt/victronenergy/dbus-systemcalc-py/ext/velib_python'))
from settingsdevice import SettingsDevice


class SystemBus(dbus.bus.BusConnection):
    def __new__(cls):
        return dbus.bus.BusConnection.__new__(cls, dbus.bus.BusConnection.TYPE_SYSTEM)


class SessionBus(dbus.bus.BusConnection):
    def __new__(cls):
        return dbus.bus.BusConnection.__new__(cls, dbus.bus.BusConnection.TYPE_SESSION)


class GrowattMODSettings(object):

    def __init__(self):
        # path, default value, min, max, logging silent or not
        supported_settings = {
            "modbus_host": ["/Settings/GrowattMOD/ModbusHost", "192.168.178.56", "", "", 0],
            "modbus_port": ["/Settings/GrowattMOD/ModbusPort", 502, 1, 65536, 0],
            "modbus_unit": ["/Settings/GrowattMOD/ModbusUnit", 1, 0, 247, 0],
            "custom_name": ["/Settings/GrowattMOD/CustomName", "Growatt MOD", "", "", 0],
            "position": ["/Settings/GrowattMOD/Position", 0, 0, 2, 0],
            "update_time_ms": ["/Settings/GrowattMOD/UpdateTimeMS", 5000, 100, 10000000, 0],
            #"power_correction_factor": ["/Settings/GrowattMOD/PowerCorrectionFactor", 0.995, 0.001, 100.0, 0],
            # "GrowattMOD" is our unique id for the moment. This needs some more thought if more than one inverter shall be supported.
            # Unfortunately we can't use the serial number, because we need the config in order to get that one, so we have a catch-22.
            "vrm_instance": ["/Settings/Devices/GrowattMOD/ClassAndVrmInstance", "pvinverter:51", "", "", 0],
        }
        self.dbus_conn = self._dbusconnection()
        self.settings = SettingsDevice(bus=self.dbus_conn, supportedSettings=supported_settings, eventCallback=self._handle_changed_setting)

    def _dbusconnection(self):
        return SessionBus() if "DBUS_SESSION_BUS_ADDRESS" in os.environ else SystemBus()

    def _handle_changed_setting(self, setting, oldvalue, newvalue):
        logging.info(f"setting changed, setting: {setting}, old: {oldvalue}, new: {newvalue}")
        logging.info("Exiting due to new setting. The service will get restarted and pick up the new setting.")
        # I consider this to be a bit of a hack, but it works for now. If there are config changes, the
        # service exits and gets restarted and thus picks up the new settings values.
        sys.exit(0)

    def get(self, setting):
        return self.settings[setting]

    def set(self, setting, value):
        self.settings[setting] = value

    def get_vrm_instance(self):
        return int(self.settings["vrm_instance"].split(":")[1])
