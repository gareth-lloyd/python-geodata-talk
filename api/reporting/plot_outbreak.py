import geopandas
import matplotlib
import shapely
from matplotlib import pyplot

from reporting import simulation
from reporting.simulation import NORTH, EAST, SOUTH, WEST


def plot_outbreak():
    from psycopg2 import connect
    connection = connect(dbname='johnsnow')
    cases = geopandas.read_postgis(
        "select * from reporting_report", connection,
        geom_col='location',
        crs={'init': 'epsg:4326'}
    )
    matplotlib.rcParams['figure.figsize'] = [16.0, 12.0]

    # Import London's rivers
    rivers = geopandas.read_file('../data/london-rivers_shp/')

    # Import London's roads
    roads = geopandas.read_file('../data/london-roads_shp/')
    # Filter the roads to just the most important ones
    mains = roads[roads['highway'].isin(('trunk', 'primary', 'secondary', 'tertiary'))]

    medical = geopandas.read_file('../data/london-medical_shp/')
    hospitals = medical[medical['amenity'] == 'hospital'].copy()

    # Create a polygone representing a zone around each hospital
    hospitals['geometry'] = hospitals['geometry'].buffer(0.001)

    # This is a polygon representing the whole area under study
    bounding_box = shapely.geometry.Polygon((
        (WEST, NORTH),
        (EAST, NORTH),
        (EAST, SOUTH),
        (WEST, SOUTH),
        (WEST, NORTH)
    ))

    # This is an area with holes in for each hospital zone
    # It will look like a slice of Swiss cheese
    minus_hospital_zones = bounding_box.difference(hospitals.unary_union)
    area_of_interest = geopandas.GeoDataFrame(
        {
            'geometry': [minus_hospital_zones],
            'name': ['Area of interest']
        },
        crs={'init': 'epsg:4326'}
    )

    # Now we do another spatial join saying
    non_hospital_cases = geopandas.sjoin(cases, area_of_interest, op='within')

    # Plot
    figure, axis = pyplot.subplots()
    rivers_plot = rivers.plot(ax=axis, color='blue', alpha=0.3)
    map_plot = mains.plot(ax=rivers_plot, color="black", alpha=0.2)
    cases_plot = non_hospital_cases.plot(
        ax=map_plot, marker="o", column="diagnosis", markersize=64, alpha=0.5
    )
    pyplot.show()
