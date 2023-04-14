from quadball.schema.db.game_pb2 import Ruleset,EndGame

RULESET_USQ_8_THRU_12 = Ruleset(
    goal_value = 10, 
    floor_minutes = 18,
    catch_value  = 30,
    endgame = EndGame.END_GAME_CATCH
)

RULESET_USQ_13 = Ruleset(
    goal_value = 10, 
    floor_minutes = 20,
    catch_value  = 30,
    endgame = EndGame.END_GAME_CATCH
)

RULESET_USQ_2023 = Ruleset(
    goal_value = 10, 
    floor_minutes = 20,
    catch_value  = 35,
    endgame = EndGame.END_GAME_SCORE,
    endgame_target = 60
)
