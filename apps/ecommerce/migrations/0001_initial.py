# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-20 02:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BillingAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=30)),
                ('state', models.CharField(max_length=30)),
                ('zipcode', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=255)),
                ('inventory', models.PositiveSmallIntegerField(default=0)),
                ('ongoing', models.CharField(max_length=5)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='productofcategory', to='ecommerce.Categories')),
            ],
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=30)),
                ('state', models.CharField(max_length=30)),
                ('zipcode', models.CharField(max_length=30)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='shipoforder', to='ecommerce.Orders')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='order_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='ordersofproduct', to='ecommerce.Orders'),
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='product_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='productoforder', to='ecommerce.Products'),
        ),
        migrations.AddField(
            model_name='images',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='imageofproduct', to='ecommerce.Products'),
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='billoforder', to='ecommerce.Orders'),
        ),
    ]