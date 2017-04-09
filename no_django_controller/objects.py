#!/usr/bin/env python
'''
Created on December 17, 2015
@author: victor
'''
import sys
import logging
logging.basicConfig(level=logging.DEBUG)
import modbus_tk.defines as cst

from interface import InterfaceError
from tools import last_update_verification, utcnow, verify_if_keys_are_present, wait

def get_link_format2table():
    return {"Holding": {"U16" : Unsigned_16bits_HoldingRegister,
                        "S16" : Signed_16bits_HoldingRegister,
                        "U32" : Unsigned_32bits_HoldingRegister,
                        "S32" : Signed_32bits_HoldingRegister
                        },
            "Input": {"U32": Unsigned_32bits_Input,
                      "S16": Signed_16bits_Input}
            }

def sum_pull_and_convert(measures):
    return lambda :sum([one_measure.pull_and_convert() for one_measure in measures])

class Plant():
    def __init__(self, options, inverters_power_and_maxs, total_powers=None, solar_powers=None, dg_powers=None):
        expected_options = ["name", "refresh_period", "DGs_min", \
                            "inverter_max_output", \
                            "max_prod_extremum", "update_warning", \
                            "update_error", "update_effect_time",
                            "emails"]
        self.total_powers = total_powers
        self.solar_powers = solar_powers
        self.dg_powers = dg_powers
        self.inverters_power_and_maxs = inverters_power_and_maxs
        self.options = options
        if not verify_if_keys_are_present(expected_options, options):
            raise ValueError("The given options %s do not contain the expected keys %s" %(options, expected_options))
        if not total_powers and not dg_powers:
            raise ValueError("If you don't give the total revenue you should at least give the dg measures")
        
        self.get_solar_power = sum_pull_and_convert(solar_powers) if solar_powers else sum_pull_and_convert([inv_p_and_m[0] for inv_p_and_m in inverters_power_and_maxs])
        if total_powers:
            self.get_load = sum_pull_and_convert(total_powers)
            if dg_powers:
                self.get_dgs_power = sum_pull_and_convert(dg_powers)
            else:
                self.get_dgs_power = lambda : self.get_load() - self.get_solar_power()
        else:
            self.get_dgs_power = sum_pull_and_convert(dg_powers)
            # we assume to have a dg_powers otherwise there would have been an exception
            self.get_load = lambda : self.get_dgs_power() + self.get_solar_power()
        print "Plant created"

    def __str__(self):
        d = "Plant %s. " % self.options["name"]
        d += "Options: %s. " % self.options
        d += "Total powers: %s. " % self.total_powers
        d += "Solar powers: %s. " % self.solar_powers
        d += "DG powers: %s. " % self.dg_powers
        d += "Inverters: %s. " % self.inverters_power_and_maxs
        return d

    def calculate_new_max(self):
        "takes care of the pull"
        total_solar_W = self.get_solar_power()
        if self.total_powers:
            total_load_W = self.get_load()
            total_DGs = total_load_W - total_solar_W
        else:
            total_DGs = self.get_dgs_power()
            total_load_W = total_DGs + total_solar_W
         
        previous_maxs = self.pull_maxs()
        if self.solar_powers:
            total_white_inverters_W = sum([inverter_power_and_maxs[0].pull_and_convert() for inverter_power_and_maxs in self.inverters_power_and_maxs])
        else:
            total_white_inverters_W = total_solar_W
            # we do this to avoid pulling unnecessary values
        
        total_red_inverters_W = total_solar_W - total_white_inverters_W
        DGs_min_W = self.options["DGs_min"]
        inverter_max = self.options["inverter_max_output"]
        nb_white_inverters = len(self.inverters_power_and_maxs)
        total_white_inverters_max = total_load_W - total_red_inverters_W - DGs_min_W
        
        # all inverters to this value
        out = cut( total_white_inverters_max*100./(inverter_max*nb_white_inverters), \
                   self.options["max_prod_extremum"] )
        
        c = """
        total_load = total_DGs + total_white_inverters + total_red_inverters
        {0} = {1} + {2} + {3} (W)
        
        total_load = DGs_min + white_inverters_max + total_red_inverters
        {0} = {4} + {5} + {3} (W)
        
        white_inverters_max = nb_white_inverters * inv_max_output * out / 100
        {5} = {6} * {7} * {8} /100 (= {9}) (W)""".format(total_load_W, total_DGs, total_white_inverters_W, total_red_inverters_W, 
                                         DGs_min_W, total_white_inverters_max,
                                         nb_white_inverters, inverter_max, out, nb_white_inverters * inverter_max * out / 100)
        print c
        logging.info(c)
        logging.info("---------------------------from max(s) " + str(previous_maxs) + " to " + str(out))
        return out
   
    def set_max(self, out):
        "sets all white inverters"
        return [inverter_max_write.push(out) for _, _, inverter_max_write in self.inverters_power_and_maxs]

    def pull_maxs(self):
        return [inverter_max_read.pull() for _, inverter_max_read, _ in self.inverters_power_and_maxs]    

    def __successful_update(self, out, maxs):
        return set(maxs) == set([out])

    def verify_written_max(self, out):
        success, error_counter, attempts = False, 0, 5
        while not success:
            maxs = self.pull_maxs()
            success = self.__successful_update(out, maxs)
            if success:
                logging.debug("%s successfully written" % out)
                return True
            else:
                logging.debug("run check again. written are %s (%s) and out %s" % (set(maxs), maxs, set([out])))
                error_counter += 1
                wait(self.options["update_effect_time"])
                if error_counter >= attempts:
                    logging.warning("Unsuccessful write check (%s attempts)" % attempts)
                    return False
        return True
        
    def _do_basic_control_cycle(self):
        "returns success of operation"
        try:
            out = self.calculate_new_max()
        except InterfaceError:
            logging.error("InterfaceError: Unable to calculate new max")
            return False
        try:
            self.set_max(out)
        except InterfaceError:
            logging.error("InterfaceError: Unable to set max")
            return False
        try:
            self.verify_written_max(out)
        except InterfaceError:
            logging.error("InterfaceError: Unable to verify max")
            return False
        return True

    def do_control_cycle(self):
        wait(self.options["refresh_period"])
        return self._do_basic_control_cycle()
        
    def control_forever(self):
        last_successful_update, warnings_flag = None, False
        while True:
            try:
                last_successful_update, warnings_flag = last_update_verification(last_successful_update, warnings_flag, self)
                if self._do_basic_control_cycle():
                    logging.debug("Successful control cycle")
                    last_successful_update, warnings_flag = utcnow(), True
                    wait(self.options["refresh_period"])
                else:
                    logging.warning("Unsuccesful control cycle")
                    wait(self.options["refresh_period"])
            except:
                msg = "Unexpected error: %s" % str(sys.exc_info())
                logging.critical(msg)
                wait(self.options["refresh_period"])
        logging.critical("CONTROL SCRIPT IS EXITING ABNORMALLY")

    def record_load_forever(self, pattern="RECORD"):
        logger = logging.getLogger("load_recorder")
        logger_handler = logging.FileHandler("load_record.log") # TODO: path.join
        logger_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
        logger_handler.setLevel(logging.INFO)
        logger.addHandler(logger_handler)
        while True:
            load = self.get_load()
            logger.info(" ".join([pattern, "load:", str(load), "(W)."]))
        

