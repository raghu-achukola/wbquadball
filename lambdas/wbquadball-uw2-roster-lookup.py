import json
import boto3
from quadball.db.api.roster_lookup import * 
from google.protobuf.json_format import ParseDict
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
    # /quadball-stats/roster-lookup?players={jsonobj}, more params
    qsp = event.get('queryStringParameters',{})
    jersey_player_name_map = json.loads(qsp.get('players',''))
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
        response = roster_lookup(db,jersey_player_name_map)
        # TODO: alter the status to return different things based on 
        # parameters/ Sometimes duplicates ok, sometimes empty ok 
        # for now, reject all but perfect match
        unmatched = response['unmatched']
        overmatched = response['overmatched']
        if unmatched or overmatched:
            return {
                'statusCode':400,
                'body':json.dumps({
                    'status':'Certain names could not be found or found >1 match',
                    'response':response
                })
            }
        return {
            'statusCode':200,
            'body':json.dumps({
                'status':'Successful roster retrieval',
                'response':response
            })
        }       
        
    except Exception as e: 
        return {
            'statusCode':500,
            'body':json.dumps({
                'title': 'Error looking up roster',
                'exception': str(e)
            })
        }
