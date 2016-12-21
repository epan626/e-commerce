# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-21 21:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0002_products_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(default='admin_app/img/img.jpg', upload_to='admin_app/img')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagetoproduct', to='ecommerce.Products')),
            ],
        ),
    ]