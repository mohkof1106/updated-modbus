import logging
#import modbus_tk.defines as cst
from modbus_tk import modbus_tcp
import modbus_tk
#modbus_logger = modbus_tk.utils.create_logger("live_control")
logger = logging.getLogger("live_control")

from django.db import models
from .hardcoded_tables_functions import callback_choices, callback_map

class Plant(models.Model):
    label = models.CharField(max_length=50, unique=True)
    refresh_period = models.FloatField("Refresh period (s)", default=30, help_text="in seconds")
    update_effect_time = models.FloatField("Time for a write to be effective (s)", default=0.1, help_text="in seconds")
    DGs_min = models.FloatField("DGs total minimum (W)", default=5000, help_text="in Watt")
    inverter_max_output = models.FloatField("Inverter max output (W)", default=20000, help_text="in Watt")
    min_prod = models.FloatField("Minimum power output", default=0, help_text="in %")
    max_prod = models.FloatField("Maximum power output", default=99.9, help_text="in %")
    update_warning = models.IntegerField("Time before sending a warning (min)", default=5, help_text="in minutes")
    update_error = models.IntegerField("Time before sending an error msg (min)", default=10, help_text="in minutes")
    send_email = models.BooleanField("Activate notification emails", default=True)
    email = models.EmailField(default="mohkof1106@gmail.com")

    def __unicode__(self):
        return self.label

modbus_exception_codes = {
    1:"ILLEGAL_FUNCTION",
    2:"ILLEGAL_DATA_ADDRESS",
    3:"ILLEGAL_DATA_VALUE",
    4:"SLAVE_DEVICE_FAILURE",
    5:"COMMAND_ACKNOWLEDGE",
    6:"SLAVE_DEVICE_BUSY",
    8:"MEMORY_PARITY_ERROR",
    7:"Negative Acknowledge",
    10:"Gateway Path Unavailable",
    11:"Gateway Target Device Failed to Respond"
} # https://en.wikipedia.org/wiki/Modbus#Main_Modbus_exception_codes

class InterfaceError(Exception):
    def __init__(self, code=None):
        if code:
            try:
                logger.error("InterfaceError: exception code for %s" % modbus_exception_codes[code])
            except KeyError:
                logger.critical("InterfaceError: Not implemented yet (modbus error")
        else:
            logger.warning("InterfaceError: No code given (modbus error)")

#supported modbus functions, see modbus_tk.defines
modbus_functions_choices = (
    (0, "undf function code"),
    (1, "READ_COILS"),
    (2, "READ_DISCRETE_INPUTS"),
    (3, "READ_HOLDING_REGISTERS"),
    (4, "READ_INPUT_REGISTERS"),
    (5, "WRITE_SINGLE_COIL"),
    (6, "WRITE_SINGLE_REGISTER"),
    (7, "READ_EXCEPTION_STATUS"),
    (8, "DIAGNOSTIC"),
    (15, "WRITE_MULTIPLE_COILS"),
    (16, "WRITE_MULTIPLE_REGISTERS"),
    (23, "READ_WRITE_MULTIPLE_REGISTERS"),            
)
#supported block types, see modbus_tk.defines
block_types_choices = (
    (0, "undf block type"),
    (1, "COILS"),
    (2, "DISCRETE_INPUTS"),
    (3, "HOLDING_REGISTERS"),
    (4, "ANALOG_INPUTS"),
)
block_types_in_template_xmls = {
    "Holding": 3,
    "Input": 4,
    "Coil": 1,
    "Discrete": 2
}

