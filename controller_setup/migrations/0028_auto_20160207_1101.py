# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controller_setup', '0027_auto_20160207_0959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='plant',
            field=models.ForeignKey(to='controller_setup.Plant'),
        ),
    ]
