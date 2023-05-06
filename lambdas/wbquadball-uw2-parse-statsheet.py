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

#Increment 19 ->  Multithread the API calls necessary here to increase speed
from concurrent.futures import ThreadPoolExecutor
import os
import requests
import urllib

"""
    This Lambda will have the following environment variables 

    API_ENDPOINT:    API endpoint that contains the roster lookup resource (among others)

"""



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
    API_ENDPOINT = os.environ['API_ENDPOINT']+'/roster-lookup?players={playerjson}'
    

    #Generate rosters
    a,b = zip(*[
        ((jersey.value,a_name.value),(jersey.value,b_name.value)) 
        for jersey,a_name,b_name in roster_worksheet['A2:C101']
        ]
    )
    a_players = {jersey:name.strip().upper() for jersey,name in a if name and name.strip()}
    b_players = {jersey:name.strip().upper() for jersey,name in b if name and name.strip()}

    # Define local function for multithreading
    def roster_api_call(roster):
        full_url = API_ENDPOINT.format(
            playerjson= urllib.parse.quote_plus(json.dumps(roster))
        )
        return requests.get(full_url)

    # Multithread the lookup
    with ThreadPoolExecutor(max_workers=2) as executor:
        response_a, response_b = executor.map(roster_api_call, [a_players,b_players])


    return response_a, response_b

def lambda_handler(event, context) -> dict:
    s3 = boto3.client('s3')
    bucket, obj = extract_first_file_from_event(event)
    response  = s3.get_object( Bucket= bucket, Key = obj)
    stream = BytesIO(response['Body'].read())
    wb = load_workbook(stream)
    ws_possessions, ws_roster, ws_metadata = extract_sheets(wb)
    possessions = process_possessions(ws_possessions)
    a_roster, b_roster = verify_roster_sheet(ws_roster)
    print(a_roster)
    print(b_roster)
    print(ws_metadata)
    return {
        'statusCode': 200,
        'body': MessageToJson(possessions[-1])
    }
