import foursquare

from django.conf import settings

from venues import models as venues_models


CATS = {
    'arts': '4d4b7104d754a06370d81259',
    'college': '4d4b7105d754a06372d81259',
    'event': '4d4b7105d754a06373d81259',
    'food': '4d4b7105d754a06374d81259',
    'nightlife': '4d4b7105d754a06376d81259',
    'outdoors': '4d4b7105d754a06377d81259',
    'professional': '4d4b7105d754a06375d81259',
    'residence': '4e67e38e036454776db1fb3a',
    'shop': '4d4b7105d754a06378d81259',
    'transport': '4d4b7105d754a06379d81259',
}
API = 'https://api.foursquare.com/v2/'
VENUES = API + 'venues/search'

WINDHOEK = (-22.57, 17.083611)


def store_venues_near(category, coords, radius_m):
    for venue_response in get_venues(category.foursquare_id, coords, radius_m):
        venue, _ = venues_models.Venue.get_or_create_from_api(venue_response)
        for category_response in venue_response['categories']:
            venues_models.VenueCategory.get_or_create_from_api(
                category_response, venue
            )


def get_venues(category_id, coords, radius_m):
    client = foursquare.Foursquare(
        client_id=settings.FOURSQUARE_CLIENT_ID,
        client_secret=settings.FOURSQUARE_SECRET
    )
    return client.venues.search(params={
        'll': '{},{}'.format(coords[0], coords[1]),
        'radius': 10000,
        'intent': 'browse',
        'categoryId': category_id,
        'limit': 50
    })
