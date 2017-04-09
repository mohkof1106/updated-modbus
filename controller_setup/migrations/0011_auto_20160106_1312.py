# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controller_setup', '0010_measure'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='measure',
            name='mapping',
        ),
        migrations.AddField(
            model_name='measure',
            name='address',
            field=models.IntegerField(default=1),
        ),
    ]
