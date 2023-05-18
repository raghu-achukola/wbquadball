import json
import boto3
from quadball.db.api.reload_game import reload_possessions
from quadball.db.api.find_entity import find
from quadball.schema.db.stats_pb2 import Possession
from google.protobuf.json_format import ParseDict,MessageToDict
from bson.objectid import ObjectId
import os
from pymongo import MongoClient
import urllib
from typing import Tuple

"""
    Environment variables for this lambda:

    MONGO_SECRET_ARN: arn for the secret containing MongoDB connection
    credentials

"""
def initialize_connection() -> Tuple[MongoClient,str]:
    """
        initializes connection to Mongo client. 
        Secret has the following key value pairs:
        username
        password
        host
        db_name
    """
    sm = boto3.client('secretsmanager')
    secret_json = json.loads(
        sm.get_secret_value(
            SecretId = os.environ['SECRET_ARN']
        )['SecretString']
    )
    
    username = secret_json.get('username','')
    password = secret_json.get('password','')
    host = secret_json.get('host','')
    db_name = secret_json.get('db_name','')

    if not (username and password and host and db_name):
        raise Exception('Empty or nonexistent connection parameters')
    CONNECTION_STRING = f'mongodb+srv://{urllib.parse.quote_plus(username)}:{urllib.parse.quote_plus(password)}@{host}/{urllib.parse.quote_plus(db_name)}'
    return MongoClient(CONNECTION_STRING), db_name
    

def lambda_handler(event,  context ) -> dict:
    # Call from an API from this format
    # /quadball-stats/reload-game/{game-id}?possessions={jsonobj}, more params

    # Step 1 -> Retrieve game
    # Step 2 -> Parse Possessions
    game_id = event.get('pathParameters',{}).get('proxy',{})
    qsp = event.get('queryStringParameters',{})
    possessions = json.loads(qsp.get('possessions',''))

    try:
        possession_objects = [ParseDict(possession, Possession()) for possession in possessions]
    except Exception as e: 
        return {
            'statusCode':400,
            'body':json.dumps({
                'title': 'Error parsing possessions',
                'exception': str(e)
            })
        }
    try:
        client, db_name = initialize_connection()
        db = client[db_name]
    # TODO: Catch specific exceptions -> show different 500 codes
    except Exception as e: 
        return {
            'statusCode':500,
            'body':json.dumps({
                'title': 'Error initializing Connection',
                'exception': str(e)
            })
        }
    
    # GET GAME NATURALLY IF NOT PROVIDED
    try:
        client, db_name = initialize_connection()
        db = client[db_name]
        game = find(db,obj_id=game_id,obj_type='game')
    # TODO: Catch specific exceptions -> show different 500 codes
    except Exception as e: 
        return {
            'statusCode':500,
            'body':json.dumps({
                'title': 'Error finding all parameters',
                'exception': str(e)
            })
        }

    try:
        new_game, new_possessions = reload_possessions(db,game._id,possession_objects)
        mtd = MessageToDict(new_game,preserving_proto_field_name=True)
        del mtd['_id']
        db['games'].replace_one({'_id':ObjectId(new_game._id)},mtd )
    except Exception as e: 
        return {
            'statusCode':500,
            'body':json.dumps({
                'title': 'Error replacing game information',
                'exception': str(e)
            })
        }
    try:
        delete_result = db['possessions'].delete_many(
            {'game_id':game._id}
        )
        insert_result = db['possessions'].insert_many(
            [MessageToDict(x, preserving_proto_field_name=True) for x in new_possessions]
        )
        return {
            'statusCode':200,
            'body':json.dumps({
                'title': 'Success',
                'game':new_game._id,
                'inserted_possession_ids':[str(x) for x in insert_result.inserted_ids],
                'deleted_count':delete_result.deleted_count
            })
        }
    except Exception as e: 
        return {
            'statusCode':500,
            'body':json.dumps({
                'title': 'Error loading possessions',
                'exception': str(e)
            })
        }