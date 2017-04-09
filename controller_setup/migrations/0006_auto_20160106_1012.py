# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controller_setup', '0005_addressmapping_template'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='file_name',
            field=models.CharField(default=b'', help_text=b'Leave blank if manually defined by the user, otherwise this field get the name of the xml file in the templates folder', unique=True, max_length=200, blank=True),
        ),
    ]
