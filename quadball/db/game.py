from quadball.schema.db.game_pb2 import *
from quadball.schema.db.season_pb2 import *
from quadball.schema.db.stats_pb2 import *
from typing import Iterable
from google.protobuf.wrappers_pb2 import UInt32Value
from quadball.db.rulesets import * 
from google.protobuf.json_format import MessageToDict
from quadball.statsheet.parser import * 
from quadball.db.statsheet_converter import convert_possession


class GameParser:
    REVERSE_MAP = {
        RCA: RCB,
        RCB: RCA, 
        OCA:OCB, 
        OCB:OCA
    }
    def __init__(self, game_id:str, roster:dict = {}, ruleset:Ruleset = None, 
                 tournament_id:str = None, team_a_id:str = None, team_b_id:str = None,
                 film_links:list =[]) -> None:
        self.ruleset = ruleset if ruleset else RULESET_USQ_8_THRU_12 # This ruleset has the most games
        self.roster = roster
        
        self.player_lookup = lambda jersey_number, team_a: roster.get(
            'A' if team_a else 'B',
            {}
        ).get(
            str(jersey_number),
            f"{team_a_id if team_a else team_b_id}-{jersey_number}"
        )

        self.possessions = []
        self.team_a_id = team_a_id
        self.team_b_id = team_b_id
        self.tournament_id = tournament_id
        #TODO: call out to get a game_id
        self.game_id = game_id
        self.film_links = film_links
        
        self.game = Game(
            _id = str(self.game_id),
            winning_team_id = self.team_a_id,
            winning_team_extras = '',
            losing_team_extras = '',
            losing_team_id = self.team_b_id,
            tournament_id = str(self.tournament_id),
        )
        self.game.film_sources.extend(film_links)


    def gen_possessions_from_statsheet(self, possessions:Iterable[StatSheetPossession]) -> Generator[Possession,None,None]:
        for possession in possessions:
            yield convert_possession(possession,self.player_lookup)
            
    def populate_from_possessions(self, possessions:Iterable[Possession]) -> None:
        for i, possession in enumerate(possessions):
            possession.possession_number.CopyFrom(UInt32Value(value = i+1))
            possession.game_id = self.game_id
            possession.stats_source = self.game.stats_source
            self.process_possession(possession)

    def process_possession(self, possession: Possession):
        """
            Advance the Game parser by the possession supplied,
            running score, extras, etc will increment based on value of possession
        """
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
        """
            self.reverse() creates a GameParser Object with team_a and team_b switched. 
            This is to handle the future case of a live-taken statsheet needing to be processed
            where team_a ended up losing. 

            Remember that Team A is always taken as the winning team to simplify things. Therefore
            we need the functionality to reverse() a GameParser object
        """
        reversed = GameParser(
            game_id = self.game_id,
            roster = {'A':self.roster.get('B',{}), 'B':self.roster.get('A',{})},
            ruleset = self.ruleset,
            tournament_id= self.tournament_id,
            team_a_id = self.team_b_id, 
            team_b_id = self.team_a_id
        )
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