data_format_url = "https://docs.python.org/2/library/struct.html#format-characters"
class Table(models.Model):
    read_only = models.BooleanField(default=True)
    label = models.CharField(max_length=200, default="undf table label")
    template_name = models.CharField(max_length=20, \
        help_text="The name usually used in the templates, like U16, S32 or String")
    quantity_of_x = models.IntegerField(default=0)
    data_format = models.CharField(max_length=10, default="", \
        help_text="Use for example >H, must be a precise value that must work for modbus_tk. For more information and example see %s" % data_format_url)
    block_type = models.IntegerField(choices=block_types_choices, default=0)
    read_function = models.IntegerField(choices=modbus_functions_choices, default=0)
    write_function = models.IntegerField(choices=modbus_functions_choices, default=0)
    callback = models.IntegerField(choices=callback_choices, default=0)
    
    def __unicode__(self):
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

    def exec_callback(self, response):
        func = callback_map[self.callback]
        return func(response)

    def save(self, *args, **kwargs):
        try:
            conflicting_table = Table.objects.filter(block_type=self.block_type).get(template_name=self.template_name)
            if conflicting_table == self:
                logger.info("Updated table %s" % str(self))
                super(Table, self).save(*args, **kwargs)
            else:
                raise ValueError("Conflicting table with same template name and block_type: %s" % conflicting_table)
        except Table.DoesNotExist:
            logger.info("No conflicting table while saving new %s" % self.pretty_string())
            super(Table, self).save(*args, **kwargs)

    @staticmethod
    def link_format2table(reg_type, table_format):
        "reg_type is like Holding, the name of the block_type in the templates, and table_format is Table.template_name"
        dictionary = block_types_in_template_xmls
        try:
            mapped_block_type = dictionary[reg_type]
        except KeyError:
            msg = "Could not find %s in dictionary %s" % (reg_type, dictionary)
            logger.error("Could not find %s in dictionary %s" % (reg_type, dictionary))
            print msg
            return None
        tables = Table.objects.filter(template_name = table_format).filter(block_type = mapped_block_type)
        if len(tables) == 0:
            msg = "No table found for reg_type %s, table_format %s" % (reg_type, table_format)
            logger.error(msg)
            print msg
            return None
        elif len(tables) == 1:
            return tables[0] # TODO: what if several tables, use get() but catch exceptions
        else:
            msg = "To many tables found for reg_type %s, format %s and tables %s. PASS" % (reg_type, table_format, tables)
            logger.error(msg)
            print msg
            return None

class Template(models.Model):
    label = models.CharField(max_length=200, default="user defined template")
    file_name = models.CharField(max_length=200, default="", blank=True, unique=True, \
        help_text="Leave blank if manually defined by the user, otherwise this field get the name of the xml file in the templates folder")

    def __unicode__(self):
        return self.label
    
    def pretty_string(self):
        comment = " from template " + self.file_name if self.file_name != "" else ""
        return self.label + comment

class AddressMapping(models.Model):
    address = models.IntegerField()
    label = models.CharField(max_length=200, default="")
    table = models.ForeignKey(Table)
    factor = models.FloatField(default=1, \
        help_text="The abstract value is stored in the table mutliplied by the factor, eg 50.0% is 500, factor 10.")
    unit = models.CharField(max_length=20, default="undf unit")
    template = models.ForeignKey(Template)
    
    def __unicode__(self):
        return self.label + " (" + self.unit + ") at address " + \
            str(self.address) + ", scaling " +  str(self.factor) + \
            " for template " + str(self.template) + ". " + str(self.table)
    
    def pretty_string(self, value):
        return str(value) + " " + self.unit

