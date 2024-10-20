import sqlite3

from nba_api.stats.library import data
from nba_api.stats.endpoints import playerprofilev2, commonteamroster
from nba_api.stats.static import teams

import pandas as pd

import os


def create_basic_player_data_csv():
    # Does file exist?
    if os.path.isfile('./stats/CSVs/basic_player_data.csv') == True:
        pass
    else:                     # Create file
        basic_player_df = pd.DataFrame(data.players)   
        basic_player_df.columns = ['ids', 'last_name', 'first_name', 'full_name', 'is_active']
        basic_player_df.to_csv('./stats/CSVs/basic_player_data.csv', index=False)


def get_basic_player_df():
    '''
    Gets (id, last name, first name, full name, activity)
    '''
    create_basic_player_data_csv()

    df = pd.read_csv('./stats/CSVs/basic_player_data.csv')

    return df


#def update_basic_player_df():
#    location = './stats/CSVs/basic_player_data.csv'
#    
#    basic_player_df = pd.DataFrame(data.players)
#    basic_player_df.columns = ['ids', 'last_name', 'first_name', 'full_name', 'is_active']
#
#    basic_player_df.to_csv(location, index=False)


def create_basic_teams_csv():
    if os.path.isfile('./stats/CSVs/basic_teams.csv') == True:
        pass
    else:
        basic_teams_df = pd.DataFrame(teams.get_teams())    
        basic_teams_df.to_csv('./stats/CSVs/basic_teams.csv', index=False)


def get_teams_df():
    create_basic_teams_csv()
    
    df = pd.read_csv('./stats/CSVs/basic_teams.csv')
    
    return df


def create_player_profile_csv(player_id):
    if os.path.isfile(f'./stats/CSVs/playerprofiles/{player_id}.csv') == True:
        pass
    else:
        try:
            player_profile_df = pd.DataFrame(playerprofilev2.PlayerProfileV2(player_id=player_id).get_data_frames()[0])
            player_profile_df.to_csv(f'./stats/CSVs/playerprofiles/{player_id}.csv')
        except:
            print(player_profilev2.PlayerProfile(player_id=player_id))
            return Exception

    
def get_player_profile_df(player_id):
    create_player_profile_csv(player_id)

    df = pd.read_csv(f'./stats/CSVs/playerprofiles/{player_id}.csv')

    return df












































