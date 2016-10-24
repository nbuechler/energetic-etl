from flask import Blueprint
from flask import render_template, redirect, url_for, jsonify, request

import controllers

transform = Blueprint('transform', __name__)

@transform.route('/')
def default():
    return 'Hello transform!'

'''
rEmotion > string
--
Returns a an object:
status - success
n number of lists - various lists, probably 4 for now, which are the similar words in each order
'''
@transform.route('/emotion/<rEmotion>/similarity/')
def build_enhanced_rEmotion_similaritiy_object(rEmotion=None):

    result = controllers.build_enhanced_rEmotion_similaritiy_object(rEmotion=rEmotion)

    return jsonify(result)
