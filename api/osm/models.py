from django.contrib.gis.db import models


class Building(models.Model):
    osm_id = models.CharField(blank=True, max_length=80)
    osm_way_id = models.CharField(
        blank=True, max_length=80, unique=True
    )
    name = models.CharField(blank=True, max_length=128)

    building = models.CharField(blank=True, max_length=80)
    building_l = models.CharField(blank=True, max_length=80)
    building_m = models.CharField(blank=True, max_length=80)
    addr_full = models.CharField(blank=True, max_length=80)
    addr_house = models.CharField(blank=True, max_length=80)
    addr_stree = models.CharField(blank=True, max_length=80)
    addr_city = models.CharField(blank=True, max_length=80)
    office = models.CharField(blank=True, max_length=80)
