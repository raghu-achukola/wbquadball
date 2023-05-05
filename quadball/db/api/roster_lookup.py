import pymongo
from quadball.schema.db.league_pb2 import *
from quadball.schema.db.season_pb2 import * 
from quadball.schema.db.tournament_pb2 import * 
from quadball.schema.db.team_pb2 import * 
from quadball.schema.db.player_pb2 import * 
from quadball.schema.db.game_pb2 import *
from google.protobuf.json_format import MessageToDict, ParseDict
import bson


def roster_lookup(db: pymongo.database.Database, jersey_player_name_map:dict) -> dict:
    """
        roster_lookup is the default function exposed to the outside API layer.

        db: DATABASE to fetch the data from. By exposing only this via API it
        removes the risk of someone calling roster_lookup with the wrong collection

        jersey_player_name_map: A dictionary where the keys are the 

        OUTPUTS: 
        
        API response: 
        {
            "overmatched":  A list of keys (jersey numbers) where >1 result was found
            "matched":      A list of keys (jersey numbers)
            "unmatched":    A list of keys (jersey numbers)
            "roster":       A dictionary with the same keys as jersey_player_name_map
                            where the values are a LIST of matching ids
        }
    """
    player_coll = db['players']

    response = {
        'overmatched':[],
        'matched':[],
        'unmatched':[],
        'roster':{
        }
    }
    for jersey_num, player_name in jersey_player_name_map.items(): 
        # Names like Alex De Vries need to processed like: 
        # first_name = Alex, last_name = 'De Vries' 

        player_first_name, *l = player_name.split()
        player_last_name = ' '.join(l)
        find_condition = {
            'player_first_name':player_first_name.upper(),
            'player_last_name':player_last_name.upper()
        }
        matches = [
            str(result['_id']) 
            for result in player_coll.find(find_condition, {'_id':1}) # Return only ids
        ]

        response['roster'][jersey_num] = matches
        if len(matches) == 1: 
            response['matched'].append(jersey_num)
        elif len(matches) > 1:
            response['overmatched'].append(jersey_num)
        else:
            response['unmatched'].append(jersey_num)
        
    return response

        
