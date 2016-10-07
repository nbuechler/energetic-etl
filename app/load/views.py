from flask import Blueprint
from flask import render_template, redirect, url_for, jsonify, request

import controllers

load = Blueprint('load', __name__)

@load.route('/')
def default():
    return 'Hello load!'

'''
Activities
'''
@load.route('/mongo2neo/create_single_activity/<activity>', methods=['POST'])
def create_single_activity(activity=None):
    return controllers.create_single_activity(activity=None)

@load.route('/mongo2neo/update_single_activity/<activity>', methods=['PUT'])
def update_single_activity(activity=None):
    return controllers.update_single_activity(activity=None)

@load.route('/mongo2neo/destroy_single_activity/<activity>', methods=['DELETE'])
def destroy_single_activity(activity=None):
    return controllers.destroy_single_activity(activity=None)

'''
Experiences
'''
@load.route('/mongo2neo/create_single_experience/<experience>', methods=['POST'])
def create_single_experience(experience=None):
    return controllers.create_single_experience(experience=None)

@load.route('/mongo2neo/update_single_experience/<experience>', methods=['PUT'])
def update_single_experience(experience=None):
    return controllers.update_single_experience(experience=None)

@load.route('/mongo2neo/destroy_single_experience/<experience>', methods=['DELETE'])
def destroy_single_experience(experience=None):
    return controllers.destroy_single_experience(experience=None)

'''
Logs
'''
@load.route('/mongo2neo/create_single_log/<log>', methods=['POST'])
def create_single_log(log=None):
    return controllers.create_single_log(log=None)

@load.route('/mongo2neo/update_single_log/<log>', methods=['PUT'])
def update_single_log(log=None):
    return controllers.update_single_log(log=None)

@load.route('/mongo2neo/destroy_single_log/<log>', methods=['DELETE'])
def destroy_single_log(log=None):
    return controllers.destroy_single_log(log=None)

'''
General Record Keeping
'''
@load.route('/mongo2neo/delete_records')
def delete_records():
    return controllers.delete_records()

@load.route('/mongo2neo/create_records')
def create_records():
    return controllers.create_records()

@load.route('/mongo2neo/create_event_supplement')
def create_event_supplement():
    # TODO: Make this method execute differently if there is a user_id
    # For example, if a user_id, make it so that user has updated event nodes
    # All distinct events for each give user
    return controllers.create_event_supplement()
