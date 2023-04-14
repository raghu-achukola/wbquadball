import quadball.schema.statsheet.statsheet_pb2  as raw
import quadball.schema.db.stats_pb2 as model
from typing import Tuple
import re
from google.protobuf import wrappers_pb2 as wrappers

EXTRA_DICTIONARY = {
    name: ev_desc.number
    for name, ev_desc in model.ExtraType.DESCRIPTOR.values_by_name.items()
    if ev_desc.number != 0
}
EXTRA_REGEX_PATTERN = re.compile(
    '({})(A|B)?([A-z0-9]+)?'.format("|".join(EXTRA_DICTIONARY.keys())) 
)

def lookup_id(player_number:str, **kwargs): 
    # TODO: will eventually turn into a way to lookup player ids from 
    # ROSTERS but until then
    return player_number

def _regex_extra_match(extra_text:str)-> Tuple[str,str,str]:
    """
        Function that takes an individual 'extra' annotation
        and extracts (Extra Type, Team, Player)
    """
    if extra_text and extra_text[0].isnumeric():
        extra_text = '_'+ extra_text
    match = re.match(EXTRA_REGEX_PATTERN, extra_text.upper().strip())
    if not match: 
        return None
    else: 
        return match.groups()
    

def convert_single_extra(extra:str, offense:str, defense:str)-> model.Extra:
    """
        Function that takes a single extra statsheet annotation and 
        converts it into our central data model concept of an Extra
        e.g
        YA23, 'A','B' -> Extra(ExtraType.Y,True,'23')
    """
    match = _regex_extra_match(extra)
    if not match: 
        raise Exception()
    extra_type, team, player = match
    # Resets do not have team annotation as they can only be forced by one team
    # and unforced by one team
    if extra_type in ('R','RC'):
        team = defense
    elif extra_type in ('UR'):
        team = offense
    
    model_extra = model.Extra()
    # R -> model.ExtraType.R
    # ADSFA -> model.ExtraType.EXTRA_TYPE_UNKNOWN (should not happen bc of the regex structure)
    model_extra.extra_type = getattr(model.ExtraType,extra_type,model.EXTRA_TYPE_UNKOWN)
    # Some extras have no team (S)
    if team: 
        model_extra.extra_team_is_offense.CopyFrom( wrappers.BoolValue(value = (team == offense)))
    # Some extras have no player (S, TO)
    if player:
        model_extra.player_id = lookup_id(player)
    return model_extra


    
def _convert_game_time(gametime_str:str) -> int:
    assert gametime_str.isnumeric() and len(gametime_str) == 4
    minutes, seconds = int(gametime_str[:2]), int(gametime_str[2:])
    return 60*minutes + seconds

        
#TODO: implement
def convert_possession(ss_possession: raw.StatSheetPossession) -> model.Possession:
    possession = model.Possession()
    
    # Standard is "Team 'A' wins", if statsheet is taken with "Team B" winning, we will write a 
    # reverse() function so "Team 'A' wins"
    teams = ['A','B']
    offense = ss_possession.offense
    defense = teams[offense == 'A']
    possession.winning_team_is_offense.CopyFrom(wrappers.BoolValue(value = (offense == 'A')))

    ## Gametime at end
    if ss_possession.end_time and ss_possession.end_time.isnumeric():
        possession.gametime_at_end.CopyFrom(wrappers.UInt32Value(value = _convert_game_time(ss_possession.end_time)))

    ## If possession result
    if ss_possession.result: 
        possession.result = getattr(model.PossessionResult, ss_possession.result.upper(), model.POSSESSION_RESULT_UNKNOWN)

    # If extras -> split up each individual one, then pass to convert_single_extra
    if ss_possession.extras:
        extra_strings = ss_possession.extras.split(',')
        extra_list = [convert_single_extra(extra_str,offense,defense) for extra_str in extra_strings]
        possession.extras.extend(extra_list)

    if ss_possession.primary: 
        if ',' in ss_possession.primary:
            # Yes, in this order player 1, player 0 
            player_1, player_0 = ss_possession.primary.split(',')
            possession.player_0_id = lookup_id(player_0)
            possession.player_1_id = lookup_id(player_1)
        else: 
            possession.player_1_id = lookup_id(ss_possession.primary)

    if ss_possession.secondary: 
        if ',' in ss_possession.secondary:
            player_2, player_3 = ss_possession.secondary.split(',')
            possession.player_2_id = lookup_id(player_2)
            possession.player_3_id = lookup_id(player_3)
        else: 
            possession.player_2_id = lookup_id(ss_possession.secondary)
        
    return possession

