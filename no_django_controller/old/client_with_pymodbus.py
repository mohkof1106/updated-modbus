#!/usr/bin/env python

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

from pymodbus.client.sync import ModbusTcpClient as ModbusClient

def read_power(client):
    pass

client = ModbusClient('192.168.1.11', port=502)
client.connect()

rr = client.read_holding_registers(60, count=2, unit=1)
print rr
print rr.registers

client.close()