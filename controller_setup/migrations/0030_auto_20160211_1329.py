# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controller_setup', '0029_auto_20160209_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='callback',
            field=models.IntegerField(default=0, choices=[(1, b'two 16bits to form a 32bits, for data_format=>HH'), (0, b'length one answer, ex (xxx,)'), (2, b'concatenate strings'), (3, b'swapped version of 2*16bits->1*32bits, make sure your data_format is correct, so either unsigned >HH or signed >hh'), (4, b'unsigned 16bits to swap float'), (5, b'signed 16bits to swap float')]),
        ),
    ]
