from django.contrib.gis.db import models
from django.contrib.gis.geos import Point


class Venue(models.Model):
    foursquare_id = models.CharField(
        max_length=64, unique=True
    )
    name = models.CharField(max_length=256)
    location = models.PointField()
    categories = models.ManyToManyField(
        'venues.FoursquareCategory', through='venues.VenueCategory'
    )
    checkins_count = models.IntegerField()
    users_count = models.IntegerField()
    tip_count = models.IntegerField()
    url = models.URLField()
    formatted_address = models.TextField()

    @classmethod
    def get_or_create_from_api(cls, venue_response):
        location = Point(
            venue_response['location']['lng'],
            venue_response['location']['lat'],
        )
        return cls.objects.get_or_create(
            foursquare_id=venue_response['id'],
            defaults=dict(
                name=venue_response['name'],
                location=location,
                checkins_count=venue_response['stats']['checkinsCount'],
                users_count=venue_response['stats']['usersCount'],
                tip_count=venue_response['stats']['tipCount'],
                url=venue_response['url'],
                formatted_address=(
                    venue_response['location'].get('formattedAddress')
                )
            )
        )

    def get_or_create_from_api(cls, venue_response):
        return

class FoursquareCategory(models.Model):
    foursquare_id = models.CharField(max_length=64, unique=True)

    name = models.CharField(max_length=256)
    plural_name = models.CharField(max_length=256)
    short_name = models.CharField(max_length=256)
    icon = models.URLField()

    @classmethod
    def get_or_create_from_api(cls, category_response):
        return cls.objects.get_or_create(
            foursquare_id=category_response['id'],
            defaults={
                'name': category_response['name'],
                'plural_name': category_response['pluralName'],
                'short_name': category_response['shortName'],
                'icon': (
                    category_response['icon']['prefix'] +
                    category_response['icon']['suffix']
                )
            }
        )


class VenueCategory(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.PROTECT)
    category = models.ForeignKey(FoursquareCategory, on_delete=models.PROTECT)
    is_primary = models.BooleanField()

    class Meta:
        unique_together = ('venue', 'category')


    @classmethod
    def get_or_create_from_api(cls, category_response, venue):
        category, _ = FoursquareCategory.get_or_create_from_api(
            category_response
        )
        return cls.objects.get_or_create(
            category=category, venue=venue,
            is_primary=category_response.get('primary', False)
        )
