# energetic-etl
A project for etl processes within Logro. Logro is the working name, or public facing name, for a project that binds together many other repositories.

# Overview
Building microservices is an important aspect of Logro. This project enacts a plan to add another application to that microservice set. energetic-etl acts as a natrual language processing engine, which performs ETL operations. Some code for making use of multiple databases is handy. This project is a service component for other projects that use its NLP toolset. Ultimately, in 2016, it takes slack off from 'hungry-interceptor' (GPLv3) and 'speedy-affect-scorer' (MIT) 

# History
The project originally was part of 'hungry-interceptor' (GPLv3) where the intercepts directory contained some of the logic this project used as boilerplate. See the other project called: hungry-interceptor

Find the project here: https://github.com/nbuechler/hungry-interceptor

# Description
Its primary function is running extract-transform-load mechanisms, of which, are used to access/load data into both MongoDB and Neo4j. This scope may expand in the future (2016).

# Getting Started
* First, install virtualenv if not done so already -- https://virtualenv.pypa.io/en/latest/installation.html(https://virtualenv.pypa.io/en/latest/installation.html)
* Then, run this command: $ virtualenv venv
* (make sure you get the'.'): $ . venv/bin/activate
* pip install -r requirements.txt

# Start databases - if they are not already running
_From a terminal, start mongo:_
'''
mongod
'''

_From a terminal start Neo4j:_
'''
sudo /etc/init.d/neo4j-service start
'''

# Run the application
'''
python app/runserver.py 5000 
'''
This contains a port - 5000 - for running local, otherwise it will try to run on the default port - 80 - and that's taken. If you run it on a server instance, such as one on AWS without the port specified, it should running open to the world. That is the usual configuration for deploying code and making it 'live' to the world. But, make sure you are prudent in running the code in the way you want it to run. 

# Scripts folder
The scripts folder is for automation. If using AWS, here's a problem I encountered in the middle of Feb, 2016:
_DO NOT UPGRADE PIP_ from 6.1.1 on a standard AWS EC2 instance, or it will bite you. I don't really know why so this might have changed when you are reading this.

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

# Things to do
* Refactor: (Bonus points if there is a command line interface -- like click pip module)
* Plan: Figure out where to store machine learning results: i.e. what kind of database?
* Refactor: Remove old code from 'hungry-interceptor' when this is complete!
* Chore: Check the config files for accuracy
* Chore: Check the Travis files for accuracy
* Chore: Check the appspec files for accuracy
* DONE: Make the 'intercepts' into specific 'extract', 'transform', and 'load' directories
* DONE: Be sure to include views!!
* DONE: Include code for making the ETL work for 'speedy-affect-scorer'

# Fun Facts
* As of 2016.Oct.15 -> On my machine, http://<root>/load/rEmotion_corpus/all took <b><i>7336244ms</i></b> or 2 hr. 2 min. 16 sec. 244 ms where 1 hr. = 3600000 ms
* Other research begins to support the idea of an I-EMOTION: http://nymag.com/scienceofus/2016/10/this-personality-trait-makes-it-hard-to-understand-symptoms.html?mid=facebook_scienceofus


# CORS and dealing with it
Make sure to pay attention to how CORS right now accepts everything.

See more here: https://flask-cors.readthedocs.org/en/latest/
'''
from flask.ext.cors import CORS
cors = CORS(app, resources={r"/\*": {"origins": "\*"}}) #CORS :WARNING everything!
'''

# LICENSE
GPLv3
