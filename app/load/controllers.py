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
                                   get_rep_emotion_order)

from transform.controllers import (cnr_user_did_activity,
                                   cnr_user_experienced_experience,
                                   cnr_user_logged_log,
                                   cnr_log_contains_sub,
                                   update_activity_node,
                                   update_experience_node,
                                   update_log_node,
                                   transform_affect_dictionary,
                                   transform_rEmotion_word,
                                   cnr_rEmotion_synonymized_by_rEmotion_word)


# TODO: Store these in a database along with a description of their origin
'''
uses the entire synopsis of emotions in the corpora
'''
all_emotions = ['abandonment', 'abhorrence', 'abomination', 'absorption', 'abstinence', 'acceptance', 'admiration', 'adoration', 'affection', 'affectionateness', 'affliction', 'aggravation', 'aggressiveness', 'agony', 'alarm', 'alienation', 'aliveness', 'aloofness', 'alteration', 'amazement', 'ambiance', 'amusement', 'anger', 'angst', 'anguish', 'animation', 'anticipation', 'antipathy', 'anxiety', 'apathy', 'appraisal', 'appreciation', 'arousal', 'arrogance', 'assimilation', 'astonishment', 'attraction', 'audaciousness', 'aversion', 'avoidance', 'awareness', 'awe', 'awfulness', 'awkwardness', 'badness', 'bashfulness', 'belief', 'bewilderment', 'bitterness', 'blame', 'blessedness', 'boldness', 'boredom', 'bravery', 'brightness', 'calmness', 'capableness', 'cautiousness', 'certainty', 'chastity', 'cheerfulness', 'cleverness', 'closeness', 'cloudiness', 'coercion', 'coldness', 'compassion', 'composure', 'compromise', 'compulsion', 'concern', 'confidence', 'conformity', 'confusion', 'consciousness', 'consideration', 'consonance', 'contempt', 'content', 'contentment', 'contrariness', 'courage', 'courageousness', 'covetousness', 'criticalness', 'crossness', 'curiosity', 'darkness', 'decency', 'defeat', 'defiance', 'delight', 'denial', 'depression', 'desire', 'desolation', 'despair', 'despicableness', 'determination', 'devastation', 'devotion', 'diffidence', 'diligence', 'dimension', 'disappointment', 'disbelief', 'disdain', 'disgrace', 'disgust', 'disillusionment', 'dislike', 'dismay', 'disorientation', 'disrespect', 'dissonance', 'distance', 'distress', 'distrust', 'disturbance', 'dominance', 'doubt', 'doubtfulness', 'dread', 'dullness', 'eagerness', 'earnestness', 'easiness', 'ecstasy', 'edginess', 'ego', 'elation', 'embarrassment', 'empathy', 'emptiness', 'encouragement', 'endurance', 'engagement', 'engrossment', 'enjoyment', 'enlightenment', 'enragement', 'enthusiasm', 'envy', 'eroticism', 'euphoria', 'exasperation', 'excitation', 'excitement', 'exhaustion', 'exploitation', 'exuberance', 'familiarity', 'fascination', 'fate', 'fatigue', 'fear', 'festivity', 'flatness', 'fondness', 'foolishness', 'forgiveness', 'fortune', 'freedom', 'fright', 'friskiness', 'frustration', 'fulfillment', 'furiousness', 'fury', 'gallantry', 'gayness', 'glee', 'gloominess', 'gluttony', 'goodness', 'grace', 'gratification', 'gratitude', 'greatness', 'greed', 'grief', 'guilt', 'happiness', 'hardiness', 'harmony', 'hate', 'helplessness', 'hesitance', 'hesitancy', 'honor', 'hope', 'hopefulness', 'horror', 'hostility', 'hotness', 'humbleness', 'humiliation', 'humility', 'hurt', 'ignorance', 'importance', 'impulse', 'impulsiveness', 'inadequacy', 'inadequateness', 'incapableness', 'indifference', 'inducement', 'indulgence', 'infatuation', 'infection', 'inferiority', 'inflammation', 'infuriation', 'innocence', 'inquisitiveness', 'insecurity', 'insignificance', 'inspiration', 'insult', 'intensity', 'intentness', 'interest', 'intimacy', 'intrigue', 'invulnerability', 'irritation', 'isolation', 'jealousy', 'joy', 'jubilance', 'keenness', 'kindness', 'liberality', 'liberation', 'lifelessness', 'liveliness', 'lividness', 'loathing', 'loneliness', 'loss', 'lousiness', 'love', 'luck', 'luckiness', 'lunacy', 'lust', 'mania', 'melancholy', 'merriness', 'misery', 'modesty', 'motivation', 'mournfulness', 'negation', 'negativeness', 'neglect', 'nervousness', 'neutrality', 'nonchalance', 'nostalgia', 'numbness', 'obsession', 'offensiveness', 'openness', 'optimism', 'outrage', 'pain', 'panic', 'paralysis', 'passion', 'passionateness', 'patience', 'peacefulness', 'permanence', 'perplexity', 'persuasion', 'perturbation', 'pessimism', 'petrification', 'pity', 'playfulness', 'pleasantness', 'pleasure', 'positiveness', 'potency', 'power', 'powerfulness', 'powerlessness', 'preoccupation', 'pride', 'provocation', 'quietness', 'quirkiness', 'rage', 'reassurance', 'rebellion', 'rebelliousness', 'reception', 'receptiveness', 'reenforcement', 'regret', 'reinforcement', 'rejection', 'relaxation', 'reliability', 'relief', 'reluctance', 'remorse', 'reproach', 'resentment', 'reservation', 'resignation', 'resistance', 'respect', 'restlessness', 'revulsion', 'ridicule', 'sadness', 'safety', 'saltiness', 'sarcasm', 'satisfaction', 'scorn', 'sensitivity', 'serenity', 'seriousness', 'shakiness', 'shame', 'shock', 'shyness', 'skepticism', 'sloth', 'snoopiness', 'sobriety', 'sourness', 'spirit', 'spiritedness', 'spite', 'stolidity', 'straightness', 'strength', 'stress', 'stubbornness', 'stupidity', 'submission', 'subversion', 'sulkiness', 'sulky', 'sullenness', 'sunniness', 'sureness', 'surprise', 'suspicion', 'sweetness', 'sympathy', 'tearfulness', 'tenaciousness', 'tenacity', 'tenderness', 'tenseness', 'terribleness', 'terror', 'thoughtfulness', 'threat', 'thrill', 'tolerance', 'tragedy', 'triumph', 'trust', 'uncertainty', 'understanding', 'uneasiness', 'unhappiness', 'unification', 'uniqueness', 'unity', 'unpleasantness', 'unpredictability', 'uselessness', 'valence', 'validation', 'vanity', 'veneration', 'vengefulness', 'victimization', 'vigor', 'vileness', 'vulnerability', 'warmness', 'weariness', 'withdrawal', 'withdrawnness', 'woe', 'woefulness', 'wonder', 'wonderfulness', 'worry', 'worthlessness', 'wrath']


