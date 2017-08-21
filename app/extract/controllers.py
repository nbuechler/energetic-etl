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

# mongo dependencies
from flask.ext.pymongo import ObjectId

# neo4j dependecies
from py2neo import Node, Relationship, Path

# bson
import json
from bson import json_util

# date
import datetime


# TODO: Store these in a database along with a description of their origin
'''
uses the entire synopsis of emotions in the corpora
'''
all_emotions = ['abandonment', 'abhorrence', 'abomination', 'absorption', 'abstinence', 'acceptance', 'admiration', 'adoration', 'affection', 'affectionateness', 'affliction', 'aggravation', 'aggressiveness', 'agony', 'alarm', 'alienation', 'aliveness', 'aloofness', 'alteration', 'amazement', 'ambiance', 'amusement', 'anger', 'angst', 'anguish', 'animation', 'anticipation', 'antipathy', 'anxiety', 'apathy', 'appraisal', 'appreciation', 'arousal', 'arrogance', 'assimilation', 'astonishment', 'attraction', 'audaciousness', 'aversion', 'avoidance', 'awareness', 'awe', 'awfulness', 'awkwardness', 'badness', 'bashfulness', 'belief', 'bewilderment', 'bitterness', 'blame', 'blessedness', 'boldness', 'boredom', 'bravery', 'brightness', 'calmness', 'capableness', 'cautiousness', 'certainty', 'chastity', 'cheerfulness', 'cleverness', 'closeness', 'cloudiness', 'coercion', 'coldness', 'compassion', 'composure', 'compromise', 'compulsion', 'concern', 'confidence', 'conformity', 'confusion', 'consciousness', 'consideration', 'consonance', 'contempt', 'content', 'contentment', 'contrariness', 'courage', 'courageousness', 'covetousness', 'criticalness', 'crossness', 'curiosity', 'darkness', 'decency', 'defeat', 'defiance', 'delight', 'denial', 'depression', 'desire', 'desolation', 'despair', 'despicableness', 'determination', 'devastation', 'devotion', 'diffidence', 'diligence', 'dimension', 'disappointment', 'disbelief', 'disdain', 'disgrace', 'disgust', 'disillusionment', 'dislike', 'dismay', 'disorientation', 'disrespect', 'dissonance', 'distance', 'distress', 'distrust', 'disturbance', 'dominance', 'doubt', 'doubtfulness', 'dread', 'dullness', 'eagerness', 'earnestness', 'easiness', 'ecstasy', 'edginess', 'ego', 'elation', 'embarrassment', 'empathy', 'emptiness', 'encouragement', 'endurance', 'engagement', 'engrossment', 'enjoyment', 'enlightenment', 'enragement', 'enthusiasm', 'envy', 'eroticism', 'euphoria', 'exasperation', 'excitation', 'excitement', 'exhaustion', 'exploitation', 'exuberance', 'familiarity', 'fascination', 'fate', 'fatigue', 'fear', 'festivity', 'flatness', 'fondness', 'foolishness', 'forgiveness', 'fortune', 'freedom', 'fright', 'friskiness', 'frustration', 'fulfillment', 'furiousness', 'fury', 'gallantry', 'gayness', 'glee', 'gloominess', 'gluttony', 'goodness', 'grace', 'gratification', 'gratitude', 'greatness', 'greed', 'grief', 'guilt', 'happiness', 'hardiness', 'harmony', 'hate', 'helplessness', 'hesitance', 'hesitancy', 'honor', 'hope', 'hopefulness', 'horror', 'hostility', 'hotness', 'humbleness', 'humiliation', 'humility', 'hurt', 'ignorance', 'importance', 'impulse', 'impulsiveness', 'inadequacy', 'inadequateness', 'incapableness', 'indifference', 'inducement', 'indulgence', 'infatuation', 'infection', 'inferiority', 'inflammation', 'infuriation', 'innocence', 'inquisitiveness', 'insecurity', 'insignificance', 'inspiration', 'insult', 'intensity', 'intentness', 'interest', 'intimacy', 'intrigue', 'invulnerability', 'irritation', 'isolation', 'jealousy', 'joy', 'jubilance', 'keenness', 'kindness', 'liberality', 'liberation', 'lifelessness', 'liveliness', 'lividness', 'loathing', 'loneliness', 'loss', 'lousiness', 'love', 'luck', 'luckiness', 'lunacy', 'lust', 'mania', 'melancholy', 'merriness', 'misery', 'modesty', 'motivation', 'mournfulness', 'negation', 'negativeness', 'neglect', 'nervousness', 'neutrality', 'nonchalance', 'nostalgia', 'numbness', 'obsession', 'offensiveness', 'openness', 'optimism', 'outrage', 'pain', 'panic', 'paralysis', 'passion', 'passionateness', 'patience', 'peacefulness', 'permanence', 'perplexity', 'persuasion', 'perturbation', 'pessimism', 'petrification', 'pity', 'playfulness', 'pleasantness', 'pleasure', 'positiveness', 'potency', 'power', 'powerfulness', 'powerlessness', 'preoccupation', 'pride', 'provocation', 'quietness', 'quirkiness', 'rage', 'reassurance', 'rebellion', 'rebelliousness', 'reception', 'receptiveness', 'reenforcement', 'regret', 'reinforcement', 'rejection', 'relaxation', 'reliability', 'relief', 'reluctance', 'remorse', 'reproach', 'resentment', 'reservation', 'resignation', 'resistance', 'respect', 'restlessness', 'revulsion', 'ridicule', 'sadness', 'safety', 'saltiness', 'sarcasm', 'satisfaction', 'scorn', 'sensitivity', 'serenity', 'seriousness', 'shakiness', 'shame', 'shock', 'shyness', 'skepticism', 'sloth', 'snoopiness', 'sobriety', 'sourness', 'spirit', 'spiritedness', 'spite', 'stolidity', 'straightness', 'strength', 'stress', 'stubbornness', 'stupidity', 'submission', 'subversion', 'sulkiness', 'sulky', 'sullenness', 'sunniness', 'sureness', 'surprise', 'suspicion', 'sweetness', 'sympathy', 'tearfulness', 'tenaciousness', 'tenacity', 'tenderness', 'tenseness', 'terribleness', 'terror', 'thoughtfulness', 'threat', 'thrill', 'tolerance', 'tragedy', 'triumph', 'trust', 'uncertainty', 'understanding', 'uneasiness', 'unhappiness', 'unification', 'uniqueness', 'unity', 'unpleasantness', 'unpredictability', 'uselessness', 'valence', 'validation', 'vanity', 'veneration', 'vengefulness', 'victimization', 'vigor', 'vileness', 'vulnerability', 'warmness', 'weariness', 'withdrawal', 'withdrawnness', 'woe', 'woefulness', 'wonder', 'wonderfulness', 'worry', 'worthlessness', 'wrath']