def cut(value, extremum):
    # TODO: use measure.device.template.get_mapping_by_address(measure.address).factor/table to deduce the floating point
    "0 < value < 22 with one digit after the float point"
    return 0.1*int(10*max(extremum[0], min(extremum[1], value)))


class Measure():
    def __init__(self, device, address):
        self.device = device
        self.address = address
        try:
            self.unit = device.template.get_mapping_by_address(address).unit
        except AttributeError:
            logging.error("No mapping found for device %s at address %s in device's template %s" % \
                          (device, address, device.template))
            self.unit = "undf unit"

    def __str__(self):
        return "Measure at address %s for mapping %s device %s" % (self.address, self.device.template.get_mapping_by_address(self.address), self.device)

    def pull(self):
        return self.device.get_value_at_address(self.address)

    def push(self, value):
        return self.device.set_value_at_address(self.address, value)
    
    def pull_and_convert(self):
        value = self.pull()
        if self.unit.startswith("k"): # TODO: model for the units
            return 1000*value
        else:
            return value

    @staticmethod
    def pull_addresses(device, addresses):
        return [__class__.pull_address(device, address) for address in addresses]
    
    @staticmethod
    def pull_address(device, address):
        measure = Measure(device, address)
        value = measure.pull()
        print value, str(measure), value
        return value
            


class Device():
    def __init__(self, template, slave_id, client):
        self.template = template
        self.slave_id = slave_id
        self.client = client

    def __str__(self):
        return "slave id: %s, through %s" % (self.slave_id, self.client)

    def exists_and_connected(self):
        return self.slave_id and self.client.client._is_opened

    def get_value_at_address(self, address):
        return self.client.get_value_from_device_at_address(self, address)

    def set_value_at_address(self, address, value):
        return self.client.set_value_from_device_at_address(value, self, address)

    def get_all_values(self):
        return [(address, Measure.pull_address(self, address)) for address in self.template.get_addresses()]
        


