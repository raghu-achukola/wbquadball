import json
import boto3
# Lambda should be able to read openpyxl from layer
from openpyxl  import load_workbook   
from typing import Tuple
from io import BytesIO
from quadball.statsheet.parser import gen_statsheet_possessions
from quadball.db.statsheet_converter import convert_single_extra

def extract_first_file_from_event(event) -> Tuple[str,str]:
    s3_event = event['Records'][0]['s3']
    return s3_event['bucket']['name'], s3_event['object']['key']
    
def lambda_handler(event, context) -> dict:
    s3 = boto3.client('s3')
    bucket, obj = extract_first_file_from_event(event)
    response  = s3.get_object( Bucket= bucket, Key = obj)
    stream = BytesIO(response['Body'].read())
    ws = load_workbook(stream).active
    for statsheet_possession in gen_statsheet_possessions(ws):
        extra_text = statsheet_possession.extras
        if extra_text:
            teams = ['A','B']
            offense = statsheet_possession.offense
            defense = teams[offense =='A']
            print(f'Trying to map extra annotation: {extra_text}')
            extra = convert_single_extra(extra_text,offense,defense)
            print(extra)


    return {
        'statusCode': 200,
        'body': json.dumps('Custom code')
    }
