# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-12-07 04:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0009_auto_20161205_1728'),
    ]

    operations = [
        migrations.CreateModel(
            name='Use_case_management',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usercasename', models.CharField(max_length=255)),
                ('casedescribe', models.TextField()),
            ],
        ),
    ]
