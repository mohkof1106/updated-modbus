# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controller_setup', '0020_linkusertoplant_port'),
    ]

    operations = [
        migrations.RenameField(
            model_name='linkusertoplant',
            old_name='port',
            new_name='reverse_port',
        ),
    ]
