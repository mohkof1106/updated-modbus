#!/usr/bin/env python
'''
Pymodbus Synchronous Client Examples
--------------------------------------------------------------------------

The following is an example of how to use the synchronous modbus client
implementation from pymodbus.

It should be noted that the client can also be used with
the guard construct that is available in python 2.5 and up::

    with ModbusClient('127.0.0.1') as client:
        result = client.read_coils(1,10)
        print result
'''
#---------------------------------------------------------------------------# 
# import the various server implementations
#---------------------------------------------------------------------------# 
#from pymodbus.client.sync import ModbusTcpClient as ModbusClient
#from pymodbus.client.sync import ModbusUdpClient as ModbusClient
from pymodbus.client.sync import ModbusSerialClient

class ModbusClient(ModbusSerialClient):
    """
    def __init__(self, method='ascii', **kwargs):
        self.rtscts = kwargs.get('rtscts', False)
        super(ModbusSerialClient, self).__init__(self, kwargs)
    """
    def connect(self):
        ''' Connect to the modbus tcp server

        :returns: True if connection succeeded, False otherwise
        '''
        if self.socket: return True
        try:
            self.socket = serial.Serial(port=self.port, timeout=self.timeout,
                bytesize=8, stopbits=self.stopbits,
                baudrate=self.baudrate, parity=self.parity, rtscts=True) # added rtscts
        except serial.SerialException, msg:
            _logger.error(msg)
            self.close()
        return self.socket != None

#---------------------------------------------------------------------------# 
# configure the client logging
#---------------------------------------------------------------------------# 
import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

#---------------------------------------------------------------------------# 
# choose the client you want
#---------------------------------------------------------------------------# 
# make sure to start an implementation to hit against. For this
# you can use an existing device, the reference implementation in the tools
# directory, or start a pymodbus server.
#
# If you use the UDP or TCP clients, you can override the framer being used
# to use a custom implementation (say RTU over TCP). By default they use the
# socket framer::
#
#    client = ModbusClient('localhost', port=5020, framer=ModbusRtuFramer)
#
# It should be noted that you can supply an ipv4 or an ipv6 host address for
# both the UDP and TCP clients.
#
# There are also other options that can be set on the client that controls
# how transactions are performed. The current ones are:
#
# * retries - Specify how many retries to allow per transaction (default = 3)
# * retry_on_empty - Is an empty response a retry (default = False)
# * source_address - Specifies the TCP source address to bind to
#
# Here is an example of using these options::
#
#    client = ModbusClient('localhost', retries=3, retry_on_empty=True)
#---------------------------------------------------------------------------# 
#client = ModbusClient('localhost', port=502)
#client = ModbusClient(method='ascii', port='/dev/pts/2', timeout=1)


import time, struct, fcntl, serial
uart4_file = '/dev/ttyO4'
baud = 19200
ser = serial.Serial(uart4_file, baud)
fd=ser.fileno()
serial_rs485 = struct.pack('hhhhhhhh', 1, 0, 0, 0, 0, 0, 0, 0)
fcntl.ioctl(fd,0x542F,serial_rs485)


client = ModbusClient(method='rtu', port=uart4_file, timeout=1, rtscts=True)
client.connect()
print client.socket
#---------------------------------------------------------------------------# 
# specify slave to query
#---------------------------------------------------------------------------# 
# The slave to query is specified in an optional parameter for each
# individual request. This can be done by specifying the `unit` parameter
# which defaults to `0x00`
#---------------------------------------------------------------------------# 
"""
rr = client.read_coils(61, 32, unit=0x06)
print rr
rr = client.read_coils(0x3d, 32, unit=0x06)
print rr
rr = client.read_coils(61, 32, unit=0x3d)
print rr
rr = client.read_coils(6, 1, unit=0x02)
print rr
rr = client.read_coils(6, 1, unit=0x06)
print rr
rr = client.read_coils(1, 1, unit=0x06)
print rr
rr = client.read_coils(6,10)
print rr
rr = client.read_discrete_inputs(1,8, unit=0x06)
print rr
rr = client.read_holding_registers(6,1, unit=0x06)
print rr
"""


rr = client.read_holding_registers(61,2, unit=0x06)
print rr

rr = client.read_holding_registers(0x3d,2, unit=0x06)
print rr