# Move a user and some relationship to the neo4j database
## A word_length is the number of words in the descriptionArrayLength
'''
This method CREATES a single activity node from neo4j

To find a user node:
MATCH (u:User {user_id: "56db97954eca34d01404888a"}) RETURN u

'''
def create_single_activity(activity=None):

    cypher = secure_graph1.cypher

    # Find all activities, but really just one in this case
    activity_cursor = mongo3.db.activities.find({"_id": ObjectId(activity)})
    json_activity = json.dumps(activity_cursor[0], default=json_util.default)

    # Create a new python dictionary from the json_activity, we'll call it activity_dict
    activity_dict = json.loads(json_activity)
    print activity_dict

    ###
    # Business logic for USER_NODE starts here, uses data from above.
    ###
    user_id = activity_dict.get('user').get('$oid')

    user_node = get_user_node(user_id=user_id)

    ###
    # Business logic for ACTIVITIY_NODE starts here, uses data from above.
    ###

    cnr_user_did_activity(new_user_node=user_node, activity_dict=activity_dict)

    return 'success'

'''
This method UPDATES a single activity node from neo4j
'''
def update_single_activity(activity=None):
    print '====update single activity node===='
    print activity

    cypher = secure_graph1.cypher

    # Find all activities, but really just one in this case
    activity_cursor = mongo3.db.activities.find({"_id": ObjectId(activity)})
    json_activity = json.dumps(activity_cursor[0], default=json_util.default)

    # Create a new python dictionary from the json_activity, we'll call it activity_dict
    activity_dict = json.loads(json_activity)

    ###
    # Business logic for USER_NODE starts here, uses data from above.
    ###
    user_id = activity_dict.get('user').get('$oid')
    user_node = get_user_node(user_id=user_id)

    ###
    # Business logic for ACTIVITY_NODE starts here, uses data from above.
    ###
    update_activity_node(new_user_node=user_node, activity_dict=activity_dict)

    # TODO: update this: where the experience node changes its containing activity

    return 'success'

