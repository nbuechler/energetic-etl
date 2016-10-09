from flask import Blueprint
from flask import render_template, redirect, url_for, jsonify, request

import controllers

extract = Blueprint('extract', __name__)

@extract.route('/')
def default():
    return 'Hello extract!'

@extract.route('/nodes/user/<user_id>')
def get_user_node(user_id=None):
    return get_user_node(user_id=None)

@extract.route('/nodes/activity/<activity_id>')
def get_activity_node(activity_id=None):
    return get_activity_node(activity_id=None)

@extract.route('/nodes/experience/<experience_id>')
def get_experience_node(experience_id=None):
    return get_experience_node(experience_id=None)

@extract.route('/nodes/log/<log_id>')
def get_log_node(log_id=None):
    return get_log_node(log_id=None)
