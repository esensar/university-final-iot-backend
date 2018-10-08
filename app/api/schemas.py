from marshmallow import Schema, post_dump


class BaseResourceSchema(Schema):
    @post_dump(pass_many=True)
    def wrap_with_envelope(self, data, many):
        return {'content': data}
