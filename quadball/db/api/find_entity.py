import pymongo
from quadball.schema.db.league_pb2 import *
from quadball.schema.db.season_pb2 import * 
from quadball.schema.db.tournament_pb2 import * 
from quadball.schema.db.team_pb2 import * 
from quadball.schema.db.player_pb2 import * 
from quadball.schema.db.game_pb2 import *
from google.protobuf.json_format import MessageToDict, ParseDict
from typing import Any

import bson

def replace_oid(message_dict:dict)-> dict: 
    message_dict['_id'] = str(message_dict['_id'])
    return message_dict

def find_league(league_collection:pymongo.collection.Collection,
                    league_id:str) -> League:
    find_condition = {'league_id':league_id}
    result = league_collection.find_one(find_condition)
    result = replace_oid(result)
    return ParseDict(result,League())

def find_season(season_collection:pymongo.collection.Collection,
                    season_id:str 
                    ) -> Season:
    find_condition = {'season_id':season_id}
    result = season_collection.find_one(find_condition)
    result = replace_oid(result)
    return ParseDict(result,Season())


def find_tournament(tournament_collection:pymongo.collection.Collection,
                    tournament_id:str 
                    ) -> Tournament:
    find_condition = {'_id':bson.ObjectId(tournament_id)}
    result = tournament_collection.find_one(find_condition)
    result = replace_oid(result)
    return ParseDict(result,Tournament())

def find_team(  team_collection:pymongo.collection.Collection,
                team_id:str ) -> Team:
    # Check if duplicate via secondary id (Team ID + LEAGUE ID )
    find_condition = {'_id':bson.ObjectId(team_id)}
    result = team_collection.find_one(find_condition)
    result = replace_oid(result)
    return ParseDict(result,Team())

def find_player(player_collection: pymongo.collection.Collection,
                   player_id:str) -> Player:
    # Check if duplicate via secondary id (Team ID + LEAGUE ID )
    find_condition = {'_id':bson.ObjectId(player_id)}
    result = player_collection.find_one(find_condition)
    result = replace_oid(result)
    return ParseDict(result,Player())

def find_game(game_collection: pymongo.collection.Collection,
                   game_id:str) -> Game:
    # Check if duplicate via secondary id (Team ID + LEAGUE ID )
    find_condition = {'_id':bson.ObjectId(game_id)}
    result = game_collection.find_one(find_condition)
    result = replace_oid(result)
    return ParseDict(result,Game())

def find(db:pymongo.database.Database ,obj_id:str, obj_type:str) -> Any:
    """
        register is the default function exposed to the outside API layer.

        db: DATABASE to enter the data into. By exposing only this via API it
        removes the risk of someone calling find_league e.g. with the season
        collection and a Tournament dict structure. 

        obj: The API layer will need to call register with json or parameter-like
        key-value pairs, as such we have obj - the json representation of the entity
        to enter

        obj_type: The API layer must specify the type of object we are registering
    """

    mapper = {
        'game':('games',find_game, Game),
        'league':('leagues',find_league, League), 
        'season':('seasons',find_season,Season),
        'tournament':('tournaments',find_tournament,Tournament),
        'team':('teams',find_team,Team),
        'player':('players',find_player,Player)
    }

    # This will get caught as a 400 error in the API layer. We want exceptions
    # being thrown if invalid API parameters are called 

    if obj_type not in mapper:
        raise Exception(f'Register called with invalid obj_type: {obj_type}')
    
    collection_name, func, proto_struct = mapper[obj_type]
    

    # We call the individual find_* functions using PARSED proto-objects
    # In this way we ensure schema validation when writing to our db
    return func(db[collection_name],obj_id)


def find_all(db:pymongo.database.Database, obj_type:str, ids_and_links_only = True) -> Any:
    """
        find_all takes a snapshot of the entire collection
    """

    mapper = {
        'game':('games',find_game, Game),
        'league':('leagues',find_league, League), 
        'season':('seasons',find_season,Season),
        'tournament':('tournaments',find_tournament,Tournament),
        'team':('teams',find_team,Team),
        'player':('players',find_player,Player)
    }

    # This will get caught as a 400 error in the API layer. We want exceptions
    # being thrown if invalid API parameters are called 

    if obj_type not in mapper:
        raise Exception(f'Register called with invalid obj_type: {obj_type}')
    
    collection_name, func, proto_struct = mapper[obj_type]
    

    # We call the individual find_* functions using PARSED proto-objects
    # In this way we ensure schema validation when writing to our db
    return func(db[collection_name],obj_id)