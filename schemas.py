from marshmallow import Schema, fields


class SetValueSchema(Schema):
    key = fields.Str(required=True)
    value = fields.Str(required=True)


class ExpireSchema(Schema):
    key = fields.Str(required=True)
    seconds = fields.Int(required=True, validate=lambda n: n > 0)
