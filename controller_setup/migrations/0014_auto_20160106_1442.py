# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controller_setup', '0013_auto_20160106_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='measure',
            name='type',
            field=models.IntegerField(default=0, choices=[(0, b'regular live value'), (1, b'revenue'), (2, b'solar'), (3, b'dg'), (4, b'inverter power'), (5, b'inverter read max'), (6, b'inverter write max')]),
        ),
        migrations.AlterField(
            model_name='plant',
            name='DGs_min',
            field=models.FloatField(default=5000, help_text=b'in Watt', verbose_name=b'DGs total minimum (W)'),
        ),
        migrations.AlterField(
            model_name='plant',
            name='inverter_max_output',
            field=models.FloatField(default=20000, help_text=b'in Watt', verbose_name=b'Inverter max output (W)'),
        ),
        migrations.AlterField(
            model_name='plant',
            name='refresh_period',
            field=models.FloatField(default=30, help_text=b'in seconds', verbose_name=b'Refresh period (s)'),
        ),
        migrations.AlterField(
            model_name='plant',
            name='update_effect_time',
            field=models.FloatField(default=0.1, help_text=b'in seconds', verbose_name=b'Time for a write to be effective (s)'),
        ),
        migrations.AlterField(
            model_name='plant',
            name='update_error',
            field=models.IntegerField(default=10, help_text=b'in minutes', verbose_name=b'Time before sending an error msg (min)'),
        ),
        migrations.AlterField(
            model_name='plant',
            name='update_warning',
            field=models.IntegerField(default=5, help_text=b'in minutes', verbose_name=b'Time before sending a warning (min)'),
        ),
    ]
