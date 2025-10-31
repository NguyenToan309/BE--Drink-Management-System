from marshmallow import Schema, fields, validate

class ProductSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    price = fields.Float(required=True, validate=validate.Range(min=0.01))
