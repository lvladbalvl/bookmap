# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0014_point_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='point',
            name='page',
            field=models.IntegerField(default=1),
        ),
    ]
