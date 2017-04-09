# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controller_setup', '0021_auto_20160110_1154'),
    ]

    operations = [
        migrations.AddField(
            model_name='linkusertoplant',
            name='distant_db_path',
            field=models.CharField(default=b'/home/pi/modbus_controller', max_length=200),
        ),
        migrations.AlterField(
            model_name='linkusertoplant',
            name='reverse_port',
            field=models.IntegerField(help_text=b'The port to connect to the reverse ssh, eg user pi1@HOST does ssh -p REVERSE_PORT pi@localhost to connect. Do not mix with the port used to connect to USER (22 by default)', null=True),
        ),
    ]
