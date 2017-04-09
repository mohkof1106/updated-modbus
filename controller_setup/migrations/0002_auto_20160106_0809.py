# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controller_setup', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddressMapping',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.IntegerField()),
                ('label', models.CharField(default=b'', max_length=200)),
                ('factor', models.FloatField(default=1, help_text=b'The abstract value is stored in the table mutliplied by the factor, eg 50.0% is 500, factor 10.')),
                ('unit', models.CharField(default=b'undf unit', max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='table',
            name='data_format',
            field=models.CharField(default=b'', help_text=b'Use for example >H, must be a precise value that must work for modbus_tk', max_length=10),
        ),
        migrations.AddField(
            model_name='addressmapping',
            name='table',
            field=models.ForeignKey(to='controller_setup.Table'),
        ),
    ]
