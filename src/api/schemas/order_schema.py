from marshmallow import Schema, fields, validate

class OrderItemInputSchema(Schema):
    product_id = fields.Str(required=True)
    quantity = fields.Int(required=True, validate=validate.Range(min=1))

class DeliveryInfoSchema(Schema):
    name = fields.Str(required=True)
    phone = fields.Str(required=True)
    address = fields.Str(required=True)

class CreateOrderSchema(Schema):
    customer_id = fields.Str(required=True)
    items = fields.List(fields.Nested(OrderItemInputSchema()), required=True, validate=validate.Length(min=1))
    delivery_info = fields.Nested(DeliveryInfoSchema(), required=True)

class OrderItemOutputSchema(Schema):
    product_id = fields.Str()
    quantity = fields.Int()
    price_at_order = fields.Float()

class OrderOutputSchema(Schema):
    id = fields.Str()
    status = fields.Method("get_status_name", dump_only=True)
    created_at = fields.DateTime()
    customer_name = fields.Str()
    customer_phone = fields.Str()
    customer_address = fields.Str()
    total_price = fields.Float()
    items = fields.List(fields.Nested(OrderItemOutputSchema()))

    def get_status_name(self, obj):
        return obj.status.value
