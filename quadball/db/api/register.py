import pymongo
from quadball.schema.db.league_pb2 import *
from quadball.schema.db.season_pb2 import * 
from quadball.schema.db.tournament_pb2 import * 
from quadball.schema.db.team_pb2 import * 
from quadball.schema.db.player_pb2 import * 
from quadball.schema.db.game_pb2 import *
from google.protobuf.json_format import MessageToDict, ParseDict
import bson

#TODO: Insert data integrity warning with seemingly duplicate insertions

def register_league(league_collection:pymongo.collection.Collection,
                    league:League) -> bson.ObjectId: 
    # Check if duplicate via secondary id
    duplicate_condition = {'league_id':league.league_id}
    if league_collection.count_documents(duplicate_condition):
        return None
    # If not duplicate, insert
    result = league_collection.insert_one(MessageToDict(league,preserving_proto_field_name= True))
    return result.inserted_id

def register_season(season_collection:pymongo.collection.Collection,
                    season:Season 
                    ) -> bson.ObjectId:
    # Check if duplicate via secondary id
    duplicate_condition = {'season_id':season.season_id}
    if season_collection.count_documents(duplicate_condition):
        return None
    # If not duplicate, insert
    result = season_collection.insert_one(MessageToDict(season,preserving_proto_field_name= True))
    return result.inserted_id

def register_tournament(tournament_collection:pymongo.collection.Collection,
                    tournament:Tournament 
                    ) -> bson.ObjectId:
    
    result = tournament_collection.insert_one(MessageToDict(tournament,preserving_proto_field_name= True))
    return result.inserted_id

def register_team(team_collection: pymongo.collection.Collection,
                   team:Team) -> bson.ObjectId:
    # Check if duplicate via secondary id (Team ID + LEAGUE ID )
    duplicate_condition = {'team_id':team.team_id,'league_id':team.league_id}
    if team_collection.count_documents(duplicate_condition):
        return None
    # If not duplicate, insert
    result = team_collection.insert_one(MessageToDict(team,preserving_proto_field_name= True))
    return result.inserted_id

def register_player(player_collection: pymongo.collection.Collection,
                   player:Player) -> bson.ObjectId:
    # Check if duplicate via secondary id
    # TODO: FIND BETTER DUPLICATE CONDITION FROM STUPID FIRST NAME + LAST NAME GOD
    duplicate_condition = {
        'player_first_name':player.player_first_name,
        'player_last_name':player.player_last_name
    }
    
    if player_collection.count_documents(duplicate_condition):
        return None
    # If not duplicate, insert    
    result = player_collection.insert_one(MessageToDict(player,preserving_proto_field_name= True))
    return result.inserted_id

def register_empty_game(game_collection: pymongo.collection.Collection, 
                        game: Game) -> bson.ObjectId:
    
    assert game.losing_team_score.value == 0 
    assert game.winning_team_score.value == 0 
    result = game_collection.insert_one(MessageToDict(game,preserving_proto_field_name= True))
    return result.inserted_id

def register(db:pymongo.database.Database ,obj:dict, obj_type:str) -> bson.ObjectId:
    """
        register is the default function exposed to the outside API layer.

        db: DATABASE to enter the data into. By exposing only this via API it
        removes the risk of someone calling register_league e.g. with the season
        collection and a Tournament dict structure. 

        obj: The API layer will need to call register with json or parameter-like
        key-value pairs, as such we have obj - the json representation of the entity
        to enter

        obj_type: The API layer must specify the type of object we are registering
    """

    mapper = {
        'empty_game':('games',register_empty_game, Game),
        'league':('leagues',register_league, League), 
        'season':('seasons',register_season,Season),
        'tournament':('tournaments',register_tournament,Tournament),
        'team':('teams',register_team,Team),
        'player':('players',register_player,Player)
    }

    # This will get caught as a 400 error in the API layer. We want exceptions
    # being thrown if invalid API parameters are called 

    if obj_type not in mapper:
        raise Exception(f'Register called with invalid obj_type: {obj_type}')
    
    collection_name, func, proto_struct = mapper[obj_type]

    # We call the individual register_* functions using PARSED proto-objects
    # In this way we ensure schema validation when writing to our db
    return func(db[collection_name], ParseDict(obj,proto_struct()))
