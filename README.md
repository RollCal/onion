# 🧅 Oπnion
Oπnion provides a discussion platform where users can freely share and exchange diverse opinions on the internet, creating a space where they can express personal viewpoints and experience various perspectives.

## 🔧 Environment

![image](https://github.com/RollCal/onion/assets/156996387/eae1642f-00e6-4989-b804-75791ee9473f)

- Python: 3.11
- React:
- Nginx: 
- Redis: 7.2.5
- Postgresql: 16.3

## 🐋 Docker Setting

Run the following two commands in the root directory of the project to create both deployment and development environments:

``
docker-compose -f docker-compose.yml -p dep up -d
``

``
docker-compose -f docker-compose-develop.yml -p dev up
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