class Template():
    def __init__(self, mappings=None):
        self.mappings = mappings
    def __str__(self):
        return "\n".join(map(str, self.mappings))

    def add_one_mapping(self, mapping):
        try:
            self.mappings.append(mapping)
        except AttributeError:
            self.mappings = [mapping]

    def add_mappings(self, mappings):
        try:
            self.mappings.extend(mappings)
        except AttributeError:
            self.mappings = mappings

    def _set_mappings(self, mappings):
        self.mappings = mappings

    def get_mapping_by_address(self, address):
        for mapping in self.mappings:
            if mapping.address == address:
                return mapping
        return None

    def get_addresses(self):
        return sorted([mapping.address for mapping in self.mappings])

   
class AddressMapping():
    def __init__(self, address, label="", table=None, factor=1, unit="undf unit"):
        self.address = address
        self.label = label
        self.table = table
        self.factor = factor # the pulled value is divided by this, the pushed multiplied
        self.unit = unit      

    def __str__(self):
        return self.label + " (" + self.unit + ") at address " + \
            str(self.address) + ", scaling " +  str(self.factor) + ". " + str(self.table)        

    def pretty_string(self, value):
        return str(value) + " " + self.unit



class Table():
    def __init__(self):
        self.read_only = True
        self.label = "undf table label"
        self.quantity_of_x = 0
        self.data_format = ""
        self.read_function = 0
        self.write_function = 0
        self.callback = None  

    def __str__(self):
        return "Modbus type: " + self.label

    def pretty_string(self):
        msg = "read_only: %s. " % self.read_only
        msg += "label: %s. " % self.label
        msg += "quantity_of_x: %s. " % self.quantity_of_x
        msg += "data_format: %s. " % self.data_format
        msg += "read_function: %s. " % self.read_function
        msg += "write_function: %s. " % self.write_function
        msg += "callback: %s. " % self.callback
        return msg.format()

    def bits16_to_bits32(self, int_tuple):
        return int(0x10000*int_tuple[0]+int_tuple[1])

class Unsigned_32bits_HoldingRegister(Table):
    def __init__(self):
        self.read_only = True
        self.label = "Holding/32 bit value"
        self.quantity_of_x = 2
        self.data_format = ">HH"
        self.read_function = cst.HOLDING_REGISTERS
        self.write_function = 0
        self.callback = self.bits16_to_bits32

class Unsigned_32bits_Input(Table):
    "untested"
    def __init__(self):
        self.read_only = True
        self.label = "Input/U32"
        self.quantity_of_x = 2
        self.data_format = ">HH"
        self.read_function = cst.READ_INPUT_REGISTERS
        self.write_function = cst.WRITE_SINGLE_REGISTER
        self.callback = self.bits16_to_bits32

class Signed_16bits_Input(Table):
    "untested"
    def __init__(self):
        self.read_only = True
        self.label = "Input/S16"
        self.quantity_of_x = 1
        self.data_format = ">h"
        self.read_function = cst.READ_INPUT_REGISTERS
        self.write_function = cst.WRITE_SINGLE_REGISTER
        self.callback = lambda x:x[0]


class Signed_32bits_HoldingRegister(Table):
    "Untested"
    def __init__(self):
        self.read_only = True
        self.label = "Holding/32 bits value with sign"
        self.quantity_of_x = 2
        self.data_format = ">hh"
        self.read_function = cst.HOLDING_REGISTERS
        self.write_function = 0
        self.callback = self.bits16_to_bits32

class Unsigned_16bits_HoldingRegister(Table):
    "untested"
    def __init__(self):
        self.read_only = False
        self.label = "Holding/16 bit value"
        self.quantity_of_x = 1
        self.data_format = ">H"
        self.read_function = cst.HOLDING_REGISTERS
        self.write_function = cst.WRITE_SINGLE_REGISTER
        self.callback = lambda x: x[0]
        
class Signed_16bits_HoldingRegister(Table):
    "untested"
    def __init__(self):
        self.read_only = False
        self.label = "Holding/Signed 16 bit value"
        self.quantity_of_x = 1
        self.data_format = ">h"
        self.read_function = cst.HOLDING_REGISTERS
        self.write_function = cst.WRITE_SINGLE_REGISTER
        self.callback = lambda x: x[0]

