# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-06 04:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0002_offer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bookmap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book', models.CharField(max_length=50, verbose_name='Book')),
                ('author', models.CharField(max_length=50, verbose_name='Author')),
                ('path', models.CharField(max_length=50, verbose_name='Path')),
            ],
        ),
    ]
