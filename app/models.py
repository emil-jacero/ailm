from app import db
from datetime import datetime



## Image
class ImageModel(db.Model):
    __tablename__ = 'image'

    id = db.Column(db.Integer, primary_key=True)
    build = db.Column(db.String(40), nullable=False)
    uuid = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    sha256 = db.Column(db.String(200), nullable=False)
    archive_path = db.Column(db.String(200), nullable=False)
    archive_filename = db.Column(db.String(200), nullable=False)
    file_suffix = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(200), nullable=False)
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
        self.url = data.get('url')
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
    def get_all_images():
        return ImageModel.query.all()

    @staticmethod
    def get_one_image():
        return ImageModel.query.get(id)

    def __repr(self):
        return '<id {}>'.format(self.id)


## Release
class ReleaseModel(db.Model):
    __tablename__ = 'release'

    id = db.Column(db.Integer, primary_key=True)
    release = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(60), nullable=False)
    datetime_added = db.Column(db.DateTime)
    datetime_modified = db.Column(db.DateTime)
    distro_id = db.Column(db.Integer, db.ForeignKey('distro.id'), nullable=False)
    distro = db.relationship('DistroModel', backref='releases')

    # class constructor
    def __init__(self, data):
        self.distro = data.get('distro')
        self.release = data.get('release')
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
    def get_all_releases():
        return ReleaseModel.query.all()

    @staticmethod
    def get_one_release():
        return ReleaseModel.query.get(id)

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



"""
## Distro
class DistroModel(db.Model):
    __tablename__ = 'distro'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    company = db.Column(db.String(60), nullable=False)
    datetime_added = db.Column(db.DateTime)
    datetime_modified = db.Column(db.DateTime)
    #releases = db.relationship("ReleaseModel", backref="distro", lazy='joined')

    # class constructor
    def __init__(self, data):
        self.name = data.get('name')
        self.company = data.get('company')
        self.releases = data.get('releases')
        self.images = data.get('images')
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

"""

"""
class Distribution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime_added = db.Column(db.DateTime)
    datetime_changed = db.Column(db.DateTime)
    name = db.Column(db.String(60), nullable=False)
    company = db.Column(db.String(60), nullable=False)
    releases = db.relationship("Release", backref="distribution", lazy='dynamic')
    images = db.relationship("Image", backref="distribution", lazy='dynamic')


class Release(db.Model):
    __tablename__ = 'release3'
    id = db.Column(db.Integer, primary_key=True)
    datetime_added = db.Column(db.DateTime)
    datetime_changed = db.Column(db.DateTime)
    distribution_id = db.Column(db.Integer, db.ForeignKey('distribution.id'))
    release = db.Column(db.String(100), nullable=False)
    build = db.Column(db.String(40), nullable=True)
    images = db.relationship("Image", backref="release3", lazy='dynamic')


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    distribution_id = db.Column(db.Integer, db.ForeignKey('distribution.id'))
    release_id = db.Column(db.Integer, db.ForeignKey('release3.id'))
    datetime_added = db.Column(db.DateTime)
    datetime_changed = db.Column(db.DateTime)
    build = db.Column(db.String(40), nullable=False)
    uuid = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    md5 = db.Column(db.String(200), nullable=True)
    sha1 = db.Column(db.String(200), nullable=True)
    sha256 = db.Column(db.String(200), nullable=False)
    archive_path = db.Column(db.String(200), nullable=False)
    archive_filename = db.Column(db.String(200), nullable=False)
    file_suffix = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(200), nullable=False)

    def __init__(self, distribution_id, release_id, datetime_added, datetime_changed, build, uuid, name, sha256,
                 archive_path, archive_filename, file_suffix, url):
        self.distribution_id = distribution_id
        self.release_id = release_id
        self.datetime_added = datetime_added
        self.datetime_changed = datetime_changed
        self.build = build
        self.uuid = uuid
        self.name = name
        self.sha256 = sha256
        self.archive_path = archive_path
        self.archive_filename = archive_filename
        self.file_suffix = file_suffix
        self.url = url

"""



