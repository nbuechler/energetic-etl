from flask import Blueprint
from flask import render_template, redirect, url_for, jsonify

#databases
from config.databases import mongo1, mongo2, mongo3, remoteDB1, secure_graph1

# mongo dependecies
from flask.ext.pymongo import ObjectId

# neo4j dependecies
from py2neo import Node, Relationship, Path

# bson
import json
from bson import json_util

# date
import datetime


'''
Helper functions - Get a new user node
Takes a user_id as a paramater
Returns a user_node (either a new one or a one that already exists)
'''
def get_user_node(user_id=None):

    cypher = secure_graph1.cypher

    user_cursor = mongo3.db.users.find({"_id": ObjectId(user_id)}) #find all activities
    json_user = json.dumps(user_cursor[0], default=json_util.default)

    # Create a new python dictionary from the json_user, we'll call it user_dict
    user_dict = json.loads(json_user)

    # Assumes either a record list of 1 or no records at all!
    user_node_list = cypher.execute("MATCH (user:User {user_id: '" + user_id + "'}) RETURN user")

    user_node=None
    if len(user_node_list) == 0:
        # Create a user node
        user_node = Node("User",
            email=user_dict.get('email'),
            user_id=user_dict.get('_id').get('$oid'),
            nodeType='user',
            )
    else:
        # Don't create a new user node it already exists
        user_node = user_node_list[0][0]

    return user_node

'''
Helper functions - Get an existing activity node
Takes an activity_id as a paramater
Returns a activity_node (either a new one or a one that already exists)
'''
def get_activity_node(activity_id=None):

    cypher = secure_graph1.cypher

    activity_cursor = mongo3.db.activities.find({"_id": ObjectId(activity_id)}) #find all activities
    json_activity = json.dumps(activity_cursor[0], default=json_util.default)

    # Create a new python dictionary from the json_activity, we'll call it activity_dict
    activity_dict = json.loads(json_activity)

    # Assumes either a record list of 1 or no records at all!
    activity_node_list = cypher.execute("MATCH (activity:Activity {activity_id: '" + activity_id + "'}) RETURN activity")

    # Define the activity node to return
    activity_node = activity_node_list[0][0]

    return activity_node

'''
Helper functions - Get an existing experience node
Takes an experience_id as a paramater
Returns a experience_node (either a new one or a one that already exists)
'''
def get_experience_node(experience_id=None):

    cypher = secure_graph1.cypher

    experience_cursor = mongo3.db.experiences.find({"_id": ObjectId(experience_id)}) #find all activities
    json_experience = json.dumps(experience_cursor[0], default=json_util.default)

    # Create a new python dictionary from the json_experience, we'll call it experience_dict
    experience_dict = json.loads(json_experience)

    # Assumes either a record list of 1 or no records at all!
    experience_node_list = cypher.execute("MATCH (experience:Experience {experience_id: '" + experience_id + "'}) RETURN experience")

    # Define the experience node to return
    experience_node = experience_node_list[0][0]

    return experience_node

'''
Helper functions - Get an existing log node
Takes an log_id as a paramater
Returns a log_node (either a new one or a one that already exists)
'''
def get_log_node(log_id=None):

    cypher = secure_graph1.cypher

    log_cursor = mongo3.db.logs.find({"_id": ObjectId(log_id)}) #find all activities
    json_log = json.dumps(log_cursor[0], default=json_util.default)

    # Create a new python dictionary from the json_log, we'll call it log_dict
    log_dict = json.loads(json_log)

    # Assumes either a record list of 1 or no records at all!
    log_node_list = cypher.execute("MATCH (log:Log {log_id: '" + log_id + "'}) RETURN log")

    # Define the log node to return
    log_node = log_node_list[0][0]

    return log_node
