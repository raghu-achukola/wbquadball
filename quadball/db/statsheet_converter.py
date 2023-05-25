import quadball.schema.statsheet.statsheet_pb2  as raw
import quadball.schema.db.stats_pb2 as model
from typing import Tuple, Callable
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
    

def convert_single_extra(extra:str, offense:str, defense:str, lookup_id: Callable = lambda x,team_a: x)-> model.Extra:
    """
        Function that takes a single extra statsheet annotation and 
        converts it into our central data model concept of an Extra
        e.g
        YA23, 'A','B' -> Extra(ExtraType.Y,True,'23')
    """
    match = _regex_extra_match(extra)
    if not match: 
        raise Exception(f'Extra {extra} does not seem to be a valid extra {list(EXTRA_DICTIONARY.keys())}')
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
        model_extra.player_id = lookup_id(player,  (team == 'A'))
    return model_extra


    
def _convert_game_time(gametime_str:str) -> int:
    """
        Gametimes are annotated as the statsheet as MMSS for sake of expediency
        e.g 9 minutes, 23 seconds -> 0923. We need to convert this to actual number
        of seconds for Data Model Purposes

        TODO: some historical gametimes are annotated based on OT time in
        descending (e.g OT-0403 = 4:03 left in OT). This is meant to be a convenience
        as the statsheet is designed to be filled with information most convenient

        Future instances might process this annotation as well 
    """
    assert gametime_str.isnumeric() and len(gametime_str) == 4
    minutes, seconds = int(gametime_str[:2]), int(gametime_str[2:])
    return 60*minutes + seconds

        
def get_player_team_from_ssp(offense:str,result:str, position:int) -> str:
    """
        Arguments: 
        offense:        either 'A' or 'B' 
        result:         any acceptable Result
        position:       either 0, 1, 2, or 3 as described bloew

        Returns: 
        team:           either 'A' or 'B' (what team should be attached to the 
                        player at specified position # in the StatSheetPossession)

        Description: 
        For the sake of statsheet convenience, player teams are not included for results.
        The result informs the structure: 

        "TC | 51,23 | 34" is read:
        turnover forced by contact by DEFENSE #51 and #23 on OFFENSE #34 because
        that is the only sensible interpretation. We exclude A and B on the sheet 
        to facilitate live stat taking. 

        As such, in parsing this function based on the position of the player (0th, 1st, 2nd, 3rd)
        as below 

        TD | 51, 23 | 34, 51
        -    1    0    2   3        (yes, 1 then 0 | 2 then 3)
        GP | 23 | 56
        -    1    2
    """
    teams = ['A','B']
    defense = teams[offense == 'A']
    if position in (2,3):
        return offense
    elif result.endswith('CA'):
        return 'A'
    elif result.endswith('CB'):
        return 'B'
    elif result.startswith('T'):
        return defense
    return offense


#TODO: implement
def convert_possession(
        ss_possession: raw.StatSheetPossession,
        lookup_id : Callable = None) -> model.Possession:
    possession = model.Possession()
    """
        Arguments: 
        ss_possession:      a Raw StatSheetPosssession Object
        lookup_id:          a Callable that acts as a "Roster" object converting jersey numbers 
                            for both teams into player names or IDs
        
        Returns:
        possession:         the same possession written in the form of our Standard Data Model
    """

    if lookup_id is None: 
        lookup_id = lambda x, team_a : x
    # Standard is "Team 'A' wins", if statsheet is taken with "Team B" winning, we will write a 
    # reverse() function so "Team 'A' wins"
    teams = ['A','B']
    offense = ss_possession.offense
    defense = teams[offense == 'A']
    possession.winning_team_is_offense.CopyFrom(wrappers.BoolValue(value = (offense == 'A')))

    ## IF G then player 0,1,2,3 = offense
    ## IF E then player 0,1,2,3 = offense
    ## IF T then player 0,1 = defense, player 2,3 = offense


    ## Gametime at end
    if ss_possession.end_time and ss_possession.end_time.isnumeric():
        possession.gametime_at_end.CopyFrom(wrappers.UInt32Value(value = _convert_game_time(ss_possession.end_time)))

    ## If possession result
    if ss_possession.result: 
        possession.result = getattr(model.PossessionResult, ss_possession.result.upper(), model.POSSESSION_RESULT_UNKNOWN)

    # If extras -> split up each individual one, then pass to convert_single_extra
    if ss_possession.extras:
        extra_strings = ss_possession.extras.split(',')
        extra_list = [convert_single_extra(extra_str,offense,defense,lookup_id) for extra_str in extra_strings]
        possession.extras.extend(extra_list)

    # Given this current possession's offense and result, 
    # convert get_player_team_from_ssp (which needs offense, result and possession) to a simpler function
    # that focuses on the only variable input (possession) and returns True or False
    is_a = lambda position:  get_player_team_from_ssp(offense=offense, result=ss_possession.result, position = position)=='A'
    if ss_possession.primary: 
        # ',' in the cell means two players
        if ',' in ss_possession.primary:
            # Yes, in this order player 1, player 0 
            player_1, player_0 = ss_possession.primary.split(',')               # TODO: will throw error if person puts 3 players by mistake
            possession.player_0_id = lookup_id(player_0, is_a(0))
            possession.player_1_id = lookup_id(player_1, is_a(1))
        else: 
            possession.player_1_id = lookup_id(ss_possession.primary,is_a(1))

    if ss_possession.secondary: 
        if ',' in ss_possession.secondary:
            player_2, player_3 = ss_possession.secondary.split(',')
            possession.player_2_id = lookup_id(player_2, is_a(2))
            possession.player_3_id = lookup_id(player_3, is_a(3))
        else: 
            possession.player_2_id = lookup_id(ss_possession.secondary, is_a(2))
        
    return possession

