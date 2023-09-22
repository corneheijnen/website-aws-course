#!/bin/bash
sudo apt-get update
sudo apt install python3-pip
sudo apt install python3-flask
sudo apt install python3-waitress
git clone https://github.com/corneheijnen/website-aws-course.git
cd website-aws-course
pip install -e .
pip install flask==2.2.5
pip install SQLAlchemy
pip install pymysql
flask --app flaskr init-db
waitress-serve --call 'flaskr:create_app'