import sys, traceback
import logging
logger = logging.getLogger("live_control")
logger_handler = logging.StreamHandler()
logger_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logger_handler.setLevel(logging.DEBUG)
logger.addHandler(logger_handler)

from django.core.management.base import BaseCommand
from optparse import make_option

from .daemon.daemon import Daemon
pidfile = "/tmp/controller.pid"

from controller_setup.models import Plant, Measure, InterfaceError, LinkUserToPlant
from controller_setup.tools import wait, last_update_verification, utcnow
from controller_setup.tools import get_HWaddr

class Command(BaseCommand):
    help = """The command to call a specific action by a Controller object.
The controller can record the load or run the live control. The live control can run as a daemon if the option --daemon=something is correctly used.
Typical usage is python manage.py control --daemon=start to start the live control according to the hardware address"""
    
    def __init__(self):
        super(Command, self).__init__()
        self.options = {}

    option_list = BaseCommand.option_list + (
        make_option('--plant', action='store', dest='plant', default="auto",
            help='This option recognizes "auto" or a plant label, like "REMRAM". It will compare the given label to the plant it is supposed to run according to the LinkUserToPlant objects. Default to "auto" if not provided.'),
        make_option('--record', action='store', dest='record', default=None,
            help='If this option is used then ignores plant and daemon options. It will start to record the revenue in a separate log. Give as value to this option the plant label you wish to record the load for.'),
        make_option('--daemon', action='store', dest='daemon', default=None,
            help='Give either start, restart, stop or status. If not specified will start the command in your thread, in other words it will not "daemonize", which can be useful for debugging. Watch out that it does not compete with the daemon possibly running in the background.')
    )

    def handle(self, *args, **options):
        self.options = options
        record = options["record"]
        if record:
            controller = get_controller_by_name(record)
            controller.record_load_forever()
        else:
            # find the plant according to the registered MAC address in the LinkUserToPlant table
            HWaddr = get_HWaddr()
            try:
                link = LinkUserToPlant.objects.get(HWaddr=HWaddr)
            except LinkUserToPlant.DoesNotExist:
                logger.error("There is no known plant linked to the hardware %s" % HWaddr)
                return False
            plant = link.plant.label
    
            asked_plant = options["plant"]
            if not asked_plant in [plant, "auto"]:
                logger.error("You asked to run %s but this hardware is supposed to run %s" % (asked_plant, plant))
                return False
            logger.info("For hardware %s runs %s. Link: %s" % (HWaddr, plant, link))
            if plant:
                controller = get_controller_by_name(plant)
                daemon_option = options["daemon"]
                if daemon_option:
                    the_daemon = DaemonScript(controller)
                    if daemon_option == "start":
                        the_daemon.start()
                    elif daemon_option == "restart":
                        the_daemon.restart()
                    elif daemon_option == "stop":
                        the_daemon.stop()
                    elif daemon_option == "status":
                        the_daemon.status()
                    else:
                        print "Unknown command"
                else:
                    controller = get_controller_by_name(plant)
                    controller.control_forever()
                
def get_controller_by_name(plant_name):
    plant = Plant.objects.get(label=plant_name)
    return get_controller(plant)

def get_controller(plant):
    measures = Measure.objects.filter(device__plant=plant)
    revenues = measures.filter(type=1)
    solars = measures.filter(type=2)
    dgs = measures.filter(type=3)
    inv_power = measures.filter(type=4)
    inv_read_max = measures.filter(type=5)
    inv_write_max = measures.filter(type=6)
    controller = Controller(plant, revenues, solars, dgs, inv_power, inv_read_max, inv_write_max)
    return controller

def sum_pull_and_convert(measures):
    return lambda :sum([one_measure.pull_and_convert() for one_measure in measures])

def cut(value, lowest, highest):
    # TODO: use measure.device.template.get_mapping_by_address(measure.address).factor/table to deduce the floating point
    "0 < value < 22 with one digit after the float point"
    return 0.1*int(10*max(lowest, min(highest, value)))

