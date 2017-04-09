# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controller_setup', '0023_auto_20160110_1230'),
    ]

    operations = [
        migrations.AddField(
            model_name='linkusertoplant',
            name='comment',
            field=models.CharField(default=b'', max_length=200),
        ),
        migrations.AlterField(
            model_name='linkusertoplant',
            name='host',
            field=models.CharField(default=b'localhost', max_length=50, choices=[(b'enerwhere.com', b'enerwhere.com'), (b'localhost', b'localhost')]),
        ),
        migrations.AlterField(
            model_name='linkusertoplant',
            name='plant',
            field=models.ForeignKey(to='controller_setup.Plant'),
        ),
        migrations.AlterField(
            model_name='linkusertoplant',
            name='user',
            field=models.CharField(max_length=20),
        ),
    ]