'''
This method DESTROYS a single activity node from neo4j
'''
def destroy_single_activity(activity=None):
    print '====destroy single activity node===='
    print activity

    # TODO: Figure how to implement this delete correctly

    return 'success'

'''
This method CREATES a single experience node from neo4j
'''
def create_single_experience(experience=None):
    print '====create single experience node===='

    cypher = secure_graph1.cypher

    # Find all activities, but really just one in this case
    experience_cursor = mongo3.db.experiences.find({"_id": ObjectId(experience)})
    json_experience = json.dumps(experience_cursor[0], default=json_util.default)

    # Create a new python dictionary from the json_experience, we'll call it experience_dict
    experience_dict = json.loads(json_experience)
    print experience_dict

    ###
    # Business logic for USER_NODE starts here, uses data from above.
    ###
    user_id = experience_dict.get('user').get('$oid')
    user_node = get_user_node(user_id=user_id)

    ###
    # Business logic for getting ACTIVITY_NODE starts here, uses data from above.
    ###
    activity_id = experience_dict.get('firstActivity').get('$oid')
    activity_node_one = get_activity_node(activity_id=activity_id)
    activity_id = experience_dict.get('secondActivity').get('$oid')
    activity_node_two = get_activity_node(activity_id=activity_id)

    ###
    # Business logic for EXPERIENCE_NODE starts here, uses data from above.
    ###
    new_experience_node = cnr_user_experienced_experience(new_user_node=user_node, experience_dict=experience_dict)

    # Create a new relationship for the activity/experience
    activity_contains_experience = Relationship(activity_node_one, "CONTAINS", new_experience_node)
    secure_graph1.create(activity_contains_experience)
    activity_contains_experience = Relationship(activity_node_two, "CONTAINS", new_experience_node)
    secure_graph1.create(activity_contains_experience)

    return 'success'

'''
This method UPDATES a single experience node from neo4j
'''
def update_single_experience(experience=None):

    print '====update single experience node===='

    cypher = secure_graph1.cypher

    # Find all activities, but really just one in this case
    experience_cursor = mongo3.db.experiences.find({"_id": ObjectId(experience)})
    json_experience = json.dumps(experience_cursor[0], default=json_util.default)

    # Create a new python dictionary from the json_experience, we'll call it experience_dict
    experience_dict = json.loads(json_experience)
    print experience_dict

    ###
    # Business logic for USER_NODE starts here, uses data from above.
    ###
    user_id = experience_dict.get('user').get('$oid')
    user_node = get_user_node(user_id=user_id)

    ###
    # Business logic for EXPERIENCE_NODE starts here, uses data from above.
    ###
    update_experience_node(new_user_node=user_node, experience_dict=experience_dict)

    # TODO: update this: where the experience node changes its containing activity


    '''
    Inspiration below, but the first experience changes, so remove/change the old relationship,
    and then add a new relationship like normal
    '''

    # http://stackoverflow.com/questions/19016947/neo4j-how-do-i-delete-a-specific-relationship-with-cypher
    # START n=node(*)
    # MATCH n-[rel:HAS_ROLE]->r
    # WHERE n.name='Tamil' AND r.name='tester'
    # DELETE rel

    return 'success'

'''
This method DESTROYS a single experience node from neo4j
'''
def destroy_single_experience(experience=None):
    print '====destroy single experience node===='
    print experience

    # TODO: Figure how to implement this delete correctly

    return 'success'

