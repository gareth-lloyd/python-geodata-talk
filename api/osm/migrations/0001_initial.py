# Generated by Django 2.0.2 on 2018-02-19 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('osm_id', models.CharField(blank=True, max_length=80)),
                ('osm_way_id', models.CharField(blank=True, max_length=80, unique=True)),
                ('name', models.CharField(blank=True, max_length=128)),
                ('building', models.CharField(blank=True, max_length=80)),
                ('building_l', models.CharField(blank=True, max_length=80)),
                ('building_m', models.CharField(blank=True, max_length=80)),
                ('addr_full', models.CharField(blank=True, max_length=80)),
                ('addr_house', models.CharField(blank=True, max_length=80)),
                ('addr_stree', models.CharField(blank=True, max_length=80)),
                ('addr_city', models.CharField(blank=True, max_length=80)),
                ('office', models.CharField(blank=True, max_length=80)),
            ],
        ),
    ]