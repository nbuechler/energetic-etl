from flask import Blueprint
from flask import render_template, redirect, url_for, jsonify, request

import controllers

load = Blueprint('load', __name__)

@load.route('/')
def default():
    return 'Hello load!'

'''
Activities
'''
@load.route('/activity/<activity>', methods=['POST'])
def create_activity(activity=None):
    return controllers.create_single_activity(activity=activity)

@load.route('/activity/<activity>', methods=['PUT'])
def update_activity(activity=None):
    return controllers.update_single_activity(activity=activity)

@load.route('/activity/<activity>', methods=['DELETE'])
def destroy_activity(activity=None):
    print 'here'
    return controllers.destroy_single_activity(activity=activity)

'''
Experiences
'''
@load.route('/experience/<experience>', methods=['POST'])
def create_experience(experience=None):
    return controllers.create_single_experience(experience=experience)

@load.route('/experience/<experience>', methods=['PUT'])
def update_experience(experience=None):
    return controllers.update_single_experience(experience=experience)

@load.route('/experience/<experience>', methods=['DELETE'])
def destroy_experience(experience=None):
    return controllers.destroy_single_experience(experience=experience)

'''
Logs
'''
@load.route('/log/<log>', methods=['POST'])
def create_log(log=None):
    return controllers.create_single_log(log=log)

@load.route('/log/<log>', methods=['PUT'])
def update_log(log=None):
    return controllers.update_single_log(log=log)

@load.route('/log/<log>', methods=['DELETE'])
def destroy_log(log=None):
    return controllers.destroy_single_log(log=log)


'''
Emotion
'''
# This loads the corpus data from mongo to neo4j
@load.route('/rEmotion_corpus/<rEmotion>', methods=['POST'])
def create_rEmotion_corpus(rEmotion=None):
    return controllers.create_single_rEmotion_corpus(rEmotion=rEmotion)

# This loads the corpus data from mongo to neo4j
@load.route('/rEmotion_corpus/all', methods=['POST'])
def create_all_rEmotion_corpora():
    return controllers.create_all_rEmotion_corpora()


'''
Affect-Word Similarty
'''

@load.route('/rEmotion_corpus/order_similarity/<mongo_db_name>', methods=['POST'])
def create_enhanced_rEmotion_corpora(mongo_db_name=None):
    return controllers.create_enhanced_rEmotion_corpora(mongo_db_name=mongo_db_name)

# This loads the graph operated data from neo4j to MongoDB
@load.route('/rEmotion_corpus/frequency_dist/<mongo_db_name>', methods=['POST'])
def create_affect_word_frequency_distribution(mongo_db_name=None):
    return controllers.create_affect_word_frequency_distribution(mongo_db_name=mongo_db_name)



'''
General Record Keeping
'''
@load.route('/delete_records')
def delete_records():
    return controllers.delete_records()

@load.route('/create_records')
def create_records():
    return controllers.create_records()

@load.route('/create_event_supplement')
def create_event_supplement():
    # TODO: Make this method execute differently if there is a user_id
    # For example, if a user_id, make it so that user has updated event nodes
    # All distinct events for each give user
    return controllers.create_event_supplement()
