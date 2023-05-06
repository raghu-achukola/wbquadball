import json
import boto3
from quadball.db.api.validate_game_metadata import *
from google.protobuf.json_format import ParseDict
import os
from pymongo import MongoClient
import urllib
from typing import Tuple
from bson import json_util


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
    
def wrap_missing_param_error(missing_param_name:str) -> dict:
    return {
        'statusCode':400,
        'body':json.dumps({
            'title': f'Missing Parameter {missing_param_name}'
        })
    }
def lambda_handler(event,  context ) -> dict:
    # Call from an API from this format
    
    # /quadball-stats/validate-game-metadata
    # ?game_id={game_id}&tournament_id={tournament_id}&season_id={season_id}
    # &team_a_id={team_a_id}&team_b_id={team_b_id}
    qsp = event.get('queryStringParameters',{})

    REQUIRED = ['game_id','tournament_id','season_id','team_a_id','team_b_id']
    api_kwargs = {}
    for param in REQUIRED:
        param_value = qsp.get(param)
        if not param_value:
            return wrap_missing_param_error(param)
        api_kwargs[param] = param_value

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
    try:
        response = validate_game_metadata(db,**api_kwargs)
        return {
            'statusCode':200,
            'body':json_util.dumps(
                response
            )
        }       
        
    except Exception as e: 
        return {
            'statusCode':500,
            'body':json.dumps({
                'title': 'Error validating game metadata',
                'exception': str(e)
            })
        }
    
