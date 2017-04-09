import logging
logger = logging.getLogger("live_control")

from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage

from modbus_controller.settings import LOGGING
from controller_setup.tools import get_HWaddr
from controller_setup.models import LinkUserToPlant

def get_local_name():
    HWaddr = get_HWaddr()
    try:
        link = LinkUserToPlant.objects.get(HWaddr=HWaddr)
    except LinkUserToPlant.DoesNotExist:
        logger.error("There is no known plant linked to the hardware %s" % HWaddr)
        return False
    return link.plant.label

def get_filename(handler_name="live_rotation"):
    try:
        handler_file = LOGGING["handlers"][handler_name]["filename"]
    except KeyError:
        logger.error("Failed to find filename for handler %s" % handler_name)
        return None
    return handler_file

def create_mail(to=["mohkof1106@gmail.com"]):
    name = get_local_name()
    subject = "[Controller][Log] live_control log"
    if name:
        subject += " for " + name
    
    body = "Please find attached the last log for live_control\n \n Sorry for the spam!"
    return EmailMessage(subject=subject, body=body, to=to)

def main():
    mail = create_mail()
    filename = get_filename()
    if not filename:
        logger.error("Not sending mail")
        return None
    mail.attach_file(filename)
    mail.send()


class Command(BaseCommand):
    def handle(self, *args, **options):
        # make sure to call main, since a view will call the same
        main()
