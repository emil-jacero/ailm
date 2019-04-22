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
        parser.add_argument('release_id', type=int, required=True)
        args = parser.parse_args()

        release = ReleaseModel.query.get(args['release_id'])
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
        parser.add_argument('image_id', type=int, required=True)
        args = parser.parse_args()

        image = ImageModel.query.get(args['image_id'])
        ser_image = image_schema.dump(image).data
        return jsonify(ser_image)


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
            release = db.session.query(ReleaseModel).filter_by(release=args['release']).first()

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
        result = dict()
        # Find and download latest release
        query = db.session.query(ReleaseModel, DistroModel).filter(ReleaseModel.distro_id == DistroModel.id).all()
        for release in query:
            release_name = release.ReleaseModel.name
            distro_name = release.DistroModel.name
            print("TEST: {}-{}".format(release_name, distro_name))

            image = get_latest_release(release=release_name, distro=distro_name)
            release_distro_combo = "{}_{}".format(release_name, distro_name)

            # Check if image already exist
            if ImageModel.image_exists(image.sha256):
                result[release_distro_combo] = {}
                result[release_distro_combo]['Message'] = {}
                result[release_distro_combo]['Message'] = "The image already exist ({}-{})".format(image.name, image.build)
                print("The image already exist ({})".format(image.sha256))
            else:
                result = dict()
                # Download image
                download_image(image, image_temporary_path)

                # Update database
                release = db.session.query(ReleaseModel).filter_by(release=release_name).first()

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


api_v1 = '/api/v1/'
api.add_resource(Release, '{}release/'.format(api_v1))
api.add_resource(Releases, '{}releases/'.format(api_v1))
api.add_resource(Image, '{}image/'.format(api_v1))
api.add_resource(Images, '{}images/'.format(api_v1))
api.add_resource(ImageScheduleUpdate, '{}image/update'.format(api_v1))
api.add_resource(ImagesScheduleUpdate, '{}images/update'.format(api_v1))


"""
@app.route('/celery', methods=['GET'])
def run_celery():
    result = add_together.delay(23, 42)
    result.wait()  # 65
    return jsonify(result.result)


@app.route('/api/releases', methods=['GET'])
def get_releases():
    all_releases = ReleaseModel.get_all_releases()
    ser_releases = release_schema.dump(all_releases, many=True).data
    return jsonify(ser_releases)


@app.route('/api/images', methods=['GET'])
def get_images():
    all_images = ImageModel.get_all_images()
    ser_images = image_schema.dump(all_images, many=True).data
    return jsonify(ser_images)





## This initates a full refresh of all stored releases
@app.route('/api/update_all_images', methods=['GET'])
def update_all_images():
    # Get all releases from database and store in variable
    releases = ReleaseModel.get_all_releases()
    ser_releases = release_schema.dump(releases, many=True).data

    # Search each release (get url)
    latest_releases_list = []
    for release in releases:
        latest = get_latest_release(distro=release.distro,
                           release=release.release)
        # returns: build, name, sha256, suffix, url
        latest_releases_list.append(latest)

    # Compare each release with existing in database

    # Download all releases that are new
    result = []
    downloaded = {}
    for latest_release in latest_releases_list:
        image_uuid = uuid.uuid4()
        print(latest_release['url'])
        image = download_image(url=latest_release['url'], destination=root_path, uuid=image_uuid)
        downloaded['uuid'] = uuid
        downloaded['temp_path'] = image['path']
        downloaded['build'] = latest_release['build']
        downloaded['name'] = latest_release['name']
        downloaded['sha256'] = latest_release['sha256']
        downloaded['suffix'] = latest_release['suffix']
        downloaded['url'] = latest_release['url']
        result.append(downloaded)

    return jsonify(result)


## This
@app.route('/api/v1.0/latest_release', methods=['GET'])
def latest_release():
    parser = reqparse.RequestParser()
    parser.add_argument('distro', type=str, required=True)
    parser.add_argument('release', type=str, required=True)
    args = parser.parse_args()
    distro = args['distro']
    release = args['release']

    data = crawler.get_latest_release(distro, release)
    image_name = data['name']
    image_sha256 = data['sha256']
    image_url = data['url']
    image_build = data['build']
    image_suffix = data['suffix']

    return jsonify(data)

@app.route('/api/image', methods=['POST'])
def add_image():
    # Recieve input data
    distribution_id = 1
    release_id = 1
    datetime_added = datetime.now()
    datetime_changed = datetime.now()
    build = request.json['build']
    uuid = request.json['uuid']
    name = request.json['name']
    sha256 = request.json['sha256']
    archive_path = request.json['archive_path']
    archive_filename = request.json['archive_filename']
    file_suffix = request.json['file_suffix']
    url = request.json['url']

    new_image = ImageModel(distribution_id,
                      release_id,
                      datetime_added,
                      datetime_changed,
                      build,
                      uuid,
                      name,
                      sha256,
                      archive_path,
                      archive_filename,
                      file_suffix,
                      url)

    # Validate that input is correct

    # Validate that data not already exist

    # Store data

    # Retrieve stored data and return to caller

    db.session.add(new_image)
    db.session.commit()

    return new_image
"""

if __name__ == '__main__':
    app.run(debug=True)