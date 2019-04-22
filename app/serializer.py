from app import ma
from app.models import ReleaseModel, ImageModel, DistroModel
from marshmallow import fields, Schema


class DistroSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    company = fields.String()
    datetime_added = fields.DateTime()
    datetime_modified = fields.DateTime()


class ReleaseSchema(Schema):
    id = fields.Integer(dump_only=True)
    release = fields.String()
    company = fields.String()
    distro = fields.Nested(DistroSchema)
    datetime_added = fields.DateTime()
    datetime_modified = fields.DateTime()


class ImageSchema(Schema):
    id = fields.Integer(dump_only=True)
    build = fields.String()
    uuid = fields.String()
    name = fields.String()
    sha256 = fields.String()
    archive_path = fields.String()
    archive_filename = fields.String()
    file_suffix = fields.String()
    url = fields.String()
    release = fields.Nested(ReleaseSchema)
    datetime_added = fields.DateTime()
    datetime_modified = fields.DateTime()

