# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-21 00:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0002_auto_20161220_2159'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='price',
            field=models.DecimalField(decimal_places=2, default=20.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='products',
            name='quantity',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='orders',
            name='status',
            field=models.CharField(default='processing', max_length=30, null=True),
        ),
    ]
