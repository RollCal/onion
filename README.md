# 🧅 Oπnion
Oπnion provides a discussion platform where users can freely share and exchange diverse opinions on the internet, creating a space where they can express personal viewpoints and experience various perspectives.

## 🔧 Environment

![image](https://github.com/RollCal/onion/assets/156996387/3fa6c01f-f80f-4a8d-9680-835b04a39983)

- Python: 3.11
- React: 18.3.1
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
