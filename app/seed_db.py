from app import db
from app.models import ImageModel, ReleaseModel, DistroModel
from datetime import datetime

distro1 = DistroModel(name="ubuntu", company="Canonical", datetime_added=datetime.utcnow(), datetime_modified=datetime.utcnow())
distro2 = DistroModel(name="centos", company="RedHat", datetime_added=datetime.utcnow(), datetime_modified=datetime.utcnow())

release1 = ReleaseModel(name="16.04", datetime_added=datetime.utcnow(), datetime_modified=datetime.utcnow(), distro_id=1)
release2 = ReleaseModel(name="18.04", datetime_added=datetime.utcnow(), datetime_modified=datetime.utcnow(), distro_id=1)
release3 = ReleaseModel(name="6", datetime_added=datetime.utcnow(), datetime_modified=datetime.utcnow(), distro_id=2)
release4 = ReleaseModel(name="7", datetime_added=datetime.utcnow(), datetime_modified=datetime.utcnow(), distro_id=2)

db.session.add_all([distro1, distro2, release1, release2, release3, release4 ])
db.session.commit()