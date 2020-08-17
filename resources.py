import json

import falcon

from db.models import polygon_table, conn
from schema import PolygonPostSchema, PolygonPatchSchema
from common.utils import prepare_polygon_data, prepare_geom
from db.templates import *


class Polygon:
    serializers = {
        'post': PolygonPostSchema,
        'patch': PolygonPatchSchema,
    }

    def on_get(self, req, resp, pk):
        epsg_type = req.params.get('epsg')
        q = get_polygon.format(pk)

        s = conn.execute(q)
        data = s.fetchone()
        if data is None:
            resp.body = json.dumps({'message': 'not found'})
            resp.status = falcon.HTTP_404
            return
        resp.status = falcon.HTTP_200
        resp.body = prepare_polygon_data([data], epsg_type, False)

    def on_patch(self, req, resp, pk):
        serializer = req.context['serializer']
        geom = req.media['geom']

        polygon = conn.execute(polygon_table.select(polygon_table.c.id == pk))
        if polygon.fetchone() is None:
            resp.status = falcon.HTTP_404
            resp.body = json.dumps({'message': 'not found'})
            return

        q = update_polygon.format(
            req.media['class_id'],
            req.media['name'],
            json.dumps(req.media['props']),
            prepare_geom(geom),
            pk
        )

        try:
            res = conn.execute(q)
            if res:
                resp.status = falcon.HTTP_200
                resp.body = prepare_polygon_data(res, '', False)
        except Exception as e:
            raise e

    def on_delete(self, req, resp, pk):
        try:
            polygon_delete = polygon_table.delete(polygon_table.c.id == pk)
            if conn.execute(polygon_delete) is not None:
                resp.status = falcon.HTTP_204
        except Exception as e:
            raise e

    def on_get_collection(self, req, resp):
        epsg_type = req.params.get('epsg')

        s = conn.execute(get_polygons)
        data = s.fetchmany(10)
        resp.status = falcon.HTTP_200
        resp.body = prepare_polygon_data(data, epsg_type)

    def on_post_collection(self, req, resp):
        serializer = req.context['serializer']
        geom = req.media['geom']
        q = create_polygon.format(
                req.media['class_id'],
                req.media['name'],
                json.dumps(req.media['props']),
                prepare_geom(geom),
            )
        try:
            res = conn.execute(q)
            if res:
                resp.status = falcon.HTTP_201
                resp.body = prepare_polygon_data(res, '', False)
        except Exception as e:
            raise e
