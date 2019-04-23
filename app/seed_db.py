from app import db
from app.models import ImageModel, ReleaseModel, DistroModel
from datetime import datetime

distro1 = dict()
distro1['name'] = "ubuntu"
distro1['company'] = "Canonical"
distro1['datetime_added'] = datetime.utcnow()
distro1['datetime_modified'] = datetime.utcnow()

distro2 = dict()
distro2['name'] = "centos"
distro2['company'] = "RedHat"
distro2['datetime_added'] = datetime.utcnow()
distro2['datetime_modified'] = datetime.utcnow()


release1 = dict()
release1['name'] = "16.04"
release1['datetime_added'] = datetime.utcnow()
release1['datetime_modified'] = datetime.utcnow()
release1['distro_id'] = 1

release2 = dict()
release2['name'] = "18.04"
release2['datetime_added'] = datetime.utcnow()
release2['datetime_modified'] = datetime.utcnow()
release2['distro_id'] =1

release3 = dict()
release3['name'] = "6"
release3['datetime_added'] = datetime.utcnow()
release3['datetime_modified'] = datetime.utcnow()
release3['distro_id'] = 2

release4 = dict()
release4['name'] = "7"
release4['datetime_added'] = datetime.utcnow()
release4['datetime_modified'] = datetime.utcnow()
release4['distro_id'] = 2


objects = [DistroModel(distro1),
           DistroModel(distro2),
           ReleaseModel(release1),
           ReleaseModel(release2),
           ReleaseModel(release3),
           ReleaseModel(release4)]
db.session.bulk_save_objects(objects)
db.session.commit()