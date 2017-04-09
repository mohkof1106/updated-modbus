# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controller_setup', '0028_auto_20160207_1101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linkusertoplant',
            name='comment',
            field=models.CharField(default=b'', help_text=b"Optional. Will appear on the 'control' page", max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='linkusertoplant',
            name='distant_project_path',
            field=models.CharField(default=b'/home/pi/modbus_controller', help_text=b'Absolute path on the local controller to the project folder', max_length=200),
        ),
        migrations.AlterField(
            model_name='table',
            name='callback',
            field=models.IntegerField(default=0, choices=[(1, b'two 16bits to form a 32bits, for data_format=>HH'), (0, b'length one answer, ex (xxx,)'), (2, b'concatenate strings'), (3, b'swapped version of 2*16bits->1*32bits, make sure your data_format is correct, so either unsigned >HH or signed >hh')]),
        ),
        migrations.AlterField(
            model_name='table',
            name='data_format',
            field=models.CharField(default=b'', help_text=b'Use for example >H, must be a precise value that must work for modbus_tk. For more information and example see https://docs.python.org/2/library/struct.html#format-characters', max_length=10),
        ),
    ]
