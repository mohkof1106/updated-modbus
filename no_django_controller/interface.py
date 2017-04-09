#!/usr/bin/env python
'''
Created on December 17, 2015
@author: victor
'''
import logging
logging.basicConfig(level=logging.DEBUG)

import modbus_tk
from modbus_tk import modbus_tcp
logger = modbus_tk.utils.create_logger("console")

class InterfaceError(Exception):
    def __init__(self):
        logging.critical("InterfaceError: Not implemented yet")

class Client():
    def __init__(self, host, port=502, timeout_in_sec=5.0):
        self.host = host
        self.port = port
        self.timeout_in_sec = timeout_in_sec
        self.client = modbus_tcp.TcpMaster(host, port, timeout_in_sec)
        self.client.open()
        logging.info(str(self))

    def __str__(self):
        return "TCP client for host %s, port %s, t/o %s" % \
            (self.host, self.port, self.timeout_in_sec)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.client.close()
    
    def get_value_from_device_at_address(self, device, address=1):
        mapping = device.template.get_mapping_by_address(address)
        if not mapping:
            logging.error("Could not find the mapping at address %s for device %s" % \
                          (address, device))
            return None
        table = mapping.table
        logging.debug("Reading from device %s, mapping %s" % (device, mapping))
        try:
            # TODO: implement expected length
            result = self.client.execute(device.slave_id, table.read_function, address-1, \
                            quantity_of_x=table.quantity_of_x, \
                            data_format=table.data_format)
        except modbus_tk.modbus.ModbusError, exc:
            logging.error("Error while reading from device %s, mapping %s" % \
                          (device, mapping))
            logging.error("%s- Code=%d", exc, exc.get_exception_code())
            raise InterfaceError()
        logging.debug("Modbus response: %s" % str(result))
        if table.callback:
            result = table.callback(result)
        result = result *1./mapping.factor
        logging.debug("Read %s at address %s from device %s, mapping %s, table %s" % \
                      (mapping.pretty_string(result), address, device, mapping, table))
        return result
    
    def set_value_from_device_at_address(self, value, device, address=1):
        mapping = device.template.get_mapping_by_address(address)
        if not mapping:
            logging.error("Could not find the mapping at address %s for device %s" % \
                          (address, device))
            return None
        else:
            logging.debug("Reading from device %s, mapping %s" % (device, mapping))
        table = mapping.table
        if table.read_only:
            msg = "Writing this register/table is either unauthorised or not implemented. "
            msg += table.pretty_string()
            logging.error(msg)
            return None
        out = value*mapping.factor
        try:
            # TODO: implement expected length
            echo = self.client.execute(device.slave_id, table.write_function, address-1, \
                            quantity_of_x=table.quantity_of_x, \
                            data_format=">HH", \
                            output_value=out)
        except modbus_tk.modbus.ModbusError, exc:
            logging.error("Error while reading from device %s, mapping %s" % \
                          (device, mapping))
            logging.error("%s- Code=%d", exc, exc.get_exception_code())
            raise InterfaceError()
        logging.debug("Modbus response (echo): %s" % str(echo))
        return echo