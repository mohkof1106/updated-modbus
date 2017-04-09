# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controller_setup', '0009_auto_20160106_1208'),
    ]

    operations = [
        migrations.CreateModel(
            name='Measure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=200, blank=True)),
                ('device', models.ForeignKey(to='controller_setup.Device')),
                ('mapping', models.ForeignKey(to='controller_setup.AddressMapping')),
            ],
        ),
    ]
