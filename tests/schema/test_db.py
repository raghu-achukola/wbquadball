
import json 
import os
from quadball.schema.db.stats_pb2 import * 
from quadball.schema.db.league_pb2 import *
from quadball.schema.db.season_pb2 import * 
from quadball.schema.db.team_pb2 import *
from quadball.schema.db.player_pb2 import *
from quadball.schema.db.tournament_pb2 import *  

from google.protobuf.json_format import ParseDict
import pytest

relpath = lambda *paths : os.path.relpath(
        os.path.join(
            os.path.dirname(__file__), *paths
        )
    )

POSSESSION_PATH = relpath(
        '..','test_data', 'schema','db','stats.json'
    )

SEASON_PATH = relpath(
        '..','test_data', 'schema','db','season.json'
    )

LEAGUE_PATH = relpath(
        '..','test_data', 'schema','db','league.json'
    )

TEAM_PATH = relpath(
        '..','test_data', 'schema','db','team.json'    
)
    
TOURNAMENT_PATH = relpath(
        '..','test_data', 'schema','db','tournament.json'    

)
    
PLAYER_PATH = relpath(
        '..','test_data', 'schema','db','player.json'    

)
@pytest.fixture
def load_possesions():
    with open(POSSESSION_PATH) as f: 
        return json.loads(f.read())

@pytest.fixture
def load_leagues():
    with open(LEAGUE_PATH) as f: 
        return json.loads(f.read())
    
@pytest.fixture
def load_seasons():
    with open(SEASON_PATH) as f: 
        return json.loads(f.read())
    
@pytest.fixture
def load_teams():
    with open(TEAM_PATH) as f: 
        return json.loads(f.read())
@pytest.fixture
def load_tournaments():
    with open(TOURNAMENT_PATH) as f: 
        return json.loads(f.read())
@pytest.fixture
def load_players():
    with open(PLAYER_PATH) as f: 
        return json.loads(f.read())

def test_db_possession(load_possesions):
    """
        Make a specific version -> eventually generalize. 
        We will have "test schema" by parsing all data 
        in schema/statsheet to Protobuf format
    """
    ssp = Possession()
    for i, obj in enumerate(load_possesions):
        try: 
            ParseDict(obj,ssp)
        except Exception as e: 
            assert False, f"Parse exception occured at index {i}: {e}"
    assert True
    
def test_db_league(load_leagues):
    """
        Make a specific version -> eventually generalize. 
        We will have "test schema" by parsing all data 
        in schema/statsheet to Protobuf format
    """ 
    
    for k, obj in load_leagues.items():
        league = League()
        try: 
            ParseDict(obj,league)
        except Exception as e: 
            assert False, f"Parse exception occured at key {k}: {e}"
    assert True
    
def test_db_season(load_seasons):
    """
        Make a specific version -> eventually generalize. 
        We will have "test schema" by parsing all data 
        in schema/statsheet to Protobuf format
    """ 
    
    for k, obj in load_seasons.items():
        season = Season()
        try: 
            ParseDict(obj,season)
        except Exception as e: 
            assert False, f"Parse exception occured at key {k}: {e}"
    assert True

def test_db_teams(load_teams):
    """
        Make a specific version -> eventually generalize. 
        We will have "test schema" by parsing all data 
        in schema/statsheet to Protobuf format
    """ 
    
    for k, obj in load_teams.items():
        team = Team()
        try: 
            ParseDict(obj,team)
        except Exception as e: 
            assert False, f"Parse exception occured at key {k}: {e}"
    assert True

def test_db_tournaments(load_tournaments):
    """
        Make a specific version -> eventually generalize. 
        We will have "test schema" by parsing all data 
        in schema/statsheet to Protobuf format
    """ 
    
    for k, obj in load_tournaments.items():
        tourney = Tournament()
        try: 
            ParseDict(obj,tourney)
        except Exception as e: 
            assert False, f"Parse exception occured at key {k}: {e}"
    assert True

def test_db_players(load_players):
    """
        Make a specific version -> eventually generalize. 
        We will have "test schema" by parsing all data 
        in schema/statsheet to Protobuf format
    """ 
    
    for k, obj in load_players.items():
        player = Player()
        try: 
            ParseDict(obj,player)
        except Exception as e: 
            assert False, f"Parse exception occured at key {k}: {e}"
    assert True