class Client(models.Model):
    label = models.CharField(max_length=200, blank=True)
    plant = models.ForeignKey(Plant)
    host = models.GenericIPAddressField()
    port = models.IntegerField(default=502)
    timeout_in_sec = models.FloatField(default=5.0)
    
    def __unicode__(self):
        return str(self.plant) + " " + self.label + "@" + str(self.host) + ":" + str(self.port)

    def save(self, *args, **kwargs):
        super(Client, self).save(*args, **kwargs)
        print "Update device and measures"
        for device in Device.objects.filter(client=self.pk):
            device.save()

    def get_value_from_device_and_mapping(self, device, mapping):
        logger.debug("Reading from device %s, mapping %s" % (device, mapping))
        master = self.get_master()
        table = mapping.table
        try:
            # TODO: implement expected length
            result = master.execute(
                            device.slave_id,
                            table.read_function,
                            mapping.address-1,
                            quantity_of_x=table.quantity_of_x if table.template_name != "String" else int(mapping.factor),
                            data_format=table.data_format
            )
        except modbus_tk.modbus.ModbusError, exc:
            logger.error("Error while reading from device %s, mapping %s" % \
                          (device, mapping))
            code = exc.get_exception_code()
            logger.error("%s- Code=%d", exc, code)
            raise InterfaceError(code)
        logger.debug("Modbus response: %s" % str(result))
        result = table.exec_callback(result)
        if table.template_name != "String": # note the hardcoded special case for Strings
            result = result*1./mapping.factor # note that 1*boolean == bolean
        logger.debug("Read %s at address %s from device %s, mapping %s, table %s" % \
                      (mapping.pretty_string(result), mapping.address, device, mapping, table))
        return result
    
    def set_value_from_device_and_mapping(self, device, mapping, value):
        logger.debug("Writing for device %s, mapping %s" % (device, mapping))
        master = self.get_master()
        table = mapping.table
        if table.read_only:
            msg = "Writing this register/table is either unauthorized or not implemented. "
            msg += table.pretty_string()
            logger.error(msg)
            return None
        out = value*mapping.factor
        try:
            # TODO: implement expected length
            echo = master.execute(
                device.slave_id,
                table.write_function,
                mapping.address-1,
                quantity_of_x=table.quantity_of_x,
                data_format=">HH", #TODO: no hard coding
                output_value=out
            )
        except modbus_tk.modbus.ModbusError, exc:
            logger.error("Error while reading from device %s, mapping %s" % \
                          (device, mapping))
            code = exc.get_exception_code()
            logger.error("%s- Code=%d", exc, code)
            raise InterfaceError(code)
        logger.debug("Modbus response (echo): %s" % str(echo))
        return echo
    
    def get_master(self):
        try:
            return self.master
        except AttributeError:
            self.master = self.get_new_master()
            return self.master
    
    def get_new_master(self):
        master = modbus_tcp.TcpMaster(self.host, self.port, self.timeout_in_sec)
        master.open()
        logger.info("New TCP client for %s" % str(self))
        return master
    
    def close_master(self):
        try:
            self.master.close()
            logger.info("Closed master for %s" % str(self))
        except AttributeError:
            logger.warning("No master to close for %s" % str(self))

class Device(models.Model):
    label = models.CharField(max_length=200)
    client = models.ForeignKey(Client)
    template = models.ForeignKey(Template)
    slave_id = models.IntegerField(default=1)
    plant = models.ForeignKey(Plant, editable=False, \
        null=True, help_text="Auto-updated at every save")
    
    def __unicode__(self):
        return self.label + "@" + str(self.plant) + " id:" + str(self.slave_id)
    
    def get_value_for_mapping(self, mapping):
        return self.client.get_value_from_device_and_mapping(self, mapping)
    
    def set_value_for_mapping(self, mapping, value):
        return self.client.set_value_from_device_and_mapping(self, mapping, value)
    
    def get_all_values(self):
        mappings = AddressMapping.objects.filter(template=self.template)
        return [self.get_value_for_mapping(mapping) for mapping in mappings]

    def save(self, *args, **kwargs):
        self.plant = self.client.plant
        super(Device, self).save(*args, **kwargs)
        if self.pk:
            for measure in Measure.objects.filter(device=self.pk):
                measure.save()