rr = client.read_holding_registers(0x0000,61, unit=0x06)
print rr

rr = client.read_discrete_inputs(61,2, unit=0x06)
print rr

rr = client.read_holding_registers(61,2, unit=6)
print rr

rr = client.read_holding_registers(0x3d,2, unit=6)
print rr

rr = client.read_holding_registers(0x0000,61, unit=6)
print rr

rr = client.read_discrete_inputs(61,2, unit=6)
print rr

rr = client.read_discrete_inputs(61,2, unit=6)
print rr



rr = client.read_holding_registers(61,2, unit=0x05)
print rr

rr = client.read_holding_registers(0x3d,2, unit=0x05)
print rr

rr = client.read_holding_registers(0x0000,61, unit=0x05)
print rr

rr = client.read_discrete_inputs(61,2, unit=0x05)
print rr

rr = client.read_holding_registers(61,2, unit=5)
print rr

rr = client.read_holding_registers(0x3d,2, unit=5)
print rr

rr = client.read_holding_registers(0x0000,61, unit=5)
print rr

rr = client.read_discrete_inputs(61,2, unit=5)
print rr

rr = client.read_discrete_inputs(61,2, unit=5)
print rr



rr = client.read_holding_registers(61,2, unit=0x6)
print rr

rr = client.read_holding_registers(0x3d,2, unit=0x6)
print rr

rr = client.read_holding_registers(0x0000,61, unit=0x6)
print rr

rr = client.read_discrete_inputs(61,2, unit=0x6)
print rr



rr = client.read_holding_registers(61,2, unit=0x5)
print rr

rr = client.read_holding_registers(0x3d,4, unit=0x5)
print rr

rr = client.read_holding_registers(0x0000,61, unit=0x5)
print rr

rr = client.read_discrete_inputs(61,4, unit=0x5)
print rr


print 
rr = client.read_holding_registers(14,1, unit=0x05)
print rr

rr = client.read_holding_registers(0x0f,1, unit=0x05)
print rr

rr = client.read_holding_registers(14,1, unit=0x06)
print rr

rr = client.read_holding_registers(14,1, unit=0x06)
print rr

rr = client.read_coils(15, 1, unit=0x06)
print rr
rr = client.read_coils(14, 1, unit=0x06)
print rr
rr = client.read_coils(15, 1, unit=0x05)
print rr
rr = client.read_coils(14, 1, unit=0x05)
print rr

'''
read_holding_registers(self, address, count=1, **kwargs):
        

        :param address: The starting address to read from
        :param count: The number of registers to read
        :param unit: The slave unit this request is targeting
        :returns: A deferred response handle
'''

#---------------------------------------------------------------------------# 
# close the client
#---------------------------------------------------------------------------# 
client.close()



client = ModbusClient(method='ascii', port=uart4_file, timeout=1, bytesize=32)
client.connect()
print client
print client.socket

client.socket = serial.Serial(port=client.port, timeout=client.timeout,
                bytesize=8, stopbits=client.stopbits,
                baudrate=client.baudrate, parity=client.parity, rtscts=True)
client.connect()
print client.socket

rr = client.read_holding_registers(61,2, unit=0x05)
print rr

rr = client.read_holding_registers(0x3d,4, unit=0x05)
print rr

rr = client.read_holding_registers(61,2, unit=0x06)
print rr

rr = client.read_holding_registers(0x3d,4, unit=0x06)
print rr



rr = client.read_holding_registers(15,1, unit=0x05)
print rr

rr = client.read_holding_registers(0x0f,1, unit=0x05)
print rr

rr = client.read_holding_registers(15,1, unit=0x06)
print rr

rr = client.read_holding_registers(15,1, unit=0x06)
print rr


rr = client.read_holding_registers(14,1, unit=0x05)
print rr

rr = client.read_holding_registers(0x0f,1, unit=0x05)
print rr

rr = client.read_holding_registers(14,1, unit=0x06)
print rr

rr = client.read_holding_registers(14,1, unit=0x06)
print rr

rr = client.read_coils(15, 1, unit=0x06)
print rr
rr = client.read_coils(14, 1, unit=0x06)
print rr
rr = client.read_coils(15, 1, unit=0x05)
print rr
rr = client.read_coils(14, 1, unit=0x05)
print rr


client.close()
