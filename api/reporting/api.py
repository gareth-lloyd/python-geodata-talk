from datetime import date
import time

from django.db import transaction
from django.utils import timezone

from routes import models as routes_models
from avios_api import availability, locations
from infrastructure import date_util


CABINS = ['economy', 'premium_economy', 'business', 'first']


def _store_location(response_dict, parent=None, location=None):
    return routes_models.Location.objects.get_or_create(
        type=response_dict['type'],
        code=response_dict['code'],
        defaults=dict(
            name=response_dict['name'],
            location=location,
            parent=parent
        )
    )[0]


def store_locations():
    for region_dict in locations.get_regions():
        region = _store_location(region_dict)

        for country_dict in locations.get_by_type(
            region_dict, locations.TYPE_COUNTRY
        ):
            country = _store_location(country_dict, parent=region)

            for city_dict in locations.get_by_type(
                country_dict, locations.TYPE_CITY
            ):
                city = _store_location(city_dict, parent=country)

                for airport_dict in locations.get_by_type(
                    city_dict, locations.TYPE_AIRPORT
                ):
                    _store_location(airport_dict, parent=city)


def update_city_to_city_availability(route, cabin, n_passengers):
    assert route.origin.type == routes_models.Location.CITY
    assert route.destination.type == routes_models.Location.CITY
    assert n_passengers <= 4

    today = date.today()
    furthest = availability.furthest_availability_date()
    journey_availability = availability.get_city_to_city_availability(
        today, furthest, route.origin.code, route.destination.code,
        cabin, n_passengers
    )
    _store_city_to_city_availability(
        today, furthest, route, cabin, n_passengers, journey_availability,
    )


@transaction.atomic
def _store_city_to_city_availability(
    start, end, route, cabin, n_passengers, journey_availability
):
    should_be_present = set(
        date_util.day_iterator_inclusive(start, end)
    )
    are_present = set(
        routes_models.RouteAvailability.objects
        .filter(route=route, cabin=cabin)
        .values_list('day', flat=True)
    )
    for day_to_create in should_be_present.difference(are_present):
        routes_models.RouteAvailability.objects.create(
            route=route, cabin=cabin, day=day_to_create
        )

    seats_field = routes_models.RouteAvailability.seat_field_name(n_passengers)
    (
        routes_models.RouteAvailability.objects
        .filter(route=route, cabin=cabin, day__gte=start)
        .update(**{seats_field: False})
    )

    available_days = [
        day for day, available in journey_availability if available
    ]
    (
        routes_models.RouteAvailability.objects
        .filter(route=route, cabin=cabin, day__in=available_days)
        .update(**{seats_field: True, 'updated': timezone.now()})
    )


def update_city_to_region_availability(
    airline, city, region, cabin, n_passengers
):
    today = date.today()
    furthest = availability.furthest_availability_date()
    availability_iter = availability.get_city_to_continent_availability(
        today, furthest, city.code, region.code, cabin, n_passengers
    )
    for origin_code, destination_code, availability_dict in availability_iter:
        origin = routes_models.Location.objects.get(
            type=routes_models.Location.CITY, code=origin_code
        )
        destination = routes_models.Location.objects.get(
            type=routes_models.Location.CITY, code=destination_code
        )
        route, _ = routes_models.Route.objects.get_or_create(
            origin=origin, destination=destination, airline=airline
        )
        _store_city_to_city_availability(
            today, furthest, route, cabin, n_passengers, availability_dict
        )


def update_city_availability(airline, city):
    regions = (
        routes_models.Location.objects.filter(
            type=routes_models.Location.REGION
        )
    )

    for region in regions:
        for cabin in CABINS:
            for n_passengers in [1, 2, 3, 4]:
                time.sleep(2)
                update_city_to_region_availability(
                    airline, city, region, cabin, n_passengers
                )


def update_availability():
    airline = routes_models.Airline.objects.get()
    origin_cities = routes_models.Location.objects.filter(is_origin=True)
    for origin in origin_cities:
        update_city_availability(airline, origin)
