      ________  ___       __________ 
     /_  __/ / / / |     / /  _/ __ \
      / / / / / /| | /| / // // / / /
     / / / /_/ / | |/ |/ // // /_/ / 
    /_/  \____/  |__/|__/___/\____/  
                                     

## Summary
This project aims to manage operating system images from different sources and keep them up to date on the destination.
The destination planned at this point is Openstack Glance.

It updates the images and keeps the two latest images from each distribution in Glance, hiding the older releases.

Primarily it will support the most popular cloud ready Linux distributions. In the short future it will support custom images as Windows Server.
In the far future it may even support generating Windows Server images with custom user scripts.


#### Q&A
**Question:** Why is this a thing?

**Answer:** The hope is that this tool can keep the images from automatic sources up to date and roll the releases at the destination.


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


## Environment variables (development)
    export FLASK_APP=rest_api
    export FLASK_ENV=development
    
    export POSTGRES_URL="localhost:5432"
    export POSTGRES_USER="postgres"
    export POSTGRES_PW="postgres"
    export POSTGRES_DB="postgres"
