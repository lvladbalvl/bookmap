# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-07 16:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0012_auto_20170407_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='point',
            name='x',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='point',
            name='y',
            field=models.FloatField(),
        ),
    ]