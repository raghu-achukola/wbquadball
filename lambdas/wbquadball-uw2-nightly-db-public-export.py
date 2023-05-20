import json
import boto3
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
import pymongo
import os
from pymongo import MongoClient
import urllib
from typing import Tuple

"""
    Environment variables for this lambda:

    MONGO_SECRET_ARN: arn for the secret containing MongoDB connection
    credentials

    EXPORT_BUCKET : bucket for the S3 dump

    EXPORT_PREFIX: prefix (folder) for the S3 dump


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
    
def export_collection(db:pymongo.database.Database, s3_client, collection_name:str ): 
    output = []
    for record in db[collection_name].find({}):
        record['_id'] = str(record['_id'])
        output.append(record)
    s3_client.put_object(
        Bucket = os.environ['EXPORT_BUCKET'],
        Key = (os.environ['EXPORT_PREFIX'] if os.environ['EXPORT_PREFIX'] else '' ) + collection_name + '.json',
        Body = json.dumps(output).encode('utf-8')
    )

def lambda_handler(event,  context ) -> dict:
    mongo_client, db_name = initialize_connection()
    s3_client = boto3.client('s3')
    db = mongo_client[db_name]
    collections =  ('leagues','seasons','tournaments','teams','games')
    with ThreadPoolExecutor(10) as executor:
        executor.map(export_collection,repeat(db),repeat(s3_client), collections)
