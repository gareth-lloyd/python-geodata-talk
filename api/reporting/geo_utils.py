from django.contrib.gis.geos import Point


# Spatial Reference IDs
GOOGLE_MAPS_ID = 3857
GPS_ID = 4326
BRITISH_NATIONAL_GRID = 27700


def transform(coord1, coord2, srid1, srid2):
    """
    Convert coordinates in one spatial reference system to another.

    For example, this can convert coordinates from GPS coordinates to Google
    Maps coordinates.

    Arguments:
        coord1 (float, int, long): horizontal coordinate
        coord2 (float, int, long): vertical coordinate
        srid1 (int): spacial reference ID for initial system
        srid2 (int): spacial reference ID for resulting system

    Output:
        (list): Coordinates in the target spatial reference system
    """
    point = Point(coord1, coord2, srid=srid1)
    point.transform(srid2)
    return [point.x, point.y]


def to_google(longitude, latitude):
    """
    Convert longitude-latitude coordinates to X-Y Google Maps coordinates.

    Arguments:
        longitude (float, int, long): degrees
        latitude (float, int, long): degrees

    Output:
        (list): Coordinates in metres, i.e. [x, y]
    """
    return transform(longitude, latitude, GPS_ID, GOOGLE_MAPS_ID)


def to_gps(x, y):
    """
    Convert X-Y Google Maps coordinates to longitude-latitude coordinates.

    Arguments:
        x (float, int, long): metres
        y (float, int, long): metres

    Output:
        (list): Coordinates in degrees, i.e. [longitude, latitude]
    """
    return transform(x, y, GOOGLE_MAPS_ID, GPS_ID)


def get_area_of_polygon_in_km2(polygon):
    """
    Return the area of polygon in metres squared.
    """
    return polygon.transform(BRITISH_NATIONAL_GRID, clone=True).area / 1000000
