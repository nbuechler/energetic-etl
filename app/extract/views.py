from flask import Blueprint
from flask import render_template, redirect, url_for, jsonify, request

import controllers

extract = Blueprint('extract', __name__)

@extract.route('/')
def default():
    return 'Hello extract!'

@extract.route('/nodes/users/<user_id>')
def get_user_node(user_id=None):
    return jsonify(dict(controllers.get_user_node(user_id=user_id).properties))

@extract.route('/nodes/activities/<activity_id>')
def get_activity_node(activity_id=None):
    return jsonify(dict(controllers.get_activity_node(activity_id=activity_id).properties))

@extract.route('/nodes/experiences/<experience_id>')
def get_experience_node(experience_id=None):
    return jsonify(dict(controllers.get_experience_node(experience_id=experience_id).properties))

@extract.route('/nodes/logs/<log_id>')
def get_log_node(log_id=None):
    return jsonify(dict(controllers.get_log_node(log_id=log_id).properties))
