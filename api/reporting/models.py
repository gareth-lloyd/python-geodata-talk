from django.contrib.gis.db import models


class Airline(models.Model):
    name = models.CharField(max_length=64, unique=True)
    loyalty_scheme_name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Location(models.Model):
    CITY = 'CITY'
    REGION = 'REGION'
    AIRPORT = 'AIRPORT'
    COUNTRY = 'COUNTRY'
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=8)
    type = models.CharField(max_length=16, db_index=True)
    parent = models.ForeignKey(
        'self', blank=True, null=True, related_name='children',
        on_delete=models.PROTECT
    )
    location = models.PointField(blank=True, null=True)
    is_origin = models.BooleanField(default=False)

    class Meta:
        unique_together = ('code', 'type')

    def __str__(self):
        return self.name


class Route(models.Model):
    origin = models.ForeignKey(
        Location, related_name='routes', on_delete=models.PROTECT
    )
    destination = models.ForeignKey(
        Location, related_name='inbound_routes', on_delete=models.PROTECT
    )
    airline = models.ForeignKey(Airline, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('origin', 'destination', 'airline')

    def __str__(self):
        return "{} to {} with {}".format(
            self.origin, self.destination, self.airline
        )


class RouteAvailability(models.Model):
    updated = models.DateTimeField(auto_now=True)
    route = models.ForeignKey(
        Route, on_delete=models.PROTECT, related_name='availability'
    )
    day = models.DateField()
    miles_cost = models.IntegerField(blank=True, null=True)
    cabin = models.CharField(max_length=16)

    # You can't ask the API "how many seats are available?"
    # but instead "Are there three seats available, yes or no?"
    seats_available_1 = models.BooleanField(default=False)
    seats_available_2 = models.BooleanField(default=False)
    seats_available_3 = models.BooleanField(default=False)
    seats_available_4 = models.BooleanField(default=False)

    @staticmethod
    def seat_field_name(seats):
        assert 1 <= seats <= 4
        return "seats_available_{}".format(seats)

    @property
    def some_availability(self):
        return (
            self.seats_available_1 or
            self.seats_available_2 or
            self.seats_available_3 or
            self.seats_available_4
        )

    class Meta:
        unique_together = ('route', 'day', 'cabin')

    def __str__(self):
        return "{} on {} in {}: {}".format(
            self.route, self.day, self.cabin,
            'available' if self.some_availability else 'unavailable'
        )
