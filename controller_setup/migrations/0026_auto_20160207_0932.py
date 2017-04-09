# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controller_setup', '0025_linkusertoplant_pi_hwaddr'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='linkusertoplant',
            name='pi_HWaddr',
        ),
        migrations.AddField(
            model_name='client',
            name='plant',
            field=models.ForeignKey(to='controller_setup.Plant', null=True),
        ),
        migrations.AddField(
            model_name='linkusertoplant',
            name='HWaddr',
            field=models.CharField(default='reset', help_text=b"The hardware MAC address from the controller (RPi, etc). Found with command:sudo ifconfig | grep eth0 | tr -s ' ' | awk -F'[ ]' '{if (/HWaddr/) print $5}'", max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='linkusertoplant',
            name='local_user',
            field=models.CharField(default=b'pi', help_text=b'The user on the controller that created the tunnel. It is the one that [user]@[HOST] finds with ssh -p [REVERSE_PORT] [local_user]@localhost', max_length=20),
        ),
        migrations.AddField(
            model_name='measure',
            name='modbus_function',
            field=models.IntegerField(default=0, help_text=b'This field is only read if multiple mappings are found for the same template and address, you may leave it at default if unused.', choices=[(0, b'undf block type'), (1, b'COILS'), (2, b'DISCRETE_INPUTS'), (3, b'HOLDING_REGISTERS'), (4, b'ANALOG_INPUTS')]),
        ),
        migrations.AddField(
            model_name='measure',
            name='plant',
            field=models.ForeignKey(editable=False, to='controller_setup.Plant', help_text=b'Auto-updated at every save', null=True),
        ),
        migrations.AlterField(
            model_name='device',
            name='plant',
            field=models.ForeignKey(editable=False, to='controller_setup.Plant', help_text=b'Auto-updated at every save', null=True),
        ),
        migrations.AlterField(
            model_name='linkusertoplant',
            name='comment',
            field=models.CharField(default=b'', max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='linkusertoplant',
            name='host',
            field=models.CharField(default=b'localhost', help_text=b'The host where the website can find the tunnel, for example from an enerwhere website, user enerwhere finds pi1@localhost', max_length=50, choices=[(b'enerwhere.com', b'enerwhere.com'), (b'localhost', b'localhost')]),
        ),
        migrations.AlterField(
            model_name='linkusertoplant',
            name='reverse_port',
            field=models.IntegerField(help_text=b'The port to connect to the reverse ssh, eg user pi1@HOST does ssh -p REVERSE_PORT [local_user]@localhost to connect. Do not mix with the port used to connect to USER (22 by default)', null=True),
        ),
        migrations.AlterField(
            model_name='linkusertoplant',
            name='user',
            field=models.CharField(help_text=b'The user where the website can find the tunnel, named pi1 in the example above', max_length=20),
        ),
        migrations.AlterField(
            model_name='table',
            name='callback',
            field=models.IntegerField(default=0, choices=[(1, b'two 16bits to form a 32bits, for data_format=>HH'), (0, b'length one answer, ex (xxx,)'), (2, b'concatenate strings')]),
        ),
        migrations.AlterField(
            model_name='table',
            name='template_name',
            field=models.CharField(help_text=b'The name usually used in the templates, like U16, S32 or String', max_length=20),
        ),
    ]
