from django.contrib import admin

# Register your models here.
from .models import Table
class TableAdmin(admin.ModelAdmin):
    list_display = ['label', 'template_name', 'block_type', 'quantity_of_x', 'data_format', 'read_only', 'read_function', 'write_function', 'callback']
    list_filter = ['template_name', 'block_type']
admin.site.register(Table, TableAdmin)

from .models import AddressMapping
class MappingAdmin(admin.ModelAdmin):
    list_display = ['label', 'address', 'table', 'factor', 'unit', 'template']
    list_filter = ['template', 'unit']
admin.site.register(AddressMapping, MappingAdmin)

from .models import Template
class TemplateAdmin(admin.ModelAdmin):
    list_display = ['label', 'pretty', 'file_name']
    
    def pretty(self, obj):
        return obj.pretty_string()
admin.site.register(Template, TemplateAdmin)

from .models import Client
class ClientAdmin(admin.ModelAdmin):
    list_display = ['label', 'plant', 'host', 'port', 'timeout_in_sec']
    list_filter = ['plant', 'host', 'port']
admin.site.register(Client, ClientAdmin)

from .models import Plant
class PlantAdmin(admin.ModelAdmin):
    list_display = ['label', 'refresh_period', 'update_effect_time', 'DGs_min', 'inverter_max_output', 'min_prod', 'max_prod',\
        'update_warning', 'update_error', 'send_email', 'email']
admin.site.register(Plant, PlantAdmin)

from .models import Device
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['label', 'plant', 'template', 'slave_id', 'client']
    list_filter = ['plant']
admin.site.register(Device, DeviceAdmin)

from .models import Measure
class MeasureAdmin(admin.ModelAdmin):
    list_display = ['label', 'type', 'address', 'device', 'plant', 'mapping']
    list_filter = ['plant', 'type', 'device']
admin.site.register(Measure, MeasureAdmin)

from .models import Document
admin.site.register(Document)

from .models import LinkUserToPlant
class LinkAdmin(admin.ModelAdmin):
    list_display = ['user', 'host', 'plant', 'comment', 'local_user', 'reverse_port', 'distant_project_path', 'HWaddr']
admin.site.register(LinkUserToPlant, LinkAdmin)