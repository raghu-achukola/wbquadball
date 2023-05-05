import json
import boto3
from quadball.db.api.register import *
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
    # /quadball-stats/register-entity/{entity-type}?object={jsonobj}, more params
    object_type = event.get('pathParameters',{}).get('proxy',{})
    qsp = event.get('queryStringParameters',{})
    object_value = json.loads(qsp.get('object',''))
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
        id = register(db,object_value,object_type)
        # TODO: Open question - is this best design? 
        # Should we not return the already existing id in the case of duplicate?
        status = 'DUPLICATE - NOT INSERTED' if id is None else 'COMPLETE'
        return {
            'statusCode':200,
            'body':json.dumps({
                'status':status,
                'inserted_id':None if id is None else str(id) 
            })
        }
    except Exception as e: 
        return {
            'statusCode':500,
            'body':json.dumps({
                'title': 'Error registering Object',
                'exception': str(e)
            })
        }
    # try:
    #     id = register(db,object_value,object_type)
    # except Exception as e: 
    #     pass
    # finally:
    #     return {'status':400,'id':id}