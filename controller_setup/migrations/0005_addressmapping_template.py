# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controller_setup', '0004_auto_20160106_0846'),
    ]

    operations = [
        migrations.AddField(
            model_name='addressmapping',
            name='template',
            field=models.ForeignKey(default=1, to='controller_setup.Template'),
            preserve_default=False,
        ),
    ]
