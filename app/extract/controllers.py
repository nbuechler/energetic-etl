from flask import Blueprint
from flask import render_template, redirect, url_for, jsonify

#databases
from config.databases import (mongo1,
                              mongo2,
                              mongo3,
                              affect_corpus,
                              affect_corpus_synopsis,
                              remoteDB1,
                              secure_graph1)

# mongo dependecies
from flask.ext.pymongo import ObjectId

# neo4j dependecies
from py2neo import Node, Relationship, Path

# bson
import json
from bson import json_util

# date
import datetime


'''
Helper functions - Get a new user node
Takes a user_id as a paramater
Returns a user_node (either a new one or a one that already exists)
'''
def get_user_node(user_id=None):

    cypher = secure_graph1.cypher

    user_cursor = mongo3.db.users.find({"_id": ObjectId(user_id)}) #find all activities
    json_user = json.dumps(user_cursor[0], default=json_util.default)

    # Create a new python dictionary from the json_user, we'll call it user_dict
    user_dict = json.loads(json_user)

    # Assumes either a record list of 1 or no records at all!
    user_node_list = cypher.execute("MATCH (user:User {user_id: '" + user_id + "'}) RETURN user")

    user_node=None
    if len(user_node_list) == 0:
        # Create a user node
        user_node = Node("User",
            email=user_dict.get('email'),
            user_id=user_dict.get('_id').get('$oid'),
            nodeType='user',
            )
    else:
        # Don't create a new user node it already exists
        user_node = user_node_list[0][0]

    return user_node

'''
Helper functions - Get an existing activity node
Takes an activity_id as a paramater
Returns a activity_node (either a new one or a one that already exists)
'''
def get_activity_node(activity_id=None):

    cypher = secure_graph1.cypher

    activity_cursor = mongo3.db.activities.find({"_id": ObjectId(activity_id)}) #find all activities
    json_activity = json.dumps(activity_cursor[0], default=json_util.default)

    # Create a new python dictionary from the json_activity, we'll call it activity_dict
    activity_dict = json.loads(json_activity)

    # Assumes either a record list of 1 or no records at all!
    activity_node_list = cypher.execute("MATCH (activity:Activity {activity_id: '" + activity_id + "'}) RETURN activity")

    # Define the activity node to return
    activity_node = activity_node_list[0][0]

    return activity_node

'''
Helper functions - Get an existing experience node
Takes an experience_id as a paramater
Returns a experience_node (either a new one or a one that already exists)
'''
def get_experience_node(experience_id=None):

    cypher = secure_graph1.cypher

    experience_cursor = mongo3.db.experiences.find({"_id": ObjectId(experience_id)}) #find all activities
    json_experience = json.dumps(experience_cursor[0], default=json_util.default)

    # Create a new python dictionary from the json_experience, we'll call it experience_dict
    experience_dict = json.loads(json_experience)

    # Assumes either a record list of 1 or no records at all!
    experience_node_list = cypher.execute("MATCH (experience:Experience {experience_id: '" + experience_id + "'}) RETURN experience")

    # Define the experience node to return
    experience_node = experience_node_list[0][0]

    return experience_node

'''
Helper functions - Get an existing log node
Takes an log_id as a paramater
Returns a log_node (either a new one or a one that already exists)
'''
def get_log_node(log_id=None):

    cypher = secure_graph1.cypher

    log_cursor = mongo3.db.logs.find({"_id": ObjectId(log_id)}) #find all activities
    json_log = json.dumps(log_cursor[0], default=json_util.default)

    # Create a new python dictionary from the json_log, we'll call it log_dict
    log_dict = json.loads(json_log)

    # Assumes either a record list of 1 or no records at all!
    log_node_list = cypher.execute("MATCH (log:Log {log_id: '" + log_id + "'}) RETURN log")

    # Define the log node to return
    log_node = log_node_list[0][0]

    return log_node



'''

Affect Extraction below

'''
# TODO: Refactor the below section, and maybe each of the above sections, into a seperate
# supporting area of the code for extract

'''
Get an order for an R-EMOTION
Takes two paramaters
1) the name of the emotion: emotion
2) the order number: order-num
Returns an order
'''
def get_rep_emotion_order(rEmotion=None, order_num=None):
    order = affect_corpus_synopsis.db['lingustic-affects'].find_one({'word': rEmotion})['order-' + str(order_num)]

    return {'status': 'success', 'result': order}

