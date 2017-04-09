# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('read_only', models.BooleanField(default=True)),
                ('label', models.CharField(default=b'undf table label', max_length=200)),
                ('quantity_of_x', models.IntegerField(default=0)),
                ('data_format', models.CharField(default=b'', max_length=10)),
                ('block_type', models.IntegerField(default=0, choices=[(0, b'undf block type'), (1, b'COILS'), (2, b'DISCRETE_INPUTS'), (3, b'HOLDING_REGISTERS'), (4, b'ANALOG_INPUTS')])),
                ('read_function', models.IntegerField(default=0, choices=[(0, b'undf function code'), (1, b'READ_COILS'), (2, b'READ_DISCRETE_INPUTS'), (3, b'READ_HOLDING_REGISTERS'), (4, b'READ_INPUT_REGISTERS'), (5, b'WRITE_SINGLE_COIL'), (6, b'WRITE_SINGLE_REGISTER'), (7, b'READ_EXCEPTION_STATUS'), (8, b'DIAGNOSTIC'), (15, b'WRITE_MULTIPLE_COILS'), (16, b'WRITE_MULTIPLE_REGISTERS'), (23, b'READ_WRITE_MULTIPLE_REGISTERS')])),
                ('write_function', models.IntegerField(default=0, choices=[(0, b'undf function code'), (1, b'READ_COILS'), (2, b'READ_DISCRETE_INPUTS'), (3, b'READ_HOLDING_REGISTERS'), (4, b'READ_INPUT_REGISTERS'), (5, b'WRITE_SINGLE_COIL'), (6, b'WRITE_SINGLE_REGISTER'), (7, b'READ_EXCEPTION_STATUS'), (8, b'DIAGNOSTIC'), (15, b'WRITE_MULTIPLE_COILS'), (16, b'WRITE_MULTIPLE_REGISTERS'), (23, b'READ_WRITE_MULTIPLE_REGISTERS')])),
                ('callback', models.IntegerField(default=0, choices=[(1, b'two 16bits to form a 32bits'), (0, b'16bits answer')])),
            ],
        ),
    ]
