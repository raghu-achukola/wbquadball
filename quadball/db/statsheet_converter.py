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


    
    

        
#TODO: implement
def convert_possession(possession: raw.StatSheetPossession) -> model.Possession:
    pass

