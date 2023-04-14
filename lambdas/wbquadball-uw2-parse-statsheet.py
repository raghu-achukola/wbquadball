import json
import boto3
# Lambda should be able to read openpyxl from layer
from openpyxl  import load_workbook   
from typing import Tuple
from io import BytesIO
from quadball.statsheet.parser import gen_statsheet_possessions
# Increment 10 -> test lambda by converting whole possessions
from quadball.db.statsheet_converter import convert_possession 
# Increment 11 -> test lambda (unit testing) by returning (not just printing) last possession
from google.protobuf.json_format import MessageToJson

def extract_first_file_from_event(event) -> Tuple[str,str]:
    s3_event = event['Records'][0]['s3']
    return s3_event['bucket']['name'], s3_event['object']['key']
    
def lambda_handler(event, context) -> dict:
    s3 = boto3.client('s3')
    bucket, obj = extract_first_file_from_event(event)
    response  = s3.get_object( Bucket= bucket, Key = obj)
    stream = BytesIO(response['Body'].read())
    ws = load_workbook(stream).active
    possessions = []
    for statsheet_possession in gen_statsheet_possessions(ws):
        possession = convert_possession(statsheet_possession)
        possessions.append(possession)
        print(possession)
    return {
        'statusCode': 200,
        'body': MessageToJson(possessions[-1])
    }
