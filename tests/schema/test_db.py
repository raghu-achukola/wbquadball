
import json 
import os
from quadball.schema.db.stats_pb2 import * 
from quadball.schema.db.season_pb2 import * 

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
    
@pytest.fixture
def load_possesions():
    with open(POSSESSION_PATH) as f: 
        return json.loads(f.read())
    
@pytest.fixture
def load_seasons():
    with open(SEASON_PATH) as f: 
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
   