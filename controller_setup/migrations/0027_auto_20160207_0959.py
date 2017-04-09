# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controller_setup', '0026_auto_20160207_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linkusertoplant',
            name='HWaddr',
            field=models.CharField(help_text=b"The hardware MAC address from the controller (RPi, etc). Found with command:sudo ifconfig | grep eth0 | tr -s ' ' | awk -F'[ ]' '{if (/HWaddr/) print $5}'", unique=True, max_length=25),
        ),
    ]
