import sys, traceback
from modbus_tk import modbus_tcp
import modbus_tk

host = "192.168.1.21"
slave_id = 1
address = 5031 - 1
quantity_of_x = 2
#data_format = ">H"
function = 4

master = modbus_tcp.TcpMaster(host, 502, 5)
print master

for data_format in [">d", ">hh", ">HH", ">i", ">I", ">l", ">L", ">f"]:
    try:
	result = master.execute(
                            slave_id,
                            function,
                            address,
                            quantity_of_x=quantity_of_x,
                            data_format=data_format
        )
	print data_format, str(result)
    except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                msg = "Unexpected error: %s" % str(exc_value)
                print(msg)
                print(repr(traceback.format_exception(exc_type, exc_value,
                                          exc_traceback)))
