# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-11-08 01:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='dict_test_case',
            fields=[
                ('id', models.IntegerField(max_length=11, primary_key=True, serialize=False)),
                ('caseName', models.CharField(blank=True, max_length=255)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('remark', models.CharField(max_length=255)),
                ('status', models.IntegerField(blank=True, max_length=11)),
                ('caseType', models.CharField(max_length=255)),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
