#!/usr/bin/env python

#---------------------------------------------------------------------------# 
# the various server implementations
#---------------------------------------------------------------------------# 
from pymodbus.server.sync import StartTcpServer
from pymodbus.server.sync import StartUdpServer
from pymodbus.server.sync import StartSerialServer

from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

#---------------------------------------------------------------------------# 
# configure the service logging
#---------------------------------------------------------------------------# 
import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

#---------------------------------------------------------------------------# 
# initialize your data store
#---------------------------------------------------------------------------# 
store = ModbusSlaveContext(
    di = ModbusSequentialDataBlock(1, [17]*100),
    co = ModbusSequentialDataBlock(1, [17]*100),
    hr = ModbusSequentialDataBlock(0, [17]*100),
    ir = ModbusSequentialDataBlock(0, [17]*100))
context = ModbusServerContext(slaves=store, single=True)

#---------------------------------------------------------------------------# 
# run the server you want
#---------------------------------------------------------------------------# 
StartTcpServer(context)
#StartUdpServer(context)
#StartSerialServer(context, port='/tmp/tty1')

from pymodbus.server.sync import ModbusTcpServer
class ModbusTcpServer_withcontext(ModbusTcpServer):
    def __init__(self, whatever_context, framer=None, identity=None, address=None):
        print context
        super(ModbusTcpServer, self).__init__(context, framer=None, identity=None, address=None)

