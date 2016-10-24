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

from extract.controllers import (get_user_node,
                                   get_activity_node,
                                   get_experience_node,
                                   get_log_node,
                                   compare_two_orders_for_common_word_list,
                                   compare_all_orders_for_common_word_list,)

'''
Helper functions - Create new User/Activity Relationship
cnr --> create new relationship
Takes a user node and activity dict as paramaters
Returns a new_activity_node
'''
def cnr_user_did_activity(new_user_node=None, activity_dict=None):

    # Create a new activity node
    new_activity_node = Node("Activity",
        name=activity_dict.get('name'),
        activity_id=activity_dict.get('_id').get('$oid'),
        privacy=activity_dict.get('privacy'),
        archived=activity_dict.get('archived'),
        word_length=activity_dict.get('descriptionArrayLength'),
        nodeType='activity',
        )

    for word in activity_dict.get('descriptionArray'):
        new_word_node = Node("Word", name=word, characters=len(word), nodeType='word',)
        activity_has_word = Relationship(new_activity_node, "HAS", new_word_node)
        secure_graph1.create(activity_has_word)
        user_spoke_word = Relationship(new_user_node, "SPOKE", new_word_node)
        secure_graph1.create(user_spoke_word)

    user_did_activity = Relationship(new_user_node, "DID", new_activity_node)
    secure_graph1.create(user_did_activity)

    return new_activity_node

'''
Helper functions - update Activity, and deletes and recreates words/relationships
update activty node
Takes a user node and activity dict as paramaters
Returns a new_activity_node
'''
def update_activity_node(new_user_node=None, activity_dict=None):

    '''
    To get the activity and change the node
    MATCH (n { activity_id: '56edf2da6b43ff691627efd8' }) SET n.name = 'Sleeping' RETURN n

    To get the activty and all of its word nodes
    MATCH (n { activity_id: '56edf2da6b43ff691627efd8' })-[r:HAS]-(w) RETURN n,w

    To delete the word nodes of an activty
    MATCH (n { activity_id: '56edf2da6b43ff691627efd8' })-[r:HAS]-(w) DETACH DELETE w
    '''

    cypher = secure_graph1.cypher

    _match = 'MATCH (n { activity_id: "' + activity_dict.get('_id').get('$oid') + '" })'
    _set = ' SET n.name="' + activity_dict.get('name') + '"'
    _set += ' SET n.privacy="' + str(activity_dict.get('privacy')) + '"'
    _set += ' SET n.archived="' + str(activity_dict.get('archived')) + '"'
    _set += ' SET n.word_length="' + str(activity_dict.get('descriptionArrayLength')) + '"'
    _return = ' RETURN n'

    # This the query that updates the node
    cypher.execute(_match + _set + _return)

    # Get the updated activity node
    updated_activity_node = get_activity_node(activity_dict.get('_id').get('$oid'))

    # Detach all the relationships and delete all the words associated with the activity
    cypher.execute('MATCH (n { activity_id: "' + activity_dict.get('_id').get('$oid') + '" })-[r:HAS]-(w) DETACH DELETE w')

    for word in activity_dict.get('descriptionArray'):
        new_word_node = Node("Word", name=word, characters=len(word), nodeType='word',)
        activity_has_word = Relationship(updated_activity_node, "HAS", new_word_node)
        secure_graph1.create(activity_has_word)
        user_spoke_word = Relationship(new_user_node, "SPOKE", new_word_node)
        secure_graph1.create(user_spoke_word)

    return updated_activity_node

