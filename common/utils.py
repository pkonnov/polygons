import datetime
import decimal
import json

import falcon
from shapely import ops
from shapely.geometry import Polygon
import pyproj

from geoalchemy2 import WKBElement


def alchemyencoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)
    elif isinstance(obj, WKBElement):
        return obj.desc


def prepare_geom(geom):
    geom_new = ''
    for p in geom:
        geom_new += str(p).replace("[", "")\
                        .replace("]", "") \
                        .replace(",", "") + ','
    return geom_new[:-1]


def convert_coordinates(polygon, epsg):
    try:
        transformer = pyproj.Transformer.from_proj(pyproj.Proj(init='epsg:4236'),
                                               pyproj.Proj(init=f'epsg:{epsg}'))
        return ops.transform(transformer.transform, polygon)
    except pyproj.exceptions.CRSError as e:
        description = 'Not found such type EPSG'
        raise falcon.HTTPError(falcon.HTTP_404,
                               'Type error',
                               description)


def prepare_polygon_data(data, epsg, collection=True):
    _data = [dict(p) for p in data]
    if epsg == '4326' or epsg is None or not epsg:
        return json.dumps(_data if collection else dict(_data[0]),
                          default=alchemyencoder)
    else:
        for item in data:
            geom = item['geom'][0]
            polygon = Polygon(geom)
            res = convert_coordinates(polygon, epsg)
            item['geom'][0] = list(res.exterior.coords[:-1])
        return json.dumps(_data if collection else dict(_data[0]),
                          default=alchemyencoder)


