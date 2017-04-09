# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controller_setup', '0008_auto_20160106_1154'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=200)),
                ('slave_id', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Plant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(unique=True, max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='client',
            name='timeout_in_sec',
            field=models.FloatField(default=5.0),
        ),
        migrations.AddField(
            model_name='device',
            name='client',
            field=models.ForeignKey(to='controller_setup.Client'),
        ),
        migrations.AddField(
            model_name='device',
            name='plant',
            field=models.ForeignKey(to='controller_setup.Plant'),
        ),
        migrations.AddField(
            model_name='device',
            name='template',
            field=models.ForeignKey(to='controller_setup.Template'),
        ),
    ]
