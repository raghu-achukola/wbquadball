from quadball.schema.db.game_pb2 import *
from quadball.schema.db.season_pb2 import *
from quadball.schema.db.stats_pb2 import *
from typing import Iterable
from google.protobuf.wrappers_pb2 import UInt32Value
from quadball.db.rulesets import * 
from google.protobuf.json_format import MessageToDict


class GameParser:
    REVERSE_MAP = {
        RCA: RCB,
        RCB: RCA, 
        OCA:OCB, 
        OCB:OCA
    }
    def __init__(self, game_id:str, roster = None, ruleset:Ruleset = None, tournament_id = None) -> None:
        self.ruleset = ruleset if ruleset else RULESET_USQ_8_THRU_12 # This ruleset has the most games
        self.roster = roster
        self.possessions = []
        self.tournament_id = tournament_id
        #TODO: call out to get a game_id
        self.game_id = game_id
        
        self.game = Game(
            _id = str(self.game_id),
            winning_team_extras = '',
            losing_team_extras = '',
            tournament_id = str(self.tournament_id),
        )


    def populate_from_possessions(self, possessions:Iterable[Possession]) -> None:
        for i, possession in enumerate(possessions):
            possession.possession_number.CopyFrom(UInt32Value(value = i))
            possession.game_id = self.game_id
            self.process_possession(possession)

    def process_possession(self, possession: Possession):
        self.possessions.append(possession)
        # Goal
        if PossessionResult.Name( possession.result) [0] == 'G': 
            if possession.winning_team_is_offense.value:
                self.game.winning_team_score.value += self.ruleset.goal_value
            else:
                self.game.losing_team_score.value +=self.ruleset.goal_value
        # Ending Catch
        elif PossessionResult.Name( possession.result) in ('RCA','OCA','2CA'):
            self.game.winning_team_score.value += self.ruleset.catch_value
            self.game.winning_team_extras += '*'
        elif PossessionResult.Name( possession.result)  in ('RCB','OCB','2CB'):
            self.game.losing_team_score.value += self.ruleset.catch_value
            self.game.losing_team_extras += '*'
        # Own Goal
        elif PossessionResult.Name( possession.result)  == 'OG':
            if possession.winning_team_is_offense.value:
                self.game.losing_team_score.value += self.ruleset.goal_value
            else:
                self.game.winning_team_score.value +=self.ruleset.goal_value

        # Nonending Catch
        if possession.extras:
            for extra in possession.extras:
                if ExtraType.Name( extra.extra_type) == 'C':
                    # if ETIO == WTIO , ET = WT -> A catch
                    if extra.extra_team_is_offense.value == possession.winning_team_is_offense.value:
                        self.game.winning_team_score.value += self.ruleset.catch_value
                        self.game.winning_team_extras += '*'
                    else:
                        self.game.losing_team_score.value += self.ruleset.catch_value
                        self.game.losing_team_extras += '*'                        

    # We use reverse here because it alleviates the stress of handling/switching extras
    # Since extras are offense defense based, NOT 
    def reverse(self) ->  'GameParser':
        reversed = GameParser(game_id = self.game_id, ruleset = self.ruleset, tournament_id= self.tournament_id)
        reversed.game.CopyFrom(self.game)
        reversed.game.winning_team_score.value, reversed.game.losing_team_score.value  = (
           0,0
        )
        reversed.game.winning_team_id, reversed.game.losing_team_id = (
            self.game.losing_team_id, self.game.winning_team_id
        )
        for p in self.possessions:
            new_p = Possession()
            new_p.CopyFrom(p)
            new_p.result  = GameParser.REVERSE_MAP.get(new_p.result,new_p.result)
            reversed.process_possession(new_p)
        print(reversed.possessions)
        return reversed

    def __str__(self) -> str:
        return f"""Game Parser:
        \t game_id \t{self.game_id}
        \t roster \t{self.roster}
        \t ruleset \t{MessageToDict(self.ruleset)}
        \t tournament_id \t{self.tournament_id}
        """