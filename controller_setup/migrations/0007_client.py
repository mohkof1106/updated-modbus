# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controller_setup', '0006_auto_20160106_1012'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=200, blank=True)),
                ('host', models.IPAddressField()),
                ('port', models.IntegerField(default=502)),
                ('timeout_in_sec', models.FloatField(verbose_name=5.0)),
            ],
        ),
    ]