'''
Helper functions - Create new User/Experience Relationship
cnr --> create new relationship
Takes a user node and experience dict as paramaters
Returns a new_activity_node
'''
def cnr_user_experienced_experience(new_user_node=None, experience_dict=None):

    # Create a new experience node
    new_experience_node = Node("Experience",
        name=experience_dict.get('name'),
        experience_id=experience_dict.get('_id').get('$oid'),
        privacy=experience_dict.get('privacy'),
        archived=experience_dict.get('archived'),
        pronoun=experience_dict.get('pronoun'),
        word_length=experience_dict.get('descriptionArrayLength'),
        nodeType='experience',
        )

    for word in experience_dict.get('descriptionArray'):
        new_word_node = Node("Word", name=word, characters=len(word), nodeType='word',)
        experience_has_word = Relationship(new_experience_node, "HAS", new_word_node)
        secure_graph1.create(experience_has_word)
        user_spoke_word = Relationship(new_user_node, "SPOKE", new_word_node)
        secure_graph1.create(user_spoke_word)

    user_experienced_experience = Relationship(new_user_node, "EXPERIENCED", new_experience_node)
    secure_graph1.create(user_experienced_experience)

    return new_experience_node

'''
Helper functions - update Experience, and deletes and recreates words/relationships
update experience node
Takes a user node and experience dict as paramaters
Returns a new_experience_node
'''
def update_experience_node(new_user_node=None, experience_dict=None):

    '''
    To get the experience and change the node
    MATCH (n { experience_id: '56ea1cf43a34fc7711ae330e' }) SET n.name = 'Sleeping' RETURN n

    To get the activty and all of its word nodes
    MATCH (n { experience_id: '56ea1cf43a34fc7711ae330e' })-[r:HAS]-(w) RETURN n,w

    To delete the word nodes of an experience
    MATCH (n { experience_id: '56ea1cf43a34fc7711ae330e' })-[r:HAS]-(w) DETACH DELETE w
    '''
    cypher = secure_graph1.cypher

    _match = 'MATCH (n { experience_id: "' + experience_dict.get('_id').get('$oid') + '" })'
    _set = ' SET n.name="' + experience_dict.get('name') + '"'
    _set += ' SET n.privacy="' + str(experience_dict.get('privacy')) + '"'
    _set += ' SET n.archived="' + str(experience_dict.get('archived')) + '"'
    _set += ' SET n.pronoun="' + experience_dict.get('pronoun') + '"'
    _set += ' SET n.word_length="' + str(experience_dict.get('descriptionArrayLength')) + '"'
    _return = ' RETURN n'

    # This the query that updates the node
    cypher.execute(_match + _set + _return)

    # Get the updated experience node
    updated_experience_node = get_experience_node(experience_dict.get('_id').get('$oid'))

    # Detach all the relationships and delete all the words associated with the experience
    cypher.execute('MATCH (n { experience_id: "' + experience_dict.get('_id').get('$oid') + '" })-[r:HAS]-(w) DETACH DELETE w')

    for word in experience_dict.get('descriptionArray'):
        new_word_node = Node("Word", name=word, characters=len(word), nodeType='word',)
        experience_has_word = Relationship(updated_experience_node, "HAS", new_word_node)
        secure_graph1.create(experience_has_word)
        user_spoke_word = Relationship(new_user_node, "SPOKE", new_word_node)
        secure_graph1.create(user_spoke_word)

    return updated_experience_node

'''
Helper functions - Create new User/Log Relationship
cnr --> create new relationship
Takes a user node and log dict as paramaters
Returns a new_log_node
'''
def cnr_user_logged_log(new_user_node=None, log_dict=None):

    milliDate = log_dict.get('created').get('$date')
    date = datetime.datetime.fromtimestamp(milliDate/1000.0)

    # Create a new log node
    new_log_node = Node("Log",
        name=log_dict.get('name'),
        log_id=log_dict.get('_id').get('$oid'),
        privacy=log_dict.get('privacy'),
        archived=log_dict.get('archived'),
        physicArrayLength=log_dict.get('physicArrayLength'),
        emotionArrayLength=log_dict.get('emotionArrayLength'),
        academicArrayLength=log_dict.get('academicArrayLength'),
        communeArrayLength=log_dict.get('communeArrayLength'),
        etherArrayLength=log_dict.get('etherArrayLength'),
        physicContent=log_dict.get('physicContent'),
        emotionContent=log_dict.get('emotionContent'),
        academicContent=log_dict.get('academicContent'),
        communeContent=log_dict.get('communeContent'),
        etherContent=log_dict.get('etherContent'),
        milliDate=milliDate,
        year=date.year,
        month=date.month,
        day=date.day,
        hour=date.hour,
        minute=date.minute,
        second=date.second,
        nodeType='log',
        )

    ## You might be wondering, where are the words for a log... see the 'cnr_user_described_sublog'

    user_logged_log = Relationship(new_user_node, "LOGGED", new_log_node)
    secure_graph1.create(user_logged_log)

    return new_log_node

