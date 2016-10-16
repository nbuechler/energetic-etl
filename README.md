# energetic-etl
A project for etl processes within logro

## Overview
In enacting a plan to add another application that acts as a natrual language processing engine. Some code for making use of multiple databases is handy. This project is a service component for that project and it is also meant to take off some of the slack from 'hungry-interceptor'

## History
The project originally was part of 'hungry-interceptor' (GPLv3) where intercepts was the main directory for this logic. See the other project called: hungry-interceptor

Find the project here: https://github.com/nbuechler/hungry-interceptor

## Description

Its primary function is running extract-transform-load mechanisms

# Steps
* first, install virtualenv if not done so already -- https://virtualenv.pypa.io/en/latest/installation.html(https://virtualenv.pypa.io/en/latest/installation.html)
* then, run this command: $ virtualenv venv
* (make sure you get the'.'): $ . venv/bin/activate
* pip install -r requirements.txt

#Start databases
Start mongo:: mongod
Start Neo4j:: sudo /etc/init.d/neo4j-service start


#Run the application
python app/runserver.py 5000 [For local, otherwise it will try to run on 80 and thats taken ;)]


# Things to do
* Refactor: Make the 'intercepts' into specific 'extract', 'transform', and 'load' directories
* Refactor: Be sure to include views!!
* Refactor: (Bonus points if there is a command line interface -- like click pip module)
* Feature: Include code for making the ETL work for 'speedy-affect-scorer'
* Plan: Figure out where to store machine learning results: i.e. what kind of database?
* Refactor: Remove old code from 'hungry-interceptor' when this is complete!
* Chore: Check the config files for accuracy
* Chore: Check the Travis files for accuracy
* Chore: Check the appspec files for accuracy


#Scripts folder
The scripts folder is for automation
If using aws, I encountered problems the 2nd week of Feb, 2016. DO NOT, FOR THE SAKE OF SANITY, UPGRADE PIP from 6.1.1 OR AWS EC2 will bite you.

# Requirements

* Flask==0.10.1
* Flask-Cors==2.1.0
* Flask-PyMongo==0.3.1
* Flask-WTF==0.11
* itsdangerous==0.24
* Jinja2==2.8
* MarkupSafe==0.23
* py2neo==2.0.8
* pymongo==2.8.1
* six==1.10.0
* Werkzeug==0.11.3
* wheel==0.24.0
* WTForms==2.0.2

-->https://flask-cors.readthedocs.org/en/latest/

# Fun Facts
* As of 2016.Oct.15, http://<root>/load/rEmotion_corpus/all took <b><i>7336244ms</i></b> or 2 hr. 2 min. 16 sec. 244 ms where 1 hr. = 3600000 ms


#CORS
from flask.ext.cors import CORS

cors = CORS(app, resources={r"/*": {"origins": "*"}}) #CORS :WARNING everything!
