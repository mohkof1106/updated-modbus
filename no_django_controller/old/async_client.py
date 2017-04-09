#!/usr/bin/env python
'''
Pymodbus Asynchronous Client Examples
--------------------------------------------------------------------------
The following is an example of how to use the asynchronous modbus
client implementation from pymodbus.
'''
#---------------------------------------------------------------------------# 
# import needed libraries
#---------------------------------------------------------------------------# 
from twisted.internet import reactor, protocol
from pymodbus.constants import Defaults

#---------------------------------------------------------------------------# 
# choose the requested modbus protocol
#---------------------------------------------------------------------------# 
from pymodbus.client.async import ModbusClientProtocol
#from pymodbus.client.async import ModbusUdpClientProtocol

#---------------------------------------------------------------------------# 
# configure the client logging
#---------------------------------------------------------------------------# 
import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

#---------------------------------------------------------------------------# 
# helper method to test deferred callbacks
#---------------------------------------------------------------------------# 
def dassert(deferred, callback):
    def _assertor(value): assert(value)
    deferred.addCallback(lambda r: _assertor(callback(r)))
    deferred.addErrback(lambda  _: _assertor(False))

#---------------------------------------------------------------------------# 
# specify slave to query
#---------------------------------------------------------------------------# 
# The slave to query is specified in an optional parameter for each
# individual request. This can be done by specifying the `unit` parameter
# which defaults to `0x00`
#---------------------------------------------------------------------------# 
def exampleRequests(client):
    rr = client.read_coils(14, 1, unit=0x06)
    print rr
    rr = client.read_coils(15, 1, unit=0x06)
    print rr

#---------------------------------------------------------------------------# 
# example requests
#---------------------------------------------------------------------------# 
# simply call the methods that you would like to use. An example session
# is displayed below along with some assert checks. Note that unlike the
# synchronous version of the client, the asynchronous version returns
# deferreds which can be thought of as a handle to the callback to send
# the result of the operation.  We are handling the result using the
# deferred assert helper(dassert).
#---------------------------------------------------------------------------# 


#---------------------------------------------------------------------------# 
# extra requests
#---------------------------------------------------------------------------# 
# If you are performing a request that is not available in the client
# mixin, you have to perform the request like this instead::
#
# from pymodbus.diag_message import ClearCountersRequest
# from pymodbus.diag_message import ClearCountersResponse
#
# request  = ClearCountersRequest()
# response = client.execute(request)
# if isinstance(response, ClearCountersResponse):
#     ... do something with the response
#
#---------------------------------------------------------------------------# 

#---------------------------------------------------------------------------# 
# choose the client you want
#---------------------------------------------------------------------------# 
# make sure to start an implementation to hit against. For this
# you can use an existing device, the reference implementation in the tools
# directory, or start a pymodbus server.
#---------------------------------------------------------------------------# 
defer = protocol.ClientCreator(reactor, ModbusClientProtocol
        ).connectTCP("192.168.1.214", Defaults.Port)
reactor.run()