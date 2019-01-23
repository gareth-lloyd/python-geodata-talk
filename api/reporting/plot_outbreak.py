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

    # Import London's rivers
    rivers = geopandas.read_file('../open-street-map-data/london-rivers_shp/')

    # Import London's roads
    roads = geopandas.read_file('../open-street-map-data/london-roads_shp/')

    # Filter the roads to just the most important ones
    mains = roads[roads['highway'].isin(('trunk', 'primary', 'secondary', 'tertiary', 'unclassified'))]

    medical = geopandas.read_file('../open-street-map-data/london-hospitals_shp/')
    hospitals = medical[medical['amenity'] == 'hospital'].copy()

    # Create a polygon representing a zone around each hospital
    hospitals['geometry'] = hospitals['geometry'].buffer(0.0015)

    # Join together the hospital zones with the cases
    # The "join" is a spatial one - we are joining cases with hospitals they are close to
    joined_cases = geopandas.sjoin(
        left_df=cases,
        right_df=hospitals,
        how='left',
        op='within',
    )

    # Now we do another spatial join saying
    non_hospital_cases = joined_cases[joined_cases['name'].isnull()].copy()

    # Plot
    _, axes = pyplot.subplots()
    rivers.plot(ax=axes, color='blue', alpha=0.3)
    mains.plot(ax=axes, color="black", alpha=0.2)
    non_hospital_cases.plot(
        ax=axes, marker="o", column="diagnosis", markersize=64, alpha=0.5, legend=True
    )
    pyplot.show()
