import pymongo
from quadball.schema.db.league_pb2 import *
from quadball.schema.db.season_pb2 import * 
from quadball.schema.db.tournament_pb2 import * 
from quadball.schema.db.team_pb2 import * 
from quadball.schema.db.player_pb2 import * 
from quadball.schema.db.game_pb2 import *
from quadball.schema.db.stats_pb2 import * 
from quadball.db.game import GameParser
from quadball.db.api.find_entity import find
from google.protobuf.json_format import MessageToDict, ParseDict, ParseError
import bson
from typing import Iterable



def reload_possessions(db:pymongo.database.Database, game_id:str, possession_list:Iterable[Possession], ruleset: Ruleset = None, game_template: Game = None) -> dict:
    """
        input format: 

        game:           Data Model Game object 

        posession_list: json structure (list of dictionaries) that contain
                        a list of objects that can be converted into 
                        Possession type objects
        
        output format: 

        {
            stagesCompleted: 
                -- 0 if delete not successful and (therefore) insert not either
                -- 1 if delete successful but insert not (INTEGRITY ERROR)
                    TODO: modify? 
                -- 2 if everything successful
            errors: <dictionary of errors> 
                -- ParseError: [list of parse_errors]
            deleted: <list of [possibly] deleted documents> 
            inserted: <inserted list of possession ids>
        }

        Note the possibly, since delete does a find() on a query followed by
        a deleteMany(). If insertions/modifications happen between those two
        the result will be different
    """

    # STEP 1 Find Game
    # STEP 2 Find Tournament
    # STEP 3 Find Season
    game = find(db,game_id,'game')
    tournament = find(db,game.tournament_id,'tournament')
    ruleset = find(db,tournament.season_id,'season').ruleset

    # STEP 5 Create Game Parser: 
    game_parser = GameParser(
        game._id, roster = None, ruleset = ruleset,
        tournament_id = game.tournament_id, team_a_id = game.winning_team_id, 
        team_b_id= game.losing_team_id, film_links=list(game.film_sources)
    )
    if game_template is not None:
        game_parser.game.film_sources.extend(game_template.film_sources)
        game_parser.game.stats_source = game_template.stats_source
    game_parser.populate_from_possessions(possessions=possession_list)
    return game_parser.game, game_parser.possessions
    # stagesCompleted = 0
    # to_insert = []
    # deleted  = []
    # # inserted = []
    # # STEP 0, parse from scratch 
    # game_parser = GameParser(
    #     game_id = game._id,
    #     roster = None,
    #     ruleset = ruleset,
    #     tournament_id=  game.tournament_id,
    #     team_a_id= game.winning_team_id, 
    #     team_b_id  = game.losing_team_id,
    #     film_links= list(game.film_links)
    # )

    # # STEP 1, ensure that Request is correct

    # # If errors in parsing have occured, abort now, request is improper
    # # in API layer return 400 code to client.

    # if errors['ParseError']: 
    #     return {
    #         'stagesCompleted': 0,
    #         'errors':  errors,
    #         'deleted': [],
    #         'inserted': []
    #     }
    # for possession_dict in possession_list:
    #     try:
    #         possession = ParseDict(possession_dict,Possession())
    #         # Inc 16 - SET the game id, we can revisit whether
    #         #           this should be intended behavior or whether
    #         #           we should assert that the game_id is already equal
    #         #           or something
    #     except ParseError as pe:
    #         errors['ParseError'].append(pe)
    #         continue
    #     to_insert.append(MessageToDict(possession,preserving_proto_field_name= True))
    
    # # If errors in parsing have occured, abort now, request is improper
    # # in API layer return 400 code to client.

    # if errors['ParseError']: 
    #     return {
    #         'stagesCompleted': 0,
    #         'errors':  errors,
    #         'deleted': [],
    #         'inserted': []
    #     }
    
    # # Otherwise continue, next step deletion. 
    # collection = db['Possessions']
    # mongodb_condition = {'game_id': game._id}
    # try:
    #     find_result = collection.find(mongodb_condition)
    #     delete_result = collection.delete_many(mongodb_condition)
    #     deleted = delete_result
    # except Exception as e:
    #     errors['DeletionError'].append(e)
    #     return {
    #         'stagesCompleted': 0,
    #         'errors':  errors,
    #         'deleted': [], 
    #         'inserted': []
    #     }
    
    # # If no exception, next step insertion.
    # try:
    #     insert_result = collection.insert_many(to_insert)
    # except Exception as e: 
    #     errors['InsertError'].append(e)
    #     return {
    #         'stagesCompleted': 1,
    #         'errors':  errors,
    #         # Yes, find_result since delete_result does not have the actual docs
    #         'deleted': find_result, 
    #         'inserted': []
    #     }
    # return {
    #     'stagesCompleted': 2,
    #     'errors':  errors,
    #     # Yes, find_result since delete_result does not have the actual docs
    #     'deleted': find_result, 
    #     'inserted': to_insert
    # }