# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controller_setup', '0015_document'),
    ]

    operations = [
        migrations.CreateModel(
            name='Link_plant_to_user',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=20)),
                ('host', models.CharField(default=b'enerwhere.com', max_length=50, choices=[(b'enerwhere.com', b'enerwhere.com'), (b'localhost', b'localhost')])),
                ('plant', models.ForeignKey(to='controller_setup.Plant')),
            ],
        ),
    ]
