from app import db
from datetime import datetime



## Image
class ImageModel(db.Model):
    __tablename__ = 'image'

    id = db.Column(db.Integer, primary_key=True)
    build = db.Column(db.String(40), nullable=False)
    uuid = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    sha256 = db.Column(db.String(200), nullable=False, unique=True)
    archive_path = db.Column(db.String(200), nullable=True)
    archive_filename = db.Column(db.String(200), nullable=True)
    file_suffix = db.Column(db.String(200), nullable=False)
    source_url = db.Column(db.String(200), nullable=False)
    datetime_added = db.Column(db.DateTime)
    datetime_modified = db.Column(db.DateTime)
    release_id = db.Column(db.Integer, db.ForeignKey('release.id'), nullable=False)
    release = db.relationship('ReleaseModel', backref='images')

    # class constructor
    def __init__(self, data):
        self.build = data.get('build')
        self.uuid = data.get('uuid')
        self.name = data.get('name')
        self.sha256 = data.get('sha256')
        self.archive_path = data.get('archive_path')
        self.archive_filename = data.get('archive_filename')
        self.file_suffix = data.get('file_suffix')
        self.source_url = data.get('source_url')
        self.datetime_added = data.get('datetime_added')
        self.datetime_modified = data.get('datetime_modified')
        self.release_id = data.get('release_id')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.datetime_modified = datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_images():
        return ImageModel.query.all()

    @staticmethod
    def get_one_image():
        return ImageModel.query.get(id)

    @staticmethod
    def image_exists(image_sha256):
        exists = db.session.query(db.exists().where(ImageModel.sha256 == image_sha256)).scalar()
        return exists

    def __repr(self):
        return '<id {}>'.format(self.id)


## Release
class ReleaseModel(db.Model):
    __tablename__ = 'release'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    datetime_added = db.Column(db.DateTime, default=datetime.utcnow())
    datetime_modified = db.Column(db.DateTime, default=datetime.utcnow())
    distro_id = db.Column(db.Integer, db.ForeignKey('distro.id'), nullable=False)
    distro = db.relationship('DistroModel', backref='releases')

    # class constructor
    def __init__(self, data):
        self.name = data.get('name')
        self.datetime_added = data.get('datetime_added')
        self.datetime_modified = data.get('datetime_modified')
        self.distro_id = data.get('distro_id')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.datetime_modified = datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_releases():
        return ReleaseModel.query.all()

    @staticmethod
    def get_one_release():
        return ReleaseModel.query.get(id)

    @staticmethod
    def get_release_by_id():
        return ReleaseModel.query.get(id)

    @staticmethod
    def get_release_by_name(release_name):
        return ReleaseModel.query.filter_by(name=release_name).first()

    def __repr(self):
        return '<id {}>'.format(self.id)


## Distro
class DistroModel(db.Model):
    __tablename__ = 'distro'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    company = db.Column(db.String(60), nullable=False)
    datetime_added = db.Column(db.DateTime)
    datetime_modified = db.Column(db.DateTime)

    # class constructor
    def __init__(self, data):
        self.name = data.get('name')
        self.company = data.get('company')
        self.datetime_added = data.get('datetime_added')
        self.datetime_modified = data.get('datetime_modified')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.datetime_modified = datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_distros():
        return DistroModel.query.all()

    @staticmethod
    def get_one_distro():
        return DistroModel.query.get(id)

    def __repr(self):
        return '<id {}>'.format(self.id)

class CloudModel(db.Model):
    __tablename__ = 'cloud'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    region = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    project_id = db.Column(db.String(32), nullable=False)
    domain_id = db.Column(db.String(32), nullable=False)
    datetime_added = db.Column(db.DateTime)
    datetime_modified = db.Column(db.DateTime)

    # class constructor
    def __init__(self, data):
        self.name = data.get('name')
        self.region = data.get('region')
        self.url = data.get('url')
        self.username = data.get('username')
        self.password = data.get('password')
        self.project_id = data.get('project_id')
        self.domain_id = data.get('domain_id')
        self.datetime_added = data.get('datetime_added')
        self.datetime_modified = data.get('datetime_modified')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.datetime_modified = datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_clouds():
        return DistroModel.query.all()

    @staticmethod
    def get_cloud_by_name(name):
        return ReleaseModel.query.filter_by(name=name).first()

    def __repr(self):
        return '<id {}>'.format(self.id)
