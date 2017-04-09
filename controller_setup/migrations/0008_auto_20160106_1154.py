# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controller_setup', '0007_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='host',
            field=models.GenericIPAddressField(),
        ),
    ]
