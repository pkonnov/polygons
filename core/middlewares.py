import falcon.status_codes as status
from marshmallow import ValidationError

from core.errors import HTTPError  # it's our new HTTPError


class SerializerMiddleware:

    def process_resource(self, req, resp, resource, params):
        req_data = req.context.get('request') or req.media
        try:
            serializer = resource.serializers[req.method.lower()]
        except (AttributeError, IndexError, KeyError):
            return
        else:
            try:
                req.context['serializer'] = serializer().load(
                    data=req_data
                )
            except ValidationError as err:
                raise HTTPError(status=status.HTTP_400, errors=err.messages)