'''
This method CREATES a single log node from neo4j
'''
def create_single_log(log=None):
    print '====create single log node===='

    cypher = secure_graph1.cypher

    # Find all activities, but really just one in this case
    log_cursor = mongo3.db.logs.find({"_id": ObjectId(log)})
    json_log = json.dumps(log_cursor[0], default=json_util.default)

    # Create a new python dictionary from the json_log, we'll call it log_dict
    log_dict = json.loads(json_log)

    ###
    # Business logic for USER_NODE starts here, uses data from above.
    ###
    user_id = log_dict.get('user').get('$oid')
    user_node = get_user_node(user_id=user_id)

    ###
    # Business logic for getting EXPERIENCE_NODE starts here, uses data from above.
    ###
    experience_id = log_dict.get('firstExperience').get('$oid')
    experience_node = get_experience_node(experience_id=experience_id)

    ###
    # Business logic for LOG_NODE starts here, uses data from above.
    ###
    new_log_node = cnr_user_logged_log(new_user_node=user_node, log_dict=log_dict)

    ###
    # Business logic for SUBLOG_NODE starts here, uses data from above.
    ###

    # List of all dictionary types
    sublog_list = ['physic', 'emotion', 'academic', 'commune', 'ether']

    for sublog_name in sublog_list:
        # This method also creates a new sublog, and builds a relationship
        # to the user (and adds the word nodes)!
        cnr_log_contains_sub(
            new_user_node=user_node,
            new_log_node=new_log_node,
            log_dict=log_dict,
            sublog_array_name=sublog_name,
            node_title=sublog_name.title() + 'Log',
            )

    # Create a new relationship for the experience/log
    experience_contains_log = Relationship(experience_node, "CONTAINS", new_log_node)
    secure_graph1.create(experience_contains_log)

    return 'success'


'''
This method UPDATES a single log node from neo4j
'''
def update_single_log(log=None):
    print '====update single log node===='

    cypher = secure_graph1.cypher

    # Find all activities, but really just one in this case
    log_cursor = mongo3.db.logs.find({"_id": ObjectId(log)})
    json_log = json.dumps(log_cursor[0], default=json_util.default)

    # Create a new python dictionary from the json_log, we'll call it log_dict
    log_dict = json.loads(json_log)
    print log_dict

    ###
    # Business logic for USER_NODE starts here, uses data from above.
    ###
    user_id = log_dict.get('user').get('$oid')

    user_node = get_user_node(user_id=user_id)

    # TODO: Get the log node, and update it and its words!!

    ###
    # Business logic for LOG_NODE starts here, uses data from above.
    ###
    log_node = update_log_node(new_user_node=user_node, log_dict=log_dict)

    # TODO: update this: where the log node changes its containing experience

    ###
    # Business logic for SUBLOG_NODE starts here, uses data from above.
    ###

    # List of all dictionary types
    sublog_list = ['physic', 'emotion', 'academic', 'commune', 'ether']

    for sublog_name in sublog_list:
        # This method also creates a new sublog, and builds a relationship
        # to the user (and adds the word nodes)!
        cnr_log_contains_sub(
            new_user_node=user_node,
            new_log_node=log_node,
            log_dict=log_dict,
            sublog_array_name=sublog_name,
            node_title=sublog_name.title() + 'Log',
            )

    return 'success'

'''
This method DESTROYS a single log node from neo4j
'''
def destroy_single_log(log=None):
    print '====destroy single log node===='
    print log

    # TODO: Figure how to implement this delete correctly

    return 'success'


