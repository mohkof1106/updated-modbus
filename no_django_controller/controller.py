#!/usr/bin/env python
# -*- coding: utf_8 -*-
'''
Created on December 17, 2015
@author: victor [AT] enerwhere [DOT] com, victor [DOT] talpaert [AT] gmail
'''
pidfile = "/tmp/controller.pid"

import os.path
BASE = os.path.dirname(__file__)
import logging
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger() # root logger
logger_handler = logging.FileHandler(os.path.join(BASE,"live_control.log"))
logger_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logger_handler.setLevel(logging.DEBUG)
logger.addHandler(logger_handler)


from tools import wait, find_plant_name
from interface import Client
from objects import Measure, Plant
from templates import get_device_by_name_and_id, get_anybus


def make_REMRAM():
    options = {"refresh_period": 30, # secs
               "DGs_min": 5000, # W
               "inverter_max_output": 23000, #W
               "max_prod_extremum": (0, 99.9), # %%
               "update_warning": 5, # min
               "update_error":10, # min
               "update_effect_time":0.1, # secs
               "name": "REMRAM",
               "emails": True
               }

    host_converter = '192.168.1.21'
    converter_interface = Client(host_converter)
    host_dgsp3 = "192.168.1.14"
    dgsp3_interface = Client(host_dgsp3)
    host_dgsp2 = "192.168.1.13"
    dgsp2_interface = Client(host_dgsp2)
    
    anybus_slave_id = 2
    inv_power_address = 3
    inv_read_max_address = 7
    inv_write_max_address = 1025
    
    agc4_slave_id = 1
    agc4_power_address = 11
    
    anybus = get_anybus(anybus_slave_id, converter_interface)
    inv_power = Measure(anybus, inv_power_address)
    inv_read_max = Measure(anybus, inv_read_max_address)
    inv_write_max = Measure(anybus, inv_write_max_address)

    dgsp2 = get_device_by_name_and_id("AGC-4 Enerwhere Custom", agc4_slave_id, dgsp2_interface)
    dgsp2_power = Measure(dgsp2, agc4_power_address)
    
    dgsp3 = get_device_by_name_and_id("AGC-4 Enerwhere Custom", agc4_slave_id, dgsp3_interface)
    dgsp3_power = Measure(dgsp3, agc4_power_address)

    inverters_power_and_maxs = [(inv_power, inv_read_max, inv_write_max)]
    dg2and3_powers = [dgsp2_power, dgsp3_power]
    remram = Plant(options, inverters_power_and_maxs, dg_powers=dg2and3_powers)
    return remram

from daemon import Daemon
import sys

class DaemonScript(Daemon):
    def __init__(self, plant_maker):
        self.plant_maker = plant_maker
        super(DaemonScript, self).__init__(pidfile)
                                           
    def start(self):
        logging.info("Asked to start new process for plant %s" % self.plant_maker)
        super(DaemonScript, self).start()

    def run(self):
        self.plant = self.plant_maker()
        logging.info("Run plant %s" % self.plant)
        self.plant.control_forever()

    def stop(self):
        pid = super(DaemonScript, self).stop()
        logging.info("Process %s stopped. Plant %s" % (pid, self.plant_maker))

def plant_makers():
    return {"REMRAM": make_REMRAM,
        "SSV": None,
        "ERS": None}

if __name__ == "__main__":
    if len(sys.argv) == 2:
        PLANT = find_plant_name()
        plants = plant_makers()
        if PLANT in plants.keys():
            plant_maker = plants[PLANT]
            theDaemon = DaemonScript(plant_maker)
            if 'start' == sys.argv[1]:
                logging.debug("Daemon : Asked to start")
                theDaemon.start()
            elif 'stop' == sys.argv[1]:
                logging.debug("Daemon : Asked to stop")
                theDaemon.stop()
            elif 'restart' == sys.argv[1]:
                logging.debug("Daemon : Asked to restart")
                theDaemon.restart()
            elif 'status' == sys.argv[1]:
                logging.debug("Daemon : Asked status")
                theDaemon.status()
            else:
                print "Unknown command"
                sys.exit(2)
        else:
            print "could not recognize the plant: PLANT should be in %s" % plants.keys()
        sys.exit(0)
    elif len(sys.argv) == 1:
        PLANT = find_plant_name()
        plants = plant_makers()
        plant = plants[PLANT]()
        plant.control_forever()
    else:
        print "usage: %s start|stop|restart|status (or none for not daemon version)" % sys.argv[0]
        sys.exit(2)