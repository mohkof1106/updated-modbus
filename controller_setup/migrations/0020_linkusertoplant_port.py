# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controller_setup', '0019_auto_20160110_1147'),
    ]

    operations = [
        migrations.AddField(
            model_name='linkusertoplant',
            name='port',
            field=models.IntegerField(null=True),
        ),
    ]
