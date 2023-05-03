from combojsonapi.utils import Relationship
from marshmallow_jsonapi import Schema, fields


class DocumentSchema(Schema):
    class Meta:
        type_ = "document"
        self_url = "document_detail"
        self_url_kwargs = {"id": "<id>"}
        self_url_many = "document_list"

    id = fields.Integer(as_string=True)
    name = fields.String(allow_none=False, required=True)
    body = fields.String(allow_none=False, required=True)
    dt_created = fields.DateTime(allow_none=False)
    version = fields.DateTime(aallow_none=False, required=True)
    id_main = fields.Integer(as_string=True)
