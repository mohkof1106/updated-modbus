# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controller_setup', '0011_auto_20160106_1312'),
    ]

    operations = [
        migrations.AddField(
            model_name='measure',
            name='mapping',
            field=models.ForeignKey(editable=False, to='controller_setup.AddressMapping', null=True),
        ),
    ]
