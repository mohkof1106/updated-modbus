# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controller_setup', '0017_auto_20160110_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linkusertoplant',
            name='plant',
            field=models.ForeignKey(to='controller_setup.Plant', unique=True),
        ),
        migrations.AlterField(
            model_name='linkusertoplant',
            name='user',
            field=models.CharField(unique=True, max_length=20),
        ),
    ]
