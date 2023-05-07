import pymongo
from quadball.schema.db.league_pb2 import *
from quadball.schema.db.season_pb2 import * 
from quadball.schema.db.tournament_pb2 import * 
from quadball.schema.db.team_pb2 import * 
from quadball.schema.db.player_pb2 import * 
from quadball.schema.db.game_pb2 import *
from google.protobuf.json_format import MessageToDict, ParseDict
import bson


def find_one(collection:pymongo.collection.Collection, find_condition:dict) -> dict:
    result = [obj for obj in collection.find(find_condition)]
    assert len(result) == 1, f'Could not find unique document in {collection}'
    return result[0]

def validate_game_metadata(db: pymongo.database.Database, game_id:str, tournament_id:str,
                  season_id:str, team_a_id:str, team_b_id:str) -> dict:
    """
        validate_game is the default function exposed to the outside API layer.

        db: DATABASE to fetch the data from. 

        game_id:        _id field of the Game collection that corresponds to this game
        tournament_id:  _id field of the Tournament collection that corresponds to
                        the tournament the Game belongs to 
        season_id:      season_id field of the Season collection that corresponds to the 
                        season of the tournament
        team_a_id:      _id field of the Team collection that corresponds to the winning 
                        team of this Game. Note, that since the games are registered empty
                        the order of which team is marked as "A"(winner) and "B" (loser) is
                        NOT validated at this point. When the game data gets rewritten 
                        eventually, the team_ids will switch as expected
        team_b_id:      _id field of the Team collection that corresponds to the losing team
                        of this Game (see description of team_a_id for more info)
        
        OUTPUTS
        Stage:          Stage of validations
                        None -              Initial stage
                        'Game' -            Game not successfully and uniquely identified
                        'Tournament' -      Tournament not correctly and uniquely identified
                        'Season' -          Season not correctly and uniquely identified 
                        'Ruleset' -         Season in question does not have a defined and valid ruleset
                        'Team'-             Teams were not correctly and uniquely identified (Complete)
                        'Success'-          Validation Successful

    """
    game_coll = db['games']
    tourney_coll = db['tournaments']
    team_coll = db['teams']
    season_coll = db['seasons']

    stage = None
    response = {
        'validation_stage':stage,
        'validation_error':None,
        'objects':{
            'game':None,
            'tournament':None,
            'season':None,
            'ruleset':None,
            'team_a':None,
            'team_b':None
        }
    }

    # VALIDATING game
   
    # GAME
    game = game_coll.find_one({'_id':bson.ObjectId(game_id)})
    response['validation_stage'] = 'Game'
    if game is None:
        response['validation_error'] = f"Could not find  {response['validation_stage']}: {game_id} "
        return response
    response['objects']['game'] = game 

    # TOURNAMENT
    response['validation_stage'] = 'Tournament'
    game_tournament_id = game.get('tournament_id',None)
    if str(game_tournament_id) != tournament_id: 
        response['validation_error'] = f'Tournament ID mismatch between given {tournament_id} and tournament tied to game {game_tournament_id}'
        return response
    tournament = tourney_coll.find_one({'_id':bson.ObjectId(tournament_id)})
    if tournament is None:        
        response['validation_error'] = f"Could not find  {response['validation_stage']}: {tournament_id} "
        return response
    response['objects']['tournament'] = tournament 
    # SEASON
    response['validation_stage'] = 'Season'
    tournament_season_id = tournament.get('season_id')
    if str(tournament_season_id) != season_id: 
        response['validation_error'] = f'Season ID mismatch between given {season_id} and season tied to tournament {tournament_season_id}'
        return response
    season = season_coll.find_one({'season_id':season_id})
    if season is None:        
        season['validation_error'] = f'Tournament ID mismatch between given {tournament_id} and tournament tied to game {game_tournament_id}'
        return response
    response['objects']['season'] = season 
    # RULESET
    response['validation_stage'] = 'Ruleset'
    ruleset = season.get('ruleset',{})
    if not ruleset:
        response['validation_error'] = 'Season given does not have an associated ruleset'
        return response
    response['objects']['ruleset'] = ruleset

    game_team_a_id = str(game.get('winning_team_id'))
    game_team_b_id = str(game.get('losing_team_id'))
    response['validation_stage'] = 'Team'
    if set([team_a_id,team_b_id]) != set([game_team_a_id,game_team_b_id]):
        response['validation_error'] = f'Team ID mismatch between given {set([team_a_id,team_b_id])} and teams tied to game { set([game_team_a_id,game_team_b_id])}'
        return response
    
    team_a = team_coll.find_one({'_id':bson.ObjectId(team_a_id)})
    team_b = team_coll.find_one({'_id':bson.ObjectId(team_b_id)})

    if team_a is None:
        response['validation_error'] = f'Could not find Team A ID {team_a_id}'
        return response
    response['objects']['team_a'] = team_a
    if team_b is None:
        response['validation_error'] = f'Could not find Team B ID {team_b_id}'
        return response
    response['objects']['team_b'] = team_b
    response['validation_stage'] = 'Success'
    return response
    

