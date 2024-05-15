# 🧅 Oπnion
Oπnion provides a discussion platform where users can freely share and exchange diverse opinions on the internet, creating a space where they can express personal viewpoints and experience various perspectives.

## 🔧 Environment
- Python: 3.11
- Redis: 
- Postgresql: 
- Nginx: 

## 🐋 Docker Setting

Run the following two commands in the root directory of the project to create both deployment and development environments:

``
docker-compose -f docker-compose.yml -p dep up -d
``

``
docker-compose -f docker-compose-develop.yml -p dev up -d
``

If the containers stop due to a computer restart or any other reason, run the following two commands to restart the containers:

``
docker start develop-env
``

``
docker start deploy-env
``

## ERD

## API

# 🚀 Release Notes

## Opinion 0.1.0(0000-00-00)

### New Features:

### Improvements:

### Bug Fixes:

### Known Issues:

### Other Information: