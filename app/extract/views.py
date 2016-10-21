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

'''
rEmotion > string
order_A > number
order_B > number
word > string
--
Returns 1 if word exists in both order_A and order_B
Returns 0 if word does NOT exist in both order_A and order_B
'''
@extract.route('/emotion/<rEmotion>/order/<order_A>,<order_B>/<word>')
def check_similarity_for_rep_emotion(rEmotion=None, order_A=None, order_B=None, word=None):
    query_result = controllers.check_similarity_for_rep_emotion(order_A=order_A, order_B=order_B, rEmotion=rEmotion, word=word)

    result = 0
    try:
        word_total = query_result[0][1]
        if word_total == 1:
            result = 0
        elif word_total == 2:
            result = 1
    except Exception as e:
        # TODO: Write the exception of index out of bounds for: query_result[0][1]
        # to a log file
        print 'Word does not exist in either order'
        pass

    return str(result)

'''
rEmotion > string
word > string
--
Returns 1 if word exists in both order_A and order_B
Returns 0 if word does NOT exist in both order_A and order_B
'''
@extract.route('/emotion/<rEmotion>/order/all/<word>')
def check_o1_o2_o3_similarity_for_rep_emotion(rEmotion=None, word=None):
    query_result = controllers.check_o1_o2_o3_similarity_for_rep_emotion(rEmotion=rEmotion, word=word)

    result = 0
    try:
        word_total = query_result[0][1]
        if word_total == 3:
            result = 1
        elif word_total == 2 or word_total == 1:
            result = 0
    except Exception as e:
        # TODO: Write the exception of index out of bounds for: query_result[0][1]
        # to a log file
        print 'Word does not exist in any order'
        pass

    return str(result)
