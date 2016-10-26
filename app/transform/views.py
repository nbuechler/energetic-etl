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

'''
--
Returns a frequency distribution for every word in the entire corpora
'''
@transform.route('/emotion/all/similarity/all')
def get_frequency_distribution_across_corpora():

    result = controllers.get_frequency_distribution_across_corpora()

    return result
