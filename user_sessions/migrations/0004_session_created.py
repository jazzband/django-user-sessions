# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime

def set_created(apps, schema_editor):
    Session = apps.get_model('user_sessions', 'Session')

    for obj in Session.objects.all():
        obj.created = obj.last_activity
        obj.save()

class Migration(migrations.Migration):

    dependencies = [
        ('user_sessions', '0003_auto_20161205_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 18, 12, 11, 0, 286186), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.RunPython(set_created, reverse_code=migrations.RunPython.noop),
    ]
