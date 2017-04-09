#!/usr/bin/env python
pidfile = "/tmp/controller.pid"

import os.path
BASE = os.path.dirname(__file__)
import logging
logging.basicConfig(level=logging.DEBUG)

checker = logging.getLogger("checker")
checker_handler = logging.FileHandler(os.path.join(BASE,"checker.log"))
checker_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
checker_handler.setLevel(logging.INFO)
checker.addHandler(checker_handler)

from tools import utcnow, send_controller_mail, find_plant_name
from daemon import Daemon

if __name__ == "__main__":
    PLANT = find_plant_name()
    theDaemon = Daemon(pidfile)
    pid = theDaemon.status()
    if pid:
        checker.debug("PLANT %s is running at pid %s" % (PLANT, pid))
    else:
        now = utcnow()
        hour = now.hour
        if 3 <= hour and hour < 14:
            txt = "PLANT %s is not running but should be" % PLANT
            checker.error(txt)
            send_controller_mail(txt)
        else:
            checker.debug("PLANT %s is not running, not a problem" % PLANT)
        
            


