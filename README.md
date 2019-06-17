      ________  ___       __________ 
     /_  __/ / / / |     / /  _/ __ \
      / / / / / /| | /| / // // / / /
     / / / /_/ / | |/ |/ // // /_/ / 
    /_/  \____/  |__/|__/___/\____/  
                                     

## Summary
This project aims to manage operating system images from different sources (ex. ubuntu and centos) and keep them up to date at a destination storage. It will only support Opentack Glance at this moment.

Tuwio updates the images and keeps the two latest images from each distribution in Glance, hiding the older releases and eventually deletes them entirely.

Primarily it will support the most popular cloud ready Linux distributions. In the future it will support custom images like Windows Server.
In the far future it may even support generating Windows Server images with custom user scripts.


## Q&A
**Question:** Why is this a thing?

**Answer:** The hope is that this tool can keep the OS images up to date and keep the latest ones in Glance.


## Tasks
- [x] Support Ubuntu
- [x] Support Centos
- [ ] Support RedHat (Manually?)
- [ ] Support CoreOS
- [ ] Support Cirros
- [ ] Support Windows Server (Manually. Maybe automatically in the future)
- [x] Download to local filesystem
- [ ] Download to Swift/S3
- [ ] Upload to Glance
- [ ] Implement schedule & Celery workers
- [ ] Implement simple Bootstrap UI


## Environment variables (development, only postgres running as docker)
    export FLASK_APP=rest_api
    export FLASK_ENV=development
    
    export POSTGRES_URL="localhost:5432"
    export POSTGRES_USER="postgres"
    export POSTGRES_PW="postgres"
    export POSTGRES_DB="postgres"
