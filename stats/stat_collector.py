import sqlite3

from nba_api.stats.library import data
from nba_api.stats.endpoints import playerprofilev2, commonteamroster
from nba_api.stats.static import teams

import pandas as pd

import os

#  #
def get_basic_player_df():
    '''
    Gets (id, last name, first name, full name, activity)
    '''

    if os.path.isfile('./CSVs/basic_player_data.csv') == True:
        pass
    else:
        basic_player_df = pd.DataFrame(data.players)   
        basic_player_df.columns = ['ids', 'last_name', 'first_name', 'full_name', 'is_active']
        basic_player_df.to_csv('./CSVs/basic_player_data.csv', index=False)

