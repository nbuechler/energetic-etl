from flask import Blueprint
from flask import render_template, redirect, url_for, jsonify, request

import controllers

load = Blueprint('load', __name__)

@load.route('/')
def default():
    return 'Hello load!'