class Controller():
    def __init__(self, plant, revenues, solars, dgs, invs_power, invs_read_max, invs_write_max):
        self.total_powers = revenues
        self.solar_powers = solars
        self.dg_powers = dgs
        self.invs_power = invs_power
        self.invs_read_max = invs_read_max
        self.invs_write_max = invs_write_max
        self.plant = plant
        if not self.total_powers and not self.dg_powers:
            raise ValueError("If you don't give the total revenue you should at least give the dg measures")
        if self.solar_powers:
            logger.info("The plant uses solar revenue meter(s)")
            self.get_solar_power = sum_pull_and_convert(self.solar_powers)
        else:
            logger.info("The plant's solar production is the sum of the inverters' one")
            self.get_solar_power = sum_pull_and_convert(self.invs_power)
        if self.total_powers:
            logger.info("The plant's load is the sum of the load revenue meters")
            self.get_load = sum_pull_and_convert(self.total_powers)
            if self.dg_powers:
                logger.info("You have given both the load, solar, and DG. Make sure load = solar + DG yourself")
                self.get_dgs_power = sum_pull_and_convert(self.dg_powers)
            else:
                self.get_dgs_power = lambda : self.get_load() - self.get_solar_power()
        else:
            logger.info("The plant's load is the addition of solar and DGs")
            self.get_dgs_power = sum_pull_and_convert(self.dg_powers)
            # we assume to have a dg_powers otherwise there would have been an exception
            self.get_load = lambda : self.get_dgs_power() + self.get_solar_power()
        print "Controller successfully loaded for %s" % plant.label

    def __str__(self):
        d = "Plant %s.\n" % str(self.plant)
        d += "Total powers: %s.\n" % str(map(str, self.total_powers))
        d += "Solar powers: %s.\n" % str(map(str, self.solar_powers))
        d += "DG powers: %s.\n" % str(map(str, self.dg_powers))
        d += "Inverters power: %s.\n" % str(map(str, self.invs_power))
        d += "Inverters read max: %s.\n" % str(map(str, self.invs_read_max))
        d += "Inverters write max: %s.\n" % str(map(str, self.invs_write_max))
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
            total_white_inverters_W = sum_pull_and_convert(self.invs_power)()
        else:
            total_white_inverters_W = total_solar_W
            # we do this to avoid pulling unnecessary values
        
        total_red_inverters_W = total_solar_W - total_white_inverters_W
        DGs_min_W = self.plant.DGs_min
        inverter_max = self.plant.inverter_max_output
        nb_white_inverters = len(self.invs_power)
        total_white_inverters_max = total_load_W - total_red_inverters_W - DGs_min_W
        
        # all inverters to this value
        out = cut( total_white_inverters_max*100./(inverter_max*nb_white_inverters), \
                   self.plant.min_prod, self.plant.max_prod )
        out = float(str(out)) # fix since the values sometimes counts as set([40.800000000000004])
        
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
        logger.info(c)
        logger.info("---------------------------from max(s) " + str(previous_maxs) + " to " + str(out))
        return out
   
    def set_max(self, out):
        "sets all white inverters"
        return [inverter_max_write.push(out) for inverter_max_write in self.invs_write_max]

    def pull_maxs(self):
        return [inverter_max_read.pull() for inverter_max_read in self.invs_read_max]    

    def __successful_update(self, out, maxs):
        return set(maxs) == set([out])

    def verify_written_max(self, out):
        success, error_counter, attempts = False, 0, 5
        while not success:
            wait(self.plant.update_effect_time)
            maxs = self.pull_maxs()
            success = self.__successful_update(out, maxs)
            if success:
                logger.debug("%s successfully written in %s attempts" % (out, error_counter))
                return True
            else:
                logger.debug("run check again. written are %s (%s) and out %s" % (set(maxs), maxs, set([out])))
                error_counter += 1
                if error_counter >= attempts:
                    logger.warning("Unsuccessful write check (%s attempts)" % attempts)
                    return False
        return True
        
    def _do_basic_control_cycle(self):
        "returns success of operation"
        try:
            out = self.calculate_new_max()
        except InterfaceError:
            logger.error("InterfaceError: Unable to calculate new max")
            return False
        try:
            self.set_max(out)
        except InterfaceError:
            logger.error("InterfaceError: Unable to set max")
            return False
        try:
            self.verify_written_max(out)
        except InterfaceError:
            logger.error("InterfaceError: Unable to verify max")
            return False
        return True

    def do_control_cycle(self):
        wait(self.plant.refresh_period)
        return self._do_basic_control_cycle()
        
    def control_forever(self):
        last_successful_update, warnings_flag = None, False
        while True:
            try:
                last_successful_update, warnings_flag = last_update_verification(last_successful_update, warnings_flag, self)
                if self._do_basic_control_cycle():
                    logger.debug("Successful control cycle")
                    last_successful_update, warnings_flag = utcnow(), True
                    wait(self.plant.refresh_period)
                else:
                    logger.warning("Unsuccesful control cycle")
                    wait(self.plant.refresh_period)
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                msg = "Unexpected error: %s" % str(exc_value)
                logger.critical(msg)
                logger.info(repr(traceback.format_exception(exc_type, exc_value,
                                          exc_traceback)))
                wait(self.plant.refresh_period)
                wait(0.5) # to give a chance for KeyboardInterrupt
        logger.critical("CONTROL SCRIPT IS EXITING ABNORMALLY")

    def record_load_forever(self, pattern="RECORD"):
        recorder = logging.getLogger("recorder")
        while True:
            load = self.get_load()
            recorder.info(" ".join([pattern, "load:", str(load), "(W)."]))

class DaemonScript(Daemon):
    def __init__(self, controller):
        self.controller = controller
        super(DaemonScript, self).__init__(pidfile)
                                           
    def start(self):
        logger.info("Asked to start new process for plant %s" % self.controller)
        super(DaemonScript, self).start()

    def run(self):
        logger.info("Run plant %s" % self.controller)
        self.controller.control_forever()

    def stop(self):
        pid = super(DaemonScript, self).stop()
        logger.info("Process %s stopped. Plant %s" % (pid, self.controller))