'''
Use this cypher query to get the [word object count,r_emotion object] pairs for a word
e.g. [2, satisfaction] - this means satisfication has the word emotion in two of its three orders
MATCH (n:rEmotion) -[r:SYNONYMIZED_BY]-(a:Word)
WHERE a.name = 'emotion'
RETURN count(DISTINCT(r)), n.name
'''
def get_word_count_for_rep_emotion(rEmotion=None, word=None):
    cypher = secure_graph1.cypher

    query = ''
    m = 'MATCH (n:rEmotion {name: "'+ rEmotion +'"}) -[r:SYNONYMIZED_BY]-(a:Word {name: "'+ word +'"})'
    w = 'WHERE a.name = "'+ word +'"'
    r = 'RETURN n,count(DISTINCT(r))'

    # Assembled query
    query = m + w + r

    query_result = cypher.execute(query)

    try:
        return {'status': 'success', 'rEmotion': rEmotion, 'word': word, 'count': query_result[0][1]}
    except Exception as e:
        pass
    return {'status': 'success', 'rEmotion': rEmotion, 'word': word, 'count': 0}

'''
Use this cypher query, for all r-emotions, to get the [word object count,r_emotion object] pairs for a word
e.g. [2, satisfaction] - this means satisfication has the word emotion in two of its three orders
MATCH (n:rEmotion) -[r:SYNONYMIZED_BY]-(a:Word)
WHERE a.name = 'emotion'
RETURN count(DISTINCT(r)), n.name
'''
def get_word_counts_across_corpora(word=None):
    cypher = secure_graph1.cypher

    query = ''
    m = 'MATCH (n:rEmotion) -[r:SYNONYMIZED_BY]-(a:Word {name: "'+ word +'"})'
    w = 'WHERE a.name = "'+ word +'"'
    r = 'RETURN n,count(DISTINCT(r))'

    # Assembled query
    query = m + w + r

    query_result = cypher.execute(query)

    print query_result

    return {'status': 'success', 'word': word, 'emotion-count': len(query_result)}



'''
This method compares two orders to find one common word in both orders.
MATCH (n:rEmotion {name: "joy"}) -[r:SYNONYMIZED_BY]-(a:Word {name: "emotion"})
WHERE (a.order = 1) OR (a.order = 2)
RETURN n,count(DISTINCT(r))
'''
def compare_two_orders_for_common_word(order_A=None, order_B=None, rEmotion=None, word=None):
    cypher = secure_graph1.cypher

    query = ''
    m = 'MATCH (n:rEmotion {name: "'+ rEmotion +'"}) -[r:SYNONYMIZED_BY]-(a:Word {name: "'+ word +'"})'
    w = 'WHERE (a.order = '+ str(order_A) +') OR (a.order = '+ str(order_B) + ')'
    r = 'RETURN n,count(DISTINCT(r))'

    # Assembled query
    query = m + w + r

    query_result = cypher.execute(query)

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

    return result

'''
This method compares all (three) orders to find one common word in all orders.
MATCH (n:rEmotion {name: "joy"}) -[r:SYNONYMIZED_BY]-(a:Word {name: "emotion"})
WHERE (a.order = 1) OR (a.order = 2) OR (a.order = 3)
RETURN n,count(DISTINCT(r))
'''
def compare_all_orders_for_common_word(rEmotion=None, word=None):
    cypher = secure_graph1.cypher

    query = ''
    m = 'MATCH (n:rEmotion {name: "'+ rEmotion +'"}) -[r:SYNONYMIZED_BY]-(a:Word {name: "'+ word +'"})'
    w = 'WHERE (a.order = 1) OR (a.order = 2) OR (a.order = 3)'
    r = 'RETURN n,count(DISTINCT(r))'

    # Assembled query
    query = m + w + r

    query_result = cypher.execute(query)

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

    return result

'''
This method compares two orders to find one common list of words in both orders.
'''
def compare_two_orders_for_common_word_list(order_A=None, order_B=None, rEmotion=None):
    o_A = get_rep_emotion_order(rEmotion=rEmotion, order_num=order_A)
    o_B = get_rep_emotion_order(rEmotion=rEmotion, order_num=order_B)

    all_words = o_A['result'] + o_B['result']

    result = []

    print '--Calculating similarities of words--'
    for word in set(all_words):
        if compare_two_orders_for_common_word(order_A=order_A, order_B=order_B, rEmotion=rEmotion, word=word) == 1:
            result.append(word)
    print '--Finished all words--'

    return {'status': 'success', 'result': result}

'''
This method compares all (three) orders to find one common list of words in all orders.
'''
def compare_all_orders_for_common_word_list(rEmotion=None):

    order_1 = get_rep_emotion_order(rEmotion=rEmotion, order_num=1)['result']
    order_2 = get_rep_emotion_order(rEmotion=rEmotion, order_num=2)['result']
    order_3 = get_rep_emotion_order(rEmotion=rEmotion, order_num=3)['result']

    all_words = order_1 + order_2 + order_3

    result = []

    print '--Calculating similarities of words--'
    for word in set(all_words):
        if compare_all_orders_for_common_word(rEmotion=rEmotion, word=word) == 1:
            result.append(word)
    print '--Finished all words--'

    return {'status': 'success', 'result': result}
