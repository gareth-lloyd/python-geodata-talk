# Generated by Django 2.0.2 on 2018-02-19 14:04

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FoursquareCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foursquare_id', models.CharField(max_length=64, unique=True)),
                ('name', models.CharField(max_length=256)),
                ('plural_name', models.CharField(max_length=256)),
                ('short_name', models.CharField(max_length=256)),
                ('icon', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foursquare_id', models.CharField(max_length=64, unique=True)),
                ('name', models.CharField(max_length=256)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('checkins_count', models.IntegerField()),
                ('users_count', models.IntegerField()),
                ('tip_count', models.IntegerField()),
                ('url', models.URLField()),
                ('formatted_address', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='VenueCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_primary', models.BooleanField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='venues.FoursquareCategory')),
                ('venue', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='venues.Venue')),
            ],
        ),
        migrations.AddField(
            model_name='venue',
            name='categories',
            field=models.ManyToManyField(through='venues.VenueCategory', to='venues.FoursquareCategory'),
        ),
        migrations.AlterUniqueTogether(
            name='venuecategory',
            unique_together={('venue', 'category')},
        ),
    ]