#!/usr/bin/env python
'''
Created on December 17, 2015
@author: victor
'''
import pytz
import datetime
import time
import logging
logger = logging.getLogger("live_control")

import os.path
BASE = os.path.dirname(__file__)
from django.core.mail import send_mail as django_send_mail
import modbus_controller.settings as settings
from controller_setup.models import FIND_HARDWARE_COMMAND
from .tools_ssh import bash

def to_iso(datetime_):
    if isinstance(datetime_, datetime.datetime):
        return datetime_.strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        return datetime_

def to_epoch(dt):
    if isinstance(dt, int):
        return dt
    return unix_time(dt)

def unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    epoch = epoch.replace(tzinfo=pytz.UTC)
    delta = dt - epoch
    return int(delta.total_seconds())

def utcnow():
    return make_timezone_aware(datetime.datetime.utcnow())

def make_timezone_aware(datetime_):
    return datetime_.replace(tzinfo=pytz.UTC)

def from_isotime(iso_timestamp):
    dt = datetime.datetime.strptime(iso_timestamp, "%Y-%m-%dT%H:%M:%SZ")
    dt = dt.replace(tzinfo=pytz.UTC)
    return dt


def wait(sec=5):
    if sec > 10:
        logger.info("sleep %s" % sec)
    else:
        logger.debug("sleep %s" % sec)
    time.sleep(sec)

def verify_if_keys_are_present(expected_keys, dic):
    result = ([] == list(set(expected_keys)-set(dic)))
    if not(result):
        logger.warning('In dict: %s, found the keys %s but expected at least %s' % (dic, set(dic), expected_keys))
    return result

smtp = 'smtp.webfaction.com'

def send_mail(txt, subject, me, you):
    django_send_mail(
        from_email = settings.DEFAULT_FROM_EMAIL,
        subject = subject,
        recipient_list = [you],
        message = txt
    )

def send_controller_mail(txt):
    # from
    me = "mohkof1106@gmail.com"
    # to
    you = me
    # subject
    subject = '[Controller][Modbus] A message from %s' % smtp
    
    send_mail(txt, subject, me, you)
def send_mail_with_subject(to, subject, txt):
    # from
    me = "Recipients <mohkof1106@gmail.com>"
    # to
    you = to
    # subject
    subject = '[Controller] ' + subject
    txt = str(to_iso(utcnow())) + "\n" + txt + "\n\nSorry for the spam!" 
    
    send_mail(txt, subject, me, you)



def last_update_verification(last_successful_update, warnings_flag, controller):
    "times in minutes, initialize at None, False"
    update_warning_time, update_error_time = controller.plant.update_warning, controller.plant.update_error
    update_max_diff = datetime.timedelta(minutes=update_error_time)
    update_warning = datetime.timedelta(minutes=update_warning_time)
    if last_successful_update:
        update_diff = utcnow() - last_successful_update
        msg = str(controller.plant)
        if  update_diff > update_max_diff:
            subject = "Error for %s" % str(controller.plant)
            msg += "Did not have a successful update for more than %s! (error). Last successful update: %s ago\n" % (update_max_diff, update_diff)
            msg += str(controller)
            logger.error(msg)
            last_successful_update = None
            if controller.plant.send_email:
                send_mail_with_subject(controller.plant.email, subject, msg)
        elif update_diff > update_warning and warnings_flag:
            subject = "Warning for %s" % str(controller.plant)
            msg += "Did not have a successful update for more than %s (warning). Last successful update: %s ago\n" % (update_warning, update_diff)
            msg += str(controller)
            logger.warning(msg)
            warnings_flag = False
            if controller.plant.send_email:
                send_mail_with_subject(controller.plant.email, subject, msg)
        else:
            logger.info("Last successful update: %s ago, less than %s" % (update_diff, update_max_diff))
    else:
        logger.debug("No last successful update to work with")
    return last_successful_update, warnings_flag


# give file or directory and returns list of files with suffix
import glob #, os.path

def crawl(path, suffix):
    files_list = []
    path_list = [path]
    for path in path_list:
        if path.endswith(suffix):
            files_list.append(path)
        if not(os.path.isfile(path)):
            path_list.extend(glob.glob(path + '/*'))
    return files_list

def find_plant_name():
    path = os.path.join(BASE,"PLANT_TO_RUN.txt")
    with open(path, "r") as f:
        name = f.read()
    return name

def get_HWaddr():
    command = FIND_HARDWARE_COMMAND
    result = bash(command)
    logger.debug("Find hardware: %s" % str(result))
    result = result[1]
    if result.endswith("\n"):
        result = result[:-1]
    logger.info("The hardware address is %s after command %s" % (result, command))
    return result
