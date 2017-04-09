# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controller_setup', '0018_auto_20160110_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linkusertoplant',
            name='plant',
            field=models.OneToOneField(to='controller_setup.Plant'),
        ),
    ]
