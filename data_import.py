import nfl_data_py as nfl
import pandas as pd

'''
['mfl_id', 'sportradar_id', 'fantasypros_id', 'gsis_id', 'pff_id',
       'sleeper_id', 'nfl_id', 'espn_id', 'yahoo_id', 'fleaflicker_id',
       'cbs_id', 'rotowire_id', 'rotoworld_id', 'ktc_id', 'pfr_id',
       'cfbref_id', 'stats_id', 'stats_global_id', 'fantasy_data_id',
       'swish_id', 'name', 'merge_name', 'position', 'team', 'birthdate',
       'age', 'draft_year', 'draft_round', 'draft_pick', 'draft_ovr',
       'twitter_username', 'height', 'weight', 'college', 'db_season']
'''
#player_col = ['name', 'position']
players = nfl.import_ids()

rb = players.loc[(players['position'] == 'RB')]

p2 = nfl.import_players()

print(p2.head(2))