# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-06 05:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0003_bookmap'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookmap',
            name='path',
        ),
        migrations.AddField(
            model_name='bookmap',
            name='upload',
            field=models.FileField(default='test', upload_to='uploads/'),
        ),
    ]
