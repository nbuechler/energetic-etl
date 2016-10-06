from flask import Blueprint
from flask import render_template, redirect, url_for, jsonify, request

import controllers

transform = Blueprint('transform', __name__)

@transform.route('/')
def default():
    return 'Hello transform!'
