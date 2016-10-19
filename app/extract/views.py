from flask import Blueprint
from flask import render_template, redirect, url_for, jsonify, request

import controllers

extract = Blueprint('extract', __name__)

@extract.route('/')
def default():
    return 'Hello extract!'

'''
User, Activity, Experience, Log
'''
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

'''
Emotion
'''
# TODO: Think about extending this out
# (remember that transforming the response happens in the transforming area of the code)
@extract.route('/emotion/<rEmotion>/order/<order_num>')
def get_rep_emotion_order(rEmotion=None, order_num=None):
    return jsonify(controllers.get_rep_emotion_order(rEmotion=rEmotion, order_num=order_num))

@extract.route('/emotion/<rEmotion>/order/all')
def get_rep_emotion_all(rEmotion=None, order_num=None):
    order_1 = controllers.get_rep_emotion_order(rEmotion=rEmotion, order_num=1)['result']
    order_2 = controllers.get_rep_emotion_order(rEmotion=rEmotion, order_num=2)['result']
    order_3 = controllers.get_rep_emotion_order(rEmotion=rEmotion, order_num=3)['result']
    return jsonify(
            {
            'rEmotion': rEmotion,
            'status': 'success',
            'order_1': order_1,
            'order_2': order_2,
            'order_3': order_3,
            }
        )


'''
Affect-Word Similarty
'''

# TODO: Think about a better developer experience for an api!
@extract.route('/emotion/<rEmotion>/comparison/<order_A>/with/<order_B>/for/<word>')
def check_similarity_for_rep_emotion(rEmotion=None, order_A=None, order_B=None, word=None):
    result = controllers.check_similarity_for_rep_emotion(order_A=order_A, order_B=order_B, rEmotion=rEmotion, word=word)
    print result
    return 'Barely Implemented'

@extract.route('/emotion/<rEmotion>/comparison/allfor/<word>')
def check_o1_o2_o3_similarity_for_rep_emotion(rEmotion=None, word=None):
    result = controllers.check_o1_o2_o3_similarity_for_rep_emotion(rEmotion=rEmotion, word=word)
    print result
    return 'Not implemented'
