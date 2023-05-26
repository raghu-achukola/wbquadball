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
from google.protobuf.json_format import MessageToJson, ParseDict,MessageToDict
from quadball.schema.db.stats_pb2 import Possession
from quadball.schema.db.game_pb2 import Game

#Increment 19 ->  Multithread the API calls necessary here to increase speed
from concurrent.futures import ThreadPoolExecutor
import os
import requests
import urllib
# Increment 19 -> Actually parse game 
from quadball.db.game import GameParser
from quadball.schema.db.season_pb2 import Ruleset

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


def verify_metadata_sheet(metadata_worksheet:Worksheet)-> Tuple[dict,dict]:
    # TODO: This method will eventually contain the logic where all the IDs in the METADATA worksheet
    # (season id, tournament id, game id, team ids )
    # are checked and validated as existing in the database
    API_ENDPOINT = os.environ['API_ENDPOINT']+'/validate-game-metadata'

    api_parameters = {
        a.value.lower().replace(' ','_'):str(b.value)
        for a,b in metadata_worksheet['A1:B5']
    }
    film_sources = [link.value for row in metadata_worksheet['B6:E6'] for link in row]
    response = requests.get(API_ENDPOINT+'?'+'&'.join({f'{param}={param_value}' for param, param_value in api_parameters.items()}))
    assert response.status_code == 200, response.json()
    return response.json(), film_sources


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
        return requests.get(full_url).json()

    # Multithread the lookup
    with ThreadPoolExecutor(max_workers=2) as executor:
        response_a, response_b = executor.map(roster_api_call, [a_players,b_players])
        for resp in (response_a,response_b):
            assert not resp['response']['overmatched'] and not resp['response']['unmatched']


    return response_a,response_b


def reload(game:Game,possessions:list[Possession]):
    API_ENDPOINT = os.environ['API_ENDPOINT']+'/reload-game/{game_id}?game_template={game_template}'
    json_obj = [MessageToDict(p,preserving_proto_field_name=True) for p in possessions]
    game_template_json = urllib.parse.quote_plus(MessageToJson(game,preserving_proto_field_name=True))
    actual = API_ENDPOINT.format(game_id = game._id,game_template=game_template_json)
    return requests.put(actual,json=json_obj ).json()
    
def archive_statsheet(s3_client, source_bucket:str, source_key:str,destination_key:str):
    region = 'us-west-2'    #NOTE: does this need to be variable?
    destination_bucket = 'wbquadball-uw2-public-metadata-storage'
    s3_client.copy({'Bucket':source_bucket, 'Key':source_key},destination_bucket,destination_key)
    url = f"https://{destination_bucket}.s3.{region}.amazonaws.com/{destination_key}"
    return url


def lambda_handler(event, context) -> dict:
    s3 = boto3.client('s3')
    bucket, obj = extract_first_file_from_event(event)
    response  = s3.get_object( Bucket= bucket, Key = obj)
    stream = BytesIO(response['Body'].read())
    wb = load_workbook(stream)
    ws_possessions, ws_roster, ws_metadata = extract_sheets(wb)
    try:
        metadata, film_sources = verify_metadata_sheet(ws_metadata)
        assert  metadata.get('validation_stage') == 'Success'
    except AssertionError as e:
        print(e)
        return {}
    
    possessions = gen_statsheet_possessions(ws_possessions)
    # GameParser requires values of roster lookup dictionary to be STRINGS not LISTS
    a_roster, b_roster = [{k:v[0] for k,v in resp['response']['roster'].items()} for resp in verify_roster_sheet(ws_roster)]
    game_parser = GameParser(
        game_id = metadata['objects']['game']['_id']['$oid'],
        roster = {'A':a_roster,'B':b_roster},
        ruleset = ParseDict(metadata['objects']['ruleset'],Ruleset()),
        tournament_id= metadata['objects']['game']['tournament_id'],
        team_a_id= metadata['objects']['team_a']['_id']['$oid'],
        team_b_id=metadata['objects']['team_b']['_id']['$oid'],
    )
    stats_source = archive_statsheet(s3,bucket,obj,f"statsheets/{game_parser.game._id}.xlsx")
    game_parser.game.film_sources.extend(film_sources)
    game_parser.game.stats_source = stats_source
    game_parser.populate_from_possessions(game_parser.gen_possessions_from_statsheet(possessions))
    print(reload(game_parser.game,game_parser.possessions))

  
    
    # print(game_parser.possessions)
    # print(game_parser)
    # print(MessageToJson(game_parser.game))
    return {
        'statusCode': 200,
        'body': [MessageToJson(p,preserving_proto_field_name=True) for p in game_parser.possessions]
    }
