from django_filters import rest_framework as filters

from infrastructure.date_util import day_iterator_inclusive
from routes import models as routes_models


def _fill_out(when_start, when_end, available_days):
    available_days = set(available_days)
    dicts = [
        dict(day=day, available=day in available_days)
        for day in day_iterator_inclusive(when_start, when_end)
    ]
    return dicts


def find_route_availabilities(
    origin_code, cabin, n_passengers, outbound_start, outbound_end,
    inbound_start=None, inbound_end=None
):
    outbound_by_route = routes_with_availability(
        [origin_code], cabin, outbound_start, outbound_end, n_passengers,
    )

    route_availabilities_by_destination = {
        route.destination: RouteAvailability(
            route,
            availability=outbound_by_route[route],
        )
        for route, availability in outbound_by_route.items()
    }

    if inbound_start and inbound_end:
        route_codes = [r.destination.code for r in outbound_by_route.keys()]
        inbound_by_route = routes_with_availability(
            route_codes, cabin, inbound_start, inbound_end, n_passengers,
            destination_code=origin_code
        )
        available_destinations = set()
        for inbound_route, availability in inbound_by_route.items():
            route_availability = (
                route_availabilities_by_destination[inbound_route.origin]
            )
            route_availability.inbound_availability = availability
            available_destinations.add(inbound_route.origin)
    else:
        available_destinations = set(route_availabilities_by_destination.keys())

    return [
        route_availability
        for destination, route_availability in
            route_availabilities_by_destination.items()
        if destination in available_destinations
    ]


def routes_with_availability(
    origin_codes, cabin, when_start, when_end, n_passengers,
    destination_code=None
):
    seat_field = routes_models.RouteAvailability.seat_field_name(n_passengers)
    filter_kwargs = dict(
        route__origin__code__in=origin_codes,
        cabin=cabin,
        day__range=(when_start, when_end),
        **{seat_field: True}
    )
    if destination_code:
        filter_kwargs['route__destination__code'] = destination_code

    route_id_days = (
        routes_models.RouteAvailability.objects
        .filter(**filter_kwargs)
        .order_by('day')
        .values_list('route', 'day')
    )

    days_by_route_id = {}
    for route_id, day in route_id_days:
        days_by_route_id.setdefault(route_id, []).append(day)

    routes = (
        routes_models.Route.objects.filter(id__in=days_by_route_id.keys())
        .prefetch_related('destination', 'origin')
    )
    return {
        route: _fill_out(when_start, when_end, days_by_route_id.get(route.id))
        for route in routes
    }


class RouteAvailability():
    def __init__(self, route, availability, inbound_availability=None):
        self.route = route
        self.origin_code = route.origin.code
        self.destination_code = route.destination.code
        self.availability = availability
        self.inbound_availability = inbound_availability