'''
Helper functions - update Log
update log node
Takes a user node and log dict as paramaters
Returns a new_log_node
'''
def update_log_node(new_user_node=None, log_dict=None):

    '''
    To get the log and change the node
    MATCH (n { log_id: '56ea1d34d73eaf7d11455fb8' }) SET n.name = 'Sleeping' RETURN n

    To get the activty and all of its word nodes
    MATCH (n { log_id: '56ea1d34d73eaf7d11455fb8' })-[r:HAS]-(w) RETURN n,w

    !!!
    This time is a little different, because we want to detach/delete the words,
    and then we also want to detach/delete the sublog
    !!!

    To delete the word nodes of a sublog for a log
    MATCH (n { log_id: '56ea1d34d73eaf7d11455fb8' })-[r:HAS]-(w) DETACH DELETE w
    '''
    cypher = secure_graph1.cypher

    _match = 'MATCH (n { log_id: "' + log_dict.get('_id').get('$oid') + '" })'
    _set = ' SET n.name="' + log_dict.get('name') + '"'
    _set += ' SET n.privacy="' + str(log_dict.get('privacy')) + '"'
    _set += ' SET n.archived="' + str(log_dict.get('archived')) + '"'
    _set += ' SET n.physicArrayLength="' + str(log_dict.get('physicArrayLength')) + '"'
    _set += ' SET n.emotionArrayLength="' + str(log_dict.get('emotionArrayLength')) + '"'
    _set += ' SET n.academicArrayLength="' + str(log_dict.get('academicArrayLength')) + '"'
    _set += ' SET n.communeArrayLength="' + str(log_dict.get('communeArrayLength')) + '"'
    _set += ' SET n.etherArrayLength="' + str(log_dict.get('etherArrayLength')) + '"'
    _set += ' SET n.physicContent="' + str(log_dict.get('physicContent')) + '"'
    _set += ' SET n.emotionContent="' + str(log_dict.get('emotionContent')) + '"'
    _set += ' SET n.academicContent="' + str(log_dict.get('academicContent')) + '"'
    _set += ' SET n.communeContent="' + str(log_dict.get('communeContent')) + '"'
    _set += ' SET n.etherContent="' + str(log_dict.get('etherContent')) + '"'
    _return = ' RETURN n'

    # This the query that updates the node
    cypher.execute(_match + _set + _return)

    # Get the updated log node
    updated_log_node = get_log_node(log_dict.get('_id').get('$oid'))

    # Detach all the relationships and delete all the words associated with the log
    cypher.execute('MATCH (n { log_id: "' + log_dict.get('_id').get('$oid') + '" })-[r:HAS]-(w) DETACH DELETE w')

    # Detach all the relationships and delete all the sublogs associated with the log
    cypher.execute('MATCH (n { log_id: "' + log_dict.get('_id').get('$oid') + '" })-[r:SUB_CONTAINS]-(sl) DETACH DELETE sl')

    ###
    # You might be wondering, where are the words are updated for a log...
    # ... they get deleted above and recreated... see the 'cnr_user_described_sublog'
    ###

    return updated_log_node

'''
Helper functions - Create new Log/SubLog Relationship
cnr --> create new relationship
Takes a user node, log node. log dict, sublog_array_name, and node_title as paramaters
Returns a new_log_node
'''
def cnr_log_contains_sub(new_user_node=None, new_log_node=None, log_dict=None, sublog_array_name=None, node_title=None):

    ## Only do the iteration step if there is a word to add
    if log_dict.get(sublog_array_name + 'ArrayLength') > 0:
        new_sub_log_node = cnr_user_described_sublog(
            new_user_node=new_user_node,
            new_log_node=new_log_node,
            log_dict=log_dict,
            sublog_array_name=sublog_array_name,
            node_title=node_title,
            )
        log_contains_sub = Relationship(new_log_node, "SUB_CONTAINS", new_sub_log_node)
        secure_graph1.create(log_contains_sub)

