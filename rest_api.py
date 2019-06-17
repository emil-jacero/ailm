from app import app, api, ma, db, celery
from app.models import ReleaseModel, ImageModel, DistroModel
from app.serializer import ReleaseSchema, ImageSchema
from flask_restful import Resource, reqparse
from flask import request, jsonify, Response
from datetime import datetime

from app.offload_functions import get_latest_release, download_image


image_temporary_path = "/home/emil/Development/Project_ailo/images/"


# Define schemas
release_schema = ReleaseSchema()
image_schema = ImageSchema()


class Release(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True)
        args = parser.parse_args()

        release = ReleaseModel.query.get(args['id'])
        ser_release = release_schema.dump(release).data
        return jsonify(ser_release)


class Releases(Resource):
    def get(self):
        all_releases = ReleaseModel.get_all_releases()
        ser_releases = release_schema.dump(all_releases, many=True).data
        return jsonify(ser_releases)


class Image(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True)
        args = parser.parse_args()

        image = ImageModel.query.get(args['id'])
        ser_image = image_schema.dump(image).data
        return jsonify(ser_image)

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True)
        args = parser.parse_args()

        image = ImageModel.query.get(args['id'])
        image.delete()
        result = dict()
        result['Message'] = {}
        result['Message'] = "Image deleted [id: {}, name: {}]".format(image.id, image.name)
        return jsonify(result)


class Images(Resource):
    def get(self):
        all_images = ImageModel.get_all_images()
        ser_images = image_schema.dump(all_images, many=True).data
        return jsonify(ser_images)


class ImageScheduleUpdate(Resource):
    def post(self):
        result = dict()
        parser = reqparse.RequestParser()
        parser.add_argument('distro', type=str, required=True)
        parser.add_argument('release', type=str, required=True)
        args = parser.parse_args()

        # Find and download latest release
        image = get_latest_release(args['distro'], args['release'])

        # Check if image already exist
        if ImageModel.image_exists(image.sha256):
            result['Message'] = {}
            result['Message'] = "The image already exist ({})".format(image.name, image.build)
        else:
            # Download image
            download_image(image, image_temporary_path)

            # Update database
            release = db.session.query(ReleaseModel).filter_by(name=args['release']).first()

            data = dict()
            data['build'] = image.build,
            data['uuid'] = image.uuid,
            data['name'] = image.name,
            data['sha256'] = image.sha256,
            data['archive_path'] = image.archive_path,
            data['archive_filename'] = image.archive_filename,
            data['file_suffix'] = image.file_suffix,
            data['source_url'] = image.source_url,
            data['release_id'] = release.id,
            data['datetime_added'] = datetime.utcnow(),
            data['datetime_modified'] = datetime.utcnow()

            db_image = ImageModel(data)
            db_image.save()
            result = image_schema.dump(db_image).data

        return jsonify(result)


class ImagesScheduleUpdate(Resource):
    def post(self):
        result = []
        image_db_data = []
        # Find and download latest release
        query = db.session.query(ReleaseModel, DistroModel).filter(ReleaseModel.distro_id == DistroModel.id).all()
        for release in query:
            release_name = release.ReleaseModel.name
            distro_name = release.DistroModel.name

            image = get_latest_release(release=release_name, distro=distro_name)
            release_distro_combo = "{}_{}".format(release_name, distro_name)

            # Check if image already exist
            message = {}
            if ImageModel.image_exists(image.sha256):
                message[release_distro_combo] = {}
                message[release_distro_combo]['Message'] = {}
                message[release_distro_combo]['Message'] = "The image already exist ({}-{})".format(image.name, image.build)
                result.append(message)
                print("The image already exist ({})".format(image.sha256))
            else:
                # Download image
                download_image(image, image_temporary_path)

                # Update database
                release = db.session.query(ReleaseModel).filter_by(name=release_name).first()

                data = dict()
                data['build'] = image.build,
                data['uuid'] = image.uuid,
                data['name'] = image.name,
                data['sha256'] = image.sha256,
                data['archive_path'] = image.archive_path,
                data['archive_filename'] = image.archive_filename,
                data['file_suffix'] = image.file_suffix,
                data['source_url'] = image.source_url,
                data['release_id'] = release.id,
                data['datetime_added'] = datetime.utcnow(),
                data['datetime_modified'] = datetime.utcnow()

                db_image = ImageModel(data)
                db_image.save()
                #image_db_data.append(db_image)
                #result = image_schema.dump(image_db_data, many=True).data
                result.append(image_schema.dump(db_image).data)

        return jsonify(result)


api_v1 = '/api/v1/'
api.add_resource(Release, f'{api_v1}release')
api.add_resource(Releases, f'{api_v1}releases')
api.add_resource(Image, f'{api_v1}image')
api.add_resource(Images, f'{api_v1}images')
api.add_resource(ImageScheduleUpdate, f'{api_v1}image/update')
api.add_resource(ImagesScheduleUpdate, f'{api_v1}images/update')


"""
@app.route('/celery', methods=['GET'])
def run_celery():
    result = add_together.delay(23, 42)
    result.wait()  # 65
    return jsonify(result.result)
"""

if __name__ == '__main__':
    app.run(debug=True)