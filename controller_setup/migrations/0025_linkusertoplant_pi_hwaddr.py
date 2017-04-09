# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controller_setup', '0024_auto_20160113_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='linkusertoplant',
            name='pi_HWaddr',
            field=models.CharField(default='do it', help_text=b"The hardware MAC address from the controller (RPi). Found with command:ifconfig | grep eth0 | tr -s ' ' | awk -F'[ ]' '{if (/HWaddr/) print $5}'", unique=True, max_length=25),
            preserve_default=False,
        ),
    ]
