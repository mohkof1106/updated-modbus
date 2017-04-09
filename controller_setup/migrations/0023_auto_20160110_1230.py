# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controller_setup', '0022_auto_20160110_1203'),
    ]

    operations = [
        migrations.RenameField(
            model_name='linkusertoplant',
            old_name='distant_db_path',
            new_name='distant_project_path',
        ),
    ]