measure_type_choices = (
    (0, "regular live value"),
    (1, "revenue"),
    (2, "solar"),
    (3, "dg"),
    (4, "inverter power"),
    (5, "inverter read max"),
    (6, "inverter write max"),
)
class Measure(models.Model):
    label = models.CharField(max_length=200, blank=True)
    device = models.ForeignKey(Device)
    address = models.IntegerField(default=1)
    modbus_function = models.IntegerField(default=0, choices=block_types_choices,
        help_text="This field is only read if multiple mappings are found for the same template and address, you may leave it at default if unused.")
    type = models.IntegerField(choices=measure_type_choices, default=0)
    mapping = models.ForeignKey(AddressMapping, editable=False, \
        null=True, help_text="Auto-update with the right mapping according to the address in the device's template")
    plant = models.ForeignKey(Plant, editable=False, \
        null=True, help_text="Auto-updated at every save")
    
    def __unicode__(self):
        return self.label + " for device " + str(self.device) +\
            " and mapping " + str(self.mapping) 
    
    def save(self, *args, **kwargs):
        self.plant = self.device.plant
        device_template = self.device.template
        try:
            self.mapping = AddressMapping.objects.filter(template=device_template).get(address=self.address)
        except AddressMapping.DoesNotExist:
            raise ValueError("There is no mapping for this address and device")
        except AddressMapping.MultipleObjectsReturned:
            try:
                self.mapping = AddressMapping.objects.filter(template=device_template).filter(table__block_type=self.modbus_function).get(address=self.address)
            except AddressMapping.DoesNotExist:
                raise ValueError("There is no mapping for this address, modbus function (mapping.table.block_type) and device")
        super(Measure, self).save(*args, **kwargs)
    
    def pull(self):
        return self.device.get_value_for_mapping(self.mapping)
    
    def push(self, value):
        return self.device.set_value_for_mapping(self.mapping, value)
    
    def pull_and_convert(self):
        value = self.pull()
        if self.mapping.unit.startswith("k"): # TODO: model for units
            return 1000 * value
        else:
            return value

class Document(models.Model):
    docfile = models.FileField()
    
    def __unicode__(self):
        return str(self.docfile)

HOST_CHOICES = (
    ("mohkof1106.tk", "mohkof1106.tk"),
    ("localhost", "localhost"),                
)

# keep sudo since /sbin/ifconfig permissions are -rwxr-xr-x  1 root on the pi
FIND_HARDWARE_COMMAND = "sudo ifconfig | grep eth0 | tr -s ' ' | awk -F'[ ]' '{if (/HWaddr/) print $5}'"

class LinkUserToPlant(models.Model):
    host = models.CharField(max_length=50, choices=HOST_CHOICES, default="localhost",
        help_text = "The host where the website can find the tunnel, for example from an enerwhere website, user enerwhere finds pi1@localhost")
    user = models.CharField(max_length=20,
        help_text = "The user where the website can find the tunnel, named pi1 in the example above")
    local_user = models.CharField(max_length=20, default="pi",
        help_text = "The user on the controller that created the tunnel. It is the one that [user]@[HOST] finds with ssh -p [REVERSE_PORT] [local_user]@localhost")
    plant = models.ForeignKey(Plant)
    reverse_port = models.IntegerField(null=True,
        help_text="The port to connect to the reverse ssh, eg user pi1@HOST does ssh -p REVERSE_PORT [local_user]@localhost to connect. Do not mix with the port used to connect to USER (22 by default)")
    distant_project_path = models.CharField(max_length=200, default="/home/pi/modbus_controller",
        help_text="Absolute path on the local controller to the project folder")
    comment = models.CharField(max_length=200, default="", blank=True,
        help_text="Optional. Will appear on the 'control' page")
    HWaddr = models.CharField(max_length=25, unique=True,
        help_text="The hardware MAC address from the controller (RPi, etc). Found with command:{0}".format(FIND_HARDWARE_COMMAND))
    
    def __unicode__(self):
        return str(self.plant) + " through " + self.user + "@" + str(self.host) + ">" + self.local_user + "@localhost:" + str(self.reverse_port)
