# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controller_setup', '0012_measure_mapping'),
    ]

    operations = [
        migrations.AddField(
            model_name='plant',
            name='DGs_min',
            field=models.FloatField(default=5000, help_text=b'in Watt'),
        ),
        migrations.AddField(
            model_name='plant',
            name='email',
            field=models.EmailField(default=b'controller@enerwhere.com', max_length=254),
        ),
        migrations.AddField(
            model_name='plant',
            name='inverter_max_output',
            field=models.FloatField(default=20000, help_text=b'in Watt'),
        ),
        migrations.AddField(
            model_name='plant',
            name='max_prod',
            field=models.FloatField(default=99.9, help_text=b'in %', verbose_name=b'Maximum power output'),
        ),
        migrations.AddField(
            model_name='plant',
            name='min_prod',
            field=models.FloatField(default=0, help_text=b'in %', verbose_name=b'Minimum power output'),
        ),
        migrations.AddField(
            model_name='plant',
            name='refresh_period',
            field=models.FloatField(default=30, help_text=b'in seconds'),
        ),
        migrations.AddField(
            model_name='plant',
            name='send_email',
            field=models.BooleanField(default=True, verbose_name=b'Activate notification emails'),
        ),
        migrations.AddField(
            model_name='plant',
            name='update_effect_time',
            field=models.FloatField(default=0.1, help_text=b'in seconds', verbose_name=b'Time for a write to be effective'),
        ),
        migrations.AddField(
            model_name='plant',
            name='update_error',
            field=models.IntegerField(default=10, help_text=b'in minutes', verbose_name=b'Time before sending an error msg'),
        ),
        migrations.AddField(
            model_name='plant',
            name='update_warning',
            field=models.IntegerField(default=5, help_text=b'in minutes', verbose_name=b'Time before sending a warning'),
        ),
        migrations.AlterField(
            model_name='measure',
            name='mapping',
            field=models.ForeignKey(editable=False, to='controller_setup.AddressMapping', help_text=b"Auto-update with the right mapping according to the address in the device's template", null=True),
        ),
    ]
