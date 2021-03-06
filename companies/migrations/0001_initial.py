# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-18 00:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyAdmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('email', models.EmailField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CompanyModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('founded_by', models.CharField(max_length=255)),
                ('is_certified', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EmployeeModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=False)),
                ('dob', models.DateField()),
                ('blood_group', models.CharField(max_length=50)),
                ('mobile', models.CharField(max_length=10)),
                ('company', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='companies.CompanyModel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='companyadmin',
            name='company',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='companies.CompanyModel'),
        ),
    ]