'''
Helper functions - Create new User/SubLog Relationship
cnr --> create new relationship
Takes a user node, log node. log dict, sublog_array_name, and node_title as paramaters
Returns a new_log_node
'''
def cnr_user_described_sublog(new_user_node=None, new_log_node=None, log_dict=None, sublog_array_name=None, node_title=None):

    # Create a new sublog node
    new_sub_log_node = Node(node_title,
        parentLogName=log_dict.get('name'),
        parentLogId=log_dict.get('_id').get('$oid'),
        privacy=log_dict.get('privacy'),
        archived=log_dict.get('archived'),
        wordLength=log_dict.get(sublog_array_name + 'ArrayLength'),
        content=log_dict.get(sublog_array_name + 'Content'),
        nodeType='sublog',
        )

    for word in log_dict.get(sublog_array_name + 'Array'):
        new_word_node = Node("Word", name=word, characters=len(word), nodeType='word',)
        log_has_word = Relationship(new_log_node, "HAS", new_word_node)
        secure_graph1.create(log_has_word)
        sublog_has_word = Relationship(new_sub_log_node, "HAS", new_word_node)
        secure_graph1.create(sublog_has_word)
        user_spoke_word = Relationship(new_user_node, "SPOKE", new_word_node)
        secure_graph1.create(user_spoke_word)

    user_described_sublog = Relationship(new_user_node, "DESCRIBED", new_sub_log_node)
    secure_graph1.create(user_described_sublog)

    return new_sub_log_node

'''
Transform an affect dictionary
Returns a new_rEmotion_node
'''
def transform_affect_dictionary(affect_dict=None, rEmotion=None):
    new_rEmotion_node = Node(
        "rEmotion",
        name=rEmotion,
        order1Length=len(affect_dict.get('order_1')),
        order2Length=len(affect_dict.get('order_2')),
        order3Length=len(affect_dict.get('order_3')),
    )

    return new_rEmotion_node

'''
Transform word to node
A word in this case is an rEmotion's synonym
Returns a new_rEmotion_node
'''
def transform_rEmotion_word(rEmotion=None, word=None, order=None):
    new_rEmotion_word_node = Node(
        "Word",
        rEmotion=rEmotion,
        name=word,
        order=order,
        characters=len(word),
        nodeType='word',
    )

    return new_rEmotion_word_node

'''
Helper functions - Create new rEmotion-Word/rEmotion Relationship
cnr --> create new relationship
Takes an rEmotion-word node, and rEmotion node
Returns an rEmotion_node
'''
def cnr_rEmotion_synonymized_by_rEmotion_word(rEmotion_node=None, rEmotion_word_node=None):

    rEmotion_synonymized_by_rEmotion_word = Relationship(rEmotion_node, "SYNONYMIZED_BY", rEmotion_word_node)
    secure_graph1.create(rEmotion_synonymized_by_rEmotion_word)

    return 'success'

'''
rEmotion > string
--
Returns a an object:
status - success
n number of lists - various lists, probably 4 for now, which are the similar words in each order
'''
def build_enhanced_rEmotion_similaritiy_object(rEmotion=None):

    order_1_and_2 = compare_two_orders_for_common_word_list(rEmotion=rEmotion, order_A=1, order_B=2)
    order_1_and_3 = compare_two_orders_for_common_word_list(rEmotion=rEmotion, order_A=1, order_B=3)
    order_2_and_3 = compare_two_orders_for_common_word_list(rEmotion=rEmotion, order_A=2, order_B=3)
    all_orders = compare_all_orders_for_common_word_list(rEmotion=rEmotion)

    return {
            'status': 'success',
            'word': rEmotion,
            'order_1_and_2': order_1_and_2['result'],
            'order_1_and_3': order_1_and_3['result'],
            'order_2_and_3': order_2_and_3['result'],
            'all_orders': all_orders['result'],
           }
