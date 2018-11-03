from marshmallow import Schema, post_dump, fields


class BaseResourceSchema(Schema):
    @post_dump(pass_many=True)
    def wrap_with_envelope(self, data, many):
        return {'content': data}


class BaseTimestampedSchema(Schema):
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)


class BaseTimestampedResourceSchema(BaseResourceSchema, BaseTimestampedSchema):
    pass