'''
This method CREATES an rEmotion node and relates it to the rEmotion-words is has in it's corpus
'''
def create_single_rEmotion_corpus(rEmotion=None):

    order_1 = get_rep_emotion_order(rEmotion=rEmotion, order_num=1)['result']
    order_2 = get_rep_emotion_order(rEmotion=rEmotion, order_num=2)['result']
    order_3 = get_rep_emotion_order(rEmotion=rEmotion, order_num=3)['result']

    affect_dict = {
                  'rEmotion': rEmotion,
                  'order_1': order_1,
                  'order_2': order_2,
                  'order_3': order_3,
                  }

    rEmotion_node = transform_affect_dictionary(affect_dict=affect_dict, rEmotion=rEmotion)

    for word in order_1:
        rEmotion_word_node = transform_rEmotion_word(rEmotion=rEmotion, word=word, order=1)
        cnr_rEmotion_synonymized_by_rEmotion_word(
            rEmotion_node=rEmotion_node, rEmotion_word_node=rEmotion_word_node
            )
    for word in order_2:
        rEmotion_word_node = transform_rEmotion_word(rEmotion=rEmotion, word=word, order=2)
        cnr_rEmotion_synonymized_by_rEmotion_word(
            rEmotion_node=rEmotion_node, rEmotion_word_node=rEmotion_word_node
            )
    for word in order_3:
        rEmotion_word_node = transform_rEmotion_word(rEmotion=rEmotion, word=word, order=3)
        cnr_rEmotion_synonymized_by_rEmotion_word(
            rEmotion_node=rEmotion_node, rEmotion_word_node=rEmotion_word_node
            )

    return 'success'


'''
This method only deletes all the records.
It relies on there being a mongo database. **VERY IMPORTANT**
'''

def delete_records():
    # Clear the database
    secure_graph1.delete_all()
    return 'success'


'''
This method deletes all the records then adds all relationships and nodes.
It relies on there being a mongo database. **VERY IMPORTANT**

Here are useful queries to find all the records for a user for a given node attr:

--Find all the nodes that are words with a name of name 'spoken' by a user with an email address of email--
MATCH (n:User {email: "<email>"})-[r:SPOKE]-(a:Word {name: "<name>"}) return a

--Find all the distinct nodes that are 'spoken' by a user--
MATCH (n:User)-[r:SPOKE]-(a) return DISTINCT a

'''

def create_records():

    # Clear the database
    secure_graph1.delete_all()

    user_cursor = mongo3.db.users.find({}) #find all users
    ####
    # For every user create a node
    ####
    for user in user_cursor:
        json_user = json.dumps(user, default=json_util.default)

        user_dict = json.loads(json_user)

        # Create a bunch of user nodes
        # TODO: Make a model for this and use that.
        new_user_node = Node("User",
            email=user_dict.get('email'),
            user_id=user_dict.get('_id').get('$oid'),
            nodeType='user',
            )

        ####
        user = user_dict.get('_id').get('$oid')
        activity_cursor = mongo3.db.activities.find({"user": ObjectId(user)}) #find all activities for a user
        ####
        # For every activity create a node
        ####
        for activity in activity_cursor:
            json_activity = json.dumps(activity, default=json_util.default)

            # Create a new python dictionary from the json_activity, we'll call it activity_dict
            activity_dict = json.loads(json_activity)

            # Output is a new_activity_node
            # TODO: Make a model for this and use that.
            new_activity_node = cnr_user_did_activity(
                new_user_node=new_user_node,
                activity_dict=activity_dict
                )

            ####
            activity = activity_dict.get('_id').get('$oid')
            experience_cursor = mongo3.db.experiences.find({"firstActivity": ObjectId(activity)}) #find all experiences for an activity
            ####
            # For every experience create a node
            ####
            for experience in experience_cursor:
                json_experience = json.dumps(experience, default=json_util.default)

                # Create a new python dictionary from the json_experience, we'll call it experience_dict
                experience_dict = json.loads(json_experience)

                # Output is a new_experience_node
                # TODO: Make a model for this and use that.
                new_experience_node = cnr_user_experienced_experience(
                    new_user_node=new_user_node,
                    experience_dict=experience_dict
                    )

                # Create a new relationship for the activity/experience
                activity_contains_experience = Relationship(new_activity_node, "CONTAINS", new_experience_node)
                secure_graph1.create(activity_contains_experience)

                ####
                experience = experience_dict.get('_id').get('$oid')
                log_cursor = mongo3.db.logs.find({"firstExperience": ObjectId(experience)}) #find all logs for an experience
                ####
                # For every log create a node
                ####
                for log in log_cursor:
                    json_log = json.dumps(log, default=json_util.default)

                    # Create a new python dictionary from the json_experience, we'll call it log_dict
                    log_dict = json.loads(json_log)

                    # TODO: Make a model for this and use that.
                    new_log_node = cnr_user_logged_log(
                        new_user_node=new_user_node,
                        log_dict=log_dict,
                        )

                    # List of all dictionary types
                    sublog_list = ['physic', 'emotion', 'academic', 'commune', 'ether']

                    for sublog_name in sublog_list:
                        # This method also creates a new sublog, and builds a relationship
                        # to the user (and adds the word nodes)!
                        cnr_log_contains_sub(
                            new_user_node=new_user_node,
                            new_log_node=new_log_node,
                            log_dict=log_dict,
                            sublog_array_name=sublog_name,
                            node_title=sublog_name.title() + 'Log',
                            )

                    experience_contains_log = Relationship(new_experience_node, "CONTAINS", new_log_node)
                    secure_graph1.create(experience_contains_log)


    return 'success'

