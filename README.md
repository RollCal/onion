# 🧅 Oπnion
Oπnion provides a discussion platform where users can freely share and exchange diverse opinions on the internet, creating a space where they can express personal viewpoints and experience various perspectives.

## 📑 Table of Contents
- [Environment](#-environment)
- [Docker Setting](#-docker-setting)
- [Release Notes](#-release-notes)
- [Key Features](#key-features)
- [Usage](#usage)


## 🔧 Environment

![image](https://github.com/RollCal/onion/assets/159862122/8e0dba91-e3bc-4beb-8c0f-2a3451769ecd)

- [Python: 3.11](https://docs.python.org/ko/3.11/)
- [React: 18.3.1](https://react.dev/learn)
- [Nginx](https://nginx.org/en/docs/)
- [Redis: 7.2.5](https://redis.io/docs/latest/)
- [Postgresql: 16.3](https://www.postgresql.org/docs/current/index.html)

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

# 🚀 Release Notes

## Opinion 1.0.0

Thank you for using Opinion! We look forward to your feedback.

### Release Information
Version: 1.0
Release Date: 2024-06-13

### Development Period
- Start Date: 2024.05.10
- End Date: 2024.06.10

## Key Features

✔ Feature 1: Tree-Structured Posts

Feel free to leave comments under posts. Popular posts are linked and visualized in the post list!
  
✔ Feature 2: Personalized Content

Highlight popular posts tailored to various ages and genders!
  
✔ Feature 3: Embedding Search

Experience a more flexible and intuitive search experience!

## Usage
Here is how you can use Opinion:
[demo video](https://youtu.be/yBol1qEtEXc)
