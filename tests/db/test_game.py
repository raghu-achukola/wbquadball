from openpyxl import load_workbook
from quadball.db.game import * 
from quadball.schema.db.game_pb2 import * 
from quadball.db.rulesets import *
from quadball.db.statsheet_converter import convert_possession
from quadball.statsheet.parser import gen_statsheet_possessions
import os
import pytest
import json

relpath = lambda *paths: os.path.realpath(os.path.join(os.path.dirname(__file__),*paths))

GAME_RAW_PATH = relpath(
    '..','test_data','statsheet','TEXAS_LSQC.xlsx'
)


@pytest.fixture
def load_ut_lsqc():
    with open(GAME_RAW_PATH,'rb') as f: 
        return load_workbook(f).active
    
def test_full_game(load_ut_lsqc):
    g = GameParser(game_id = '1',ruleset = RULESET_USQ_8_THRU_12, tournament_id = '1')
    posslist = [convert_possession(sp) for   sp in gen_statsheet_possessions(load_ut_lsqc)]
    g.populate_from_possessions(posslist)
    assert g.game.winning_team_score.value == 120 and g.game.losing_team_score.value == 90 and g.game.winning_team_extras == '*'


def test_reverse(load_ut_lsqc):
    g = GameParser(game_id = '1',ruleset = RULESET_USQ_8_THRU_12, tournament_id = '1')
    posslist = [convert_possession(sp) for   sp in gen_statsheet_possessions(load_ut_lsqc)]
    g.populate_from_possessions(posslist)
    g = g.reverse()
    assert g.game.winning_team_score.value == 90 and g.game.losing_team_score.value == 120 and g.game.losing_team_extras == '*'