# Move an event - as a year, month, or day - and some relationship to the neo4j database
'''
The whole point of running this step is to store this information as a data warehouse

To find all the distinct dates (event):
    MATCH (u)-[r:LOGGED]->(n:Log) RETURN DISTINCT n.year, n.month, n.day, u.email

To find all the sums we care about for a given date (event):
    MATCH (u)-[r:LOGGED]->(n:Log) where n.year = 2016 and n.month = 1 and n.day = 6
    RETURN sum(n.physicArrayLength), sum(n.academicArrayLength), sum(n.emotionArrayLength), sum(n.communeArrayLength), sum(n.etherArrayLength)

To find all the nodes we care about for a given date (event):
    MATCH (n:Log) where n.year = 2015 and n.month = 11 and n.day = 29
    RETURN n

To find all nodes in a year (event):
  MATCH (n:Log) where n.year = 2016 RETURN (n)

To find all nodes in a month (event):
  MATCH (n:Log) where n.year = 2016 and n.month = 1 RETURN (n)

To find all nodes in a day (event):
  MATCH (n:Log) where n.year = 2016 and n.month = 1 and n.day = 6 RETURN (n)
'''

def create_event_supplement():
    # Create events with the following attributes...
    # logCount, highestValue, totals for each category, winningCategoryName
    cypher = secure_graph1.cypher
    for event_record in cypher.execute("MATCH (u)-[r:LOGGED]->(n:Log) RETURN DISTINCT n.year, n.month, n.day, u.user_id"):
        sums = cypher.execute("MATCH (u)-[r:LOGGED]->(n:Log) where n.year = " + str(event_record[0]) + " and n.month = " + str(event_record[1]) + " and n.day = " + str(event_record[2]) + " and u.user_id = '" + event_record[3] + "' " +
                              "RETURN sum(n.physicArrayLength), sum(n.emotionArrayLength), sum(n.academicArrayLength), sum(n.communeArrayLength), sum(n.etherArrayLength), u.user_id, count(n)")[0]
        # Find the position of the max values in the list
        winningIndexes = []

        sum_list = [sums[0], sums[1], sums[2], sums[3], sums[4]]
        max_value = max(sum_list)

        for idx,s in enumerate(sum_list):
            if s >= max_value:
                winningIndexes.append(idx)

        # TODO: Make a model for this and use that.
        new_event_node = Node("Event",
            user = sums[5],
            ymd=str(event_record[0]) + '-' + str(event_record[1]) + '-' + str(event_record[2]),
            year=event_record[0],
            month=event_record[1],
            day=event_record[2],
            physicArrayLengthSum = sums[0],
            emotionArrayLengthSum = sums[1],
            academicArrayLengthSum = sums[2],
            communeArrayLengthSum = sums[3],
            etherArrayLengthSum = sums[4],
            winningIndexes = winningIndexes,
            logCount = sums[6],
            )

        for log_record in cypher.execute("MATCH (u)-[r:LOGGED]->(n:Log) where n.year = " + str(event_record[0]) + " and n.month = " + str(event_record[1]) + " and n.day = " + str(event_record[2]) + " and u.user_id = '" + event_record[3] + "' " + " " +
                                         "RETURN n"):
            for log_node in log_record:
                event_includes_log = Relationship(new_event_node, "INCLUDES", log_node)
                secure_graph1.create(event_includes_log)

    return 'success'
