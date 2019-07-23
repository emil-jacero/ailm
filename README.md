## Description
This project aims to manage operating system images from different public sources (ex. ubuntu and centos) and keep them up to date. It uses webscraping to get the latest builds of the images and stores them locally or in S3 compatible storage.

Using a customizable schema that defines what image, how many versions and schedule, it will strive to keep that at the destionation location (ex. Glance).


## Q&A
**Question:** Why is this a thing?

**Answer:** Stop updating images manually! Automation is key.


## Tasks
- [x] Support Ubuntu
- [x] Support Centos
- [ ] Support RedHat
- [ ] Support CoreOS
- [ ] Support Cirros
- [ ] Support Windows Server (Manually. Maybe automatically in the future)
- [x] Download to local filesystem
- [ ] Download to S3 compatible APIs
- [ ] Upload to Glance
- [ ] Design customizable schema
- [ ] Implement simple web frontend


## Environment variables (development, only postgres running as docker)
    export FLASK_APP=rest_api
    export FLASK_ENV=development
    
    export POSTGRES_URL="localhost:5432"
    export POSTGRES_USER="postgres"
    export POSTGRES_PW="postgres"
    export POSTGRES_DB="postgres"
