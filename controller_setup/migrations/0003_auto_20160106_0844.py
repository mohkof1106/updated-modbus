# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('controller_setup', '0002_auto_20160106_0809'),
    ]

    operations = [
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(default=b'user defined template', max_length=200)),
                ('file_name', models.CharField(default=b'', help_text=b'Leave blank if manually defined by the user, otherwise this field get the name of the xml file in the templates folder', max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='table',
            name='template_name',
            field=models.CharField(default='U16', help_text=b'The name usually used in the templates, like U16 or S32', max_length=20),
            preserve_default=False,
        ),
    ]
