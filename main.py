from wsgiref import simple_server

import falcon

from resources import Polygon

from config import SERVER_POLYGON_PORT
from core.middlewares import SerializerMiddleware

app = falcon.API(middleware=[
    SerializerMiddleware(),
])

polygon = Polygon()

app.add_route('/polygon/{pk}', polygon)
app.add_route('/polygon', polygon, suffix='collection')


if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', SERVER_POLYGON_PORT, app)
    httpd.serve_forever()
