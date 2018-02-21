# Putting Python on the Map
_Talk originally prepared for Pycon Namibia_

An exploration of the power of spatial data, with an application based on John Snow's 1854 Cholera map.

As I discuss, the famous map is somewhat [mythical](http://spatialgeek.com/blog/john-snow-the-myth-of-the-map/). It was not drawn until months after the epidemic had passed. What if we could do better with modern GIS technology?

## Code
### GeoDjango application

`/api` contains a Django application which scratches the surface of what's possible with GeoDjango by modelling reports of disease cases with geo-coordinates, and provides a simple Django Rest Framework API to read and write repots.

`/api/venues/` is an untested sketch of a way of importing FourSquare venues. It was an ambition for the talk which I didn't have time to complete.

### Angular application
`src/app` contains an Angular web application to locate the user and allow them to report disease cases.

### Analysis
`api/john-snow-analysis.ipynb` is a Jupyter Notebook containing a simple geospatial simulation and analysis of an "epidemic".

Running the analysis is independent of the other apps, but it will require a PostGIS database.

```bash
pip install -r requirements.txt
python api/manage.py migrate
python api/manage.py shell_plus --notebook
```


## Resources
### Libraries
#### GeoPandas

[This talk](https://www.youtube.com/watch?v=O1dNEt3P7Sw) is a fantastic taster of the GeoPandas's capabilities.

The [GeoPandas website](http://geopandas.org/) is a good introduction to the library.

#### GeoDjango

The [official docs](https://docs.djangoproject.com/en/2.0/ref/contrib/gis/) are the best place to go for installation advice and to get started.

#### Django Rest Framework

For creating geo-capable REST APIs in Django, use [Django REST Framework](http://www.django-rest-framework.org/api-guide/fields/#django-rest-framework-gis). 

There are [add-ons](https://github.com/djangonauts/django-rest-framework-gis) for read and write GeoJSON.

#### Shapely 

[Shapely](https://shapely.readthedocs.io/en/latest/) brings the spatial modelling power of [GEOS](https://trac.osgeo.org/geos) into Python, and powers a lot of GeoPandas functionality.


