from marshmallow import fields, Schema


class PolygonPostSchema(Schema):

    class Meta:
        strict = True

    class_id = fields.Integer(required=True)
    name = fields.Str(required=True)
    props = fields.Dict(required=True)
    geom = fields.List(cls_or_instance=fields.List(cls_or_instance=fields.Integer), required=True)


class PolygonPatchSchema(PolygonPostSchema):
    pass
