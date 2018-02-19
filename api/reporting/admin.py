from django.contrib.gis import admin
from reporting.models import Report


admin.site.register(Report, admin.GeoModelAdmin)