'''
Utility functions
'''

def convert_unicode_list(unicode_list):
    string_list = []
    for x in unicode_list:
        string_list.append(str(x))

    return string_list

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

def get_rEmotion_flat_corpora(rEmotion=None):

    order_1 = get_rep_emotion_order(rEmotion=rEmotion, order_num=1)
    order_2 = get_rep_emotion_order(rEmotion=rEmotion, order_num=2)
    order_3 = get_rep_emotion_order(rEmotion=rEmotion, order_num=3)


    rEmotion_flat_list = (order_1['result']) + (order_2['result']) + (order_3['result'])
    unq_rEmotion_flat_list = list(set(rEmotion_flat_list))

    result = {"status": 'success', 'rEmotion': rEmotion, 'rEmotion-words': unq_rEmotion_flat_list, 'rEmotion-word-length': len(unq_rEmotion_flat_list)}

    return result

def get_all_rep_emotion_flat_corpora():

    all_rEmotion_flat_list = []

    for rEmotion in all_emotions:
        r = get_rEmotion_flat_corpora(rEmotion=rEmotion)
        all_rEmotion_flat_list = all_rEmotion_flat_list + (r['rEmotion-words'])
        print 'Completed: ' + rEmotion

    unq_all_rEmotion_flat_list = list(set(all_rEmotion_flat_list))

    result = {"status": 'success', 'corpora_words': unq_all_rEmotion_flat_list, 'rEmotion-word-length': len(unq_all_rEmotion_flat_list)}

    return result


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

'''
This method finds the affect/orders for all given words
MATCH (n:rEmotion) -[r:SYNONYMIZED_BY]-(a:Word)
WHERE a.name = 'emotion'
RETURN n.name + ' ' + a.order
===
Note: Due to time constraints, I didn't make the simpler find_all_affect_orders_for_a_single_given_word
Note: compare_all_orders_for_common_word_list is similar to what would be find_single_affect_order_for_a_all_given_words
'''
def find_all_affect_orders_for_all_given_words():

    word_list_result = get_all_rep_emotion_flat_corpora()

    lists_of_word_affect_order_objects = []
    word_count = 0
    for word in word_list_result['corpora_words'][0:10]:
        word_count += 1
        list_of_rEmotion_orders = []
        cypher = secure_graph1.cypher

        query = ''
        m = 'MATCH (n:rEmotion) -[r:SYNONYMIZED_BY]-(a:Word)'
        w = 'WHERE a.name = "'+ word +'"'
        r = 'RETURN n.name + " " + a.order'

        # Assembled query
        query = m + w + r

        query_result = cypher.execute(query)
        # print query_result
        # TODO: Use the python logging library instead of print statements.
        print 'Finished: =====' + word + '====='
        if word_count % 50 == 0:
            print 'Completed - ' + str(word_count)

        for i in query_result:
            list_of_rEmotion_orders += i
        affect_order_word_object = {
            "word": word,
            "list_of_rEmotion_orders": list_of_rEmotion_orders,
        }
        lists_of_word_affect_order_objects.append(affect_order_word_object)

    return {
        'status': 'success',
        'result': lists_of_word_affect_order_objects,
        'length_of_affect_order_objects_list': len(lists_of_word_affect_order_objects),
        }

'''
This method finds the affect/orders for all given words
MATCH (n:rEmotion) RETURN n.name, n.order1Length, n.order2Length, n.order3Length
===
Note: I don't get order intersections.
'''
def find_all_order_lengths_for_all_given_affects():
    cypher = secure_graph1.cypher

    query = ''
    m = 'MATCH (n:rEmotion) RETURN n.name, n.order1Length, n.order2Length, n.order3Length'
    w = ''
    r = ''

    # Assembled query
    query = m + w + r

    query_result = cypher.execute(query)

    lists_of_word_affect_length_key_values = {}
    for item in query_result:
        lists_of_word_affect_length_key_values[item[0] + ' 1'] = item[1]
        lists_of_word_affect_length_key_values[item[0] + ' 2'] = item[2]
        lists_of_word_affect_length_key_values[item[0] + ' 3'] = item[3]

    return {
        'status': 'success',
        'result': lists_of_word_affect_length_key_values,
        }
