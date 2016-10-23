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
@extract.route('/emotion/<rEmotion>/order/<order_A>,<order_B>/similarity/<word>')
def compare_two_orders_for_common_word(rEmotion=None, order_A=None, order_B=None, word=None):
    result = controllers.compare_two_orders_for_common_word(order_A=order_A, order_B=order_B, rEmotion=rEmotion, word=word)

    return str(result)

'''
rEmotion > string
word > string
--
Returns 1 if word exists in both order_A and order_B
Returns 0 if word does NOT exist in both order_A and order_B
'''
@extract.route('/emotion/<rEmotion>/order/all/similarity/<word>')
def compare_all_orders_for_common_word(rEmotion=None, word=None):
    result = controllers.compare_all_orders_for_common_word(rEmotion=rEmotion, word=word)

    return str(result)


@extract.route('/emotion/<rEmotion>/order/<order_A>,<order_B>/similarity/all')
def compare_two_orders_for_common_word_list(rEmotion=None, order_A=None, order_B=None, word_list=None):
    result = controllers.compare_two_orders_for_common_word_list(rEmotion=None, order_A=None, order_B=None, word_list=None)

    return result

@extract.route('/emotion/<rEmotion>/order/all/similarity/all')
def compare_all_orders_for_common_word_list(rEmotion=None, word_list=None):
    result = controllers.compare_all_orders_for_common_word_list(rEmotion=None, word_list=None)

    return result
