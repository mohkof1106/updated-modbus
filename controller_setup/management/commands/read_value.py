import logging
logger = logging.getLogger("live_control")

from django.core.management.base import BaseCommand
from optparse import make_option

from controller_setup.models import Measure, Device, AddressMapping

help_text = "You can read from a measure's pk, or with a device pk, and mapping pk"
class Command(BaseCommand):
    def __init__(self):
        super(Command, self).__init__()
        self.options = {}

    option_list = BaseCommand.option_list + (
        make_option('--measure', action='store', dest='measure', default=None, help='a measure pk'),
        make_option('--device', action='store', dest='device', default=None, help='if no measure, a device pk'),
        make_option('--mapping', action='store', dest='mapping', default=None, help='if no measure, an optional mapping pk')
    )

    def handle(self, *args, **options):
        self.options = options
        if self.options["measure"]:
            pk_measure = int(self.options["measure"])
            measure = Measure.objects.get(pk=pk_measure) # raise an error if measure does not exist
            print str(measure), "value:", measure.pull()
        elif self.options["device"]:
            pk_device = int(self.options["device"])
            device = Device.objects.get(pk=pk_device)
            if self.options["mapping"]:
                pk_mapping = int(self.options["mapping"])
                mapping = AddressMapping.objects.get(pk=pk_mapping)
                print str(mapping), "value:", device.get_value_for_mapping(mapping)
            else:
                mappings = AddressMapping.objects.filter(template=device.template)
                for mapping in mappings:
                    print str(mapping), "value:", device.get_value_for_mapping(mapping)
        print "Done"
        