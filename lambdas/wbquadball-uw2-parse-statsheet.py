import json
import boto3
# Lambda should be able to read openpyxl from layer
from openpyxl  import load_workbook
from openpyxl.workbook.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from typing import Tuple
from io import BytesIO
from quadball.statsheet.parser import gen_statsheet_possessions
# Increment 10 -> test lambda by converting whole possessions
from quadball.db.statsheet_converter import convert_possession 
# Increment 11 -> test lambda (unit testing) by returning (not just printing) last possession
from google.protobuf.json_format import MessageToJson
from quadball.schema.db.stats_pb2 import Possession

def extract_first_file_from_event(event) -> Tuple[str,str]:
    s3_event = event['Records'][0]['s3']
    return s3_event['bucket']['name'], s3_event['object']['key']

def extract_sheets(workbook:Workbook) -> Tuple[Worksheet, Worksheet, Worksheet]:
    """
        extract_sheets will eventually be exception-proofed, but currently 
        converts a Statsheet workbook object into 3 worksheets
        
        in order: 
        -   possessions, which is usually called 'POSSESSIONS'
        -   roster, which is usually called 'ROSTERS'
        -   metadata, which is usually called 'METADATA' 


    """

    # In the future there needs to be an unchangeable structure here, 
    # but due to the variability of historical records - here we keep this icky code
    WORKSHEET_POSSESSIONS = 'POSSESSIONS'
    WORKSHEET_ROSTER = 'ROSTERS'
    WORKSHEET_METADATA = 'METADATA'
    return ( 
        workbook.get_sheet_by_name(name = ws) 
        for ws in [WORKSHEET_POSSESSIONS, WORKSHEET_ROSTER, WORKSHEET_METADATA] 
    )

def process_possessions(possession_worksheet:Worksheet) -> list[Possession]:
    """
        process_possessions takes in

        INPUTS: 
        possession_worksheet :  the worksheet that contains possession information
                                in the template given
        
        and returns

        OUTPUTS: 
        possessions           : a list of Possession (Mongodb Data Model) objects
    """
    possessions = []
    
    for statsheet_possession in gen_statsheet_possessions(possession_worksheet):
        possession = convert_possession(statsheet_possession)
        possessions.append(possession)
    
    return possessions

def verify_metadata_sheet(metadata_worksheet:Worksheet) :
    # TODO: This method will eventually contain the logic where all the IDs in the METADATA worksheet
    # (season id, tournament id, game id, team ids )
    # are checked and validated as existing in the database
    pass

def verify_roster_sheet (roster_worksheet: Worksheet):
    # TODO: This method will eventually contain the logic which will check if all the players in 
    # the ROSTER sheet are validated as existing in the database
    pass

def lambda_handler(event, context) -> dict:
    s3 = boto3.client('s3')
    bucket, obj = extract_first_file_from_event(event)
    response  = s3.get_object( Bucket= bucket, Key = obj)
    stream = BytesIO(response['Body'].read())
    wb = load_workbook(stream)
    ws_possessions, ws_roster, ws_metadata = extract_sheets(wb)
    possessions = process_possessions(ws_possessions)
    print(ws_roster)
    print(ws_metadata)
    return {
        'statusCode': 200,
        'body': MessageToJson(possessions[-1])
    }
